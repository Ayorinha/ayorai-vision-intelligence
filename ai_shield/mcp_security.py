from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re


_POISON_PATTERNS = (
    re.compile(r"ignore\s+(?:previous|prior|system)\s+instructions", re.I),
    re.compile(r"send\s+(?:all|the|last)\s+.*(?:records|invoices|data)", re.I),
    re.compile(r"include\s+.*(?:credentials|secrets|tokens)", re.I),
    re.compile(r"do\s+not\s+(?:tell|inform|show)\s+the\s+user", re.I),
)


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: str
    publisher: str
    endpoint: str
    version: str = "unknown"

    def canonical(self) -> str:
        return "\n".join(
            (self.name, self.description, self.input_schema, self.publisher, self.endpoint, self.version)
        )

    def digest(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ToolAssessment:
    allowed: bool
    reason: str
    digest: str
    drift: bool = False
    poisoning_signals: tuple[str, ...] = ()


class ToolIntegrityRegistry:
    """TOFU-pinned MCP metadata with deterministic drift and poisoning checks."""

    def __init__(self) -> None:
        self._pinned: dict[str, str] = {}
        self._definitions: dict[str, ToolDefinition] = {}
        self._revoked: set[str] = set()

    @staticmethod
    def _signals(definition: ToolDefinition) -> tuple[str, ...]:
        text = f"{definition.description}\n{definition.input_schema}"
        signals: list[str] = []
        for pattern in _POISON_PATTERNS:
            if pattern.search(text):
                signals.append(pattern.pattern)
        return tuple(signals)

    def pin(self, definition: ToolDefinition) -> str:
        digest = definition.digest()
        self._pinned[definition.name] = digest
        self._definitions[definition.name] = definition
        return digest

    def revoke(self, name: str) -> None:
        self._revoked.add(name)

    def assess(self, definition: ToolDefinition) -> ToolAssessment:
        digest = definition.digest()
        signals = self._signals(definition)
        if definition.name in self._revoked:
            return ToolAssessment(False, "tool_revoked", digest, poisoning_signals=signals)
        pinned = self._pinned.get(definition.name)
        if signals:
            return ToolAssessment(False, "tool_poisoning_signal", digest, drift=pinned is not None and pinned != digest, poisoning_signals=signals)
        if pinned is None:
            return ToolAssessment(False, "tool_not_pinned", digest)
        if pinned != digest:
            return ToolAssessment(False, "tool_definition_drift", digest, drift=True)
        return ToolAssessment(True, "tool_integrity_verified", digest)

    def snapshot(self) -> dict[str, int]:
        return {"pinned_tools": len(self._pinned), "revoked_tools": len(self._revoked)}
