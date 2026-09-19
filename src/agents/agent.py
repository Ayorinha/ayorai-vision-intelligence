class EvidenceAgent:
    """Evidence-first agent boundary for a future local/private LLM adapter."""
    def __init__(self, orchestrator):
        self.orchestrator=orchestrator

    def inspect(self, query):
        return self.orchestrator.answer(query)
