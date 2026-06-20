# Sprechakt: Fehlerklassen WetterApi

Zeitpunkt: 2026-06-11 10:20
Sprechakt-Klasse: SP3
Betroffener Begriff: WetterApiNichtErreichbar, OrtNichtGefunden
Status: festgelegt

## Festlegung

WetterApiNichtErreichbar:
  Recoverable. System darf Retry anwenden, maximal drei Versuche.

OrtNichtGefunden:
  Terminal. Kein Retry. Direkt an Aufrufer weitergeben.

## Folgeartefakte

- glossar-system.md
- src/regenbogen/system/ports/wetterapi_port.py
