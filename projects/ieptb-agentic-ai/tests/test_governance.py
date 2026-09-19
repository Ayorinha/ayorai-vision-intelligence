from src.core.authz import Principal, Role, can_call
from src.core.state import Stage, transition

def test_cross_tenant_access_is_denied():
    assert not can_call(Principal("tenant-a", Role.ANALYST), "validate_remessa", "tenant-b")

def test_viewer_cannot_validate():
    assert not can_call(Principal("tenant-a", Role.VIEWER), "validate_remessa", "tenant-a")

def test_state_machine_rejects_skip():
    try:
        transition(Stage.INGEST, Stage.DECISION)
    except ValueError:
        return
    raise AssertionError("invalid transition was accepted")
