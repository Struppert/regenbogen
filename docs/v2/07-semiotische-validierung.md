# Semiotische Validierung: Peirces Zeichentheorie in der Praxis

**Zielgruppe:** Agenten, Test-Designer, Validierungs-Architekten  
**Zweck:** Praktisches Framework für "Was macht einen Test zu einem echten Oracle?"

---

## Problem: Wie wissen wir, dass ein Test wirklich validiert?

Klassisches Dilemma:

```
Code: def calculate_rainbow_probability(...) -> float

Test 1:
  assert isinstance(result, float)  # Prüft nur Typ, nicht Logik
  
Test 2:
  assert 0 <= result <= 1  # Prüft nur Bereichs-Invariante
  
Test 3:
  assert probability == 0.42 if conditions == "test_case_X"
  # Prüft Verhalten, aber nur für eine Bedingung

Frage: Welcher Test ist "richtig"?
```

**Antwort:** Keiner allein. Ein vollständiger Test braucht **alle drei Ebenen der Peirce-Semiotik**.

---

## 1. Peirce's Zeichendreieck

### Die Klassische Definition (1906)

**Charles Sanders Peirce** definiert ein Zeichen durch drei Komponenten:

```
           Interpretant (Bedeutungsinhalt)
                   /\
                  /  \
                 /    \
            Sign _______ Objekt
         (Zeichen)   (Referent)
```

Beispiel: Das Wort "Regenbogen"

```
Sign (Zeichen):      Das Wort "Regenbogen" (Phonem, Graphem)
Object (Referent):   Das physikalische Phänomen (Licht in Wassertropfen)
Interpretant:        Die Bedeutung im Kopf (konzeptuelles Verstehen)
```

### Drei semiotische Typen

**Peirce unterscheidet drei Typen:**

| Typ | Definition | Beispiel |
|-----|---|---|
| **Ikon** | Zeichen ähnelt Objekt | Fotografie ähnelt Person |
| **Index** | Zeichen wirkt direkt auf Objekt | Rauch zeigt auf Feuer (kausal) |
| **Symbol** | Zeichen bezieht sich auf Objekt durch Konvention | Wort "Baum" = Baum (willkürlich) |

---

## 2. Übertragung auf Code: Sign-Object-Interpretant

### Was ist ein Glossar-Begriff als Zeichen?

Ein Glossar-Begriff ist ein **komplexes Zeichen** mit drei Ebenen:

```
GLOSSAR-BEGRIFF: RegenbogenWahrscheinlichkeit

Sign (Zeichen):           Das Wort "RegenbogenWahrscheinlichkeit"
                         (die Schreibweise im Glossar)

Object (Referent):        Der Regenbogen-Entstehungsprozess in der Physik
                         (Was existiert wirklich?)

Interpretant:            Die Bedeutung in unserem Projekt:
                         "Die mathematische Wahrscheinlichkeit, dass unter
                          gegebenen Bedingungen ein Regenbogen sichtbar ist"
```

### Was ist Code als Zeichen?

Der Code ist ein **Abbildung desselben Zeichendreiecks**:

```
CODE-SYMBOL: class RainbowProbability

Sign (Zeichen):           Der Klassname "RainbowProbability"
                         (syntaktisches Zeichen)

Object (Referent):        Der Regenbogen-Entstehungsprozess
                         (GLEICH wie im Glossar!)

Interpretant:            Die Implementierung:
                         def probability(humidity, angle): ...
                         (die Bedeutung in Funktionen und Datenstrukturen)
```

**Kritisch:** Object sollte **identisch** sein. Wenn Glossar und Code unterschiedliche Referenten haben, ist das System inkonsistent.

---

## 3. Ikonische Validierung (Form-Ähnlichkeit)

### Was heißt "ikonisch"?

Ein **ikonisches Zeichen** ähnelt seinem Referent in der Form.

