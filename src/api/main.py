from fastapi import FastAPI
from src.mcp.registry import ToolRegistry
from src.mcp.tools import build_registry
from src.vision.models import Detection
from src.vision.tracker import TrackStore

app = FastAPI(title="AYORAI Vision Intelligence", version="0.1.0")
store = TrackStore()
tools: ToolRegistry = build_registry(store)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ayorai-vision-intelligence"}

@app.get("/tools")
def list_tools() -> dict[str, list[str]]:
    return {"tools": tools.names()}

@app.post("/detections")
def add_detection(detection: Detection) -> dict[str, object]:
    store.add(detection)
    return {"accepted": True, "action": "stored"}

@app.get("/tracks")
def tracks() -> list[dict]:
    return [item.model_dump() for item in store.summary()]
