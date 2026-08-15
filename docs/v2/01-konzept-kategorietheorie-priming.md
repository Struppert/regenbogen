# Agent-Priming v2: Semiotik + Kategorietheorie

**Datum:** 2026-08-15  
**Zweck:** Formales Rahmenwerk für konsistente Abbildung von Glossar-Begriffen in Code  
**Zielgruppe:** Agenten, Entwickler, Architekten  
**Status:** Konzept / Pilotphase  

---

## 1. Problem und Motivation

### Das aktuelle System (v1)

```
Glossar/Ontologie
  ↓ [Implizit, informal]
Code
  ↓ [Hoffnung, dass es passt]
Tests/Validierung
```

**Probleme:**
- Mapping zwischen Glossar und Code ist **nicht formalisiert**
- Agenten wissen nicht, wie sie Glossar-Begriffe strukturkonsistent in Code abbilden
- Tests prüfen oft nur Funktionalität, nicht Korrespondenz zum Glossar
- Keine maschinenprüfbare Regel für "ist diese Abbildung korrekt?"

### Die Lösung: Formale Strukturen

Statt informale Abbildung → **formale Funktoren zwischen Kategorien**

```
Glossar-Kategorie
  (Objekte + semantische Pfeile)
       ↓ Funktor F
Code-Kategorie
  (Symbole + Code-Abhängigkeiten)
       ↓ Funktor T
Validierungs-Kategorie
  (Tests + Assertions)
```

---

## 2. Theoretische Grundlagen

### 2.1 Semiotik: Bedeutung innerhalb einer Domäne

**Peirces semiotisches Dreieck:**

```
      SIGNIFIKANT
      (Zeichen/Wort)
            |
            |  repräsentiert
            |
   SIGNIFIKAT ←→ OBJEKT
 (Bedeutung)  referiert auf
           (Realität)
```

**Für Glossare:**

```
Glossar-Eintrag "RegenbogenWahrscheinlichkeit"
  |
  Signifikant: Wort "RegenbogenWahrscheinlichkeit"
  Signifikat: mathematische Größe ∈ [0,100]
  Objekt: tatsächliches Naturphänomen
  
Invarianten: 0 ≤ wert ≤ 100
Kompetenzfrage: Kann Domänenexperte das verstehen?
Projektion: glossar-domain.md + Code + Tests
```

**Semiotik antwortet:** "Was bedeutet dieser Begriff?"

---

### 2.2 Kategorietheorie: Struktur zwischen Domänen

**Kernidee:** Nicht die Objekte selbst sind wichtig, sondern die **Pfeile (Morphismen)** zwischen ihnen.

```
Kategorie C:
  Objekte:      A, B, C, ...
  Morphismen:   A → B, B → C, ...
  Komposition:  (B → C) ∘ (A → B) = A → C
  Identität:    id_A: A → A
```

**Für dein System:**

```
GLOSSAR-KATEGORIE G:
  Objekte: Glossar-Begriffe
    RegenbogenWahrscheinlichkeit, Wetterzustand, SonnenstandsFaktor
  Morphismen: semantische Abhängigkeiten
    RegenbogenWahrscheinlichkeit → Wetterzustand (depends_on)
    RegenbogenWahrscheinlichkeit → SonnenstandsFaktor (depends_on)
  Komposition: transitive Abhängigkeiten
    A → B → C bedeutet A hängt transitiv von C ab

CODE-KATEGORIE K:
  Objekte: Code-Symbole
    class RegenbogenWahrscheinlichkeit, class Wetterzustand
  Morphismen: Code-Abhängigkeiten
    RegenbogenWahrscheinlichkeit → Wetterzustand (imports)
    RegenbogenWahrscheinlichkeit → SonnenstandsFaktor (calls)
  Komposition: transitive Imports/Calls
    import A; A imports B bedeutet transitiv von B abhängig

VALIDIERUNGS-KATEGORIE V:
  Objekte: Test-Oracles, Assertions
    test_wahrscheinlichkeit_bounds, assert(0 ≤ value ≤ 100)
  Morphismen: Test-Abhängigkeiten
    test_wahrscheinlichkeit_bounds → RegenbogenWahrscheinlichkeit (validates)
  Komposition: Test-Suites können andere Tests aufrufen
    Suite A → Test B → Test C
```

