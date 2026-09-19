from src.core.audit import audit_event
from src.core.audit_store import AuditStore
from src.core.authz import Principal, Role
from src.core.retrieval import retrieve
from src.core.schemas import Remessa
from src.core.security import detect_prompt_injection, redact_pii
from src.core.state import Stage, transition
from src.core.tools import call_tool

def analyze(remessa: Remessa, query: str, principal: Principal | None = None) -> dict:
    principal = principal or Principal(tenant_id="synthetic", role=Role.ANALYST)
    stage = Stage.INGEST
    stage = transition(stage, Stage.SECURITY)
    attacks = detect_prompt_injection(query)
    safe_query, pii = redact_pii(query)
    if attacks:
        stage = transition(stage, Stage.FAILED)
    else:
        stage = transition(stage, Stage.RETRIEVAL)
        evidence = retrieve(safe_query)
        stage = transition(stage, Stage.VALIDATION)
        validation = call_tool("validate_remessa", remessa.model_dump(), principal, principal.tenant_id)
        stage = transition(stage, Stage.POLICY)
        critical = call_tool("release_remessa", {"remessa_id": remessa.remessa_id}, Principal(principal.tenant_id, Role.REVIEWER), principal.tenant_id)
        stage = transition(stage, Stage.DECISION)
    explanation = (
        "Prompt injection detected; request treated as untrusted."
        if attacks else
        "Synthetic remessa analyzed with deterministic validation, evidence retrieval and policy controls."
    )
    event = audit_event("analysis.completed", {
        "remessa_id": remessa.remessa_id,
        "tenant_id": principal.tenant_id,
        "role": principal.role.value,
        "injection_detected": bool(attacks),
        "pii_types": pii,
        "validation_allowed": False if attacks else validation.allowed,
        "release_allowed": False if attacks else critical.allowed,
        "stage": stage.value,
    })
    AuditStore().append(event)
    if attacks:
        status = "BLOCKED"
        evidence = []
        requires_human = False
        release_blocked = True
    else:
        status = "REVIEW" if critical.requires_human else "ANALYZE"
        requires_human = critical.requires_human
        release_blocked = not critical.allowed
    return {
        "status": status,
        "explanation": explanation,
        "evidence": evidence,
        "requires_human_review": requires_human,
        "security": {"prompt_injection_detected": bool(attacks), "pii_redacted": pii, "unauthorized_release_blocked": release_blocked},
        "state": stage.value,
        "audit_id": event["id"],
    }
