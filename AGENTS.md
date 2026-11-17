# AGENTS.md — Python-Projekt: bindender Einstieg fuer Agenten

> Ebene: MIXED-TRANSITION
> Primaerer Anteil: PRIMING-ROUTER
> Sekundaere Projektion: REPOSITORY
> Rolle: bindender Einstieg und Ladeprotokoll
> Autoritative Frage: Welche Kernregeln gelten immer und welche Detailquelle wird aktiviert?
> Nicht zustaendig fuer: vollstaendige Detailprotokolle, konkrete Laufplanung

> Immer aktive Kernregeln und Ladeprotokoll. Detailregeln nur bei konkretem
> Task-Ausloeser laden. Verlinkte Dokumente nicht pauschal laden.

## 0. Geltung

Diese Regeln gelten fuer `Regenbogen` nach Instanziierung von
`box-python` mit Python-Package `regenbogen`.

Nicht ersetzte Platzhalter in aktiven Regeln sind H7. Im Template-Zustand sind
Platzhalter erlaubt.

Projektmarker: Greenfield nutzt `.agent-box/instantiation.md`, Brownfield
nutzt `.agent-box/adoption.md`. Genau einer muss existieren.

## 1. Autoritaet und Ladeprinzip

`AGENTS.md` ist der bindende Router. Spezialdokumente sind autoritativ fuer
ihre Detailfrage:

```text
Raum, Import, Architektur        -> package-schema.md
Begriff, Status, Fehler, Policy  -> glossar-README.md,
                                    glossar-domain.md,
                                    glossar-system.md,
                                    glossar-meta.md
Menschliche Entscheidung         -> sprechakt-protokoll.md
Semantischer Task-Schnitt        -> task-schnitt.md
Brownfield oder Altbruch         -> BROWNFIELD-MIGRATION.md
Testpflicht                      -> test-obligations.md
Modelltreue, Testoracle, Evidence -> korrespondenz-protokoll.md
Schreibrechte, Schutz, Drift     -> regelmatrix.md
Arbeitsmodus, Mandat, WG-MUTATION -> ausfuehrungsmandat-protokoll.md
Run-Checkpoint                  -> docs/runs/checkpoint-template.md
Blocker, Abbruch, Wiedereinstieg -> blocker-und-abbruch-protokoll.md
Bridge-Symbol                    -> migration-bridges.md
Erfahrungsbericht-Ausloeser      -> erfahrungsbericht-protokoll.md
Setup oder Instanziierung        -> AGENT-SETUP.md
Projektaufbau, was liegt wo      -> PROJEKT.md (lokal)
Lokale Regeln, Befehle, Werkzeuge -> REGELN-UND-TOOLS.md (lokal)
Name -> Datei (Begriffsindex)    -> BEGRIFFSINDEX.md (lokal, falls vorhanden)
Plan-Form, Merge-Gate, Aufgabenindex -> aufgaben-lebenszyklus-protokoll.md (lokal)
```

Bei Widerspruch zwischen autoritativen Artefakten nicht selbst entscheiden.
Blocker klassifizieren und gueltig stoppen.

## 2. Unbedingte Kernregeln

1. Keine fachliche, systemische oder metasprachliche Bedeutung erfinden.
2. Infrastructure beobachtet; System Semantics urteilt.
3. Binding uebersetzt und erzeugt keine neue Semantik.
4. Tests definieren keine neue Produktsemantik.
5. Keine stillen Fallbacks, Fehlerunterdrueckung oder Plausibilitaetsreparatur.
6. Keine neue Runtime-Dependency ohne Freigabe.
7. Keine oeffentliche API-Aenderung ohne Freigabe.
8. Keine geschuetzte Governance-Datei ohne explizite Freigabe aendern.
9. Keine Import-, Layer- oder Testregel durch Toolaenderung umgehen.
10. Kein Push, History-Rewrite, Tag oder Remote-Eingriff.
11. Brownfield-Bestand ist zuerst Observed State, nicht Freigabe.
12. Keine normative oder projekt-transformative Repository-Mutation ohne
    aktives, scope-gueltiges Ausfuehrungsmandat.
13. Gruene Checks belegen nur ihre benannte Pruefbeziehung; sie ersetzen
    keinen Modelltreue-Nachweis.

