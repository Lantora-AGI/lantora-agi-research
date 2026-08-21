from __future__ import annotations

from typing import Any

from .models import AdapterResponse, JSONValue, Task


class ReferenceAdapter:
    """Deterministic, no-network adapter for exercising the harness."""

    name = "reference"
    version = "0.1.0"

    def configuration(self) -> dict[str, JSONValue]:
        return {"network": False, "shell": False, "deterministic": True}

    def run(self, task: Task, *, seed: int) -> AdapterResponse:
        del seed
        operations = {
            "sort_records": self._sort_records,
            "apply_rules": self._apply_rules,
            "topological_order": self._topological_order,
        }
        try:
            output = operations[task.operation](task.input)
        except KeyError as exc:
            raise ValueError(f"unsupported operation: {task.operation}") from exc
        return AdapterResponse(output=output, steps=1)

    @staticmethod
    def _sort_records(value: JSONValue) -> JSONValue:
        if not isinstance(value, dict) or not isinstance(value.get("records"), list):
            raise ValueError("sort_records requires a records list")
        records = value["records"]
        return sorted(records, key=lambda row: (row["priority"], row["name"]))

    @staticmethod
    def _apply_rules(value: JSONValue) -> JSONValue:
        if not isinstance(value, dict):
            raise ValueError("apply_rules requires an object")
        facts = set(value.get("facts", []))
        rules = value.get("rules", [])
        changed = True
        while changed:
            changed = False
            for rule in rules:
                if set(rule["if"]).issubset(facts) and rule["then"] not in facts:
                    facts.add(rule["then"])
                    changed = True
        return sorted(facts)

    @staticmethod
    def _topological_order(value: JSONValue) -> JSONValue:
        if not isinstance(value, dict):
            raise ValueError("topological_order requires an object")
        nodes = sorted(value.get("nodes", []))
        edges = value.get("before", [])
        incoming = {node: set() for node in nodes}
        outgoing = {node: set() for node in nodes}
        for first, second in edges:
            incoming[second].add(first)
            outgoing[first].add(second)
        ready = sorted(node for node in nodes if not incoming[node])
        result: list[str] = []
        while ready:
            node = ready.pop(0)
            result.append(node)
            for following in sorted(outgoing[node]):
                incoming[following].remove(node)
                if not incoming[following]:
                    ready.append(following)
                    ready.sort()
        if len(result) != len(nodes):
            raise ValueError("planning graph contains a cycle")
        return result

