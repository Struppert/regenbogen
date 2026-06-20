from regenbogen.infrastructure.open_meteo_client import OpenMeteoClient
from regenbogen.system.ports.standort_port import StandortKoordinaten


BERLIN = StandortKoordinaten(52.532, 13.384, "Europe/Berlin")


def stunden_antwort(stunden_count: int = 24) -> dict:
    """Minimale Open-Meteo hourly response mit stunden_count Eintraegen."""
    times = [f"2026-06-20T{h:02d}:00" for h in range(stunden_count)]
    return {
        "hourly": {
            "time": times,
            "sunshine_duration": [1800.0] * stunden_count,
            "precipitation": [5.0] * stunden_count,
            "rain": [5.0] * stunden_count,
            "showers": [0.0] * stunden_count,
            "snowfall": [0.0] * stunden_count,
            "weather_code": [61] * stunden_count,
            "cloud_cover": [60.0] * stunden_count,
            "visibility": [10_000.0] * stunden_count,
            "direct_radiation": [400.0] * stunden_count,
            "temperature_2m": [12.0] * stunden_count,
        }
    }


def test_parse_hourly_liefert_korrekte_anzahl():
    client = OpenMeteoClient()
    result = client._parse_hourly_response(stunden_antwort(24), "Europe/Berlin")
    assert len(result) == 24


def test_parse_hourly_zeitpunkt_ist_utc():
    client = OpenMeteoClient()
    result = client._parse_hourly_response(stunden_antwort(1), "Europe/Berlin")
    utcoffset = result[0].zeitpunkt_utc.utcoffset()
    assert utcoffset is not None
    assert utcoffset.total_seconds() == 0


def test_parse_hourly_konvertiert_lokalzeit_zu_utc():
    client = OpenMeteoClient()
    # 00:00 Europe/Berlin (UTC+2 im Sommer) → 22:00 UTC des Vortags
    result = client._parse_hourly_response(stunden_antwort(1), "Europe/Berlin")
    assert result[0].zeitpunkt_utc.hour == 22


def test_parse_hourly_messung_felder():
    client = OpenMeteoClient()
    result = client._parse_hourly_response(stunden_antwort(1), "Europe/Berlin")
    m = result[0].messung
    assert m.sonnenschein_sekunden == 1800.0
    assert m.niederschlag_mm == 5.0
    assert m.rain_mm == 5.0
    assert m.weather_code == 61
    assert m.visibility_m == 10_000.0


def test_parse_hourly_none_visibility():
    client = OpenMeteoClient()
    data = stunden_antwort(1)
    data["hourly"]["visibility"] = [None]
    result = client._parse_hourly_response(data, "Europe/Berlin")
    assert result[0].messung.visibility_m is None


def test_parse_hourly_leere_antwort():
    client = OpenMeteoClient()
    result = client._parse_hourly_response({"hourly": {"time": []}}, "Europe/Berlin")
    assert result == []
