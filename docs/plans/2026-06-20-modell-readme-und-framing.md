# Plan: MODELL-README und Framing fuer Modellarbeit

Status: abgeschlossen
Datum: 2026-06-20
Bearbeiter: Codex

## Aufgabe

Ein neues `MODELL-README.md` im Projektroot einführen, das das aktuell
implementierte Regenbogen-Modell erklärt:

- fachliche Zielgröße des Modells
- aktuell verwendete Eingangsgrößen
- Ableitung von Wahrscheinlichkeit und Sichtbarkeit
- Heuristiken und Modellgrenzen
- Beziehung zwischen Domain-Begriffen, System-Ableitungen und technischen
  Wetterfeldern

Zusätzlich soll geklärt werden, wie dieses Modell-README dauerhaft in das
Agenten-Framing eingebunden wird, so dass es bei jeder Modelländerung
mitaktualisiert werden muss.

## Betroffene Räume

- `docs/` / Projektroot:
  - neues `MODELL-README.md`
- `glossar-domain.md`:
  - Abgleich und ggf. Ergänzung fachlicher Modellbegriffe
- `glossar-system.md`:
  - Abgleich systemischer Begriffe, falls Modellbeschreibung auf
    systemsemantische Begriffe verweist
- geschützte Agentendokumente:
  - nur falls die Updatepflicht des Modell-README als dauerhafte Regel im
    Agentensystem verankert werden soll

## Nicht-Ziele

- keine Erweiterung des meteorologischen Modells in diesem Schnitt
- keine Einführung neuer Wetterdaten oder neuer Modellfaktoren
- keine sofortige Änderung geschützter Agentendokumente ohne separate Freigabe
- keine implizite Umdeutung technischer API-Felder zu Domain-Begriffen

## Schreibrechte

- direkt erlaubt:
  - neues `MODELL-README.md`
  - Planfortschreibung in `docs/plans/`
- nur nach gesonderter Entscheidung/Freigabe:
  - Änderungen an `AGENTS.md`, `AGENTS-COMPACT.md`,
    `preflight-checkliste.md`, `test-obligations.md` oder anderen
    geschützten Agentendokumenten
- bei Glossaränderungen:
  - `glossar-domain.md` und `glossar-system.md` sind geschützt und erfordern
    daher ebenfalls explizite Freigabe, falls sie in diesem Schnitt geändert
    werden sollen

## Erwartete Änderungen

1. Das aktuelle Modell aus Code, Tests und Glossaren rekonstruieren.
2. Prüfen, welche Begriffe bereits kanonisch vorliegen und welche für eine
   Modellbeschreibung aktiv benötigt werden.
3. `MODELL-README.md` als kanonische Modellbeschreibung schreiben.
4. Explizit dokumentieren, welche Teile:
   - Domain-Begriffe sind
   - systemische Ableitungen sind
   - technische Eingangsdaten aus der Wetter-API sind
5. Das gewünschte Framing als Regelbedarf formulieren:
   - Modelländerung => `MODELL-README.md` prüfen und bei Bedarf aktualisieren
   - neue fachliche Modellbegriffe => Glossarprüfung / ggf. Glossareintrag

## Testpflicht

Da dies primär ein Dokumentations- und Framing-Schnitt ist:

- Modellbeschreibung gegen Code und Tests prüfen
- verwendete Begriffe gegen Glossar prüfen
- keine Aussage ins Modell-README schreiben, die im aktuellen Code nicht
  projektiert ist

Wenn neue Modellbegriffe für das README nötig wären, aber im Glossar fehlen,
tritt T1 auf; wenn sie aktiv nötig bleiben, folgt SP7.

## Sprechakte / Entscheidungen

### Sicher nicht nötig, solange nur beschrieben wird

- Kein Sprechakt nur für die Erstellung eines rein beschreibenden
  `MODELL-README.md`, sofern es den aktuellen Modellstand korrekt wiedergibt
  und keine neue Semantik einführt.

### Möglicherweise nötig

- `SP7`, wenn für die Modellbeschreibung aktiv benötigte Begriffe im Glossar
  fehlen oder unvollständig sind.
- `SP1`, wenn im Zuge der Modellbeschreibung neue fachliche Begriffe explizit
  eingeführt werden müssten, z. B. ein neuer eigenständiger Domain-Begriff.
- `SP2`, wenn die Updatepflicht von `MODELL-README.md` als neue dauerhafte
  Agenten-/Systemregel materialisiert werden soll und dafür eine neue
  systemsemantische Arbeitsregel festgelegt werden muss.

### Zusätzlich wichtig

Die eigentliche Verankerung "jede Modelländerung muss `MODELL-README.md`
aktualisieren" ist nicht bloß Inhalt des neuen Dokuments, sondern eine
Agentenregel. Wenn diese Regel verbindlich in das lokale System aufgenommen
werden soll, berührt das geschützte Agentendokumente und braucht deshalb
explizite Freigabe.

## Abbruchbedingungen

- `H1`, wenn geschützte Agentendokumente oder Glossare ohne Freigabe geändert
  werden müssten
- `H3`, wenn Modell, Glossar und Programmdoku sich in zentralen Aussagen
  widersprechen
- `H7` / `SP7`, wenn für aktive Modellbegriffe relevante Glossareinträge fehlen
  oder unvollständig sind
- `H4`, wenn neue Begriffe faktisch eingeführt würden, ohne dass sie als solche
  behandelt werden

## Wiedereinstiegspunkt

Nach Freigabe dieses Plans:

1. Modellquellen lesen
2. aktive Modellbegriffe bestimmen
3. Glossarabgleich durchführen
4. `MODELL-README.md` entwerfen
5. prüfen, ob nur Doku entsteht oder ob ein SP-/Freigabebedarf für das
   dauerhafte Framing ausgelöst wird

## Abschlusskriterien

- `MODELL-README.md` existiert und beschreibt das aktuell implementierte Modell
  präzise
- das Dokument trennt technische Eingangsdaten, systemische Ableitungen und
  Domain-Begriffe sichtbar
- notwendige Sprechakte oder Freigaben für das dauerhafte Framing sind klar
  benannt, statt implizit unterlaufen zu werden

## Ergebnis

- `MODELL-README.md` im Projektroot erstellt
- SP2 als festgelegter Sprechakt unter `docs/sprechakte/` dokumentiert
- Updatepflicht fuer Modellarbeit in `AGENTS.md`,
  `AGENTS-COMPACT.md` und `preflight-checkliste.md` verankert
- keine Glossaraenderung in diesem Schnitt noetig
