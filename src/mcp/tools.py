from .registry import ToolRegistry
from ..vision.tracker import TrackStore
from ..core.repository import list_detections,list_reviews,decide_review,list_events,search_knowledge

def build_registry(store=None):
    registry=ToolRegistry()
    registry.register("get_track_history",lambda track_id:[d.model_dump() for d in (store.history(int(track_id)) if store else [])])
    registry.register("get_track_summary",lambda:[d.model_dump() for d in (store.summary() if store else [])])
    registry.register("get_low_confidence_events",lambda threshold=0.70:[d for d in list_detections() if d["confidence"]<float(threshold)])
    registry.register("get_review_queue",lambda:list_reviews("PENDING"))
    registry.register("get_events",lambda job_id=None:list_events(job_id))
    registry.register("search_knowledge",lambda query,top_k=5:search_knowledge(query,int(top_k)))
    registry.register("approve_review",lambda review_id,reviewer="human",final_label=None:decide_review(int(review_id),"APPROVED",reviewer,final_label))
    registry.register("reject_review",lambda review_id,reviewer="human",final_label=None:decide_review(int(review_id),"REJECTED",reviewer,final_label))
    registry.register("export_annotations",lambda job_id=None:{"format":"json","records":list_detections(job_id)})
    return registry
