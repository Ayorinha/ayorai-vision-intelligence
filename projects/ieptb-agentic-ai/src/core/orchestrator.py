from src.core.audit import audit_event
from src.core.retrieval import retrieve
from src.core.schemas import Remessa
from src.core.security import detect_prompt_injection, redact_pii
from src.core.tools import call_tool

def analyze(remessa: Remessa, query: str) -> dict:
    attacks=detect_prompt_injection(query)
    safe_query, pii=redact_pii(query)
    evidence=retrieve(safe_query)
    validation=call_tool("validate_remessa", remessa.model_dump())
    critical=call_tool("release_remessa", {"remessa_id":remessa.remessa_id})
    status="BLOCKED" if attacks else ("REVIEW" if critical.requires_human else "ANALYZE")
    explanation=(
        "Prompt injection detected; request treated as untrusted."
        if attacks else
        "Synthetic remessa analyzed with deterministic validation, evidence retrieval and policy controls."
    )
    event=audit_event("analysis.completed",{
        "remessa_id":remessa.remessa_id,"injection_detected":bool(attacks),
        "pii_types":pii,"validation_allowed":validation.allowed,
        "release_allowed":critical.allowed,
    })
    return {
        "status":status,
        "explanation":explanation,
        "evidence":evidence,
        "requires_human_review":critical.requires_human,
        "security":{"prompt_injection_detected":bool(attacks),"pii_redacted":pii,
                    "unauthorized_release_blocked":not critical.allowed},
        "audit_id":event["id"],
    }
