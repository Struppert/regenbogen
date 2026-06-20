import httpx

from regenbogen.system.ports.standort_port import (
    PostleitzahlUnbekannt,
    StandortKoordinaten,
    StandortPort,
)


class PlzStandortLookup(StandortPort):
    """Standortaufloesung fuer deutsche PLZ mit lokalem Fallback."""

    BASE_URL = "https://api.zippopotam.us/de/{plz}"

    _PLZ = {
        "10115": StandortKoordinaten(52.532, 13.384, "Europe/Berlin"),
        "80331": StandortKoordinaten(48.137, 11.575, "Europe/Berlin"),
        "72138": StandortKoordinaten(48.5333, 9.15, "Europe/Berlin"),
    }
    _ORTE = {
        "berlin": "10115",
        "muenchen": "80331",
        "kirchentellinsfurt": "72138",
    }

    def finde_koordinaten(
        self,
        ort: str,
        postleitzahl: str | None,
    ) -> StandortKoordinaten:
        if postleitzahl:
            return self._finde_per_plz(postleitzahl)

        plz = self._ORTE.get(ort.casefold())
        if plz is not None:
            return self._finde_per_plz(plz)

        raise PostleitzahlUnbekannt(
            f"Keine Koordinaten fuer Ort={ort!r}, PLZ={postleitzahl!r}"
        )

    def _finde_per_plz(self, postleitzahl: str) -> StandortKoordinaten:
        try:
            response = httpx.get(
                self.BASE_URL.format(plz=postleitzahl),
                timeout=5.0,
            )
            if response.status_code == 404:
                raise PostleitzahlUnbekannt(
                    f"Keine Koordinaten fuer PLZ={postleitzahl!r}"
                )
            response.raise_for_status()
            return self._parse_response(response.json())
        except (httpx.HTTPError, KeyError, TypeError, ValueError):
            if postleitzahl in self._PLZ:
                return self._PLZ[postleitzahl]
            raise PostleitzahlUnbekannt(
                f"Keine Koordinaten fuer PLZ={postleitzahl!r}"
            ) from None

    def _parse_response(self, data: dict) -> StandortKoordinaten:
        places = data["places"]
        if not places:
            raise ValueError("PLZ-Antwort enthaelt keinen Ort")
        place = places[0]
        return StandortKoordinaten(
            latitude=float(place["latitude"]),
            longitude=float(place["longitude"]),
            zeitzone="Europe/Berlin",
        )


DemoStandortLookup = PlzStandortLookup
