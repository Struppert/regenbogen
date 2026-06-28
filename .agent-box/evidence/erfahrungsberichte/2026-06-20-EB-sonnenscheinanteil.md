# Erfahrungsbericht: Sonnenscheinanteil

Zeitpunkt: 2026-06-20
Bezug auf Plan: `docs/plans/2026-06-20-sonnenscheinanteil-begriffsklaerung.md`

## Kontext

Die Anzeige `Sonnenschein (25 %)` wurde als Sonnenscheinwahrscheinlichkeit
missverstanden. Der Code berechnet aber einen Anteil aus
`sunshine_duration / 3600`.

## Beobachtungen

1. Der Fehler lag nicht in der numerischen Berechnung, sondern in der
   begrifflichen Projektion nach aussen.
2. Eine reine UI-Korrektur haette die Modellbedeutung nicht dauerhaft
   stabilisiert.
3. Der neue Begriff `SonnenscheinAnteil` gehoert ins Domain-Glossar, weil er
   als fachlicher Modellfaktor genutzt wird.

## Was gut funktioniert hat

- Der Fund war klein, aber semantisch relevant.
- Das Zusammenspiel aus Glossar, Modell-README, README und Test hat die
  Korrektur gezwungen, nicht nur oberflaechlich zu bleiben.
- Die bestehende Modell-README-Pflicht hat direkt gegriffen.

## Reibungspunkte

- Der Code verwendet intern weiterhin `sonnenschein_intensitaet`. Das ist fuer
  diesen Schnitt toleriert, weil der Begriff im Glossar und der Anzeige
  geklaert wurde. Eine spaetere Umbenennung waere ein eigener Refactoring-
  Schnitt.

## Lernwert fuer das Priming

Dieser Schnitt zeigt klar, warum Begriffsdokumentation und UI-Text nicht
getrennt betrachtet werden koennen. Ein Prozentwert wird ohne expliziten
Begriff schnell als Wahrscheinlichkeit gelesen.

## Naechste Folgerung

Bei kuenftigen Wetterwerten sollte frueh geklaert werden:

- Ist der Wert ein Anteil?
- Ist er eine Intensitaet?
- Ist er eine Wahrscheinlichkeit?
- Oder ist er nur ein technisches API-Feld?
