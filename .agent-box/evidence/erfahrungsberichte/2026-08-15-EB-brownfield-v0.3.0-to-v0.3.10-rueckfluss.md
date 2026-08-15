# Erfahrungsbericht: Brownfield-Migration v0.3.0 → v0.3.10 – Rückfluss-Analyse

Datum: 2026-08-15  
Learning-Matrix-Kandidat: ja  
Vorgeschlagene Musterkennung: GLOSSAR-OMISSION, MERGE-STRATEGIE-DEFEKT, LEGACY-PLAN-ZUSTAND  
Session-Typ: Retrospektive nach abgeschlossener Migration  
Aufgabe: Analyse der Brownfield-Migration v0.3.0 → v0.3.10 und Identifikation verallgemeinerbarer Rückflussmuster  
Ergebnis: Vier Rückfluss-Kandidaten identifiziert, strukturelle Muster erkannt  

---

## 1. Kontext: Was war die Migration und wer führte sie aus?

### Migration-Grunddaten

```
Ausgangsversion:    v0.3.0
Zielversion:        v0.3.10
Datum:              2026-06-28
Freigabeperson:     Dieter Haag
Freigabetext:       "mit der Freigabe wird ausdrücklich eine Freigabe 
                     für alle Governance-Dateien gewährt"
Scope:              Governance-Dateien, Tool-Tests, Evidence-Struktur
Nicht im Scope:     tools/instantiate/*, tutorial.md, historische Pläne
Status nach Lauf:   OK (Checker mit Warnings, Tests grün)
```

### Was die Migration erreicht hat

✓ **Gut:**
- Checkpoint-Template integriert
- 19 Erfahrungsberichte strukturiert
- 49 neue Tool-Tests hinzugefügt
- Zentrale Governance auf v0.3.10-Stand

✓ **Funktional OK:**
- 76 Produkttests grün
- Import-Layer OK (43 Dateien)
- Mypy und Ruff OK

⚠ **Mit Warnings:**
- 14 historische Pläne ohne Plan-Schema-Version
- Checker-Status: WARNINGS (nicht kritisch, aber nicht OK)

---

## 2. Rückfluss-Kandidaten: Die vier Lücken

### RC1: Glossar-Omission – 4 Einträge fehlend

**Betroffene Einträge:**
```
- Korrespondenzsatz
- Modellreview
- Oracle-Treue
- Aussenkorrespondenz
```

**Ursache:** `glossar-meta.md` wurde mit `replace/instantiate` migriert.

**Technische Kette:**
1. Template v0.3.10 enthält diese 4 Einträge
2. Regenbogen v0.3.0 hatte diese Einträge nicht
3. **Aber:** Sie waren auch lokal nicht explizit gelöscht
4. Migration: `replace` bedeutet Template-Version wird 1:1 kopiert
5. **Resultat:** Fehlende Einträge wurden nicht erkannt, weil sie lokal gar nicht vorhanden waren

**Klassifikation:** `GLOSSARY-OMISSION`  
**Impact:** MITTEL
- Nicht produktionskritisch (Einträge werden nicht verwendet)
- Aber semantisch inkonsistent (Template hat diese, Projekt nicht)
- Könnte in zukünftigen Läufen relevant werden

**Status post-fix:** Behoben (2026-08-15)

---

### RC2: Anti-Zeno – Glossar-Eintrag fehlt

**Beschreibung:** Anti-Zeno ist operative Regel (blocker-und-abbruch-protokoll.md § 6), wird aber nicht im Glossar formalisiert.

**Nachweis der Aktivität:**
```
- blocker-und-abbruch-protokoll.md § 6 → normative Regel
- AGENTS.md E4 → Erfahrungsbericht-Trigger
- Sekundärbogen-EB (2026-06-27) → praktisch angewendet
```

**Klassifikation:** `SP7-TRIGGER` (aktiv benötigter Begriff ohne ausreichenden Glossareintrag)

**Ursache:** Nicht durch die Migration eingeführt, sondern bereits in v0.3.0 bestanden geblieben. Die Migration hat Anti-Zeno nicht als Glossar-Kandidat erkannt.

**Status post-fix:** Behoben (2026-08-15)

---