**Beispiele:**
- Eine Karte ähnelt dem Gebiet (räumliche Form)
- Ein Schaltplan ähnelt der Schaltung (strukturelle Form)
- Ein Organigramm ähnelt der Organisationsstruktur (Hierarchie)

### Ikonische Validierung in Tests

Ein Test **ikonisch validiert**, wenn seine Form der Glossar-Definition ähnelt.

**Beispiel: Definition**

```
Glossar:
  RegenbogenWahrscheinlichkeit: Float, Bereich [0, 1], 
                                abhängig von (Luftfeuchte, Winkel)
```

**Ikonischer Test (gut):**

```python
@pytest.mark.oracle("glossar.RegenbogenWahrscheinlichkeit.ikonisch")
def test_rainbow_probability_form():
    # Form ähnelt Definition:
    # - Input: (humidity, angle) wie Glossar sagt
    # - Output: float wie Glossar sagt
    # - Range: [0, 1] wie Glossar sagt
    
    result = calculate_rainbow_probability(
        humidity=0.8,    # Input 1
        angle=45.0       # Input 2
    )
    
    assert isinstance(result, float)      # Form: ist ein float
    assert 0.0 <= result <= 1.0           # Form: Bereich
    assert len(inspect.signature(...).parameters) == 2  # Form: zwei Parameter
```

**Nicht-ikonischer Test (schlecht):**

```python
def test_magic_number():
    result = calculate_rainbow_probability(0.8, 45)
    assert result == 0.42  # Wo kommt 0.42 her? Nicht aus Glossar.
                           # Keine Form-Ähnlichkeit.
```

### Ikonische Regel

> Ein Test ist ikonisch, wenn die Teststruktur die Glossar-Struktur spiegelt.
> Wenn Glossar sagt "hat 3 Invarianten", sollte der Test mindestens 3 Assertions haben.

---

## 4. Indexikalische Validierung (Kausal-Wirksam)

### Was heißt "indexikalisch"?

Ein **indexikalisches Zeichen** wirkt direkt kausal auf seinen Referent.

**Beispiele:**
- Rauch ist ein Index für Feuer (verursacht durch Feuer)
- Fieber ist ein Index für Krankheit (direkt kausal)
- Eine Signalfahne ist ein Index für Eisenbahn (direkt wirksam)

**Kern:** Das Zeichen ist **nicht willkürlich** — es ist **durch Ursache gebunden**.

### Indexikalische Validierung in Tests

Ein Test **indexikalisch validiert**, wenn das Test-Resultat **das System wirksam verändert oder prüft**.

**Beispiel: Indexikalischer Test**

```python
@pytest.mark.oracle("glossar.RegenbogenWahrscheinlichkeit.indexikalisch")
def test_rainbow_probability_causal():
    # Dieser Test prüft nicht nur Struktur, sondern Kausalität.
    
    # Glossar sagt: "Wahrscheinlichkeit WÄCHST mit Luftfeuchte"
    # → Das ist eine kausale Behauptung
    
    p1 = calculate_rainbow_probability(humidity=0.5, angle=45)
    p2 = calculate_rainbow_probability(humidity=0.9, angle=45)
    
    # Indexikalische Assertion: Die Kausalität ist wirksam
    assert p2 > p1, "Higher humidity must cause higher probability"
                    # DIREKTE KAUSALITÄT PRÜFEN
    
    # Nicht nur "beide sind float", sondern "die Funktion wirkt
    # in der physikalisch erwarteten Richtung"
```

**Nicht-indexikalischer Test (schlecht):**

```python
def test_probabilities_are_numbers():
    p1 = calculate_rainbow_probability(0.5, 45)
    p2 = calculate_rainbow_probability(0.9, 45)
    
    assert isinstance(p1, float)  # Form, nicht Kausalität
    assert isinstance(p2, float)  # Form, nicht Kausalität
                                   # Keine Index-Wirkung geprüft
```

### Indexikalische Regel

