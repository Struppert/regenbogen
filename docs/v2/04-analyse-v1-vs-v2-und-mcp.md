# Analyse: v1 vs. v2 + MCP-Integration

**Datum:** 2026-08-15  
**Frage:** Wird unsere Arbeit mit v2 klarer? Sicherer? Und wie passt MCP rein?  
**Status:** Strategische Analyse

---

## 🔍 Vergleich: v1 vs. v2

### v1: Das aktuelle System (Status quo)

```
Struktur (v1):

├─ AGENTS.md
│  ├─ Arbeitsmodi (ANALYSE/PLAN/AUSFUEHRUNG)
│  ├─ Abbruch-Bedingungen (H1–H10, SA1–SA6)
│  ├─ Sprechakt-Regeln
│  ├─ Pflichttests
│  ├─ Schreibrechte
│  └─ Python-Coding-Sperren
│
├─ glossar-domain.md, glossar-system.md, glossar-meta.md
│  ├─ Begriffe (Was bedeuten sie?)
│  ├─ Invarianten (Was gilt?)
│  ├─ Kompetenzfragen (Wer urteilt?)
│  └─ Projektionen (Wo sichtbar?)
│
├─ package-schema.md
│  ├─ Semantische Räume (domain, system, infrastructure)
│  ├─ Erlaubte Imports
│  ├─ Known Breaches
│  └─ G(PKG)-Definition
│
├─ tools/check_*.py
│  ├─ check_agent_docs_consistency.py
│  ├─ check_import_layers.py
│  └─ resolve_test_obligations.py
│
└─ docs/plans/[TASK].md
   ├─ Zielzustand
   ├─ Scope
   └─ Phasen
```

**Charakteristika v1:**

```
✓ Stärken:
  - Explizite Regeln (nicht implizit)
  - Evidence-System (Nachweise dokumentiert)
  - Abbruch-Garantien (H1–H10 stoppen bei Fehlern)
  - Glossare als Ontologie-Start
  - Checker für automatische Validierung

✗ Schwächen:
  - Mapping Glossar → Code nicht formalisiert
  - "Bedeutung" und "Implementierung" are separate Welten
  - Checker prüfen Struktur, nicht Korrespondenz
  - Keine Garantie, dass Code Glossar-Struktur respektiert
  - Tests prüfen Funktionalität, nicht Glossar-Invarianten
  - "Hoffnung" dass alles passt (informale Abbildung)
  - Keine explizite Dokumentation: Glossar-Objekt → Code-Symbol
  - Abbruch-Regeln helfen, aber sind reaktiv, nicht präventiv
```

**Workflow v1:**

```
1. Agent liest Glossar
   → "OK, RegenbogenWahrscheinlichkeit ist [0,100]"

2. Agent liest Regeln
   → "OK, domain/ importiert nicht infrastructure/"

3. Agent schreibt Code
   → "Macht Sinn, eine Klasse mit Assertion"

4. Agent schreibt Tests
   → "Tests prüfen, ob Wert ∈ [0,100]"

5. Checker lädt Code
   → "Import-Layer OK, Typen OK"

6. Tests laufen
   → "Alle grün"

7. Mensch prüft Code-Review
   → "Sieht gut aus"

PROBLEM: Nirgendwo wird explizit geprüft:
  "Ist die Glossar-Abhängigkeit RegenbogenW. → Wetterzustand
   auch im Code respektiert (imports Wetterzustand)?"
```

---

### v2: Das neue System (mit Kategorietheorie)

