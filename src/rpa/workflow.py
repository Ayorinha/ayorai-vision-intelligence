from dataclasses import dataclass
from pathlib import Path
from ..core.repository import create_job

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}

@dataclass
class IngestionResult:
    discovered: int
    accepted: int
    job_ids: list[str]

def scan_input_directory(path: str = "data/input") -> IngestionResult:
    files = [p for p in Path(path).glob("*") if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS]
    jobs = [create_job(p.name) for p in files]
    return IngestionResult(len(files), len(files), jobs)
