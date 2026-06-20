from dataclasses import dataclass


@dataclass(frozen=True)
class Sonnenstand:
    """Sonnenposition relativ zum Beobachter."""

    sonnenhoehe_grad: float
    sonnenazimut_grad: float


def berechne_sonnenstands_faktor(sonnenstand: Sonnenstand) -> float:
    """Geometrischer Faktor fuer den primaeren Regenbogen."""
    hoehe = sonnenstand.sonnenhoehe_grad

    if hoehe <= 0.0:
        return 0.0
    if hoehe >= 42.0:
        return 0.0
    if hoehe <= 25.0:
        return 1.0

    return max(0.0, (42.0 - hoehe) / (42.0 - 25.0))
