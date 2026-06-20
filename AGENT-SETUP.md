# box-python

Agenten-Vorlage für Python-Projekte.

Diese Box wird nicht als Unterordner in ein Zielprojekt eingebunden.
Der Inhalt wird direkt in den Root des Zielprojekts kopiert und dort angepasst.

```text
box-python   = Vorlage
Projektroot  = operative Wahrheit
```

---

## Zweck

`box-python` stellt lokale Operationsregeln für KI-Agenten bereit.
Nach der Instanziierung besitzt das Zielprojekt eigene Agentenregeln,
die im Projektroot liegen und dort von KI-Agenten gelesen werden.

---

## Inhalt

```text
box-python/
  AGENT-SETUP.md                       ← dieses Dokument (Instanziierungsanleitung)
  AGENTS.md                            ← operative Hauptautorität
  AGENTS-COMPACT.md                    ← Schnelleinstieg
  grundsatz.md                         ← Theorie / Begründung des Systems
  package-schema.md                    ← Raumregeln, Importmatrix, Known Breaches
  preflight-checkliste.md              ← P1–P10 vor jeder Änderung
  task-schnitt.md                      ← Schnitt von Aufgaben und SWS
  sprechakt-protokoll.md               ← menschliche Festlegungen (SP1–SP7)
  regelmatrix.md                       ← Autoritätsreihenfolge, Drift-Regeln
  test-obligations.md                  ← Testpflicht-Matrix
  migration-bridges.md                 ← Symbolsperren und Bridge-Begriffe
  erfahrungsbericht-protokoll.md       ← E1–E5 nach Sessions
  learning-matrix.md                   ← aggregierte Muster (leer beim Start)
  glossar-domain.md                    ← Fachdomänenbegriffe (leer beim Start)
  glossar-system.md                    ← Betriebsbegriffe (leer beim Start)
  glossar-README.md                    ← Ladeprotokoll für das Glossar
  tools/
    check_import_layers.py             ← Layer-Checker (mit --preflight)
    check_agent_docs_consistency.py    ← Docs-Drift-Check (mit --preflight)
    resolve_test_obligations.py        ← Testpflicht-Ableitung
    instantiate/
      instantiate_project_box.py       ← einmaliger Instanziierungs-Sprechakt
      README.md                        ← Regeln für das Einmal-Werkzeug
  .agent-box-template.md             ← Markdown-Manifest der Template-Platzhalter und Dateien
```

Diese Box enthält bewusst **kein** `README.md`.
`README.md` gehört dem Template-Repository (`agent-templates/README.md`)
oder dem späteren Zielprojekt — niemals der Box.
Das Zielprojekt-README beschreibt den Projektzweck, nicht die Agenten-Mechanik.

---

## Lesepfad für neue Agenten

```text
1. AGENTS-COMPACT.md   → Schnelleinstieg (Pflichtlektüre vor jeder Session)
2. AGENTS.md           → vollständige Regeln
3. grundsatz.md        → einmalig, einmal lesen, dann nur bei Bedarf
4. preflight-checkliste.md → bei jeder nichttrivialen Änderung
5. Spezialdokumente nach Bedarf (Glossar, Bridges, Erfahrungsberichte)
```

---

## Instanziierung

```bash
cp -a agent-boxes/box-python/. /pfad/zum/neuen-projekt/
```

Danach im Zielprojekt **nicht** per globalem `sed` oder manuellem Search/Replace
instanziieren. Die Platzhalter werden kontrolliert durch das einmalige
Instanziierungswerkzeug ersetzt:

```bash
python tools/instantiate/instantiate_project_box.py \
  --project-display-name Regenbogen \
  --python-package-name regenbogen \
  --source-root src \
  --test-root tests \
  --docs-root docs \
  --tools-root tools \
  --python-lint-cmd "python -m ruff check ." \
  --python-format-check-cmd "python -m ruff format --check ." \
  --python-typecheck-cmd "python -m mypy src" \
  --python-test-cmd "python -m pytest" \
  --full-validation-cmd "python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest"
```

Projekt-Anzeigename und Python-Package-Name sind bewusst getrennt.

Beispiel:

```text
Projekt-Anzeigename:  Regenbogen
Python-Package-Name: regenbogen
Codepfad:             src/regenbogen/
```

Das Tool vollzieht den Instanziierungs-Sprechakt:

```text
Template-Zustand
  → Projekt-Anzeigename, Python-Package-Name und lokale Wurzeln festlegen
  → Platzhalter in freigegebenen Dateien ersetzen
  → docs/plans/, docs/sprechakte/, tmp/erfahrungsberichte/ anlegen
  → Quell- und Testwurzel anlegen, falls sie noch fehlen
  → generischen BR-001-Beispieleintrag entfernen
  → TEST_COMMANDS konservativ mit PYTHON_TEST_CMD füllen
  → .agent-box/instantiation.md schreiben
  → Post-Checks ausführen
  → Projekt-Zustand
```

