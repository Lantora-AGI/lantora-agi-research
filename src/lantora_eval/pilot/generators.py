from __future__ import annotations

import itertools
import json
import random
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable

from ..artifacts import sha256
from ..models import JSONValue, Task
from ..scoring import score
from . import GENERATOR_VERSION


CONDITIONS = ("control", "transfer", "harder")
FAMILIES = ("abstract-reasoning", "learning-transfer", "planning")
DEFAULT_BUDGET = {
    "max_input_units": 4096,
    "max_output_units": 512,
    "max_steps": 8,
    "max_seconds": 5,
    "allowed_tools": [],
    "memory": "task-only",
    "retries": 0,
    "samples": 1,
    "human_interventions": 0,
}


def _rotate(sequence: list[str]) -> list[str]:
    return sequence[1:] + sequence[:1]


def _reverse(sequence: list[str]) -> list[str]:
    return list(reversed(sequence))


def _swap_pairs(sequence: list[str]) -> list[str]:
    result = sequence[:]
    for index in range(0, len(result) - 1, 2):
        result[index], result[index + 1] = result[index + 1], result[index]
    return result


BASE_OPERATIONS: dict[str, Callable[[list[str]], list[str]]] = {
    "reverse": _reverse,
    "rotate_left": _rotate,
    "swap_pairs": _swap_pairs,
}


def operation_candidates(condition: str) -> dict[str, Callable[[list[str]], list[str]]]:
    if condition != "harder":
        return BASE_OPERATIONS
    result: dict[str, Callable[[list[str]], list[str]]] = {}
    for first_name, first in BASE_OPERATIONS.items():
        for second_name, second in BASE_OPERATIONS.items():
            if first_name == second_name:
                continue
            # These two operations commute for the even-length sequences used
            # by the pilot, so retaining both would make the latent rule label
            # unidentifiable even though their observable mapping is identical.
            if first_name == "swap_pairs" and second_name == "reverse":
                continue
            result[f"{first_name}+{second_name}"] = (
                lambda value, first=first, second=second: second(first(value))
            )
    return result


def infer_operation(demos: list[dict[str, Any]], condition: str) -> list[str]:
    matches = []
    for name, operation in operation_candidates(condition).items():
        if all(operation(item["input"]) == item["output"] for item in demos):
            matches.append(name)
    return matches


def _abstract_task(seed: int, index: int, condition: str) -> Task:
    rng = random.Random(f"abstract:{seed}:{index}:{condition}")
    candidates = operation_candidates(condition)
    rule_name = rng.choice(sorted(candidates))
    operation = candidates[rule_name]
    alphabet = list("ABCDEFGH")
    if condition == "transfer":
        alphabet = [f"symbol-{number}" for number in rng.sample(range(20, 99), 8)]
    demos: list[dict[str, Any]] = []
    for _ in range(20):
        value = rng.sample(alphabet, 6)
        demos.append({"input": value, "output": operation(value)})
        if infer_operation(demos, condition) == [rule_name]:
            break
    if infer_operation(demos, condition) != [rule_name]:
        raise ValueError("abstract generator failed to identify a unique rule")
    query = rng.sample(alphabet, 6)
    return _task(
        family="abstract-reasoning",
        condition=condition,
        seed=seed,
        index=index,
        operation="pilot_abstract",
        prompt="Infer the transformation from demonstrations and transform the query sequence.",
        task_input={"demonstrations": demos, "query": query},
        expected=operation(query),
        scorer="exact_match",
    )


Rule = tuple[str, tuple[str, ...]]


def learning_candidates(attributes: list[str], condition: str) -> list[Rule]:
    singles = [("single", (name,)) for name in attributes]
    if condition != "harder":
        return singles
    pairs = list(itertools.combinations(attributes, 2))
    return singles + [(kind, pair) for kind in ("and", "or") for pair in pairs]


def apply_rule(rule: Rule, values: dict[str, bool]) -> bool:
    kind, attributes = rule
    selected = [values[name] for name in attributes]
    if kind == "single":
        return selected[0]
    if kind == "and":
        return all(selected)
    if kind == "or":
        return any(selected)
    raise ValueError(f"unknown rule: {kind}")


