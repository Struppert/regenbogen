# Modell-README: Regenbogen

Dieses Dokument beschreibt das aktuell implementierte Modell von `Regenbogen`.
Es ist die zusammenhängende Modellbeschreibung für Menschen. Es ersetzt weder
Glossar noch Code, sondern erklärt, wie die vorhandenen Begriffe und
Ableitungen im aktuellen Stand zusammenwirken.

## Zweck des Modells

Das Modell schätzt für einen Beobachtungsort zwei Größen:

- `RegenbogenWahrscheinlichkeit` in `[0, 100]`
- `RegenbogenSichtbarkeit` in `[0, 100]`

Die erste Größe beantwortet:

`Wie plausibel ist unter den aktuellen Bedingungen ein sichtbarer normaler
Sonnen-Regenbogen?`

Die zweite Größe beantwortet:

`Wie gut dürfte ein solcher Regenbogen unter den aktuellen Bedingungen zu
sehen sein?`

Das Modell wendet dieselben Berechnungen auf alle Tagstunden des aktuellen Tages an
und liefert damit eine `TagesPrognose` — eine geordnete Folge von `PrognoseStunde`-Werten
für jede Stunde mit positivem Sonnenstand. Daraus wird die Spitzenstunde abgeleitet.

## Modellgrenze

Das Modell ist bewusst heuristisch. Es ist kein vollständiges optisches oder
meteorologisches Fachmodell.

Es modelliert insbesondere nicht:

- echte Regenfront-Geometrie
- räumliche Verteilung des Niederschlags um den Beobachter
- Radar- oder Satellitendaten
- Spektraloptik, Mehrfachregenbogen oder Spezialformen
- exakte Mikrophysik der Tropfen

## Einschätzung des Modellwerts

Der aktuelle Wert des Modells liegt nicht darin, bereits ein belastbares
meteorologisches Fachsystem zu sein, sondern in einer guten Zwischenstufe:

- stärker als ein reines Spielzeugbeispiel
- klein genug, um fachlich vollständig nachvollziehbar zu bleiben
- konkret genug, um echte Wetter- und Optiksignale zu verarbeiten
- offen für kontrollierte Erweiterungen in Richtung eines ernsteren Modells

Das Modell hat im aktuellen Stand vier praktische Stärken:

1. Es koppelt reale Wetterdaten mit einer sichtbaren fachlichen Ableitung.
2. Es trennt Wahrscheinlichkeit und Sichtbarkeit, statt nur einen einzigen
   simplen Score auszugeben.
3. Es bildet bereits mehrere reale Einflussgrößen ab:
   Sonnenstand, Regenmenge, Direktlicht, Sicht, Kontrast und
   Niederschlagsphase.
4. Es ist klein genug, dass Modelländerungen begrifflich sauber geführt werden
   können.

Sein aktueller Erkenntniswert ist daher:

- gut als erklärbares Beispielprogramm
- gut als Testbett für Modell- und Priming-Iterationen
- gut als Ausgangspunkt für ein schrittweise ernster werdendes
  meteorologisches Modell
- noch nicht ausreichend für belastbare operative Vorhersagen

Kurzform:

`Das Modell ist bereits fachlich interessant, aber noch bewusst heuristisch und
experimentell.`

## Eingaben des Modells

Das implementierte Modell verwendet drei Eingangsebenen.

### 1. Technische Eingangsdaten

Diese Werte kommen aus Standort- und Wetterquellen:

- Koordinaten und Zeitzone des Beobachtungsorts
- aktuelle Wetterfelder von Open-Meteo:
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

Diese Felder sind noch keine Fachbegriffe des Modells, sondern technische
Mess- oder API-Werte.

### 2. Systemische Ableitungen

Aus den technischen Eingangsdaten werden im System abgeleitet:

- Sonnenstand für den konkreten Ort und Zeitpunkt
- ein `Wetterzustand`
- optische Hilfsfaktoren für die Sichtbarkeit

Diese Ableitungen verbinden technische Wetterwerte mit der fachlichen
Berechnung.

### 3. Fachliche Zielbegriffe

Das Modell arbeitet fachlich mit:

