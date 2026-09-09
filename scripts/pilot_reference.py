#!/usr/bin/env python3
"""Build or compare deterministic Stage 2 pilot reference data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def canonical_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": result["task_id"],
        "task_version": result["task_version"],
        "family": result["family"],
        "condition": result["condition"],
        "status": result["status"],
        "output_sha256": result["output_sha256"],
        "score": result["score"],
        "error": result["error"],
        "steps": result["steps"],
    }


def canonical_run(manifest: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "adapter": manifest["adapter"],
        "seed": manifest["seed"],
        "task_count": manifest["task_count"],
        "exclusions": manifest["exclusions"],
        "retries": manifest["retries"],
        "grouped_statistics": manifest["grouped_statistics"],
        "transfer_differences": manifest["transfer_differences"],
        "results": [canonical_result(item) for item in results],
    }


def build_reference(arguments: argparse.Namespace) -> dict[str, Any]:
    generation = load(arguments.generation_manifest)
    heuristic_manifest = load(arguments.heuristic_manifest)
    random_manifest = load(arguments.random_manifest)
    return {
        "reference_schema_version": "1.0.0",
        "status": "retroactively-published-maintainer-reference",
        "source_commit": arguments.source_commit,
        "publication_date": arguments.publication_date,
        "equivalence_excludes": [
            "timestamps",
            "durations",
            "platform strings",
            "environment inventories",
            "whole-file hashes containing excluded fields",
        ],
        "generation": {
            "generator_version": generation["generator_version"],
            "seed": generation["seed"],
            "task_count": generation["task_count"],
            "tasks": generation["tasks"],
        },
        "runs": {
            "heuristic": canonical_run(heuristic_manifest, load(arguments.heuristic_results)),
            "random": canonical_run(random_manifest, load(arguments.random_results)),
        },
    }


def differences(expected: Any, observed: Any, path: str = "$", limit: int = 100) -> list[str]:
    found: list[str] = []
    if type(expected) is not type(observed):
        return [f"{path}: type {type(expected).__name__} != {type(observed).__name__}"]
    if isinstance(expected, dict):
        for key in sorted(set(expected) | set(observed)):
            if len(found) >= limit:
                break
            if key not in expected:
                found.append(f"{path}.{key}: unexpected")
            elif key not in observed:
                found.append(f"{path}.{key}: missing")
            else:
                found.extend(differences(expected[key], observed[key], f"{path}.{key}", limit - len(found)))
    elif isinstance(expected, list):
        if len(expected) != len(observed):
            found.append(f"{path}: length {len(expected)} != {len(observed)}")
        for index, (left, right) in enumerate(zip(expected, observed)):
            if len(found) >= limit:
                break
            found.extend(differences(left, right, f"{path}[{index}]", limit - len(found)))
    elif expected != observed:
        found.append(f"{path}: {expected!r} != {observed!r}")
    return found[:limit]


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subcommands = result.add_subparsers(dest="command", required=True)
    for name in ("build", "compare"):
        command = subcommands.add_parser(name)
        command.add_argument("--generation-manifest", type=Path, required=True)
        command.add_argument("--heuristic-manifest", type=Path, required=True)
        command.add_argument("--heuristic-results", type=Path, required=True)
        command.add_argument("--random-manifest", type=Path, required=True)
        command.add_argument("--random-results", type=Path, required=True)
        command.add_argument("--source-commit", default="8adf28a42715f0e4de51e75e8cd943269de32e1b")
        command.add_argument("--publication-date", default="2026-09-08")
    subcommands.choices["build"].add_argument("--output", type=Path, required=True)
    subcommands.choices["compare"].add_argument("--reference", type=Path, required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    observed = build_reference(arguments)
    if arguments.command == "build":
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(json.dumps(observed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote canonical reference to {arguments.output}")
        return 0
    mismatches = differences(load(arguments.reference), observed)
    if mismatches:
        print(f"Reference mismatch ({len(mismatches)} shown):")
        for mismatch in mismatches:
            print(f"- {mismatch}")
        return 1
    print("Reference matches all canonical fields.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
