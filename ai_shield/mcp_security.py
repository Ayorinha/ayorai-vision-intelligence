from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re

from .publisher_auth import PublisherKey, ManifestSigner


_POISON_PATTERNS = (
    re.compile(
        r"ignore\s+(?:previous|prior|system)\s+instructions",
        re.IGNORECASE,
    ),
    re.compile(
        r"send\s+(?:all|the|last)\s+.*(?:records|invoices|data)",
        re.IGNORECASE,
    ),
    re.compile(
        r"include\s+.*(?:credentials|secrets|tokens)",
        re.IGNORECASE,
    ),
    re.compile(
        r"do\s+not\s+(?:tell|inform|show)\s+the\s+user",
        re.IGNORECASE,
    ),
)


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: str
    publisher: str
    endpoint: str
    version: str = "unknown"
    publisher_key_id: str | None = None
    signature: str | None = None

    def canonical(self) -> str:
        return f"{self.name}\n{self.description}\n{self.input_schema}\n{self.publisher}\n{self.endpoint}\n{self.version}"

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

    def __init__(
        self,
        trusted_publishers: dict[str, PublisherKey] | None = None,
        require_publisher_auth: bool = False,
    ) -> None:
        self._pinned: dict[str, str] = {}
        self._trusted_publishers = dict(trusted_publishers or {})
        self._require_publisher_auth = require_publisher_auth
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
        if self._require_publisher_auth:
            key = self._trusted_publishers.get(definition.publisher_key_id or "")
            if key is None or definition.signature is None:
                return ToolAssessment(False, "publisher_auth_required", digest, poisoning_signals=signals)
            if not ManifestSigner(key).verify(definition.canonical(), definition.signature):
                return ToolAssessment(False, "publisher_signature_invalid", digest, poisoning_signals=signals)
        if definition.name in self._revoked:
            return ToolAssessment(
                False,
                "tool_revoked",
                digest,
                poisoning_signals=signals,
            )
        pinned = self._pinned.get(definition.name)
        if signals:
            return ToolAssessment(
                False,
                "tool_poisoning_signal",
                digest,
                drift=pinned is not None and pinned != digest,
                poisoning_signals=signals,
            )
        if pinned is None:
            return ToolAssessment(False, "tool_not_pinned", digest)
        if pinned != digest:
            return ToolAssessment(
                False,
                "tool_definition_drift",
                digest,
                drift=True,
            )
        return ToolAssessment(True, "tool_integrity_verified", digest)

    def snapshot(self) -> dict[str, int]:
        return {
            "pinned_tools": len(self._pinned),
            "revoked_tools": len(self._revoked),
        }
