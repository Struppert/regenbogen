from dataclasses import dataclass


@dataclass(frozen=True)
class Sonnenstand:
    """Sonnenposition relativ zum Beobachter."""

    sonnenhoehe_grad: float
    sonnenazimut_grad: float


_HIMMELSRICHTUNGEN_16 = [
    "Nord",
    "NNO",
    "Nordost",
    "ONO",
    "Ost",
    "OSO",
    "Südost",
    "SSO",
    "Süd",
    "SSW",
    "Südwest",
    "WSW",
    "West",
    "WNW",
    "Nordwest",
    "NNW",
]


def berechne_regenbogen_azimut(sonnenstand: Sonnenstand) -> float:
    return (sonnenstand.sonnenazimut_grad + 180.0) % 360.0


def azimut_zu_himmelsrichtung(azimut_grad: float) -> str:
    index = round(azimut_grad / 22.5) % 16
    return _HIMMELSRICHTUNGEN_16[index]


SEKUNDAERBOGEN_DAEMPFUNG: float = 0.57


def berechne_sonnenstands_faktor(sonnenstand: Sonnenstand) -> float:
    """Geometrischer Faktor fuer den primaeren Regenbogen (Cutoff 42 Grad)."""
    hoehe = sonnenstand.sonnenhoehe_grad

    if hoehe <= 0.0:
        return 0.0
    if hoehe >= 42.0:
        return 0.0
    if hoehe <= 25.0:
        return 1.0

    return max(0.0, (42.0 - hoehe) / (42.0 - 25.0))


def berechne_sonnenstands_faktor_sekundaerbogen(sonnenstand: Sonnenstand) -> float:
    """Geometrischer Faktor fuer den Sekundaerbogen (Cutoff 51 Grad)."""
    hoehe = sonnenstand.sonnenhoehe_grad

    if hoehe <= 0.0:
        return 0.0
    if hoehe >= 51.0:
        return 0.0
    if hoehe <= 25.0:
        return 1.0

    return max(0.0, (51.0 - hoehe) / (51.0 - 25.0))
