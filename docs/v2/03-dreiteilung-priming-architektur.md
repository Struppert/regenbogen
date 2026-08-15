# Agent-Priming Architektur: Die Dreiteilung

**Datum:** 2026-08-15  
**Zweck:** Strukturiere Agent-Priming in drei orthogonale Schichten  
**Status:** Konzept / Pilotphase

---

## 🎯 Das Problem mit monolithischen Priming-Systemen

Ein Agent braucht drei verschiedene Arten von Information:

```
FALSCH (monolithisch):
  AGENTS.md enthält:
    - wie arbeitet der Agent (Process)
    - was bedeuten Begriffe (Content)
    - was ist die konkrete Aufgabe (Task)
  
  → Alles vermischt
  → Bei Änderungen ist unklar, was betroffen ist
  → Schwer zu reuse über Projekte hinweg
```

**Lösung:** Trennung in drei orthogonale Schichten:

```
RICHTIG (dreiteilig):

┌─────────────────────────────────────────┐
│ 1. AGENT-PRIMING                         │
│    Wie arbeitet der Agent?               │
│    (AGENTS.md + Checker)                 │
├─────────────────────────────────────────┤
│ 2. PROJECT-PRIMING                       │
│    Was bedeuten die Begriffe?            │
│    (Ontologie, Glossar, Schema)          │
├─────────────────────────────────────────┤
│ 3. TASK-PRIMING                          │
│    Was ist genau zu tun?                 │
│    (Plan, Scope, Mandate)                │
└─────────────────────────────────────────┘
```

---

## 1️⃣ AGENT-PRIMING: Wie arbeitet der Agent?

### Definition

**Agent-Priming** beschreibt die **operativen Regeln** für Agentenarbeit.

**Unabhängig vom Projekt.**

```
Agent-Priming ist projektübergreifend.
Es gilt für jeden Agenten in jedem Projekt, das diese Box nutzt.
```

### Komponenten

#### 1.1 **AGENTS.md** – Der operative Router

```markdown
# AGENTS.md

## Was gehört hier rein?

✓ Arbeitsmodi: ANALYSE | PLAN | AUSFUEHRUNG
✓ Abbruch-Bedingungen: H1–H10 (HARD), SA1–SA6 (SOFT)
✓ Wirkungsgates: WG-MUTATION
✓ Ausfuehrungsmandate: was erlaubt wann
✓ Preflight: was prüfen vor Änderung
✓ Safe Tasks: was darf Agent autonom
✓ Sprechakte: wann Mensch entscheiden
✓ Git- und Commit-Regeln
✓ Python-spezifische Coding-Sperren
✓ Guardrails gegen strukturelle Fehler

## Was gehört NICHT hier rein?

✗ Projektspezifische Begriffe (gehört zu PROJECT-PRIMING)
✗ Konkrete Aufgabenziele (gehört zu TASK-PRIMING)
✗ Spezifische Dateipfade (gehört zu PROJECT-PRIMING)
```

**Beispiel-Auszug (projektübergreifend gültig):**

```markdown
## Arbeitsmodi

Ein Auftrag erlaubt nur den eindeutig ausgesprochenen Arbeitsmodus.

ANALYSE
  Erlaubt: lesen, untersuchen, Befunde benennen
  Verboten: Repository-Mutation

PLAN
  Erlaubt: ANALYSE + Plan + Entscheidungsfragen
  Verboten: Code-Änderungen

AUSFUEHRUNG
  Erlaubt: freigegebenen Plan umsetzen
  Voraussetzung: aktives Mandat
```

---

#### 1.2 **Checker & Tools** – Die Regeln-Durchsetzung

```python
# tools/check_agent_docs_consistency.py
# Prüft: Sind die Agenten-Regeln konsistent?

# tools/check_import_layers.py
# Prüft: Werden die semantischen Räume respektiert?

# tools/resolve_test_obligations.py
# Prüft: Welche Tests sind für welche Änderungen nötig?
```

**Was Checker prüfen (Agent-Priming-Ebene):**

