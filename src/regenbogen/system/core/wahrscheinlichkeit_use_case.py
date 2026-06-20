from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from regenbogen.domain.regenbogen import berechne_regenbogen_wahrscheinlichkeit
from regenbogen.domain.regenbogen_geometrie import (
    Sonnenstand,
    berechne_sonnenstands_faktor,
)
from regenbogen.domain.regenbogen_optik import (
    RegenbogenOptikFaktoren,
    berechne_regenbogen_sichtbarkeit,
)
from regenbogen.domain.wetter import Wetterzustand
from regenbogen.system.core.optische_bedingungen import leite_optische_bedingungen_ab
from regenbogen.system.core.sonnenstand import berechne_sonnenstand
from regenbogen.system.ports.logging_port import (
    EventLogger,
    LogEvent,
    LogLevel,
    NullEventLogger,
)
from regenbogen.system.ports.standort_port import StandortKoordinaten, StandortPort
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


@dataclass(frozen=True)
class WetterErgebnis:
    """Vollstaendiges Ergebnis fuer UI und CLI."""

    ort: str
    postleitzahl: str | None
    zustand: Wetterzustand
    sonnenstand: Sonnenstand
    wahrscheinlichkeit: int
    sichtbarkeit: int


class RegenbogenWahrscheinlichkeitUseCase:
    MAX_VERSUCHE = 3

    def __init__(
        self,
        api: WetterApiPort,
        standort: StandortPort,
        sleep: Callable[[float], None],
        clock: Callable[[], datetime],
        logger: EventLogger | None = None,
    ) -> None:
        self._api = api
        self._standort = standort
        self._sleep = sleep
        self._clock = clock
        self._logger = logger or NullEventLogger()

    def berechne(self, ort: str, postleitzahl: str | None = None) -> int:
        return self.berechne_vollstaendig(ort, postleitzahl).wahrscheinlichkeit

    def berechne_vollstaendig(
        self,
        ort: str,
        postleitzahl: str | None = None,
    ) -> WetterErgebnis:
        self._logger.log(
            LogEvent(
                name="regenbogen.berechnung.gestartet",
                level=LogLevel.INFO,
                message="Regenbogen-Berechnung gestartet",
                fields={"ort": ort, "plz_vorhanden": postleitzahl is not None},
            )
        )

        koordinaten = self._standort.finde_koordinaten(ort, postleitzahl)
        sonnenstand = berechne_sonnenstand(self._clock(), koordinaten)
        messung = self._hole_messung_mit_retry(koordinaten)
        zustand = self._messung_zu_wetterzustand(messung)
        wahrscheinlichkeit = berechne_regenbogen_wahrscheinlichkeit(
            zustand,
            sonnenstand,
        )
        sichtbarkeit = self._berechne_sichtbarkeit(messung, sonnenstand)

        self._logger.log(
            LogEvent(
                name="regenbogen.berechnung.abgeschlossen",
                level=LogLevel.INFO,
                message="Regenbogen-Berechnung abgeschlossen",
                fields={
                    "ort": ort,
                    "wahrscheinlichkeit": wahrscheinlichkeit,
                    "sichtbarkeit": sichtbarkeit,
                    "sonnenhoehe": round(sonnenstand.sonnenhoehe_grad, 2),
                },
            )
        )

        return WetterErgebnis(
            ort=ort,
            postleitzahl=postleitzahl,
            zustand=zustand,
            sonnenstand=sonnenstand,
            wahrscheinlichkeit=wahrscheinlichkeit,
            sichtbarkeit=sichtbarkeit,
        )

    def _hole_messung_mit_retry(
        self,
        koordinaten: StandortKoordinaten,
    ) -> WetterApiMessung:
        letzter_fehler: WetterApiNichtErreichbar | None = None

        for versuch in range(1, self.MAX_VERSUCHE + 1):
            try:
                return self._api.hole_aktuelle_messung(koordinaten)
            except WetterApiNichtErreichbar as exc:
                letzter_fehler = exc
                if versuch < self.MAX_VERSUCHE:
                    self._sleep(1.0)
            except OrtNichtGefunden:
                raise

        assert letzter_fehler is not None
        raise letzter_fehler

    def _messung_zu_wetterzustand(self, messung: WetterApiMessung) -> Wetterzustand:
        sonnenschein_intensitaet = min(messung.sonnenschein_sekunden / 3600.0, 1.0)
        regen_intensitaet = min(messung.niederschlag_mm / 10.0, 1.0)
        return Wetterzustand(
            sonnenschein=sonnenschein_intensitaet > 0.0,
            regen=regen_intensitaet > 0.0,
            sonnenschein_intensitaet=sonnenschein_intensitaet,
            regen_intensitaet=regen_intensitaet,
        )

    def _berechne_sichtbarkeit(
        self,
        messung: WetterApiMessung,
        sonnenstand: Sonnenstand,
    ) -> int:
        optik = leite_optische_bedingungen_ab(messung)
        wasser_mm = messung.rain_mm + messung.showers_mm
        if (
            wasser_mm <= 0.0
            and messung.niederschlag_mm > 0.0
            and messung.snowfall_cm <= 0.0
        ):
            wasser_mm = messung.niederschlag_mm
        regen_faktor = min(wasser_mm, 5.0) / 5.0
        return berechne_regenbogen_sichtbarkeit(
            RegenbogenOptikFaktoren(
                sonnenstands_faktor=berechne_sonnenstands_faktor(sonnenstand),
                regen_faktor=regen_faktor,
                direktlicht_faktor=optik.direktlicht_faktor,
                tropfen_qualitaet=optik.tropfen_qualitaet,
                sicht_faktor=optik.sicht_faktor,
                hintergrund_kontrast_faktor=optik.hintergrund_kontrast_faktor,
                niederschlags_phasen_faktor=optik.niederschlags_phasen_faktor,
            )
        )
