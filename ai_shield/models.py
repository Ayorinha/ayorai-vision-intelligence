from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class Decision(str, Enum):
    ALLOW = "allow"
    REVIEW = "review"
    BLOCK = "block"
    ISOLATE = "isolate"

class Classification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

@dataclass(frozen=True)
class Identity:
    subject: str
    role: str
    assurance: int
    active: bool = True

@dataclass(frozen=True)
class AgentRequest:
    request_id: str
    identity: Identity
    agent_id: str
    capability: str
    resource: str
    classification: Classification
    amount: float = 0.0
    destination: str | None = None
    external_network: bool = False
    human_approved: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class PolicyResult:
    decision: Decision
    reason: str
    controls: tuple[str, ...] = ()

@dataclass
class ProvenanceEvent:
    event_id: str
    request_id: str
    actor: str
    agent_id: str
    action: str
    resource: str
    decision: Decision
    parent_event_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