---

### 2.3 Funktoren: Struktur-erhaltende Abbildungen

**Definition:** Ein Funktor F: C → K ist eine Abbildung zwischen Kategorien, die **Struktur erhält**.

```
Funktor F: Glossar-Kategorie → Code-Kategorie

Objekt-Abbildung:
  F(RegenbogenWahrscheinlichkeit) = class RegenbogenWahrscheinlichkeit(int)
  F(Wetterzustand) = class Wetterzustand
  
Morphismus-Abbildung (Struktur-Erhaltung!):
  Wenn A → B im Glossar (A hängt von B ab)
  Dann F(A) → F(B) im Code (Code respektiert Abhängigkeit)
  
  GLOSSAR:          CODE:
  RegenbogenW. → Wetterzustand
       |              |
    F  |              |  F
       ↓              ↓
  RegenbogenW. → Wetterzustand
     (Code)
     
  Komposition erhalten:
    F(A → B → C) = F(A) → F(B) → F(C)
```

**Kritisch:** Struktur muss erhalten bleiben!

```
FALSCH:
  Glossar: A → B (A depends on B)
  Code: class A (keine Abhängigkeit zu B, obwohl B nötig ist)
  Funktor NICHT struktur-erhaltend

RICHTIG:
  Glossar: A → B
  Code: class A imports B
  Funktor struktur-erhaltend
```

---

### 2.4 Funktor-Komposition: Validierungsketten

```
Funktor F: G → K  (Glossar → Code)
Funktor T: K → V  (Code → Tests)

Komposition (T ∘ F): G → V  (Glossar → Validierung)

RegenbogenWahrscheinlichkeit
  ──[F]──→ class RegenbogenWahrscheinlichkeit(int)
              ──[T]──→ test_wahrscheinlichkeit_bounds()
```

**Bedeutung:** 
- Glossar-Begriff wird in Code abgebildet
- Code wird durch Tests validiert
- Dadurch: Glossar-Invariante ist durch Tests nachgewiesen

---

## 3. Die drei Kategorien im Detail

### 3.1 Glossar-Kategorie G

**Objekte (Glossar-Einträge):**

```markdown
### RegenbogenWahrscheinlichkeit

Semantischer Raum: domain
Bedeutung: Prozentwert der Wahrscheinlichkeit eines sichtbaren Regenbogens
Invariante: 0 ≤ wert ≤ 100
```

**Morphismen (Abhängigkeiten):**

```
RegenbogenWahrscheinlichkeit
  ──depends_on──→ Wetterzustand
  ──depends_on──→ SonnenstandsFaktor
  ──depends_on──→ Sonnenstand

Wetterzustand
  ──depends_on──→ Sonnenscheinanteil
  ──depends_on──→ RegenIntensität

SonnenstandsFaktor
  ──depends_on──→ Sonnenstand
  ──depends_on──→ geometrische_modellierung
```

**Kommutative Diagramme (Pfeile-Struktur):**

```
RegenbogenWahrscheinlichkeit ──→ Wetterzustand
            |                        |
            ↓                        ↓
      SonnenstandsFaktor ──→ Sonnenstand

Wenn A → B → C, dann muss A → C transitiv gelten
```

---

### 3.2 Code-Kategorie K

**Objekte (Code-Symbole):**

```python
# src/regenbogen/domain/wahrscheinlichkeit.py

class RegenbogenWahrscheinlichkeit(int):
    """F(RegenbogenWahrscheinlichkeit)"""
    def __init__(self, wert: int):
        assert 0 <= wert <= 100
        self.wert = wert
```

**Morphismen (Code-Abhängigkeiten):**

```python
# Pfeil: RegenbogenWahrscheinlichkeit → Wetterzustand
from regenbogen.domain.wetterzustand import Wetterzustand

class RegenbogenWahrscheinlichkeit:
    def __init__(self, wetterzustand: Wetterzustand):
        # F(depends_on) erhalten: Code respektiert Glossar-Abhängigkeit
        self.wetterzustand = wetterzustand
```

