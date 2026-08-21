from __future__ import annotations

import importlib.metadata
import platform
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .artifacts import sha256, write_bundle
from .models import SystemAdapter, Task
from .scoring import score


def _git_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def _dependencies() -> list[str]:
    return sorted(f"{item.metadata['Name']}=={item.version}" for item in importlib.metadata.distributions())


def run_evaluation(
    tasks: list[Task], adapter: SystemAdapter, output_dir: Path, *, seed: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    random.seed(seed)
    started = datetime.now(timezone.utc)
    results: list[dict[str, Any]] = []
    for task in tasks:
        task_started = time.monotonic()
        status = "completed"
        error = None
        output = None
        steps = 0
        try:
            response = adapter.run(task, seed=seed)
            output, steps = response.output, response.steps
            elapsed = time.monotonic() - task_started
            if steps > task.limits["max_steps"]:
                raise RuntimeError("step budget exceeded")
            if elapsed > task.limits["max_seconds"]:
                raise TimeoutError("time budget exceeded")
            task_score = score(task, output)
        except Exception as exc:  # preserve task failures as data
            elapsed = time.monotonic() - task_started
            status, error = "failed", f"{type(exc).__name__}: {exc}"
            task_score = {"scorer": task.scorer, "score": 0.0, "matched": False}
        results.append(
            {
                "task_id": task.task_id,
                "task_version": task.version,
                "family": task.family,
                "status": status,
                "output": output,
                "output_sha256": sha256(output),
                "score": task_score,
                "steps": steps,
                "duration_seconds": round(elapsed, 6),
                "error": error,
            }
        )
    ended = datetime.now(timezone.utc)
    manifest = {
        "schema_version": "0.1.0",
        "harness_version": __version__,
        "repository_commit": _git_commit(),
        "started_at": started.isoformat(),
        "ended_at": ended.isoformat(),
        "duration_seconds": round((ended - started).total_seconds(), 6),
        "seed": seed,
        "adapter": {
            "name": adapter.name,
            "version": adapter.version,
            "configuration": adapter.configuration(),
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "architecture": platform.machine(),
            "dependencies": _dependencies(),
        },
        "task_count": len(tasks),
        "tasks": [
            {
                "task_id": task.task_id,
                "version": task.version,
                "scorer": task.scorer,
                "limits": task.limits,
                "input_sha256": sha256(task.input),
            }
            for task in tasks
        ],
        "results_sha256": sha256(results),
        "retries": 0,
        "exclusions": [],
    }
    write_bundle(output_dir, manifest, results)
    return manifest, results

