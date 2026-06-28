# Checkpoint

> Ebene: REPOSITORY
> Rolle: Schema fuer PLAN/RUN-Checkpoints
> Geltung: dieses Projekt
> Autoritative Frage: Welche Felder muss ein konkreter Run-Checkpoint besitzen?
> Nicht zustaendig fuer: konkreten Laufzustand, Planinhalt, Ausfuehrungsmandat
> Instanzebene: PLAN/RUN

Run-ID:
Contract-ID:
Plan-ID:
Plan-Revision:
Mandat-ID:
Mandatstatus:
Priming-Revision:
Repository-Vertragsrevision:
Base-Snapshot:
Interaktionsprofil: interaktiv | autonom
Recovery-Profil: normal | overnight
Arbeitsprofil: feature | brownfield-migration | governance-migration
Checkpoint-Nr:
Vorgaenger-Checkpoint:
Zeitpunkt-UTC:
Run-Status: PREPARED | RUNNING | PAUSED | BLOCKED | ABORTED | COMPLETED
Checkpoint-Status: draft | sealed

Aktueller HEAD:
Letzter sicherer Snapshot:
Worktree-State: clean | dirty | detached
Dirty paths:
Recovery artifact:
Recovery status: unsecured | secured | restored

Aktuelle Phase:

Erledigt:

Offen:

Naechster zulaessiger Schritt:

Evidence:

Blocker:

<!-- Fortsetzungspruefung — nur bei Recovery-Profil: overnight                                    -->
<!-- Contract-ID unveraendert:                ja | nein                                           -->
<!-- Gebundene Revisionen noch gueltig:        ja | nein                                           -->
<!-- Base-Snapshot und Zustand nachvollziehbar: ja | nein                                          -->
<!-- Kein offener HARD- oder deontischer Blocker: ja | nein                                       -->
<!-- Naechster zulaessiger Schritt dokumentiert: ja | nein                                        -->
<!-- Fortsetzung zulaessig: ja | nein | Bedingung offen                                           -->

<!-- Optionale Governance-Evidence — nur ausfuellen bei Arbeitsprofil governance-migration       -->
<!-- Geaenderte Governance-Dateien:                                                               -->
<!-- Governance-Rueckfluss-Status:                                                                -->
<!--   LOCAL-ONLY | ERFAHRUNGSBERICHT | TEMPLATE-CANDIDATE | TOOLING-CANDIDATE | UNKNOWN | NO-RETURN -->
<!-- Konformitaetsbestaetigung:                                                                   -->

Lebenszyklus:

```text
Erzeugung:
  Vor jeder laengeren autonomen Phase oder Phasengrenze.
  Beim Pausieren, Blockieren oder Abbrechen eines Laufs.
  Checkpoints sind append-only — vorhandene Checkpoints werden nicht ueberschrieben.

Versiegeln:
  Checkpoint-Status auf sealed setzen nach Abschluss der Phase.
  Versiegelte Checkpoints sind unveraenderlich.
  Naechste Phase erzeugt die naechste Checkpoint-Nummer.
  Run-Status COMPLETED: nur beim letzten Checkpoint des gesamten Runs.

Benennung:
  docs/runs/<Run-ID>/checkpoint-<NNNN>.md
  NNNN ist vierstellig mit fuehrender Null (0001, 0002, ...).
  Andere .md-Dateien im selben Verzeichnis (README.md, contract.md usw.)
  sind keine Checkpoints und werden nicht als solche geprueft.
```

Pflicht wenn:

```text
Interaktionsprofil: autonom
Recovery-Profil: overnight
mehrphasiger Lauf mit geplanter Wiederaufnahme
```
