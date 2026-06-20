# Plan: Blickrichtung — wohin schauen für den Regenbogen

Status: abgeschlossen
Datum: 2026-06-20
Freigabe: 2026-06-20 (Dieter Haag)
Bearbeiter: Claude Sonnet 4.6

## Aufgabe

Das Programm soll sagen, in welche Himmelsrichtung man schauen muss.
Der Regenbogen steht immer gegenüber der Sonne:
`regenbogen_azimut = (sonnenazimut_grad + 180) % 360`

`Sonnenstand.sonnenazimut_grad` ist bereits berechnet und in `WetterErgebnis`
vorhanden — kein neuer API-Call, keine neue Infrastruktur.

Neue Ausgabe (Beispiel):
```
Wetter: Sonnenscheinanteil (70 % der Stunde), Regen (45 %)
Regenbogen: 62 %
Sichtbarkeit: 48 %
Blickrichtung: Südosten
```

---

## Betroffene Räume

```text
domain/
  Erweiterung: regenbogen_geometrie.py
  Neue Funktion: berechne_regenbogen_azimut(sonnenstand) -> float
  Neue Funktion: azimut_zu_himmelsrichtung(azimut_grad) -> str

cli/
  Erweiterung: gui_format.py — formatiere_wetter() zeigt Blickrichtung
  Evtl.:       formatiere_tagesprognose() — abhängig von SP3

tests/
  Erweiterung: tests/domain/test_regenbogen_geometrie.py (neu oder bestehend)
  Erweiterung: tests/cli/test_gui_format.py
```

---

## Nicht-Ziele

- kein neuer API-Call
- keine neue Infrastruktur
- keine GUI-Erweiterung
- keine 16-Punkt-Kompassrose (8 Himmelsrichtungen genügen, SP1-abhängig)
- kein Mondbogen

---

## Sprechakt-Entscheidungen

### SP1: Darstellung der Richtung — ENTSCHIEDEN

**Entscheidung:** Nur Bezeichnung — `"Südosten"` (SP1-A).
Kein Azimut in Grad.

### SP2: TagesPrognose — Richtung anzeigen? — ENTSCHIEDEN

**Entscheidung:** Nur für Spitzenstunde als Footer-Zeile (SP2-B).
`"Beste Chance: 15:00 — schau nach Südosten"`
Kein Umbau von `PrognoseStunde`. Kein neuer Domain-Typ.

### SP3: Granularität der Himmelsrichtung — ENTSCHIEDEN

**Entscheidung:** 16 Himmelsrichtungen (SP3-B).
N, NNO, NO, ONO, O, OSO, SO, SSO, S, SSW, SW, WSW, W, WNW, NW, NNW.

---

## Schreibrechte

```text
Erlaubt ohne Sonderfreigabe:
  src/regenbogen/domain/regenbogen_geometrie.py
  src/regenbogen/cli/gui_format.py
  tests/domain/test_regenbogen_geometrie.py
  tests/cli/test_gui_format.py
  docs/plans/
```

---

## Erwartete Änderungen

### Schritt 1 — Domain

In `domain/regenbogen_geometrie.py`:

```python
def berechne_regenbogen_azimut(sonnenstand: Sonnenstand) -> float:
    return (sonnenstand.sonnenazimut_grad + 180.0) % 360.0

def azimut_zu_himmelsrichtung(azimut_grad: float) -> str:
    # 8 Himmelsrichtungen, je 45°-Sektor
    sektoren = ["Nord", "Nordost", "Ost", "Südost", "Süd", "Südwest", "West", "Nordwest"]
    index = round(azimut_grad / 45.0) % 8
    return sektoren[index]
```

### Schritt 2 — CLI

`formatiere_wetter()` erweitern: wenn Wahrscheinlichkeit > 0, Blickrichtung ausgeben.
Bei 0 % keine Richtungsangabe (SP3-Äquivalent: kein Regenbogen → keine Richtung sinnvoll).

```python
if ergebnis.wahrscheinlichkeit > 0:
    azimut = berechne_regenbogen_azimut(ergebnis.sonnenstand)
    richtung = azimut_zu_himmelsrichtung(azimut)
    # ggf. + f" ({azimut:.0f}°)" je nach SP1
    zeilen.append(f"Blickrichtung: {richtung}")
```

TagesPrognose: abhängig von SP2-Entscheidung.

### Schritt 3 — Tests

```text
tests/domain/test_regenbogen_geometrie.py:
  - berechne_regenbogen_azimut: Sonne im Osten → Regenbogen im Westen
  - berechne_regenbogen_azimut: Sonne im Süden → Regenbogen im Norden
  - azimut_zu_himmelsrichtung: Grenzwerte der 8 Sektoren
  - azimut_zu_himmelsrichtung: 0° → "Nord", 180° → "Süd"

tests/cli/test_gui_format.py:
  - formatiere_wetter mit Wahrscheinlichkeit > 0 → enthält Blickrichtung
  - formatiere_wetter mit Wahrscheinlichkeit = 0 → keine Blickrichtung
```

---

## Testpflicht

```text
- berechne_regenbogen_azimut: geometrische Korrektheit (Sonne O → Regenbogen W)
- azimut_zu_himmelsrichtung: alle 8 Sektorgrenzen testen
- Formatter-Tests für beide Wahrscheinlichkeitszweige
- Import-/Layer-Checker nach Implementierung
```

---

## Abbruchbedingungen

```text
H2   Import-Verletzung (cli importiert domain direkt mit Typannotation)
H3   Widerspruch zwischen SP-Entscheidung und Implementierung
SA1  Test rot nach Implementierungsschritt
```

---

## Wiedereinstiegspunkt

Nach Freigabe und SP-Entscheidungen:

```text
1. Domain-Funktionen in regenbogen_geometrie.py + Tests
2. formatiere_wetter() erweitern + Tests
3. TagesPrognose (je nach SP2)
4. Vollvalidierung
```

---

## Abschlusskriterien

```text
- berechne_regenbogen_azimut und azimut_zu_himmelsrichtung implementiert und getestet
- formatiere_wetter() zeigt Blickrichtung wenn Wahrscheinlichkeit > 0
- alle Tests grün
- Import-/Layer-Checker grün
- Lint, Format, Typecheck grün
```

---

## Erfahrungsbericht

Nach Abschluss immer schreiben.

Protokoll (Format, Pflichtfelder, Ablageort): `erfahrungsbericht-protokoll.md`

Ablageort: `tmp/erfahrungsberichte/YYYY-MM-DD-EB-blickrichtung.md`
