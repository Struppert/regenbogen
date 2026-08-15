# Agent-Priming: Wartungs- und Wachstumsprinzipien

**Zweck:** Verhindert, dass AGENTS.md, Glossare und Dokumentation unkontrolliert wachsen, während ihre operative Klarheit erhalten bleibt.

**Geltung:** Template-Repository (agent-templates) und alle Instanziierungen. Diese Regeln beschreiben, wie die Infrastruktur selbst evolvieren sollte, nicht einzelne Task-Ausführungen.

---

## 1. AGENTS.md bleibt komprimiert

### Problem
AGENTS.md wächst monoton: Neue Erkenntnisse werden addiert, nie komprimiert oder umgeordnet. Nach wenigen Brownfield-Zyklen wird die Datei unmaintainable — niemand liest 50 Seiten Regeln vor jeder Aufgabe.

### Lösung: Vier Prinzipien

**A. Spezialisierung erkennen**

Vor jeder neuen Regel oder neuem Abbruch-Code (H11, H12, SA7) prüfen:
- Ist das ein Spezialfall einer bestehenden Regel (H1–H10, SA1–SA6)?
- Kann ich die bestehende Regel verallgemeinern statt einen neuen Punkt zu addieren?

**Beispiel:** Wenn H3 ("Abhängigkeit nicht dokumentiert") schon existiert, gehört "Glossar-Morphismus nicht im Code" nicht als H11, sondern als Präzisierung von H3.

**B. Begründungen auslagern**

AGENTS.md ist eine Policy, nicht eine Erklärung. "Warum" gehört nicht inline.

```
FALSCH (macht Datei fett):
H7: Glossar-Begriff ohne Morphismen
    Grund: Saussure zeigte, dass Bedeutung aus Unterscheidungen
    entsteht. Ohne Morphismen wissen wir nicht, worauf der Begriff ankommt...
    
RICHTIG (Datei bleibt knapp):
H7: Glossar-Begriff ohne dokumentierte Morphismen.

(Die Erklärung steht in learning-matrix.md oder erfahrungsbericht-protokoll.md)
```

**C. Guardrails kapseln**

Spezialisierte, projekt-unabhängige Regeln (z.B. "keine erfundenen Aufwandsschätzungen", "keine unbelegte Sicherheitssprache") in separate Dateien:

```
AGENTS.md
├─ Kernregeln (immer geladen): Arbeitsmodi, H1–H10, WG-MUTATION
└─ Guardrails (bei Bedarf nachgeladen):
   ├─ guardrail-no-unbelieved-claims.md
   ├─ guardrail-python-specifics.md
   └─ guardrail-sycophancy-defense.md
```

Referenzierung in AGENTS.md:
```
## Guardrails (siehe auch guardrail-*.md)
- Unbelegte Sicherheits-/Vollständigkeitssignale entfernen
- Python-spezifische Import-Regeln
- ...
```

**D. Kompressionszyklus**

Alle 6–12 Monate (oder nach 5+ neuen Regeln):
1. Welche H-Codes könnten zusammengefasst werden?
2. Welche Begründungen sind inline und gehören in Evidence?
3. Welche Guardrails sollten ausgelagert werden?
4. Ist die Reihenfolge noch logisch?

---

## 2. Glossare sind operative, nicht akademische Datenbanken

### Problem
Glossar-Einträge wachsen durch Begründungen, theoretische Hintergründe, Zitate. Nach der Überarbeitung von v2-Dokumentation sichtbar: Ein Eintrag wurde von fünf Zeilen (Def + Invarianten + Morphismen) auf 20 Zeilen (+ Saussure, + Tesnière, + Lakoff).

### Lösung: Test-Regel für Glossar-Felder

**Jedes Feld eines Glossar-Eintrags muss sich in eine dieser Kategorien übersetzen:**

1. **Code-Annotation:** @functor_source, @invariant_check, @morphism_required
2. **Checker-Regel:** check_funktor_structure.py prüft dieses Feld
3. **Test-Oracle:** @pytest.mark.oracle prüft diesen Eintrag

Ohne eine dieser drei: Der Eintrag ist Zierde, nicht operative Semantik.

**Beispiel (richtig):**

```markdown
### RegenbogenWahrscheinlichkeit

Definition: Prozentwert [0,100], Wahrscheinlichkeit eines sichtbaren Regenbogens.

Invarianten:
  - 0 ≤ value ≤ 100              [Code: assert; Test: oracle]
  - Wenn Sonne nicht sichtbar: value = 0  [Code: assertion; Test: oracle]

Morphismen:
  - depends_on: Wetterzustand     [Code: import; Checker: transitiv-Check]
  - depends_on: Sonnenstand       [Code: import; Checker: transitiv-Check]
```

Jede Zeile hat eine Konsequenz im Code oder Test.

**Beispiel (falsch):**

```markdown
### RegenbogenWahrscheinlichkeit

Definition: ...

Theoretischer Hintergrund: 
  Saussure (1916) zeigte, dass Bedeutung aus Unterscheidungen entsteht.
  Die Morphismen zu Wetterzustand und Sonnenstand sind daher nicht optional...

[Keine Code-Konsequenz, keine Checker-Regel, kein Test-Marker]
```

Dieser Abschnitt wird raus, nicht hinein.

---

## 3. Dokumentation unterteilt sich in vier Schichten

Nicht alles gehört in AGENTS.md oder das Glossar.

**Schicht 1: Operative Policy (AGENTS.md, Glossare)**
- Checklisten, Regeln, Definitionen
- Kurz, durchsetzbar, ohne Begründung
- Gelesen vor jeder Aufgabe

