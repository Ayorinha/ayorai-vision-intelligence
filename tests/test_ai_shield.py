from ai_shield.engine import ShieldEngine
from ai_shield.models import AgentRequest, Classification, Decision, Identity
from ai_shield.transaction import TransactionProfile, score

def req(**kwargs):
    base = dict(request_id="r1", identity=Identity("u", "analyst", 95), agent_id="a1", capability="read_internal", resource="synthetic", classification=Classification.INTERNAL)
    base.update(kwargs); return AgentRequest(**base)

def test_unknown_capability_is_blocked(): assert ShieldEngine().evaluate(req(capability="delete_everything")).decision == Decision.BLOCK

def test_role_escalation_is_blocked(): assert ShieldEngine().evaluate(req(capability="execute_transaction")).decision == Decision.BLOCK

def test_restricted_read_requires_human():
    r=req(identity=Identity("u","senior_analyst",95),capability="read_restricted",classification=Classification.RESTRICTED)
    assert ShieldEngine().evaluate(r).decision == Decision.REVIEW

def test_external_egress_defaults_to_deny():
    r=req(external_network=True,destination="example.invalid")
    assert ShieldEngine().evaluate(r).decision == Decision.BLOCK

def test_critical_transaction_is_blocked():
    r=req(identity=Identity("u","treasury",95),capability="execute_transaction",classification=Classification.RESTRICTED,amount=250000,human_approved=True)
    assert ShieldEngine().evaluate(r,TransactionProfile(250000,False,8,95)).decision == Decision.BLOCK

def test_isolation_revokes_capabilities():
    e=ShieldEngine(); e.emergency_isolate("synthetic adversarial event"); assert e.evaluate(req()).decision == Decision.ISOLATE

def test_transaction_risk_bounds():
    assert 0 <= score(TransactionProfile(100,True,0,100)) <= 100
    assert score(TransactionProfile(200000,False,10,50)) == 100

def test_provenance_is_recorded():
    e=ShieldEngine(); e.evaluate(req()); events=e.provenance.chain("r1"); assert len(events)==1 and events[0].decision==Decision.ALLOW