### RC3: Plan-Schema-Versionen – 14 historische Pläne

**Betroffene Pläne:** 14 Planinstanzen ohne `Plan-Schema-Version: v0.3.7`

**Checker-Status:**
```
WARN: Plan-Schema-Version fehlt. Aeltere Plaene werden nur auf 
Kernfelder geprueft. Fuer vollstaendige Pruefung Plan-Schema-Version: 
v0.3.7 ergaenzen.
```

**Ursache:** Bewusste Migrationsentscheidung

Die Migration-Evidence (2026-06-28) dokumentiert:
```
"Bewusst nicht uebernommene Aenderungen:
  - historische Planinstanzen nicht auf Plan-Schema-Version v0.3.7 gehoben"
```

**Begründung:** Altpläne sind historisch, nicht aktiv. Sie zu updaten kostet Aufwand ohne aktuellen Nutzen.

**Klassifikation:** `LEGACY-DEFECT` (bewusst akzeptiert)

**Impact:** MITTEL bis HOCH (abhängig vom Use-Case)
- ✓ Für menschlich betreute Läufe OK
- ✗ Für autonome Overnight-Läufe nicht ideal
- ⚠ Checker-Status ist nicht "rot" (nicht OK), aber auch nicht "grün" (vollständig)
- ⚠ Das ist ein "schwebender Zustand" mit latenter Wartungsschuld

**Offene Frage:** Sollen historische Pläne als "Legacy-only, nicht aktiv" klassifiziert werden? Oder sollen sie nachgezogen werden?

---

### RC4: Merge-Strategie-Fehler – replace statt merge

**Beobachtung:** `glossar-meta.md` wurde mit Aktion `replace/instantiate` migriert.

**Pattern:**
```
Zu bewertende Glossare:

glossar-domain.md   → merge (lokal als Basis)       ✓ korrekt
glossar-system.md   → merge (lokal als Basis)       ✓ korrekt
glossar-meta.md     → replace/instantiate            ✗ zu breit
glossar-README.md   → replace/instantiate            ✗ zu breit
```

**Problem:**

`replace` funktioniert wie:
```python
lokal = ""
target = copyfile(template_version)
```

Das bedeutet:
- Neue Template-Einträge → werden kopiert (manchmal richtig)
- Lokale Ergänzungen → gehen verloren (immer falsch)
- Entries nur lokal gelöscht → werden wiederhergestellt (manchmal falsch)

**Hätte sein sollen:**

```
glossar-meta.md → merge (lokal als Basis)
```

Das bedeutet:
- Template-Neuerungen können nachgeladen werden (manuell)
- Lokale Glossareinträge bleiben erhalten
- Entscheidung über Neuerungen bleibt beim Projekt

**Klassifikation:** `MERGE-STRATEGIE-DEFEKT`

**Impact:** MITTEL
- Betrifft 2 Dateien (glossar-meta.md, glossar-README.md)
- Könnte zu Datenverlust führen bei lokalen Glossar-Erweiterungen
- Ist für v0.3.0 → v0.3.10 kein akutes Problem, aber Muster-Fehler

---

## 3. Rückfluss-Prioritäten und Zielmodell

### Was sollte sich ändern?

#### **Template-Ebene (box-python v0.3.10+)**

**Verallgemeinerter Kern:** Brownfield-Migrationen sollten zwischen verschiedenen Datei-Typen unterscheiden.

| Datei-Typ | Aktion | Begründung |
|-----------|--------|-----------|
| operative Regeln (AGENTS.md) | replace | Neue Regeln sollen geladen werden |
| semantische Räume (package-schema.md) | merge lokal als Basis | lokale Struktur kann abweichen |
| Glossare (glossar-*.md) | merge lokal als Basis | lokale Einträge können ergänzt sein |
| Tests (tools/tests/) | merge | neue Tests sollen geladen werden |
| Artefakt-Vorlagen (checkpoint-template.md) | add | neu in der Version |

**Offene Frage für Template-Entwicklung:**
- Sollte der Konsistenzchecker `replace` vs. `merge` validieren?
- Sollte es eine Checkliste für Merge-Strategien geben?

#### **Regenbogen-Ebene (sofort machbar)**

