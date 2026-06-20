# Plan: Tagesprognose — stündliche Regenbogen-Übersicht für heute

Status: abgeschlossen
Datum: 2026-06-20
Freigabe: 2026-06-20 (Dieter Haag)
Bearbeiter: Claude Sonnet 4.6

## Aufgabe

Das Programm soll nicht nur die aktuelle Stunde bewerten, sondern alle Stunden
des aktuellen Tages. Ergebnis ist eine `TagesPrognose`: eine geordnete Liste
von Stunden-Werten mit Wahrscheinlichkeit und Sichtbarkeit, plus der
`SpitzenStunde` (die Stunde mit dem höchsten Wahrscheinlichkeitswert).

Nutzernutzen: "Wann soll ich heute rausgehen?"

Ausgabe CLI:
```
Regenbogen-Prognose für Berlin — Freitag, 20.06.2026
  14:00  Wahrscheinlichkeit  62 %   Sichtbarkeit  48 %
  15:00  Wahrscheinlichkeit  78 %   Sichtbarkeit  61 %   ← Spitze
  16:00  Wahrscheinlichkeit  31 %   Sichtbarkeit  20 %
  ...
```

Neue CLI-Option: `--prognose` neben dem bestehenden Einzel-Ergebnis.
GUI-Erweiterung ist **nicht** Teil dieses Schnitts.

---

## Betroffene Räume

```text
domain/
  Neue Typen: PrognoseStunde, TagesPrognose
  Neue Datei: src/regenbogen/domain/tagesprognose.py

system/ports/
  Erweiterung: WetterApiPort um hole_stundliche_messungen()
  Neuer Typ:   StundlicheWetterApiMessung (zeitpunkt + WetterApiMessung)
  Datei:       src/regenbogen/system/ports/wetterapi_port.py

system/core/
  Neue Klasse: TagesPrognoseUseCase (SP2-A — eigene Klasse)
  Neue Datei:  src/regenbogen/system/core/tagesprognose_use_case.py

infrastructure/
  Erweiterung: OpenMeteoClient um stündliche Abfrage
  Datei:       src/regenbogen/infrastructure/open_meteo_client.py

cli/
  Erweiterung: --prognose Flag und Formatierungsfunktion
  Dateien:     src/regenbogen/cli/main.py
               src/regenbogen/cli/gui_format.py (neue Formatierfunktion)

tests/
  Neue Tests:  tests/domain/test_tagesprognose.py
               tests/system/test_tagesprognose_use_case.py
               tests/infrastructure/test_open_meteo_client.py (erweitert)
               tests/cli/test_gui_format.py (erweitert)
```

---

## Nicht-Ziele

- keine GUI-Erweiterung in diesem Schnitt
- keine Mehrtagges-Prognose (nur heute)
- keine neue Runtime-Dependency
- keine Änderung der bestehenden `berechne` / `berechne_vollstaendig` Signatur
- keine Änderung des bestehenden Retry-Verhaltens für die Einzel-Abfrage
- kein Caching der stündlichen Daten
- keine Unterstützung beliebiger Datumsangaben (nur aktueller Tag)
- keine CLI-Ausgabe für GUI-Modus (gui_main.py bleibt unberührt)
- kein Mondbogen: Regenbogenwahrscheinlichkeit bei Mondlicht ist ein eigenständiges
  Phänomen (Mondbögen existieren, sind aber selten) — explizit nicht in diesem Schnitt

---

## Sprechakt-Entscheidungen

Alle SP-Entscheidungen sind getroffen (2026-06-20, Dieter Haag).
Kein weiterer Sprechakt vor Implementierung nötig.

### SP1-A: TagesPrognose — ENTSCHIEDEN

Neuer Domain-Begriff.

Bedeutung: Geordnete Folge von Stunden-Bewertungen aller **Tagstunden**
(Stunden mit positivem Sonnenstand) des aktuellen Kalendertags an einem
Beobachtungsort.

**Entscheidung:** Nur Stunden mit positivem Sonnenstand. Nachtstunden (Sonnenstand ≤ 0)
werden nicht in `TagesPrognose.stunden` aufgenommen — sie sind fachlich irrelevant,
da ohne Sonnenlicht kein Regenbogen möglich ist.

