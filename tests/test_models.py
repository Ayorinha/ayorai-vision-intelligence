import pytest
from pydantic import ValidationError
from src.vision.models import Detection, ReviewDecision

def test_detection_accepts_valid_bbox():
    d = Detection(frame=1, track_id=7, label="person", confidence=0.95, bbox=(1,2,10,20))
    assert d.track_id == 7

def test_detection_rejects_invalid_bbox():
    with pytest.raises(ValidationError):
        Detection(frame=1, label="person", confidence=0.95, bbox=(10,2,1,20))



def test_detection_rejects_non_finite_values():
    with pytest.raises(ValidationError):
        Detection(frame=1, label="person", confidence=float("nan"), bbox=(1, 2, 10, 20))
    with pytest.raises(ValidationError):
        Detection(frame=1, label="person", confidence=0.9, bbox=(1, 2, float("inf"), 20))


def test_review_decision_rejects_unknown_decision():
    with pytest.raises(ValidationError):
        ReviewDecision(decision="MAYBE")
