# Sprechakt: MODELL-README als Pflichtprojektion bei Modellarbeit

Aufgabe:          Modellbeschreibung fuer Regenbogen als eigenes Artefakt einfuehren und in das Agenten-Framing aufnehmen
Zeitpunkt:        2026-06-20 11:30
Sprechakt-Klasse: SP2 — Neuer systemsemantischer Steuerwert würde entstehen
Betroffener Begriff / Grenze: Modellarbeit und Pflichtprojektion MODELL-README
Status: festgelegt
Folgeartefakte:
- AGENTS.md
- AGENTS-COMPACT.md
- preflight-checkliste.md
- MODELL-README.md
Ersetzt:
Ersetzt durch:

## Was fehlt

Es fehlte eine explizite Regel, wie das aktuell implementierte Modell als
zusammenhaengende Beschreibung im Projekt gehalten werden muss und wann diese
Beschreibung bei Aenderungen nachgezogen werden muss.

## Was der Agent sieht

symbol:
  MODELL-README.md existierte nicht.
package_says:
  keine spezielle Modellprojektion definiert
glossar_says:
  Einzelbegriffe vorhanden, aber keine zusammenhaengende Modellbeschreibung
code_says:
  Modelllogik liegt verteilt ueber domain/, system/core/ und system/ports/
tests_say:
  Teilinvarianten sind vorhanden, aber keine kanonische Gesamtbeschreibung
schema_says:
  keine abweichende Raumregel, aber auch keine Modellpflege-Regel

## Analyse des Agenten

Die fachliche und systemische Modellbeschreibung war ueber mehrere Artefakte
verteilt. Fuer kuenftige Modellarbeit fehlte damit eine sichtbare Pflicht-
projektion, die nicht neue Autoritaet ueber Glossar und Code erhebt, aber
deren aktuellen Zusammenhang dokumentiert.

## Vorschlag des Agenten

`MODELL-README.md` wird als kanonische zusammenhaengende Beschreibung des
aktuell implementierten Modells fuer Menschen eingefuehrt.

Die neue Regel lautet:

- Wenn Modelllogik geaendert wird, muss `MODELL-README.md` geprueft und bei
  Bedarf aktualisiert werden.
- Neue fachliche Modellbegriffe duerfen dort nicht still entstehen; dafuer ist
  weiterhin das Glossar zustaendig.

## Warum der Agent nicht fortfahren kann

Ohne menschliche Festlegung waere unklar geblieben, ob `MODELL-README.md` nur
optionale Doku oder verbindliche Pflichtprojektion bei Modellarbeit ist.

## Was der Mensch festlegt

`MODELL-README.md` ist verbindliche Pflichtprojektion fuer Modellarbeit.
Bei jeder Aenderung am implementierten Modell muss das Dokument geprueft und
bei Bedarf aktualisiert werden.

Das Dokument ist keine konkurrierende Bedeutungsautoritaet neben Glossar und
Code. Es beschreibt den aktuell implementierten Zusammenhang des Modells.

## Was der Agent danach tut

1. `MODELL-README.md` erstellen
2. Regel in AGENTS.md, AGENTS-COMPACT.md und preflight-checkliste.md
   verankern
3. bei kuenftigen Modellaenderungen das Dokument im Preflight mit pruefen
