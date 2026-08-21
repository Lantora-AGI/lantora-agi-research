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
        "These fixtures validate the harness; passing them is not evidence of AGI.",
        "",
        "| Task | Family | Score | Status |",
        "|---|---|---:|---|",
    ]
    for result in results:
        lines.append(
            f"| {result['task_id']} | {result['family']} | "
            f"{result['score']['score']:.1f} | {result['status']} |"
        )
    (directory / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

