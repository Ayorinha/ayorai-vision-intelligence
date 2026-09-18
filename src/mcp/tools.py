from .registry import ToolRegistry
from ..vision.tracker import TrackStore

def build_registry(store: TrackStore) -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("get_track_history", lambda track_id: [
        d.model_dump() for d in store.history(int(track_id))
    ])
    registry.register("get_track_summary", lambda: [
        item.model_dump() for item in store.summary()
    ])
    registry.register("get_low_confidence_events", lambda threshold=0.70: [
        d.model_dump() for d in store.low_confidence(float(threshold))
    ])
    registry.register("export_annotations", lambda: {
        "status": "available",
        "format": "json",
        "records": [
            d.model_dump()
            for detections in store._tracks.values()
            for d in detections
        ],
    })
    return registry