Mondbögen (Regenbogen bei Mondlicht) sind ein reales Phänomen, aber explizit
nicht Gegenstand dieser Erweiterung.

### SP1-B: PrognoseStunde — ENTSCHIEDEN

Neuer Domain-Begriff.

Bedeutung: Bewertung eines einzelnen Zeitslots (eine Stunde) mit
Wahrscheinlichkeit und Sichtbarkeit.

**Entscheidung:** `stunde: int` (lokale Stunde 0–23) im Domain-Typ.
Konvertierung UTC → lokale Stunde erfolgt in system/core.
Nur ändern wenn und falls starke Gründe entstehen.

### SP1-C: SpitzenStunde — ENTSCHIEDEN

**Entscheidung:** `SpitzenStunde` ist kein eigenständiger Domain-Begriff.
`spitzenstunde` ist eine abgeleitete Property auf `TagesPrognose`.

### SP2-A: TagesPrognoseUseCase — ENTSCHIEDEN

**Entscheidung:** Eigene Klasse `TagesPrognoseUseCase` in
`src/regenbogen/system/core/tagesprognose_use_case.py`.
Nicht als neue Methode auf dem bestehenden `RegenbogenWahrscheinlichkeitUseCase`.

Begründung: Eine neue Klasse hält die Verantwortlichkeiten getrennt und
vermeidet schleichende Erweiterung des bestehenden Use Case.
Gemeinsame Infrastruktur (Standort-Logik, Retry) wird über Komposition geteilt,
nicht durch Vererbung oder direkte Erweiterung.

### SP3-A: Leere Prognose — ENTSCHIEDEN

**Entscheidung:** Eigene Rückmeldung — keine leere Tabelle, keine Nullen-Tabelle.

Eine TagesPrognose mit leeren `stunden` (kein Regen und/oder kein Tageslicht)
ist semantisch etwas anderes als eine Tabelle mit lauter Nullen.
Leere stunden → CLI gibt dedizierte Meldung aus: "Heute kein Regenbogen zu erwarten."

Diese Unterscheidung gilt auch für den Grenzfall, dass zwar Tagstunden vorhanden
sind, aber alle Wahrscheinlichkeiten 0 ergeben: auch das ist eine inhaltliche
Aussage, keine Fehler — aber sie braucht eine eigene Darstellung, nicht eine
Null-Tabelle.

---

## Erwartete Änderungen

### Schritt 1 — Domain

Neue Datei `src/regenbogen/domain/tagesprognose.py`:

```python
@dataclass(frozen=True)
class PrognoseStunde:
    stunde: int               # lokale Stunde 0–23 (SP1-B)
    wahrscheinlichkeit: int   # [0, 100]
    sichtbarkeit: int         # [0, 100]

@dataclass(frozen=True)
class TagesPrognose:
    ort: str
    stunden: tuple[PrognoseStunde, ...]   # nur Tagstunden (SP1-A)

    @property
    def spitzenstunde(self) -> PrognoseStunde | None:   # Property, kein Begriff (SP1-C)
        if not self.stunden:
            return None
        return max(self.stunden, key=lambda s: s.wahrscheinlichkeit)

    @property
    def hat_regenbogen_chance(self) -> bool:
        return any(s.wahrscheinlichkeit > 0 for s in self.stunden)
```

`hat_regenbogen_chance` liefert den CLI-Verzweigungspunkt für SP3-A.

Glossareinträge für `TagesPrognose` und `PrognoseStunde` anlegen.

### Schritt 2 — System-Port

Neues DTO und neue Methode in `wetterapi_port.py`:

```python
@dataclass(frozen=True)
class StundlicheWetterApiMessung:
    zeitpunkt_utc: datetime    # UTC-Zeitpunkt der Stunde
    messung: WetterApiMessung

class WetterApiPort(ABC):
    # bestehende Methode bleibt unberührt
    @abstractmethod
    def hole_stundliche_messungen(
        self,
        koordinaten: StandortKoordinaten,
        datum_utc: date,
    ) -> list[StundlicheWetterApiMessung]:
        raise NotImplementedError
```

