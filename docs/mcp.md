# MCP / Tool Architecture

## Protocol server

The project now includes a protocol-compliant MCP server in `src/mcp/server.py` using the official Python SDK and Streamable HTTP transport.

Exposed read-only tools:

- `get_track_summary`
- `get_low_confidence_events`
- `get_review_queue`
- `get_events`
- `search_knowledge`

## Safety boundary

The MCP surface intentionally does not expose `approve_review` or `reject_review`. Those are consequential operations and remain behind the application policy boundary, where explicit human approval and reviewer identity are required.

## Legacy HTTP gateway

`src/mcp/http_server.py` remains available as the lightweight application gateway for direct internal integration. It is separate from the standards-based MCP server.

## Run

```bash
python -m src.mcp.server
```

The server can be inspected with an MCP-compatible client or Inspector. The repository does not treat the Inspector as a production dependency.