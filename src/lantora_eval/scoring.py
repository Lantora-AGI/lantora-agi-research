from __future__ import annotations

from .models import JSONValue, Task


def score(task: Task, output: JSONValue) -> dict[str, JSONValue]:
    if isinstance(output, dict) and output.get("abstain") is True:
        return {"scorer": task.scorer, "score": 0.0, "matched": False, "outcome": "abstained"}
    if task.scorer == "exact_match":
        matched = output == task.expected
        return {
            "scorer": "exact_match",
            "score": 1.0 if matched else 0.0,
            "matched": matched,
            "outcome": "correct" if matched else "incorrect",
        }
    if task.scorer == "constraint_validity":
        matched, violations = _valid_plan(task.input, output)
        return {
            "scorer": "constraint_validity",
            "score": 1.0 if matched else 0.0,
            "matched": matched,
            "outcome": "correct" if matched else "incorrect",
            "violations": violations,
        }
    raise ValueError(f"unsupported scorer: {task.scorer}")


def _valid_plan(task_input: JSONValue, output: JSONValue) -> tuple[bool, list[str]]:
    if not isinstance(task_input, dict) or not isinstance(output, list):
        return False, ["plan must be a list"]
    nodes = task_input.get("nodes", [])
    before = task_input.get("before", [])
    violations: list[str] = []
    if len(output) != len(nodes) or set(output) != set(nodes):
        violations.append("plan must contain every node exactly once")
        return False, violations
    positions = {node: index for index, node in enumerate(output)}
    for first, second in before:
        if positions[first] >= positions[second]:
            violations.append(f"{first} must precede {second}")
    return not violations, violations
