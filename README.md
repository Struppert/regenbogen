# Regenbogen

`Regenbogen` ist ein kleines Python-Programm, das fuer einen Ort die
Wahrscheinlichkeit eines sichtbaren Regenbogens abschaetzt.

Das Programm verbindet drei Dinge:

- einen Beobachtungsort
- aktuelle Wetterdaten
- ein einfaches Modell fuer Sonnenstand und Regenbogenoptik

Das Ergebnis ist kein meteorologisches Vorhersagesystem, sondern ein
nachvollziehbares Beispielprogramm: Es zeigt, wie aus Wetter- und
Standortdaten eine fachliche Abschaetzung fuer `RegenbogenWahrscheinlichkeit`
und `RegenbogenSichtbarkeit` abgeleitet werden kann.

## Was das Programm macht

Fuer einen Ort ruft `Regenbogen` aktuelle Wetterdaten ab und berechnet:

- `Regenbogen-Wahrscheinlichkeit` als Prozentwert in `[0, 100]`
- `Sichtbarkeit` als separaten Score in `[0, 100]`

Die Wahrscheinlichkeitslogik folgt dem einfachen fachlichen Kern:

- ohne Sonnenschein: `0`
- ohne Regen: `0`
- mit Sonnenschein und Regen: grobe Wahrscheinlichkeit aus Intensitaeten
- zusaetzlich beeinflusst der Sonnenstand das Ergebnis

Der Sichtbarkeits-Score bewertet nicht nur, ob ein Regenbogen moeglich ist,
sondern wie gut er unter den aktuellen Bedingungen voraussichtlich zu sehen
waere.

## Wie das Programm funktioniert

Der Ablauf ist:

1. Ort und optionale Postleitzahl entgegennehmen
2. Koordinaten des Beobachtungsorts bestimmen
3. Sonnenstand fuer Ort und Zeitpunkt berechnen
4. aktuelle Wetterdaten laden
5. Wetterdaten in einen fachlichen `Wetterzustand` uebersetzen
6. Wahrscheinlichkeit und Sichtbarkeit berechnen
7. Ergebnis in CLI oder GUI ausgeben

## Fachliches Modell

### Wetterzustand

`Wetterzustand` ist die beobachtete Kombination von Wetterphaenomenen zu einem
Zeitpunkt an einem Ort.

Wichtig:

- Sonnenschein und Regen koennen gleichzeitig auftreten
- Intensitaeten liegen jeweils in `[0.0, 1.0]`
- `sonnenschein=True` erfordert eine positive Sonnenintensitaet
- `regen=True` erfordert eine positive Regenintensitaet

### Regenbogen-Wahrscheinlichkeit

Die `RegenbogenWahrscheinlichkeit` ist ein Prozentwert in `[0, 100]`.

Das Programm kombiniert:

- Sonnenintensitaet
- Regenintensitaet
- geometrischen Sonnenstands-Faktor

Der Sonnenstands-Faktor ist fuer einen normalen primaeren Regenbogen nur dann
guenstig, wenn die Sonne:

- ueber dem Horizont steht
- aber nicht zu hoch steht

Im Modell gilt:

- Sonnenhoehe `<= 0 Grad` -> Faktor `0`
- Sonnenhoehe `>= 42 Grad` -> Faktor `0`
- niedrige bis mittlere Sonnenhoehen sind am guenstigsten

### Regenbogen-Sichtbarkeit

Die `RegenbogenSichtbarkeit` ist ein separater Score in `[0, 100]`.

Sie wird aus mehreren Faktoren abgeleitet:

- Sonnenstands-Faktor
- Regenmenge
- Direktlicht
- Tropfenqualitaet
- Sichtweite
- Hintergrundkontrast
- Niederschlagsphase

Das Modell bevorzugt typischen fluessigen Niederschlag fuer einen normalen
Sonnen-Regenbogen. Schnee oder Eis werden deutlich abgewertet.

## Verwendete Daten

Aktuell nutzt das Programm:

- Standortdaten aus einer PLZ-Aufloesung fuer deutsche Postleitzahlen
- aktuelle Wetterdaten von Open-Meteo

Die Wetterabfrage verwendet insbesondere:

- `sunshine_duration`
- `precipitation`
- `rain`
- `showers`
- `snowfall`
- `weather_code`
- `cloud_cover`
- `visibility`
- `direct_radiation`
- `temperature_2m`

Diese Werte werden nicht unveraendert an den Benutzer durchgereicht, sondern in
fachliche Begriffe und heuristische Faktoren uebersetzt.

## Orte und Grenzen der Standortauflosung

Die Standortauflosung nutzt fuer deutsche Postleitzahlen einen externen
PLZ-Dienst. Fuer bekannte Beispielorte gibt es zusaetzlich lokale Fallbacks,
damit das Programm auch ohne erfolgreiche PLZ-Abfrage fuer diese Orte
ausprobierbar bleibt.

