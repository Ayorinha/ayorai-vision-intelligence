from datetime import UTC, datetime

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
    if not approval.approval_id.strip() or not approval.approved_by.strip():
        return False
    if approval.request_digest != _request_digest(request):
        return False
    try:
        approved_at = datetime.fromisoformat(approval.approved_at)
    except ValueError:
        return False
    if approved_at.tzinfo is None:
        return False
    now = datetime.now(UTC)
    if approved_at > now:
        return False
    if approval.expires_at is not None:
        try:
            expires_at = datetime.fromisoformat(approval.expires_at)
        except ValueError:
            return False
        if expires_at.tzinfo is None or now >= expires_at:
            return False
        if expires_at <= approved_at:
            return False
    return True

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
    if requires_human and not _approval_valid(request):
        reason = "human_approval_required" if not request.human_approved else "approval_binding_invalid"
        return PolicyResult(Decision.REVIEW, reason, ("human_in_the_loop",))
    return PolicyResult(Decision.ALLOW, "policy_satisfied", ("least_privilege",))