```
Struktur (v2):

LAYER 1: AGENT-PRIMING (Process)
├─ AGENTS.md (wie vorher, aber mit PF-FUNKTOR)
├─ tools/check_*.py (erweitert um check_funktor_structure.py)
└─ preflight-checkliste.md (mit Phase: Struktur-Erhaltung)

LAYER 2: PROJECT-PRIMING (Content)
├─ glossar-*.md (erweitert um Funktor-Felder)
│  ├─ Morphismen: A → B Abhängigkeiten
│  ├─ Funktor F: Glossar → Code
│  ├─ Funktor T: Code → Tests
│  └─ Peirce-Klassifikation: ikonisch/indexikalisch/symbolisch
│
├─ package-schema.md (wie vorher, mit Funktor-Mapping)
│
└─ Neue Tools
   └─ tools/check_funktor_structure.py
      ├─ Für jeden Glossar-Pfeil: existiert Code-Pfeil?
      ├─ Ist Komposition erhalten?
      └─ Gibt es Code-Pfeile ohne Glossar-Quelle?

LAYER 3: TASK-PRIMING (Task)
├─ docs/plans/[TASK].md (wie vorher, mit SWS + Funktor-Check)
├─ Mandate (wie vorher)
└─ Checkpoints (wie vorher)
```

**Charakteristika v2:**

```
✓ Neue Stärken:
  - Mapping Glossar → Code strukturiert (Abhängigkeiten + Invarianten)
  - Struktur-Erhaltung ist prüfbar (nicht nur gehofft)
  - Checker können Struktur-Verletzungen erkennen (nicht nur Syntax)
  - Tests sind direkt an Glossar gebunden (@pytest.mark.oracle)
  - Vollständige Validierungskette: Glossar → Code → Tests
  - Dreiteilung ermöglicht klare Verantwortlichkeiten
  - Agent-Instruktionen werden präzise ("respektiere Abhängigkeiten")
  - Struktur-Verletzungen sind vor Commit sichtbar

✓ Erhält alle v1-Stärken:
  - Explizite Regeln
  - Evidence-System
  - Abbruch-Garantien
  - Checker für Automation

✗ Neue Anforderungen:
  - Glossar-Struktur explizit machen (Morphismen dokumentieren)
  - Checker erweitern (strukturelle Abhängigkeits-Prüfung)
  - Tests als Oracle markieren (@pytest.mark.oracle)
  - Agent muss Abhängigkeits-Logik verstehen (PF-FUNKTOR-Checkliste hilft)
```

---

## 📊 Vergleich: 7 Dimensionen

### 1. **Klarheit: Ist das System selbsterklärend?**

| Aspekt | v1 | v2 |
|--------|---|---|
| **"Was ist RegenbogenWahrscheinlichkeit?"** | Glossar-Eintrag lesen | Glossar + Morphismen + Invarianten |
| **"Wo ist das im Code?"** | Suche manuell | Glossar sagt: class RegenbogenWahrscheinlichkeit |
| **"Sind alle Abhängigkeiten in Code?"** | Hoffen, dann Code-Review | check_funktor_structure.py prüft automatisch |
| **"Validieren Tests Glossar-Invarianten?"** | Hoffen, dann lesen | @pytest.mark.oracle("") dokumentiert Bindung |
| **"Ist die Struktur erhalten?"** | Implizit | Explizit (PF-FUNKTOR Checkliste) |

**Klarheit-Gewinn:** Sehr hoch — Abhängigkeiten sind nicht mehr implizit

---

### 2. **Sicherheit: Kann das System Fehler erkennen?**

| Fehler | v1 erkennt? | v2 erkennt? |
|--------|---|---|
| **Glossar-Pfeil fehlt im Code** | ❌ Nein (Code-Review) | ✓ Ja (check_funktor_structure.py) |
| **Code-Pfeil ohne Glossar** | ❌ Nein (implizit ok) | ✓ Ja (Funktor-Checker) |
| **Komposition verletzt** | ❌ Nein (meist zu spät) | ✓ Ja (transitiv-Check) |
| **Test validiert nicht Glossar** | ⚠️ Implizit (Code-Review) | ✓ Ja (@pytest.mark.oracle) |
| **Invariante nicht durchgesetzt** | ⚠️ Test kann fehlschlagen | ✓ Assertion + oracle-Marking |

**Sicherheit-Gewinn:** ⭐⭐⭐⭐⭐ (sehr hoch, präventiv statt reaktiv)

---

### 3. **Wartbarkeit: Ist das System leicht zu ändern?**

