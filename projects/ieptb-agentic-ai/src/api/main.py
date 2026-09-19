from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from src.core.authz import Principal, Role
from src.core.observability import new_correlation_id
from src.core.orchestrator import analyze
from src.core.schemas import Remessa

app = FastAPI(title="AyorAI Secure Remessa Intelligence", version="0.2.0", description="Synthetic-data research API for safe agentic analysis of regulated remessa workflows.")

class AnalysisRequest(BaseModel):
    remessa: Remessa
    query: str = Field(min_length=3, max_length=2000)
    tenant_id: str = Field(default="synthetic", min_length=1, max_length=64)
    role: Role = Role.ANALYST

@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    correlation_id = new_correlation_id()
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ayorai-secure-remessa-intelligence", "version": "0.2.0"}

@app.post("/analyze")
def analyze_remessa(request: AnalysisRequest) -> dict:
    principal = Principal(tenant_id=request.tenant_id, role=request.role)
    return analyze(request.remessa, request.query, principal)