Code-Familien: H1-H10 allgemeiner HARD-Abbruch und SA1-SA6 allgemeiner
SOFT-Abbruch stehen in `blocker-und-abbruch-protokoll.md`; SP1-SP7 stehen in
`sprechakt-protokoll.md`; BF1-BF12 stehen in `BROWNFIELD-MIGRATION.md`.

## 3. Arbeitsmodus und Wirkungsgate

Ein Auftrag erlaubt nur den eindeutig ausgesprochenen Arbeitsmodus.

Ohne eindeutige Modusangabe gilt `ANALYSE`.
Ein ausdruecklicher Planungsauftrag aktiviert `PLAN`.
`AUSFUEHRUNG` erfordert ein aktives, scope-gueltiges Ausfuehrungsmandat.

```text
ANALYSE      lesen, untersuchen, im Chat berichten
PLAN         Planentwuerfe, offene Entscheidungsfragen, offene Sprechakte
             und diagnostische Evidence erstellen
AUSFUEHRUNG  freigegebenen Plan oder Direktauftrag im Mandatsscope umsetzen
```

Diagnostische Repository-Mutation ist nur im Arbeitsmodus PLAN oder
AUSFUEHRUNG und nur in den dafuer vorgesehenen Artefaktraeumen erlaubt.

Vor der ersten Repository-Mutation und bei jedem Wechsel von Wirkungstyp,
Scope, Schutzklasse, Mandatsstatus oder Grundlage muss WG-MUTATION aus
`ausfuehrungsmandat-protokoll.md` fuer den jeweiligen Wirkungstyp gruen sein.

Schreibrecht, Planexistenz, Fast-Path, festgelegter Sprechakt und fehlender
Blocker ersetzen kein Ausfuehrungsmandat.

Ein Aufgabenlauf darf Priming und Repository-Vertrag lesen, aber nicht als
unbeabsichtigte Folge seiner Aufgabe veraendern. Aendert sich waehrend eines
Laufs eine gebundene Priming-, Repository-, Plan-, Scope-, Autorisierungs-,
Base-Snapshot- oder eine der drei Profil-Revisionen (Interaktions-, Recovery-,
Arbeitsprofil) durch unerwartete externe Wirkung, ist der bisherige
Laufvertrag ungueltig. Fortsetzung erfordert neuen Preflight, neue Contract-ID
und, soweit betroffen, neue Autorisierung.

Eine im Laufvertrag ausdruecklich geplante Governance- oder
Repository-Transformation invalidiert den Vertrag nicht bei jeder
Zwischenmutation. Sie bleibt an die gebundene Baseline und das entschiedene
Zielmodell gebunden, bis Verify den neuen Zielzustand bestaetigt oder der Lauf
abbricht.

## 4. Task-Einstieg

Zuerst betroffene Dateien, Begriffe und semantische Raeume bestimmen.

Fast-Path ist nur erlaubt, wenn ALLE der folgenden Kriterien erfuellt sind:

```text
1. Genau ein semantischer Schnitt — keine Raum- oder Verantwortungsgrenze.
2. Nur vorhandene, bereits entschiedene Begriffe — keine offene Sprechaktfrage.
3. Keine geschuetzte Datei betroffen (Governance, Glossare, Schema, Checker).
4. Keine API-, Dependency-, Bridge- oder Known-Breach-Aenderung.
5. Keine Brownfield-Aufnahme und keine Box-Migration.
6. Keine neue Importkante.
7. Testpflicht vollstaendig bekannt und eindeutig ableitbar.
8. Scope aus dem aktuellen Auftrag eindeutig bestimmbar — kein mehrphasiger
   Recovery-Bedarf.
```

Fehlt auch nur eines dieser Kriterien: kein Fast-Path, sondern Preflight und
bei Bedarf Plan.

Fast-Path reduziert Governance-Pruefungen. Fast-Path erteilt kein
Ausfuehrungsmandat. Fast-Path kann mit Direktmandat ohne Planartefakt laufen.
Mit aktivem Mandat werden Fast-Path-Aufgaben ohne
zusaetzliche Governance-Zerlegung vollstaendig ausgefuehrt und validiert.
Bei Governance-Ausloeser nur das zugehoerige Dokument laden.

## 5. Ausfuehrungsbreite

Task-Schnitt ist semantisch, nicht datei-, mengen- oder zeilenbasiert.

Blosse Teilbarkeit ist kein Schnittgrund. Gleichartige Aenderungen innerhalb
eines mandatsgedeckten semantischen Schnitts werden gebuendelt ausgefuehrt.

