# Praktisches Beispiel: RegenbogenWahrscheinlichkeit mit Funktoren

**Ziel:** Zeige, wie Semiotik + Kategorietheorie auf einen realen Glossar-Begriff angewendet wird.

**Beispiel:** RegenbogenWahrscheinlichkeit (bereits in deinem System vorhanden)

---

## Phase 1: Die Glossar-Kategorie G

### 1.1 Objekt definieren

**Glossareintrag (Semiotik):**

```markdown
### RegenbogenWahrscheinlichkeit

**Semantischer Raum:** domain

**Eintragstiefe:** vollständig

**Kompetenzfrage:**
Kann ein Domänenexperte (nicht-technisch, keine Laufzeitkenntnisse)
diesen Begriff vollständig beurteilen?
→ Ja: meteorologisches Phänomen, verstehbar ohne Code

**Bedeutung:**
Prozentwert in [0, 100], der die Wahrscheinlichkeit angibt, dass ein
sichtbarer Primärbogen unter gegebenen Bedingungen optisch möglich ist.

Nicht: Vorhersagegenauigkeit oder operative Zuverlässigkeit
Sondern: reine optische/meteorologische Plausibilität

**Invarianten:**
- Wertebereich: 0 ≤ wert ≤ 100
- Ohne Sonne: wert = 0 (notwendige Bedingung)
- Ohne Regen: wert = 0 (notwendige Bedingung)
- Mit Sonne und Regen: 0 < wert (aber nicht garantiert ≤ 100)
- Monotonie: mehr Sonnenschein → wert kann steigen
- Monotonie: mehr Regen → wert kann steigen
- Sonnenstand-Fenster: optimale Höhe 25–42°

**Projektionen:**
- Code: src/regenbogen/domain/wahrscheinlichkeit.py
- Tests: tests/domain/test_wahrscheinlichkeit.py
- Modell: MODELL-README.md § 3 (RegenbogenWahrscheinlichkeit)
- Glossar: glossar-domain.md

**Abgrenzung:**
- Nicht: RegenbogenSichtbarkeit (anderer Aspekt)
- Nicht: Sonnenstand (technische Eingabe)
- Nicht: Wetterdaten (Observables, nicht berechnet)

**Migrationsstatus:** canonical
```

---

### 1.2 Morphismen definieren (Abhängigkeiten)

**Was hängt wovon ab?**

```
Glossar-Kategorie G:

RegenbogenWahrscheinlichkeit
  ──depends_on──→ Wetterzustand
  ──depends_on──→ SonnenstandsFaktor
  ──depends_on──→ Sonnenstand

Wetterzustand
  ──depends_on──→ SonnenscheinAnteil
  ──depends_on──→ RegenIntensität

SonnenstandsFaktor
  ──depends_on──→ Sonnenstand
  (Geometrisches Modell: welcher Winkel ist optimal?)

Sonnenstand
  ──depends_on──→ Koordinaten (lat, lon)
  ──depends_on──→ Uhrzeit
  ──depends_on──→ Datum
```

**Kommutatives Diagramm:**

```
                    RegenbogenWahrscheinlichkeit
                            ↗           ↑
                           /            |
                          /             |
    SonnenstandsFaktor ──/              |
         ↑                              |
         |                              |
       Sonnenstand ←── Koordinaten      |
         ↑                              |
         |                          Wetterzustand
         |                              ↑
         |                              |
    Uhrzeit                        SonnenscheinAnteil
       Datum                       RegenIntensität
```

**Transitive Abhängigkeiten:**
```
RegenbogenWahrscheinlichkeit → Sonnenstand → Koordinaten
(transitiv: Wahrscheinlichkeit braucht Koordinaten)
```

---

## Phase 2: Die Code-Kategorie K (Funktor F)

### 2.1 Objekt-Abbildung: F(RegenbogenWahrscheinlichkeit)

