from __future__ import annotations

from .models import JSONValue, Task


def score(task: Task, output: JSONValue) -> dict[str, JSONValue]:
    if task.scorer != "exact_match":
        raise ValueError(f"unsupported scorer: {task.scorer}")
    matched = output == task.expected
    return {"scorer": "exact_match", "score": 1.0 if matched else 0.0, "matched": matched}

