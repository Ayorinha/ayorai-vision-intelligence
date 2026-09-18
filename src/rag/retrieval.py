from dataclasses import dataclass

@dataclass
class RetrievedContext:
    source: str
    content: str
    score: float

class Retriever:
    """Provider-neutral RAG contract. Plug in a local vector store in production."""

    def search(self, query: str, top_k: int = 5) -> list[RetrievedContext]:
        return []