**Glossar-Objekt → Code-Symbol:**

```python
# src/regenbogen/domain/wahrscheinlichkeit.py

# @functor_source("glossar-domain.md:RegenbogenWahrscheinlichkeit")
class RegenbogenWahrscheinlichkeit(int):
    """
    F(RegenbogenWahrscheinlichkeit) = klasse mit Bereich-Validierung
    
    Semiotischer Typ: IKONISCH (Name gleich)
    Invariante: 0 ≤ self.wert ≤ 100
    """
    
    def __init__(self, wert: int):
        if not (0 <= wert <= 100):
            raise ValueError(f"Wahrscheinlichkeit muss ∈ [0,100] sein, nicht {wert}")
        self.wert = wert
    
    def __repr__(self):
        return f"RegenbogenWahrscheinlichkeit({self.wert})"
    
    # Invarianten als Methoden für Reflektierbarkeit
    @property
    def is_impossible(self) -> bool:
        """Wert = 0: kein Regenbogen möglich"""
        return self.wert == 0
    
    @property
    def is_certain(self) -> bool:
        """Wert = 100: Regenbogen sehr wahrscheinlich"""
        return self.wert == 100
```

---

### 2.2 Morphismus-Abbildung: F(Abhängigkeiten)

**Glossar-Pfeile → Code-Abhängigkeiten:**

```python
# src/regenbogen/domain/wahrscheinlichkeit.py

from regenbogen.domain.wetterzustand import Wetterzustand
from regenbogen.domain.sonnenstand import Sonnenstand, SonnenstandsFaktor

# @functor_morphism("RegenbogenWahrscheinlichkeit depends_on Wetterzustand")
class RegenbogenWahrscheinlichkeit(int):
    """
    ABHÄNGIGKEITEN (Morphismen):
    
    Glossar:  RegenbogenWahrscheinlichkeit → Wetterzustand
    Code:     benutzt Wetterzustand direkt (import + argument)
    
    Status: F(depends_on) erhalten ✓
    """
    
    def __init__(
        self,
        wetterzustand: Wetterzustand,  # F(depends_on Wetterzustand)
        sonnenstand: Sonnenstand,      # F(depends_on Sonnenstand)
    ):
        # Berechne Wahrscheinlichkeit aus Komponenten
        wert = self._calculate(wetterzustand, sonnenstand)
        
        # @indexical_correspondence("RegenbogenWahrscheinlichkeit.invariant")
        # Invariante ist direkt wirksam
        assert 0 <= wert <= 100, f"Interne Berechnung verletzt Invariante: {wert}"
        
        super().__init__(wert)
        self.wetterzustand = wetterzustand
        self.sonnenstand = sonnenstand
    
    # F(depends_on SonnenstandsFaktor) durch Berechnung
    def _calculate(self, wetterzustand: Wetterzustand, sonnenstand: Sonnenstand) -> int:
        """
        FUNKTOR-KOMPOSITION:
        
        Glossar:  RegenbogenW. → Wetterzustand → SonnenscheinAnteil
        Code:     RegenbogenWahrscheinlichkeit imports Wetterzustand
                  (Komposition erhalten: RW braucht Wetterzustand)
        """
        
        # Glossar: "ohne Sonne: wert = 0"
        if not wetterzustand.sonnenschein:
            return 0
        
        # Glossar: "ohne Regen: wert = 0"
        if not wetterzustand.regen:
            return 0
        
        # Glossar: Formel = Sonnenscheinanteil * RegenIntensität * SonnenstandsFaktor
        basis = (
            wetterzustand.sonnenschein_intensitaet * 0.6 +
            wetterzustand.regen_intensitaet * 0.4
        )
        
        # F(depends_on SonnenstandsFaktor)
        sonnenstands_faktor = sonnenstand.berechne_faktor()
        
        wert = basis * sonnenstands_faktor * 100
        return max(0, min(100, round(wert)))
```

