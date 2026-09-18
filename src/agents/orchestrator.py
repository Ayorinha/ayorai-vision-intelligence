from dataclasses import dataclass
from typing import Any

@dataclass
class AgentTask:
    objective: str
    tools: list[str]
    context: dict[str, Any]

class VisionOrchestrator:
    """Evidence-first orchestration boundary for local/private LLM adapters."""
    def __init__(self, tool_registry, retriever) -> None:
        self.tools = tool_registry
        self.retriever = retriever

    def plan(self, objective: str) -> AgentTask:
        return AgentTask(objective=objective, tools=self.tools.names(),
                         context={"rag": self.retriever.search(objective)})

    def answer(self, objective: str) -> dict:
        task = self.plan(objective)
        return {
            "objective": objective,
            "evidence": [c.__dict__ for c in task.context["rag"]],
            "available_tools": task.tools,
            "mode": "deterministic-orchestration",
            "note": "Attach a local/private LLM adapter for natural-language reasoning."
        }
