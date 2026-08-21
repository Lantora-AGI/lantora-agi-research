# Evaluation harness threat model and limitations

## Trust boundaries

Task files, candidate-system outputs, and imported result bundles are untrusted
data. The reference adapter operates only on in-memory JSON values and does not
offer shell, filesystem, network, credential, or tool access to the evaluated
system. Result bundles are written only to a caller-selected new directory.

The harness currently invokes adapters in the evaluator process. Therefore,
third-party adapters are trusted Python code and are **not sandboxed**. Do not
install or run an unknown adapter. A future executable-system adapter must use
an independently reviewed isolation boundary before it can run untrusted code.

## Addressed risks

- Task definitions cannot embed executable Python code.
- The reference path needs no credentials or network access.
- Canonical SHA-256 hashes identify inputs and outputs.
- Existing result directories are never overwritten.
- Exceptions become explicit failed-task records rather than disappearing.
- CI receives read-only repository permissions.

## Known limitations

- The wall-clock limit is detected after an in-process adapter returns; it does
  not preempt a stalled or malicious adapter.
- Step counts are reported by the adapter and cannot yet be independently
  verified.
- Environment dependency inventories may contain unrelated packages installed
  in the active environment.
- Timestamps and measured durations intentionally differ between reruns. Output
  hashes and scores, rather than whole manifests, are the v0.1 equivalence
  criterion.
- JSON Schema files are published for interoperability, while the dependency-free
  runtime performs its own narrower validation.
- Public fixtures are susceptible to contamination and have no value as hidden
  tests.
- Exact-match scores do not measure uncertainty, robustness, calibration,
  social intelligence, safety, or general intelligence.

## Interpretation boundary

Passing the included fixtures demonstrates that the harness plumbing works. It
does not demonstrate AGI, model capability, alignment, or deployment readiness.
Any later scientific evaluation must preregister claims, baselines, uncertainty,
holdout controls, contamination analysis, safety review, and replication plans.