```
✓ Sind alle Regeldateien vorhanden?
✓ Sind Definitionen konsistent (z.B. H1–H10 in mehreren Dateien)?
✓ Sind Import-Layer-Grenzen respektiert?
✓ Sind Test-Pflichten ableitbar?
✗ Was gehört NICHT hier hin:
  - Projekt-spezifische Invarianten
  - Aufgaben-Zielzustände
```

---

#### 1.3 **Charakteristika**

```
Stabilität:       HOCH (ändert sich selten)
Wiederverwendung: JA (über alle Projekte)
Umfang:           KLEIN (nur Regeln + Checker)
Autorität:        Agent-Box-Template
```

---

## 2️⃣ PROJECT-PRIMING: Was bedeuten die Begriffe?

### Definition

**Project-Priming** beschreibt die **semantische Wahrheit** eines Projekts.

**Projekt-spezifisch.**

```
Project-Priming ist lokal autoritativ.
Es definiert, was Begriffe in DIESEM Projekt bedeuten.
```

### Komponenten

#### 2.1 **Glossare** – Die Ontologie

```markdown
# glossar-domain.md
# Fachbegriffe dieses Projekts

### RegenbogenWahrscheinlichkeit

Bedeutung: Prozentwert [0,100] für optische Plausibilität

Invarianten:
  - 0 ≤ wert ≤ 100
  - ohne Sonne → 0
  - ohne Regen → 0

Morphismen (Abhängigkeiten):
  → Wetterzustand
  → Sonnenstand
  → SonnenstandsFaktor

Funktor F (zu Code):
  Code-Symbol: class RegenbogenWahrscheinlichkeit(int)
  Datei: src/regenbogen/domain/wahrscheinlichkeit.py

Test-Oracle:
  Funktor T: tests/domain/test_wahrscheinlichkeit.py
```

---

#### 2.2 **package-schema.md** – Semantische Räume

```markdown
# package-schema.md

## Raumkarte

domain/
  Fachbegriffe (RegenbogenWahrscheinlichkeit, Wetterzustand, ...)
  Invariante: Domänenexperte kann urteilen ohne Laufzeitwissen

system/
  Betriebsregeln (Use Cases, Policies, Fehlerbehandlung)
  Invariante: Systemarchitekt urteilt ohne Plattform-Details

infrastructure/
  Technische Implementierung (HTTP, DB, Filesystem)
  Invariante: Infrastruktur-Implementierung ohne Domänenbegriffe
```

**Package-Schema beantwortet:**
- Welche Symbole dürfen wo leben?
- Welche Imports sind erlaubt?
- Welche Invarianten sind unverletzbar?

---

#### 2.3 **Charakteristika**

```
Stabilität:       MITTEL (ändert sich mit Projekt-Evolution)
Wiederverwendung: NEIN (projekt-spezifisch)
Umfang:           GROSS (vollständige Ontologie)
Autorität:        Projekt-Repository
```

---

## 3️⃣ TASK-PRIMING: Was ist genau zu tun?

### Definition

**Task-Priming** beschreibt die **konkrete Aufgabe**.

**Aufgabenspezifisch.**

```
Task-Priming ist temporär und aufgabenbezogen.
Es existiert nur für die Dauer einer konkreten Aufgabe.
```

### Komponenten

#### 3.1 **Plan** – Die Aufgaben-Spezifikation

```markdown
# Plan: Sekundärbogen-Prognose implementieren

## Semantic Working Set

Task-SWS-ID: task-sekundaerbogen-2026-06-27
Glossar-Revision: v0.3.0
Erforderliche Schliessung:
  - TERM-Sekundaerbogen
  - TERM-SonnenstandsFaktorSekundaerbogen
  - BINDING-Wahrscheinlichkeit-zu-Sekundaerbogen
  - INV-SekundaerbogenDaempfung

## Scope

Dateien betroffen:
  - src/regenbogen/domain/wahrscheinlichkeit.py
  - src/regenbogen/system/use_case.py
  - src/regenbogen/cli/main.py
  - tests/domain/test_wahrscheinlichkeit.py

Nicht betroffen:
  - Infrastructure
  - Alte Tests

## Mandate & Profile

Mandats-ID: m-sekundaerbogen-27-06
Status: aktiv
Freigebung: "OK, Glossar-Einträge gültig, Ausführung starten"

Profile:
  - Interaktionsprofil: interaktiv
  - Recovery-Profil: normal
  - Arbeitsprofil: feature
```

