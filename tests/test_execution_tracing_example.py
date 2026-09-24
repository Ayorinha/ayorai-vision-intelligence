from ai_shield.models import Decision
from examples.execution_tracing_example import run


def test_execution_tracing_example_covers_allow_review_and_block():
    trace = run()
    decisions = {entry["scenario"]: entry["decision"] for entry in trace}

    assert decisions["allowed read-only operation"] == Decision.ALLOW.value
    assert decisions["consequential operation pending human review"] == Decision.REVIEW.value
    assert decisions["unknown capability denied"] == Decision.BLOCK.value


def test_execution_tracing_example_records_a_chained_audit_event_per_scenario():
    trace = run()

    for entry in trace:
        events = entry["audit_events"]
        assert len(events) == 1
        assert events[0]["decision"] == entry["decision"]
        assert events[0]["event_hash"]
