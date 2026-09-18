from dataclasses import dataclass
from typing import Any

@dataclass
class AgentTask:
    objective: str
    tools: list[str]
    context: dict[str, Any]

class VisionOrchestrator:
    """Provider-neutral orchestration contract for an Astra-class reasoning layer."""

    def __init__(self, tool_registry, retriever) -> None:
        self.tools = tool_registry
        self.retriever = retriever

    def plan(self, objective: str) -> AgentTask:
        return AgentTask(
            objective=objective,
            tools=self.tools.names(),
            context={"rag": self.retriever.search(objective)},
        )