---

#### 3.2 **Scope** – Die Grenzen

```markdown
## Scope Specification

IN-SCOPE:
  ✓ Neue Glossar-Begriffe: Sekundaerbogen, SonnenstandsFaktorSekundaerbogen
  ✓ Code-Änderungen: domain/ + system/ + cli/
  ✓ Tests: neue Test-Oracles für Sekundaerbogen

OUT-OF-SCOPE:
  ✗ Infrastructure-Änderungen
  ✗ GUI-Implementierung
  ✗ Performance-Optimierung

Trigger-Regeln (wann vergrößert sich Scope?):
  - Neue Glossar-Begriffe entdeckt? → Sprechakt
  - Neue Räume betroffen? → Task-Schnitt prüfen
  - Abhängigkeitsexplosion? → Abbruch oder Sprechakt
```

---

#### 3.3 **Aufgaben-Struktur (Phasen)**

```markdown
## Phase 1: Sprechakt SP1 (Sekundaerbogen-Begriffe)

Blockiert Ausführung bis:
  ☐ Glossar-Einträge festgelegt
  ☐ SWS geschlossen

Freigegeben durch: SP1-Artefakt 2026-06-27-sekundaerbogen-begriffe.md

---

## Phase 2: Geometriefunktion

Blockiert durch: Phase 1 (SP1 muss grün sein)

Ziel:
  ☐ berechne_sonnenstands_faktor_sekundaerbogen() implementieren
  ☐ Tests grün
  ☐ Invarianten validiert

---

## Phase 3: Datenmodell & Use Case

Abhängig von: Phase 2

Ziel:
  ☐ PrognoseStunde.sekundaerbogen_wahrscheinlichkeit hinzufügen
  ☐ Use-Case-Berechnung erweitern
  ☐ Tests grün

---

## Phase 4: CLI-Ausgabe

Abhängig von: Phase 3

Ziel:
  ☐ CLI zeigt Sekundaerbogen-Fenster
  ☐ formatiere_tagesprognose() erweitert
  ☐ Tests grün

---

## Phase 5: Validierung

Abhängig von: Phase 4

Ziel:
  ☐ Alle 4 Checker grün
  ☐ 76+ Tests grün
  ☐ Glossar konsistent
```

---

#### 3.4 **Checkpoint & Evidence**

```markdown
## Checkpoint nach Phase 2

SWS-Zustand:
  Glossar-Revision: v0.3.0
  Initiales Task-SWS: [5 Begriffe]
  Aktuelle Revision: Phase 2

Remaining SWS:
  - Datenmodell
  - Use-Case-Integration
  - CLI-Ausgabe

Closed SWS:
  - Sekundaerbogen-Begriffe (Glossar)
  - Geometriefunktion (Code)
  - Geometrie-Tests (Validation)

SWS monoton fallend: JA ✓
```

---

#### 3.5 **Charakteristika**

```
Stabilität:       NIEDRIG (existiert nur während Aufgabe)
Wiederverwendung: NEIN (aufgabenspezifisch)
Umfang:           MITTEL (Scope + Phasen + SWS)
Autorität:        Plan-Dokument + Mandat
```

---

## 🔗 Wie die drei Teile zusammenhängen

