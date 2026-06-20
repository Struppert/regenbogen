import httpx

from regenbogen.system.ports.standort_port import StandortKoordinaten
from regenbogen.system.ports.wetterapi_port import (
    WetterApiMessung,
    WetterApiNichtErreichbar,
    WetterApiPort,
)


class OpenMeteoClient(WetterApiPort):
    """Implementiert WetterApiPort ueber die Open-Meteo API."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def hole_aktuelle_messung(
        self,
        koordinaten: StandortKoordinaten,
    ) -> WetterApiMessung:
        try:
            response = httpx.get(
                self.BASE_URL,
                params={
                    "latitude": koordinaten.latitude,
                    "longitude": koordinaten.longitude,
                    "current": ",".join(
                        [
                            "temperature_2m",
                            "precipitation",
                            "rain",
                            "showers",
                            "snowfall",
                            "weather_code",
                            "cloud_cover",
                            "visibility",
                            "direct_radiation",
                            "sunshine_duration",
                        ]
                    ),
                },
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.ConnectError as exc:
            raise WetterApiNichtErreichbar(f"Nicht erreichbar: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise WetterApiNichtErreichbar(
                f"API-Fehler: {exc.response.status_code}"
            ) from exc

        return self._parse_response(response.json())

    def _parse_response(self, data: dict) -> WetterApiMessung:
        current = data.get("current", {})
        return WetterApiMessung(
            sonnenschein_sekunden=float(current.get("sunshine_duration", 0.0)),
            niederschlag_mm=float(current.get("precipitation", 0.0)),
            rain_mm=float(current.get("rain", 0.0)),
            showers_mm=float(current.get("showers", 0.0)),
            snowfall_cm=float(current.get("snowfall", 0.0)),
            weather_code=int(current.get("weather_code", 0)),
            cloud_cover=float(current.get("cloud_cover", 100.0)),
            visibility_m=(
                float(current["visibility"])
                if current.get("visibility") is not None
                else None
            ),
            direct_radiation=float(current.get("direct_radiation", 0.0)),
            temperature_2m=float(current.get("temperature_2m", 0.0)),
        )
