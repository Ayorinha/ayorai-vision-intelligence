from dataclasses import dataclass, field
from .models import Decision, ProvenanceEvent

@dataclass
class ProvenanceGraph:
    events: list[ProvenanceEvent] = field(default_factory=list)
    def record(self, *, event_id, request_id, actor, agent_id, action, resource, decision, parent_event_id=None):
        event = ProvenanceEvent(event_id, request_id, actor, agent_id, action, resource, decision, parent_event_id)
        self.events.append(event)
        return event
    def chain(self, request_id):
        return [event for event in self.events if event.request_id == request_id]
