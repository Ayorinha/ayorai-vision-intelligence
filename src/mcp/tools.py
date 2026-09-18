from .registry import ToolRegistry
from ..vision.tracker import TrackStore

def build_registry(store: TrackStore) -> ToolRegistry:
    registry = ToolRegistry()

    registry.register("get_track_history", lambda track_id: [
        d.model_dump() for d in store._tracks.get(int(track_id), [])
    ])
    registry.register("get_track_summary", lambda: [
        item.model_dump() for item in store.summary()
    ])
    registry.register("get_low_confidence_events", lambda threshold=0.70: [
        d.model_dump()
        for detections in store._tracks.values()
        for d in detections
        if d.confidence < float(threshold)
    ])
    registry.register("export_annotations", lambda: {
        "status": "contract-ready",
        "message": "Connect this tool to the dataset/export service."
    })
    return registry
