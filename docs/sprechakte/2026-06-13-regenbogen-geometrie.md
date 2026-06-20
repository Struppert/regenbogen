# Sprechakt: Regenbogen-Geometrie und Sonnenstand

Zeitpunkt: 2026-06-13 09:10
Sprechakt-Klasse: SP7
Betroffener Begriff: Sonnenstand, Sonnenhoehe, Sonnenazimut, Regenbogenwinkel, SonnenstandsFaktor
Status: festgelegt

## Festlegung

Sonnenhoehe:
  Winkel der Sonne ueber dem Horizont in Grad.

Sonnenazimut:
  Himmelsrichtung der Sonne in Grad.

SonnenstandsFaktor:
  Faktor in [0, 1].
  - Sonnenhoehe <= 0 Grad: 0
  - 0 Grad < Sonnenhoehe <= 25 Grad: 1
  - 25 Grad < Sonnenhoehe < 42 Grad: linear fallend
  - Sonnenhoehe >= 42 Grad: 0

## Modellgrenze

Ohne Regenzellenrichtung bleibt das Ergebnis ein Sichtbarkeits-Score,
kein Nachweis eines sichtbaren Regenbogens.
