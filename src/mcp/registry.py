from collections.abc import Callable
from typing import Any

from src.core.policy import authorize_tool

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, handler: Callable[..., Any]) -> None:
        self._tools[name] = handler

    def call(self, name: str, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        authorize_tool(name, kwargs)
        return self._tools[name](**kwargs)

    def names(self) -> list[str]:
        return sorted(self._tools)