- `Wetterzustand`
- `SonnenscheinAnteil`
- `Sonnenstand`
- `SonnenstandsFaktor`
- `RegenbogenWahrscheinlichkeit`
- `RegenbogenSichtbarkeit`
- `TropfenQualitaet`

Diese Begriffe sind die eigentlichen Modellbegriffe. Ihre Bedeutungen liegen
im Glossar oder sind dort über Sprechakte festgelegt.

## Modellteil A: Wetterzustand

`Wetterzustand` ist die fachliche Projektion der aktuellen Wetterlage an einem
Ort zu einem Zeitpunkt.

Aus den Wetterdaten werden zwei Intensitäten normiert:

- `SonnenscheinAnteil` aus `sunshine_duration`
- Regenintensität aus `precipitation`

Die Normierung im aktuellen Modell ist heuristisch:

- `sunshine_duration / 3600.0`, gedeckelt auf `1.0`
- `precipitation / 10.0`, gedeckelt auf `1.0`

`SonnenscheinAnteil` bedeutet dabei: Anteil einer Bezugsstunde, in der direkte
Sonneneinstrahlung beobachtet wurde. Der Wert ist keine Wahrscheinlichkeit.

Aus diesen Intensitäten wird entschieden:

- `sonnenschein=True`, wenn der `SonnenscheinAnteil` größer als `0.0` ist
- `regen=True`, wenn die normierte Regenintensität größer als `0.0` ist

## Modellteil B: Sonnenstand

Der Sonnenstand wird aus:

- Uhrzeit
- Datum
- Koordinaten
- Zeitzone

berechnet.

Ergebnis ist ein `Sonnenstand` mit:

- Sonnenhöhe
- Sonnenazimut

Für die Regenbogenwahrscheinlichkeit wird daraus der
`SonnenstandsFaktor` abgeleitet.

Im aktuellen Modell gilt:

- Sonne unter dem Horizont -> Faktor `0`
- Sonne ab `42 Grad` Höhe -> Faktor `0`
- niedrige bis mittlere Sonnenhöhen sind günstig

Das bildet die bekannte Bedingung ab, dass ein normaler primärer Regenbogen
vor allem bei tieferer Sonne sichtbar wird.

## Modellteil C: Regenbogen-Wahrscheinlichkeit

Die `RegenbogenWahrscheinlichkeit` ist die einfachere der beiden Zielgrößen.

Sie folgt diesen Kernregeln:

- ohne Sonnenschein -> `0`
- ohne Regen -> `0`
- sonst Kombination aus Sonnenscheinanteil und Regenintensität
- optional multipliziert mit dem `SonnenstandsFaktor`

Im aktuellen Modell gewichtet die Basis:

- Sonnenscheinanteil mit `0.6`
- Regenintensität mit `0.4`

Dann wird auf einen Prozentwert in `[0, 100]` gerundet.

## Modellteil D: Regenbogen-Sichtbarkeit

Die `RegenbogenSichtbarkeit` ist stärker heuristisch und kombiniert mehrere
Einflussgrößen.

Sie wird nur positiv, wenn mindestens diese Bedingungen erfüllt sind:

- günstiger Sonnenstand
- vorhandener flüssiger Niederschlag
- vorhandenes Direktlicht
- keine reine Schnee-/Eisphase

Die Sichtbarkeit ergibt sich aus dem Produkt mehrerer Faktoren:

- Sonnenstands-Faktor
- Regen-Faktor
- Direktlicht-Faktor
- Tropfenqualität
- Sicht-Faktor
- Hintergrundkontrast-Faktor
- Niederschlagsphasen-Faktor

Der Score wird anschließend auf `[0, 100]` begrenzt.

## Ableitung der Sichtbarkeitsfaktoren

### Regen-Faktor

Der Regen-Faktor basiert auf der verfügbaren Wasser-Niederschlagsmenge:

- bevorzugt `rain + showers`
- falls diese `0` sind, aber `precipitation > 0` und kein Schnee vorliegt:
  Fallback auf `precipitation`

Bis `5 mm` wird die Regenmenge auf einen Faktor in `[0, 1]` normiert.

### Direktlicht

Direktlicht wird aus `direct_radiation` abgeleitet:

- `direct_radiation / 400.0`
- begrenzt auf `[0, 1]`

