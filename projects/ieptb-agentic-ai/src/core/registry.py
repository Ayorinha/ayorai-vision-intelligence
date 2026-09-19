from dataclasses import dataclass
from enum import StrEnum
from typing import Callable, Any

class ToolRisk(StrEnum):
    LOW="low"; MEDIUM="medium"; HIGH="high"; CRITICAL="critical"

@dataclass(frozen=True)
class ToolSpec:
    name: str
    risk: ToolRisk
    permission: str
    side_effect: bool
    handler: Callable[[dict[str, Any]], Any]

class ToolRegistry:
    def __init__(self) -> None: self._tools: dict[str, ToolSpec] = {}
    def register(self, spec: ToolSpec) -> None: self._tools[spec.name] = spec
    def get(self, name: str) -> ToolSpec: return self._tools[name]
    def names(self) -> list[str]: return sorted(self._tools)
