# regelmatrix.md — Autorität, Hierarchie, Rollentrennung

> Dieses Dokument stabilisiert den Agenten-Dokumentenverbund.
>
> Es beschreibt, welches Dokument welche Frage beantwortet,
> und was passiert, wenn Dokumente einander widersprechen.

---

## 1. Zweck

Ein Agent darf nicht selbst entscheiden, welcher Text gerade gilt.

Dieses Dokument legt fest:

```text
Welche Datei ist für welche Frage autoritativ?
Welche Datei ist nur Hilfsmittel?
Was passiert bei Drift?
Welche Änderungen erzeugen Kopplungspflichten?
```

---

## 2. Autoritaetsmodell

Autorität folgt der Zuständigkeit, nicht einer pauschalen Totalordnung.

```text
AGENTS.md
   Bindender Einstieg, Kerninvarianten, Ladeprotokoll, Code-Familien.
   AGENTS.md wiederholt Detailregeln nicht vollständig.

package-schema.md
   Semantische Paket-/Modulräume, Importregeln, Known Breaches.

glossar-domain.md / glossar-system.md / glossar-meta.md
   Begriffe und ihre Bedingungsräume. Autoritativ für Bedeutung.
   Ladeprotokoll: glossar-README.md.

regelmatrix.md
   Schreibrechte, Schutzlisten, Autoritätsordnung und Drift-Regeln.

preflight-checkliste.md
   Durchführung vor Änderungen.

test-obligations.md
   Ableitung der Test- und Checkpflichten.

sprechakt-protokoll.md
   Ablauf menschlicher Festlegungen.

task-schnitt.md
   Schnitt von Aufgaben und Semantic Working Set.

ausfuehrungsmandat-protokoll.md
   Arbeitsmodus, Ausfuehrungsmandat und Wirkungsgate W0.

blocker-und-abbruch-protokoll.md
   H-/SA-Abbrüche, Blocker, Abbruch-Evidence, Wiedereinstieg.

migration-bridges.md
   Symbolsperren und Bridge-Begriffe.

BROWNFIELD-MIGRATION.md
   Operative Autorität für Brownfield-Aufnahme, Box-Versionsmigration und
   Reparatur abgebrochener Erstinstanziierung.

erfahrungsbericht-protokoll.md / learning-matrix.md
   Lernprotokoll und aggregierter Rückfluss. Keine direkte Regelautorität.

grundsatz.md
   Theorie / Hintergrund. Keine operative Regelquelle.

AGENT-SETUP.md / README.md / sonstige Projektdokumentation
   Orientierung und Instanziierungsanleitung. Keine operative Agentenautorität.
```

Wenn zwei Dokumente dieselbe Detailfrage unterschiedlich beantworten:
Drift melden. Keine Quelle still bevorzugen.

---

## 3. Regelmatrix: Welche Datei beantwortet was?

| Frage | Autoritative Quelle | Agent tut |
| --- | --- | --- |
| Was liest der Agent zuerst? | `AGENTS.md` | Router und Kernregeln laden |
| Welche Detaildokumente werden geladen? | `AGENTS.md` | Aktivierung nach Task-Auslöser |
| Was darf der Agent ändern? | `regelmatrix.md` | Schreibrechte prüfen |
| Welche Dateien sind geschützt? | `regelmatrix.md` | Bei Bedarf H1 |
| Darf der Agent jetzt Wirkung erzeugen? | `ausfuehrungsmandat-protokoll.md` | W0 prüfen |
| Wann muss der Agent allgemein abbrechen? | `blocker-und-abbruch-protokoll.md` | Abbruch-Evidence erzeugen |
| Was ist Fast-Path? | `AGENTS.md` | Risikoklasse bestimmen |
| Welche Invarianten gelten immer? | `AGENTS.md` | Invariante prüfen |
| Was bedeutet dieser Begriff fachlich? | `glossar-domain.md` | Ladeprotokoll folgen |
| Was bedeutet dieser Betriebsbegriff? | `glossar-system.md` | Ladeprotokoll folgen |
| Was bedeutet dieser Meta-Begriff? | `glossar-meta.md` | Ladeprotokoll folgen |
| Welches Glossar wann laden? | `glossar-README.md` | Ladeprotokoll ausführen |
| Ist die Autonomieregel erfüllt? | passendes Glossar | H10 wenn verletzt |
| Welchem Raum gehört ein Modul an? | `package-schema.md` | Raum klassifizieren |
| Welche Imports sind erlaubt? | `package-schema.md` | Import-Checker ausführen |
| Welche Known Breaches existieren? | `package-schema.md` + Checker | Aktiv/passiv prüfen |
| Darf dieses Symbol angefasst werden? | `migration-bridges.md` | Migrationsstatus prüfen |
| Welche Checks sind Pflicht? | `test-obligations.md` | Testpflicht ableiten |
| Wie wird Preflight ausgeführt? | `preflight-checkliste.md` | Schrittfolge ausführen |
| Wann wird Task-Schnitt geprüft? | `task-schnitt.md` | Semantischen Schnitt bewerten |
| Wann ist ein Sprechakt nötig? | `AGENTS.md` + `sprechakt-protokoll.md` | Sprechakt-Artefakt erzeugen |
| Wie sieht ein Sprechakt-Artefakt aus? | `sprechakt-protokoll.md` | Vorlage verwenden |
| Wie wird Brownfield migriert? | `BROWNFIELD-MIGRATION.md` | Brownfield-Verfahren ausführen |
| Welche BF-Abbrüche gelten? | `BROWNFIELD-MIGRATION.md` | Brownfield-Evidence schreiben |
| Wie wird Dokumentdrift bewertet? | `regelmatrix.md` | Kopplung prüfen |
| Warum ist dieses System so gebaut? | `grundsatz.md` | Einmal lesen, verstehen |

