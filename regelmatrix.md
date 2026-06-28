# regelmatrix.md — Autoritaet, Hierarchie, Rollentrennung

> Ebene: REPOSITORY
> Rolle: lokaler Autoritaets- und Schreibrechtsvertrag
> Geltung: dieses Projekt
> Autoritative Frage: Welche Quelle beantwortet welche Projektfrage und welche Dateien sind geschuetzt?
> Nicht zustaendig fuer: Ausfuehrungsmandat, fachliche Begriffe

> Dieses Dokument stabilisiert den Agenten-Dokumentenverbund.
>
> Es beschreibt, welches Dokument welche Frage beantwortet,
> und was passiert, wenn Dokumente einander widersprechen.

---

## 1. Zweck

Ein Agent darf nicht selbst entscheiden, welcher Text gerade gilt.

Dieses Dokument legt fest:

```text
Welche Datei ist fuer welche Frage autoritativ?
Welche Datei ist nur Hilfsmittel?
Was passiert bei Drift?
Welche Aenderungen erzeugen Kopplungspflichten?
```

---

## 2. Autoritaetsmodell

Autoritaet folgt der Zuständigkeit, nicht einer pauschalen Totalordnung.

```text
AGENTS.md
   Bindender Einstieg, Kerninvarianten, Ladeprotokoll, Code-Familien.
   AGENTS.md wiederholt Detailregeln nicht vollstaendig.

package-schema.md
   Semantische Paket-/Modulraeume, Importregeln, Known Breaches.

glossar-domain.md / glossar-system.md / glossar-meta.md
   Begriffe und ihre Bedingungsraeume. Autoritativ fuer Bedeutung.
   Ladeprotokoll: glossar-README.md.

regelmatrix.md
   Schreibrechte, Schutzlisten, Autoritaetsordnung und Drift-Regeln.

preflight-checkliste.md
   Durchfuehrung vor Aenderungen.

test-obligations.md
   Ableitung der Test- und Checkpflichten.

sprechakt-protokoll.md
   Ablauf menschlicher Festlegungen.

task-schnitt.md
   Schnitt von Aufgaben und Semantic Working Set.

blocker-und-abbruch-protokoll.md
   H-/SA-Abbrueche, Blocker, Abbruch-Evidence, Wiedereinstieg.

ausfuehrungsmandat-protokoll.md
   Arbeitsmodus, Ausfuehrungsmandat und Wirkungsgate WG-MUTATION.

migration-bridges.md
   Symbolsperren und Bridge-Begriffe.

BROWNFIELD-MIGRATION.md
    Operative Autoritaet fuer Brownfield-Aufnahme, Box-Versionsmigration und
    Reparatur abgebrochener Erstinstanziierung.

erfahrungsbericht-protokoll.md / learning-matrix.md
    Lernprotokoll und aggregierter Rueckfluss. Keine direkte Regelautoritaet.

grundsatz.md
    Theorie / Hintergrund. Keine operative Regelquelle.

AGENT-SETUP.md / README.md / sonstige Projektdokumentation
    Orientierung und Instanziierungsanleitung. Keine operative Agentenautoritaet.
```

Wenn zwei Dokumente dieselbe Detailfrage unterschiedlich beantworten:
Drift melden. Keine Quelle still bevorzugen.

---

## 3. Regelmatrix: Welche Datei beantwortet was?

