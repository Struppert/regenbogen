from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class StandortKoordinaten:
    """Beobachtungsort fuer Sonnenstandsberechnung und Wetterabfrage."""

    latitude: float
    longitude: float
    zeitzone: str


class PostleitzahlUnbekannt(Exception):
    """PLZ kann nicht in Koordinaten uebersetzt werden. Terminal."""


class StandortPort(ABC):
    @abstractmethod
    def finde_koordinaten(
        self,
        ort: str,
        postleitzahl: str | None,
    ) -> StandortKoordinaten:
        raise NotImplementedError
