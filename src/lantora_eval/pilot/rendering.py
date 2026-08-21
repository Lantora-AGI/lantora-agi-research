from __future__ import annotations

from typing import Any

from ..models import Task


def render_task(task: Task) -> dict[str, Any]:
    """Return the candidate-visible payload, excluding gold and private metadata."""

    return {
        "task_id": task.task_id,
        "family": task.family,
        "condition": task.condition,
        "instructions": task.prompt,
        "input": task.input,
        "budget": task.budget,
    }

