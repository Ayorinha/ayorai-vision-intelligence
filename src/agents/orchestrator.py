from dataclasses import dataclass
from typing import Any

from .providers import OpenAICompatibleProvider

@dataclass
class AgentTask:
    objective: str
    tools: list[str]
    context: dict[str, Any]

class VisionOrchestrator:
    """Evidence-first orchestration with an optional private/OpenAI-compatible provider."""
    def __init__(self, tool_registry, retriever, provider=None) -> None:
        self.tools = tool_registry
        self.retriever = retriever
        self.provider = provider or OpenAICompatibleProvider()

    def plan(self, objective: str) -> AgentTask:
        return AgentTask(
            objective=objective,
            tools=self.tools.names(),
            context={"rag": self.retriever.search(objective)},
        )

    def answer(self, objective: str) -> dict:
        task = self.plan(objective)
        evidence = [c.__dict__ for c in task.context["rag"]]
        result = {
            "objective": objective,
            "evidence": evidence,
            "available_tools": task.tools,
            "mode": "deterministic-orchestration",
        }
        if not self.provider.configured:
            result["note"] = "No external LLM configured; reasoning remains deterministic and evidence-first."
            return result
        completion = self.provider.generate([
            {"role": "system", "content": "Answer only from supplied evidence. Never authorize tools."},
            {"role": "user", "content": f"Objective: {objective}\nEvidence: {evidence}"},
        ])
        result["mode"] = "llm-assisted-evidence-first"
        result["model_response"] = completion
        return result