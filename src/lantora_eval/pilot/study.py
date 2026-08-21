from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any

from ..artifacts import sha256
from ..runner import run_evaluation
from .generators import generate_suite, write_suite


def run_seed_study(
    *,
    seeds: list[int],
    items_per_condition: int,
    adapter: Any,
    output: Path,
) -> dict[str, Any]:
    if len(seeds) < 5:
        raise ValueError("a seed study requires at least five distinct seeds")
    if len(set(seeds)) != len(seeds):
        raise ValueError("seed study seeds must be distinct")
    output.mkdir(parents=True, exist_ok=False)
    runs = []
    rates: dict[tuple[str, str], list[float]] = {}
    for seed in seeds:
        seed_root = output / f"seed-{seed}"
        tasks = generate_suite(seed, items_per_condition)
        generation = write_suite(tasks, seed_root / "suite", seed=seed)
        manifest, _ = run_evaluation(tasks, adapter, seed_root / "run", seed=seed)
        for group in manifest["grouped_statistics"]:
            rates.setdefault((group["family"], group["condition"]), []).append(
                group["success_rate"]
            )
        runs.append(
            {
                "seed": seed,
                "task_count": generation["task_count"],
                "generation_manifest_sha256": sha256(generation),
                "results_sha256": manifest["results_sha256"],
                "grouped_statistics": manifest["grouped_statistics"],
            }
        )
    variation = []
    for (family, condition), values in sorted(rates.items()):
        variation.append(
            {
                "family": family,
                "condition": condition,
                "seed_count": len(values),
                "mean_success_rate": statistics.fmean(values),
                "population_standard_deviation": statistics.pstdev(values),
                "minimum_success_rate": min(values),
                "maximum_success_rate": max(values),
            }
        )
    summary = {
        "schema_version": "0.1.0",
        "adapter": {"name": adapter.name, "version": adapter.version},
        "items_per_condition": items_per_condition,
        "seeds": seeds,
        "runs": runs,
        "seed_variation": variation,
        "interpretation": "No composite AGI score is calculated; results apply only to this generated distribution.",
    }
    (output / "study-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# Pilot multi-seed study",
        "",
        f"- Adapter: {adapter.name} {adapter.version}",
        f"- Seeds: {', '.join(map(str, seeds))}",
        f"- Items per family-condition per seed: {items_per_condition}",
        "",
        "No composite AGI score is calculated.",
        "",
        "| Family | Condition | Seeds | Mean | Population SD | Min | Max |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for item in variation:
        lines.append(
            f"| {item['family']} | {item['condition']} | {item['seed_count']} | "
            f"{item['mean_success_rate']:.3f} | {item['population_standard_deviation']:.3f} | "
            f"{item['minimum_success_rate']:.3f} | {item['maximum_success_rate']:.3f} |"
        )
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary

