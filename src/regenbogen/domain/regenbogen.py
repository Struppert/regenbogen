from regenbogen.domain.regenbogen_geometrie import (
    Sonnenstand,
    berechne_sonnenstands_faktor,
)
from regenbogen.domain.wetter import Wetterzustand


def berechne_regenbogen_wahrscheinlichkeit(
    zustand: Wetterzustand,
    sonnenstand: Sonnenstand | None = None,
) -> int:
    """Regenbogen-Wahrscheinlichkeit als Prozentwert in [0, 100]."""
    if not zustand.sonnenschein or not zustand.regen:
        return 0

    basis = (
        zustand.sonnenschein_intensitaet * 0.6
        + zustand.regen_intensitaet * 0.4
    )

    if sonnenstand is not None:
        basis *= berechne_sonnenstands_faktor(sonnenstand)

    return max(0, min(100, round(basis * 100)))
