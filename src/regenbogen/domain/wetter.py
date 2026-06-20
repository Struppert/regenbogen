from dataclasses import dataclass


@dataclass(frozen=True)
class Wetterzustand:
    """Beobachtete Wetterphaenomene an einem Ort zu einem Zeitpunkt."""

    sonnenschein: bool
    regen: bool
    sonnenschein_intensitaet: float = 0.0
    regen_intensitaet: float = 0.0

    def __post_init__(self) -> None:
        if not (0.0 <= self.sonnenschein_intensitaet <= 1.0):
            raise ValueError("sonnenschein_intensitaet muss in [0.0, 1.0] liegen")
        if not (0.0 <= self.regen_intensitaet <= 1.0):
            raise ValueError("regen_intensitaet muss in [0.0, 1.0] liegen")
        if self.sonnenschein and self.sonnenschein_intensitaet == 0.0:
            raise ValueError("sonnenschein=True erfordert Intensitaet > 0.0")
        if self.regen and self.regen_intensitaet == 0.0:
            raise ValueError("regen=True erfordert Intensitaet > 0.0")
