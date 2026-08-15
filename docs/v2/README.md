# Agent-Priming v2: Semiotik + Kategorietheorie

**Zweck:** Formales Rahmenwerk für die Abbildung von Glossar-Begriffen in Code mit mathematischen Garantien.

**Status:** Konzept / Pilotphase (August 2026)

---

## 🎯 Das Problem

Das aktuelle System (v1) hat ein Lücke:

```
Glossar/Ontologie (was bedeuten die Begriffe?)
    ↓ [Implizit, informell]
Code (wie werden sie kodiert?)
    ↓ [Hoffnung, dass es passt]
Tests (wurden die Invarianten verletzt?)
```

**Fehlendes Stück:** Wie wird die **Struktur** von Glossar zu Code abgebildet? Und wie wird das validiert?

---

## 💡 Die Lösung: Funktoren zwischen Kategorien

Statt informale Abbildung → **formale, strukturelle Abbildung mittels Funktoren**:

```
Glossar-Kategorie G
  (Begriffe + Abhängigkeiten)
       ↓ Funktor F (struktur-erhaltend)
Code-Kategorie K
  (Symbole + Imports)
       ↓ Funktor T (Validierung)
Validierungs-Kategorie V
  (Tests/Oracles)
```

**Wichtig:** Funktoren **erhalten Struktur** — wenn A → B im Glossar, dann F(A) → F(B) im Code.

---

## 📚 Dokumente in dieser Serie

### 1. **01-konzept-kategorietheorie-priming.md** – Die Theorie

**Zielgruppe:** Entwickler, Architekten, theoretisch Interessierte

**Inhalte:**
- Semiotik (Peirce): Zeichen und Bedeutung innerhalb einer Domäne
- Kategorietheorie: Strukturen und Pfeile zwischen Kategorien
- Funktoren: struktur-erhaltende Abbildungen
- Die drei Kategorien: Glossar | Code | Tests
- Semiotische Klassifikation (ikonisch, indexikalisch, symbolisch)
- Integration in das Projekt

**Zeitaufwand:** 30–60 Minuten zum Verstehen

**Kernfrage:** Wie bildet man Struktur formal ab?

---

### 2. **02-beispiel-regenbogenwahrscheinlichkeit.md** – Die Praxis

**Zielgruppe:** Agenten, Entwickler (hands-on learning)

**Inhalte:**
- Vollständiges Durchbeispiel: RegenbogenWahrscheinlichkeit
- Glossar-Kategorie: Objekte + Morphismen (Abhängigkeiten)
- Funktor F: Glossar → Code (mit vollständigem Code-Beispiel)
- Funktor T: Code → Tests (mit vollständigen Tests)
- Funktor-Komposition: die komplette Validierungskette
- PF-FUNKTOR-Checkliste angewendet
- Fehler-Szenarien: Was schiefgehen kann
- Semiotische Klassifikation auf das Beispiel angewendet

**Zeitaufwand:** 1–2 Stunden zum Durcharbeiten + Experimentieren

**Kernfrage:** Wie sieht das konkret aus?

---

### 3. **03-dreiteilung-priming-architektur.md** – Die Architektur

**Zielgruppe:** Architekten, Framework-Designer

**Inhalte:**
- Orthogonale Dreiteilung des Priminig-Systems
- AGENT-PRIMING (Prozess): AGENTS.md, Checker, PF-FUNKTOR
- PROJECT-PRIMING (Semantik): Glossare, Funktoren, Validierung
- TASK-PRIMING (Spezifikation): Plan, Scope, Mandate, Checkpoints
- Warum Orthogonalität (Wartung, Skalierung, Wiederverwendbarkeit)
- Interaktion der drei Schichten
- Anwendungsbeispiel

**Zeitaufwand:** 45–90 Minuten

**Kernfrage:** Wie organisiert sich das System strukturell?

---

### 4. **04-analyse-v1-vs-v2-und-mcp.md** – Die Integration

**Zielgruppe:** Architekten, Entscheidungsträger

**Inhalte:**
- Vergleich v1 (aktuelles System) vs. v2 (neues Framework) über 7 Dimensionen
- Clarity, Safety, Maintainability, Scalability, Automatability, Formal Guarantees
- MCP (Model Context Protocol) Integration:
  - Warum MCP für Funktoren ideal ist
  - Drei MCP-Services: Agent-Priming, Project-Priming, Task-Priming
  - Dreiphasen-Rollout (4-6 wk, 6-8 wk, 2-4 wk)
- Implementierungs-Roadmap
- Governance und Rückfluss in Template-System

**Zeitaufwand:** 1–2 Stunden (Details lesen)

