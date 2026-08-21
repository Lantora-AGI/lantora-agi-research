from __future__ import annotations

import hashlib
import random
from typing import Any

from ..models import AdapterResponse, JSONValue, Task
from .generators import (
    apply_rule,
    infer_learning_rule,
    infer_operation,
    operation_candidates,
    topological_order,
)


class PilotOracleAdapter:
    name = "pilot-oracle"
    version = "0.1.0"
    trusted_gold_access = True

    def configuration(self) -> dict[str, JSONValue]:
        return {"network": False, "shell": False, "uses_gold_answers": True}

    def run(self, task: Task, *, seed: int) -> AdapterResponse:
        del seed
        if task.scorer == "constraint_validity":
            output = topological_order(task.input["nodes"], task.input["before"])
        else:
            output = task.expected
        return AdapterResponse(output=output, steps=1)


class PilotHeuristicAdapter:
    """Transparent enumerative and graph-algorithm baseline."""

    name = "pilot-heuristic"
    version = "0.1.0"

    def configuration(self) -> dict[str, JSONValue]:
        return {"network": False, "shell": False, "method": "enumerative-and-topological"}

    def run(self, task: Task, *, seed: int) -> AdapterResponse:
        del seed
        if task.operation == "pilot_abstract":
            matches = infer_operation(task.input["demonstrations"], task.condition)
            if len(matches) != 1:
                return AdapterResponse(output={"abstain": True}, steps=len(matches))
            output = operation_candidates(task.condition)[matches[0]](task.input["query"])
        elif task.operation == "pilot_learning":
            matches = infer_learning_rule(task.input["demonstrations"], task.condition)
            if len(matches) != 1:
                return AdapterResponse(output={"abstain": True}, steps=len(matches))
            output = apply_rule(matches[0], task.input["query"])
        elif task.operation == "pilot_planning":
            output = topological_order(task.input["nodes"], task.input["before"])
        else:
            raise ValueError(f"unsupported pilot operation: {task.operation}")
        return AdapterResponse(output=output, steps=1)


class PilotRandomAdapter:
    name = "pilot-random"
    version = "0.1.0"

    def configuration(self) -> dict[str, JSONValue]:
        return {"network": False, "shell": False, "method": "seeded-random"}

    def run(self, task: Task, *, seed: int) -> AdapterResponse:
        digest = hashlib.sha256(f"{seed}:{task.task_id}".encode()).hexdigest()
        rng = random.Random(int(digest[:16], 16))
        if task.operation == "pilot_abstract":
            output = rng.sample(task.input["query"], len(task.input["query"]))
        elif task.operation == "pilot_learning":
            output = bool(rng.getrandbits(1))
        elif task.operation == "pilot_planning":
            output = rng.sample(task.input["nodes"], len(task.input["nodes"]))
        else:
            raise ValueError(f"unsupported pilot operation: {task.operation}")
        return AdapterResponse(output=output, steps=1)


class PilotMajorityAdapter:
    """Learning-only majority-label baseline; abstains on other families."""

    name = "pilot-majority"
    version = "0.1.0"

    def configuration(self) -> dict[str, JSONValue]:
        return {"network": False, "shell": False, "method": "demonstration-majority"}

    def run(self, task: Task, *, seed: int) -> AdapterResponse:
        del seed
        if task.operation != "pilot_learning":
            return AdapterResponse(output={"abstain": True}, steps=0)
        labels = [item["label"] for item in task.input["demonstrations"]]
        output = sum(labels) > len(labels) / 2
        return AdapterResponse(output=output, steps=1)


ADAPTERS = {
    "oracle": PilotOracleAdapter,
    "heuristic": PilotHeuristicAdapter,
    "majority": PilotMajorityAdapter,
    "random": PilotRandomAdapter,
}
