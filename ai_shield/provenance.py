from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import hashlib
import json

from .models import ProvenanceEvent


@dataclass
class ProvenanceGraph:
    events: list[ProvenanceEvent] = field(default_factory=list)
    _sealed_count: int = field(default=0, init=False, repr=False)
    _sealed_head_hash: str | None = field(default=None, init=False, repr=False)

    @staticmethod
    def _canonical(event: ProvenanceEvent) -> str:
        payload = {
            "event_id": event.event_id, "request_id": event.request_id, "actor": event.actor,
            "agent_id": event.agent_id, "action": event.action, "resource": event.resource,
            "decision": event.decision.value, "parent_event_id": event.parent_event_id,
            "timestamp": event.timestamp, "previous_hash": event.previous_hash, "metadata": event.metadata,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    @classmethod
    def _digest(cls, event: ProvenanceEvent) -> str:
        return hashlib.sha256(cls._canonical(event).encode("utf-8")).hexdigest()

    def record(self, *, event_id, request_id, actor, agent_id, action, resource, decision, parent_event_id=None, metadata=None):
        previous_hash = self.events[-1].event_hash if self.events else None
        event = ProvenanceEvent(event_id=event_id, request_id=request_id, actor=actor, agent_id=agent_id, action=action, resource=resource, decision=decision, parent_event_id=parent_event_id, timestamp=datetime.now(UTC).isoformat(), previous_hash=previous_hash, metadata=dict(metadata or {}))
        event.event_hash = self._digest(event)
        self.events.append(event)
        self._sealed_count = len(self.events)
        self._sealed_head_hash = event.event_hash
        return event

    def verify_integrity(self) -> bool:
        if len(self.events) != self._sealed_count:
            return False
        previous_hash = None
        for event in self.events:
            if event.previous_hash != previous_hash or event.event_hash != self._digest(event):
                return False
            previous_hash = event.event_hash
        return previous_hash == self._sealed_head_hash

    def chain(self, request_id):
        return [event for event in self.events if event.request_id == request_id]
