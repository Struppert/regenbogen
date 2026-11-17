# Sprechakt: Lebenszyklus der Aufgaben-Artefakte (Kurzform, Checkpoints, Ablage)

Aufgabe:          PLAN-2026-11-16-task-dokument-und-lebenszyklus (Phase 0)
Zeitpunkt:        2026-11-16
Sprechakt-Klasse: SP2 — Neuer systemsemantischer Steuerwert würde entstehen
Betroffener Begriff / Grenze: Plan-Form (Kurz | Voll), Lebenszyklus-Zustand verdichtet, Merge-Gate, Abschlussdokument, Aufgabenindex
Status: festgelegt
Folgeartefakte:
- aufgaben-lebenszyklus-protokoll.md (neu)
- docs/plans/template.md (nur Verweis) und Kurzform-Vorlage
- docs/aufgabenindex.md (neu)
- tools/check_agent_docs_consistency.py
- regelmatrix.md
Ersetzt:
Ersetzt durch:
Widerruft:
Freigabequelle: Dieter Haag, 2026-11-16: L2 "A: semantische Kriterien", L3 "C: B jetzt, A messen", L4 "Eigene Datei, Kurzform in docs/plans/" (Antworten auf die Entscheidungsvorlage). Zuvor festgelegt: L1 ("checkliste reicht"), L5 ("ich bevorzuge squash ... ein eigenes dokument ... aus der Aufgabe bestimmt"), Auslöser ("Run-Ende plus Aufräumpunkt", "Aus Arbeitsbaum entfernen"), Merge-Punkt ("die Entwicklung findet immer in einem Feature-Branch statt ... Der Punkt vor dem Merge ist die Stelle in der das bereinigt werden kann")

## Was fehlt

Das Template v0.3.11 kennt für Pläne und Checkpoints keinen Abschluss und keine Bereinigung.
Im Beobachtungsfall (deutlich größeres Projekt, nicht einsehbar) explodieren Plan-Dateien und
Checkpoints. Drei Festlegungen fehlen noch, bevor Plan B ein Mandat bekommen kann:

```text
L2  Wann genügt die Kurzform, wann ist der Vollplan Pflicht?
L3  Wie wird die Zahl der Checkpoints begrenzt?
L4  Dateinamen und Ablageort der neuen Artefakte.
```

## Was der Agent sieht

Template-Fakten, gelesen am 2026-11-16:

```text
- Mandatsgrundlage ist Plan oder Direktauftrag. Direktauftrag: kleine, vollständig bestimmte
  Fast-Path-Arbeit ohne Planartefakt, unveränderlich, gilt nur im aktuellen Kontext.
  "Für wiederaufnehmbare Arbeit ist ein Plan erforderlich."
  (ausfuehrungsmandat-protokoll.md, Abschnitt Ausfuehrungsmandat)
- Task-Schnitt ist semantisch, nicht datei-, mengen- oder zeilenbasiert. (AGENTS.md, Ausfuehrungsbreite)
- Jede nichttriviale Verhaltensänderung braucht im Plan Korrespondenzsätze oder
  "nicht anwendbar" mit Begründung. (korrespondenz-protokoll.md, docs/plans/template.md)
- Checkpointpflicht gilt bei Interaktionsprofil autonom, Recovery-Profil overnight und
  mehrphasigen Läufen mit geplanter Wiederaufnahme. Interaktiv: Checkpoint optional.
- AGENTS.md: "Nach jeder abgeschlossenen Phase neuen Checkpoint erzeugen und vorherigen
  versiegeln." Versiegelte Checkpoints sind unveränderlich (regelmatrix.md,
  docs/runs/checkpoint-template.md). Daraus folgt eine neue Datei je Phase.
- Der Checker prüft jede Datei in docs/plans/*.md auf die Kernfelder Plan-ID, Plan-Version,
  Mandat-ID, Mandatstatus, Ressourcenscope, Wirkungsscope, Capability-Scope. Checkpoints
  werden nur als docs/runs/<Run-ID>/checkpoint-NNNN.md erkannt.
Lokal: Dieses Projekt arbeitet interaktiv und hat keine Run-Verzeichnisse. Die Checkpoint-Last
ist hier nicht messbar.
```

## Analyse des Agenten

Mit Squash-Merge und branch-lokalen Plänen und Checkpoints (L5) erreicht nichts davon den
Hauptzweig. Die Last bleibt innerhalb eines Branches: Rauschen für Agent und Review, ein
langsamerer Checker, bei langen Overnight-Läufen viele Checkpoint-Dateien. Dort wirkt L3.
Die Kurzform (L2) hängt an den Regeln zu Direktauftrag, Plan und Korrespondenz, die nicht
dupliziert werden dürfen. Ablageort (L4) muss mit den Checkerprüfungen verträglich sein.

## Vorschlag des Agenten

**L2: Kriterien für die Kurzform.**

