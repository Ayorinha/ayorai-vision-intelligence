import pytest
from pydantic import ValidationError
from src.vision.models import Detection

def test_detection_accepts_valid_bbox():
    d = Detection(frame=1, track_id=7, label="person", confidence=0.95, bbox=(1,2,10,20))
    assert d.track_id == 7

def test_detection_rejects_invalid_bbox():
    with pytest.raises(ValidationError):
        Detection(frame=1, label="person", confidence=0.95, bbox=(10,2,1,20))