Lokale Fallbacks existieren aktuell fuer:

- `Berlin` / `10115`
- `Muenchen` / `80331`
- `Kirchentellinsfurt` / `72138`

Unbekannte Eingaben fuehren derzeit zu einem terminalen Standortfehler.

Weitere Grenzen des Beispiels:

- keine vollstaendige freie Texteingabe fuer beliebige Ortsnamen
- keine echte Regenfront-Erkennung
- kein Radar
- keine astronomisch exakte Spezialoptik
- heuristische Ableitung der Tropfenqualitaet aus Standard-Wetterdaten

Das Programm ist damit ein gutes Erklaerungs- und Testbeispiel, aber kein
vollstaendiges meteorologisches Fachsystem.

## Datenfluss im Projekt

Die wichtigsten Projektteile sind:

- `src/regenbogen/cli/`
  - CLI und GUI
- `src/regenbogen/adapters/wiring.py`
  - verbindet die konkreten Komponenten fuer den Standardlauf
- `src/regenbogen/system/core/`
  - Ablaufsteuerung, Sonnenstandsberechnung und Ableitung optischer Bedingungen
- `src/regenbogen/domain/`
  - fachliche Begriffe und Berechnungen
- `src/regenbogen/infrastructure/`
  - Wetter-Client, Logging und Demo-Standortquelle

Kurzform des Laufs:

```text
CLI / GUI
  -> Wiring
  -> Use Case
  -> Standort + Wetterdaten
  -> Sonnenstand + optische Bedingungen
  -> fachliche Berechnung
  -> Ausgabe
```

## Modellbeschreibung

Die zusammenhängende Beschreibung des aktuell implementierten Modells steht in
[MODELL-README.md](air-file://gvmdc6n3maq77b7l3om5/home/dieter/repos/regenbogen/MODELL-README.md?type=file&root=%252F).

Dieses Dokument erklärt:

- welche Wetter- und Standortdaten in das Modell eingehen
- wie daraus fachliche Begriffe und Faktoren abgeleitet werden
- wie `RegenbogenWahrscheinlichkeit` und `RegenbogenSichtbarkeit`
  zustandekommen
- welche Grenzen und Heuristiken der aktuelle Modellstand hat

## Installation

Die Installationshinweise stehen in [INSTALLATION.md](air-file://gvmdc6n3maq77b7l3om5/home/dieter/repos/regenbogen/INSTALLATION.md?type=file&root=%252F).

Kurz:

- Dependencies werden ueber `pyproject.toml` installiert
- `uv` wird fuer die lokale `.venv` verwendet
- fuer Wetter- und PLZ-HTTP-Zugriffe wird `httpx` benoetigt
- fuer die GUI wird eine Python-Installation mit Tk-Unterstuetzung benoetigt

## Nutzung

### CLI

```bash
.venv/bin/regenbogen Berlin
.venv/bin/regenbogen Berlin --plz 10115
.venv/bin/regenbogen Kirchentellinsfurt --plz 72138
```

Die Befehle werden nach der Installation aus dem Projektroot gestartet. Die CLI gibt die berechnete
Regenbogen-Wahrscheinlichkeit als Prozentwert aus.

Moegliche Fehlerfaelle:

- Ort oder PLZ unbekannt
- Wetterdienst nicht erreichbar

### GUI

```bash
.venv/bin/regenbogen-gui
```

Die GUI fragt Ort und optionale Postleitzahl ab und zeigt anschliessend:

- Wetterlage
- Regenbogen-Wahrscheinlichkeit
- Sichtbarkeit

## Beispielhafte Interpretation

Typischerweise ist ein gutes Ergebnis zu erwarten, wenn:

- die Sonne scheint
- gleichzeitig Regen faellt
- die Sonne nicht zu hoch steht
- ausreichend Direktlicht vorhanden ist
- der Niederschlag zu fluessigen Tropfen passt
- Sicht und Hintergrund den Regenbogen nicht komplett verschlucken

Ein hoher Wahrscheinlichkeitswert bedeutet also:

`Unter diesen Bedingungen ist ein normaler sichtbarer Regenbogen plausibel.`

Ein hoher Sichtbarkeitswert bedeutet:

`Wenn ein Regenbogen auftritt, duerfte er unter den aktuellen Bedingungen
vergleichsweise gut zu sehen sein.`

## Weiterer Ausbau

Das Beispiel kann spaeter um weitere wetterbezogene Signale erweitert werden,
etwa:

- Windrichtung und Windgeschwindigkeit
- zeitliche Trends der Niederschlags- und Strahlungsdaten
- heuristische Aussagen zur Guenstigkeit der Regenlage

Der aktuelle Stand bleibt absichtlich klein und nachvollziehbar.
