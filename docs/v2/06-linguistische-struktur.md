# Linguistische Struktur: Was Glossar-Design braucht

**Zielgruppe:** Glossar-Designer, Projekt-Architekten  
**Zweck:** Vier praktische Felder für jeden Glossar-Eintrag

---

## Das Problem

Glossare werden oft wie Wörterbücher behandelt: isolierte Definitionen, keine Struktur.

```
Falsch: RegenbogenWahrscheinlichkeit: "Die Wahrscheinlichkeit eines Regenbogens"
Richtig: RegenbogenWahrscheinlichkeit mit Morphismen + Invarianten + Kontext
```

Ohne Struktur fehlt: Wie hängen Begriffe zusammen? Was ist primitiv, was abgeleitet? Wo entstehen Mehrdeutigkeiten?

---

## Vier Glossar-Felder

Jeder Eintrag braucht diese vier Felder:

### 1. **Morphismen (Abhängigkeiten)**

Welche Begriffe braucht dieser Begriff? Welche Begriffe hängen von diesem ab?

```
RegenbogenWahrscheinlichkeit:
  depends_on: [Wetterzustand, Sonnenstand]
  is_used_by: [Prognose-Service, Kalibrierungs-Check]
```

**Warum:** Diese Pfeile werden zu Code-Imports. Wenn sie fehlen, kann der Checker sofort sagen: "Morphismus verletzt."

**Hintergrund (Linguistik):** Saussure zeigte, dass Bedeutung nicht in isolierten Wörtern, sondern in Unterscheidungen liegt. "RegenbogenWahrscheinlichkeit" bedeutet nur etwas im Kontext seiner Abhängigkeiten zu anderen Begriffen.

---

### 2. **Disambiguierung (Polysemie/Homonymie)**

Hat dieser Begriff mehrere Bedeutungen im Projekt? Sind sie verwandt oder unabhängig?

```
Spektrum:
  Bedeutung A: "Die Gesamtheit des sichtbaren Lichts (400-700nm)"
  Bedeutung B: "Eine einzelne Wellenlänge innerhalb des Spektrums"
  Relation: B ⊂ A (hierarchisch verwandt)

→ Notwendige Glossar-Einträge:
   - Spektrum-Gesamt
   - Spektrum-Komponente
   - Morphismus: Spektrum-Komponente → Spektrum-Gesamt
```

**Warum:** Mehrdeutige Namen crashen den Code. "Spektrum" in zwei verschiedenen Funktionen = zwei verschiedene Typen = Silent Errors.

**Hintergrund (Linguistik):** Polysemie muss explizit gemacht werden, nicht implizit angenommen.

---

### 3. **Verwendungskontext (Register/Stakeholder)**

Wer verwendet diesen Begriff? In welchen Kontexten?

```
Niederschlagschance:
  [Business] "Wird es morgen regnen?" (0-100%)
  [Science] "Wahrscheinlichkeit für Wassertropfen-Suspension" (mathematisch)
  [System] "Trigger für Event-basierte Alerts" (0 oder 1)

→ Drei Register, aber derselbe Glossar-Eintrag
```

**Warum:** Derselbe Begriff kann in verschiedenen Systemen andere Anforderungen haben. Code-Projekt nutzt Register [System], aber Anforderung kommt aus Register [Business]. Agent muss wissen, dass die Brücke existiert.

**Hintergrund (Linguistik):** Register ist Sprachvariation je nach Kontext (Halliday). Glossare müssen mehrere Register bewusst machen.

---

### 4. **Bildungsregeln (Morphologie)**

Welche Wortbildungsregeln gelten?

```
Basis: Wahrscheinlichkeit

Regel: [Phänomen] + wahrscheinlichkeit = Wahrscheinlichkeit für [Phänomen]

Beispiele:
  - Regen + wahrscheinlichkeit = Regenwahrscheinlichkeit
  - Schnee + wahrscheinlichkeit = Schneewahrscheinlichkeit
  - Regenbogen + wahrscheinlichkeit = Regenbogenwahrscheinlichkeit
```

**Warum:** Wenn die Regel im Glossar steht, weiß jeder Neue, wie man neue Begriffe nach dem gleichen Muster benennt. Das reduziert willkürliche Namenswahl.

**Hintergrund (Linguistik):** Morphologie ist die Wissenschaft von Wortbildungsregeln. Ohne Regeln entsteht semantisches Chaos.

---

## Glossar-Template

Jeder Eintrag in glossar-domain.md, glossar-system.md, glossar-meta.md sollte diese Felder haben:

```markdown
### RegenbogenWahrscheinlichkeit

**Definition:** Prozentwert [0, 100], die Wahrscheinlichkeit eines sichtbaren Regenbogens unter gegebenen Bedingungen.

**Invarianten:**
- 0 ≤ value ≤ 100
- Wenn Sonneneinstrahlung < 0°, dann value = 0

**Morphismen (Abhängigkeiten):**
- depends_on: Wetterzustand, Sonnenstand
- is_used_by: Prognose-Service

**Verwendungskontext:**
- [Business] "Regenbogenzeiten für Events"
- [System] "Trigger für Sichtbarkeitsprognose"

**Disambiguierung:**
- Keine (eindeutiger Begriff im Projekt)

**Bildungsregel:**
- Zugehörig zu Muster: [Wetter-Phänomen] + wahrscheinlichkeit
```

---

## Zusammenfassung

**Glossare sind nicht Wörterbücher — sie sind Sprachsysteme mit Struktur.**

Die vier Felder machen diese Struktur explizit:

1. **Morphismen** — wer hängt von wem ab (Pfeilrichtung)
2. **Disambiguierung** — mehrere Bedeutungen trennen (homonym-aware)
3. **Kontext** — welche Register existieren (stakeholder-aware)
4. **Bildungsregeln** — wie neue Begriffe entstehen (scalable)

Ohne diese Felder ist der Glossar unvollständig. Mit ihnen weiß jeder Agent, was zu kodieren ist.

---

**Erstellt:** 2026-08-15  
**Version:** 0.2 (gekürzt: vier praktische Felder, keine Theorie-Abschnitte ohne Konsequenz)
