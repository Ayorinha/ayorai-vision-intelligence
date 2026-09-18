from collections import defaultdict
from .models import Detection, TrackSummary

class TrackStore:
    """Minimal persistent-ID store; replaceable by a production MOT implementation."""

    def __init__(self) -> None:
        self._tracks: dict[int, list[Detection]] = defaultdict(list)

    def add(self, detection: Detection) -> None:
        if detection.track_id is not None:
            self._tracks[detection.track_id].append(detection)

    def summary(self) -> list[TrackSummary]:
        result = []
        for track_id, detections in sorted(self._tracks.items()):
            result.append(
                TrackSummary(
                    track_id=track_id,
                    label=max(set(d.label for d in detections), key=[d.label for d in detections].count),
                    first_frame=min(d.frame for d in detections),
                    last_frame=max(d.frame for d in detections),
                    frames_seen=len(detections),
                    mean_confidence=sum(d.confidence for d in detections) / len(detections),
                )
            )
        return result
