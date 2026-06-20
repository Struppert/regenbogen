from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime

from regenbogen.system.ports.standort_port import StandortKoordinaten


@dataclass(frozen=True)
class WetterApiMessung:
    """Technische Messung der Wetter-API."""

    sonnenschein_sekunden: float
    niederschlag_mm: float
    rain_mm: float = 0.0
    showers_mm: float = 0.0
    snowfall_cm: float = 0.0
    weather_code: int = 0
    cloud_cover: float = 100.0
    visibility_m: float | None = None
    direct_radiation: float = 0.0
    temperature_2m: float = 0.0


@dataclass(frozen=True)
class StundlicheWetterApiMessung:
    """Port-DTO: WetterApiMessung mit UTC-Zeitpunkt fuer stündliche Abfragen."""

    zeitpunkt_utc: datetime
    messung: WetterApiMessung


class WetterApiNichtErreichbar(Exception):
    """API nicht erreichbar. Recoverable."""


class OrtNichtGefunden(Exception):
    """Unbekannter Ort. Terminal."""


class WetterApiPort(ABC):
    @abstractmethod
    def hole_aktuelle_messung(
        self,
        koordinaten: StandortKoordinaten,
    ) -> WetterApiMessung:
        raise NotImplementedError

    @abstractmethod
    def hole_stundliche_messungen(
        self,
        koordinaten: StandortKoordinaten,
        datum: date,
    ) -> list[StundlicheWetterApiMessung]:
        raise NotImplementedError