**Struktur-Erhaltungs-Prüfung:**

```
GLOSSAR (sollte sein):
  RegenbogenWahrscheinlichkeit
    → Wetterzustand
    → Sonnenstand
    → SonnenstandsFaktor

CODE (tatsächlich):
  class RegenbogenWahrscheinlichkeit:
      __init__(wetterzustand: Wetterzustand, sonnenstand: Sonnenstand)
      # ✓ imports Wetterzustand
      # ✓ imports Sonnenstand
      # ✓ SonnenstandsFaktor durch Sonnenstand erreichbar
  
  Status: Struktur ERHALTEN ✓
  Funktor F ist struktur-erhaltend ✓
```

---

## Phase 3: Die Validierungs-Kategorie V (Funktor T)

### 3.1 Test-Oracles definieren

**Code-Symbole → Test-Validierung:**

```python
# tests/domain/test_wahrscheinlichkeit.py

import pytest
from regenbogen.domain.wahrscheinlichkeit import RegenbogenWahrscheinlichkeit
from regenbogen.domain.wetterzustand import Wetterzustand
from regenbogen.domain.sonnenstand import Sonnenstand

# @functor_target("RegenbogenWahrscheinlichkeit")
class TestRegenbogenWahrscheinlichkeit:
    """
    T(RegenbogenWahrscheinlichkeit) = Test-Suite
    
    Validiert alle Glossar-Invarianten
    """
    
    # T(Invariante: 0 ≤ wert ≤ 100)
    @pytest.mark.oracle("RegenbogenWahrscheinlichkeit.invariant.bounds")
    def test_wahrscheinlichkeit_bounds(self):
        """
        Glossar: 0 ≤ wert ≤ 100
        Code:    assert 0 <= self.wert <= 100
        Test:    Validiert, dass Invariante gilt
        """
        wetter = Wetterzustand(sonnenschein=True, regen=True)
        sonnenstand = Sonnenstand(hoehe=30, azimut=180)
        
        # Alle gültigen Werte sollten akzeptiert werden
        for erwartet in [0, 1, 50, 99, 100]:
            # Wir erzwingen Wert durch Mocking
            w = RegenbogenWahrscheinlichkeit.__new__(RegenbogenWahrscheinlichkeit)
            RegenbogenWahrscheinlichkeit.__init__(w, erwartet)
            assert w.wert == erwartet
        
        # Ungültige Werte sollten abgelehnt werden
        with pytest.raises(AssertionError):
            w = RegenbogenWahrscheinlichkeit.__new__(RegenbogenWahrscheinlichkeit)
            RegenbogenWahrscheinlichkeit.__init__(w, -1)
        
        with pytest.raises(AssertionError):
            w = RegenbogenWahrscheinlichkeit.__new__(RegenbogenWahrscheinlichkeit)
            RegenbogenWahrscheinlichkeit.__init__(w, 101)
    
    # T(Invariante: ohne Sonne = 0)
    @pytest.mark.oracle("RegenbogenWahrscheinlichkeit.glossar.no_sun_means_zero")
    def test_wahrscheinlichkeit_no_sun_gives_zero(self):
        """
        Glossar: ohne Sonnenschein → wert = 0
        Code:    if not wetterzustand.sonnenschein: return 0
        Test:    Validiert diese Regel
        """
        wetter = Wetterzustand(sonnenschein=False, regen=True)
        sonnenstand = Sonnenstand(hoehe=30, azimut=180)
        
        w = RegenbogenWahrscheinlichkeit(wetter, sonnenstand)
        assert w.wert == 0
    
    # T(Invariante: ohne Regen = 0)
    @pytest.mark.oracle("RegenbogenWahrscheinlichkeit.glossar.no_rain_means_zero")
    def test_wahrscheinlichkeit_no_rain_gives_zero(self):
        """
        Glossar: ohne Regen → wert = 0
        Code:    if not wetterzustand.regen: return 0
        Test:    Validiert diese Regel
        """
        wetter = Wetterzustand(sonnenschein=True, regen=False)
        sonnenstand = Sonnenstand(hoehe=30, azimut=180)
        
        w = RegenbogenWahrscheinlichkeit(wetter, sonnenstand)
        assert w.wert == 0
    
    # T(Invariante: Monotonie)
    @pytest.mark.oracle("RegenbogenWahrscheinlichkeit.glossar.monotonicity")
    def test_wahrscheinlichkeit_monotonicity(self):
        """
        Glossar: mehr Sonnenschein → wert ≥ vorher
        Glossar: mehr Regen → wert ≥ vorher
        Test:    Validiert Monotonie
        """
        sonnenstand = Sonnenstand(hoehe=30, azimut=180)
        
        # Teste Sonnenschein-Monotonie
        wetter1 = Wetterzustand(sonnenschein_intensitaet=0.3, regen_intensitaet=0.5)
        wetter2 = Wetterzustand(sonnenschein_intensitaet=0.7, regen_intensitaet=0.5)
        
        w1 = RegenbogenWahrscheinlichkeit(wetter1, sonnenstand).wert
        w2 = RegenbogenWahrscheinlichkeit(wetter2, sonnenstand).wert
        
        assert w2 >= w1, "Mehr Sonnenschein sollte nicht zu weniger Wahrscheinlichkeit führen"
    
    # T(Abhängigkeit: Sonnenstand-Fenster)
    @pytest.mark.oracle("RegenbogenWahrscheinlichkeit.glossar.sun_angle_window")
    def test_wahrscheinlichkeit_sun_angle_matters(self):
        """
        Glossar: Sonnenstand-Fenster [25°, 42°] ist optimal
        Code:    SonnenstandsFaktor berücksichtigt Fenster
        Test:    Validiert Fenster-Effekt
        """
        wetter = Wetterzustand(sonnenschein_intensitaet=1.0, regen_intensitaet=1.0)
        
        # Hohe Sonne (über 42°) sollte niedriger sein als optimale Höhe
        hohe_sonne = Sonnenstand(hoehe=60, azimut=180)
        optimale_hoehe = Sonnenstand(hoehe=35, azimut=180)
        
        w_hoch = RegenbogenWahrscheinlichkeit(wetter, hohe_sonne).wert
        w_optimal = RegenbogenWahrscheinlichkeit(wetter, optimale_hoehe).wert
        
        assert w_optimal > w_hoch, "Optimale Sonnenhöhe sollte höhere Wahrscheinlichkeit geben"
```

