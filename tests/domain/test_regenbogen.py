from regenbogen.domain.regenbogen import berechne_regenbogen_wahrscheinlichkeit
from regenbogen.domain.regenbogen_geometrie import Sonnenstand
from regenbogen.domain.wetter import Wetterzustand


def test_kein_sonnenschein_ergibt_null():
    zustand = Wetterzustand(sonnenschein=False, regen=True, regen_intensitaet=0.8)
    assert berechne_regenbogen_wahrscheinlichkeit(zustand) == 0


def test_kein_regen_ergibt_null():
    zustand = Wetterzustand(
        sonnenschein=True, regen=False, sonnenschein_intensitaet=0.9
    )
    assert berechne_regenbogen_wahrscheinlichkeit(zustand) == 0


def test_beide_faktoren_ergeben_groesser_null():
    zustand = Wetterzustand(
        sonnenschein=True,
        regen=True,
        sonnenschein_intensitaet=0.5,
        regen_intensitaet=0.5,
    )
    assert berechne_regenbogen_wahrscheinlichkeit(zustand) > 0


def test_unguenstiger_sonnenstand_kann_null_ergeben():
    zustand = Wetterzustand(
        sonnenschein=True,
        regen=True,
        sonnenschein_intensitaet=1.0,
        regen_intensitaet=1.0,
    )
    ergebnis = berechne_regenbogen_wahrscheinlichkeit(
        zustand,
        Sonnenstand(45.0, 180.0),
    )
    assert ergebnis == 0