def infer_learning_rule(demos: list[dict[str, Any]], condition: str) -> list[Rule]:
    attributes = sorted(demos[0]["attributes"])
    return [
        rule
        for rule in learning_candidates(attributes, condition)
        if all(apply_rule(rule, item["attributes"]) == item["label"] for item in demos)
    ]


def _learning_task(seed: int, index: int, condition: str) -> Task:
    rng = random.Random(f"learning:{seed}:{index}:{condition}")
    count = 4 if condition == "harder" else 3
    attributes = [f"feature_{number}" for number in range(count)]
    if condition == "transfer":
        attributes = [f"property_{number}" for number in rng.sample(range(10, 90), count)]
    candidates = learning_candidates(attributes, condition)
    rule = rng.choice(candidates)
    rows = []
    for values in itertools.product((False, True), repeat=count):
        mapping = dict(zip(attributes, values))
        rows.append({"attributes": mapping, "label": apply_rule(rule, mapping)})
    rng.shuffle(rows)
    demos: list[dict[str, Any]] = []
    query = None
    for possible_query in rows:
        possible_demos = [item for item in rows if item is not possible_query]
        selected: list[dict[str, Any]] = []
        for item in possible_demos:
            selected.append(item)
            if infer_learning_rule(selected, condition) == [rule]:
                break
        if infer_learning_rule(selected, condition) == [rule]:
            present_labels = {item["label"] for item in selected}
            if len(present_labels) == 1:
                opposite = next(
                    (item for item in possible_demos if item["label"] not in present_labels),
                    None,
                )
                if opposite is None:
                    continue
                selected.append(opposite)
            demos, query = selected, possible_query
            break
    if query is None:
        raise ValueError("learning generator failed to identify a unique rule")
    positives = sum(item["label"] for item in demos)
    if positives in {0, len(demos)}:
        raise ValueError("learning demonstrations are label-imbalanced")
    return _task(
        family="learning-transfer",
        condition=condition,
        seed=seed,
        index=index,
        operation="pilot_learning",
        prompt="Infer the classification rule from demonstrations and classify the query.",
        task_input={"demonstrations": demos, "query": query["attributes"]},
        expected=query["label"],
        scorer="exact_match",
    )


def topological_order(nodes: list[str], edges: list[list[str]]) -> list[str]:
    incoming = {node: set() for node in nodes}
    outgoing = {node: set() for node in nodes}
    for first, second in edges:
        if first not in incoming or second not in incoming or first == second:
            raise ValueError("malformed planning edge")
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
        raise ValueError("planning graph is unsatisfiable")
    return result


def _planning_task(seed: int, index: int, condition: str) -> Task:
    rng = random.Random(f"planning:{seed}:{index}:{condition}")
    count = 7 if condition == "harder" else 5
    names = [f"action_{number}" for number in range(count)]
    if condition == "transfer":
        names = [f"step_{number}" for number in rng.sample(range(10, 90), count)]
    hidden_order = rng.sample(names, len(names))
    edges: set[tuple[str, str]] = set()
    for left in range(len(hidden_order)):
        for right in range(left + 1, len(hidden_order)):
            if rng.random() < 0.28:
                edges.add((hidden_order[left], hidden_order[right]))
    for position in range(len(hidden_order) - 1):
        if not any(edge[0] == hidden_order[position] for edge in edges):
            edges.add((hidden_order[position], hidden_order[position + 1]))
    previous_plan = topological_order(names, [list(edge) for edge in sorted(edges)])
    changed_constraint = None
    if condition == "harder":
        # Add a non-cycling constraint that the prior canonical plan violates,
        # forcing an observable revision rather than a cosmetic input change.
        previous_positions = {node: position for position, node in enumerate(previous_plan)}
        choices = [
            (hidden_order[left], hidden_order[right])
            for left in range(len(hidden_order))
            for right in range(left + 1, len(hidden_order))
            if (hidden_order[left], hidden_order[right]) not in edges
            and previous_positions[hidden_order[left]] > previous_positions[hidden_order[right]]
        ]
        if not choices:
            raise ValueError("planning instance cannot force a plan revision")
        changed_constraint = rng.choice(choices)
        edges.add(changed_constraint)
    ordered_edges = [list(edge) for edge in sorted(edges)]
    oracle = topological_order(names, ordered_edges)
    task_input: dict[str, Any] = {"nodes": rng.sample(names, len(names)), "before": ordered_edges}
    if previous_plan and condition == "harder":
        task_input.update(
            {"previous_plan": previous_plan, "changed_constraint": list(changed_constraint or ())}
        )
    return _task(
        family="planning",
        condition=condition,
        seed=seed,
        index=index,
        operation="pilot_planning",
        prompt="Return a plan containing every action once and satisfying every before constraint.",
        task_input=task_input,
        expected=oracle,
        scorer="constraint_validity",
    )