| Frage | Autoritative Quelle | Agent tut |
| --- | --- | --- |
| Was liest der Agent zuerst? | `AGENTS.md` | Router und Kernregeln laden |
| Welche Detaildokumente werden geladen? | `AGENTS.md` | Aktivierung nach Task-Ausloeser |
| Was darf der Agent aendern? | `regelmatrix.md` | Schreibrechte pruefen |
| Welche Dateien sind geschuetzt? | `regelmatrix.md` | Bei Bedarf H1 |
| Darf der Agent jetzt Wirkung erzeugen? | `ausfuehrungsmandat-protokoll.md` | WG-MUTATION pruefen |
| Wann muss der Agent allgemein abbrechen? | `blocker-und-abbruch-protokoll.md` | Abbruch-Evidence erzeugen |
| Was ist Fast-Path? | `AGENTS.md` | Risikoklasse bestimmen |
| Welche Invarianten gelten immer? | `AGENTS.md` | Invariante pruefen |
| Was bedeutet dieser Begriff fachlich? | `glossar-domain.md` | Ladeprotokoll folgen |
| Was bedeutet dieser Betriebsbegriff? | `glossar-system.md` | Ladeprotokoll folgen |
| Was bedeutet dieser Meta-Begriff? | `glossar-meta.md` | Ladeprotokoll folgen |
| Welches Glossar wann laden? | `glossar-README.md` | Ladeprotokoll ausfuehren |
| Ist die Autonomieregel erfuellt? | passendes Glossar | H10 wenn verletzt |
| Welchem Raum gehoert ein Modul an? | `package-schema.md` | Raum klassifizieren |
| Welche Imports sind erlaubt? | `package-schema.md` | Import-Checker ausfuehren |
| Welche Known Breaches existieren? | `package-schema.md` + Checker | Aktiv/passiv pruefen |
| Darf dieses Symbol angefasst werden? | `migration-bridges.md` | Migrationsstatus pruefen |
| Welche Checks sind Pflicht? | `test-obligations.md` | Testpflicht ableiten |
| Wie wird Preflight ausgefuehrt? | `preflight-checkliste.md` | Schrittfolge ausfuehren |
| Wann wird Task-Schnitt geprueft? | `task-schnitt.md` | Semantischen Schnitt bewerten |
| Wann ist ein Sprechakt noetig? | `AGENTS.md` + `sprechakt-protokoll.md` | Sprechakt-Artefakt erzeugen |
| Wie sieht ein Sprechakt-Artefakt aus? | `sprechakt-protokoll.md` | Vorlage verwenden |
| Wie wird Brownfield migriert? | `BROWNFIELD-MIGRATION.md` | Brownfield-Verfahren ausfuehren |
| Welche BF-Abbrueche gelten? | `BROWNFIELD-MIGRATION.md` | Brownfield-Evidence schreiben |
| Wie wird Dokumentdrift bewertet? | `regelmatrix.md` | Kopplung pruefen |

---

## 4. Redundanzregel

Jede Regel hat genau eine autoritative Quelle.

`AGENTS.md` aktiviert Detailregeln, wiederholt sie aber nicht vollstaendig.
Spezialdokumente duerfen die Kernregeln referenzieren, aber keine eigene
konkurrierende Autoritaet erfinden.

Wenn zwei Dokumente dieselbe Detailfrage unterschiedlich beantworten:
Drift melden. Keine Quelle still bevorzugen.

---

## 5. Drift-Regeln

### Aenderung an `AGENTS.md`

Zwingend pruefen:

```text
preflight-checkliste.md
task-schnitt.md
regelmatrix.md
test-obligations.md
erfahrungsbericht-protokoll.md
tools/check_agent_docs_consistency.py
blocker-und-abbruch-protokoll.md
ausfuehrungsmandat-protokoll.md
```

Hinweis: `check_agent_docs_consistency.py --changed-file AGENTS.md` gibt
Kopplungshinweise. Das Tool prueft Dateipraesenz und Stichwort-Vorkommen,
keinen Inhaltsabgleich. Inhaltsabgleich ist manueller Review.

---

### Aenderung an `package-schema.md`

Zwingend pruefen:

```text
AGENTS.md
test-obligations.md
tools/check_import_layers.py  -> LAYER_BY_PACKAGE_PART und FORBIDDEN_IMPORTS nachziehen
```

Wenn ein neuer Raum oder eine neue Importausnahme entsteht:
Checker muss nachgezogen werden; sonst laeuft er mit veralteter Konfiguration.

---

### Aenderung an `glossar-domain.md`, `glossar-system.md` oder `glossar-meta.md`

Zwingend pruefen:

```text
glossar-README.md
package-schema.md
migration-bridges.md
AGENTS.md
```

Wenn ein neuer Begriff eingetragen wird: package-schema.md auf Raumkorrespondenz
pruefen. Wenn ein Begriff geaendert wird: migration-bridges.md auf
Migrationsstatus pruefen.

---

### Aenderung an `preflight-checkliste.md`

Zwingend pruefen:

```text
AGENTS.md
task-schnitt.md
regelmatrix.md
ausfuehrungsmandat-protokoll.md
```

Preflight darf keine neuen Abbruchregeln erfinden.

---

### Aenderung an `task-schnitt.md`

Zwingend pruefen:

```text
AGENTS.md
preflight-checkliste.md
sprechakt-protokoll.md
blocker-und-abbruch-protokoll.md
ausfuehrungsmandat-protokoll.md
```

---

### Aenderung an `sprechakt-protokoll.md`