`tools/instantiate/instantiate_project_box.py` läuft genau einmal. Wenn
`.agent-box/instantiation.md` bereits existiert, verweigert das Tool einen
weiteren Lauf. Eine erneute Instanziierung ist nur mit expliziter menschlicher
Freigabe und `--force` zulässig.

Optional kann `--skip-post-checks` verwendet werden, wenn lokale Tool-Abhängigkeiten
noch fehlen. Der Instanziierungs-Sprechakt bleibt dann gültig, aber der
Projektzustand ist noch nicht vollständig geprüft; die Post-Checks müssen
nachgeholt werden.

Nach dem Toollauf im Zielprojekt:

```text
1. package-schema.md an reale Projektstruktur prüfen/anpassen
2. tools/check_import_layers.py: lokale Layer-Ausnahmen nur über KNOWN_BREACHES eintragen
3. tools/resolve_test_obligations.py: TEST_COMMANDS prüfen und bei Bedarf schärfen
   (das Instanziierungswerkzeug setzt zunächst konservativ alle Gruppen auf PYTHON_TEST_CMD;
   projektspezifisch bessere Befehle wie "pytest tests/domain" sind erwünscht)
4. Glossar-Templates füllen (nach Bedarf, mindestens beim ersten Sprechakt SP1/SP2;
   Eintragsformat: "### <Begriffsname>")
5. migration-bridges.md: Beispiel-Eintrag entfernen oder durch reale Bridges ersetzen
6. Projekt-README.md neu anlegen oder prüfen (beschreibt den Projektzweck, nicht die Agenten-Mechanik)
7. AGENT-SETUP.md nach docs/agent-box-instantiation.md verschieben oder entfernen
   (die Datei ist Template-Artefakt — im instanziierten Projekt nicht mehr Pflicht)
8. Falls Post-Checks rot waren: Ursache beheben, nicht ignorieren
```

---

## Platzhalter

```text
Regenbogen         Anzeigename des Projekts, z. B. Regenbogen
regenbogen         Python-Package-/Importname, z. B. regenbogen
src                 Quellcode-Wurzel, z. B. src/
tests                   Test-Wurzel, z. B. tests/
docs                   Dokumentations-Wurzel, z. B. docs/
tools                  Tooling-Wurzel, z. B. tools/
python tools/check_import_layers.py --preflight src tests tools      Projektbefehl für Import-/Layer-Check
python -m ruff check .             Projektbefehl für Lint
python -m ruff format --check .     Projektbefehl für Format-Check
python -m mypy src        Projektbefehl für Typecheck
python -m pytest             Projektbefehl für Tests
python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest         vollständige Validierung
```

Nicht ersetzte Platzhalter in aktiven Regeln im **instanziierten Projekt**
sind Abbruchgrund H7.

Im **Template-Zustand** sind Platzhalter erlaubt — das ist die Box selbst.

---

## Instanziierungswerkzeug

`tools/instantiate/instantiate_project_box.py` ist das einzige vorgesehene Werkzeug
für den Übergang vom Template-Zustand in den Projekt-Zustand.

```text
Normale Tools:
  prüfen den laufenden Projektzustand

Instanziierungswerkzeug:
  erzeugt den initialen Projektzustand
  ersetzt Platzhalter kontrolliert
  schreibt Evidence
  läuft genau einmal
```

Die Quelle der ersetzbaren Dateien und Platzhalter ist:

```text
.agent-box-template.md
```

Der Nachweis des vollzogenen Sprechakts ist:

```text
.agent-box/instantiation.md
```

Nach erfolgreicher Instanziierung gilt:

```text
- tools/instantiate/* ist kein normales Agentenwerkzeug.
- erneute Ausführung ist verboten.
- Änderungen an Projektname, Root-Verzeichnissen oder Layer-Struktur sind
  keine Re-Instanziierung, sondern ein neuer Sprechakt über sprechakt-protokoll.md.
```

---

## Template-Zustand vs. Projekt-Zustand

Diese Box hat zwei Lebensphasen. Alle drei Tools folgen demselben Modusmodell:

```text
Template-Mode (Default ohne --instantiated):
  Prüft:    strukturelle Integrität der Box
  Erlaubt:  Platzhalter, leere Glossare, Beispiel-Bridge, leere TEST_COMMANDS
  Verbietet: README.md in der Box
  Pflicht:  AGENT-SETUP.md ist Pflichtdatei
  Ergebnis: grün, solange die Box strukturell vollständig ist

Instantiated-Mode (--instantiated):
  Prüft:    projektsemantische Vollständigkeit
  Verbietet: jeden Platzhalter, jede leere TEST_COMMANDS-Gruppe, das Beispiel
             'legacy_customer_id' in migration-bridges.md
  Erlaubt:  Projekt-README.md
  Pflicht:  AGENT-SETUP.md NICHT mehr Pflicht (nach docs/ verschoben/entfernt)
  Ergebnis: grün erst wenn alle Platzhalter weg und alle Testgruppen aufgelöst sind
```

Pro-Tool-Verhalten:

```text
check_agent_docs_consistency.py
  --template      Pflichtdateien + README-Verbot + Drift-Heuristiken (Default)
  --instantiated  Platzhalter=ERROR, README erlaubt, AGENT-SETUP optional

check_import_layers.py
  --template      kein Scan (Platzhalter in Konfiguration erwartet)
  (Default)       Scan; Konfigurationsplatzhalter → Exit 2
  --preflight     kompakter Agenten-Output mit Evidence

resolve_test_obligations.py
  --selfcheck                 Template-Modus: Platzhalter und TODOs erlaubt
  --selfcheck --instantiated  ERROR bei Platzhaltern und offenen TEST_COMMANDS
```

Tools unterstützen beide Modi:

```bash
# Im Template-Repository
python tools/check_agent_docs_consistency.py --template
python tools/check_import_layers.py --template
python tools/resolve_test_obligations.py --selfcheck

# Im instanziierten Projekt
python tools/check_agent_docs_consistency.py --instantiated
python tools/check_import_layers.py
python tools/resolve_test_obligations.py --selfcheck --instantiated
```

---

## Erste Prüfung nach Instanziierung

```bash
python tools/check_agent_docs_consistency.py --instantiated
python tools/check_import_layers.py
python tools/resolve_test_obligations.py --selfcheck --instantiated
```

Wenn einer dieser Befehle fehlschlägt: nicht ignorieren.
Die Box ist noch nicht korrekt instanziiert.

---

## Geschützte Dateien

Nach der Instanziierung gelten alle Agentendokumente und Tools als geschützt.
Liste in `AGENTS.md` Abschnitt 9.

Ein Agent darf diese Dateien nicht ohne explizite Freigabe ändern.

---

## Was diese Box NICHT ist

```text
- kein Python-Projektgenerator
- kein Packaging-Standard
- keine uv/poetry/pip-Vorgabe
- kein Testframework
- kein Architekturframework
- kein Ersatz für Projektentscheidungen
```

Sie ist:

```text
- ein operativer Agenten-Regelverbund
- ein Startpunkt für lokale Projektregeln
- ein Schutz gegen Bedeutungsdrift
- ein Preflight-/Abbruch-System
- ein Schema für semantische Paketgrenzen
```

---

## Erwartetes Ziel-Layout

```text
my-python-project/
  README.md              ← NEU vom Zielprojekt erstellt, beschreibt Projektzweck
  AGENT-SETUP.md         ← aus der Box, Instanziierungsanleitung
  AGENTS.md
  AGENTS-COMPACT.md
  (alle weiteren Box-Dateien im Root)
  pyproject.toml
  src/
    my_project/
      domain/
      system/
      infrastructure/
      adapters/
      cli/
  tests/
  docs/
    plans/
    sprechakte/
  tmp/
    erfahrungsberichte/
  tools/
    check_import_layers.py
    resolve_test_obligations.py
    check_agent_docs_consistency.py
    instantiate/
      instantiate_project_box.py
  .agent-box-template.md
  .agent-box/
    instantiation.md       ← Markdown-Evidence des Instanziierungs-Sprechakts
```

Das `README.md` im Zielprojekt wird **nach** dem Kopieren neu erstellt
und beschreibt das Projekt selbst — nicht die Agenten-Mechanik.
Die Box liefert es nicht mit.

`system/ports/` wird initial angelegt, weil es die standardisierte erlaubte
Importfläche von `infrastructure` nach `system` ist. Projekte ohne Port-Abstraktion
lassen den Ordner leer; er darf nicht für allgemeine Systemlogik missbraucht werden.

Andere Layouts sind möglich.
Dann muss `package-schema.md` und `LAYER_BY_PACKAGE_PART` in `check_import_layers.py`
entsprechend angepasst werden.

---

## Kurzregel

```text
Diese Box ist vollständig.
Diese Box wird kopiert.
Nach dem Kopieren lebt sie im Projektroot.
Ab dann ist sie lokale Wahrheit.
```