**Struktur-Eigenschaft:**

```
Glossar hat Pfeile:
  A → B → C

Code muss haben:
  class A imports B
  class B imports C
  (oder transitiv: A kann auf C zugreifen)
  
Wenn diese Struktur nicht erhalten ist:
  Funktor F ist NICHT korrekt
  → Agent-Präflight muss das finden
```

---

### 3.3 Validierungs-Kategorie V

**Objekte (Test-Oracles):**

```python
# tests/domain/test_wahrscheinlichkeit.py

@pytest.mark.oracle("RegenbogenWahrscheinlichkeit_invariant")
def test_wahrscheinlichkeit_bounds():
    """T(RegenbogenWahrscheinlichkeit)"""
    # Validiert Invariante: 0 ≤ wert ≤ 100
    for val in [0, 50, 100]:
        w = RegenbogenWahrscheinlichkeit(val)
        assert 0 <= w.wert <= 100
    
    with pytest.raises(AssertionError):
        RegenbogenWahrscheinlichkeit(101)
```

**Morphismen (Test-Abhängigkeiten):**

```
test_wahrscheinlichkeit_bounds
  ──validates──→ RegenbogenWahrscheinlichkeit (Code)
  ──validates_glossar_invariant──→ RegenbogenWahrscheinlichkeit (Glossar)

test_wahrscheinlichkeit_with_wetterzustand
  ──validates──→ RegenbogenWahrscheinlichkeit
  ──validates──→ Wetterzustand
  (Test prüft gemeinsame Invariante)
```

---

## 4. Agent-Priming mit Funktoren

### 4.1 Preflight-Checkliste: PF-FUNKTOR

**Vor jeder Code-Änderung eines Glossar-Begriffs:**

```markdown
## PF-FUNKTOR: Struktur-Erhaltung prüfen

### Phase 1: Glossar-Struktur verstehen
☐ Glossareintrag identifizieren: A = [Begriff]
☐ Alle Abhängigkeiten im Glossar finden: A → B, A → C, ...
☐ Transitive Abhängigkeiten verstehen: A → D → E → F
☐ Invarianten dokumentieren: [Liste]

### Phase 2: Funktor F definieren (Glossar → Code)

☐ Code-Symbol eindeutig: F(A) = [class/function name]
☐ Code-Datei: src/regenbogen/[space]/[file].py
☐ Objekt-Abbildung dokumentiert in Code-Kommentar

### Phase 3: Struktur-Erhaltung prüfen

Für jeden Glossar-Pfeil A → B:
  ☐ Existiert Pfeil F(A) → F(B) im Code?
  ☐ Typ des Pfeils dokumentiert (imports, calls, inheritance)?
  ☐ Richtung korrekt? (A → B → F(A) → F(B))

Komposition-Erhaltung:
  ☐ Wenn A → B → C im Glossar
  ☐ Dann F(A) → F(B) → F(C) im Code
  ☐ Alle Zwischenschritte vorhanden?

### Phase 4: Funktor T definieren (Code → Tests)

☐ Test-Oracle geplant für F(A)
☐ Test-Datei: tests/domain/test_[name].py
☐ Invarianten des Glossars in Assertions kodiert

### Phase 5: Funktor-Komposition validieren (T ∘ F)

Glossar A ──[F]──→ Code F(A) ──[T]──→ Test T(F(A))

☐ Test prüft Glossar-Invarianten?
☐ Wenn Test fehlschlägt, ist Glossar-Invariante verletzt?
☐ Test ist vom Code abhängig (nicht vom Glossar)?

### Phase 6: Vollständigkeits-Checkliste

☐ Alle Glossar-Pfeile haben Code-Entsprechung?
☐ Keine neuen Pfeile im Code ohne Glossar-Quelle?
☐ Komposition-Struktur erhalten?
☐ Tests decken alle Invarianten ab?
```

---

### 4.2 Agent-Instruktion: Funktoren respektieren