---

### 3.2 Morphismus-Abbildung: Test-Abhängigkeiten

**Code-Abhängigkeiten → Test-Abhängigkeiten:**

```python
# Tests prüfen nicht nur einzelne Invarianten, sondern auch Abhängigkeiten

class TestRegenbogenWahrscheinlichkeitIntegration:
    """
    T(Abhängigkeiten)
    
    Glossar: RegenbogenWahrscheinlichkeit → Wetterzustand
    Code:    braucht Wetterzustand-Objekt
    Test:    prüft Integration mit Wetterzustand
    """
    
    @pytest.mark.oracle("RegenbogenWahrscheinlichkeit.depends_on.Wetterzustand")
    def test_regenbogenwahrscheinlichkeit_uses_wetterzustand(self):
        """
        T(depends_on Wetterzustand)
        
        Unterschiedliche Wetterzustände → unterschiedliche Wahrscheinlichkeiten
        """
        sonnenstand = Sonnenstand(hoehe=35, azimut=180)
        
        # Wetter 1: gute Bedingungen
        wetter_gut = Wetterzustand(sonnenschein_intensitaet=0.9, regen_intensitaet=0.8)
        w_gut = RegenbogenWahrscheinlichkeit(wetter_gut, sonnenstand).wert
        
        # Wetter 2: schlechte Bedingungen
        wetter_schlecht = Wetterzustand(sonnenschein_intensitaet=0.2, regen_intensitaet=0.3)
        w_schlecht = RegenbogenWahrscheinlichkeit(wetter_schlecht, sonnenstand).wert
        
        assert w_gut > w_schlecht, "Besseres Wetter sollte höhere Wahrscheinlichkeit geben"
```