> Ein Test ist indexikalisch, wenn er die **direkten Ursache-Wirkungs-Beziehungen** aus dem Glossar prüft.
> Wenn Glossar sagt "A verursacht Erhöhung von B", der Test muss diese Kausalität beobachten.

---

## 5. Symbolische Validierung (Konventions-Gebunden)

### Was heißt "symbolisch"?

Ein **symbolisches Zeichen** bezieht sich auf seinen Referent durch **gesellschaftliche Konvention**, nicht durch Form oder Kausalität.

**Beispiele:**
- Worte in einer Sprache (Deutsch, Englisch)
- Flaggen (rot = Gefahr, per Konvention)
- Noten in Musik (G-Schlüssel = bestimmte Tonhöhe, per Konvention)

**Kern:** Das Zeichen ist **willkürlich gewählt**, aber **projektintern obligatorisch**.

### Symbolische Validierung in Tests

Ein Test **symbolisch validiert**, wenn er die **projektinterne Konvention** prüft.

**Beispiel: Symbolischer Test**

```python
@pytest.mark.oracle("glossar.RegenbogenWahrscheinlichkeit.symbolisch")
def test_rainbow_probability_convention():
    # Glossar definiert Konvention:
    # "Regenbogen kann nur entstehen, wenn beide Bedingungen erfüllt:"
    #   1. Wassertropfen vorhanden (Luftfeuchte > 0)
    #   2. Lichteintritt möglich (Winkel richtig)
    
    # Konvention A: Wenn keine Feuchte, Wahrscheinlichkeit = 0
    result_no_moisture = calculate_rainbow_probability(
        humidity=0.0,  # Konvention: 0 = keine Feuchte
        angle=45
    )
    assert result_no_moisture == 0, "Project convention: No moisture → probability 0"
    
    # Konvention B: Negativ impossible
    result_any = calculate_rainbow_probability(0.5, 45)
    assert result_any >= 0, "Project convention: Probabilities are non-negative"
    
    # Konvention C: In unserem Projekt ist 1.0 = mathematische Sicherheit
    result_maximum = calculate_rainbow_probability(1.0, 45)  # Maximum moisture
    assert result_maximum <= 1.0, "Project convention: Probability ≤ 1.0"
```

**Nicht-symbolischer Test (schlecht):**

```python
def test_returns_something():
    result = calculate_rainbow_probability(0.5, 45)
    assert result is not None  # Keine Konvention
```

### Symbolische Regel

> Ein Test ist symbolisch, wenn er die **projektinterne Konvention und Normen** prüft.
> Diese sind die "Spielregeln" des Projekts.

---

## 6. Die Validierungs-Pyramide

### Drei Ebenen, eine Struktur

```
           ╔═══════════════════════╗
           ║    Symbolisch         ║  Was ist Konvention im Projekt?
           ║  (Normen, Regeln)     ║  Prüft: assert 0 <= p <= 1
           ╚═══════════════════════╝
                      ▲
                      │
           ╔═══════════════════════╗
           ║    Indexikalisch      ║  Was verursacht was?
           ║  (Kausalität, Wirkung)║  Prüft: higher humidity → higher p
           ╚═══════════════════════╝
                      ▲
                      │
           ╔═══════════════════════╗
           ║      Ikonisch         ║  Ähnelt die Form der Definition?
           ║   (Struktur, Form)    ║  Prüft: isinstance(p, float), 2 params
           ╚═══════════════════════╝
```

**Ein vollständiger Test braucht alle drei Ebenen.**

### Beispiel: Kompletter Oracle-Test