```markdown
## Instruktion: Funktor-Respekt

Als Agent in diesem System:

1. VERSTEHE DIE GLOSSAR-STRUKTUR
   - Nicht nur einzelne Begriffe, sondern Pfeile
   - Welche Abhängigkeiten existieren?
   - Welche Invarianten gelten?

2. BILDE STRUKTUR KONSISTENT AB
   - Jeder Glossar-Pfeil → Code-Pfeil
   - Keine stillen Struktur-Änderungen
   - Komposition bleibt erhalten

3. SCHREIBE TESTS ALS FUNKTOR T
   - Tests prüfen nicht nur "funktioniert"
   - Tests prüfen "Glossar-Invariante erfüllt"
   - Tests sind strukturelle Evidenz

4. DOKUMENTIERE DEN FUNKTOR
   - Code-Kommentar: "F([Glossar-Begriff]) ="
   - Test-Markierung: @pytest.mark.oracle("[Glossar-Invariante]")
   - Package-Schema: welche Räume sind beteiligt?

5. VALIDIERE STRUKTUR-ERHALTUNG
   - PF-FUNKTOR-Checkliste vor Code-Änderung
   - Wenn Struktur verletzt: Sprechakt oder Abbruch
```

---

## 5. Peirce's Kategorien: Ikonisch / Indexikalisch / Symbolisch

Erweitere die Funktoren-Beschreibung mit **semiotischen Relationstypen**:

### 5.1 Ikonische Korrespondenz

**Form-Ähnlichkeit zwischen Glossar und Code:**

```
Glossar-Name = Code-Name (direkter Bezug)

Beispiel:
  Glossar: "RegenbogenWahrscheinlichkeit"
  Code: "class RegenbogenWahrscheinlichkeit"
  
  ✓ Ikonisch: Name gleich, Form ähnlich
  
Funktor-Markierung:
  @iconic_correspondence("RegenbogenWahrscheinlichkeit")
  class RegenbogenWahrscheinlichkeit:
      pass
```

---

### 5.2 Indexikalische Korrespondenz

**Direkte Verursachung: Code verursacht Glossar-Verhalten:**

```
Glossar-Invariante wird direkt im Code durchgesetzt

Beispiel:
  Glossar: "0 ≤ wert ≤ 100"
  Code: "assert 0 <= self.wert <= 100"
  
  ✓ Indexikalisch: Invariante ist direkt wirksam
  
Funktor-Markierung:
  class RegenbogenWahrscheinlichkeit:
      def __init__(self, wert: int):
          # @indexical_correspondence("RegenbogenWahrscheinlichkeit.invariant")
          assert 0 <= wert <= 100
```

---

### 5.3 Symbolische Korrespondenz

**Konvention: Code folgt etabliertem Pattern:**

```
Glossar-Konzept wird durch Projekt-Konvention realisiert

Beispiel:
  Glossar: "numerische Größe mit Bereich"
  Konvention im Projekt:
    - Subclass von int
    - __init__ mit Assertion
    - Getter/Setter für Invariante
  Code: Folgt dieser Konvention
  
  ✓ Symbolisch: nicht direkt ähnlich, aber konventionell verbunden
  
Funktor-Markierung in package-schema.md:
  domain/wahrscheinlichkeit.py:
    Pattern: "bounded_numeric_entity"
    Convention: "int subclass with __init__ assertion"
```

---

## 6. Fehlererkennung: Strukturverletzungen

### 6.1 Beispiel: Pfeil fehlt

```
GLOSSAR (sollte sein):
  RegenbogenWahrscheinlichkeit → Wetterzustand (depends_on)

CODE (tatsächlich):
  class RegenbogenWahrscheinlichkeit:
      def __init__(self):
          # ❌ Wetterzustand wird nicht importiert
          self.value = 0

PROBLEM:
  Funktor F nicht struktur-erhaltend
  Pfeil RegenbogenW. → Wetterzustand ist nicht abgebildet
  
ERKENNUNG:
  Checker könnte prüfen:
    "Für jede Glossar-Abhängigkeit A → B:
     existiert Code-Abhängigkeit F(A) → F(B)?"
```

---

### 6.2 Beispiel: Komposition verletzt

