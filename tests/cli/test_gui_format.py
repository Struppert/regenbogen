from regenbogen.cli.gui_format import formatiere_tagesprognose, formatiere_wetter
from regenbogen.domain.regenbogen_geometrie import Sonnenstand
from regenbogen.domain.tagesprognose import PrognoseStunde, TagesPrognose
from regenbogen.domain.wetter import Wetterzustand
from regenbogen.system.core.wahrscheinlichkeit_use_case import WetterErgebnis


def ergebnis(zustand: Wetterzustand, wahrscheinlichkeit: int) -> WetterErgebnis:
    return WetterErgebnis(
        ort="Berlin",
        postleitzahl="10115",
        zustand=zustand,
        sonnenstand=Sonnenstand(sonnenhoehe_grad=20.0, sonnenazimut_grad=250.0),
        wahrscheinlichkeit=wahrscheinlichkeit,
        sichtbarkeit=wahrscheinlichkeit,
    )


def test_formatiert_beide_faktoren():
    ausgabe = formatiere_wetter(
        ergebnis(
            Wetterzustand(
                sonnenschein=True,
                regen=True,
                sonnenschein_intensitaet=0.5,
                regen_intensitaet=0.5,
            ),
            50,
        )
    )
    assert "Sonnenscheinanteil (50 % der Stunde)" in ausgabe
    assert "Regen" in ausgabe
    assert "50 %" in ausgabe


def test_formatiert_kein_regen():
    ausgabe = formatiere_wetter(
        ergebnis(
            Wetterzustand(
                sonnenschein=True,
                regen=False,
                sonnenschein_intensitaet=0.8,
            ),
            0,
        )
    )
    assert "Sonnenscheinanteil (80 % der Stunde)" in ausgabe
    assert "0 %" in ausgabe


def test_formatiert_bedeckt():
    ausgabe = formatiere_wetter(
        ergebnis(Wetterzustand(sonnenschein=False, regen=False), 0)
    )
    assert "Bedeckt" in ausgabe


def prognose_mit_stunden(*stunden) -> TagesPrognose:
    return TagesPrognose(ort="Berlin", stunden=stunden)


def test_tagesprognose_zeigt_tabelle_mit_stunden():
    prognose = prognose_mit_stunden(
        PrognoseStunde(stunde=14, wahrscheinlichkeit=62, sichtbarkeit=48),
        PrognoseStunde(stunde=15, wahrscheinlichkeit=78, sichtbarkeit=61),
        PrognoseStunde(stunde=16, wahrscheinlichkeit=31, sichtbarkeit=20),
    )
    ausgabe = formatiere_tagesprognose(prognose)
    assert "14:00" in ausgabe
    assert "15:00" in ausgabe
    assert "62" in ausgabe
    assert "78" in ausgabe


def test_tagesprognose_markiert_spitze():
    prognose = prognose_mit_stunden(
        PrognoseStunde(stunde=14, wahrscheinlichkeit=30, sichtbarkeit=20),
        PrognoseStunde(stunde=15, wahrscheinlichkeit=78, sichtbarkeit=61),
    )
    ausgabe = formatiere_tagesprognose(prognose)
    assert "← Spitze" in ausgabe
    zeilen = ausgabe.splitlines()
    spitzen_zeile = [z for z in zeilen if "← Spitze" in z]
    assert len(spitzen_zeile) == 1
    assert "15:00" in spitzen_zeile[0]


def test_tagesprognose_keine_chance_gibt_eigene_meldung():
    prognose = prognose_mit_stunden(
        PrognoseStunde(stunde=13, wahrscheinlichkeit=0, sichtbarkeit=0),
        PrognoseStunde(stunde=14, wahrscheinlichkeit=0, sichtbarkeit=0),
    )
    ausgabe = formatiere_tagesprognose(prognose)
    assert "kein Regenbogen" in ausgabe
    assert "13:00" not in ausgabe


def test_tagesprognose_leere_stunden_gibt_eigene_meldung():
    prognose = TagesPrognose(ort="Berlin", stunden=())
    ausgabe = formatiere_tagesprognose(prognose)
    assert "kein Regenbogen" in ausgabe


def test_formatiere_wetter_zeigt_blickrichtung():
    e = WetterErgebnis(
        ort="Berlin",
        postleitzahl=None,
        zustand=Wetterzustand(
            sonnenschein=True,
            regen=True,
            sonnenschein_intensitaet=0.7,
            regen_intensitaet=0.4,
        ),
        sonnenstand=Sonnenstand(sonnenhoehe_grad=20.0, sonnenazimut_grad=250.0),
        wahrscheinlichkeit=60,
        sichtbarkeit=50,
        blickrichtung="Nordost",
    )
    ausgabe = formatiere_wetter(e)
    assert "Blickrichtung: Nordost" in ausgabe


def test_formatiere_wetter_keine_blickrichtung_bei_null():
    e = WetterErgebnis(
        ort="Berlin",
        postleitzahl=None,
        zustand=Wetterzustand(sonnenschein=False, regen=False),
        sonnenstand=Sonnenstand(sonnenhoehe_grad=20.0, sonnenazimut_grad=250.0),
        wahrscheinlichkeit=0,
        sichtbarkeit=0,
        blickrichtung=None,
    )
    ausgabe = formatiere_wetter(e)
    assert "Blickrichtung" not in ausgabe


def test_tagesprognose_zeigt_blickrichtung_footer():
    prognose = TagesPrognose(
        ort="Berlin",
        stunden=(
            PrognoseStunde(stunde=14, wahrscheinlichkeit=30, sichtbarkeit=20),
            PrognoseStunde(stunde=15, wahrscheinlichkeit=78, sichtbarkeit=61),
        ),
        blickrichtung="Südost",
    )
    ausgabe = formatiere_tagesprognose(prognose)
    assert "schau nach Südost" in ausgabe
    assert "15:00" in ausgabe