**Kernfrage:** Wie integrieren wir das in die Praxis?

---

### 5. **05-philosophische-grundlagen.md** – Epistemologie

**Zielgruppe:** Theoretisch Interessierte, Framework-Architekten

**Inhalte:**
- Epistemologie: Wie Agenten "verstehen" ohne Psychologie
- Strukturelles vs. psychologisches Verständnis
- Korrespondentz-Modell der Wahrheit (nicht Kohärenz)
- Searles Chinese Room und semiotische Grounding
- Transzendentale Argumente (Kant): Was muss wahr sein für Priming?
- Freges Problem in der Softwarearchitektur (Sinn vs. Referent)
- Warum Philosophie in praktischer Softwareentwicklung zählt

**Zeitaufwand:** 1–2 Stunden (konzeptuell dicht)

**Kernfrage:** Warum ist dieses Framework philosophisch konsistent?

---

### 6. **06-linguistische-struktur.md** – Linguistik

**Zielgruppe:** Glossar-Designer, Language-Engineers

**Inhalte:**
- Glossare als Sprachsysteme (nicht Wörterbücher)
- Saussure: Bedeutung aus Unterscheidungen (Morphismen), nicht Objekte
- Dependenzgrammatik: Glossar-Begriffe wie Verben mit Argumenten
- Markedness: markiert vs. unmarkiert (Spezialisierung)
- Polysemie, Homonymie, Ambiguität
- Wortbildungsregeln (Morphologie) im Glossar
- Metaphern und konzeptuelle Strukturen
- Register und Kontextualisierung (mehrere Stakeholder)
- Sieben-Ebenen-Hierarchie einer Sprache
- Syntax vs. Semantik vs. Pragmatik im Code

**Zeitaufwand:** 1.5–2 Stunden

**Kernfrage:** Wie strukturieren sich Glossare wie echte Sprachsysteme?

---

### 7. **07-semiotische-validierung.md** – Semiotik in der Praxis

**Zielgruppe:** Agenten, Test-Designer, Validierungs-Architekten

**Inhalte:**
- Peirce's Zeichendreieck: Sign, Object, Interpretant
- Drei semiotische Typen: Ikonisch (Form), Indexikalisch (Kausalität), Symbolisch (Konvention)
- Ikonische Validierung: Test-Form spiegelt Glossar-Definition
- Indexikalische Validierung: Prüfung von Ursache-Wirkungs-Relationen
- Symbolische Validierung: Projekt-Konventionen und Normen
- Validierungs-Pyramide: Alle drei Ebenen braucht ein Oracle-Test
- Anti-Pattern: Validierung ohne Semiotik
- Sieben Ebenen der Validierung (Qualiszeichen bis Symbol-Index-Ikon)
- Test-Checkliste: Ist dieser Test semiotisch vollständig?
- Rückfluss ins Glossar wenn Tests brechen

**Zeitaufwand:** 2–3 Stunden (mit Code-Beispielen)

**Kernfrage:** Wie validiert man wirklich? (Nicht nur oberflächlich)

---

### 8. **08-funktoren-epistemologie.md** – Mathematische Garantien

**Zielgruppe:** Architekten, Mathematik-Interessierte

**Inhalte:**
- Was ist ein Funktor mathematisch (struktur-erhaltende Abbildung)
- Die drei Kategorien formal: Glossar (G), Code (K), Validierung (V)
- Funktor F: G → K (Glossar zu Code)
- Funktor T: K → V (Code zu Tests)
- Komposition T ∘ F: G → V (Vollständige Validierungskette)
- **Haupttheorem:** Wenn F und T Funktoren sind, ist auch T ∘ F ein Funktor
- Implikation: Mathematische Garantie für Korrektheit (nicht nur Hoffnung)
- Was "Struktur erhalten" praktisch bedeutet
- Natürliche Transformationen (Advanced)
- PF-FUNKTOR Checker: Wie man automatisch prüft, ob F wirklich ein Funktor ist
- Epistemische Schichtung durch Funktoren
- Universalität: Das Modell ist projektunabhängig

**Zeitaufwand:** 1.5–2.5 Stunden (mathematisch präzise)

**Kernfrage:** Wie können wir Korrektheit mathematisch garantieren?

---

## 🚀 Schnelleinstieg für Agenten

### Wenn du einen Glossar-Begriff in Code abbildest:

```markdown
## Checkliste: Funktor-Respekt

### 1. GLOSSAR-STRUKTUR VERSTEHEN
  ☐ Welche Abhängigkeiten hat dieser Begriff?
  ☐ Welche Invarianten gelten?
  ☐ Welche Morphismen (Pfeile) sind im Glossar?

### 2. FUNKTOR F DEFINIEREN (Glossar → Code)
  ☐ Code-Symbol eindeutig benennen
  ☐ Kommentar: @functor_source("glossar:Begriff")
  ☐ Alle Glossar-Pfeile → Code-Pfeile abgebildet?
  ☐ Struktur erhalten? (if A → B, dann F(A) → F(B))

### 3. TESTS ALS FUNKTOR T SCHREIBEN
  ☐ Test für jede Glossar-Invariante
  ☐ Markierung: @pytest.mark.oracle("glossar.invariant")
  ☐ Test validiert Glossar-Invariante direkt

### 4. KOMPOSITION PRÜFEN (T ∘ F)
  ☐ Glossar-Invariante → Code-Assertion → Test?
  ☐ Wenn Test fehlschlägt → Glossar verletzt?
  ☐ Validierungskette vollständig?

### 5. PF-FUNKTOR BESTANDEN?
  Alle Struktur-Erhaltungs-Anforderungen erfüllt?
  → JA: Code ist korrekt
  → NEIN: Sprechakt oder Abbruch
```

---

## 🔍 Wichtige Konzepte (Kurzreferenz)

| Konzept | Was es tut | Beispiel |
|---------|---|---|
| **Kategorie** | Sammlung von Objekten + Pfeilen | Glossar-Kategorie: Begriffe + Abhängigkeiten |
| **Morphismus** | Pfeil zwischen Objekten | A → B bedeutet "A hängt von B ab" |
| **Funktor** | struktur-erhaltende Abbildung zwischen Kategorien | F: Glossar → Code |
| **Struktur-Erhaltung** | Pfeile bleiben erhalten | wenn A → B, dann F(A) → F(B) |
| **Komposition** | Pfeile hintereinander | A → B → C ist eine Komposition |
| **Ikonisch** | Form-ähnlich | Name gleich: "RegenbogenWahrscheinlichkeit" |
| **Indexikalisch** | direkt wirksam | Assertion durchgesetzt: assert 0 ≤ value ≤ 100 |
| **Symbolisch** | konventionell | Pattern-Gebunden: "Domain-Entity hat __init__ assertion" |

---

## 📋 Integration in dein Projekt

### Dateien die aktualisiert werden müssen:

```
glossar-meta.md
  └─ Neue Sektion: "## 4. Funktor-Mapping"
     └─ Für jeden Begriff: Funktor F dokumentieren

glossar-domain.md, glossar-system.md
  └─ Neue Felder:
     ├─ Morphismen: [Liste von Abhängigkeiten]
     ├─ Funktor F: Zielort im Code
     ├─ Semiotischer Typ: ikonisch/indexikalisch/symbolisch
     └─ Test-Oracle: Zielort im Tests

package-schema.md
  └─ Neue Sektion: "## 9. Funktor-Mapping und Validierung"
     └─ Conventions für jeden semantischen Raum

preflight-checkliste.md
  └─ Neuer Schritt: "PF-FUNKTOR"
     └─ Struktur-Erhaltung vor Code-Änderung

AGENTS.md
  └─ Neue Instruktion: "Funktoren respektieren"
```

### Neue Tools:

```python
# tools/check_funktor_structure.py
# Checker, der prüft:
#   - Sind alle Glossar-Pfeile im Code erhalten?
#   - Ist Komposition erhalten?
#   - Gibt es Code-Pfeile ohne Glossar-Quelle?
```

---

## 🎓 Lernpfad

### Anfänger (Glossar-Nutzer)

1. Lese: **02-beispiel-regenbogenwahrscheinlichkeit.md** (Teile 1–3)
2. Lese: **07-semiotische-validierung.md** (Praktischer Teil, nicht Theorie)
3. Tu: Wende PF-FUNKTOR-Checkliste auf einen Begriff an
4. Tu: Schreibe einen semiotisch vollständigen Test
5. Frage: Agenten um Review ("Ist der Funktor korrekt? Ist der Test semiotisch?")

### Fortgeschrittene (Agenten/Architekten)

1. Lese: **01-konzept-kategorietheorie-priming.md** vollständig
2. Lese: **02-beispiel-regenbogenwahrscheinlichkeit.md** vollständig
3. Lese: **03-dreiteilung-priming-architektur.md** (Systemisches Verständnis)
4. Lese: **07-semiotische-validierung.md** (Test-Qualität)
5. Tu: Durcharbeite ein neues Beispiel (z.B. Wetterzustand)
6. Implement: Schreibe einen Checker für Funktor-Struktur

