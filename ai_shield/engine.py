from .egress import evaluate
from .isolation import SovereignIsolator
from .models import AgentRequest, Decision, PolicyResult
from .policy import authorize
from .provenance import ProvenanceGraph
from .transaction import TransactionProfile, govern

class ShieldEngine:
    """Deterministic decision pipeline. No LLM is used for authorization."""
    def __init__(self):
        self.isolator = SovereignIsolator()
        self.provenance = ProvenanceGraph()
    def evaluate(self, request: AgentRequest, transaction: TransactionProfile | None = None) -> PolicyResult:
        if not self.isolator.can_execute(request.capability):
            result = PolicyResult(Decision.ISOLATE, "capability_revoked_by_isolation", ("sovereign_isolator",))
        else:
            result = authorize(request)
            if result.decision == Decision.ALLOW and transaction is not None:
                result = govern(request, transaction)
            if result.decision == Decision.ALLOW and request.external_network:
                result = evaluate(request.destination, approved_destination=False)
        self.provenance.record(event_id=f"event-{len(self.provenance.events)+1}", request_id=request.request_id, actor=request.identity.subject, agent_id=request.agent_id, action=request.capability, resource=request.resource, decision=result.decision)
        return result
    def emergency_isolate(self, reason: str) -> None:
        self.isolator.isolate(reason)
