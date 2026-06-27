from collections.abc import Callable
from datetime import date, datetime
from zoneinfo import ZoneInfo

from regenbogen.domain.regenbogen import berechne_regenbogen_wahrscheinlichkeit
from regenbogen.domain.regenbogen_geometrie import (
    SEKUNDAERBOGEN_DAEMPFUNG,
    azimut_zu_himmelsrichtung,
    berechne_regenbogen_azimut,
    berechne_sonnenstands_faktor,
    berechne_sonnenstands_faktor_sekundaerbogen,
)
from regenbogen.domain.regenbogen_optik import (
    RegenbogenOptikFaktoren,
    berechne_regenbogen_sichtbarkeit,
)
from regenbogen.domain.tagesprognose import PrognoseStunde, TagesPrognose
from regenbogen.domain.wetter import Wetterzustand
from regenbogen.system.core.optische_bedingungen import leite_optische_bedingungen_ab
from regenbogen.system.core.sonnenstand import berechne_sonnenstand
from regenbogen.system.ports.standort_port import StandortKoordinaten, StandortPort
from regenbogen.system.ports.wetterapi_port import (
    OrtNichtGefunden,
    StundlicheWetterApiMessung,
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


class TagesPrognoseUseCase:
    MAX_VERSUCHE = 3

    def __init__(
        self,
        api: WetterApiPort,
        standort: StandortPort,
        sleep: Callable[[float], None],
        clock: Callable[[], datetime],
    ) -> None:
        self._api = api
        self._standort = standort
        self._sleep = sleep
        self._clock = clock

    def berechne(self, ort: str, postleitzahl: str | None = None) -> TagesPrognose:
        koordinaten = self._standort.finde_koordinaten(ort, postleitzahl)
        jetzt = self._clock()
        lokales_datum = jetzt.astimezone(ZoneInfo(koordinaten.zeitzone)).date()
        stundliche_messungen = self._hole_mit_retry(koordinaten, lokales_datum)

        stunden = []
        bester_sonnenstand = None
        beste_wahrscheinlichkeit = -1
        for sm in stundliche_messungen:
            sonnenstand = berechne_sonnenstand(sm.zeitpunkt_utc, koordinaten)
            if sonnenstand.sonnenhoehe_grad <= 0:
                continue
            zustand = self._messung_zu_wetterzustand(sm.messung)
            w = berechne_regenbogen_wahrscheinlichkeit(zustand, sonnenstand)
            s = self._berechne_sichtbarkeit(sm.messung, sonnenstand)
            w_s = self._berechne_sekundaerbogen_wahrscheinlichkeit(zustand, sonnenstand)
            lokale_stunde = sm.zeitpunkt_utc.astimezone(
                ZoneInfo(koordinaten.zeitzone)
            ).hour
            stunden.append(
                PrognoseStunde(
                    stunde=lokale_stunde,
                    wahrscheinlichkeit=w,
                    sichtbarkeit=s,
                    sekundaerbogen_wahrscheinlichkeit=w_s,
                )
            )
            if w > beste_wahrscheinlichkeit:
                beste_wahrscheinlichkeit = w
                bester_sonnenstand = sonnenstand

        blickrichtung = None
        if bester_sonnenstand is not None and beste_wahrscheinlichkeit > 0:
            blickrichtung = azimut_zu_himmelsrichtung(
                berechne_regenbogen_azimut(bester_sonnenstand)
            )

        return TagesPrognose(
            ort=ort, stunden=tuple(stunden), blickrichtung=blickrichtung
        )

    def _hole_mit_retry(
        self,
        koordinaten: StandortKoordinaten,
        datum: date,
    ) -> list[StundlicheWetterApiMessung]:
        letzter_fehler: WetterApiNichtErreichbar | None = None
        for versuch in range(1, self.MAX_VERSUCHE + 1):
            try:
                return self._api.hole_stundliche_messungen(koordinaten, datum)
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

    def _berechne_sekundaerbogen_wahrscheinlichkeit(
        self,
        zustand: Wetterzustand,
        sonnenstand,
    ) -> int:
        if not zustand.sonnenschein or not zustand.regen:
            return 0
        faktor_s = berechne_sonnenstands_faktor_sekundaerbogen(sonnenstand)
        if faktor_s <= 0.0:
            return 0
        basis = zustand.sonnenschein_intensitaet * 0.6 + zustand.regen_intensitaet * 0.4
        return max(0, min(100, round(basis * faktor_s * SEKUNDAERBOGEN_DAEMPFUNG * 100)))

    def _berechne_sichtbarkeit(
        self,
        messung: WetterApiMessung,
        sonnenstand,
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