```text
Option A (empfohlen): semantische Kriterien.
  Vollplan ist Pflicht, wenn mindestens eines zutrifft:
    - Arbeitsprofil brownfield-migration oder governance-migration
    - Interaktionsprofil autonom oder Recovery-Profil overnight
    - eine geschützte Datei liegt im Scope
    - ein neuer Begriff, Status oder eine neue Fehlerbedeutung braucht einen Sprechakt
    - Schema-, API-, Dependency- oder Bridge-Änderung
    - mehr als ein semantischer Schnitt (Task-Schnitt T2 oder T3)
  Sonst genügt die Kurzform. Die Kurzform führt Korrespondenzsätze oder "nicht anwendbar".
  Fast-Path-Arbeit bleibt Direktauftrag ohne Planartefakt.
Option B: nur Profile. Kurzform bei Arbeitsprofil feature und interaktiv/normal, sonst Vollplan.
  Einfacher, aber grob (ein Sprechakt-Fall würde nicht erfasst).
Option C: nach Dateizahl oder Zeilenzahl. Nicht empfohlen: widerspricht dem Grundsatz,
  dass der Schnitt semantisch und nicht mengenbasiert ist.
```

**L3: Begrenzung der Checkpoints.**

```text
Option B (empfohlen): Regel unverändert. Der Plan schneidet nur Phasen mit eigener
  Wiederaufnahmegrenze, interne Arbeitsschritte sind keine Phasen. Zwischen-Checkpoints
  werden am Run-Ende entfernt (Stufe 1). Kein Eingriff in AGENTS.md und die Vorlage.
Option A: Checkpoint in-place fortschreiben (draft) und nur vor Pause, Kontextwechsel,
  Abbruch und am Run-Ende versiegeln. Wirksamer gegen die Dateizahl, ändert aber die
  Router-Regel in AGENTS.md und den Lebenszyklus der Checkpoint-Vorlage (lokale
  Divergenz vom Template).
Option C: B jetzt, A als Rückfluss-Vorschlag. Wirksamkeit von A im großen Projekt messen
  (Verzeichnisliste per find genügt), bevor die Regel geändert wird.
```

Empfehlung: C. Begründung: B kostet keine Template-Divergenz. A ist plausibel, aber an
diesem Projekt nicht prüfbar.

**L4: Namen und Ablage.**

```text
Protokoll:         aufgaben-lebenszyklus-protokoll.md im Root, als optionale lokale Datei im
                   Checker (wie PROJEKT.md). Alternative: als Abschnitt in REGELN-UND-TOOLS.md,
                   dann keine neue Datei, aber schwerer als Template-Kandidat herauszulösen.
Kurzform-Vorlage:  docs/plans/task-kurz-template.md. Kurzform-Instanzen liegen in docs/plans/
                   und tragen die Kernfelder des Checkers in kompakter Form (Feld Plan-Form:
                   Kurz). So bleibt ein einziger Ort und der Checker bleibt verträglich.
                   Alternative: docs/aufgaben/ (eigener Ort, dann ist eine neue Checkerregel
                   nötig).
Aufgabenindex:     docs/aufgabenindex.md.
Abschlussdokument: kein fester Name. Das Feld Abschlussdokument im Task-Dokument nennt
                   Pfad, Zweck und Form (entschieden in L5).
```

## Warum der Agent nicht fortfahren kann

Die Kriterien der Kurzform, die Checkpoint-Regel und Dateinamen sind Festlegungen des
Menschen. Ohne sie darf der Plan kein Mandat bekommen (neuer Steuerwert, SP2).

## Was der Mensch festlegt

```text
L2:  A | B | C | eigene Kriterien
L3:  A | B | C
L4:  Protokoll als eigene Datei oder Abschnitt; Kurzform in docs/plans/ oder docs/aufgaben/;
     Name des Aufgabenindex
```

## Was festgelegt wurde

```text
L1  Merge-Gate: die Review-Checkliste genügt (kein verbindlicher Checker in CI oder Branch-Schutz).
L2  Option A. Vollplan ist Pflicht bei mindestens einem der Kriterien: Arbeitsprofil
    brownfield-migration oder governance-migration; Interaktionsprofil autonom oder Recovery-Profil
    overnight; geschützte Datei im Scope; neuer Begriff, Status oder neue Fehlerbedeutung
    (Sprechakt); Schema-, API-, Dependency- oder Bridge-Änderung; mehr als ein semantischer
    Schnitt (T2 oder T3). Sonst genügt die Kurzform. Fast-Path-Arbeit bleibt Direktauftrag.
L3  Option C. Die Checkpoint-Regel bleibt unverändert. Der Plan schneidet nur Phasen mit
    eigener Wiederaufnahmegrenze. Zwischen-Checkpoints fallen am Run-Ende weg. In-place-
    Checkpoints (Option A) sind ein Rückfluss-Vorschlag; ihre Wirkung wird im großen Projekt
    gemessen, bevor die Regel geändert wird.
L4  aufgaben-lebenszyklus-protokoll.md im Root als optionale lokale Datei. Kurzform-Vorlage
    docs/plans/task-kurz-template.md, Kurzform-Instanzen in docs/plans/ mit den Kernfeldern des
    Checkers (Feld Plan-Form: Kurz). Aufgabenindex docs/aufgabenindex.md. Das Abschlussdokument
    hat keinen festen Namen (L5).
L5  Squash, kein Archiv-Verweis, ein eigenes Abschlussdokument je Aufgabe, Form aus der Aufgabe.
```

## Was der Agent danach tut

Status auf festgelegt setzen und versiegeln, die Festlegung in PLAN-2026-11-16-task-dokument-
und-lebenszyklus eintragen (Planversion erhöhen, wenn der Scope sich ändert), dann das Mandat
zur Aktivierung vorlegen.