✓ **Umgesetzt (2026-08-15):**
- Glossar-Omission behoben (4 Einträge + Anti-Zeno)

⏳ **Offen – Entscheidung nötig:**
- RC3: Behandlung historischer Pläne
  - Option A: Plan-Schema-Version v0.3.7 für alle 14 Pläne (Aufwand: ~30 min)
  - Option B: Pläne als "Legacy-only" klassifizieren, nicht updaten (Aufwand: ~10 min)

---

## 4. Detaillierte Analyse: Warum die Lücken entstanden

### Warum RC1 (Glossar-Omission) nicht auffiel

**Erkennungskette:**
```
Preflight der Migration:
  ✓ check_agent_docs_consistency.py → OK
  ✓ check_import_layers.py → OK (38 Dateien)
  ✓ resolve_test_obligations.py → OK

Was die Checks nicht prüfen:
  ✗ "Haben wir alle Template-Glossar-Einträge?"
  ✗ "Fehlen operative Regeln im Glossar?"
  ✗ "Sind Glossar-Einträge im Merge verloren gegangen?"
```

**Grund:** Die Checks prüfen Struktur und Konsistenz, nicht Vollständigkeit gegen Template.

**Hätte aufgefallen wenn:**
- Ein Checker würde `glossar-meta.md` gegen Template validieren
- Die Migration-Evidence würde Glossar-Vergleiche dokumentieren
- Ein "Glossar-Diff Template vs. Projekt" gemacht würde

---

### Warum Anti-Zeno nicht glossarisiert war

**Historischer Grund:**
- v0.2.7 → v0.3.0 Migration (2026-06-27) hat Anti-Zeno eingeführt
- Einführung erfolgte durch `blocker-und-abbruch-protokoll.md` § 6 (Regel)
- **Aber:** Der Glossareintrag wurde "später machen" (ist nie passiert)
- v0.3.0 → v0.3.10 Migration (2026-06-28) hat das übernommen, ohne Lücke zu schließen

**Das ist ein Integrations-Muster:**
```
neue operative Regel wird eingeführt
  → Glossar-Eintrag wird "später" gemacht
  → Nächste Migration übernimmt Regel ohne Glossar
  → Lücke wird strukturell
```

---

### Warum die Merge-Strategie-Wahl getroffen wurde

**Migration-Evidence dokumentiert:**
```
glossar-meta.md | replace/instantiate | Template | abgeschlossen
```

**Vermutete Gründe (nicht explizit dokumentiert):**
1. "glossar-meta.md ist rein vom Template" (falsch – es kann lokal Einträge haben)
2. "replace ist schneller als merge" (technisch richtig, aber Risiko höher)
3. "Lokale Divergenz war nicht bekannt" (plausibel – lokal sind keine einträge ergänzt worden)

---

## 5. Muster für Learning-Matrix

### M1: Glossar-Omission bei Template-Migrationen

**Muster:** Template wird migriert, aber nicht alle neuen Glossar-Einträge werden geladen.

**Auslöser:**
- `replace/instantiate` Aktion auf Glossare
- Keine explizite Validierung gegen Template
- Glossare als "lokal spezifisch" behandelt, obwohl Template-Basis

**Hätte vermieden werden können:**
```
Option A: Merge statt Replace
  glossar-meta.md | merge | lokal als Basis | prüfung auf Template-Diff
  
Option B: Explizite Glossar-Validierung
  python check_glossar_against_template.py glossar-meta.md
```

**Rückfluss:** Template sollte bessere Migrate-Strategie-Guidance haben.

---

### M2: SP7-Trigger als Lückenmelder

**Muster:** Operative Regel wird eingeführt, aber Glossareintrag kommt später (kommt nie).

**Erkennungsmuster:**
- Regel existiert in blocker-und-abbruch-protokoll.md
- Regel wird in AGENTS.md referenziert
- Aber kein Glossareintrag
- → SP7-Trigger (fehlender Glossareintrag für aktiv benötigten Begriff)

**Hätte vermieden werden können:**
```
Review-Checkliste:
  ☐ Neue Regel in blocker-und-abbruch-protokoll.md?
  ☐ Neue Regel braucht Glossareintrag?
  ☐ Glossareintrag vor oder parallel mit Regel hinzufügen?
```

