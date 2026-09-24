from math import isfinite

from pydantic import BaseModel, Field, field_validator


class Detection(BaseModel):
    frame: int = Field(ge=0)
    track_id: int | None = Field(default=None, ge=0)
    label: str = Field(min_length=1, max_length=100)
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: tuple[float, float, float, float]

    @field_validator("confidence")
    @classmethod
    def finite_confidence(cls, value: float) -> float:
        if not isfinite(value):
            raise ValueError("Confidence must be finite")
        return value

    @field_validator("bbox")
    @classmethod
    def valid_bbox(cls, value):
        x1, y1, x2, y2 = value
        if not all(isfinite(v) for v in value):
            raise ValueError("Bounding box coordinates must be finite")
        if x2 < x1 or y2 < y1:
            raise ValueError("Invalid bounding box")
        return value


class ReviewDecision(BaseModel):
    decision: str
    reviewer: str = Field(default="human", min_length=1, max_length=100)
    final_label: str | None = Field(default=None, max_length=100)

    @field_validator("decision")
    @classmethod
    def valid_decision(cls, value: str) -> str:
        if value not in {"APPROVED", "REJECTED"}:
            raise ValueError("decision must be APPROVED or REJECTED")
        return value


class TrackSummary(BaseModel):
    track_id: int
    label: str
    first_frame: int
    last_frame: int
    frames_seen: int
    mean_confidence: float
