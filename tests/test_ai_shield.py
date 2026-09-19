from ai_shield.engine import ShieldEngine
from ai_shield.models import AgentRequest, Classification, Decision, HumanApproval, Identity
from ai_shield.transaction import TransactionProfile, score

def req(**kwargs):
    base = dict(request_id="r1", identity=Identity("u", "analyst", 95), agent_id="a1", capability="read_internal", resource="synthetic", classification=Classification.INTERNAL)
    base.update(kwargs); return AgentRequest(**base)

def approved(request):
    return HumanApproval("approval-1", "reviewer", "2026-09-19T09:00:00+00:00", ShieldEngine.request_digest(request))

def test_unknown_capability_is_blocked(): assert ShieldEngine().evaluate(req(capability="delete_everything")).decision == Decision.BLOCK
def test_role_escalation_is_blocked(): assert ShieldEngine().evaluate(req(capability="execute_transaction")).decision == Decision.BLOCK

def test_restricted_read_requires_human():
    r = req(identity=Identity("u", "senior_analyst", 95), capability="read_restricted", classification=Classification.RESTRICTED)
    assert ShieldEngine().evaluate(r).decision == Decision.REVIEW

def test_restricted_read_accepts_scoped_approval():
    r = req(identity=Identity("u", "senior_analyst", 95), capability="read_restricted", classification=Classification.RESTRICTED, human_approved=True)
    r = AgentRequest(**{**r.__dict__, "approval": approved(r)})
    assert ShieldEngine().evaluate(r).decision == Decision.ALLOW

def test_external_egress_defaults_to_deny(): assert ShieldEngine().evaluate(req(external_network=True, destination="example.invalid")).decision == Decision.BLOCK

def test_critical_transaction_is_blocked():
    r = req(identity=Identity("u", "treasury", 95), capability="execute_transaction", classification=Classification.RESTRICTED, amount=250000, human_approved=True)
    r = AgentRequest(**{**r.__dict__, "approval": approved(r)})
    assert ShieldEngine().evaluate(r, TransactionProfile(250000, False, 8, 95)).decision == Decision.BLOCK

def test_isolation_revokes_capabilities():
    e = ShieldEngine(); e.emergency_isolate("synthetic adversarial event"); assert e.evaluate(req()).decision == Decision.ISOLATE

def test_transaction_risk_bounds():
    assert 0 <= score(TransactionProfile(100, True, 0, 100)) <= 100
    assert score(TransactionProfile(200000, False, 10, 50)) == 100

def test_provenance_is_recorded_and_integrity_verifies():
    e = ShieldEngine(); e.evaluate(req()); events = e.provenance.chain("r1")
    assert len(events) == 1 and events[0].decision == Decision.ALLOW
    assert e.provenance.verify_integrity()

def test_provenance_tampering_is_detected():
    e = ShieldEngine(); e.evaluate(req()); e.provenance.events[0].resource = "tampered"
    assert not e.provenance.verify_integrity()

def test_provenance_tail_truncation_is_detected():
    e = ShieldEngine(); e.evaluate(req()); e.provenance.events.pop()
    assert not e.provenance.verify_integrity()

def test_replay_is_blocked_for_consequential_requests():
    e = ShieldEngine(); r = req(identity=Identity("u", "senior_analyst", 95), capability="read_restricted", classification=Classification.RESTRICTED, human_approved=True)
    r = AgentRequest(**{**r.__dict__, "approval": approved(r)})
    assert e.evaluate(r).decision == Decision.ALLOW
    assert e.evaluate(r).decision == Decision.BLOCK

def test_approval_cannot_be_replayed_for_modified_request():
    e = ShieldEngine(); original = req(identity=Identity("u", "senior_analyst", 95), capability="read_restricted", classification=Classification.RESTRICTED, resource="record-A", human_approved=True)
    modified = AgentRequest(**{**original.__dict__, "resource": "record-B", "approval": approved(original)})
    assert e.evaluate(modified).decision == Decision.REVIEW