Zwingend pruefen:

```text
AGENTS.md
task-schnitt.md
preflight-checkliste.md
```

Neue Sprechaktklasse gehoert zuerst oder gleichzeitig nach `AGENTS.md`.

---

### Aenderung an `ausfuehrungsmandat-protokoll.md`

Zwingend pruefen:

```text
AGENTS.md
preflight-checkliste.md
docs/plans/template.md
regelmatrix.md
sprechakt-protokoll.md
BROWNFIELD-MIGRATION.md
tools/check_agent_docs_consistency.py
```

Mandatsregeln duerfen keine Semantikentscheidung ersetzen.

---

### Aenderung an `test-obligations.md`

Zwingend pruefen:

```text
AGENTS.md
preflight-checkliste.md
tools/resolve_test_obligations.py
```

---

### Aenderung an `erfahrungsbericht-protokoll.md`

Zwingend pruefen:

```text
AGENTS.md
learning-matrix.md
tools/check_agent_docs_consistency.py
```

---

### Aenderung an `grundsatz.md`

Zwingend pruefen:

```text
AGENTS.md
regelmatrix.md
```

`grundsatz.md` ist Theorie. Operative Aenderungen gehoeren in das passende
operative Dokument.

---

### Aenderung an Checker-Tools

Betroffen: `check_import_layers.py`, `resolve_test_obligations.py`,
`check_agent_docs_consistency.py`

Zwingend pruefen:

```text
AGENTS.md
package-schema.md
test-obligations.md
preflight-checkliste.md
CI-Konfiguration
```

Checker-Aenderungen sind geschuetzt (H1, H5).
Keine Aenderung zur Fehlerunterdrueckung.

---

## 6. Widerspruchsregel

```text
AGENTS.md vs. package-schema.md
  -> HARD-Abbruch H3. Keine Quelle still bevorzugen.

package-schema.md vs. Import-Checker
  -> HARD-Abbruch H2 oder Known-Breach-Pruefung.
  -> Checker ist Alarm, nicht Architekturautoritaet.

test-obligations.md vs. resolve_test_obligations.py
  -> Testpflicht unklar -> HARD-Abbruch H6.

sprechakt-protokoll.md vs. AGENTS.md
  -> AGENTS.md gilt fuer Kernregeln. Sprechakt-Dokument driftet.

regelmatrix.md vs. AGENTS.md
  -> Schutz- oder Autoritaetsdrift. HARD-Abbruch H3.
```

---

## 7. Geschuetzte Dateien

Schreibstatus:

```text
beschreibbar
  Die Dateiklasse kann grundsaetzlich durch Agenten veraendert werden.

geschuetzt
  Die Dateiklasse braucht zusaetzliche explizite Berechtigung.

freigegeben
  Die konkrete Aenderung ist durch ein aktives, scope-gueltiges
  Ausfuehrungsmandat gedeckt.
```

Beschreibbarkeit ist eine Policy-Eigenschaft. Sie ist kein
Ausfuehrungsmandat.

Eine geschuetzte Datei ist nur freigegeben, wenn das Mandat sie ausdruecklich
nennt.

Geschuetzt sind:

```text
AGENTS.md
AGENT-SETUP.md
BROWNFIELD-MIGRATION.md
blocker-und-abbruch-protokoll.md
ausfuehrungsmandat-protokoll.md
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
docs/runs/checkpoint-template.md
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

Aenderung nur mit aktivem Ausfuehrungsmandat und ausdruecklicher Deckung der
geschuetzten Datei.

Konkrete Checkpoints unter `docs/runs/<Run-ID>/` sind nur im zugehoerigen
Contract und Run beschreibbar. Versiegelte Checkpoints sind unveraenderlich.

---

## 8. Known-Breach-Regel

Known Breaches duerfen nicht erweitert, verschoben, umbenannt, still repariert
oder als Praezedenzfall verwendet werden.

Wenn eine Aufgabe einen Known Breach beruehrt:

```text
1. Aktiv oder passiv?
2. Im Plan enthalten?
3. Checker klassifiziert ihn?
4. package-schema.md beschreibt ihn?
5. Aendert die Aufgabe seine Bedeutung?
```

Wenn aktiv und nicht geplant: Task-Schnitt oder HARD-Abbruch H2.

---

## 9. Schlussregel

Wenn unklar ist, welches Dokument gilt:
nicht interpretieren. Abbruch mit Evidence.
