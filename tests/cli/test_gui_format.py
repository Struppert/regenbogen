from regenbogen.cli.gui_format import formatiere_wetter
from regenbogen.domain.regenbogen_geometrie import Sonnenstand
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
