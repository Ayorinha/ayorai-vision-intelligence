import pytest

from src.vision.models import Detection
from src.vision.tracker import TrackStore

def test_tracker_history_and_summary():
    store = TrackStore()
    store.add(Detection(frame=1, track_id=3, label="person", confidence=0.9, bbox=(0,0,1,1)))
    store.add(Detection(frame=2, track_id=3, label="person", confidence=0.8, bbox=(0,0,2,2)))
    assert len(store.history(3)) == 2
    assert store.summary()[0].frames_seen == 2
    assert store.summary()[0].mean_confidence == pytest.approx(0.85)
