from regenbogen.system.ports.standort_port import (
    PostleitzahlUnbekannt,
    StandortKoordinaten,
    StandortPort,
)


class DemoStandortLookup(StandortPort):
    """Kleine lokale PLZ-Tabelle fuer das Tutorial."""

    _PLZ = {
        "10115": StandortKoordinaten(52.532, 13.384, "Europe/Berlin"),
        "80331": StandortKoordinaten(48.137, 11.575, "Europe/Berlin"),
    }

    def finde_koordinaten(
        self,
        ort: str,
        postleitzahl: str | None,
    ) -> StandortKoordinaten:
        if postleitzahl and postleitzahl in self._PLZ:
            return self._PLZ[postleitzahl]
        if ort == "Berlin":
            return self._PLZ["10115"]
        if ort == "Muenchen":
            return self._PLZ["80331"]
        raise PostleitzahlUnbekannt(
            f"Keine Koordinaten fuer Ort={ort!r}, PLZ={postleitzahl!r}"
        )