def _task(
    *,
    family: str,
    condition: str,
    seed: int,
    index: int,
    operation: str,
    prompt: str,
    task_input: JSONValue,
    expected: JSONValue,
    scorer: str,
) -> Task:
    return Task(
        task_id=f"pilot-{family}-{condition}-{seed}-{index:04d}",
        version=GENERATOR_VERSION,
        family=family,
        condition=condition,
        prompt=prompt,
        operation=operation,
        input=task_input,
        expected=expected,
        scorer=scorer,
        limits={"max_seconds": 5, "max_steps": 8},
        budget=DEFAULT_BUDGET.copy(),
        metadata={"generator_version": GENERATOR_VERSION, "seed": seed, "item_index": index},
    )


GENERATORS = {
    "abstract-reasoning": _abstract_task,
    "learning-transfer": _learning_task,
    "planning": _planning_task,
}


def generate_suite(seed: int, items_per_condition: int) -> list[Task]:
    if items_per_condition <= 0:
        raise ValueError("items_per_condition must be positive")
    tasks: list[Task] = []
    seen_inputs: set[str] = set()
    for family in FAMILIES:
        for condition in CONDITIONS:
            accepted = 0
            candidate_index = 0
            while accepted < items_per_condition:
                if candidate_index >= items_per_condition * 100:
                    raise ValueError("generator could not produce enough unique task inputs")
                try:
                    task = GENERATORS[family](seed, candidate_index, condition)
                except ValueError:
                    candidate_index += 1
                    continue
                candidate_index += 1
                input_hash = sha256(task.input)
                if input_hash in seen_inputs:
                    continue
                seen_inputs.add(input_hash)
                tasks.append(task)
                accepted += 1
    if len({task.task_id for task in tasks}) != len(tasks):
        raise ValueError("generator produced duplicate task identifiers")
    validate_suite(tasks)
    return tasks


def validate_suite(tasks: list[Task]) -> None:
    for task in tasks:
        if task.family == "abstract-reasoning":
            matches = infer_operation(task.input["demonstrations"], task.condition)
            if len(matches) != 1:
                raise ValueError(f"{task.task_id}: abstract rule is ambiguous")
            expected = operation_candidates(task.condition)[matches[0]](task.input["query"])
            if expected != task.expected:
                raise ValueError(f"{task.task_id}: abstract oracle mismatch")
        elif task.family == "learning-transfer":
            demos = task.input["demonstrations"]
            if {item["label"] for item in demos} != {False, True}:
                raise ValueError(f"{task.task_id}: demonstrations are label-imbalanced")
            matches = infer_learning_rule(demos, task.condition)
            if len(matches) != 1:
                raise ValueError(f"{task.task_id}: learning rule is ambiguous")
            if apply_rule(matches[0], task.input["query"]) != task.expected:
                raise ValueError(f"{task.task_id}: learning oracle mismatch")
        elif task.family == "planning":
            oracle = topological_order(task.input["nodes"], task.input["before"])
            if not score(task, oracle)["matched"]:
                raise ValueError(f"{task.task_id}: planning oracle is invalid")
        else:
            raise ValueError(f"{task.task_id}: unsupported pilot family")


def write_suite(tasks: list[Task], directory: Path, *, seed: int) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=False)
    tasks_directory = directory / "tasks"
    tasks_directory.mkdir()
    entries = []
    for task in tasks:
        raw = asdict(task)
        path = tasks_directory / f"{task.task_id}.json"
        path.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        entries.append({"task_id": task.task_id, "sha256": sha256(raw)})
    manifest = {
        "generator_version": GENERATOR_VERSION,
        "seed": seed,
        "task_count": len(tasks),
        "tasks": entries,
    }
    (directory / "generation-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest
