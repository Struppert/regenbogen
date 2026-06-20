import httpx
import pytest

from regenbogen.infrastructure.plz_lookup import PlzStandortLookup
from regenbogen.system.ports.standort_port import PostleitzahlUnbekannt


class FakeResponse:
    def __init__(self, status_code: int, data: dict) -> None:
        self.status_code = status_code
        self._data = data

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                "HTTP error",
                request=httpx.Request("GET", "https://example.test"),
                response=httpx.Response(self.status_code),
            )

    def json(self) -> dict:
        return self._data


def test_plz_lookup_nutzt_http_daten(monkeypatch):
    def fake_get(url: str, timeout: float):
        assert url == "https://api.zippopotam.us/de/72138"
        assert timeout == 5.0
        return FakeResponse(
            200,
            {
                "places": [
                    {
                        "latitude": "48.5333",
                        "longitude": "9.1500",
                    }
                ]
            },
        )

    monkeypatch.setattr("regenbogen.infrastructure.plz_lookup.httpx.get", fake_get)

    koordinaten = PlzStandortLookup().finde_koordinaten("Kirchentellinsfurt", "72138")

    assert koordinaten.latitude == 48.5333
    assert koordinaten.longitude == 9.15
    assert koordinaten.zeitzone == "Europe/Berlin"


def test_plz_lookup_nutzt_lokalen_fallback_bei_http_fehler(monkeypatch):
    def fake_get(url: str, timeout: float):
        raise httpx.ConnectError("offline")

    monkeypatch.setattr("regenbogen.infrastructure.plz_lookup.httpx.get", fake_get)

    koordinaten = PlzStandortLookup().finde_koordinaten("Kirchentellinsfurt", "72138")

    assert koordinaten.latitude == 48.5333
    assert koordinaten.longitude == 9.15


def test_plz_lookup_meldet_unbekannte_plz(monkeypatch):
    def fake_get(url: str, timeout: float):
        return FakeResponse(404, {})

    monkeypatch.setattr("regenbogen.infrastructure.plz_lookup.httpx.get", fake_get)

    with pytest.raises(PostleitzahlUnbekannt):
        PlzStandortLookup().finde_koordinaten("Unbekannt", "00000")


def test_plz_lookup_findet_ort_ueber_lokale_ortszuordnung(monkeypatch):
    def fake_get(url: str, timeout: float):
        raise httpx.ConnectError("offline")

    monkeypatch.setattr("regenbogen.infrastructure.plz_lookup.httpx.get", fake_get)

    koordinaten = PlzStandortLookup().finde_koordinaten("Kirchentellinsfurt", None)

    assert koordinaten.latitude == 48.5333
    assert koordinaten.longitude == 9.15
