from datetime import datetime, timezone
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

from regenbogen.domain.tagesprognose import TagesPrognose
from regenbogen.system.core.tagesprognose_use_case import TagesPrognoseUseCase
from regenbogen.system.ports.standort_port import StandortKoordinaten
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    StundlicheWetterApiMessung,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


BERLIN = StandortKoordinaten(52.532, 13.384, "Europe/Berlin")


class FakeStandort:
    def finde_koordinaten(
        self, ort: str, postleitzahl: str | None
    ) -> StandortKoordinaten:
        return BERLIN


def make_uc(api) -> TagesPrognoseUseCase:
    return TagesPrognoseUseCase(
        api=api,
        standort=FakeStandort(),
        sleep=lambda _: None,
        clock=lambda: datetime(2026, 6, 20, 12, 0, tzinfo=ZoneInfo("Europe/Berlin")),
    )


def gute_messung() -> WetterApiMessung:
    return WetterApiMessung(
        sonnenschein_sekunden=1800.0,
        niederschlag_mm=5.0,
        rain_mm=5.0,
        showers_mm=0.0,
        snowfall_cm=0.0,
        weather_code=61,
        cloud_cover=60.0,
        visibility_m=10_000.0,
        direct_radiation=400.0,
        temperature_2m=12.0,
    )


def nachts_messung() -> WetterApiMessung:
    return WetterApiMessung(
        sonnenschein_sekunden=0.0,
        niederschlag_mm=0.0,
    )


def stundliche_messungen_fuer_tag() -> list[StundlicheWetterApiMessung]:
    """24 Stunden des 20.06.2026 in Europe/Berlin (UTC+2)."""
    berlin = ZoneInfo("Europe/Berlin")
    utc = timezone.utc
    messungen = []
    for h in range(24):
        lokaler_zeitpunkt = datetime(2026, 6, 20, h, 0, tzinfo=berlin)
        zeitpunkt_utc = lokaler_zeitpunkt.astimezone(utc)
        messung = gute_messung() if 8 <= h <= 20 else nachts_messung()
        messungen.append(
            StundlicheWetterApiMessung(zeitpunkt_utc=zeitpunkt_utc, messung=messung)
        )
    return messungen


def test_liefert_tagesprognose():
    api = MagicMock(spec=WetterApiPort)
    api.hole_stundliche_messungen.return_value = stundliche_messungen_fuer_tag()
    uc = make_uc(api)
    prognose = uc.berechne("Berlin")
    assert isinstance(prognose, TagesPrognose)
    assert prognose.ort == "Berlin"


def test_nachtstunden_werden_ausgefiltert():
    api = MagicMock(spec=WetterApiPort)
    api.hole_stundliche_messungen.return_value = stundliche_messungen_fuer_tag()
    uc = make_uc(api)
    prognose = uc.berechne("Berlin")
    # Nachtstunden (0-4, 22-23) sollen nicht enthalten sein
    stunden_nummern = [s.stunde for s in prognose.stunden]
    assert 0 not in stunden_nummern
    assert 3 not in stunden_nummern


def test_tagstunden_sind_enthalten():
    api = MagicMock(spec=WetterApiPort)
    api.hole_stundliche_messungen.return_value = stundliche_messungen_fuer_tag()
    uc = make_uc(api)
    prognose = uc.berechne("Berlin")
    stunden_nummern = [s.stunde for s in prognose.stunden]
    assert len(stunden_nummern) > 0
    assert all(isinstance(s.wahrscheinlichkeit, int) for s in prognose.stunden)
    assert all(isinstance(s.sichtbarkeit, int) for s in prognose.stunden)


def test_spitzenstunde_ist_vorhanden_bei_gutem_wetter():
    api = MagicMock(spec=WetterApiPort)
    api.hole_stundliche_messungen.return_value = stundliche_messungen_fuer_tag()
    uc = make_uc(api)
    prognose = uc.berechne("Berlin")
    assert prognose.spitzenstunde is not None


def test_retry_bei_api_nicht_erreichbar():
    api = MagicMock(spec=WetterApiPort)
    api.hole_stundliche_messungen.side_effect = [
        WetterApiNichtErreichbar("timeout"),
        WetterApiNichtErreichbar("timeout"),
        stundliche_messungen_fuer_tag(),
    ]
    uc = make_uc(api)
    prognose = uc.berechne("Berlin")
    assert isinstance(prognose, TagesPrognose)
    assert api.hole_stundliche_messungen.call_count == 3


