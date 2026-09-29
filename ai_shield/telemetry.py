from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class TelemetryEvent:
    """Small, dependency-free event model with OpenTelemetry-style attributes."""

    name: str
    attributes: dict[str, object] = field(default_factory=dict)


class TelemetrySink(Protocol):
    """Adapter boundary for OpenTelemetry or another observability backend."""

    def emit(self, event: TelemetryEvent) -> None:
        ...


class NullTelemetry:
    """No-op default so observability never becomes an authorization dependency."""

    def emit(self, event: TelemetryEvent) -> None:
        return None


@dataclass
class InMemoryTelemetry:
    """Deterministic sink used by tests and local evaluation."""

    events: list[TelemetryEvent] = field(default_factory=list)

    def emit(self, event: TelemetryEvent) -> None:
        self.events.append(event)
