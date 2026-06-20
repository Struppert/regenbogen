from regenbogen.domain.regenbogen_optik import (
    RegenbogenOptikFaktoren,
    berechne_regenbogen_sichtbarkeit,
)


def _faktoren(**overrides):
    werte = dict(
        sonnenstands_faktor=1.0,
        regen_faktor=1.0,
        direktlicht_faktor=1.0,
        tropfen_qualitaet=1.0,
        sicht_faktor=1.0,
        hintergrund_kontrast_faktor=1.0,
        niederschlags_phasen_faktor=1.0,
    )
    werte.update(overrides)
    return RegenbogenOptikFaktoren(**werte)


def test_kein_direktlicht_ergibt_null():
    assert berechne_regenbogen_sichtbarkeit(_faktoren(direktlicht_faktor=0.0)) == 0


def test_schneephase_ergibt_null():
    assert (
        berechne_regenbogen_sichtbarkeit(_faktoren(niederschlags_phasen_faktor=0.0))
        == 0
    )


def test_alle_faktoren_guenstig_ergeben_hohen_score():
    assert berechne_regenbogen_sichtbarkeit(_faktoren()) == 100
