import time
from datetime import datetime
from zoneinfo import ZoneInfo

from regenbogen.infrastructure.event_logger import (
    StdlibEventLogger,
    configure_logging,
)
from regenbogen.infrastructure.open_meteo_client import OpenMeteoClient
from regenbogen.infrastructure.plz_lookup import PlzStandortLookup
from regenbogen.system.core.tagesprognose_use_case import TagesPrognoseUseCase
from regenbogen.system.core.wahrscheinlichkeit_use_case import (
    RegenbogenWahrscheinlichkeitUseCase,
)


def create_regenbogen_use_case() -> RegenbogenWahrscheinlichkeitUseCase:
    """Verdrahtet alle Infrastruktur-Komponenten fuer den Produktivlauf."""
    configure_logging()
    return RegenbogenWahrscheinlichkeitUseCase(
        api=OpenMeteoClient(),
        standort=PlzStandortLookup(),
        sleep=time.sleep,
        clock=lambda: datetime.now(ZoneInfo("Europe/Berlin")),
        logger=StdlibEventLogger(),
    )


def create_tagesprognose_use_case() -> TagesPrognoseUseCase:
    """Verdrahtet alle Infrastruktur-Komponenten fuer den Tagesprognose-Lauf."""
    return TagesPrognoseUseCase(
        api=OpenMeteoClient(),
        standort=PlzStandortLookup(),
        sleep=time.sleep,
        clock=lambda: datetime.now(ZoneInfo("Europe/Berlin")),
    )