Ohne Direktlicht liefert das Modell keine positive Sichtbarkeit.

### Sicht

Sichtweite wird aus `visibility` abgeleitet:

- `visibility / 10000.0`
- begrenzt auf `[0, 1]`

Fehlt die Sichtweitenmessung, verwendet das Modell konservativ `0.7`.

### Hintergrundkontrast

Bewölkung dient als grobe Heuristik für den Kontrast hinter dem Regenbogen:

- wenig Bewölkung -> etwas schwächerer Kontrast
- mittlere Bewölkung -> günstig
- sehr hohe Bewölkung -> leicht abgewertet

### Tropfenqualität

Die Tropfenqualität beschreibt, wie gut die vorhandene Niederschlagsart und
-menge zu einem normalen sichtbaren Regenbogen passt.

Sie wird heuristisch aus:

- `weather_code`
- Wasser-Niederschlagsmenge

abgeleitet.

Das Modell bevorzugt normalen Regen und Schauer und wertet Schnee,
gefrierende Formen oder sehr ungeeignete Niederschlagsarten ab.

### Niederschlagsphase

Die Niederschlagsphase wird ebenfalls heuristisch bewertet.

Stark abgewertet oder ausgeschlossen werden:

- Schnee
- gefrierende oder eisnahe Niederschlagsformen

`temperature_2m` wird dabei aktuell nur indirekt verwendet:

- sehr kalte Temperaturen senken die Eignung der Niederschlagsphase
- Temperatur ist im aktuellen Stand kein eigenständiger fachlicher Zielbegriff,
  sondern ein technisches Hilfssignal für die Heuristik

## Fehler- und Ablaufannahmen

Das Modell läuft in einem Use Case mit folgenden Annahmen:

- Standort wird zuerst in Koordinaten übersetzt
- Wetterdaten werden danach geholt
- vorübergehende Unerreichbarkeit der Wetter-API ist retrybar
- unbekannter Ort ist terminal
- unbekannte Postleitzahl ist terminal

Diese Regeln gehören nicht zur fachlichen Optik des Regenbogens, aber zum
implementierten Laufmodell des Programms.

## Aktueller Modellzuschnitt

Das aktuelle Modell ist absichtlich klein und erklärbar:

- ein Beobachtungsort
- ein aktueller Wetterzeitpunkt oder alle Tagstunden des aktuellen Tages
- eine lokale Sonnenstandsberechnung
- heuristische Kopplung von Niederschlag, Licht und Sichtbedingungen

Das Modell unterscheidet zwei Betriebsmodi:

- **Einzelzeitpunkt**: liefert `WetterErgebnis` mit aktuellem Stand
- **Tagesprognose**: liefert `TagesPrognose` mit allen Tagstunden (positiver Sonnenstand)

Für die Tagesprognose werden stündliche Wetterdaten von Open-Meteo abgerufen.
Die Modellrechnung (Modellteil A–D) ist dabei pro Stunde identisch mit dem Einzelmodus.
Nachtstunden (Sonnenstand ≤ 0°) werden gefiltert — ohne Sonnenlicht ist kein
Sonnen-Regenbogen möglich.

Ergibt die Prognose keine Stunde mit positiver Wahrscheinlichkeit, lautet die
semantische Aussage "Heute kein Regenbogen zu erwarten" — nicht "Fehler" und
nicht "leeres Ergebnis".

Damit ist es stark genug, um echte meteorologische Modellierungsschritte
vorzubereiten, aber klein genug, um fachliche Änderungen kontrolliert und
begrifflich sauber weiterzuentwickeln.

## Pflege-Regel

Wenn sich das implementierte Modell ändert, muss dieses Dokument geprüft und
bei Bedarf aktualisiert werden.

Dazu gehören insbesondere Änderungen an:

- fachlichen Zielgrößen
- Modellfaktoren
- Heuristiken
- Übersetzung technischer Wetterfelder in fachliche Begriffe
- systemischen Ablaufannahmen, soweit sie das Modell sichtbar prägen

Neue fachliche Modellbegriffe entstehen nicht still in diesem Dokument.
Wenn ein neuer Domain-Begriff nötig wird, muss das Glossar geprüft und bei
Bedarf per Sprechakt erweitert werden.
