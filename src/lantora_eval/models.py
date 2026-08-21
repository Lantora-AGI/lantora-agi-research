from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


# Kept intentionally permissive at the Python type layer; task validation and
# published JSON Schemas define the serialized boundary.
JSONValue = Any


@dataclass(frozen=True)
class Task:
    task_id: str
    version: str
    family: str
    prompt: str
    operation: str
    input: JSONValue
    expected: JSONValue
    scorer: str
    limits: dict[str, int | float]
    condition: str = "infrastructure"
    budget: dict[str, JSONValue] = field(default_factory=dict)
    metadata: dict[str, JSONValue] = field(default_factory=dict)


@dataclass(frozen=True)
class AdapterResponse:
    output: JSONValue
    steps: int


class SystemAdapter(Protocol):
    name: str
    version: str

    def configuration(self) -> dict[str, JSONValue]: ...

    def run(self, task: Task, *, seed: int) -> AdapterResponse: ...
