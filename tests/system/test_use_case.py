from datetime import datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)
from regenbogen.system.ports.standort_port import StandortKoordinaten
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


class FakeStandort:
    def finde_koordinaten(self, ort: str, postleitzahl: str | None):
        return StandortKoordinaten(52.532, 13.384, "Europe/Berlin")


def make_uc(api):
    return RegenbogenWahrscheinlichkeitUseCase(
        api=api,
        standort=FakeStandort(),
        sleep=lambda _: None,
        clock=lambda: datetime(2026, 6, 13, 19, 0, tzinfo=ZoneInfo("Europe/Berlin")),
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


def test_gibt_wahrscheinlichkeit_zurueck():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.return_value = gute_messung()
    uc = make_uc(api)
    assert uc.berechne("Berlin") > 0


def test_retry_bei_api_nicht_erreichbar():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.side_effect = [
        WetterApiNichtErreichbar("timeout"),
        WetterApiNichtErreichbar("timeout"),
        gute_messung(),
    ]
    uc = make_uc(api)
    assert uc.berechne("Berlin") > 0
    assert api.hole_aktuelle_messung.call_count == 3


def test_kein_retry_bei_ort_nicht_gefunden():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.side_effect = OrtNichtGefunden("Atlantis")
    uc = make_uc(api)
    with pytest.raises(OrtNichtGefunden):
        uc.berechne("Atlantis")
    assert api.hole_aktuelle_messung.call_count == 1


def test_fehler_nach_max_versuchen():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.side_effect = WetterApiNichtErreichbar("down")
    uc = make_uc(api)
    with pytest.raises(WetterApiNichtErreichbar):
        uc.berechne("Berlin")
    assert api.hole_aktuelle_messung.call_count == 3


def test_berechne_vollstaendig_gibt_zustand_und_wahrscheinlichkeit():
    api = MagicMock(spec=WetterApiPort)
    api.hole_aktuelle_messung.return_value = gute_messung()
    uc = make_uc(api)
    ergebnis = uc.berechne_vollstaendig("Berlin", "10115")
    assert ergebnis.ort == "Berlin"
    assert ergebnis.postleitzahl == "10115"
    assert ergebnis.zustand.sonnenschein is True
    assert ergebnis.wahrscheinlichkeit > 0
    assert ergebnis.sichtbarkeit > 0
