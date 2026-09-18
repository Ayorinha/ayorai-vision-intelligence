# Tool / MCP architecture

The repository currently exposes a controlled HTTP tool gateway and a reusable ToolRegistry.

Available tools include:

- get_track_history
- get_track_summary
- get_low_confidence_events
- get_review_queue
- get_events
- search_knowledge
- approve_review
- reject_review
- export_annotations

This is intentionally described as a **tool gateway**, not as a claim of full MCP protocol compliance. A protocol-compliant MCP transport is a separate roadmap item.
