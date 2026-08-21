# Research Roadmap

Timelines are planning estimates, not predictions of AGI.

## Stage 1 — Operationalize the target

Define breadth, transfer, learning efficiency, long-horizon autonomy, robustness, uncertainty, and safety. Record explicit non-goals and stop conditions.

Exit gate: success criteria and a threat model exist before capability experiments begin.

## Stage 2 — Build the evaluator

Create held-out task families, contamination controls, immutable logs, inference and training budgets, and reproducible scoring.

Exit gate: an independent contributor can reproduce evaluation results.

## Stage 3 — Establish baselines

Evaluate capable open systems and document failure modes, human interventions, cost, variance, and reliability as task horizons increase.

Exit gate: baselines are reproducible within a declared tolerance.

## Stage 4 — Select a bottleneck

Rank failures by frequency, severity, generality, and tractability. Select one falsifiable mechanism.

Exit gate: the proposed mechanism predicts an observable result that differs from credible alternatives.

## Stage 5 — Run controlled architectural research

Potential research areas include hierarchical planning, typed memory, continual learning, world models, metacognition, and tool learning.

Exit gate: improvements survive ablation and compute-matched comparison across held-out task families.

## Stage 6 — Integrate cautiously

Combine independently supported components in a restricted sandbox. Measure transfer, regressions, oversight burden, and recovery from injected failures.

Exit gate: integration produces broad gains without unacceptable safety or reliability regressions.

## Stage 7 — Replicate before scaling

Require adversarial evaluation, independent replication, and a documented safety case before increasing compute, autonomy, permissions, or deployment scope.