`StundlicheWetterApiMessung` ist ein technisches Port-DTO, kein Domain-Begriff.

### Schritt 3 — Infrastructure

`OpenMeteoClient` erhält `hole_stundliche_messungen`:
- Open-Meteo `hourly`-Parameter mit denselben Feldern wie aktuelle Abfrage
- `timezone=auto` Parameter damit Open-Meteo lokale Zeiten zurückgibt
- Parst Liste von Stundenwerten in `list[StundlicheWetterApiMessung]`
- Selbe Fehlerbehandlung wie `hole_aktuelle_messung`

### Schritt 4 — System Use Case

Neue Datei `src/regenbogen/system/core/tagesprognose_use_case.py` (SP2-A):
Eigene Klasse `TagesPrognoseUseCase`.

```python
class TagesPrognoseUseCase:
    def __init__(
        self,
        wetterapi: WetterApiPort,
        standort: StandortPort,
        clock: Callable[[], datetime] = datetime.now,
    ) -> None: ...

    def berechne(
        self,
        ort: str,
        postleitzahl: str | None = None,
    ) -> TagesPrognose:
        koordinaten = self._standort.finde_koordinaten(ort, postleitzahl)
        stundliche_messungen = self._hole_mit_retry(koordinaten)
        stunden = []
        for stundenmessung in stundliche_messungen:
            sonnenstand = berechne_sonnenstand(stundenmessung.zeitpunkt_utc, koordinaten)
            if sonnenstand.hoehe <= 0:
                continue  # Nachtstunden ausfiltern (SP1-A)
            zustand = ...
            w = berechne_regenbogen_wahrscheinlichkeit(zustand, sonnenstand)
            s = ...
            lokale_stunde = _utc_zu_lokale_stunde(stundenmessung.zeitpunkt_utc, koordinaten.zeitzone)
            stunden.append(PrognoseStunde(stunde=lokale_stunde, wahrscheinlichkeit=w, sichtbarkeit=s))
        return TagesPrognose(ort=ort, stunden=tuple(stunden))
```

Retry-Verhalten wie in `RegenbogenWahrscheinlichkeitUseCase` (MAX_VERSUCHE = 3).

### Schritt 5 — CLI

`main.py` erhält `--prognose` Flag:
```
regenbogen Berlin --prognose
regenbogen Berlin --plz 10115 --prognose
```

Neue Formatierungsfunktion in `gui_format.py`:
```python
def formatiere_tagesprognose(prognose: TagesPrognose) -> str:
    ...
```

Ausgabe wenn keine Chance (SP3-A):
```
Regenbogen-Prognose für Berlin — Freitag, 20.06.2026
Heute kein Regenbogen zu erwarten.
```

Ausgabe wenn Chance vorhanden:
```
Regenbogen-Prognose für Berlin — Freitag, 20.06.2026
  14:00  Wahrscheinlichkeit  62 %   Sichtbarkeit  48 %
  15:00  Wahrscheinlichkeit  78 %   Sichtbarkeit  61 %   ← Spitze
  16:00  Wahrscheinlichkeit  31 %   Sichtbarkeit  20 %
```

`prognose.hat_regenbogen_chance` steuert die Verzweigung.
Spitzenstunde wird markiert via `prognose.spitzenstunde`.

### Schritt 6 — Tests

```text
tests/domain/test_tagesprognose.py
  - PrognoseStunde erstellen
  - TagesPrognose.spitzenstunde bei mehreren Stunden
  - TagesPrognose.spitzenstunde bei leerer Folge (→ None)
  - TagesPrognose.hat_regenbogen_chance: True wenn mindestens eine Stunde > 0
  - TagesPrognose.hat_regenbogen_chance: False bei allen Nullen
  - TagesPrognose.hat_regenbogen_chance: False bei leerer Folge

tests/system/test_tagesprognose_use_case.py
  - Prognose mit Fake-API und Fake-Standort
  - Nachtstunden (Sonnenstand ≤ 0) werden ausgefiltert (SP1-A)
  - Spitzenstunde korrekt ermittelt
  - Retry-Verhalten bei WetterApiNichtErreichbar
  - leere stunden wenn alle Stunden Nachtstunden

tests/infrastructure/test_open_meteo_client.py (erweitert)
  - hole_stundliche_messungen parst korrekte Anzahl Stunden
  - fehlende Felder werden defensiv behandelt

tests/cli/test_gui_format.py (erweitert)
  - formatiere_tagesprognose mit bekannter Prognose → Tabelle mit Spitze
  - hat_regenbogen_chance=False → "Heute kein Regenbogen zu erwarten" (SP3-A)
  - leere stunden → "Heute kein Regenbogen zu erwarten"
```

