import math
from datetime import datetime
from zoneinfo import ZoneInfo

from regenbogen.domain.regenbogen_geometrie import Sonnenstand
from regenbogen.system.ports.standort_port import StandortKoordinaten


def berechne_sonnenstand(
    zeitpunkt: datetime,
    koordinaten: StandortKoordinaten,
) -> Sonnenstand:
    """Naeherungsweise Sonnenhoehe und Sonnenazimut."""
    lokaler_zeitpunkt = zeitpunkt.astimezone(ZoneInfo(koordinaten.zeitzone))
    tag_des_jahres = lokaler_zeitpunkt.timetuple().tm_yday
    stunde = (
        lokaler_zeitpunkt.hour
        + lokaler_zeitpunkt.minute / 60.0
        + lokaler_zeitpunkt.second / 3600.0
    )

    gamma = 2.0 * math.pi / 365.0 * (tag_des_jahres - 1 + (stunde - 12.0) / 24.0)
    deklination = (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2.0 * gamma)
        + 0.000907 * math.sin(2.0 * gamma)
        - 0.002697 * math.cos(3.0 * gamma)
        + 0.00148 * math.sin(3.0 * gamma)
    )
    zeitgleichung = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2.0 * gamma)
        - 0.040849 * math.sin(2.0 * gamma)
    )

    utc_offset = lokaler_zeitpunkt.utcoffset()
    assert utc_offset is not None
    timezone_offset_stunden = utc_offset.total_seconds() / 3600.0
    zeit_offset = (
        zeitgleichung
        + 4.0 * koordinaten.longitude
        - 60.0 * timezone_offset_stunden
    )
    wahre_sonnenzeit = stunde * 60.0 + zeit_offset
    stundenwinkel = math.radians(wahre_sonnenzeit / 4.0 - 180.0)

    breite = math.radians(koordinaten.latitude)
    hoehe = math.asin(
        math.sin(breite) * math.sin(deklination)
        + math.cos(breite) * math.cos(deklination) * math.cos(stundenwinkel)
    )
    azimut = math.atan2(
        math.sin(stundenwinkel),
        math.cos(stundenwinkel) * math.sin(breite)
        - math.tan(deklination) * math.cos(breite),
    )
    azimut_grad = (math.degrees(azimut) + 180.0) % 360.0

    return Sonnenstand(
        sonnenhoehe_grad=math.degrees(hoehe),
        sonnenazimut_grad=azimut_grad,
    )
