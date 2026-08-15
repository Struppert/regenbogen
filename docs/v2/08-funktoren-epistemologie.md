# Funktoren als Struktur-Erhaltung

**Zielgruppe:** Architekten, Checker-Implementierer  
**Zweck:** Formales Modell für "Ist der Code korrekt?"

---

## Das Modell: Drei Kategorien

Ein Funktor ist eine **Abbildung zwischen Kategorien, die Struktur erhält**.

**Drei Kategorien in unserem System:**

```
Glossar-Kategorie G
  Objekte: Glossar-Begriffe
  Pfeile: Abhängigkeiten (A → B bedeutet "A hängt von B ab")

Code-Kategorie K
  Objekte: Code-Symbole
  Pfeile: Imports/Calls

Validierungs-Kategorie V
  Objekte: Test-Oracles
  Pfeile: Test-Abhängigkeiten
```

---

## Der Funktor F: Glossar → Code

**Definition:** Ein Funktor F bildet Glossar auf Code ab und **erhält die Pfeile**.

```
Wenn A → B im Glossar (A hängt von B ab)
Dann F(A) → F(B) im Code (der Code von A importiert den Code von B)
```

**Beispiel:**

```
Glossar:           RegenbogenWahrscheinlichkeit → Wetterzustand

F (Glossar→Code):
  F(RegenbogenWahrscheinlichkeit) = class RainbowProbability
  F(Wetterzustand) = class Weather
  F(→) = imports

Code:              class RainbowProbability imports Weather
```

**Was bedeutet das:** Wenn ein Glossar-Pfeil existiert, muss der entsprechende Code-Pfeil existieren. Das ist nicht optional.

---

## Der Funktor T: Code → Tests

**Definition:** Ein Funktor T bildet Code auf Tests ab und erhält die Struktur.

```
T(RainbowProbability) = oracle_rainbow_probability
T(Weather) = oracle_weather

Wenn RainbowProbability → Weather im Code
Dann oracle_rainbow_probability → oracle_weather in Tests
  (Der Test für Rainbow kann nicht bestanden sein, wenn Weather-Test fehlschlägt)
```

---

## Die Komposition T ∘ F: Glossar → Tests

```
Glossar-Begriff X
  ↓ Funktor F
Code-Symbol F(X)
  ↓ Funktor T
Test T(F(X))
```

**Das bedeutet:** Ein Glossar-Begriff kann direkt durch seinen Test validiert werden.

**Wichtig:** Wenn F und T beide Struktur erhalten, dann auch die Komposition. Das folgt aus der Definition von Funktor — es ist nicht neu, aber es ist verlässlich.

---

## Was "Struktur-Erhaltung" in der Praxis bedeutet

### Falsch (Struktur verletzt):

```python
# Glossar sagt: RegenbogenWahrscheinlichkeit → Wetterzustand

class RainbowProbability(int):
    def __init__(self, wetter: WeatherState):
        pass  # Wetter wird nicht gespeichert oder genutzt
              # Pfeil ist "gelogen" — Code respektiert ihn nicht
```

### Richtig (Struktur erhalten):

```python
# Glossar sagt: RegenbogenWahrscheinlichkeit → Wetterzustand

class RainbowProbability:
    def __init__(self, weather: Weather):  # ← Abhängigkeit explizit
        self.weather = weather
        self.probability = self._calculate()  # Wetter wird wirklich genutzt
```

---

## Der Checker: PF-FUNKTOR

Das Werkzeug, das Struktur-Erhaltung prüft:

```python
def check_funktor_structure(glossar_term: str, code_symbol: str):
    """
    Prüfe: Sind alle Glossar-Pfeile im Code erhalten?
    """
    
    # Schritt 1: Hat der Code-Symbol die Glossar-Pfeile?
    glossar_deps = get_glossar_morphisms(glossar_term)
    code_deps = get_code_imports(code_symbol)
    
    for dep in glossar_deps:
        expected_code_dep = apply_funktor_mapping(dep)
        if expected_code_dep not in code_deps:
            return FAIL(f"Missing: {glossar_term} should import {dep}")
    
    # Schritt 2: Sind transitive Abhängigkeiten auch erhalten?
    glossar_transitive = compute_transitive_closure(glossar_term)
    code_transitive = compute_transitive_closure(code_symbol)
    
    for trans_dep in glossar_transitive:
        expected_trans = apply_funktor_mapping(trans_dep)
        if not has_transitive_path(code_symbol, expected_trans):
            return FAIL(f"Composition broken: {glossar_term} ⇒ {trans_dep} not in code")
    
    # Schritt 3: Gibt es Code-Importe ohne Glossar-Grund?
    extra_imports = code_deps - set(apply_funktor_mapping(d) for d in glossar_deps)
    if extra_imports:
        return WARN(f"Extra imports (not in glossar): {extra_imports}")
    
    return PASS("Funktor F respektiert Struktur")
```

**Das ist alles, was der Checker tut:** Abhängigkeiten zählen. Keine mathematischen Beweise, nur strukturelle Konsistenz-Prüfung.

---

## Wann funktioniert das System nicht?

Das System funktioniert **nur**, wenn:

1. **Glossar ist explizit** — Morphismen sind dokumentiert
2. **Code respektiert Glossar** — Pfeile sind als Imports/Calls sichtbar
3. **Tests sind strukturell gebunden** — @pytest.mark.oracle zeigt, welcher Test welchen Code validiert
4. **Checker laufen** — automatisch vor Commit

Fehlt eine dieser Bedingungen, funktioniert's nicht. Das ist nicht mathematisches Elegant, sondern praktische Notwendigkeit.

---

## Zusammenfassung

Ein Funktor sagt: "Wenn A von B abhängt (Glossar), dann muss F(A) von F(B) abhängen (Code)."

Das ist nicht kompliziert. Es ist einfach: **Pfeile bleiben Pfeile.**

Der Checker prüft das. Das war's.

---

**Erstellt:** 2026-08-15  
**Version:** 0.2 (gekürzt: nur Struktur-Erhaltung + Checker, keine Theorem-Sprache)
