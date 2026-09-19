from pydantic import BaseModel, Field


class Remessa(BaseModel):
    remessa_id: str
    apresentante: str
    quantidade_titulos: int = Field(ge=0)
    valor_total: float = Field(ge=0)
    arquivo: str


class Evidence(BaseModel):
    source_id: str
    snippet: str
    score: float = Field(ge=0, le=1)


class AnalysisResult(BaseModel):
    status: str
    explanation: str
    evidence: list[Evidence]
    requires_human_review: bool
