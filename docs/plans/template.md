# Plan: <Kurzbeschreibung>

> Ebene: REPOSITORY
> Rolle: Schema fuer PLAN/RUN-Artefakte
> Geltung: dieses Projekt
> Autoritative Frage: Welche Felder muss ein konkreter Transformationsplan besitzen?
> Nicht zustaendig fuer: konkreten Laufzustand, allgemeines Priming
> Instanzebene: PLAN/RUN

Plan-ID: PLAN-YYYY-MM-DD-<kurzbeschreibung>
Plan-Version: 1
Plan-Schema-Version: v0.3.7
Planstatus: entwurf | entscheidungsbereit | angenommen | verworfen
Erstellt im Modus: PLAN | AUSFUEHRUNG
Datum:
Bearbeiter:

<!-- Laufbindung (v0.3.7) — Pflichtfelder fuer jeden nichttrivialen Plan.
     Projekte ohne Contract-/Run-Infrastruktur tragen "—" als Platzhalterwert
     (nur zulässig fuer Legacy-Transition und Brownfield-Verfahren B, nicht
     fuer neue autonome oder overnight-Laeufe).
     Laufzustand gehoert in Checkpoints, nicht in den gebundenen Plan:
     Aktuelle Phase, erledigte Schritte und HEAD stehen im Checkpoint. -->
## Laufbindung

Contract-ID: CONTRACT-YYYY-MM-DD-<kurzbeschreibung>
Contract-Status: proposed | active | invalidated | completed | aborted
Run-ID: RUN-YYYY-MM-DD-<kurzbeschreibung>
Priming-Revision:
Repository-Vertragsrevision:
Plan-Revision: <Plan-ID>@<Plan-Version>
Scope-ID: SCOPE-YYYY-MM-DD-<kurzbeschreibung>
Scope-Version: 1
Authorization-Revision:
Base-Snapshot:
Interaktionsprofil: interaktiv | autonom
Recovery-Profil: normal | overnight
Arbeitsprofil: feature | brownfield-migration | governance-migration

## Ausführungsmandat

Mandat-ID: MD-YYYY-MM-DD-<kurzbeschreibung>
Mandatstatus: nicht erteilt | aktiv | widerrufen | erloschen
Mandatsgrundlage: Plan
Contract-ID:
Run-ID:
Mandatsrevision:
Authorization-Revision: <Mandat-ID>@<Mandatsrevision>
Grundlagen-ID: <diese Plan-ID>
Grundlagen-Version: <diese Plan-Version>
Freigabezeitpunkt:
Freigabetext oder Freigabereferenz:
Freigegebener Scope:
Freigegebene geschützte Dateien:
Nicht freigegeben:
Gültigkeit: bis Abschluss | bis Widerruf | begrenzte Phase

## Ressourcenscope

Pfade:
Komponenten:
Semantische Räume:

## Wirkungsscope

### Explizit erlaubte Wirkungen

- ...

### Abgeleitete Wirkungen

- zugehörige Tests
- notwendige Imports
- Formatierung geänderter Dateien
- Dokumentationsprojektionen im freigegebenen Scope

### Verbotene Wirkungen

- ...

## Capability-Scope

Normale Dateien:
Geschützte Dateien:
Governance:
Dependencies:

Priorität:

```text
verboten
> fehlende Capability
> explizit erlaubt
> abgeleitet
```

Verbotene Wirkung hat Vorrang. Eine abgeleitete Wirkung ist nur zulässig,
wenn sie innerhalb des freigegebenen semantischen Arbeitsschnitts bleibt und
die passende Capability vorhanden ist.

## Mandatsrelevante Änderungen

Plan-Version erhöhen bei Änderung an Zielzustand, Scope, geschützten Dateien,
Semantik, Dependencies, öffentlicher API, Validierungs- oder Rollback-Grenze.

## Aufgabe

## Zugesagter semantischer Endzustand

## Betroffene Räume

## Nicht-Ziele

## Schreibrechte

## Bereits erteilte Freigaben / Sprechakte

## Erwartete Änderungen

## Interne Phasen

Phasengrenzen sind keine Benutzer-Checkpoints, solange keine neue Freigabe,
kein neuer Sprechakt und kein echter Task-Schnitt nötig wird.

Fortschritt wird nicht im Plan fortgeschrieben. Aktuelle Phase, erledigte
Schritte, offene Schritte, HEAD, Blocker und nächster zulässiger Schritt
stehen ausschließlich im Checkpoint.

## Gebündelte mechanische Änderungen

## Testpflicht

## Abbruchbedingungen

## Echter Task-Schnitt

Schnitt nötig: ja/nein
Begründung:

## Wiedereinstiegspunkt

## Abschlusskriterien

## Erfahrungsbericht

Auslöser geprüft: E1 | E2 | E3 | E4 | E5 | keiner
Bericht erforderlich: ja/nein
Begründung:

Protokoll (Format, Pflichtfelder, Ablageort): `erfahrungsbericht-protokoll.md`

Ablageort: `.agent-box/evidence/erfahrungsberichte/YYYY-MM-DD-EB-<kurzbeschreibung>.md`
