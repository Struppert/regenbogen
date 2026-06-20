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

## 2. Autoritätsreihenfolge

Bei Widerspruch zwischen Dokumenten gilt diese Reihenfolge:

```text
1. AGENTS.md
   Operative Regeln, Schreibrechte, Abbruchbedingungen, Safe Tasks.
   Kanonische Quelle für alle Listen (Invarianten, H-Codes, S-Codes, Schreibrechte).

2. package-schema.md
   Semantische Paket-/Modulräume, Importregeln, Known Breaches.

3. glossar-domain.md / glossar-system.md
   Begriffe und ihre Bedingungsräume. Autoritativ für Bedeutung.
   Ladeprotokoll: glossar-README.md.

4. preflight-checkliste.md
   Durchführung vor Änderungen.

5. test-obligations.md
   Ableitung der Test- und Checkpflichten.

6. sprechakt-protokoll.md
   Ablauf menschlicher Festlegungen.

7. task-schnitt.md
   Schnitt von Aufgaben und Semantic Working Set.

8. migration-bridges.md
   Symbolsperren und Bridge-Begriffe.

9. AGENTS-COMPACT.md
   Schnelleinstieg. Destillat aus AGENTS.md. Darf AGENTS.md nicht widersprechen.

10. grundsatz.md
    Warum dieses System so gebaut ist. Theorie / Hintergrund.
    Keine operativen Regeln — aber Begründung für alle operativen Regeln.
    Kein Agent muss grundsatz.md für jeden Preflight lesen.
    Jeder Agent sollte es einmal gelesen haben.

11. AGENT-SETUP.md / README.md / sonstige Projektdokumentation
    AGENT-SETUP.md: Instanziierungsanleitung der Box, informativ.
    README.md (im Zielprojekt): Projektzweck, keine Agentenautorität.
    Orientierung — keine operative Agentenautorität.
```

Wenn ein niedrigeres Dokument einem höheren widerspricht:
nicht lokal reparieren. Drift melden. Je nach Relevanz: HARD-Abbruch.

---

## 3. Regelmatrix: Welche Datei beantwortet was?

| Frage                                  | Autoritative Quelle                     | Agent tut                    |
| -------------------------------------- | --------------------------------------- | ---------------------------- |
| Was darf der Agent ändern?             | `AGENTS.md`                             | Schreibrechte prüfen         |
| Welche Dateien sind geschützt?         | `AGENTS.md`                             | Bei Bedarf HARD-Abbruch      |
| Wann muss der Agent abbrechen?         | `AGENTS.md`                             | Abbruch-Evidence erzeugen    |
| Was ist ein Safe Task?                 | `AGENTS.md`                             | Risikoklasse bestimmen       |
| Welche Invarianten gelten?             | `AGENTS.md`                             | Invariante prüfen            |
| Was bedeutet dieser Begriff fachlich?  | `glossar-domain.md`                     | Ladeprotokoll folgen         |
| Was bedeutet dieser Betriebsbegriff?   | `glossar-system.md`                     | Ladeprotokoll folgen         |
| Welches Glossar wann laden?            | `glossar-README.md`                     | Ladeprotokoll ausführen      |
| Ist die Autonomieregel erfüllt?        | `glossar-domain.md` / `glossar-system.md` | H10 wenn verletzt          |
| Welchem Raum gehört ein Modul an?      | `package-schema.md`                     | Raum klassifizieren          |
| Welche Imports sind erlaubt?           | `package-schema.md`                     | Import-Checker ausführen     |
| Welche Known Breaches existieren?      | `package-schema.md` + Checker           | Aktiv/passiv prüfen          |
| Darf dieses Symbol angefasst werden?   | `migration-bridges.md`                  | Migrationsstatus prüfen      |
| Welche Checks sind Pflicht?            | `test-obligations.md`                   | Testpflicht ableiten         |
| Wie wird Preflight ausgeführt?         | `preflight-checkliste.md`               | Schrittfolge ausführen       |
| Wann wird Task-Schnitt geprüft?        | `task-schnitt.md`                       | SWS schneiden                |
| Wann ist ein Sprechakt nötig?          | `AGENTS.md` + `sprechakt-protokoll.md`  | Sprechakt-Artefakt erzeugen  |
| Wie sieht ein Sprechakt-Artefakt aus?  | `sprechakt-protokoll.md`                | Vorlage verwenden            |
| Was liest der Agent zuerst?            | `AGENTS-COMPACT.md`                     | Startkontext laden           |
| Wie wird Dokumentdrift bewertet?       | `regelmatrix.md`                        | Kopplung prüfen              |
| Warum ist dieses System so gebaut?     | `grundsatz.md`                          | Einmal lesen, verstehen      |