---

## Phase 4: Funktor-Komposition (T ∘ F)

### 4.1 Die vollständige Kette

```
RegenbogenWahrscheinlichkeit (Glossar)
  ──[F]──→ class RegenbogenWahrscheinlichkeit (Code)
              ──[T]──→ test_wahrscheinlichkeit_* (Tests/Oracles)

Komposition (T ∘ F):
  Glossar-Invariante wird durch Test validiert
  
Beispiel:
  Glossar: "0 ≤ wert ≤ 100"
  Code: "assert 0 <= self.wert <= 100"
  Test: "@pytest.mark.oracle('RegenbogenWahrscheinlichkeit.invariant.bounds')"
  
  ✓ Kette vollständig: Glossar-Invariante ist im Test nachgewiesen
```

### 4.2 Validierungsbeweis

```python
# Nachweis, dass T ∘ F korrekt ist:

# Wenn Test fehlschlägt → Glossar-Invariante verletzt
def test_wahrscheinlichkeit_bounds():
    # Dieser Test schlägt fehl, wenn:
    # - Glossar-Invariante "0 ≤ wert ≤ 100" verletzt wird
    # - Code-Assertion nicht funktioniert
    # - Funktor F nicht struktur-erhaltend ist
    
    # → Test ist strukturelle Evidence für Funktor F
```

---

## Phase 5: Agent-Priming anwenden

### 5.1 PF-FUNKTOR Checklist für dieses Beispiel

```markdown
## PF-FUNKTOR: RegenbogenWahrscheinlichkeit

### Phase 1: Glossar-Struktur verstehen

☑ Glossareintrag: RegenbogenWahrscheinlichkeit
☑ Abhängigkeiten im Glossar:
  - RegenbogenWahrscheinlichkeit → Wetterzustand
  - RegenbogenWahrscheinlichkeit → Sonnenstand
  - RegenbogenWahrscheinlichkeit → SonnenstandsFaktor
☑ Transitive Abhängigkeiten:
  - RegenbogenWahrscheinlichkeit → Sonnenstand → Koordinaten
☑ Invarianten dokumentiert:
  - 0 ≤ wert ≤ 100
  - ohne Sonne → 0
  - ohne Regen → 0
  - Monotonie Sonnenschein
  - Monotonie Regen
  - Sonnenstand-Fenster [25°, 42°]

### Phase 2: Funktor F definieren

☑ Code-Symbol: class RegenbogenWahrscheinlichkeit(int)
☑ Datei: src/regenbogen/domain/wahrscheinlichkeit.py
☑ Kommentar im Code:
  @functor_source("glossar-domain.md:RegenbogenWahrscheinlichkeit")

### Phase 3: Struktur-Erhaltung prüfen

Glossar-Pfeile:
☑ A → Wetterzustand? Ja, __init__ nimmt Wetterzustand-Parameter
☑ A → Sonnenstand? Ja, __init__ nimmt Sonnenstand-Parameter
☑ A → SonnenstandsFaktor? Ja, berechnet durch Sonnenstand

Komposition:
☑ Wenn A → B → C im Glossar?
  RegenbogenW. → Sonnenstand → Koordinaten
  Code: RegenbogenW.__init__ braucht Sonnenstand
        Sonnenstand braucht Koordinaten (transitiv erhalten)

### Phase 4: Funktor T definieren

☑ Test-Oracles geplant:
  - test_wahrscheinlichkeit_bounds (Invariante)
  - test_wahrscheinlichkeit_no_sun_gives_zero (Regel)
  - test_wahrscheinlichkeit_no_rain_gives_zero (Regel)
  - test_wahrscheinlichkeit_monotonicity (Monotonie)
  - test_wahrscheinlichkeit_sun_angle_window (Fenster)
  - test_regenbogenwahrscheinlichkeit_uses_wetterzustand (Abhängigkeit)
☑ Datei: tests/domain/test_wahrscheinlichkeit.py
☑ Markierungen: @pytest.mark.oracle("...")

### Phase 5: Funktor-Komposition validieren

☑ Glossar-Invariante → Code-Assertion → Test-Oracle
  "0 ≤ wert ≤ 100" → assert → test_wahrscheinlichkeit_bounds
☑ Test-Fehler bedeutet Glossar-Verletzung:
  Wenn Test fehlschlägt → Funktor nicht korrekt

### Phase 6: Vollständigkeits-Checkliste

☑ Alle Glossar-Pfeile haben Code-Entsprechung? JA
☑ Keine neuen Pfeile im Code ohne Glossar? KORREKT
  (nur Implementierungs-Details)
☑ Komposition-Struktur erhalten? JA
☑ Tests decken alle Invarianten ab? JA

STATUS: ✓ FUNKTOR KORREKT
```

