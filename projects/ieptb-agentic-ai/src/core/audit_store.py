import json
from pathlib import Path
from threading import Lock
from typing import Any

class AuditStore:
    """Append-only JSONL audit store with a hash chain for tamper evidence."""
    def __init__(self, path: str = "data/audit/events.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        from hashlib import sha256
        with self._lock:
            previous = "GENESIS"
            if self.path.exists():
                lines = self.path.read_text(encoding="utf-8").splitlines()
                if lines:
                    previous = json.loads(lines[-1])["hash"]
            payload = {**event, "previous_hash": previous}
            payload["hash"] = sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(payload, sort_keys=True) + "\n")
            return payload
