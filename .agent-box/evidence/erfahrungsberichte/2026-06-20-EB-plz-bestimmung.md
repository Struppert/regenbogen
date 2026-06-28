# Erfahrungsbericht: Echte PLZ-Bestimmung

Zeitpunkt: 2026-06-20
Bezug auf Plan: `docs/plans/2026-06-20-echte-plz-bestimmung.md`

## Kontext

Der Standortadapter sollte von einer reinen Demo-Tabelle zu einer echten
PLZ-gestuetzten Koordinatenbestimmung erweitert werden. Konkreter Nutzerfall
war `72138` fuer Kirchentellinsfurt.

## Beobachtungen

1. Der bestehende Sprechakt fuer PLZ als Standort-Eingabe war ausreichend.
   Die Domain bleibt frei von PLZ und sieht weiterhin nur Koordinaten.

2. Die Aenderung gehoert in `infrastructure` und `adapters/wiring.py`.
   Neue fachliche Modellbegriffe waren nicht noetig.

3. Eine vollstaendige neue Fehlerklasse fuer einen Standortdienst wurde
   vermieden. Der Adapter bleibt beim bestehenden terminalen Fehler
   `PostleitzahlUnbekannt`, wenn keine Koordinaten bestimmt werden koennen.

4. Die lokale Umgebung ist fuer echte Laufvalidierung noch nicht ausreichend:
   `pytest` und `httpx` fehlen.

## Was gut funktioniert hat

- Der Schnitt blieb klein: Standortadapter, Wiring, Tests, README.
- Die neue PLZ `72138` ist als lokaler Fallback vorhanden und kann bei
  installierten Abhaengigkeiten auch ueber den HTTP-Pfad getestet werden.
- Der Import-/Layer-Check blieb gruen.

## Reibungspunkte

- Ohne installierte Runtime-/Testabhaengigkeiten kann der relevante Pytest-Lauf
  nicht ausgefuehrt werden.
- Der direkte Laufcheck kann ohne `httpx` nicht einmal bis zum lokalen Fallback
  importieren, weil `httpx` beim Modulimport benoetigt wird. Das entspricht
  dem bestehenden Projektzustand, denn auch der Wetterclient benoetigt `httpx`.

## Lernwert fuer das Priming

Der Schnitt zeigt eine praktische Grenze zwischen implementierter Aenderung und
validierter Aenderung. Die Regeln erzwingen hier zu Recht, die fehlende lokale
Abhaengigkeitsinstallation nicht zu uebergehen.

## Naechste Folgerung

Das Projekt braucht fuer weitere echte Ausbauten eine reproduzierbare
Installationsspur fuer Runtime- und Testabhaengigkeiten. Ohne diese bleibt jede
Integration mit HTTP-Adaptern nur teilweise validierbar.

## Nachtrag

Nach Installation von `httpx`, `pytest`, `ruff` und `mypy` in die vorhandene
lokale `.venv` konnten die blockierten Validierungen ausgefuehrt werden.

Der PLZ-Schnitt ist damit technisch validiert:

- relevante Tests: 10 passed
- volle Testsuite: 28 passed
- Import-/Layer-Check: gruen
- direkter Adaptercheck fuer `72138`: liefert Koordinaten fuer Kirchentellinsfurt