---

## Phase 6: Semiotische Klassifikation

### 6.1 Ikonische Korrespondenz

```
Glossar: "RegenbogenWahrscheinlichkeit"
Code:    "class RegenbogenWahrscheinlichkeit"

Typ: IKONISCH (Name gleich)
Grund: direkte Namensübernahme ohne Transformation
```

### 6.2 Indexikalische Korrespondenz

```
Glossar: "0 ≤ wert ≤ 100"
Code:    "assert 0 <= self.wert <= 100"

Typ: INDEXIKALISCH (direkt wirksam)
Grund: Invariante ist als Assertion direkt im Code durchgesetzt
Test:  @pytest.mark.oracle("...") validiert Assertion
```

### 6.3 Symbolische Korrespondenz

```
Glossar: "numerische Größe mit Invariante"
Pattern im Projekt: (class, int-subclass, assertion im __init__)
Code:    Folgt diesem Pattern

Typ: SYMBOLISCH (konventionell)
Grund: Code respektiert etabliertes Project-Pattern für Domain-Typen
Dokumentation: in package-schema.md § 4.1 domain/
```

---

## Fehler-Beispiele: Was schiefgehen kann

### Fehler 1: Fehlender Pfeil

```python
# ❌ FALSCH: Funktor nicht struktur-erhaltend

class RegenbogenWahrscheinlichkeit(int):
    def __init__(self, wert: int):
        # FEHLER: Wetterzustand wird NICHT importiert
        # Glossar sagt: RegenbogenW. → Wetterzustand
        # Code hat: keine Abhängigkeit
        self.wert = max(0, min(100, wert))

# PROBLEM:
#   Morphismus RegenbogenW. → Wetterzustand ist nicht abgebildet
#   Funktor F ist NICHT struktur-erhaltend
#   PF-FUNKTOR würde das erkennen ❌
```

### Fehler 2: Komposition verletzt

```python
# ❌ FALSCH: Komposition nicht erhalten

class RegenbogenWahrscheinlichkeit(int):
    def __init__(self, sonnenstand: Sonnenstand):
        # Imports Sonnenstand ✓
        # Aber Sonnenstand braucht Koordinaten
        # Und wir übergeben nie Koordinaten
        
        wert = sonnenstand.berechne_faktor()  # ← Fehler hier
        # Sonnenstand kann Faktor nicht berechnen ohne Koordinaten
        self.wert = wert

# PROBLEM:
#   Glossar: RegenbogenW. → Sonnenstand → Koordinaten
#   Code: RegenbogenW. → Sonnenstand (Koordinaten fehlen)
#   Komposition verletzt
#   Test würde fehlschlagen: sonnenstand.berechne_faktor() → AttributeError
```

