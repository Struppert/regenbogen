# Plan: README fuer Programmdoku von Regenbogen

Status: abgeschlossen
Datum: 2026-06-20
Bearbeiter: Codex

## Aufgabe

Ein kanonisches `README.md` fuer das Beispielprojekt `Regenbogen` erstellen.
Das README soll das Programm selbst erklaeren: Zweck, fachliche Idee,
Eingaben, Ausgaben, Datenquellen, Berechnungslogik, CLI/GUI-Nutzung,
Grenzen des Modells und Projektstruktur aus Sicht des Beispielprogramms.

Das README ist ausdruecklich keine Doku fuer die Agenten-Box und keine
Wiederholung von `AGENTS.md`.

Zusaetzlich werden die in der Programmdoku verwendeten Begriffe mit den
bestehenden Glossaren abgeglichen. Wenn Programmdoku und Glossar
auseinanderlaufen, wird nicht improvisiert: Entweder die Doku wird an den
kanonischen Glossarstand angepasst oder es wird eine semantische Luecke
explizit benannt.

## Betroffene Raeume

- `docs/`:
  Neues `README.md` als kanonische Programmdoku.
- `glossar-domain.md`:
  Abgleich fachlicher Begriffe, die im README erklaert oder verwendet werden.
- `glossar-system.md`:
  Abgleich systemischer Begriffe fuer Use Case, Fehler und Ergebnisobjekt.
- `src/regenbogen/**`:
  Nur als Projektionsraum fuer die tatsaechliche Funktionsweise lesen, keine
  geplante Produktcode-Aenderung in diesem Schnitt.

## Nicht-Ziele

- Keine Erweiterung der Programmlogik.
- Keine neue Wetterquelle oder neue Internetdaten in diesem Schnitt.
- Keine Aenderung des Agenten-Metasystems.
- Keine Ueberarbeitung von `AGENTS.md`, `package-schema.md` oder Checker-Tools.
- Kein Marketing- oder Template-README; das README beschreibt das konkrete
  Beispielprogramm.

## Schreibrechte

- Erlaubt:
  - neues `README.md` im Projektroot
  - bei Bedarf Planfortschreibung in `docs/plans/`
- Nur nach gesonderter Entscheidung:
  - Glossaraenderungen, falls beim Abgleich echte inhaltliche Luecken sichtbar
    werden
- Nicht Teil dieses Plans:
  - geschuetzte Agentendokumente und Tools

## Erwartete Aenderungen

1. Bestehende Programmartfakte lesen:
   - CLI- und GUI-Einstieg
   - Use Case
   - Domain-Modelle
   - vorhandene Projekttexte wie `INSTALLATION.md`, `tutorial.md`,
     `regentropfen-und-wetterdaten.md`
2. Kanonische Programmerzhaehlung festlegen:
   - Was das Programm tut
   - Wie es fachlich zu einem Regenbogen kommt
   - Welche Daten real genutzt werden
   - Welche Vereinfachungen/Heuristiken gelten
3. Glossarabgleich:
   - verwendete Fachbegriffe gegen `glossar-domain.md`
   - verwendete Systembegriffe gegen `glossar-system.md`
   - eventuelle begriffliche Drift oder Leerstellen notieren
4. `README.md` schreiben mit mindestens:
   - Projektzweck
   - Funktionsprinzip
   - Datenfluss
   - Eingaben und Ausgaben
   - CLI/GUI-Nutzung
   - Installationshinweise oder Verweis darauf
   - Grenzen des Modells
5. Abschlusspruefung:
   - README beschreibt das Beispielprogramm eindeutig
   - Glossarbegriffe werden nicht still uminterpretiert

## Testpflicht

Da dieser Schnitt primaer Doku erzeugt, stehen keine Produktverhaltenstests im
Vordergrund. Pflicht ist stattdessen inhaltliche Konsistenz:

- README gegen Codepfade pruefen
- README gegen Glossare pruefen
- keine Behauptung ueber Datenquellen oder Berechnungslogik, die im Code nicht
  projektiert ist

Wenn der Abgleich zeigt, dass ein aktiv benoetigter Begriff im Glossar fuer die
README-Aussage fehlt oder unvollstaendig ist, greift Task-Schnitt T1 und
gegebenenfalls SP7.

## Abbruchbedingungen

- HARD:
  - H1, wenn geschuetzte Agentendokumente geaendert werden muessten
  - H3, wenn Doku, Glossar und Code sich in einer fuer das README zentralen
    Aussage widersprechen
  - H6, wenn unklar bleibt, wie die Programmdoku gegen die vorhandenen
    Artefakte validiert werden soll
  - H7/SP7, wenn fuer zentrale README-Begriffe relevante Glossareintraege
    fehlen oder unvollstaendig sind
- SOFT:
  - SA6, wenn lokale Inkonsistenzen zwischen bestehenden Programmdokumenten
    sichtbar werden, aber noch kein semantischer Widerspruch feststeht

## Wiedereinstiegspunkt

Nach Freigabe dieses Plans:

1. Programmbezogene Quell- und Dokuartefakte gezielt lesen
2. aktive Begriffe fuer das README bestimmen
3. Glossarabgleich durchfuehren
4. `README.md` entwerfen
5. Konsistenzpruefung und Fertigstellung

## Abschlusskriterien

- Im Projektroot existiert ein `README.md`, das `Regenbogen` als Beispielprogramm
  praezise und eigenstaendig erklaert.
- Das README verwechselt Programmdoku nicht mit Agenten-Metadoku.
- Die verwendeten Begriffe sind mit dem aktuellen Glossar vereinbar oder eine
  Luecke ist explizit als solche benannt.
- Das README ist fuer einen Leser nuetzlich, der das Programm verstehen und
  ausprobieren will, ohne zuerst das Agentensystem lesen zu muessen.

## Ergebnis

- `README.md` im Projektroot erstellt
- Programmbeschreibung gegen Codepfade und Glossarbegriffe abgeglichen
- keine zusaetzliche Glossaraenderung in diesem Schnitt noetig