### Experten (Theory + Practice)

1. Lese: alle acht Dokumente in dieser Ordnung: 01, 02, 03, 04, 05, 06, 07, 08
2. Tiefe: **05-philosophische-grundlagen.md** (Epistemologie)
3. Tiefe: **06-linguistische-struktur.md** (Semantische Struktur)
4. Tiefe: **08-funktoren-epistemologie.md** (Mathematische Garantien)
5. Extend: Überlege Erweiterungen (z.B. Natural Transformations, Kan Extensions)
6. Research: Verknüpfe mit anderen Theorie-Ansätzen (Homotopy Type Theory, etc.)
7. Implement: MCP-Server für Funktoren (siehe 04)

---

## ⚡ Schnelle Verweisung für Agenten

**Frage: "Wie bilde ich einen Glossar-Begriff in Code ab?"**
→ Siehe: **02-beispiel-regenbogenwahrscheinlichkeit.md, Phase 1–3**

**Frage: "Was ist ein Funktor?"**
→ Siehe: **01-konzept-kategorietheorie-priming.md, § 2.3** ODER **08-funktoren-epistemologie.md, § 1–2**

**Frage: "Wie prüfe ich Struktur-Erhaltung?"**
→ Siehe: **02-beispiel-regenbogenwahrscheinlichkeit.md, Phase 5** (PF-FUNKTOR) ODER **08-funktoren-epistemologie.md, § 6**

**Frage: "Was sind ikonische vs. indexikalische Korrespondenzen?"**
→ Siehe: **02-beispiel-regenbogenwahrscheinlichkeit.md, Phase 6** ODER **07-semiotische-validierung.md, § 3–5**

**Frage: "Wie schreibe ich einen echten Oracle-Test?"**
→ Siehe: **07-semiotische-validierung.md, § 6** (Die Validierungs-Pyramide)

**Frage: "Warum ist dieses Framework epistemologisch solide?"**
→ Siehe: **05-philosophische-grundlagen.md** (ganze Lektüre, 1–2h)

**Frage: "Wie sind Glossare wie Sprachsysteme strukturiert?"**
→ Siehe: **06-linguistische-struktur.md** (ganze Lektüre, 1.5–2h)

**Frage: "Wieso sind Funktoren mathematische Garantien?"**
→ Siehe: **08-funktoren-epistemologie.md, § 3–5** (Das Haupttheorem)

**Frage: "Was ist die Dreiteilung von Agent/Project/Task Priming?"**
→ Siehe: **03-dreiteilung-priming-architektur.md**

**Frage: "Wie wird v2 in die Praxis integriert? MCP?"**
→ Siehe: **04-analyse-v1-vs-v2-und-mcp.md**

---

## 🔗 Verknüpfung mit bestehendem System

Dieses Framework ist **komplementär**, nicht ersetzend:

```
Bestehendes System (v1):
  ├─ Glossare (Semiotik auf einzelne Begriffe)
  ├─ Semantische Räume (domain, system, infrastructure)
  ├─ Import-Checker (Layer-Durchsetzung)
  ├─ Tests (Verhalten prüfen)
  └─ Evidence-System (Nachweise dokumentieren)

Neues Framework (v2):
  ├─ Funktoren (Struktur zwischen Glossar und Code)
  ├─ Korrespondenzmapping (explizite Abbildung)
  ├─ Funktor-Checker (Struktur-Erhaltung prüfen)
  ├─ Oracle-Tests (Invarianten validieren)
  └─ Peirce-Klassifikation (semiotische Typen)

Integration:
  Glossar + Funktor = vollständiges Priming-System
```

---

## 📖 Literatur-Verweise

### Semiotik und Bedeutungstheorie
- **Charles Sanders Peirce** (1896): The Definition of Pragmatic Sign — Die Basis des Zeichendreiecks
- **Umberto Eco** (1976): A Theory of Semiotics — Semiotische Theorie in großem Detail
- **Ferdinand de Saussure** (1916): Cours de Linguistique Générale — Bedeutung aus Unterscheidungen
- **Roman Jakobson** (1960): Closing Statement: Linguistics and Poetics — Markedness und Funktionen der Sprache
- Kernidee: Zeichen = Signifikant + Signifikat + Referent; Bedeutung entsteht durch Kontraste

### Kategorie- und Funktoren-Theorie
- **Saunders Mac Lane** (1971): Categories for the Working Mathematician — Das Standardwerk
- **Steve Awodey** (2010): Category Theory (Oxford Logic Guides)
- **Tom Leinster** (2014): Basic Category Theory — Moderner Zugang
- Kernidee: Struktur liegt in Morphismen, nicht Objekten; Funktoren erhalten diese Struktur

