# Linguistische Struktur: Glossare als Sprachsysteme

**Zielgruppe:** Architekten, Glossar-Pfleger, Language-Design-Interessierte  
**Zweck:** Erklärt, wie Glossare wie **Sprachsysteme** strukturiert sind — nicht nur wie "Wörterbücher".

---

## Problem: Glossare ohne linguistische Struktur

Klassischer Fehler: Glossare werden wie Wörterbücher behandelt.

```
Falsch:
  Glossar = Sammlung unabhängiger Definitionen
  
  RegenbogenWahrscheinlichkeit: "Die Wahrscheinlichkeit eines Regenbogens"
  Farbe: "Eine Farbtönung"
  Spektrum: "Das sichtbare Licht"
  
  → Jeder Begriff isoliert. Keine Struktur.
```

**Problem:** Ohne Struktur fehlen:
- Wie hängen die Begriffe zusammen?
- Welche Begriffe sind primitiv, welche abgeleitet?
- Wo entstehen Mehrdeutigkeiten?
- Wie ändert sich ein Begriff, wenn ein anderer sich ändert?

**Unser Ansatz:** Glossare sind **Sprachsysteme** — sie folgen linguistischen Prinzipien.

---

## 1. Glossar als Sprachsystem (Saussure)

### Saussures Modell der Sprache (1916)

**Saussure:** Sprache ist ein System von Zeichen, das durch interne Beziehungen definiert ist.

```
Sprache = {Zeichen} + {Beziehungen}

nicht: Sammlung von Wörtern
sondern: Struktur von Unterscheidungen
```

**Beispiel:**

Das Wort "Rot" in Deutsch:
- Unterscheidet sich von "Blau", "Grün", etc.
- Hat eine interne Struktur (Morphem: rot + Adjektiv-Form)
- Ist Teil eines Feldes (Farbadjektive)

**Ohne die Unterscheidungen (=Morphismen) ist "Rot" sinnlos.**

### Glossare als Saussuresche Sprachsysteme

Ein Glossar ist ein Sprachsystem mit:

```
Glossar-Begriffe = Zeichen
Morphismen = interne Beziehungen zwischen Zeichen

Beispiel:
  RegenbogenWahrscheinlichkeit → abhängig von Spectrum
  Spectrum → abhängig von Wellenlänge
  Wellenlänge → primitive Größe

Diese Kette ist die linguistische Struktur.
```

**Nicht:**
```
RegenbogenWahrscheinlichkeit = Definition + Invariante
```

**Sondern:**
```
RegenbogenWahrscheinlichkeit = Definition + Invariante + Morphismen
                                          (Bedeutung kommt aus Unterscheidungen)
```

---

## 2. Semantische Felder und Paradigmen

### Semantisches Feld (Trier, 1931)

Ein semantisches Feld ist eine Gruppe von Wörtern, die sich ein bedeutungsmäßiges Gebiet teilen.

**Beispiel: Farbadjektive im Englischen**

```
Primär:    red, blue, green, yellow, orange, purple
Sekundär:  crimson, azure, lime, chartreuse
Derivativ: reddish, bluish, greenish
```

Sie sind alle unterschiedlich, aber durch ihre **gegenseitigen Unterscheidungen** definiert.

### Glossar-Felder im Projekt

Ein Projekt-Glossar organisiert sich in **semantischen Feldern**:

```
Feld A: ZEIT UND WETTER
  ├─ Niederschlag
  ├─ Temperatur
  ├─ Windgeschwindigkeit
  ├─ Regenbogen (nur wenn Bedingungen erfüllt sind)
  └─ Tageszeit

Feld B: SICHTBARKEIT
  ├─ Sichtweite
  ├─ Lichtstärke
  └─ Spektrum
```

**Saussures Prinzip angewendet:**

- "Niederschlag" hat Bedeutung nur im Kontext von Feld A (es unterscheidet sich von anderen meteorologischen Größen)
- "Spektrum" gehört zu Feld B, nicht A
- Ein Begriff kann in mehreren Feldern sein → impliziert Beziehungen zwischen Feldern

**Linguistische Konsequenz:**

Wenn wir einen Term aus einem Feld entfernen, **ändert sich die Bedeutung** aller anderen Terme im Feld.

---

## 3. Morphosyntax und Dependenzien

### Dependenzgrammatik (Tesnière, 1959)

**Tesnière:** Sätze sind nicht nur linear, sondern hierarchisch organisiert. Der Kern ist das Verb, das Argumente bindet.

```
Beispiel-Satz: "Der rote Regenbogen erscheint am Horizont"

Strukturbaum:
         erscheint (Verb)
         /    |    \
       Der  Horizont  rote Regenbogen
       (Det) (Adverbial) (Nominale Gruppe)
```

### Dependenzgrammatik in Glossaren

