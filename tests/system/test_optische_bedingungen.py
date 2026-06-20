from regenbogen.system.core.optische_bedingungen import (
    leite_optische_bedingungen_ab,
)
from regenbogen.system.ports.wetterapi_port import WetterApiMessung


def messung(**overrides):
    werte = dict(
        sonnenschein_sekunden=1800.0,
        niederschlag_mm=2.0,
        rain_mm=2.0,
        showers_mm=0.0,
        snowfall_cm=0.0,
        weather_code=61,
        cloud_cover=60.0,
        visibility_m=10_000.0,
        direct_radiation=400.0,
        temperature_2m=12.0,
    )
    werte.update(overrides)
    return WetterApiMessung(**werte)


def test_regen_liefert_gute_tropfenqualitaet():
    optik = leite_optische_bedingungen_ab(messung(weather_code=61, rain_mm=2.0))
    assert optik.tropfen_qualitaet > 0.5


def test_schnee_wird_fuer_normalen_regenbogen_abgewertet():
    optik = leite_optische_bedingungen_ab(
        messung(weather_code=71, snowfall_cm=1.0, rain_mm=0.0)
    )
    assert optik.niederschlags_phasen_faktor == 0.0


def test_fehlende_sichtweite_ist_konservativ_aber_nicht_null():
    optik = leite_optische_bedingungen_ab(messung(visibility_m=None))
    assert 0.0 < optik.sicht_faktor < 1.0
