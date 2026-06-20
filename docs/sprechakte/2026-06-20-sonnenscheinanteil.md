# Sprechakt: SonnenscheinAnteil

Aufgabe:          Sonnenscheinanzeige semantisch klaeren
Zeitpunkt:        2026-06-20 18:10
Sprechakt-Klasse: SP1 — Neuer Fachbegriff würde entstehen
Betroffener Begriff / Grenze: SonnenscheinAnteil
Status: festgelegt
Folgeartefakte:
- glossar-domain.md
- MODELL-README.md
- README.md
- src/regenbogen/cli/gui_format.py
- tests/cli/test_gui_format.py
Ersetzt:
Ersetzt durch:

## Was fehlt

Die bisherige Anzeige `Sonnenschein (25 %)` konnte als
Sonnenscheinwahrscheinlichkeit gelesen werden. Tatsächlich ist der Wert ein
aus `sunshine_duration / 3600` abgeleiteter Anteil einer Bezugsstunde.

## Was der Agent sieht

symbol:
  sonnenschein_intensitaet
package_says:
  Domain darf Fachbegriffe halten; technische API-Felder bleiben ausserhalb der Domain.
glossar_says:
  Wetterzustand nennt Intensitaeten in [0.0, 1.0], aber kein eigener Begriff
  klaert den Sonnenscheinanteil.
code_says:
  `sonnenschein_intensitaet = min(sunshine_duration / 3600.0, 1.0)`
tests_say:
  CLI-Format prueft nur grob auf `Sonnenschein`.
schema_says:
  Keine abweichende Raumregel.

## Analyse des Agenten

Der Wert ist fachlich relevant fuer das Modell, aber kein
Wahrscheinlichkeitswert. Eine reine UI-Textaenderung waere zu schwach, weil
Modell-README und Glossar ebenfalls klarstellen muessen, was der Wert bedeutet.

## Vorschlag des Agenten

Den Begriff `SonnenscheinAnteil` als Domain-Begriff einfuehren:

```text
Anteil einer Bezugsstunde, in der direkte Sonneneinstrahlung beobachtet wurde.
Wert in [0.0, 1.0]. Wird aus sunshine_duration / 3600 abgeleitet.
Keine Wahrscheinlichkeit.
```

## Warum der Agent nicht fortfahren kann

Ohne Begriffsfestlegung wuerde die Korrektur nur den Anzeigetext reparieren,
aber die Modellbedeutung bliebe implizit.

## Was der Mensch festlegt

`SonnenscheinAnteil` ist der kanonische Fachbegriff fuer den aus
`sunshine_duration / 3600` abgeleiteten Anteil einer Bezugsstunde mit direkter
Sonneneinstrahlung. Er ist keine Wahrscheinlichkeit.

## Was der Agent danach tut

1. `glossar-domain.md` ergaenzen
2. Ausgabeformat anpassen
3. Tests aktualisieren
4. `MODELL-README.md` und `README.md` nachziehen
5. Validierung ausfuehren