| Szenario | v1 | v2 |
|----------|---|---|
| **Glossar-Begriff hinzufügen** | Eintrag schreiben | + Morphismen + Funktor dokumentieren |
| **Glossar-Abhängigkeit ändern** | Code-Review notwendig | Checker zeigt automatisch Fehler |
| **Code-Refactoring** | Glossar/Code/Tests manuell abgleichen | PF-FUNKTOR-Checkliste strukturiert die Arbeit |
| **Neuer semantischer Raum** | Manual konzipieren | Dreiteilung gibt Struktur vor |

**Wartbarkeit-Gewinn:** Qualitativ besser durch explizite Struktur; Quantitativ abhängig von Projekt.

---

### 4. **Skalierbarkeit: Funktioniert das über viele Projekte?**

| Aspekt | v1 | v2 |
|--------|---|---|
| **Template-Reuse** | AGENTS.md ist reusable | AGENTS.md + PF-FUNKTOR ist reusable |
| **Glossar-Patterns** | Pro Projekt neu denken | Funktoren-Pattern ist universal |
| **Fehler-Klassen** | "Hoffen" wird zur Schuld | Fehlerklasse "Funktor verletzt" ist systematisch |
| **Neue Projekte** | ~2 Tage Setup | ~1.5 Tage (v2-Docs als Vorlage) |

**Skalierbarkeit-Gewinn:** ⭐⭐⭐⭐ (hoch, systematisch)

---

### 5. **Automatisierbarkeit: Können Tools helfen?**

| Tool | v1 kann prüfen | v2 kann prüfen |
|------|---|---|
| **check_agent_docs_consistency.py** | Struktur, Platzhalter | + Dreiteilung-Konsistenz |
| **check_import_layers.py** | Layer-Grenzen | + Funktor-Einhaltung |
| **resolve_test_obligations.py** | Test-Pflicht | + oracle-Markierung |
| **NEW: check_funktor_structure.py** | ❌ | ✓ Glossar→Code Struktur |
| **NEW: validate_funktor_composition.py** | ❌ | ✓ Komposition A→B→C |

**Automatisierbarkeit-Gewinn:** ⭐⭐⭐⭐⭐ (neue Klasse von Checks möglich)

---

### 6. **Agent-Guidance: Sind Instruktionen präzise?**

| Instruktion | v1 | v2 |
|-------------|---|---|
| **"Schreib Code für Glossar-Begriff"** | "Mach ähnlich wie der Rest" | "Respektiere Funktoren: A→B ⟹ F(A)→F(B)" |
| **"Schreib Tests"** | "Prüf Funktionalität" | "Schreib oracle-Tests für Glossar-Invarianten" |
| **"Vor Code-Änderung"** | "Wende Preflight an" | "PF-FUNKTOR: Struktur erhalten?" (6 Phasen) |
| **"Fehler erkannt"** | "Code-Review" | "check_funktor_structure zeigt was falsch" |

**Agent-Guidance-Gewinn:** ⭐⭐⭐⭐ (sehr präzise)

---

### 7. **Formale Garantien: Gibt es mathematische Zusicherungen?**

| Garantie | v1 | v2 |
|----------|---|---|
| **Keine Silent Errors** | ⚠️ Tests können falsch sein | ✓ oracle-Marking + Checker |
| **Struktur-Erhaltung** | ❌ Keine | ✓ Mathematisch definiert |
| **Komposition-Konsistenz** | ❌ Keine | ✓ T ∘ F beweisen Glossar |
| **Morphismus-Vollständigkeit** | ❌ Hoffen | ✓ Checker validiert |

**Formale-Garantien-Gewinn:** ⭐⭐⭐⭐⭐ (Qualitätssprung)

---

## 📈 Zusammenfassung: Die Verbesserung

**Effekt der Migration v1 → v2:**

- **Klarheit:** Glossar→Code-Mapping wird explizit (nicht implizit)
- **Sicherheit:** Struktur-Verletzungen werden präventiv erkannt (nicht reaktiv via Code-Review)
- **Skalierbarkeit:** Funktor-Pattern ist projektunabhängig anwendbar
- **Automatisierbarkeit:** Neue Checker-Klasse möglich (Struktur-Erhaltung, nicht nur Syntax)
- **Agent-Guidance:** Instruktionen werden präzise ("respektiere Funktoren: A→B ⟹ F(A)→F(B)")
- **Formale Garantien:** Komposition T ∘ F beweist Glossar-Invarianten (neue Qualitätsklasse)