---

## 4. Redundanzregel

Listen, die an mehreren Stellen stehen könnten (Schreibrechte, Abbruchbedingungen,
Invarianten, Sprechakt-Klassen), haben genau eine kanonische Quelle: `AGENTS.md`.

Alle anderen Dokumente dürfen diese Listen in Kurzform wiederholen oder darauf verweisen.
Sie dürfen sie nicht eigenständig erweitern.

Wenn AGENTS-COMPACT.md eine Abbruchregel enthält, die in AGENTS.md fehlt:
COMPACT driftet — HARD-Abbruch H3.

---

## 5. Drift-Regeln

### Änderung an `glossar-domain.md` oder `glossar-system.md`

Zwingend prüfen:

```text
glossar-README.md  — Ladeprotokoll noch korrekt?
package-schema.md  — neue Raumzuordnung nötig?
migration-bridges.md — neuer Begriff mit Bridge-Status?
AGENTS.md          — neue Invariante aus dem Begriff ableitbar?
```

Wenn ein neuer Begriff eingetragen wird: package-schema.md auf Raumkorrespondenz prüfen.
Wenn ein Begriff geändert wird: migration-bridges.md auf Migrationsstatus prüfen.

---

### Änderung an `grundsatz.md`

Zwingend prüfen:

```text
AGENTS.md          — folgt eine operative Konsequenz?
regelmatrix.md     — ändert sich die Hierarchie?
```

grundsatz.md ist Theorie — operative Änderungen gehören nach AGENTS.md, nicht hierher.

---

### Änderung an `AGENTS.md`

Zwingend prüfen:

```text
AGENTS-COMPACT.md  — Kurzform abgleichen (Invarianten, Abbrüche, Schreibrechte)
preflight-checkliste.md
package-schema.md
regelmatrix.md
```

Hinweis: `check_agent_docs_consistency.py --changed-file AGENTS.md` gibt Kopplungshinweise.
Das Tool prüft Dateipräsenz und Stichwort-Vorkommen — keinen Inhaltsabgleich.
Inhaltsabgleich ist manueller Review.

---

### Änderung an `AGENTS-COMPACT.md`

Zwingend prüfen:

```text
AGENTS.md  — COMPACT darf keine neue Regel enthalten, die nicht in AGENTS.md steht.
```

---

### Änderung an `package-schema.md`

Zwingend prüfen:

```text
AGENTS.md
AGENTS-COMPACT.md
test-obligations.md
tools/check_import_layers.py  → LAYER_BY_PACKAGE_PART und FORBIDDEN_IMPORTS nachziehen
```

Wenn ein neuer Raum oder eine neue Importausnahme entsteht:
Checker muss nachgezogen werden — sonst läuft er mit veralteter Konfiguration.

---

### Änderung an `preflight-checkliste.md`

Zwingend prüfen:

```text
AGENTS.md
AGENTS-COMPACT.md
regelmatrix.md
```

Preflight darf keine neuen Abbruchregeln erfinden.
Neue Abbruchregel gehört zuerst nach `AGENTS.md`.

---

### Änderung an `task-schnitt.md`

Zwingend prüfen:

```text
AGENTS.md
preflight-checkliste.md
sprechakt-protokoll.md
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

### Änderung an `test-obligations.md`

Zwingend prüfen:

```text
AGENTS.md
preflight-checkliste.md
tools/resolve_test_obligations.py
```

---

### Änderung an Checker-Tools

Betroffen: `check_import_layers.py`, `resolve_test_obligations.py`, `check_agent_docs_consistency.py`

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

AGENTS.md vs. AGENTS-COMPACT.md
  → AGENTS.md gilt. COMPACT driftet. Melden.

package-schema.md vs. Import-Checker
  → HARD-Abbruch H2 oder Known-Breach-Prüfung.
  → Checker ist Alarm, nicht Architekturautorität.

test-obligations.md vs. resolve_test_obligations.py
  → Testpflicht unklar → HARD-Abbruch H6.

sprechakt-protokoll.md vs. AGENTS.md
  → AGENTS.md gilt. Sprechakt-Dokument driftet.
```

---

## 7. Known-Breach-Regel

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

## 8. Agenten-Dokumente sind operative Regeln

```text
AGENTS.md, AGENTS-COMPACT.md, package-schema.md,
preflight-checkliste.md, task-schnitt.md, sprechakt-protokoll.md,
regelmatrix.md, test-obligations.md
```

Diese Dateien sind nicht „nur Doku".
Änderung nur mit expliziter Freigabe (→ H1).

---

## 9. Schlussregel

Wenn unklar ist, welches Dokument gilt:
nicht interpretieren. Abbruch mit Evidence.