```
┌────────────────────────────────────────────────────────┐
│ AGENT-PRIMING (Wie arbeitet der Agent?)                │
│                                                         │
│ Regeln:                                                 │
│  - ANALYSE / PLAN / AUSFUEHRUNG                        │
│  - H1–H10, SA1–SA6 (Abbrüche)                          │
│  - WG-MUTATION (Wirkungsgate)                          │
│  - PF-FUNKTOR (vor Code-Änderung)                      │
│                                                         │
│ Checker:                                                │
│  - check_agent_docs_consistency.py                     │
│  - check_import_layers.py                              │
│  - resolve_test_obligations.py                         │
└────────────────────────────────────────────────────────┘
         ↑ braucht Input von ↓
┌────────────────────────────────────────────────────────┐
│ PROJECT-PRIMING (Was bedeuten Begriffe?)               │
│                                                         │
│ Ontologie:                                              │
│  - Glossare (domain, system, meta)                     │
│  - Semantische Räume (domain, system, infrastructure)  │
│  - Funktoren (Glossar → Code → Tests)                  │
│  - Package-Schema (erlaubte Imports)                   │
│                                                         │
│ Autorität:                                              │
│  - glossar-domain.md (Fachbegriffe)                    │
│  - glossar-system.md (Betriebsbegriffe)                │
│  - package-schema.md (Raumstruktur)                    │
└────────────────────────────────────────────────────────┘
         ↑ wird verwendet in ↓
┌────────────────────────────────────────────────────────┐
│ TASK-PRIMING (Was genau ist zu tun?)                   │
│                                                         │
│ Aufgabe:                                                │
│  - Plan (Phasen, Dependencies, SWS)                    │
│  - Scope (IN / OUT / Trigger)                          │
│  - Mandate (Freigabe, Autorität)                       │
│  - Checkpoints (Phase-Übergänge)                       │
│                                                         │
│ Temporär:                                               │
│  - Existiert nur während der Aufgabe                   │
│  - Wird archiviert als Evidence                        │
│  - Inputs zu Learning-Matrix                           │
└────────────────────────────────────────────────────────┘
```

---

## 📐 Die Dreiteilung und Kategorietheorie

Wie passt die v2-Kategorietheorie in diese Dreiteilung?

```
AGENT-PRIMING (Regeln):
  ├─ "Ein Funktor F muss Struktur erhalten"
  └─ "PF-FUNKTOR prüft: A → B ⟹ F(A) → F(B)"

PROJECT-PRIMING (Ontologie):
  ├─ Glossar-Kategorie G (Begriffe + Abhängigkeiten)
  ├─ Code-Kategorie K (Symbole + Imports)
  ├─ Validierungs-Kategorie V (Tests + Oracles)
  └─ Funktoren F: G → K, T: K → V

TASK-PRIMING (konkrete Aufgabe):
  ├─ Wende Funktor F auf Glossar-Begriffe an
  ├─ Schreibe Tests als Funktor T
  ├─ Prüfe Struktur-Erhaltung mittels PF-FUNKTOR
  └─ Dokumentiere Komposition T ∘ F
```

---

## 🎬 Anwendungsablauf: Die Dreiteilung in Aktion