### Linguistische Struktur
- **Lucien Tesnière** (1959): Éléments de Syntaxe Structurale — Dependenzgrammatik
- **George Lakoff & Mark Johnson** (1980): Metaphors We Live By — Konzeptuelle Metaphern
- **Michael Halliday** (1978): Language as Social Semiotic — Register und Kontextualisierung
- Kernidee: Sprache ist strukturiert durch Abhängigkeiten, Metaphern und Kontext

### Epistemologie und Philosophie der KI
- **Immanuel Kant** (1781): Kritik der reinen Vernunft — Transzendentale Argumente
- **John Searle** (1980): Minds, Brains and Programs — Das Chinese Room Argument
- **Aristoteles** (~350 BC): Metaphysics — Korrespondenztheorie der Wahrheit
- **Gottlob Frege** (1892): "Über Sinn und Bedeutung" — Das Frege-Problem
- Kernidee: Verstehen ist strukturell, nicht psychologisch; Wahrheit ist Korrespondentz

### Praktische Anwendungen
- **Robert C. Martin** (2009): Clean Code — Code als Sprache
- **Eric Evans** (2003): Domain-Driven Design — Glossare und Ubiquitous Language
- Kernidee: Gutes Code-Design respektiert Glossar-Struktur

---

## 🎯 Nächste Schritte für dein Projekt

1. **Pilot:** Wende v2-Framework auf 1–2 Begriffe an (2–4 Std)
2. **Checklisten:** Integriere PF-FUNKTOR in preflight-checkliste.md
3. **Werkzeuge:** Schreibe `tools/check_funktor_structure.py`
4. **Glossare:** Füge Funktor-Felder zu glossar-domain.md hinzu
5. **Agent-Priming:** Aktualisiere AGENTS.md mit Funktor-Instruktionen
6. **Learning:** Dokumentiere Lessons in learning-matrix.md

---

## 📞 Fragen? Probleme?

**Im Projekt:**
- Sprechakt: Neue Funktor-Fragen → SP7 oder neue Kategorie?
- Glossar: Sind Morphismus-Felder für alle Begriffe nötig?
- Checker: Soll Funktor-Struktur-Prüfung mandatory sein?

**Erfahrungsbericht:**
- EB bei Pilot-Anwendung schreiben
- Muster identifizieren (welche Funktoren sind häufig?)
- Learning-Matrix aktualisieren

---

**Erstellt:** 2026-08-15  
**Version:** 0.2 (Komplette Serie: 8 Dokumente)

**Dokumente:**
- 01-konzept: Theorie (Kategorietheorie + Semiotik)
- 02-beispiel: Praxis (RegenbogenWahrscheinlichkeit)
- 03-dreiteilung: Architektur (Agent/Project/Task Priming)
- 04-analyse: Integration (v1 vs v2, MCP)
- 05-philosophische: Epistemologie (Strukturelles Verständnis)
- 06-linguistische: Semantik (Glossare als Sprachsysteme)
- 07-semiotische: Validierung (Peirce in der Praxis)
- 08-funktoren: Garantien (Mathematische Korrektheit)

**Autor:** Claude + Dieter  
**Forschungs-Kontext:** Agent-Priming als formales System (nicht nur Regenbogen-Projekt)  
**Status:** Theoretische Basis komplett; nächste Phase: MCP-Implementierung + Brownfield-Migration

---

## 🚀 Nächste Arbeitsschritte

Diese v2-Serie bildet die theoretische Basis. Um sie praktisch zu machen:

### Phase 1: Template-Integration
- v2-Dokumentation in `agent-templates/docs/v2` oder separates Verzeichnis integrieren
- `AGENTS.md` in Template mit Funktor-Regeln aktualisieren
- `preflight-checkliste.md` mit PF-FUNKTOR-Schritt erweitern

### Phase 2: Referenz-Implementierung
- `tools/check_funktor_structure.py` im Template (oder Regenbogen als Pilot)
- Oracle-Test-Marker (@pytest.mark.oracle) standardisieren
- Semiotische Test-Klassifikation toolunterstützen

### Phase 3: MCP-Services
- Agent-Priming-Server (AGENTS.md, Checker)
- Project-Priming-Server (Glossar-Funktoren)
- Task-Priming-Server (Plan, Scope, Checkpoints)

### Phase 4: Brownfield-Migration v2
- Regenbogen komplett nach v2 migrieren
- Erfahrungsbericht und Learning-Rückfluss

---

**Viel Erfolg bei der Anwendung! 🚀**
