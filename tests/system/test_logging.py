from datetime import datetime
from zoneinfo import ZoneInfo

from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)
from regenbogen.system.ports.logging_port import EventLogger, LogEvent
from regenbogen.system.ports.standort_port import StandortKoordinaten, StandortPort
from regenbogen.system.ports.wetterapi_port import WetterApiMessung, WetterApiPort


class RecordingLogger(EventLogger):
    def __init__(self) -> None:
        self.events: list[LogEvent] = []

    def log(self, event: LogEvent) -> None:
        self.events.append(event)


class FakeStandort(StandortPort):
    def finde_koordinaten(
        self, ort: str, postleitzahl: str | None = None
    ) -> StandortKoordinaten:
        return StandortKoordinaten(
            latitude=52.52,
            longitude=13.41,
            zeitzone="Europe/Berlin",
        )


class FakeWetterApi(WetterApiPort):
    def hole_aktuelle_messung(self, koordinaten: StandortKoordinaten) -> WetterApiMessung:
        return WetterApiMessung(
            sonnenschein_sekunden=1800.0,
            niederschlag_mm=2.0,
            rain_mm=2.0,
            showers_mm=0.0,
            snowfall_cm=0.0,
            weather_code=61,
            cloud_cover=60.0,
            visibility_m=10000.0,
            direct_radiation=300.0,
            temperature_2m=12.0,
        )


def test_use_case_schreibt_systemische_log_events():
    logger = RecordingLogger()
    uc = RegenbogenWahrscheinlichkeitUseCase(
        api=FakeWetterApi(),
        standort=FakeStandort(),
        sleep=lambda _: None,
        clock=lambda: datetime(2026, 6, 14, 18, 0, tzinfo=ZoneInfo("Europe/Berlin")),
        logger=logger,
    )

    uc.berechne_vollstaendig("Berlin", "10115")

    namen = [event.name for event in logger.events]
    assert "regenbogen.berechnung.gestartet" in namen
    assert "regenbogen.berechnung.abgeschlossen" in namen
