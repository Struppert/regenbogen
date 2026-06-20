import logging
from typing import Mapping

from regenbogen.system.ports.logging_port import EventLogger, LogEvent, LogLevel


_LEVELS = {
    LogLevel.INFO: logging.INFO,
    LogLevel.WARNING: logging.WARNING,
    LogLevel.ERROR: logging.ERROR,
}


def configure_logging(level: int = logging.INFO) -> None:
    """Konfiguriert das technische Logging fuer den Standardlauf."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


class StdlibEventLogger(EventLogger):
    """EventLogger-Implementierung auf Basis der Python-Standardbibliothek."""

    def __init__(self, logger_name: str = "regenbogen") -> None:
        self._logger = logging.getLogger(logger_name)

    def log(self, event: LogEvent) -> None:
        self._logger.log(
            _LEVELS[event.level],
            "%s | %s | %s",
            event.name,
            event.message,
            _format_fields(event.fields),
        )


def _format_fields(fields: Mapping[str, object]) -> str:
    if not fields:
        return "{}"
    teile = []
    for key in sorted(fields):
        value = fields[key]
        if isinstance(value, (str, int, float, bool)) or value is None:
            teile.append(f"{key}={value!r}")
        else:
            teile.append(f"{key}=<unsupported>")
    return "{" + ", ".join(teile) + "}"
