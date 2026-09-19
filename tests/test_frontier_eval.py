from ai_shield.engine import ShieldEngine
from ai_shield.frontier_eval import EvaluationCase, evaluate_cases
from ai_shield.models import AgentRequest, Classification, Decision, Identity

def test_frontier_harness_keeps_model_proposal_non_authoritative():
    request=AgentRequest("frontier-1",Identity("u","analyst",100),"frontier-agent","execute_transaction","synthetic",Classification.RESTRICTED,human_approved=False,metadata={"model_confidence":1.0,"model_claim":"authorized"})
    results=evaluate_cases(ShieldEngine(),[EvaluationCase("model-claim-cannot-authorize",request,Decision.BLOCK)])
    assert results[0].passed

def test_frontier_harness_is_deterministic():
    request=AgentRequest("frontier-2",Identity("u","analyst",95),"agent","read_internal","synthetic",Classification.INTERNAL)
    a=evaluate_cases(ShieldEngine(),[EvaluationCase("same",request,Decision.ALLOW)])
    b=evaluate_cases(ShieldEngine(),[EvaluationCase("same",request,Decision.ALLOW)])
    assert a[0].observed==b[0].observed==Decision.ALLOW