Ein Schnitt ist nur erforderlich, wenn sich menschliche Festlegung,
semantischer Raum oder Urteilskompetenz, Schreibrecht, Freigabe, Validierungs-,
Rollback-Grenze oder unabhaengig abschliessbarer Lieferzustand unterscheiden.

Beispiele: 100 gleichartige Importkorrekturen oder ein freigegebenes Symbol an
allen Verwendungsstellen sind ein Arbeitspaket. Domain-Semantik und HTTP-Binding sind mindestens zwei interne semantische
Phasen. Ein echter Task-Schnitt ist nur bei unterschiedlicher Freigabe-,
Validierungs- oder Rollback-Grenze noetig. Fehlende menschliche Festlegung
ist Sprechakt, kein Mikroschnitt.

## 6. Blocker und Anti-Zeno

Blocker: epistemisch = Information fehlt, technisch = Umsetzung oder
Validierung ist nicht beherrscht, deontisch = menschliche Festlegung oder
Freigabe fehlt. Details: `blocker-und-abbruch-protokoll.md`.

Deontische Blocker duerfen nicht durch kleinere Aufgaben ersetzt werden.

Bleibt derselbe Blocker nach zwei inhaltlichen Schritten unveraendert, kein
weiterer Mikroschnitt und kein dritter gleichartiger Versuch. Dann gilt:
Sprechakt, gezielte Klaerung oder gueltiger Abbruch.

Widerspruechliche festgelegte Sprechakte niemals selbst aufloesen.

## 7. Schreib- und Evidence-Regeln

Produktcode, Tests, Plaene, temporaere Evidence und `CHANGELOG.md` sind
beschreibbare Dateiklassen. Beschreibbarkeit ist kein Ausfuehrungsmandat.

Governance, Glossare, Schema, Checker, Dependency-Dateien, Workflows,
Plan-Templates und Agenten-Box-Metadaten sind geschuetzt. Exakte Liste:
`regelmatrix.md`.

Markdown ist das operative Artefaktformat.

Fortschritt wird nicht im gebundenen Plan fortgeschrieben. Laufzustand,
aktuelle Phase, erledigte/offene Schritte, HEAD, Blocker und naechster
zulaessiger Schritt stehen im Checkpoint.

Bei Interaktionsprofil `autonom` oder Recovery-Profil `overnight` sowie bei
mehrphasigen Laeufen mit geplanter Wiederaufnahme gilt:

```text
Checkpoint vor der ersten normativen oder projekt-transformativen Wirkung erzeugen.
Nach jeder abgeschlossenen Phase neuen Checkpoint erzeugen und vorherigen versiegeln.
Vor Pause, Kontextwechsel oder Abbruch neuen Checkpoint erzeugen und vorherigen versiegeln.
Letzten Checkpoint mit Run-Status COMPLETED und Checkpoint-Status sealed abschliessen.
```

Wenn das Projekt ein `CHANGELOG.md` fuehrt, wird es bei Abschluss eines extern
sichtbaren oder architektonisch relevanten Arbeitspakets aktualisiert, nicht
beim blossen Anlegen eines Plans.

Ein Erfahrungsbericht entsteht nur bei Ausloesern aus
`erfahrungsbericht-protokoll.md`.

## 8. Validierung

Vor nichttrivialer Codearbeit:

```bash
python tools/check_import_layers.py --preflight src tests tools
```

Danach die aus `test-obligations.md` abgeleiteten Tests und Checks ausfuehren.
Bei nichttrivialer Verhaltensaenderung die Korrespondenzsaetze aus
`korrespondenz-protokoll.md` im Plan und Modellreview abschliessen.

Vollvalidierung:

```bash
python tools/check_agent_docs_consistency.py --instantiated
python tools/check_import_layers.py --preflight src tests tools
python tools/resolve_test_obligations.py --selfcheck --instantiated
python tools/check_agent_docs_consistency.py --instantiated && python tools/check_import_layers.py --preflight src tests tools && python tools/resolve_test_obligations.py --selfcheck --instantiated && python -m pytest
```

Rot ist ein diagnostizierter Abbruchzustand, keine Aufforderung zum
Abschwaechen des Pruefwerkzeugs.

## 9. Abschluss

Der Agent optimiert auf einen vollstaendigen, validierbaren semantischen
Arbeitsschnitt: nicht auf minimale Diffgroesse, nicht auf maximale Aktivitaet
und nicht auf Mikroschnitte.
