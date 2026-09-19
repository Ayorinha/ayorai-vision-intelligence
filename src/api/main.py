from pathlib import Path
from datetime import UTC, datetime
import csv
import io
from fastapi import BackgroundTasks, FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from src.core.database import init_db, connect
from src.core.settings import settings
from src.core.repository import create_job,get_job,update_job,list_detections,list_reviews,decide_review,list_events,add_event,upsert_knowledge
from src.core.policy import POLICIES
from src.mcp.registry import ToolRegistry
from src.mcp.tools import build_registry
from src.rag.retrieval import Retriever
from src.agents.orchestrator import VisionOrchestrator
from src.vision.models import Detection,ReviewDecision
from src.vision.tracker import TrackStore
from src.vision.confidence import classify_confidence
from src.vision.pipeline import VisionPipeline

app=FastAPI(title=settings.app_name,version="2.1.0")
store=TrackStore(); tools:ToolRegistry=build_registry(store)
retriever=Retriever(); agent=VisionOrchestrator(tools,retriever)
init_db()

def run_job(job_id,input_path,output_path):
    update_job(job_id,"PROCESSING",started_at=datetime.now(UTC).isoformat(),progress=0)
    try:
        summaries=VisionPipeline(settings.model_path,job_id=job_id).process(str(input_path),str(output_path))
        update_job(job_id,"COMPLETED",output_path=str(output_path),progress=1,completed_at=datetime.now(UTC).isoformat())
        add_event(job_id,"job_completed",{"tracks":len(summaries)})
    except Exception as exc:
        update_job(job_id,"FAILED",error=str(exc),completed_at=datetime.now(UTC).isoformat())
        add_event(job_id,"job_failed",{"error":str(exc)})

@app.get("/health")
def health(): return {"status":"ok","environment":settings.environment,"version":"2.1.0"}

@app.get("/ready")
def ready(): return {"ready":True,"model":settings.model_path,"database":"sqlite"}

@app.get("/metrics")
def metrics():
    with connect() as db:
        jobs=db.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        detections=db.execute("SELECT COUNT(*) FROM detections").fetchone()[0]
        pending_reviews=db.execute("SELECT COUNT(*) FROM reviews WHERE status='PENDING'").fetchone()[0]
        events=db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    return {"jobs":jobs,"detections":detections,"pending_reviews":pending_reviews,"events":events}

@app.get("/tools")
def list_tools(): return {"tools":tools.names()}

@app.post("/detections")
def add_detection(detection:Detection):
    store.add(detection); return {"accepted":True,"action":classify_confidence(detection.confidence)}

@app.get("/tracks")
def tracks(): return [item.model_dump() for item in store.summary()]

@app.post("/jobs",status_code=202)
async def create_video_job(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename: raise HTTPException(400,"Missing filename")
    suffix=Path(file.filename).suffix.lower()
    if suffix not in {".mp4",".mov",".avi",".mkv"}: raise HTTPException(415,"Unsupported video format")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024: raise HTTPException(413,"Upload exceeds configured limit")
    safe_name=Path(file.filename).name; input_path=Path("data/input")/safe_name
    output_path=Path("data/output")/(input_path.stem+"_tracked.mp4")
    input_path.parent.mkdir(parents=True,exist_ok=True); output_path.parent.mkdir(parents=True,exist_ok=True)
    input_path.write_bytes(data); job_id=create_job(safe_name)
    background_tasks.add_task(run_job,job_id,input_path,output_path)
    return {"job_id":job_id,"status":"QUEUED"}

@app.get("/jobs/{job_id}")
def job(job_id):
    result=get_job(job_id)
    if not result: raise HTTPException(404,"Job not found")
    return result

@app.get("/jobs/{job_id}/detections")
def job_detections(job_id): return list_detections(job_id)

@app.get("/jobs/{job_id}/events")
def job_events(job_id): return list_events(job_id)

@app.get("/jobs/{job_id}/export.csv")
def export_csv(job_id):
    if not get_job(job_id): raise HTTPException(404,"Job not found")
    rows=list_detections(job_id)
    output=io.StringIO()
    fields=["id","frame","track_id","label","confidence","x1","y1","x2","y2","created_at"]
    writer=csv.DictWriter(output,fieldnames=fields); writer.writeheader()
    for row in rows: writer.writerow({k:row.get(k) for k in fields})
    return StreamingResponse(iter([output.getvalue()]),media_type="text/csv",
                             headers={"Content-Disposition":f"attachment; filename={job_id}.csv"})

@app.get("/reviews")
def reviews(status="PENDING"): return list_reviews(status)

@app.post("/reviews/{review_id}")
def review(review_id:int,decision:ReviewDecision):
    try: return decide_review(review_id,decision.decision,decision.reviewer,decision.final_label)
    except (KeyError,ValueError) as exc: raise HTTPException(400,str(exc))

@app.post("/knowledge")
def add_knowledge(source:str,content:str): return {"id":upsert_knowledge(source,content)}

@app.post("/agent/query")
def agent_query(query:str): return agent.answer(query)

@app.post("/mcp/call/{name}")
def mcp_call(name: str, arguments: dict | None = None):
    policy = POLICIES.get(name)
    if policy is None:
        raise HTTPException(404, "Tool not found")
    if not policy.read_only or policy.requires_human_approval:
        raise HTTPException(403, "Critical or state-changing tools must use the dedicated review workflow")
    try:
        return {"result": tools.call(name, **(arguments or {}))}
    except KeyError as exc:
        raise HTTPException(404, str(exc))

@app.get("/output/{filename}")
def output(filename:str):
    path=Path("data/output")/Path(filename).name
    if not path.exists(): raise HTTPException(404,"Output not found")
    return FileResponse(path)
