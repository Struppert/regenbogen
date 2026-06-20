from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class LogLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class LogEvent:
    """Systemisches Laufzeitereignis fuer Diagnose-Logging."""

    name: str
    level: LogLevel
    message: str
    fields: Mapping[str, object] = field(default_factory=dict)


class EventLogger(ABC):
    @abstractmethod
    def log(self, event: LogEvent) -> None:
        raise NotImplementedError


class NullEventLogger(EventLogger):
    def log(self, event: LogEvent) -> None:
        pass
