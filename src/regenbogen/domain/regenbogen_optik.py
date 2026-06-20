from dataclasses import dataclass


@dataclass(frozen=True)
class RegenbogenOptikFaktoren:
    sonnenstands_faktor: float
    regen_faktor: float
    direktlicht_faktor: float
    tropfen_qualitaet: float
    sicht_faktor: float
    hintergrund_kontrast_faktor: float
    niederschlags_phasen_faktor: float


def berechne_regenbogen_sichtbarkeit(faktoren: RegenbogenOptikFaktoren) -> int:
    """Berechnet einen Sichtbarkeits-Score in [0, 100]."""
    if faktoren.sonnenstands_faktor <= 0.0:
        return 0
    if faktoren.regen_faktor <= 0.0:
        return 0
    if faktoren.direktlicht_faktor <= 0.0:
        return 0
    if faktoren.niederschlags_phasen_faktor <= 0.0:
        return 0

    score = (
        faktoren.sonnenstands_faktor
        * faktoren.regen_faktor
        * faktoren.direktlicht_faktor
        * faktoren.tropfen_qualitaet
        * faktoren.sicht_faktor
        * faktoren.hintergrund_kontrast_faktor
        * faktoren.niederschlags_phasen_faktor
    )
    return round(max(0.0, min(1.0, score)) * 100)
