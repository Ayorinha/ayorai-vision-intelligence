from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from src.core.database import init_db
from src.core.settings import settings
from src.mcp.registry import ToolRegistry
from src.mcp.tools import build_registry
from src.vision.models import Detection
from src.vision.tracker import TrackStore
from src.vision.confidence import classify_confidence
from src.vision.pipeline import VisionPipeline

app = FastAPI(title=settings.app_name, version="1.0.0")
store = TrackStore()
tools: ToolRegistry = build_registry(store)
init_db()

@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment, "version": "1.0.0"}

@app.get("/ready")
def ready():
    return {"ready": True, "model": settings.model_path}

@app.get("/tools")
def list_tools():
    return {"tools": tools.names()}

@app.post("/detections")
def add_detection(detection: Detection):
    store.add(detection)
    return {"accepted": True, "action": classify_confidence(detection.confidence)}

@app.get("/tracks")
def tracks():
    return [item.model_dump() for item in store.summary()]

@app.post("/process-video")
async def process_video(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "Missing filename")
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".mp4", ".mov", ".avi", ".mkv"}:
        raise HTTPException(415, "Unsupported video format")
    input_path = Path("data/input") / Path(file.filename).name
    output_path = Path("data/output") / f"{input_path.stem}_tracked.mp4"
    input_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    input_path.write_bytes(await file.read())
    summaries = VisionPipeline(settings.model_path).process(str(input_path), str(output_path))
    return {"status": "completed", "output": str(output_path), "tracks": [s.model_dump() for s in summaries]}

@app.get("/output/{filename}")
def output(filename: str):
    path = Path("data/output") / Path(filename).name
    if not path.exists():
        raise HTTPException(404, "Output not found")
    return FileResponse(path)
