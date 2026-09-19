from dataclasses import dataclass
from .models import AgentRequest, Decision, PolicyResult

@dataclass(frozen=True)
class TransactionProfile:
    amount: float
    known_destination: bool
    recent_velocity: int
    identity_assurance: int

def score(profile: TransactionProfile) -> int:
    risk = 0
    if profile.amount >= 100_000: risk += 50
    elif profile.amount >= 10_000: risk += 25
    if not profile.known_destination: risk += 25
    if profile.recent_velocity >= 5: risk += 15
    if profile.identity_assurance < 80: risk += 20
    return min(risk, 100)

def govern(request: AgentRequest, profile: TransactionProfile) -> PolicyResult:
    risk = score(profile)
    if risk >= 70: return PolicyResult(Decision.BLOCK, f"critical_transaction_risk:{risk}", ("transaction_governor",))
    if risk >= 40: return PolicyResult(Decision.REVIEW, f"elevated_transaction_risk:{risk}", ("transaction_governor",))
    return PolicyResult(Decision.ALLOW, f"transaction_risk:{risk}", ("transaction_governor",))