Ein Glossar-Begriff ist wie ein **Verb**, das Argumente bindet:

```
Glossar-Begriff: RegenbogenWahrscheinlichkeit(wahrscheinlichkeit, spektrum, wetter)

Das ist eine linguistische Struktur, nicht nur eine Definition:
- wahrscheinlichkeit = obligatorisches Argument (Dependens)
- spektrum = obligatorisches Argument
- wetter = Kontext-Dependens (wird manchmal angenommen, manchmal nicht)

Morphismus ausdrücken:
  RegenbogenWahrscheinlichkeit →[braucht] Wahrscheinlichkeit
  RegenbogenWahrscheinlichkeit →[braucht] Spektrum
  RegenbogenWahrscheinlichkeit →[braucht?] Wetter (optional)
```

**Linguistisch:**
- Dependenzen = Argument-Struktur
- Morphismen = Dependenz-Relationen (wer hängt von wem ab?)

---

## 4. Markedness und Kontext (Jakobson)

### Markedness

**Jakobson:** In einer Oppositions-Paar ist ein Glied markiert (merkmalreich) und eins unmarkiert (merkmalarm).

Beispiele:
- "Hund" (unmarkiert) vs. "Hündin" (markiert)
- "Lachen" (unmarkiert) vs. "Auflachen" (markiert)

Der markierte Form trägt *zusätzliche Information*.

### Markedness in Glossaren

```
Unmarkiert: Niederschlag (generisch)
Markiert:   Schneefall (spezifisch: Niederschlag + Temperatur < 0°C)

Unmarkiert: Farbe (generisch)
Markiert:   Spektralfarbe (spezifisch: Farbe + Wellenlänge definiert)
```

**Linguistische Struktur:**

```
Schneefall →[ist-spezialisierung] Niederschlag
Spektralfarbe →[ist-spezialisierung] Farbe

Diese Morphismen sind *linguistisch nicht optional*.
Sie sind Teil der Wort-Bildungsregeln (Morphologie).
```

**Konsequenz für Code:**

Wenn "Schneefall" im Code definiert ist, aber "Niederschlag" fehlt, ist die Glossar-Struktur verletzt.

---

## 5. Polysemie, Homonymie, Ambiguität

### Polysemie (mehrere verwandte Bedeutungen)

"Bank" in Deutsch:
- **Bank A:** Möbel zum Sitzen
- **Bank B:** Finanzinstitution

Die Bedeutungen sind **verwandt** (etymologisch, konzeptuell).

### Homonymie (mehrere unverwandte Bedeutungen)

"Schloss" in Deutsch:
- **Schloss A:** Gebäude
- **Schloss B:** Verschlussmechanismus

Keine linguistische Verwandtschaft.

### Im Glossar

Polysemie und Homonymie müssen **explizit gemacht** werden:

```
FALSCH:
  Spektrum: "Das sichtbare Licht"
  (unklar: ist es die Gesamtheit, oder eine einzelne Wellenlänge?)

RICHTIG:
  Spektrum-Gesamt: "Die Gesamtheit des sichtbaren Lichts"
  Spektrum-Komponente: "Eine einzelne Wellenlänge im Spektrum"
  
  Morphism: Spektrum-Komponente ∈ Spektrum-Gesamt
```

**Linguistische Regel:**

> Polysemie und Homonymie müssen im Glossar sichtbar sein.
> Unterschiedliche Bedeutungen = unterschiedliche Einträge + explizite Morphismen.

---

## 6. Word Formation Rules (Morphologie im Glossar)

### Morphologie

**Definition:** Regeln, nach denen Wörter aus Morphemen (kleinste bedeutungstragende Einheiten) gebildet werden.

**Beispiel: Englisch**

```
play (Morphem) + -er (Morphem) = player
play + -ing = playing
play + re- = replay
```

**Regeln:**
- -er: Agent-Suffix (wer tut X)
- -ing: Progressiv-Form (X am Laufen sein)
- re-: Wiederholung (X nochmal tun)

### Morphologie in Glossaren

Ein Glossar sollte **Wortbildungsregeln** kodifizieren:

```
Basis-Konzept: Wahrscheinlichkeit

Wortbildungsregeln:
  [Concept]_wahrscheinlichkeit = Wahrscheinlichkeit für [Concept]
  
  Anwendungen:
    Regen_wahrscheinlichkeit (Wahrscheinlichkeit für Regen)
    Schnee_wahrscheinlichkeit (Wahrscheinlichkeit für Schnee)
    Regenbogen_wahrscheinlichkeit (Wahrscheinlichkeit für Regenbogen)
```

**Linguistische Struktur:**

