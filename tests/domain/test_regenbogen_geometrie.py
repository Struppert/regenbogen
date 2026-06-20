from regenbogen.domain.regenbogen_geometrie import (
    Sonnenstand,
    berechne_sonnenstands_faktor,
)


def test_sonne_unter_horizont_ergibt_null():
    assert berechne_sonnenstands_faktor(Sonnenstand(-2.0, 180.0)) == 0.0


def test_niedrige_sonne_ist_guenstig():
    assert berechne_sonnenstands_faktor(Sonnenstand(10.0, 180.0)) == 1.0


def test_hohe_sonne_ergibt_null():
    assert berechne_sonnenstands_faktor(Sonnenstand(45.0, 180.0)) == 0.0


def test_uebergangsbereich_faellt_linear():
    faktor = berechne_sonnenstands_faktor(Sonnenstand(33.5, 180.0))
    assert 0.0 < faktor < 1.0
