"""Model-agnostic frontier-agent evaluation harness.
This module never executes network attacks or real transactions. A caller supplies an agent proposal; the deterministic ShieldEngine remains the authority.
"""
from dataclasses import dataclass
from .engine import ShieldEngine
from .models import AgentRequest, Decision
@dataclass(frozen=True)
class EvaluationCase:
    name: str
    request: AgentRequest
    expected: Decision
@dataclass(frozen=True)
class EvaluationResult:
    name: str
    expected: Decision
    observed: Decision
    passed: bool
    reason: str
def evaluate_cases(engine: ShieldEngine, cases: list[EvaluationCase]) -> list[EvaluationResult]:
    results=[]
    for case in cases:
        observed=engine.evaluate(case.request)
        results.append(EvaluationResult(case.name,case.expected,observed,observed==case.expected,"decision recorded"))
    return results
