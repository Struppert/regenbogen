import pytest

from regenbogen.domain.tagesprognose import PrognoseStunde, TagesPrognose


def stunde(h: int, w: int, s: int = 0) -> PrognoseStunde:
    return PrognoseStunde(stunde=h, wahrscheinlichkeit=w, sichtbarkeit=s)


def test_prognosestunde_felder():
    ps = stunde(14, 62, 48)
    assert ps.stunde == 14
    assert ps.wahrscheinlichkeit == 62
    assert ps.sichtbarkeit == 48


def test_spitzenstunde_bei_mehreren_stunden():
    prognose = TagesPrognose(
        ort="Berlin",
        stunden=(stunde(13, 30), stunde(15, 78), stunde(16, 45)),
    )
    assert prognose.spitzenstunde == stunde(15, 78)


def test_spitzenstunde_bei_einer_stunde():
    prognose = TagesPrognose(ort="Berlin", stunden=(stunde(14, 50),))
    assert prognose.spitzenstunde == stunde(14, 50)


def test_spitzenstunde_bei_leerer_folge():
    prognose = TagesPrognose(ort="Berlin", stunden=())
    assert prognose.spitzenstunde is None


def test_hat_regenbogen_chance_true():
    prognose = TagesPrognose(
        ort="Berlin",
        stunden=(stunde(13, 0), stunde(14, 1)),
    )
    assert prognose.hat_regenbogen_chance is True


def test_hat_regenbogen_chance_false_bei_allen_nullen():
    prognose = TagesPrognose(
        ort="Berlin",
        stunden=(stunde(13, 0), stunde(14, 0)),
    )
    assert prognose.hat_regenbogen_chance is False


def test_hat_regenbogen_chance_false_bei_leerer_folge():
    prognose = TagesPrognose(ort="Berlin", stunden=())
    assert prognose.hat_regenbogen_chance is False


def test_tagesprognose_ist_frozen():
    prognose = TagesPrognose(ort="Berlin", stunden=(stunde(14, 50),))
    with pytest.raises(Exception):
        prognose.ort = "München"  # type: ignore[misc]
