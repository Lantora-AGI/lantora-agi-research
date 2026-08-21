# Evaluations

Evaluations must state the capability dimension, task distribution, holdout policy, contamination checks, scoring method, uncertainty, compute budget, and known limitations. Avoid treating a single benchmark as evidence of general intelligence.

## Harness v0.1

The `lantora-eval` Python package loads versioned JSON tasks, executes them
through a narrow adapter interface, scores their outputs, and writes an
immutable result bundle. The included reference adapter is deterministic and
does not use a model, network, shell, or credentials.

Run it from the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --no-deps -e .
lantora-eval --output runs/example --seed 17
```

Task fixtures live in `evaluations/tasks/`. Their public JSON Schema is
`evaluations/schemas/task.schema.json`. Result and manifest schemas are in the
same directory.

Each successful bundle contains:

- `manifest.json`: source revision, versions, environment, seed, limits, hashes,
  retries, and exclusions;
- `results.json`: per-task outputs, hashes, scores, failures, steps, and timing;
- `report.md`: a short human-readable summary with an explicit interpretation
  warning.

See [threat model and limitations](threat-model.md) before adding adapters or
tasks.

## Stage 2 scientific pilot

The [pilot suite](pilot/README.md) adds deterministic generators for abstract
reasoning, learning and transfer, and planning. It separates control, transfer,
and harder conditions; validates ambiguity and satisfiability; supplies
transparent non-model baselines; and reports per-group Wilson intervals without
creating a composite AGI score.

The pilot contains public development machinery only. It does not include a
model integration or protected audit data.

## Adding a task

1. Start from one of the harmless fixtures in `evaluations/tasks/`.
2. Give the task a stable identifier and semantic version.
3. State its taxonomy family, deterministic scoring method, and limits.
4. Add tests for successful execution and relevant failure paths.
5. Document validity, contamination, and misuse considerations in the proposal.

The v0.1 registry accepts only the `exact_match` scorer. New scorers require a
reviewed interface change; do not encode executable code in task files.