```
GLOSSAR:
  A → B → C (transitive Abhängigkeit)

CODE (falsch):
  class A:
      from B import something  # ✓
  
  class B:
      # ❌ importiert C nicht, obwohl A das braucht
      self.value = 0

PROBLEM:
  Komposition nicht erhalten
  A hat implizit Abhängigkeit von C, aber:
  B → C fehlt im Code
  
LÖSUNG:
  Entweder:
  1. B muss C importieren (Komposition retten)
  2. Oder Glossar-Struktur ist falsch (Sprechakt)
```

---

## 7. Integration in das Projekt

### 7.1 Neue Dateien / Struktur

```
glossar-meta.md
  ├─ Neue Sektion: "## 4. Funktor-Mapping"
  │  └─ Für jeden Begriff: Funktor F dokumentieren
  │
glossar-domain.md
  ├─ Neue Felder in Einträgen:
  │  ├─ Morphismen: [Liste von Abhängigkeiten]
  │  ├─ Funktor F: src/..., class/function name
  │  ├─ Semiotischer Typ: ikonisch | indexikalisch | symbolisch
  │  └─ Test-Oracle: tests/..., function name
  │
package-schema.md
  ├─ Neue Sektion: "## 9. Funktor-Mapping und -Validierung"
  │  └─ Conventions für jeden Raum
  │
preflight-checkliste.md
  ├─ Neuer Schritt: "PF-FUNKTOR"
  │  └─ Struktur-Erhaltung vor Code-Änderung
```

### 7.2 Neue Checker/Tools

```python
# tools/check_funktor_structure.py

def check_glossar_funktor(glossar_entry):
    """
    Prüft, ob Glossar-Struktur im Code erhalten ist:
    - Für A → B im Glossar
    - Existiert F(A) → F(B) im Code?
    """
    pass

def check_composition(glossar_path, code_path):
    """
    Prüft Komposition-Erhaltung:
    - Wenn A → B → C im Glossar
    - Dann F(A) → F(B) → F(C) im Code
    """
    pass
```

---

## 8. Warum das funktioniert

### 8.1 Für Agenten

```
Statt: "Mach ein ähnliches Mapping im Code"
Jetzt: "Respektiere die Funktoren-Struktur:
        - Jeder Glossar-Pfeil → Code-Pfeil
        - Komposition bleibt erhalten
        - Tests validieren via T ∘ F"
        
Das ist maschinenprüfbar und formal.
```

### 8.2 Für Menschen

```
Statt: "Hoffen, dass das Code-Design gut ist"
Jetzt: "Glossar-Struktur ist explizit in Code sichtbar
        und durch Tests nachgewiesen"
        
Code-Design folgt Glossar-Struktur, nicht umgekehrt.
```

### 8.3 Für Validierung

```
Statt: "Tests prüfen nur Funktionalität"
Jetzt: "Funktor T beweist, dass Code-Struktur
        Glossar-Invarianten erfüllt"
        
Tests sind strukturelle Evidence.
```

---

## 9. Nächste Schritte

1. **Pilotbeispiel durcharbeiten:** RegenbogenWahrscheinlichkeit
   (siehe: `02-beispiel-regenbogenwahrscheinlichkeit.md`)

2. **Checker implementieren:** `tools/check_funktor_structure.py`

3. **Agent-Instruktion aktualisieren:** AGENTS.md + preflight-checkliste.md

4. **Learning-Matrix:** Patterns dokumentieren (welche Funktoren sind häufig?)

---

## Glossar dieser Dokumentation

| Term | Bedeutung |
|------|-----------|
| **Kategorie** | mathematische Struktur: Objekte + Pfeile |
| **Morphismus** | Pfeil zwischen Objekten (Abhängigkeit) |
| **Funktor** | struktur-erhaltende Abbildung zwischen Kategorien |
| **Korrespondenzsatz** | Bindung Glossar ↔ Code ↔ Test |
| **Struktur-Erhaltung** | wenn A → B, dann F(A) → F(B) |
| **Komposition** | transitive Abhängigkeiten: A → B → C |
| **Ikonisch** | form-ähnlich (Name = Name) |
| **Indexikalisch** | direkt wirksam (Assertion = Invariante) |
| **Symbolisch** | konventionell (Pattern-Gebunden) |