**Kern:** v2 macht das System von "hoffentlich korrekt" zu "strukturell verifiable".

---

## 🔗 MCP-Integration: Funktoren als Services

### Was ist MCP?

**Model Context Protocol** = Standardprotokoll für Tools (JSON-RPC over stdio)

```
MCP Server (Data/Logic)
  ↑↓ (JSON-RPC via Tools + Resources)
AI Client (Claude, Agent)
```

MCP servers exposieren **Tools** (callable functions) und **Resources** (readable data), nicht HTTP-Endpunkte.

### Wie passen Funktoren in MCP?

**Funktoren können MCP-Server sein!**

```
Drei neue MCP-Server für die Dreiteilung:

1. AGENT-PRIMING-SERVER (Regeln)
   Tools:
   - get_agent_rules() → returns ANALYSE/PLAN/AUSFUEHRUNG modes + abort-codes H1–H10
   - validate_wg_mutation(mutation_spec) → checks WG-MUTATION validity
   - validate_preflight(phase: 1-6) → runs PF-* checklist phase
   Resources:
   - rules://agent/modes, rules://agent/abort-codes, rules://agent/guardrails

2. PROJECT-PRIMING-SERVER (Ontologie + Funktoren)
   Tools:
   - glossar_get_term(term: string) → returns term + morphisms + functor mappings
   - functor_validate_structure(glossar_morphisms, code_morphisms) → checks if F preserves structure
   - functor_check_composition(glossar_term, code_file, test_file) → validates T∘F chain
   Resources:
   - glossar://domain/[term], glossar://system/[term], glossar://morphisms

3. TASK-PRIMING-SERVER (Aufgaben)
   Tools:
   - get_plan_structure(task_id) → returns phases + scope
   - validate_sws_closure(sws_terms) → checks if SWS is semantically closed
   - create_checkpoint(phase: int) → record phase completion
   Resources:
   - task://plan/[id], task://scope/[id], task://mandate/[id]
```

**Wichtig:** MCP-Tools sind *synchrone, callable functions*, nicht REST-Endpunkte. Sie werden von Claude direkt aufgerufen.

---

### Praktisches Beispiel: Funktor-Server in Aktion

```
SZENARIO: Agent will RegenbogenWahrscheinlichkeit-Code schreiben

1. Agent ruft MCP-Tool auf: glossar_get_term("RegenbogenWahrscheinlichkeit")
   
   Response:
   {
     "term": "RegenbogenWahrscheinlichkeit",
     "meaning": "Prozentwert [0,100]...",
     "invariants": ["0 <= wert <= 100", "no sun → 0"],
     "morphisms": [
       {"from": "RegenbogenWahrscheinlichkeit", "to": "Wetterzustand"},
       {"from": "RegenbogenWahrscheinlichkeit", "to": "Sonnenstand"}
     ],
     "functor_f": {
       "code_symbol": "class RegenbogenWahrscheinlichkeit(int)",
       "file": "src/regenbogen/domain/wahrscheinlichkeit.py"
     },
     "functor_t": {
       "test_oracle": "test_wahrscheinlichkeit_bounds",
       "file": "tests/domain/test_wahrscheinlichkeit.py"
     }
   }

2. Agent führt PF-FUNKTOR Phase 3 durch
   MCP-Tool: validate_preflight(phase=3, glossar_term="RegenbogenWahrscheinlichkeit")
   
   Response: {status: "OK", required_morphisms_found: 2, violations: []}

3. Agent schreibt Code: class RegenbogenWahrscheinlichkeit(int): ...
   
   MCP-Tool: functor_validate_structure(
     glossar_morphisms=[{from: "RegenbogenW", to: "Wetterzustand"}],
     code_morphisms=[{from: "RainbowProb", to: "Weather"}]
   )

4. Agent schreibt Tests mit oracle-Marking
   @pytest.mark.oracle("RegenbogenWahrscheinlichkeit.invariant")
   def test_bounds(): assert 0 <= result <= 100

5. Finale Check: Composition T ∘ F
   MCP-Tool: functor_check_composition(
     glossar_term="RegenbogenWahrscheinlichkeit",
     code_file="src/regenbogen/domain/wahrscheinlichkeit.py",
     test_file="tests/domain/test_wahrscheinlichkeit.py"
   )
   
   Response: {composition_valid: true, glossar_invariant_tested: true}
     "code_projection": "assert 0 <= self.wert <= 100",
     "test_oracle": "test_wahrscheinlichkeit_bounds validates invariant",
     "chain_complete": true
   }
```

