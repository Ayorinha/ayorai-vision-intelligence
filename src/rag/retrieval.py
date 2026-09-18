from dataclasses import dataclass
from ..core.repository import search_knowledge

@dataclass
class RetrievedContext:
    source: str
    content: str
    score: float

class Retriever:
    """Local-first deterministic retrieval. The interface is ready for local embeddings/vector search."""
    def search(self, query: str, top_k: int = 5) -> list[RetrievedContext]:
        return [RetrievedContext(**item) for item in search_knowledge(query, top_k)]
