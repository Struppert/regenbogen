from dataclasses import dataclass


@dataclass(frozen=True)
class PrognoseStunde:
    stunde: int
    wahrscheinlichkeit: int
    sichtbarkeit: int
    sekundaerbogen_wahrscheinlichkeit: int = 0


@dataclass(frozen=True)
class TagesPrognose:
    ort: str
    stunden: tuple[PrognoseStunde, ...]
    blickrichtung: str | None = None

    @property
    def spitzenstunde(self) -> PrognoseStunde | None:
        if not self.stunden:
            return None
        return max(self.stunden, key=lambda s: s.wahrscheinlichkeit)

    @property
    def hat_regenbogen_chance(self) -> bool:
        return any(s.wahrscheinlichkeit > 0 for s in self.stunden)

    @property
    def hat_sekundaerbogen_chance(self) -> bool:
        return any(s.sekundaerbogen_wahrscheinlichkeit > 0 for s in self.stunden)
