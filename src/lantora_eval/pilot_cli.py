from __future__ import annotations

import argparse
from pathlib import Path

from .pilot.adapters import ADAPTERS
from .pilot.generators import generate_suite, validate_suite, write_suite
from .pilot.study import run_seed_study
from .registry import load_tasks
from .runner import run_evaluation


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="lantora-pilot")
    commands = result.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("generate", help="generate a deterministic pilot suite")
    generate.add_argument("--seed", type=int, required=True)
    generate.add_argument("--items-per-condition", type=int, default=50)
    generate.add_argument("--output", type=Path, required=True)
    evaluate = commands.add_parser("evaluate", help="run a generated pilot suite")
    evaluate.add_argument("--tasks", type=Path, required=True)
    evaluate.add_argument("--adapter", choices=sorted(ADAPTERS), default="heuristic")
    evaluate.add_argument("--seed", type=int, default=0)
    evaluate.add_argument("--output", type=Path, required=True)
    validate = commands.add_parser("validate", help="validate generated pilot tasks")
    validate.add_argument("--tasks", type=Path, required=True)
    study = commands.add_parser("study", help="run and summarize at least five seeds")
    study.add_argument("--seeds", type=int, nargs="+", required=True)
    study.add_argument("--items-per-condition", type=int, default=50)
    study.add_argument("--adapter", choices=sorted(ADAPTERS), default="heuristic")
    study.add_argument("--output", type=Path, required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        if arguments.command == "generate":
            tasks = generate_suite(arguments.seed, arguments.items_per_condition)
            manifest = write_suite(tasks, arguments.output, seed=arguments.seed)
            print(f"Generated {manifest['task_count']} tasks in {arguments.output}")
            return 0
        if arguments.command == "study":
            adapter = ADAPTERS[arguments.adapter]()
            summary = run_seed_study(
                seeds=arguments.seeds,
                items_per_condition=arguments.items_per_condition,
                adapter=adapter,
                output=arguments.output,
            )
            print(f"Completed {len(summary['seeds'])}-seed study in {arguments.output}")
            return 0
        tasks = load_tasks(arguments.tasks)
        if arguments.command == "validate":
            validate_suite(tasks)
            print(f"Validated {len(tasks)} pilot tasks")
            return 0
        adapter = ADAPTERS[arguments.adapter]()
        _, results = run_evaluation(tasks, adapter, arguments.output, seed=arguments.seed)
        successes = sum(result["score"]["matched"] for result in results)
        print(f"Completed {len(results)} tasks: {successes} passed. Artifacts: {arguments.output}")
        return 0
    except (OSError, ValueError) as exc:
        parser().error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
