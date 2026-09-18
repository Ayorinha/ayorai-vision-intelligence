from dataclasses import dataclass
from pathlib import Path

@dataclass
class IngestionResult:
    discovered: int
    accepted: int

def scan_input_directory(path: str = "data/input") -> IngestionResult:
    files = [
        p for p in Path(path).glob("*")
        if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".avi", ".mkv"}
    ]
    return IngestionResult(discovered=len(files), accepted=len(files))
