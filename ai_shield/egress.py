from .models import Decision, PolicyResult

def evaluate(destination: str | None, approved_destination: bool = False) -> PolicyResult:
    if destination is None: return PolicyResult(Decision.BLOCK, "no_destination", ("egress_default_deny",))
    if not approved_destination: return PolicyResult(Decision.BLOCK, "destination_not_allowlisted", ("egress_default_deny",))
    return PolicyResult(Decision.ALLOW, "destination_allowlisted", ("egress_allowlist",))