```
Morphem: wahrscheinlichkeit
Regel: [Wetter] + wahrscheinlichkeit
Bedeutung: Die Regel wird "transparent" — aus dem Muster ist die Bedeutung errätbar

Wenn die Regel im Glossar fehlt, ist das Glossar linguistisch unvollständig.
```

---

## 7. Metapher und Übertragung

### Konzeptuelle Metapher (Lakoff & Johnson, 1980)

Menschen verstehen abstrakte Konzepte durch **konkrete, körperliche Metaphern**.

Beispiele:
- "Zeit ist Geld" (wir "sparen" Zeit, "verschwenden" Zeit, Zeit "verfließt")
- "Argumente sind Kriege" (wir "gewinnen" Argumente, "greifen an", "verteidigen")

### Metaphern im Glossar

Jeder Domain-Glossar nutzt implizite Metaphern:

```
Meteorologie-Glossar:
  "Luft FLIESS über Land"       → Metapher: Luft ist Fluss
  "Druck WÄCHST"               → Metapher: Druck ist Pflanze
  "Front ZIEHT über Region"    → Metapher: Front ist bewegliches Objekt

Domain-Glossar für Finance:
  "Geld FLIESS zwischen Accounts"  → Metapher: Geld ist Fluss
  "Portfolio WÄCHST"               → Metapher: Portfolio ist Pflanze
```

**Linguistische Regel:**

> Metaphern müssen im Glossar kodifiziert werden, weil sie die Bedeutungsstruktur prägen.

**Beispiel: RegenbogenWahrscheinlichkeit**

Implizite Metapher im Projekt:
- "Wahrscheinlichkeit WÄCHST von 0 zu 1" → Metapher: Wahrscheinlichkeit ist Höhe/Temperatur

Code folgt dieser Metapher:
```python
if probability >= 0.5:  # Wahrscheinlichkeit ist "hoch"
    show_rainbow()      # "Jetzt ist sie groß genug"
```

Wenn die Metapher im Glossar nicht kodifiziert ist, weiß ein Agent nicht, warum `0 ≤ probability ≤ 1` die "richtige" Metapher ist.

---

## 8. Register und Stile

### Register (Variation je nach Kontext)

**Linguistik:** Register ist die Variation einer Sprache je nach sozialen Faktor:
- Formales Register: Akademisch, juristisch
- Informales Register: Alltag, Freunde
- Technisches Register: Fachsprache einer Domain

### Register in Glossaren

Ein Projekt mit mehreren Stakeholdern hat mehrere Register:

```
Geschäft-Register:
  "Niederschlagschance am Wochenende"
  "Regenbogenzeiten für Events"

Wissenschaft-Register:
  "Wahrscheinlichkeit für Wassertropfen-Suspension"
  "Lichtrechnungsbrechungs-Index und Wellenlänge"

Programmier-Register:
  "probability() -> float"
  "RainbowForecast(spectrum: Spectrum, ...)"
```

**Linguistische Regel:**

> Glossare sollten Begriffe aus mehreren Registern enthalten + explizit machen, welche Register sie bedienen.

**Problem in vielen Projekten:**

Code verwendet Programmier-Register, aber Anforderungen nutzen Business-Register. Glossar vermittelt nicht zwischen ihnen → Verständnis-Lücke.

---

## 9. Pragmatik und Kontextualisierung

### Pragmatik: Bedeutung hängt vom Kontext ab

**Austin (1962) / Searle (1969):** Worte haben nicht nur "Wahrheitsbedingungen", sondern **Verwendungsbedingungen**.

Beispiel: "Ist die Tür offen?"

- Als Frage: Bittet um Information
- Als Befehl (Ausrufezeichen): Forde auf, die Tür zu öffnen
- Als Vorwurf (Im Ton): Kritisiere, dass die Tür offen ist

**Bedeutung = Verwendung.**

### Pragmatik im Glossar

Ein Glossar-Begriff hat nicht nur eine Bedeutung, sondern **Verwendungskontexte**:

```
RegenbogenWahrscheinlichkeit:
  Definition: Wahrscheinlichkeit für Regenbogen unter Bedingungen X, Y, Z
  
  Verwendungskontexte (Pragma):
    [Context A] "Prognose": Nutzer fragt: "Wird es morgen einen Regenbogen geben?"
    [Context B] "Kalibrierung": System prüft: "Ist unser Modell korrekt?"
    [Context C] "Recherche": Analyst fragt: "Wann sind Regenbögen am häufigsten?"
  
  In jedem Kontext hat der Begriff unterschiedliche Anforderungen:
    [Context A] → braucht Echtzeit-Prognose
    [Context B] → braucht Validierungs-Metriken
    [Context C] → braucht historische Daten
```

**Linguistische Struktur:**

```
RegenbogenWahrscheinlichkeit →[verwendet-in-Kontext] Prognose
RegenbogenWahrscheinlichkeit →[verwendet-in-Kontext] Kalibrierung
RegenbogenWahrscheinlichkeit →[verwendet-in-Kontext] Recherche

Diese Morphismen sind Teil des Glossars, nicht optional.
```

