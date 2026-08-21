from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def write_bundle(directory: Path, manifest: dict[str, Any], results: list[dict[str, Any]]) -> None:
    directory.mkdir(parents=True, exist_ok=False)
    (directory / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (directory / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    passed = sum(result["score"]["matched"] for result in results)
    lines = [
        "# Lantora evaluation run",
        "",
        f"- Adapter: {manifest['adapter']['name']} {manifest['adapter']['version']}",
        f"- Seed: {manifest['seed']}",
        f"- Tasks passed: {passed}/{len(results)}",
        "",
        "Results describe only the tested task distribution; passing is not evidence of AGI.",
        "",
        "| Task | Family | Score | Status |",
        "|---|---|---:|---|",
    ]
    for result in results:
        lines.append(
            f"| {result['task_id']} | {result['family']} | "
            f"{result['score']['score']:.1f} | {result['status']} |"
        )
    grouped = manifest.get("grouped_statistics", [])
    if grouped:
        lines.extend(
            [
                "",
                "## Family and condition results",
                "",
                "No composite AGI score is calculated.",
                "",
                "| Family | Condition | Success | Rate | 95% Wilson interval |",
                "|---|---|---:|---:|---:|",
            ]
        )
        for group in grouped:
            low, high = group["wilson_95"]
            lines.append(
                f"| {group['family']} | {group['condition']} | "
                f"{group['successes']}/{group['total']} | {group['success_rate']:.3f} | "
                f"[{low:.3f}, {high:.3f}] |"
            )
    differences = manifest.get("transfer_differences", [])
    if differences:
        lines.extend(
            [
                "",
                "## Control-to-transfer differences",
                "",
                "| Family | Control n | Transfer n | Transfer minus control |",
                "|---|---:|---:|---:|",
            ]
        )
        for difference in differences:
            lines.append(
                f"| {difference['family']} | {difference['control_total']} | "
                f"{difference['transfer_total']} | {difference['transfer_minus_control']:+.3f} |"
            )
    (directory / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
