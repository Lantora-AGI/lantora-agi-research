# Validation-seed and reproduction protocol

## Partitions

- **Development:** seeds listed in `public-seeds.json`. They may be inspected,
  debugged against, and used in CI. They are never held-out evidence.
- **Validation:** five seeds sampled from the documented integer range only
  after the candidate system, prompt, adapter, budget, and analysis plan are
  frozen in a preregistration commit.
- **Audit:** future protected cases governed separately. This repository
  contains no audit seeds or tasks.

## Validation seed selection

1. Record the frozen repository commit and configuration.
2. Obtain a public, timestamped source of unpredictable bytes chosen in advance
   (for example, a future public randomness beacon).
3. Record the source, timestamp, and raw value before generating tasks.
4. Hash the raw value with SHA-256 and deterministically map successive digest
   blocks into the inclusive range in `public-seeds.json`.
5. Reject duplicates and development seeds until five seeds are obtained.
6. Commit only the selection record and resulting run manifests after the run;
   do not relabel exposed validation results as confirmatory after tuning.

This procedure is specified now but is not executed until a candidate
configuration exists. Inventing validation seeds during development would turn
them into development data.

## Equivalence criterion

For the same repository commit, generator version, configuration, and seed, an
independent reproduction must have identical canonical task hashes, oracle
answers or accepted-solution validity, outcome classifications, scores, and
grouped statistics. Timestamps and measured durations may differ.

The reproducer should use a clean environment, follow the documented commands,
publish the generation and run manifests, and disclose platform differences.

