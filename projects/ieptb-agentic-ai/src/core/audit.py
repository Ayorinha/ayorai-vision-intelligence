from datetime import datetime, timezone
from hashlib import sha256
import json
from uuid import uuid4

def audit_event(event_type: str, payload: dict) -> dict:
    event={"id":str(uuid4()),"timestamp":datetime.now(timezone.utc).isoformat(),"type":event_type,"payload":payload}
    canonical=json.dumps(event, sort_keys=True, separators=(",",":")).encode()
    event["event_hash"]=sha256(canonical).hexdigest()
    return event
