from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from .adapters import ReferenceAdapter
from .registry import TaskValidationError, load_tasks
from .runner import run_evaluation


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="lantora-eval")
    result.add_argument("--tasks", type=Path, default=Path("evaluations/tasks"))
    result.add_argument("--output", type=Path, help="new directory for the result bundle")
    result.add_argument("--seed", type=int, default=0)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    output = args.output or Path("runs") / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    try:
        tasks = load_tasks(args.tasks)
        _, results = run_evaluation(tasks, ReferenceAdapter(), output, seed=args.seed)
    except (OSError, ValueError, TaskValidationError) as exc:
        parser().error(str(exc))
    passed = sum(result["score"]["matched"] for result in results)
    print(f"Completed {len(results)} tasks: {passed} passed. Artifacts: {output}")
    return 0 if passed == len(results) else 1

