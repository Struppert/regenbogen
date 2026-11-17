# PROJEKT.md — Regenbogen: Architektur und Orientierung

> Ebene: REPOSITORY
> Rolle: Projektlandkarte fuer Menschen und Agenten
> Geltung: dieses Projekt
> Autoritative Frage: Wie ist Regenbogen aufgebaut und was liegt wo?
> Nicht zustaendig fuer: Begriffsbedeutungen, Importregeln im Detail, Laufsteuerung

> Dieses Dokument beschreibt das Projekt in Prosa. Es ist die erste Anlaufstelle
> fuer die Frage "wo finde ich was". Bedeutungen stehen im Glossar, die
> Zuordnung von Namen zu Dateien im Begriffsindex, Regeln in
> `REGELN-UND-TOOLS.md`, Raumregeln und Importmatrix in `package-schema.md`.

---

## 1. Was das Projekt macht

Regenbogen berechnet fuer einen Ort die Wahrscheinlichkeit und die
Sichtbarkeit eines Regenbogens. Es holt Wetterdaten von Open-Meteo,
bestimmt den Sonnenstand, leitet daraus die optischen Bedingungen ab und
liefert eine Prozentzahl, eine Blickrichtung und auf Wunsch eine stuendliche
Tagesprognose, auch mit Sekundaerbogen.

Fachliche Beschreibung: `README.md` (Nutzer) und `MODELL-README.md`
(aktuell implementiertes Modell). Diese Datei wiederholt sie nicht.

---

## 2. Aufbau nach semantischen Raeumen

```text
src/regenbogen/
  domain/           Fachdomaene: Regeln und Typen ohne Laufzeitmechanik
  system/
    core/           Use Cases und Ableitungen (Ablaufregeln, Retry, Politik)
    ports/          abstrakte Schnittstellen und Fehlerwerte
  infrastructure/   Technik: HTTP, Postleitzahlen, Logging
  adapters/         Verdrahtung der Raeume
  cli/              Einstiegspunkte und Oberflaeche
tests/              Testprojektionen, gespiegelt nach Raeumen
tools/              Checker und Hilfswerkzeuge der Agenten-Box
```

Was in einem Raum liegen darf, steht in `package-schema.md`. Hier steht,
was heute tatsaechlich dort liegt:

| Raum | Dateien | Rolle |
|---|---|---|
| domain | `regenbogen.py`, `regenbogen_geometrie.py`, `regenbogen_optik.py`, `tagesprognose.py`, `wetter.py` | Wetterzustand, Wahrscheinlichkeit, Geometrie (Sonnenstand, Blickrichtung, Sekundaerbogen), Sichtbarkeit, Prognosetypen |
| system/core | `wahrscheinlichkeit_use_case.py`, `tagesprognose_use_case.py`, `optische_bedingungen.py`, `sonnenstand.py` | Use Cases mit Retry, Ableitung optischer Bedingungen, Sonnenstandsberechnung |
| system/ports | `wetterapi_port.py`, `standort_port.py`, `logging_port.py` | Schnittstellen und Fehlerwerte (`OrtNichtGefunden`, `WetterApiNichtErreichbar`, `PostleitzahlUnbekannt`) |
| infrastructure | `open_meteo_client.py`, `plz_lookup.py`, `event_logger.py` | Open-Meteo-Client (httpx), Standortaufloesung, Logging |
| adapters | `wiring.py` | baut die produktiven Use Cases aus den Infrastrukturteilen |
| cli | `main.py`, `gui_main.py`, `gui_format.py`, `config_dialog.py`, `ausgabe_fenster.py` | Kommandozeile, Fenster (tkinter), Textformatierung |

Welcher Begriff in welcher Datei steht: `BEGRIFFSINDEX.md`.

---

## 3. Einstiegspunkte

```text
regenbogen       src/regenbogen/cli/main.py:main        Kommandozeile
regenbogen-gui   src/regenbogen/cli/gui_main.py:main    Fenster
```

Beide rufen ueber `adapters/wiring.py` die Use Cases auf. Dort entstehen die
echten Verbindungen (Netzwerk, Zeit, Schlaf). Alles darunter bekommt sie
injiziert und ist dadurch ohne Netz testbar.

---

## 4. Datenfluss in einem Lauf