```
Szenario: "Implementiere Sekundaerbogen-Prognose"

┌─────────────────────────────────────────────────────────┐
│ 1. AGENT LIEST AGENT-PRIMING                            │
└─────────────────────────────────────────────────────────┘

Agent fragt: "Welche Regeln gelten für diese Arbeit?"

Antwort (aus AGENTS.md):
  - Modus: PLAN (Plan existiert) + AUSFUEHRUNG (Mandat aktiv)
  - WG-MUTATION: OK (aktives Mandat, Scope gültig)
  - PF-FUNKTOR: vor jeder Code-Änderung prüfen
  - Abbruch-Regeln: H1–H10 gelten

         ↓

┌─────────────────────────────────────────────────────────┐
│ 2. AGENT LIEST PROJECT-PRIMING                          │
└─────────────────────────────────────────────────────────┘

Agent fragt: "Was bedeuten diese Begriffe im Projekt?"

Antwort (aus Glossaren):
  - Sekundaerbogen: neuer Fachbegriff, noch nicht im Glossar
  - RegenbogenWahrscheinlichkeit: existiert, depends_on Sonnenstand
  - Sonnenstand: geometrisches Modell
  - package-schema.md: domain/ darf domain/ importieren
  - Funktor F: RegenbogenWahrscheinlichkeit → class RegenbogenWahrscheinlichkeit

         ↓

┌─────────────────────────────────────────────────────────┐
│ 3. AGENT LIEST TASK-PRIMING                             │
└─────────────────────────────────────────────────────────┘

Agent fragt: "Was genau soll ich tun?"

Antwort (aus Plan):
  - SWS: Sekundaerbogen + SonnenstandsFaktor + Tests
  - Phase 1: SP1 (Glossar-Begriffe) blockiert Phase 2
  - Phase 2: Geometriefunktion implementieren
  - Phase 3: Use-Case erweitern
  - Phase 4: CLI-Ausgabe
  - Scope: domain/ + system/ + cli/ (IN), infrastructure (OUT)
  - Mandat: aktiv, deckt glossar-domain.md

         ↓

┌─────────────────────────────────────────────────────────┐
│ 4. AGENT HANDELT (Regeln + Ontologie + Aufgabe)         │
└─────────────────────────────────────────────────────────┘

Konkrete Handlung:

Phase 1: Sprechakt SP1
  "Diese 3 neuen Glossar-Begriffe: Sekundaerbogen, ..."
  → Glossar-Einträge hinzufügen (PROJECT-PRIMING update)
  → SWS geschlossen? Ja → Phase 2 kann starten

Phase 2: Code-Änderung
  1. PF-FUNKTOR prüfen (AGENT-PRIMING):
     - Glossar-Struktur verstanden?
     - Alle Pfeile → Code-Pfeile?
  2. Implementiere Geometriefunktion
     - Benutze Funktor F: Glossar → Code
     - Respektiere package-schema.md
  3. Schreibe Tests als Funktor T
     - @pytest.mark.oracle("SekundaerbogenWahrscheinlichkeit.invariant")
     - Validiere Glossar-Invarianten
  4. Checkpoint (TASK-PRIMING):
     - SWS monoton gefallen? Ja
     - Remaining SWS: [Datenmodell, Use-Case, CLI]
     - Phase 2 COMPLETE ✓
     - Phase 3 startet

         ↓ (repeat für Phase 3, 4)

Phase 5: Validierung
  - Alle 4 Checker grün (AGENT-PRIMING: check_*)
  - Alle Tests grün (Funktor T validiert Glossar)
  - Glossar konsistent (PROJECT-PRIMING)
  - Komposition T ∘ F vollständig (v2-Framework)

Plan abgeschlossen ✓
```

---

## 📋 Checkliste: Sind alle drei Teile vorhanden?

### Vor einer Agentenaufgabe:

```markdown
## Agent-Priming (Prozess)

☐ AGENTS.md vorhanden und konsistent?
☐ Checker vorhanden und grün?
☐ Abbruch-Bedingungen dokumentiert?
☐ Wirkungsgates definiert?

## Project-Priming (Ontologie)

☐ Glossare vorhanden (domain, system, meta)?
☐ Neue Begriffe im Glossar?
☐ Package-Schema aktuell?
☐ Funktoren F dokumentiert (Glossar → Code)?
☐ Funktoren T dokumentiert (Code → Tests)?

## Task-Priming (Aufgabe)

☐ Plan vorhanden?
☐ Scope definiert (IN / OUT)?
☐ SWS geschlossen?
☐ Mandat aktiv?
☐ Phasen und Dependencies klar?

→ Nur wenn alle drei ✓:
   Agent kann arbeit
```

---

## 🎓 Lernpfad: Die Dreiteilung verstehen

### Level 1: Anfänger

1. Lese: **Dieses Dokument, § 1–3**
2. Verstehe: Die **Orthogonalität** (die drei Teile sind unabhängig)
3. Frage: "Was braucht mein Agent für diese Aufgabe?"

### Level 2: Fortgeschrittene

1. Lese: Dieses Dokument vollständig
2. Lese: **01-konzept-kategorietheorie-priming.md**
3. Implementiere: Dreiteilung in dein Projekt
4. Schreibe: Custom Checker für PROJECT-PRIMING

### Level 3: Experten

1. Verstehe: Kategorietheorie-Ebenen in der Dreiteilung
2. Designc: Neue Kategorien für dein Meta-System
3. Research: Wie könnte das generalisiert werden?

---

## 🔄 Warum diese Dreiteilung funktioniert

### Orthogonalität (unabhängig, aber zusammenhängend)

