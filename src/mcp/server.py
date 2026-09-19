from mcp.server import MCPServer

from src.mcp.registry import ToolRegistry
from src.mcp.tools import build_registry

mcp = MCPServer("AYORAI Secure Tool Server")
registry: ToolRegistry = build_registry()

def _call(name: str, **arguments):
    return registry.call(name, **arguments)

@mcp.tool()
def get_track_summary() -> list[dict]:
    """Read current tracked-object summaries."""
    return _call("get_track_summary")

@mcp.tool()
def get_low_confidence_events(threshold: float = 0.70) -> list[dict]:
    """Read detections below a deterministic confidence threshold."""
    return _call("get_low_confidence_events", threshold=threshold)

@mcp.tool()
def get_review_queue() -> list[dict]:
    """Read pending human-review items."""
    return _call("get_review_queue")

@mcp.tool()
def get_events(job_id: str | None = None) -> list[dict]:
    """Read auditable job events."""
    return _call("get_events", job_id=job_id)

@mcp.tool()
def search_knowledge(query: str, top_k: int = 5) -> list[dict]:
    """Retrieve evidence from the local knowledge base."""
    return _call("search_knowledge", query=query, top_k=top_k)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")