---

## 4. Redundanzregel

Jede Regel hat genau eine autoritative Quelle.

`AGENTS.md` aktiviert Detailregeln, wiederholt sie aber nicht vollständig.
Spezialdokumente dürfen die Kernregeln referenzieren, aber keine eigene
konkurrierende Autorität erfinden.

Wenn zwei Dokumente dieselbe Detailfrage unterschiedlich beantworten:
Drift melden. Keine Quelle still bevorzugen.

---

## 5. Drift-Regeln

### Änderung an `AGENTS.md`

Zwingend prüfen:

```text
preflight-checkliste.md
task-schnitt.md
regelmatrix.md
test-obligations.md
erfahrungsbericht-protokoll.md
blocker-und-abbruch-protokoll.md
ausfuehrungsmandat-protokoll.md
tools/check_agent_docs_consistency.py
```

Hinweis: `check_agent_docs_consistency.py --changed-file AGENTS.md` gibt
Kopplungshinweise. Das Tool prüft Dateipräsenz und Stichwort-Vorkommen,
keinen Inhaltsabgleich. Inhaltsabgleich ist manueller Review.

---

### Änderung an `package-schema.md`

Zwingend prüfen:

```text
AGENTS.md
test-obligations.md
tools/check_import_layers.py  → LAYER_BY_PACKAGE_PART und FORBIDDEN_IMPORTS nachziehen
```

Wenn ein neuer Raum oder eine neue Importausnahme entsteht:
Checker muss nachgezogen werden — sonst läuft er mit veralteter Konfiguration.

---

### Änderung an `glossar-domain.md`, `glossar-system.md` oder `glossar-meta.md`

Zwingend prüfen:

```text
glossar-README.md
package-schema.md
migration-bridges.md
AGENTS.md
```

Wenn ein neuer Begriff eingetragen wird: package-schema.md auf Raumkorrespondenz
prüfen. Wenn ein Begriff geändert wird: migration-bridges.md auf
Migrationsstatus prüfen.

---

### Änderung an `preflight-checkliste.md`

Zwingend prüfen:

```text
AGENTS.md
task-schnitt.md
regelmatrix.md
ausfuehrungsmandat-protokoll.md
```

Preflight darf keine neuen Abbruchregeln erfinden.

---

### Änderung an `task-schnitt.md`

Zwingend prüfen:

```text
AGENTS.md
preflight-checkliste.md
sprechakt-protokoll.md
blocker-und-abbruch-protokoll.md
ausfuehrungsmandat-protokoll.md
```

---

### Änderung an `sprechakt-protokoll.md`

Zwingend prüfen:

```text
AGENTS.md
task-schnitt.md
preflight-checkliste.md
```

Neue Sprechaktklasse gehört zuerst oder gleichzeitig nach `AGENTS.md`.

---

### Änderung an `ausfuehrungsmandat-protokoll.md`