```
AGENT-PRIMING (Process)
  Nicht abhängig von: spezifischem Projekt, spezifischer Aufgabe
  Abhängig von: Agenten-Box-Regeln
  Reuse: 100% über alle Projekte

PROJECT-PRIMING (Content)
  Nicht abhängig von: spezifischer Aufgabe, Agent-Regeln (direkt)
  Abhängig von: Projekt-Spezifikation
  Reuse: projektübergreifend für Begriffe, aber Projekt-lokal verankert

TASK-PRIMING (Task)
  Abhängig von: AGENT-PRIMING (Regeln), PROJECT-PRIMING (Begriffe)
  Nicht abhängig von: anderen Aufgaben
  Reuse: NEIN (aufgabenspezifisch)
```

### Wartbarkeit

```
Wenn sich AGENTS.md ändert:
  → Nur Agent-Verhalten betroffen
  → Projekt-Ontologie bleibt gleich
  → Bestehende Tasks bleiben gültig

Wenn sich Glossar ändert:
  → Project-Semantik aktualisiert
  → Agent-Regeln bleiben gleich
  → Tasks müssen eventuell angepasst werden

Wenn sich Task-Plan ändert:
  → Nur diese Aufgabe betroffen
  → AGENT-PRIMING und PROJECT-PRIMING unverändern
```

---

## 🚀 Nächste Schritte: Dreiteilung im Projekt etablieren

### Unmittelbar (1–2 Std)

1. **Prüfe:** Sind die Drei Teile in deinem Projekt separiert?
2. **Dokumentiere:** Wo lebt was?
   ```
   Agent-Priming:   AGENTS.md + tools/check_*.py
   Project-Priming: glossar-*.md + package-schema.md
   Task-Priming:    docs/plans/[TASK].md
   ```

### Kurz-Mittel (1–2 Tage)

3. **Refactor:** Vermischte Inhalte in die richtige Schicht verschieben
4. **Validator:** Schreib einen Checker, der prüft:
   - Ist AGENTS.md projekt-unabhängig?
   - Ist Glossar vollständig?
   - Sind Task-Pläne in scope-Grenzen?

### Langfristig

5. **Learn:** Patterns dokumentieren (welche Tasks wiederholen sich?)
6. **Template:** Die Dreiteilung in neue Projekte exportieren

---

## 📊 Visuell: Die Dreiteilung

```
                    ╔════════════════════════════════════════╗
                    ║      AGENT-PRIMING (Workflow)          ║
                    ║                                        ║
                    ║  AGENTS.md → Abbruch-Regeln           ║
                    ║  checker.py → Constraints              ║
                    ║  PF-FUNKTOR → Struktur-Prüfung        ║
                    ╚════════════════════════════════════════╝
                                    ↓
                                 Input zu:
                                    ↓
┌─────────────────────╦════════════════════════╦──────────────────┐
│                     ║  PROJECT-PRIMING       ║                  │
│                     ║  (Semantik)            ║                  │
│                     ║                        ║                  │
│                     ║  glossar-*.md          ║                  │
│                     ║  package-schema.md     ║                  │
│                     ║  Funktoren F, T        ║                  │
│                     ║  Kategorie G, K, V     ║                  │
│                     ╚════════════════════════╝                  │
│                                                                 │
│  Input zu: ─────────────────────────────────────────────────→  │
│                                                                 │
│             ┌────────────────────────────────────────────────┐ │
│             ║     TASK-PRIMING (Konkrete Aufgabe)          ║ │
│             ║                                              ║ │
│             ║  Plan → Phasen, SWS, Scope                  ║ │
│             ║  Mandat → Freigabe, Autorität               ║ │
│             ║  Checkpoint → Phase-Übergänge               ║ │
│             └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Fazit: Warum diese Dreiteilung das bessere System ist

| Aspekt | Monolithisch | Dreiteilung |
|--------|---|---|
| **Klarheit** | Alles vermischt | Klar separiert |
| **Reuse** | Project-spezifisch | Agent-Rules reusable |
| **Wartbarkeit** | Änderung = großer Impact | Impact isoliert |
| **Skalierbarkeit** | Schwierig über Projekte | Template transferierbar |
| **Testbarkeit** | Schwer zu isolieren | Jede Schicht testbar |
| **Agent-Guidance** | Vage | Präzise Regeln |

---

**Status:** Dieses Konzept beschreibt die **logische Struktur**. Die konkrete Umsetzung (wo genau diese Inhalte im Projekt leben) folgt im nächsten Dokument.
