from regenbogen.domain.regenbogen_geometrie import (
    Sonnenstand,
    azimut_zu_himmelsrichtung,
    berechne_regenbogen_azimut,
    berechne_sonnenstands_faktor,
    berechne_sonnenstands_faktor_sekundaerbogen,
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


def test_regenbogen_azimut_sonne_im_osten():
    assert berechne_regenbogen_azimut(Sonnenstand(20.0, 90.0)) == 270.0


def test_regenbogen_azimut_sonne_im_sueden():
    assert berechne_regenbogen_azimut(Sonnenstand(20.0, 180.0)) == 0.0


def test_regenbogen_azimut_sonne_im_westen():
    assert berechne_regenbogen_azimut(Sonnenstand(20.0, 270.0)) == 90.0


def test_azimut_zu_himmelsrichtung_kardinalrichtungen():
    assert azimut_zu_himmelsrichtung(0.0) == "Nord"
    assert azimut_zu_himmelsrichtung(90.0) == "Ost"
    assert azimut_zu_himmelsrichtung(180.0) == "Süd"
    assert azimut_zu_himmelsrichtung(270.0) == "West"


def test_azimut_zu_himmelsrichtung_zwischenrichtungen():
    assert azimut_zu_himmelsrichtung(45.0) == "Nordost"
    assert azimut_zu_himmelsrichtung(135.0) == "Südost"
    assert azimut_zu_himmelsrichtung(225.0) == "Südwest"
    assert azimut_zu_himmelsrichtung(315.0) == "Nordwest"


def test_azimut_zu_himmelsrichtung_16_punkt():
    assert azimut_zu_himmelsrichtung(22.5) == "NNO"
    assert azimut_zu_himmelsrichtung(67.5) == "ONO"
    assert azimut_zu_himmelsrichtung(337.5) == "NNW"


def test_azimut_zu_himmelsrichtung_360_entspricht_nord():
    assert azimut_zu_himmelsrichtung(360.0) == "Nord"


# --- Sekundaerbogen-Geometrie ---


def test_sekundaerbogen_sonne_unter_horizont_ergibt_null():
    assert berechne_sonnenstands_faktor_sekundaerbogen(Sonnenstand(-5.0, 180.0)) == 0.0


def test_sekundaerbogen_niedrige_sonne_ist_voll():
    assert berechne_sonnenstands_faktor_sekundaerbogen(Sonnenstand(10.0, 180.0)) == 1.0


def test_sekundaerbogen_sonne_ueber_51_grad_ergibt_null():
    assert berechne_sonnenstands_faktor_sekundaerbogen(Sonnenstand(52.0, 180.0)) == 0.0


def test_sekundaerbogen_genau_51_grad_ergibt_null():
    assert berechne_sonnenstands_faktor_sekundaerbogen(Sonnenstand(51.0, 180.0)) == 0.0


def test_sekundaerbogen_uebergangsbereich_faellt_linear():
    faktor = berechne_sonnenstands_faktor_sekundaerbogen(Sonnenstand(38.0, 180.0))
    assert 0.0 < faktor < 1.0


def test_sekundaerbogen_zwischen_42_und_51_ist_positiv():
    """Zwischen 42 und 51 Grad: Sekundaerbogen moeglich, Primaerbogen nicht."""
    faktor_primaer = berechne_sonnenstands_faktor(Sonnenstand(46.0, 180.0))
    faktor_sekundaer = berechne_sonnenstands_faktor_sekundaerbogen(
        Sonnenstand(46.0, 180.0)
    )
    assert faktor_primaer == 0.0
    assert faktor_sekundaer > 0.0


def test_sekundaerbogen_faktor_groesser_als_primaer_im_ueberlappbereich():
    """Unter 42 Grad fallen beide positiv aus; Sekundaerbogen faellt langsamer ab
    (Cutoff 51 statt 42 Grad) und hat daher einen groesseren geometrischen Faktor.
    Die niedrigere Gesamtwahrscheinlichkeit entsteht erst durch SekundaerbogenDaempfung."""
    hoehe = 30.0
    faktor_p = berechne_sonnenstands_faktor(Sonnenstand(hoehe, 180.0))
    faktor_s = berechne_sonnenstands_faktor_sekundaerbogen(Sonnenstand(hoehe, 180.0))
    assert faktor_s > faktor_p