```python
@pytest.mark.oracle("glossar.RegenbogenWahrscheinlichkeit")
def test_rainbow_probability_complete():
    """
    Peirce-Semiotik: Ikonisch + Indexikalisch + Symbolisch
    """
    
    # IKONISCH: Ähnelt die Form der Glossar-Definition?
    sig = inspect.signature(calculate_rainbow_probability)
    assert len(sig.parameters) == 2, "Icon: 2 parameters as defined"
    
    p = calculate_rainbow_probability(humidity=0.8, angle=45)
    assert isinstance(p, float), "Icon: Returns float"
    
    # INDEXIKALISCH: Was ist die Kausalität?
    p_low_humidity = calculate_rainbow_probability(humidity=0.3, angle=45)
    p_high_humidity = calculate_rainbow_probability(humidity=0.9, angle=45)
    assert p_high_humidity > p_low_humidity, "Index: Higher humidity causes higher probability"
    
    p_optimal_angle = calculate_rainbow_probability(humidity=0.8, angle=42)
    p_suboptimal_angle = calculate_rainbow_probability(humidity=0.8, angle=20)
    assert p_optimal_angle >= p_suboptimal_angle, "Index: Better angle causes higher probability"
    
    # SYMBOLISCH: Was sind die Konventionen?
    p_no_moisture = calculate_rainbow_probability(humidity=0.0, angle=45)
    assert p_no_moisture == 0, "Symbol: Convention in project = no moisture → zero probability"
    
    p_any = calculate_rainbow_probability(humidity=0.5, angle=45)
    assert 0 <= p_any <= 1, "Symbol: Convention = probability in [0,1]"
    
    print("✓ Oracle test passed: Ikonisch + Indexikalisch + Symbolisch validated")
```

---

## 7. Anti-Pattern: Validierung ohne Semiotik

### Was Agenten oft tun (falsch)

```python
# FALSCH: Nur Type-Checks
def test_simple():
    result = calculate_rainbow_probability(0.8, 45)
    assert result is not None
    assert isinstance(result, float)
```

**Problem:** Prüft nur das **Zeichen (Sign)**, nicht den **Referent (Object)** oder die **Bedeutung (Interpretant)**.

### Was Agenten machen sollten

```python
# RICHTIG: Semiotisch vollständig
def test_semiotically_complete():
    # 1. Sign (Form, Struktur)
    assert parameter_count == 2
    assert return_type == float
    
    # 2. Object (Kausalität, Was ist wirklich)
    assert humidity_increase_causes_probability_increase
    
    # 3. Interpretant (Konvention, Was bedeutet es im Projekt)
    assert 0 <= probability <= 1
    assert no_moisture_means_zero_probability
```

---

## 8. Die sieben Ebenen der Validierung

**Peirce** hat später ein komplexeres System vorgeschlagen mit **zehn** Zeichenklassen. Vereinfacht auf sieben für unseren Kontext:

| Ebene | Semiotischer Typ | Test-Typ | Beispiel |
|---|---|---|---|
| 1 | Qualiszeichen | Syntaxtest | `isinstance(x, float)` |
| 2 | Sinszeichen | Typtest | `hasattr(obj, 'probability')` |
| 3 | Ikonisches Zeichen | Strukturtest | Parameter-Anzahl, Return-Typ |
| 4 | Indexikalisches Zeichen | Kausaltest | `higher_input → higher_output` |
| 5 | Ikon-Index | Struktur + Kausalität | Form UND Wirkung zusammen |
| 6 | Symbolisches Zeichen | Konventionstest | Bereichs-Invariante: [0,1] |
| 7 | Symbol-Index-Ikon | Vollständig | Alle drei zusammen prüfen |

**Ein Oracle-Test sollte mindestens Ebene 5-7 erreichen.**

---

## 9. Die Test-Checkliste: Semiotisch

### Für jeden Test fragen:

```markdown
## Ist dieser Test semiotisch vollständig?

### IKONISCH (Form)
☐ Prüft der Test die Struktur (Parameter, Return-Typ, Felder)?
☐ Ist die Teststruktur eine "Form" des Glossar?
☐ Wären die Assertions auch wahr für korrekte Alternative Impl.?

### INDEXIKALISCH (Kausalität)
☐ Prüft der Test Ursache-Wirkungs-Relationen?
☐ Gibt es mehrere Inputs mit beobachtbarer Auswirkung auf Output?
☐ Können wir die physikalische Kausalität nachvollziehen?

### SYMBOLISCH (Konvention)
☐ Prüft der Test Projekt-Konventionen (Bereichs-Invarianten)?
☐ Sind "Edge cases" gemäß Projekt-Norm definiert?
☐ Reflektiert der Test, was "in diesem Projekt wahr" bedeutet?

## Test-Qualität

- Nur ikonisch:       Oberflächlich, falsch positive leicht
- Nur indexikalisch:  Fragil, abhängig von Zahlen-Details
- Nur symbolisch:     Brittle, testet nur "erwartetes Verhalten"
- Ikonisch + Index:   Besser, prüft Form UND Kausalität
- Ikonisch + Symbol:  Besser, prüft Form UND Konvention
- Alle drei:          ★ ORACLE ★ Semiotisch vollständig
```

---

## 10. Rückfluss: Wenn Semiotik bricht

### Szenario: Test schlägt fehl

```python
def test_rainbow_probability():
    p = calculate_rainbow_probability(0.8, 45)
    assert p > calculate_rainbow_probability(0.5, 45)
    # AssertionError: 0.42 is not > 0.43
```

**Was ist passiert?**

Die **indexikalische Relation** ist verletzt: Höhere Feuchte sollte höhere Wahrscheinlichkeit bewirken, tut es aber nicht.

**Diagnose nach Peirce:**

```
Sign (Code):       calculate_rainbow_probability() existiert und läuft
Object (Realität):  "Höhere Feuchte → höhere Wahrscheinlichkeit" ist falsch!
Interpretant:      Entweder ist der Glossar falsch, oder der Code falsch.
```

**Rückfluss ins Glossar:**

```
Hypothese 1: Der Glossar ist falsch.
  → Sprechakt: "Erhöht Feuchte wirklich die Regenbogen-Wahrscheinlichkeit?"
  → Antwort: "Nein, manchmal sinkt sie, wenn der Winkel ungünstig wird"
  → Update Glossar: "Abhängig von Feuchte UND Winkel mit Interaktion"

Hypothese 2: Der Code ist falsch.
  → Sprechakt: "Ist die Implementierung korrekt?"
  → Antwort: "Es gibt einen Bug: Feuchtigkeit wird vergessen in Zeile 42"
  → Fix Code
```

---

## 11. MCP-Server für Semiotische Validierung

### Idealer MCP-Endpoint

```python
POST /validate/semiotics/{glossar_term}

Input:
  {
    "test_code": "...",
    "glossar_definition": "...",
    "implementation": "..."
  }

Output:
  {
    "ikonisch": {
      "valid": true,
      "details": "Parameter count matches"
    },
    "indexikalisch": {
      "valid": true,
      "details": "Causal direction verified"
    },
    "symbolisch": {
      "valid": false,
      "details": "Range invariant violated: result > 1.0"
    },
    "overall": "PARTIALLY_VALID",
    "recommendation": "Add symbolic assertion for range"
  }
```

Ein solcher Service würde den Agenten **systematisch** sagen, welche semiotische Ebene verletzt ist.

---

## Zusammenfassung

**Semiotische Validierung ist praktikal:**

1. **Ikonisch** = Form des Tests ähnelt Glossar-Definition
2. **Indexikalisch** = Test prüft Ursache-Wirkungs-Beziehungen
3. **Symbolisch** = Test prüft Projekt-Konventionen
4. **Oracle** = Test auf allen drei Ebenen vollständig
5. **Rückfluss** = Wenn Test bricht, diagnostiziert Peirce, wo die Lücke ist

Ein Agent, der semiotisch validiert, versteht nicht nur den Code — er versteht die **Bedeutungsstruktur** dahinter.

---

**Erstellt:** 2026-08-15  
**Thema:** Semiotik, Peirce, Validierung  
**Nächste Lektüre:** 08-funktoren-epistemologie.md (Funktoren als epistemische Garantien)
