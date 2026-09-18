from collections import defaultdict
from .models import Detection, TrackSummary

class TrackStore:
    """Thread-safe-in-practice in-memory store for one API process; use PostgreSQL for multi-worker production."""

    def __init__(self) -> None:
        self._tracks: dict[int, list[Detection]] = defaultdict(list)

    def add(self, detection: Detection) -> None:
        if detection.track_id is not None:
            self._tracks[detection.track_id].append(detection)

    def history(self, track_id: int) -> list[Detection]:
        return list(self._tracks.get(int(track_id), []))

    def low_confidence(self, threshold: float = 0.70) -> list[Detection]:
        return [
            d for detections in self._tracks.values()
            for d in detections if d.confidence < threshold
        ]

    def summary(self) -> list[TrackSummary]:
        result = []
        for track_id, detections in sorted(self._tracks.items()):
            labels = [d.label for d in detections]
            result.append(TrackSummary(
                track_id=track_id,
                label=max(set(labels), key=labels.count),
                first_frame=min(d.frame for d in detections),
                last_frame=max(d.frame for d in detections),
                frames_seen=len(detections),
                mean_confidence=sum(d.confidence for d in detections) / len(detections),
            ))
        return result
