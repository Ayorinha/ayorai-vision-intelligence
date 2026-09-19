from enum import StrEnum

class Stage(StrEnum):
    INGEST = "ingest"
    SECURITY = "security"
    RETRIEVAL = "retrieval"
    VALIDATION = "validation"
    POLICY = "policy"
    DECISION = "decision"
    AUDIT = "audit"
    FAILED = "failed"

ALLOWED_TRANSITIONS = {
    Stage.INGEST: {Stage.SECURITY},
    Stage.SECURITY: {Stage.RETRIEVAL, Stage.FAILED},
    Stage.RETRIEVAL: {Stage.VALIDATION, Stage.FAILED},
    Stage.VALIDATION: {Stage.POLICY, Stage.FAILED},
    Stage.POLICY: {Stage.DECISION, Stage.FAILED},
    Stage.DECISION: {Stage.AUDIT, Stage.FAILED},
    Stage.AUDIT: set(),
    Stage.FAILED: {Stage.AUDIT},
}

def transition(current: Stage, target: Stage) -> Stage:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"invalid transition: {current} -> {target}")
    return target
