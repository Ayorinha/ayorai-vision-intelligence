from pydantic import BaseModel, Field

class Detection(BaseModel):
    frame: int
    track_id: int | None = None
    label: str
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: tuple[float, float, float, float]

class ReviewDecision(BaseModel):
    track_id: int
    decision: str
    reviewer: str = "human"

class TrackSummary(BaseModel):
    track_id: int
    label: str
    first_frame: int
    last_frame: int
    frames_seen: int
    mean_confidence: float