---

### M3: Schwebende Zustände nach Brownfield-Migrationen

**Muster:** Einige Artefakte werden nicht migriert → bleiben im "Warning-Zustand".

**Beispiel:** 14 historische Pläne ohne Plan-Schema-Version
```
Status nach Migration:
  ✗ nicht rot (funktionieren noch)
  ✗ nicht grün (fehlende Felder)
  = schwebender Zustand
```

**Problem:** Checker-Warnings werden als "ok, ignorieren" behandelt.

**Hätte verhindert werden können:**
```
Klare Klassifikation vor Migration:
  Plan A: "Alle Pläne werden auf v0.3.7 gehoben" → tun oder nicht tun
  Plan B: "Altpläne sind Legacy-only" → dokumentieren, Checker anpassen
  
Nicht: "Wir migrieren, Pläne bleiben im Zustand X" 
        (ohne X zu klassifizieren)
```

---

## 6. Recommendations für die nächste Template-Version (v0.3.11+)

### Für template-repository

1. **Merge-Strategie-Matrix erstellen**
   - Welche Dateien `replace`, welche `merge`?
   - Für Glossare explizit `merge lokal als Basis`
   - In BROWNFIELD-MIGRATION.md dokumentieren

2. **Glossar-Diff-Checker entwickeln**
   ```bash
   python check_glossar_against_template.py glossar-meta.md
   ```
   - Warnt wenn Template-Einträge fehlen
   - Kann vor oder nach Migration laufen

3. **SP7-Lücken-Melder**
   - Wenn Regel in blocker-/ausfuehrungsmandat-protokoll existiert
   - Aber nicht im Glossar
   - → Warnung bei Consistency-Check

4. **Plan-Schema-Klassifikation**
   - Template sollte dokumentieren: sind historische Pläne "Legacy-only" oder "zu updaten"?
   - Checker sollte anpassbar sein für diesen Mode

---

## 7. Recommendations für Regenbogen (und ähnliche Projekte)

### Unmittelbar (vor nächster Feature-Iteration)

- [ ] Glossar-Omission-Behebung validieren
  ```bash
  python tools/check_agent_docs_consistency.py --instantiated
  ```
  Erwartet: nur Legacy-Plan-Warnings, keine Glossar-Warnungen

- [ ] Entscheidung treffen: Historische Pläne
  - Sollen sie migriert werden? → Plan-Schema-Version v0.3.7
  - Oder "Legacy-only"? → Checker-Mode adjustieren
  - Dokumentation in migration-bridges.md

### Mittelfristig

- [ ] Merge-Strategie-Review
  - Glossare: sollte immer `merge` sein
  - Dokumentieren in regelmatrix.md

- [ ] Learning-Matrix updaten
  - Die Muster M1–M3 hinzufügen
  - Mit Erkennungs-Checklisten

---

## 8. Nicht-Ziel dieses Berichts

Dieser Bericht ist **keine Kritik an der durchgeführten Migration**. Die Migration war strukturell korrekt und hat das Projekt auf v0.3.10-Stand gebracht. Der Bericht dokumentiert **Verbesserungsmuster**, die für die nächsten Migrationen oder Projekte hilfreich sein könnten.

Die Migrationsarbeit war kompetent. Die Rückfluss-Muster sind **System-Level-Beobachtungen**, nicht Fehler der Ausführung.

---

## Abschlussentscheidung

**Status der Rückfluss-Kandidaten:**

| RC | Klassifikation | Status | Nächster Schritt |
|-------|---|--------|--|
| RC1 | GLOSSARY-OMISSION | ✓ Behoben 2026-08-15 | keine |
| RC2 | SP7-TRIGGER | ✓ Behoben 2026-08-15 | keine |
| RC3 | LEGACY-DEFECT | ⏳ Offen | Entscheidung: migrate oder classify-as-legacy |
| RC4 | MERGE-STRATEGIE-DEFEKT | ⏳ Template-Level | Feedback an Template-Maintainer |

**Rückfluss an Template v0.3.10+:**
- Merge-Strategie-Matrix
- Glossar-Diff-Checker
- SP7-Lücken-Erkennung
- Plan-Schema-Klassifikation