---

## Schreibrechte

```text
Erlaubt ohne Sonderfreigabe:
  src/regenbogen/domain/tagesprognose.py                    (neu)
  src/regenbogen/system/core/tagesprognose_use_case.py      (neu, SP2-A)
  src/regenbogen/system/ports/wetterapi_port.py
  src/regenbogen/infrastructure/open_meteo_client.py
  src/regenbogen/cli/main.py
  src/regenbogen/cli/gui_format.py
  tests/domain/test_tagesprognose.py                        (neu)
  tests/system/test_tagesprognose_use_case.py               (neu)
  tests/infrastructure/test_open_meteo_client.py
  tests/cli/test_gui_format.py
  docs/plans/

Glossar-Einträge (geschützt, Freigabe über SP-Artefakte):
  glossar-domain.md    (TagesPrognose, PrognoseStunde)
  glossar-system.md    (StundlicheWetterApiMessung, falls nötig)
  MODELL-README.md     (Prüfung und ggf. Update Pflicht nach Modelländerung)
```

---

## Testpflicht

```text
- jede neue Produktionsdatei braucht passende Tests
- neue Port-Methode braucht Fake-Implementierung in Tests
- neue CLI-Ausgabe braucht Formatierungstest
- MODELL-README.md prüfen: TagesPrognose erweitert das Modell —
  Beschreibung muss nachgezogen werden
- Import-/Layer-Checker nach jedem Schritt ausführen
```

---

## Abbruchbedingungen

```text
H1   Glossar oder MODELL-README ohne Freigabe geändert
H2   Import-Verletzung (z.B. domain importiert datetime von system)
H3   Widerspruch zwischen SP-Entscheidung und Implementierung
H4   TagesPrognose oder PrognoseStunde ohne SP1-Freigabe implementiert
H6   Testpflicht für neuen Port oder neue Klasse nicht ableitbar
H10  datetime in domain-Typ — Autonomieregel: Domänenexperte kann
     Stunde als int beurteilen, datetime-Semantik aber nicht ohne Systemwissen
SA1  Test rot nach Implementierungsschritt
SA4  httpx nicht installiert bei Integration-Test
```

---

## Wiedereinstiegspunkt

Nach Freigabe dieses Plans und Vorliegen aller SP-Artefakte:

```text
1. Glossareinträge anlegen (TagesPrognose, PrognoseStunde)
2. MODELL-README.md Lage prüfen — Prognose ist Modellerweiterung
3. Domain-Typen implementieren + Tests
4. Port erweitern + Fake für Tests
5. OpenMeteoClient erweitern + Tests
6. Use Case erweitern + Tests
7. CLI erweitern + Formatierungstest
8. Vollvalidierung
```

Zwischen jedem Schritt: `python tools/check_import_layers.py --preflight src tests tools`

---

## Abschlusskriterien

```text
- TagesPrognose und PrognoseStunde im Glossar eingetragen
- MODELL-README.md auf aktuellem Stand
- domain/tagesprognose.py implementiert und getestet
- WetterApiPort um hole_stundliche_messungen erweitert
- OpenMeteoClient implementiert stündliche Abfrage
- TagesPrognoseUseCase implementiert (eigene Klasse, SP2-A)
- Nachtstunden werden ausgefiltert (SP1-A)
- CLI kennt --prognose und gibt kompakte Tabelle aus
- Spitzenstunde wird in Ausgabe markiert
- leere oder null-Prognose → "Heute kein Regenbogen zu erwarten" (SP3-A)
- alle Tests grün
- Import-/Layer-Checker grün
- Lint, Format, Typecheck grün
```