**Schicht 2: Beispiele und Erfahrung (Learning-Matrix, Erfahrungsberichte)**
- "Warum" diese Regel existiert
- Fallgeschichten, Muster, Lektionen
- Nachgelesen bei Fragen oder nach Problemen

**Schicht 3: Theorie und Kontext (v2-Dokumentation)**
- Warum das System so funktioniert
- Semiotik, Linguistik, Kategorientheorie als Werkzeuge, nicht Feier
- Gelesen für tieferes Verständnis, nicht Alltagsarbeit

**Schicht 4: Design-Entscheidungen (Archivdokumente, CHANGELOG)**
- Historische Begründung ("Warum wurde H7 so und nicht anders definiert?")
- Nicht gelesen bei operativen Aufgaben, archiviert für spätere Diskussionen

**Guardrail:** Wenn ein Satz "warum" anfängt, ist wahrscheinlich die falsche Schicht aktiv.

---

## 4. Wachstum messbar machen

### Metriken (monatlich gemessen)

- **AGENTS.md Zeilenzahl:** Ziel: < 500 Zeilen (Kern + Referenzen)
- **Durchschnittliche Glossar-Eintrags-Länge:** Ziel: < 10 Zeilen (Def + Inv + Morph)
- **Regelzahl H/SA/WG:** Ziel: < 15 Regeln (Spezialisierung prüfen)
- **Begründungs-Prozentsatz in AGENTS.md:** Ziel: < 10% (Rest ausgelagert)

### Schwellenwerte für Aktionen

| Metrik | Grün | Gelb | Rot | Aktion |
|--------|------|------|-----|--------|
| AGENTS.md | < 400 Z | 400–600 Z | > 600 Z | Review + Kompression |
| Glossar-Eintrag | < 8 Z | 8–15 Z | > 15 Z | Eintrag aufteilen |
| H/SA/WG | < 12 | 12–15 | > 15 | Spezialisierung erkennen |
| Begründungen | < 5% | 5–10% | > 10% | Auslagern zu Learning-Matrix |

---

## 5. Konkrete Beispiele: Diese Überarbeitung

### RegenbogenWahrscheinlichkeit v1 (falsch)

```markdown
### RegenbogenWahrscheinlichkeit

[2 Zeilen Definition]
[3 Zeilen Invarianten]
[1 Zeile Morphismen]
[6 Zeilen: "Saussure zeigte, dass Bedeutung..."]
[4 Zeilen: "Tesnière entwickelte die Dependenzgrammatik..."]
[5 Zeilen: "Lakoff und Johnson führten Metaphern-Theorie ein..."]

→ Total: 21 Zeilen, 10 davon ohne Code-Konsequenz
```

### RegenbogenWahrscheinlichkeit v2 (richtig)

```markdown
### RegenbogenWahrscheinlichkeit

Definition: Prozentwert [0,100]...
Invarianten: 0 ≤ value ≤ 100; Sonne=falsch → value=0
Morphismen: → Wetterzustand, → Sonnenstand

→ Total: 4 Zeilen, alle operative Semantik
→ Theorie-Bezüge gehören zu v2-Docs (nicht ins operative Glossar)
```

### AGENTS.md Guardrail: Vorher vs. Nachher

**Vorher (4 Checkboxen, wirkt neu und addiert):**
```
## Guardrail: Unbelegte Sicherheits- oder Vollständigkeitssprache
☐ Zahlen ohne Messung?
☐ Theorem/Beweis für Ungeprüftes?
☐ Zitate ohne Leserzweck?
☐ Formatierung ohne Funktion?
Begründung: (5 Sätze über Sycophancy)
```

**Nachher (1 Prinzip, referenziert):**
```
## Guardrails
- Unbelegte Sicherheits-/Vollständigkeitssignale entfernen 
  (siehe guardrail-no-unfounded-claims.md)
- Python-spezifische Regeln (siehe guardrail-python.md)
- ...
```

---

## 6. Rückfluss ins Template

Diese Prinzipien gelten für das Template-Repository (agent-templates).

Nach einer Brownfield-Verschiebung oder nach Erkenntnissen aus einer Instanziierung:

1. **Beobachtung:** "Wir haben Regel H7 zum 5. Mal gebraucht"
   → Gehört sie in die Referenzimplementierung? Ja → rückfluss zu agent-templates
   
2. **Beobachtung:** "Glossar-Einträge werden immer länger"
   → box-python/glossar-meta.md anpassen, um zu zeigen, wie kurz es sein kann
   
3. **Beobachtung:** "Agent hat immer wieder Aufwandszahlen erfunden"
   → guardrail-no-unfounded-claims.md ins Template, alle Instanziierungen erben es

---

## Zusammenfassung

**Kernregel:** Operative Policy und Theorie trennen. Keine Begründungen in AGENTS.md oder Glossaren, nur in Evidence-Systemen. Jede Datei bleibt so kurz wie möglich für ihre Funktion.

**Metriken:** Überwachen, damit AGENTS.md und Glossare nicht >600 Zeilen / >15 Zeilen werden.

**Hebel gegen Wachstum:** Nicht neue Punkte addieren, sondern existierende verallgemeinern. Nicht erklären, sondern referenzieren. Nicht theoretisieren, sondern operationalisieren.

---

**Erstellt:** 2026-08-15  
**Anwendung:** Alle Instanziierungen + Template-Evoluzion  
**Review-Rhythmus:** 6–12 Monate oder nach 5+ neuen Regeln