Zwingend prüfen:

```text
AGENTS.md
preflight-checkliste.md
docs/plans/template.md
regelmatrix.md
sprechakt-protokoll.md
BROWNFIELD-MIGRATION.md
tools/check_agent_docs_consistency.py
```

Mandatsregeln dürfen keine Semantikentscheidung ersetzen.

---

### Änderung an `test-obligations.md`

Zwingend prüfen:

```text
AGENTS.md
preflight-checkliste.md
tools/resolve_test_obligations.py
```

---

### Änderung an `erfahrungsbericht-protokoll.md`

Zwingend prüfen:

```text
AGENTS.md
learning-matrix.md
tools/resolve_test_obligations.py
tools/check_agent_docs_consistency.py
```

---

### Änderung an `grundsatz.md`

Zwingend prüfen:

```text
AGENTS.md
regelmatrix.md
```

`grundsatz.md` ist Theorie. Operative Änderungen gehören in das passende
operative Dokument.

---

### Änderung an Checker-Tools

Betroffen: `check_import_layers.py`, `resolve_test_obligations.py`,
`check_agent_docs_consistency.py`

Zwingend prüfen:

```text
AGENTS.md
package-schema.md
test-obligations.md
preflight-checkliste.md
CI-Konfiguration
```

Checker-Änderungen sind geschützt (H1, H5).
Keine Änderung zur Fehlerunterdrückung.

---

## 6. Widerspruchsregel

```text
AGENTS.md vs. package-schema.md
  → HARD-Abbruch H3. Keine Quelle still bevorzugen.

package-schema.md vs. Import-Checker
  → HARD-Abbruch H2 oder Known-Breach-Prüfung.
  → Checker ist Alarm, nicht Architekturautorität.

test-obligations.md vs. resolve_test_obligations.py
  → Testpflicht unklar → HARD-Abbruch H6.

sprechakt-protokoll.md vs. AGENTS.md
  → AGENTS.md gilt für Kernregeln. Sprechakt-Dokument driftet.

regelmatrix.md vs. AGENTS.md
  → Schutz- oder Autoritätsdrift. HARD-Abbruch H3.
```

---

## 7. Schreibstatus

```text
beschreibbar
  Die Dateiklasse kann grundsätzlich durch Agenten verändert werden.

geschützt
  Die Dateiklasse braucht zusätzliche explizite Berechtigung.

freigegeben
  Die konkrete Änderung ist durch ein aktives, scope-gültiges
  Ausfuehrungsmandat gedeckt.
```

Beschreibbarkeit ist eine Policy-Eigenschaft. Sie ist kein Ausfuehrungsmandat.

Eine geschützte Datei ist nur freigegeben, wenn das Mandat sie ausdrücklich nennt.

Geschützt sind:

```text
AGENTS.md
AGENT-SETUP.md
BROWNFIELD-MIGRATION.md
ausfuehrungsmandat-protokoll.md
blocker-und-abbruch-protokoll.md
package-schema.md
preflight-checkliste.md
task-schnitt.md
sprechakt-protokoll.md
regelmatrix.md
test-obligations.md
migration-bridges.md
erfahrungsbericht-protokoll.md
learning-matrix.md
glossar-README.md
glossar-domain.md
glossar-system.md
glossar-meta.md
grundsatz.md
docs/plans/template.md
tools/check_agent_docs_consistency.py
tools/check_import_layers.py
tools/resolve_test_obligations.py
tools/instantiate/instantiate_project_box.py
tools/instantiate/README.md
.agent-box-template.md
.agent-box/instantiation.md
.agent-box/adoption.md
pyproject.toml
Lockfiles
.github/workflows/
```

---

## 8. Known-Breach-Regel

Known Breaches dürfen nicht erweitert, verschoben, umbenannt,
still repariert oder als Präzedenzfall verwendet werden.

Wenn eine Aufgabe einen Known Breach berührt:

```text
1. Aktiv oder passiv?
2. Im Plan enthalten?
3. Checker klassifiziert ihn?
4. package-schema.md beschreibt ihn?
5. Ändert die Aufgabe seine Bedeutung?
```

Wenn aktiv und nicht geplant: Task-Schnitt oder HARD-Abbruch H2.

---

## 9. Schlussregel

Wenn unklar ist, welches Dokument gilt:
nicht interpretieren. Abbruch mit Evidence.
