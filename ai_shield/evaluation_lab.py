from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .models import AgentRequest, Decision
from .trust import AgentTrustFabric


class Scenario(str, Enum):
    PROMPT_INJECTION = "prompt_injection"
    UNKNOWN_CAPABILITY = "unknown_capability"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DELEGATION_ABUSE = "delegation_abuse"
    REPLAY = "replay"
    DATA_EXFILTRATION = "data_exfiltration"


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    scenario: Scenario
    request: AgentRequest
    expected: Decision
    metadata: dict[str, str] | None = None


@dataclass(frozen=True)
class EvaluationResult:
    case: str
    scenario: Scenario
    expected: Decision
    observed: Decision

    @property
    def passed(self) -> bool:
        return self.expected == self.observed


def evaluate_case(fabric: AgentTrustFabric, case: EvaluationCase) -> EvaluationResult:
    observed = fabric.authorize(case.request).decision
    return EvaluationResult(case.name, case.scenario, case.expected, observed)


def summarize(results: list[EvaluationResult]) -> dict[str, float | int]:
    total = len(results)
    passed = sum(result.passed for result in results)
    return {
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": total - passed,
        "pass_rate": (passed / total) if total else 1.0,
    }
