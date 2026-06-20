from datetime import datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)
from regenbogen.system.ports.standort_port import StandortKoordinaten
from regenbogen.system.ports.wetterapi_port import WetterApiMessung


class FakeStandort:
    def finde_koordinaten(self, ort: str, postleitzahl: str | None):
        return StandortKoordinaten(52.532, 13.384, "Europe/Berlin")


def test_winkelmodell_nutzt_feste_uhrzeit():
    api = MagicMock()
    api.hole_aktuelle_messung.return_value = WetterApiMessung(
        sonnenschein_sekunden=1800.0,
        niederschlag_mm=5.0,
        rain_mm=5.0,
        weather_code=61,
        cloud_cover=60.0,
        visibility_m=10_000.0,
        direct_radiation=400.0,
        temperature_2m=12.0,
    )
    uc = RegenbogenWahrscheinlichkeitUseCase(
        api=api,
        standort=FakeStandort(),
        sleep=lambda _: None,
        clock=lambda: datetime(2026, 6, 13, 19, 0, tzinfo=ZoneInfo("Europe/Berlin")),
    )

    ergebnis = uc.berechne_vollstaendig("Berlin", "10115")

    assert ergebnis.postleitzahl == "10115"
    assert ergebnis.sonnenstand.sonnenhoehe_grad > 0.0
    assert 0 <= ergebnis.wahrscheinlichkeit <= 100
    assert 0 <= ergebnis.sichtbarkeit <= 100
