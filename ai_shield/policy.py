from datetime import datetime, timezone

from .models import AgentRequest, Classification, Decision, PolicyResult


_LEVEL = {
    Classification.PUBLIC: 0,
    Classification.INTERNAL: 1,
    Classification.CONFIDENTIAL: 2,
    Classification.RESTRICTED: 3,
}
_CAPABILITIES = {
    "read_public": ("analyst", Classification.PUBLIC, False),
    "read_internal": ("analyst", Classification.INTERNAL, False),
    "read_restricted": ("senior_analyst", Classification.RESTRICTED, True),
    "analyze_transaction": ("analyst", Classification.CONFIDENTIAL, False),
    "execute_transaction": ("treasury", Classification.RESTRICTED, True),
}


def _approval_valid(request: AgentRequest) -> bool:
    approval = request.approval
    if not request.human_approved or approval is None:
        return False
    if approval.request_digest != _request_digest(request):
        return False
    if approval.expires_at is None:
        return True
    try:
        return datetime.now(timezone.utc) < datetime.fromisoformat(approval.expires_at)
    except ValueError:
        return False


def _request_digest(request: AgentRequest) -> str:
    from .engine import ShieldEngine
    return ShieldEngine.request_digest(request)


def authorize(request: AgentRequest) -> PolicyResult:
    if not request.identity.active:
        return PolicyResult(Decision.BLOCK, "inactive_identity", ("identity",))
    capability = _CAPABILITIES.get(request.capability)
    if capability is None:
        return PolicyResult(Decision.BLOCK, "unknown_capability", ("least_privilege",))
    role, maximum, requires_human = capability
    if request.identity.role != role:
        return PolicyResult(Decision.BLOCK, "role_not_authorized", ("least_privilege",))
    if _LEVEL[request.classification] > _LEVEL[maximum]:
        return PolicyResult(Decision.BLOCK, "classification_exceeds_clearance", ("data_boundary",))
    if request.external_network:
        return PolicyResult(Decision.BLOCK, "unauthorized_egress", ("egress",))
    if requires_human and not _approval_valid(request):
        reason = "human_approval_required" if not request.human_approved else "approval_binding_invalid"
        return PolicyResult(Decision.REVIEW, reason, ("human_in_the_loop",))
    return PolicyResult(Decision.ALLOW, "policy_satisfied", ("least_privilege",))
