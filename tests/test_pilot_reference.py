from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "pilot_reference.py"
SPEC = importlib.util.spec_from_file_location("pilot_reference", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PilotReferenceTests(unittest.TestCase):
    def test_differences_accept_identical_values(self) -> None:
        self.assertEqual(MODULE.differences({"a": [1, 2]}, {"a": [1, 2]}), [])

    def test_differences_report_nested_value(self) -> None:
        self.assertEqual(
            MODULE.differences({"a": [1, 2]}, {"a": [1, 3]}),
            ["$.a[1]: 2 != 3"],
        )

    def test_canonical_result_excludes_duration_and_raw_output(self) -> None:
        result = {
            "task_id": "task",
            "task_version": "1",
            "family": "family",
            "condition": "control",
            "status": "completed",
            "output_sha256": "abc",
            "score": {"matched": True},
            "error": None,
            "steps": 1,
            "duration_seconds": 3.5,
            "output": "not retained",
        }
        canonical = MODULE.canonical_result(result)
        self.assertNotIn("duration_seconds", canonical)
        self.assertNotIn("output", canonical)
        self.assertEqual(canonical["output_sha256"], "abc")


if __name__ == "__main__":
    unittest.main()