---

## 10. Syntax vs. Semantik im Code

### Programmiersprachliche Struktur

Code hat eigene linguistische Struktur:

```python
def calculate_rainbow_probability(
    humidity: float,        # Argument
    angle: float,          # Argument  
    wavelength: float = 450  # Optional, mit Default
) -> float:                # Return-Typ
    """Compute probability based on optical physics."""
    assert 0 <= humidity <= 1
    # ... Berechnung ...
    return probability
```

**Linguistische Ebenen des Codes:**

| Ebene | Beispiel | Linguistischer Bezug |
|-------|---------|---|
| Syntax | `def`, `->`, `:` | Grammatik des Code |
| Semantik | `humidity: float` | Bedeutung von Parametern |
| Pragmatik | `assert 0 <= humidity` | Verwendungsbedingung prüfen |
| Morphologie | `calculate_`, `_probability` | Wortbildung |

### Glossar-Code-Isomorphie

Der Glossar sollte die **semantische Struktur** des Codes spiegeln:

```
Glossar:
  RegenbogenWahrscheinlichkeit →[abhängig von] Luftfeuchte
  RegenbogenWahrscheinlichkeit →[abhängig von] Betrachtungswinkel
  RegenbogenWahrscheinlichkeit →[abhängig von] Lichtwellenlänge (optional)

Code:
  def calculate_rainbow_probability(
      humidity,      # ← Glossar: Luftfeuchte
      angle,         # ← Glossar: Betrachtungswinkel
      wavelength = 450  # ← Glossar: Lichtwellenlänge (optional)
  )
```

**Linguistic Isomorphism:**

Wenn Glossar-Struktur ≠ Code-Struktur, dann liegt ein Verständnis-Fehler vor.

---

## 11. Die 7-Ebenen-Hierarchie einer Sprache

### Jakobsons Acht Funktionen der Sprache

(Vereinfacht zu sieben für Glossare:)

| Ebene | Funktion | Glossar-Beispiel |
|---|---|---|
| 1. Laut (Phonetik) | Wie klingt es? | Name des Begriffs |
| 2. Morphem | Wie ist es gebaut? | Morpheme: "Regen-bogen" |
| 3. Wort | Was bedeutet es? | Definition |
| 4. Satz | Wie wird es verwendet? | Morphismen (abhängig von...) |
| 5. Text | Wie passt es zusammen? | Feld-Struktur, Register |
| 6. Diskurs | Wer spricht zu wem? | Stakeholder, Kontexte |
| 7. Konvention | Was ist die Regel? | Glossar als Norm für das Projekt |

**Glossare müssen auf allen sieben Ebenen konsistent sein.**

---

## 12. Integrierteste Glossar-Struktur

### Minimal viable glossary

Ein minimales Glossar muss enthalten:

```
Pro Begriff:
  1. Name (Phonetik/Morphologie)
  2. Definition (Semantik)
  3. Invarianten (Bedeutungsgrenzen)
  4. Morphismen (Abhängigkeiten)
  5. Kontext/Register (wo wird es verwendet?)
  6. Metapher (was ist die konzeptuelle Metapher?)
  7. Wortbildungsregeln (wie entstehen verwandte Begriffe?)

Pro Glossar:
  1. Semantische Felder
  2. Markedness-Relationen (markiert/unmarkiert)
  3. Polysemie/Homonymie-Distinktionen
  4. Register
  5. Pragmatische Kontexte
```

Ohne diese Struktur ist der Glossar linguistisch **unvollständig** — und damit auch der Code.

---

## Zusammenfassung

**Glossare sind Sprachsysteme mit linguistischer Struktur:**

1. **Saussureanisch:** Bedeutung kommt aus Unterscheidungen (Morphismen), nicht aus isolierten Definitionen
2. **Dependenziell:** Begriffe haben Argument-Strukturen wie Verben
3. **Morphologisch:** Wortbildungsregeln müssen kodifiziert sein
4. **Metaphorisch:** Konzeptuelle Metaphern prägen Bedeutung
5. **Register-Sensibel:** Unterschiedliche Stakeholder, unterschiedliche Register
6. **Pragmatisch:** Verwendungskontexte verändern Bedeutung
7. **Isomorph:** Glossar-Struktur muss Code-Struktur spiegeln

Ein Agent, der diese **linguistische Struktur** respektiert, versteht nicht nur die Worte, sondern das **System** dahinter.

---

**Erstellt:** 2026-08-15  
**Thema:** Linguistik, Semantik, Glossar-Struktur  
**Nächste Lektüre:** 07-semiotische-validierung.md (Peirce-basierte Validierung)