---

### Wie MCP die Arbeit ändert

```
VOR MCP (v2, manuell):

Agent: "Welche Morphismen hat RegenbogenWahrscheinlichkeit?"
→ Agent liest glossar-domain.md manuell
→ Agent sucht Funktor F manuell
→ Agent schreibt PF-FUNKTOR-Checkliste per Hand
→ Agent prüft mit check_funktor_structure.py

MIT MCP (v2 + Server):

Agent: "Welche Morphismen hat RegenbogenWahrscheinlichkeit?"
→ MCP-Server antwortet direkt (cached)
→ Agent kann direkt Code-Struktur validieren
→ PF-FUNKTOR wird automatisch in Echtzeit geprüft
→ Checker wird zum Real-Time-Service

EFFEKT:
- Glossar ist nicht nur Dokumentation, sondern lebender Service
- Funktoren sind nicht nur Konzept, sondern prüfbare Bedingungen
- Agent arbeitet gegen ein System, nicht gegen Dokumentation
```

---

## 🚀 Migration-Roadmap: v1 → v2 + MCP

### Phase 1: v2 ohne MCP (4–6 Wochen)

```
✓ Dokumentation schreiben (DONE)
□ Glossar-Funktor-Felder hinzufügen
□ PF-FUNKTOR in Checklisten
□ check_funktor_structure.py schreiben (manueller Checker)
□ 2–3 Begriffe refactorn (Pilot)
□ Learning-Matrix updaten

Ergebnis: v2 als dokumentiertes System, manuell angewendet
```

### Phase 2: MCP-Server schreiben (6–8 Wochen)

```
□ PROJECT-PRIMING-SERVER (Ontologie + Funktoren)
  ├─ glossar_get_term(term)
  ├─ functor_validate_structure(glossar_morphisms, code_morphisms)
  └─ functor_check_composition(glossar_term, code_file, test_file)

□ AGENT-PRIMING-SERVER (Regeln)
  ├─ validate_wg_mutation(spec)
  └─ validate_preflight(phase)

□ TASK-PRIMING-SERVER (Aufgaben)
  ├─ get_plan_structure(task_id)
  └─ validate_sws_closure(terms)

Ergebnis: v2 als Live-MCP-Services (JSON-RPC)
```

### Phase 3: Agent-Integration (2–4 Wochen)

```
□ Agent nutzt PROJECT-PRIMING-SERVER für Glossar-Queries
□ Agent nutzt PF-FUNKTOR über AGENT-PRIMING-SERVER
□ Echtzeit-Validierung statt Post-hoc-Checker
□ Oracle-Marking automatisch geprüft

Ergebnis: v2 + MCP als vollständiges, automatisiertes System
```

---

## 📊 Effekt: v1 vs. v2 vs. v2+MCP

| Dimension | v1 | v2 | v2+MCP |
|-----------|---|---|---|
| **Klarheit** | Implizit ("hoffen") | Explizit (Funktor-dokumentiert) | Live (MCP-queries) |
| **Sicherheit** | Reaktiv (Code-Review) | Präventiv (Checker vor Commit) | Proaktiv (Real-time während Arbeit) |
| **Wartbarkeit** | Manuell kompliziert | Strukturiert, aber noch manuell | Automatisiert |
| **Automation** | Begrenzt (Syntax-Checker) | Struktur-Checker möglich | Vollautomat |
| **Agent-Guidance** | Vague ("mach ähnlich") | Präzise (Funktor-Regeln) | Präzis + Live |
| **Komplexität** | Niedrig | Mittel-Hoch (aber dokumentiert) | Hoch (aber wert) |

