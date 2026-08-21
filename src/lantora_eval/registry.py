from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Task


class TaskValidationError(ValueError):
    pass


REQUIRED_FIELDS = {
    "task_id",
    "version",
    "family",
    "prompt",
    "operation",
    "input",
    "expected",
    "scorer",
    "limits",
}


def _validate(raw: Any, path: Path) -> Task:
    if not isinstance(raw, dict):
        raise TaskValidationError(f"{path}: task must be a JSON object")
    missing = REQUIRED_FIELDS - raw.keys()
    unknown = raw.keys() - REQUIRED_FIELDS
    if missing or unknown:
        raise TaskValidationError(
            f"{path}: missing={sorted(missing)} unknown={sorted(unknown)}"
        )
    for field in ("task_id", "version", "family", "prompt", "operation", "scorer"):
        if not isinstance(raw[field], str) or not raw[field].strip():
            raise TaskValidationError(f"{path}: {field} must be a non-empty string")
    limits = raw["limits"]
    if not isinstance(limits, dict) or set(limits) != {"max_seconds", "max_steps"}:
        raise TaskValidationError(f"{path}: limits must contain max_seconds and max_steps")
    if not isinstance(limits["max_seconds"], (int, float)) or limits["max_seconds"] <= 0:
        raise TaskValidationError(f"{path}: max_seconds must be positive")
    if not isinstance(limits["max_steps"], int) or limits["max_steps"] <= 0:
        raise TaskValidationError(f"{path}: max_steps must be a positive integer")
    if raw["scorer"] != "exact_match":
        raise TaskValidationError(f"{path}: unsupported scorer {raw['scorer']!r}")
    return Task(**raw)


def load_tasks(directory: Path) -> list[Task]:
    paths = sorted(directory.glob("*.json"))
    if not paths:
        raise TaskValidationError(f"no task files found in {directory}")
    tasks = [_validate(json.loads(path.read_text(encoding="utf-8")), path) for path in paths]
    identities = [(task.task_id, task.version) for task in tasks]
    if len(identities) != len(set(identities)):
        raise TaskValidationError("task_id and version pairs must be unique")
    return tasks

