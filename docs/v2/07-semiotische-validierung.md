# Semiotische Validierung: Drei Ebenen von Tests

**Zielgruppe:** Agenten, Test-Designer  
**Zweck:** Praktisches Framework für vollständige Oracle-Tests.

---

## Problem: Oberflächliche Tests

```
Test 1: assert isinstance(result, float)        # Nur Typ
Test 2: assert 0 <= result <= 1                 # Nur Bereich
Test 3: assert probability == 0.42 if X == "Y" # Nur ein Fall

Welcher ist "richtig"? Alle drei sind zu schwach.
```

**Antwort:** Ein echtes Oracle braucht **drei Ebenen**, nicht eine.

---

## Die Drei Ebenen

### 1. **Ikonische Ebene: Form-Struktur**

Prüft, ob die **Struktur des Tests der Glossar-Definition entspricht**.

```python
Glossar sagt: float, [0, 1], abhängig von (humidity, angle)

Test (ikonisch):
  result = func(humidity=0.8, angle=45)
  assert isinstance(result, float)    # Form: float ✓
  assert 0 <= result <= 1             # Form: Bereich ✓
  assert len(signature.parameters) == 2  # Form: zwei Parameter ✓
```

**Warum:** Wenn die Form nicht stimmt, stimmt auch der Rest nicht.

---

### 2. **Indexikalische Ebene: Kausalität**

Prüft, ob **Ursache-Wirkungs-Relationen** aus dem Glossar im Code gelten.

```python
Glossar sagt: "Höhere Luftfeuchte → höhere Wahrscheinlichkeit"

Test (indexikalisch):
  p1 = func(humidity=0.3, angle=45)
  p2 = func(humidity=0.9, angle=45)
  assert p2 > p1, "Higher humidity must increase probability"
```

**Warum:** Dieser Test beobachtet die physikalische Realität — nicht nur Typ/Bereich, sondern die Funktionsweise.

---

### 3. **Symbolische Ebene: Projekt-Konvention**

Prüft, ob **Projekt-Konventionen** eingehalten sind.

```python
Glossar sagt (Konvention): "Keine Sonne → Wahrscheinlichkeit = 0"

Test (symbolisch):
  p_no_sun = func(humidity=0.8, angle=45, sunlight_angle=-5)
  assert p_no_sun == 0, "Convention: no sun → zero probability"
```

**Warum:** Manche Regeln sind pure Konvention (dieses Projekt definiert es so), aber müssen trotzdem im Code durchgesetzt sein.

---

## Die Test-Checkliste: Vollständig

```python
@pytest.mark.oracle("glossar.RegenbogenWahrscheinlichkeit")
def test_rainbow_probability_complete():
    """
    Alle drei Ebenen: Struktur + Kausalität + Konvention
    """
    
    # IKONISCH: Form-Struktur
    result = calculate_rainbow_probability(humidity=0.8, angle=45)
    assert isinstance(result, float), "Form: returns float"
    assert 0 <= result <= 1, "Form: in range [0,1]"
    
    # INDEXIKALISCH: Kausalität
    p_low_humidity = calculate_rainbow_probability(humidity=0.3, angle=45)
    p_high_humidity = calculate_rainbow_probability(humidity=0.9, angle=45)
    assert p_high_humidity > p_low_humidity, "Index: humidity causes increase"
    
    # SYMBOLISCH: Projekt-Konvention
    p_no_conditions = calculate_rainbow_probability(humidity=0.0, angle=45)
    assert p_no_conditions == 0, "Symbol: no moisture → zero"
    
    p_any = calculate_rainbow_probability(humidity=0.5, angle=45)
    assert 0 <= p_any <= 1, "Symbol: range invariant"
```

---

## Wann ist ein Test vollständig?

| Level | Prüft | Erkannt? | Beispiel-Fehler |
|-------|-------|----------|---|
| Nur Ikonisch | Typ, Struktur | ❌ Falscher Wert, verletzte Kausalität | Code mit falscher Berechnung |
| Nur Indexikalisch | Kausalität | ❌ Typ-Fehler, Konventionsverletzung | `if condition: return -0.5` |
| Nur Symbolisch | Konvention | ❌ Kausalität verletzt | Richtige Konvention, aber falsche Physik |
| **Alle drei** | Struktur + Kausalität + Konvention | ✓ Fast alles | **Oracle-Test** |

---

## Anti-Pattern

```python
# FALSCH: Nur Type-Check
def test_simple():
    result = calculate_rainbow_probability(0.8, 45)
    assert result is not None

# FALSCH: Nur Bereichs-Check
def test_range():
    result = calculate_rainbow_probability(0.8, 45)
    assert 0 <= result <= 1

# RICHTIG: Alle drei Ebenen (siehe Test-Checkliste oben)
```

---

## Rückfluss: Wenn ein Test fehlschlägt

```
Test fehlschlägt: p2 > p1 (Indexikalisch)
  
Diagnose:
  - Glossar sagt: "Feuchte erhöht Wahrscheinlichkeit"
  - Code tut das nicht
  
Sprechakt: "Ist das Glossar falsch oder der Code?"
  
Mögliche Antwort 1: "Nein, Feuchte SINKT Wahrscheinlichkeit bei ungünstigem Winkel"
  → Update Glossar (Interaktion hinzufügen)
  
Mögliche Antwort 2: "Nein, der Code hat einen Bug in Zeile 42"
  → Fix Code
```

Der Test zeigt **exakt**, wo das Problem liegt.

---

## Zusammenfassung

**Ein Oracle-Test braucht drei Ebenen:**

1. **Ikonisch:** Form der Glossar-Definition spiegeln
2. **Indexikalisch:** Ursache-Wirkungs-Relationen prüfen  
3. **Symbolisch:** Projekt-Konventionen durchsetzen

Ohne alle drei ist der Test zu schwach. Mit allen drei wird ein Fehler sofort sichtbar.

---

**Erstellt:** 2026-08-15  
**Version:** 0.2 (gekürzt: nur die Test-Checkliste, keine Peirce-Theorie ohne Konsequenz)
