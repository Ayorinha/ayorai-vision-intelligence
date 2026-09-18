# MCP Tool Contract

The initial registry exposes provider-neutral tool contracts:

- `get_track_history`
- `get_track_summary`
- `get_low_confidence_events`
- `export_annotations`

The registry is intentionally separated from the transport layer. A production MCP server can expose the same handlers through the selected MCP transport without coupling domain logic to the protocol implementation.
