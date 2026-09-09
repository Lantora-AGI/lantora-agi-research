# Independent replication runbook

This runbook is for an independent reproduction of the Stage 2 pilot suite.
It verifies deterministic generation, validation, scoring, and artifact
production. It does not evaluate an AGI system or establish that AGI exists.

Report the attempt in
[Issue #15](https://github.com/Lantora-AGI/lantora-agi-research/issues/15),
including failures and mismatches. Do not silently repair the primary run.

## Who qualifies

The primary reproducer must not have authored or modified the pilot generator,
scorers, adapters, tests, or the reference run. Prior familiarity with the
repository is acceptable if that independence condition is met.

## 1. Record the clean environment

Use a fresh clone and Python 3.12. Before installing or running the harness,
record the repository commit and platform details:

```bash
git clone https://github.com/Lantora-AGI/lantora-agi-research.git
cd lantora-agi-research
git rev-parse HEAD
git status --short
python3.12 --version
python3.12 -m pip --version
uname -a
```

On Windows, record `systeminfo` instead of `uname -a`. Save this terminal
output with the submission. The worktree must be clean before the primary run.

## 2. Install without modifying the source

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

If installation or tests fail, preserve the complete output before attempting
any fix. Report the original failure and every subsequent change separately.

## 3. Generate and validate the reference suite

Run these commands exactly once in a new `runs/replication-primary` directory:

```bash
lantora-pilot generate \
  --seed 13001 \
  --items-per-condition 50 \
  --output runs/replication-primary/pilot-13001

lantora-pilot validate \
  --tasks runs/replication-primary/pilot-13001/tasks
```

Expected console facts:

- generation reports 450 tasks;
- validation reports 450 valid pilot tasks;
- the generator refuses to overwrite the existing output directory.

Do not edit generated tasks, manifests, source files, or tests between
generation and evaluation.

## 4. Run the reference baselines

```bash
lantora-pilot evaluate \
  --tasks runs/replication-primary/pilot-13001/tasks \
  --adapter heuristic \
  --seed 17 \
  --output runs/replication-primary/heuristic

lantora-pilot evaluate \
  --tasks runs/replication-primary/pilot-13001/tasks \
  --adapter random \
  --seed 17 \
  --output runs/replication-primary/random
```

The reference expectations recorded in Issue #15 are 450/450 for the
heuristic adapter and 85/450 for the seeded random adapter. A different result
is evidence to report, not a result to adjust away.

## 5. Inventory and hash the artifacts

Create a sorted inventory and SHA-256 file list without changing the run:

```bash
find runs/replication-primary -type f -print | LC_ALL=C sort \
  > replication-files.txt

while IFS= read -r file; do
  shasum -a 256 "$file"
done < replication-files.txt > replication-sha256.txt
```

On Windows PowerShell, use `Get-ChildItem -Recurse -File` with
`Get-FileHash -Algorithm SHA256` and sort paths before saving the output.

Compare canonical task hashes, outcome classifications, scores, and grouped
statistics using the equivalence rules in
[the validation protocol](validation-protocol.md). Timestamps and measured
durations may differ, so whole-file hashes of timestamped manifests are an
inventory aid rather than the equivalence criterion.

## 6. Submit the evidence

Open a replication report using the repository's **Replication** issue
template and link it to Issue #15. Include:

- reproducer identity or stable GitHub handle and independence statement;
- operating system, architecture, Python and pip versions;
- exact repository commit SHA and clean-worktree evidence;
- complete install, test, generation, validation, and evaluation logs;
- `replication-files.txt` and `replication-sha256.txt`;
- generated manifests, baseline manifests, results, and reports;
- a table of every expected-versus-observed comparison;
- all errors, warnings, deviations, retries, and troubleshooting changes.

If artifact size prevents attaching the run bundle to GitHub, publish it in a
content-addressed archive or research repository and include its SHA-256 hash
and durable URL. Do not include credentials, personal data, restricted data,
model weights, or unrelated machine information.

## 7. Preserve discrepancies

When a mismatch occurs:

1. stop and copy the untouched primary output to read-only storage;
2. document the mismatch before debugging;
3. perform troubleshooting only in a separate clone or output directory;
4. report the primary result even if a later attempt succeeds;
5. do not describe Stage 2 as complete until maintainers review the evidence.

Stage 3 planning may continue, but baseline results do not become milestone
evidence until the Stage 2 exit gate is independently satisfied.