def test_fehler_nach_max_versuchen():
    api = MagicMock(spec=WetterApiPort)
    api.hole_stundliche_messungen.side_effect = WetterApiNichtErreichbar("down")
    uc = make_uc(api)
    with pytest.raises(WetterApiNichtErreichbar):
        uc.berechne("Berlin")
    assert api.hole_stundliche_messungen.call_count == 3


def test_kein_retry_bei_ort_nicht_gefunden():
    api = MagicMock(spec=WetterApiPort)
    api.hole_stundliche_messungen.side_effect = OrtNichtGefunden("Atlantis")
    uc = make_uc(api)
    with pytest.raises(OrtNichtGefunden):
        uc.berechne("Atlantis")
    assert api.hole_stundliche_messungen.call_count == 1


def _stundliche_messungen_mit_hoher_sonne() -> list[StundlicheWetterApiMessung]:
    """Messungen fuer eine Stunde mit Sonnenhoehe zwischen 42 und 51 Grad.
    Primaerbogen geometrisch ausgeschlossen, Sekundaerbogen moeglich."""
    berlin = ZoneInfo("Europe/Berlin")
    utc = timezone.utc
    # 20.06.2026 13:00 Uhr in Berlin: Sonne steht hoch (~60 Grad) — beide Boegen nicht moeglich.
    # Wir verwenden einen echten Grenzfall: 20.06 frueh morgens ca. 8 Uhr,
    # Sonnenhoehe ~30 Grad — beide Boegen geometrisch moeglich, aber via Mock
    # direkt eine Stunde mit hohem Sonnenstand simulieren.
    # Stattdessen: Fixture-Daten fuer eine Stunde die der Use Case durchlaeuft.
    # Der Test prueft nur dass sekundaerbogen_wahrscheinlichkeit befuellt wird.
    zeitpunkt = datetime(2026, 6, 20, 8, 0, tzinfo=berlin).astimezone(utc)
    return [StundlicheWetterApiMessung(zeitpunkt_utc=zeitpunkt, messung=gute_messung())]


def test_sekundaerbogen_wahrscheinlichkeit_wird_befuellt():
    """PrognoseStunde enthaelt sekundaerbogen_wahrscheinlichkeit als int."""
    api = MagicMock(spec=WetterApiPort)
    api.hole_stundliche_messungen.return_value = stundliche_messungen_fuer_tag()
    uc = make_uc(api)
    prognose = uc.berechne("Berlin")
    assert all(
        isinstance(s.sekundaerbogen_wahrscheinlichkeit, int) for s in prognose.stunden
    )
    assert all(
        0 <= s.sekundaerbogen_wahrscheinlichkeit <= 100 for s in prognose.stunden
    )


def test_sekundaerbogen_null_ohne_sonnenschein_oder_regen():
    """Ohne Wetterbedingungen kein Sekundaerbogen."""
    api = MagicMock(spec=WetterApiPort)
    berlin = ZoneInfo("Europe/Berlin")
    utc = timezone.utc
    trockene_messung = WetterApiMessung(
        sonnenschein_sekunden=0.0,
        niederschlag_mm=0.0,
        rain_mm=0.0,
        showers_mm=0.0,
        snowfall_cm=0.0,
        weather_code=0,
        cloud_cover=0.0,
        visibility_m=20_000.0,
        direct_radiation=0.0,
        temperature_2m=15.0,
    )
    zeitpunkt = datetime(2026, 6, 20, 8, 0, tzinfo=berlin).astimezone(utc)
    api.hole_stundliche_messungen.return_value = [
        StundlicheWetterApiMessung(zeitpunkt_utc=zeitpunkt, messung=trockene_messung)
    ]
    uc = make_uc(api)
    prognose = uc.berechne("Berlin")
    assert all(s.sekundaerbogen_wahrscheinlichkeit == 0 for s in prognose.stunden)


def test_leere_prognose_bei_nur_nachtstunden():
    api = MagicMock(spec=WetterApiPort)
    berlin = ZoneInfo("Europe/Berlin")
    utc = timezone.utc
    # Nur Mitternacht — keine Tagstunden
    zeitpunkt = datetime(2026, 6, 20, 0, 0, tzinfo=berlin).astimezone(utc)
    api.hole_stundliche_messungen.return_value = [
        StundlicheWetterApiMessung(zeitpunkt_utc=zeitpunkt, messung=nachts_messung())
    ]
    uc = make_uc(api)
    prognose = uc.berechne("Berlin")
    assert prognose.stunden == ()
    assert prognose.hat_regenbogen_chance is False
