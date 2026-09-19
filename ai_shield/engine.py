from __future__ import annotations

import hashlib
import json

from .egress import evaluate
from .isolation import SovereignIsolator
from .models import AgentRequest, Decision, PolicyResult
from .policy import authorize
from .provenance import ProvenanceGraph
from .transaction import TransactionProfile, govern
from .trust import AgentTrustFabric


class ShieldEngine:
    """Deterministic decision pipeline. No LLM is used for authorization."""

    def __init__(self, trust_fabric: AgentTrustFabric | None = None):
        self.isolator = SovereignIsolator()
        self.provenance = ProvenanceGraph()
        self.trust_fabric = trust_fabric
        self._seen_requests: set[str] = set()

    @staticmethod
    def request_digest(request: AgentRequest) -> str:
        payload = {
            "request_id": request.request_id,
            "identity": {
                "subject": request.identity.subject,
                "role": request.identity.role,
                "assurance": request.identity.assurance,
                "active": request.identity.active,
            },
            "agent_id": request.agent_id,
            "capability": request.capability,
            "resource": request.resource,
            "classification": request.classification.value,
            "amount": request.amount,
            "destination": request.destination,
            "external_network": request.external_network,
            "idempotency_key": request.idempotency_key,
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _consequential(request: AgentRequest) -> bool:
        return request.capability in {"execute_transaction", "read_restricted"}

    def evaluate(self, request: AgentRequest, transaction: TransactionProfile | None = None) -> PolicyResult:
        replay_key = request.idempotency_key or request.request_id
        if self._consequential(request) and replay_key in self._seen_requests:
            result = PolicyResult(Decision.BLOCK, "replay_detected", ("replay_protection",))
        elif not self.isolator.can_execute(request.capability):
            result = PolicyResult(
                Decision.ISOLATE, "capability_revoked_by_isolation", ("sovereign_isolator",)
            )
        else:
            result = self.trust_fabric.authorize(request) if self.trust_fabric is not None else authorize(request)
            if result.decision == Decision.ALLOW:
                result = authorize(request)
            if result.decision == Decision.ALLOW and transaction is not None:
                result = govern(request, transaction)
            if result.decision == Decision.ALLOW and request.external_network:
                result = evaluate(request.destination, approved_destination=False)

        if result.decision in {Decision.ALLOW, Decision.REVIEW} and self._consequential(request):
            self._seen_requests.add(replay_key)

        self.provenance.record(
            event_id=f"event-{len(self.provenance.events)+1}",
            request_id=request.request_id,
            actor=request.identity.subject,
            agent_id=request.agent_id,
            action=request.capability,
            resource=request.resource,
            decision=result.decision,
            metadata={
                "request_digest": self.request_digest(request),
                "trust_fabric": self.trust_fabric is not None,
            },
        )
        return result

    def emergency_isolate(self, reason: str) -> None:
        self.isolator.isolate(reason)
