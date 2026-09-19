from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.core.orchestrator import analyze
from src.core.schemas import Remessa

app = FastAPI(
    title="AyorAI Secure Remessa Intelligence",
    version="0.1.0",
    description="Synthetic-data research API for safe agentic analysis of regulated remessa workflows.",
)

class AnalysisRequest(BaseModel):
    remessa: Remessa
    query: str = Field(min_length=3, max_length=2000)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ayorai-secure-remessa-intelligence"}

@app.post("/analyze")
def analyze_remessa(request: AnalysisRequest) -> dict:
    return analyze(request.remessa, request.query)