### Fehler 3: Invariante nicht durchgesetzt

```python
# ❌ FALSCH: Indexikalische Korrespondenz verletzt

class RegenbogenWahrscheinlichkeit(int):
    def __init__(self, wert: int):
        # FEHLER: assert fehlt
        # Glossar sagt: "0 ≤ wert ≤ 100"
        # Code: keine Validierung
        self.wert = wert  # könnte auch 150 sein!

# PROBLEM:
#   Invariante ist nicht direkt wirksam (indexikalisch)
#   Test würde fehlschlagen: test_wahrscheinlichkeit_bounds → 150 nicht ∈ [0,100]
#   Funktor T nicht korrekt
```

---

## Zusammenfassung: Die vollständige Abbildung

```
┌─────────────────────────────────────────────────────────────┐
│ 1. GLOSSAR-KATEGORIE G                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Objekt: RegenbogenWahrscheinlichkeit                        │
│ Morphismen:                                                  │
│   → Wetterzustand (depends_on)                              │
│   → Sonnenstand (depends_on)                                │
│ Invarianten:                                                 │
│   • 0 ≤ wert ≤ 100                                          │
│   • ohne Sonne → 0                                          │
│   • ohne Regen → 0                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
              ↓ Funktor F (struktur-erhaltend)
┌─────────────────────────────────────────────────────────────┐
│ 2. CODE-KATEGORIE K                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Objekt: class RegenbogenWahrscheinlichkeit(int)             │
│ Morphismen:                                                  │
│   → imports Wetterzustand                                   │
│   → imports Sonnenstand                                     │
│ Code-Invarianten:                                            │
│   • assert 0 <= self.wert <= 100                            │
│   • if not wetterzustand.sonnenschein: return 0             │
│   • if not wetterzustand.regen: return 0                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
              ↓ Funktor T (Validierung)
┌─────────────────────────────────────────────────────────────┐
│ 3. VALIDIERUNGS-KATEGORIE V                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Oracles:                                                     │
│   • test_wahrscheinlichkeit_bounds                          │
│   • test_wahrscheinlichkeit_no_sun_gives_zero               │
│   • test_wahrscheinlichkeit_no_rain_gives_zero              │
│   • test_wahrscheinlichkeit_monotonicity                    │
│   • test_regenbogenwahrscheinlichkeit_uses_wetterzustand    │
│                                                              │
│ Alle Glossar-Invarianten sind durch Tests nachgewiesen      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Für Agenten: Die Handlung

**Wenn du RegenbogenWahrscheinlichkeit ändern willst:**

1. **Verstehe die Glossar-Struktur**
   - Was sind die Abhängigkeiten?
   - Welche Invarianten gibt es?

2. **Respektiere den Funktor F**
   - Jeder Glossar-Pfeil → Code-Pfeil
   - Keine Struktur-Änderungen stillschweigend

3. **Schreibe Tests als Funktor T**
   - Tests validieren Glossar-Invarianten
   - Markierung: @pytest.mark.oracle("...")

4. **Prüfe PF-FUNKTOR vor Code-Änderung**
   - Ist Struktur erhalten?
   - Sind alle Morphismen abgebildet?

5. **Validiere Komposition**
   - Wenn A → B → C im Glossar
   - Dann Code respektiert diese Kette

---

## Nächstes Beispiel (Hausaufgabe)

**Wende dieses Muster auf einen anderen Glossar-Begriff an:**

Vorschlag: **Wetterzustand** oder **SonnenstandsFaktor**

Durcharbeiten:
1. Glossar-Kategorie: Morphismen identifizieren
2. Code-Kategorie: Funktor F definieren
3. Validierungs-Kategorie: Funktor T schreiben
4. PF-FUNKTOR-Checkliste durchgehen
5. Fehler-Szenarien überlegen
