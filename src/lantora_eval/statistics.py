from __future__ import annotations

import math
from collections import defaultdict
from typing import Any


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total <= 0:
        return 0.0, 0.0
    proportion = successes / total
    denominator = 1 + z * z / total
    centre = (proportion + z * z / (2 * total)) / denominator
    margin = z * math.sqrt(
        proportion * (1 - proportion) / total + z * z / (4 * total * total)
    ) / denominator
    return max(0.0, centre - margin), min(1.0, centre + margin)


def grouped_summary(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for result in results:
        groups[(result["family"], result.get("condition", "infrastructure"))].append(result)
    summaries = []
    for (family, condition), items in sorted(groups.items()):
        successes = sum(bool(item["score"]["matched"]) for item in items)
        low, high = wilson_interval(successes, len(items))
        outcomes: dict[str, int] = defaultdict(int)
        for item in items:
            outcomes[item["score"].get("outcome", "invalid")] += 1
        summaries.append(
            {
                "family": family,
                "condition": condition,
                "successes": successes,
                "total": len(items),
                "success_rate": successes / len(items),
                "wilson_95": [low, high],
                "outcomes": dict(sorted(outcomes.items())),
            }
        )
    return summaries


def transfer_differences(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_family = {(group["family"], group["condition"]): group for group in groups}
    differences = []
    for family in sorted({group["family"] for group in groups}):
        control = by_family.get((family, "control"))
        transfer = by_family.get((family, "transfer"))
        if control and transfer:
            differences.append(
                {
                    "family": family,
                    "control_total": control["total"],
                    "transfer_total": transfer["total"],
                    "control_rate": control["success_rate"],
                    "transfer_rate": transfer["success_rate"],
                    "transfer_minus_control": transfer["success_rate"] - control["success_rate"],
                }
            )
    return differences