```text
Eingabe (Ort, optional PLZ)
  -> StandortPort           Koordinaten finden            (infrastructure/plz_lookup)
  -> Sonnenstand            aus Uhrzeit und Koordinaten   (system/core/sonnenstand)
  -> WetterApiPort          Messung holen, mit Retry      (infrastructure/open_meteo_client)
  -> Wetterzustand          Messung in Fachbegriffe       (system/core + domain/wetter)
  -> Wahrscheinlichkeit     Sonne, Regen, Sonnenstand     (domain/regenbogen)
  -> Sichtbarkeit           optische Faktoren             (system/core/optische_bedingungen, domain/regenbogen_optik)
  -> Ausgabe                Prozent, Blickrichtung        (cli)
```

Die Tagesprognose wiederholt das fuer jede Stunde und fuegt den
Sekundaerbogen hinzu (`system/core/tagesprognose_use_case.py`).

---

## 5. Externe Abhaengigkeiten

```text
httpx      HTTP-Client fuer Open-Meteo und Postleitzahlen (Runtime-Dependency)
tkinter    Fenster der GUI (Standardbibliothek)
```

Neue Runtime-Dependencies brauchen Freigabe (Sprechakt SP4, H8).

---

## 6. Tests

```text
tests/domain/          Fachregeln
tests/system/          Use Cases, Winkelmodell, optische Bedingungen, Logging
tests/infrastructure/  Open-Meteo-Client, Postleitzahlen (benoetigen httpx)
tests/cli/             Formatierung
tools/tests/           Tests der Agenten-Box-Werkzeuge
```

Welche Tests zu einer geaenderten Datei gehoeren, leitet
`tools/resolve_test_obligations.py` ab (siehe `REGELN-UND-TOOLS.md`).

---

## 6a. Bekannte Brueche und oeffentliche API

```text
Bekannte Brueche:   keine eingetragen (package-schema.md, Abschnitt Known Breaches)
Bridge-Symbole:     keine eingetragen (migration-bridges.md)
Oeffentliche API:   Kommandos regenbogen und regenbogen-gui;
                    src/regenbogen/__init__.py ist leer
```

Offene Beobachtung: Der Begriff `SonnenscheinAnteil` steht im Domain-Glossar,
seine einzige Umsetzung liegt aber in `system/core` (im Use Case). Das ist zu
klaeren, bevor der Begriff als sauber verortet gilt (Begriffsindex,
Warnung Raum gegen Pfad).

---

## 7. Wo finde ich was

```text
Bedeutung eines Begriffs            glossar-domain.md, glossar-system.md
Datei zu einem Namen                BEGRIFFSINDEX.md
Regeln und Werkzeugaufrufe          REGELN-UND-TOOLS.md
Importregeln und Raumgrenzen        package-schema.md
Schreibrechte und Autoritaet        regelmatrix.md
Ablauf vor einer Aenderung          preflight-checkliste.md
Aufgaben-Lebenszyklus, Merge-Gate    aufgaben-lebenszyklus-protokoll.md
Abgeschlossene Aufgaben             docs/aufgabenindex.md
Menschliche Entscheidungen          docs/sprechakte/
Plaene der Arbeitslaeufe            docs/plans/
Erfahrungen und Abbrueche           .agent-box/evidence/erfahrungsberichte/
Fachliches Modell                   MODELL-README.md
Nutzung des Programms               README.md
```

---

## 8. Wo gehört neuer Code hin

```text
Fachlicher Begriff                              → domain
Use Case / Ablaufregel / Policy                 → system
Fehlerklassifikation                            → system
DB / HTTP / Filesystem / Queue / Framework      → infrastructure
Übersetzung zwischen Räumen                     → adapters
CLI / Prozessstart / Argumente / Environment    → cli oder entrypoints
Tests                                           → tests
Agenten-/Entwicklungstools                      → tools
Semantisch neutrale Hilfstypen                  → shared (mit Vorsicht)
```

Wenn keine Zuordnung möglich ist:
Task-Schnitt prüfen. Dann Sprechakt. Nicht raten.

---

## 9. Pflege

Dieses Dokument ist mit dem Code zu aktualisieren, wenn Dateien, Raeume,
Einstiegspunkte oder Abhaengigkeiten sich aendern. Es fuehrt keine Begriffe
ein und keine Regeln. Widerspricht es dem Code, gilt der Code als Befund und
das Dokument ist nachzuziehen.