**Qualitätslinie:** v1 → v2 (dokumentiert + mathematisch) → v2+MCP (live + vollautomatisiert)

---

## ✅ Fazit: Wird die Arbeit klarer? Sicherer?

### **Klarheit: JA, fundamental**

```
v1: "RegenbogenWahrscheinlichkeit ist [0,100]"
    Agent: "Irgendwie im Code wahrscheinlich..."

v2: "RegenbogenWahrscheinlichkeit ist:
     - [0,100]
     - morphisms: → Wetterzustand, → Sonnenstand
     - functor F: class RegenbogenWahrscheinlichkeit(int)
     - functor T: test_wahrscheinlichkeit_bounds
     - semiotic: ICONIC"
    Agent: "Ah, genau weiß ich was zu tun ist"

v2+MCP: Agent queries MCP-Server
        MCP sagt direkt: "Das ist deine Klasse,
                          das sind deine Tests,
                          hier sind die Struktur-Anforderungen"
        Agent: "Perfekt, ich weiß exakt was zu prüfen ist"
```

### **Sicherheit: JA, dramatisch**

```
v1: Fehler können entstehen:
    ✗ Code-Abhängigkeit vergessen (erst bei Code-Review gefunden)
    ✗ Test validiert nicht Glossar-Invariante
    ✗ Komposition gebrochen (schwer zu erkennen)
    
    Recovery: Code-Review, dann Fixes

v2: Fehler werden erkannt:
    ✓ check_funktor_structure.py zeigt fehlende Pfeile
    ✓ @pytest.mark.oracle dokumentiert Bindung
    ✓ Komposition-Checker prüft T ∘ F
    
    Recovery: Automatic via Checker vor Commit

v2+MCP: Fehler werden präventiv verhindert:
        ✓ Agent bekommt Struktur-Anforderungen live
        ✓ PF-FUNKTOR wird in Echtzeit geprüft
        ✓ Keine Silent Errors möglich
        
        Recovery: Nicht nötig, Fehler entstehen gar nicht
```

### **Arrows und MCP: PERFEKTER MATCH**

```
Funktoren (mathematisch)  = Pfeile zwischen Kategorien
                            = Struktur-Erhaltung

MCP (praktisch)          = Services die Queries beantworten
                          = Live-Daten statt Dokumente
                          
MCP + Funktoren          = Arrows werden zu Queries
                          = "Welche Pfeile hat dieser Begriff?"
                          = "Ist diese Struktur erhalten?"
                          = "Validiere Komposition T ∘ F"

Eleganz: Funktoren sind PERFECT für MCP-Modeling
```

---

## 🎯 Die Empfehlung

```
PHASE 1 (Jetzt): Nutze v2 dokumentiert (4–6 Wochen)
  - Klare Verbesserung sofort sichtbar
  - Baut Verständnis auf
  - Check-Phase gibt Feedback

PHASE 2 (Später): Baue MCP-Server (6–8 Wochen)
  - Automatisiert Validierung
  - Macht Funktoren zu Live-Queries
  - Arrows werden zu Services

ERGEBNIS: v2+MCP ist ein Qualitätssprung
  - Klarer: ✓ (Funktor-Queries statt Dokument-Lesen)
  - Sicherer: ✓ (präventiv statt reaktiv)
  - Wartbarer: ✓ (Services sind single-source-of-truth)
  - Automatisiert: ✓ (Real-time Validierung)
```

---

**TL;DR:**

| Frage | Antwort |
|-------|---------|
| Wird es klarer? | **JA** — Funktoren als explizite Abbildungen |
| Wird es sicherer? | **JA** — Struktur wird automatisch validiert |
| Passt MCP? | **PERFEKT** — Arrows = MCP-Queries |
| Sollte man machen? | **JA** — Phase 1 jetzt, Phase 2 später |
