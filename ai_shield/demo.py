from .engine import ShieldEngine
from .models import AgentRequest, Classification, Identity
from .transaction import TransactionProfile

def main():
    shield = ShieldEngine()
    request = AgentRequest("demo-001", Identity("synthetic-user-01", "treasury", 95), "agent-demo", "execute_transaction", "synthetic-account-01", Classification.RESTRICTED, amount=250000, destination="synthetic-beneficiary", human_approved=True)
    result = shield.evaluate(request, TransactionProfile(250000, False, 8, 95))
    print(f"decision={result.decision.value} reason={result.reason}")

if __name__ == "__main__": main()
