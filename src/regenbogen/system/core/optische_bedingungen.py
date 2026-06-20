from dataclasses import dataclass

from regenbogen.system.ports.wetterapi_port import WetterApiMessung


@dataclass(frozen=True)
class OptischeBedingungen:
    """Aus Wetterdaten abgeleitete Faktoren fuer das Domain-Modell."""

    tropfen_qualitaet: float
    direktlicht_faktor: float
    sicht_faktor: float
    hintergrund_kontrast_faktor: float
    niederschlags_phasen_faktor: float


def leite_optische_bedingungen_ab(messung: WetterApiMessung) -> OptischeBedingungen:
    return OptischeBedingungen(
        tropfen_qualitaet=_tropfen_qualitaet(messung),
        direktlicht_faktor=_direktlicht_faktor(messung.direct_radiation),
        sicht_faktor=_sicht_faktor(messung.visibility_m),
        hintergrund_kontrast_faktor=_hintergrund_kontrast_faktor(messung.cloud_cover),
        niederschlags_phasen_faktor=_niederschlags_phasen_faktor(messung),
    )


def _direktlicht_faktor(direct_radiation: float) -> float:
    return max(0.0, min(1.0, direct_radiation / 400.0))


def _sicht_faktor(visibility_m: float | None) -> float:
    if visibility_m is None:
        return 0.7
    return max(0.0, min(1.0, visibility_m / 10_000.0))


def _hintergrund_kontrast_faktor(cloud_cover: float) -> float:
    if cloud_cover < 20.0:
        return 0.7
    if cloud_cover <= 80.0:
        return 1.0
    return 0.8


def _niederschlags_phasen_faktor(messung: WetterApiMessung) -> float:
    if messung.weather_code in {56, 57, 66, 67, 71, 73, 75, 77}:
        return 0.0
    if messung.snowfall_cm > 0.0:
        return 0.0
    if messung.temperature_2m < -1.0:
        return 0.2
    return 1.0


def _wasser_mm(messung: WetterApiMessung) -> float:
    wasser = messung.rain_mm + messung.showers_mm
    if wasser <= 0.0 and messung.niederschlag_mm > 0.0 and messung.snowfall_cm <= 0.0:
        return messung.niederschlag_mm
    return wasser


def _tropfen_qualitaet(messung: WetterApiMessung) -> float:
    code = messung.weather_code
    wasser_mm = _wasser_mm(messung)

    if wasser_mm <= 0.0:
        return 0.0

    if code in {56, 57, 66, 67, 71, 73, 75, 77}:
        return 0.0
    if code in {51, 53, 55}:
        return min(0.6, 0.2 + wasser_mm / 2.0)
    if code in {61, 63, 65}:
        return min(1.0, 0.4 + wasser_mm / 5.0)
    if code in {80, 81, 82}:
        return min(1.0, 0.5 + wasser_mm / 4.0)

    return min(0.8, wasser_mm / 5.0)
