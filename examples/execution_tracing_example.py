"""Execution tracing example for the AI Shield deterministic decision pipeline.

Walks three synthetic agent requests through the same pipeline the MCP tool
gateway and API use: policy evaluation (`ShieldEngine.evaluate`), the
resulting tool decision (`PolicyResult`), and the tamper-evident audit/trace
output (`ProvenanceGraph`). All data is synthetic, everything runs in
memory, and no network calls or credentials are involved.

Run it directly:

    python -m examples.execution_tracing_example

See docs/execution-tracing-example.md for the documented expected output.
"""
from __future__ import annotations

from ai_shield.engine import ShieldEngine
from ai_shield.models import AgentRequest, Classification, Identity

SCENARIOS: list[tuple[str, AgentRequest]] = [
    (
        "allowed read-only operation",
        AgentRequest(
            request_id="trace-demo-001",
            identity=Identity("synthetic-analyst-01", "analyst", 90),
            agent_id="agent-vision-01",
            capability="read_internal",
            resource="synthetic-report-01",
            classification=Classification.INTERNAL,
        ),
    ),
    (
        "consequential operation pending human review",
        AgentRequest(
            request_id="trace-demo-002",
            identity=Identity("synthetic-senior-analyst-01", "senior_analyst", 95),
            agent_id="agent-vision-01",
            capability="read_restricted",
            resource="synthetic-record-02",
            classification=Classification.RESTRICTED,
        ),
    ),
    (
        "unknown capability denied",
        AgentRequest(
            request_id="trace-demo-003",
            identity=Identity("synthetic-analyst-01", "analyst", 90),
            agent_id="agent-vision-01",
            capability="export_ledger",
            resource="synthetic-report-01",
            classification=Classification.INTERNAL,
        ),
    ),
]


def run() -> list[dict]:
    """Evaluate each scenario and return its decision plus audit trail."""
    engine = ShieldEngine()
    trace = []
    for label, request in SCENARIOS:
        result = engine.evaluate(request)
        events = engine.provenance.chain(request.request_id)
        trace.append(
            {
                "scenario": label,
                "request_id": request.request_id,
                "capability": request.capability,
                "decision": result.decision.value,
                "reason": result.reason,
                "controls": result.controls,
                "audit_events": [
                    {
                        "event_id": e.event_id,
                        "decision": e.decision.value,
                        "previous_hash": e.previous_hash,
                        "event_hash": e.event_hash,
                    }
                    for e in events
                ],
            }
        )
    return trace


def main() -> None:
    for entry in run():
        print(f"scenario: {entry['scenario']}")
        print(f"  capability={entry['capability']!r}")
        print(f"  decision={entry['decision']} reason={entry['reason']} controls={entry['controls']}")
        for event in entry["audit_events"]:
            print(
                f"  audit_event id={event['event_id']} decision={event['decision']} "
                f"event_hash={event['event_hash'][:12]}... previous_hash="
                f"{(event['previous_hash'] or 'none')[:12]}"
            )
        print()


if __name__ == "__main__":
    main()
