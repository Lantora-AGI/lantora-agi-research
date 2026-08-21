# Research Governance

## Evidence levels

1. **Proposal:** a falsifiable hypothesis with a plausible mechanism.
2. **Preliminary:** a completed experiment with artifacts and stated limitations.
3. **Supported:** replicated across seeds and more than one held-out task family.
4. **Replicated:** reproduced independently from the original implementation team.

Only independently replicated findings should be described as established project results.

## Required experiment record

Before execution:

- hypothesis and predicted observation;
- datasets and contamination controls;
- baselines and compute budget;
- primary metric and success threshold;
- safety boundaries and stopping rule;
- planned analyses and exclusions.

After execution:

- complete configuration and version identifiers;
- seeds, costs, interventions, and failure traces;
- all prespecified results, including negative results;
- deviations from the preregistration;
- uncertainty estimates, ablations, and limitations.

## Decision process

- Open-ended ideas begin in Discussions.
- A maintainer converts sufficiently defined work into an Issue.
- Capability-relevant work requires safety review.
- Changes enter the default branch through reviewed pull requests.
- Material scientific disagreements are recorded rather than erased.
- Conflicts of interest must be disclosed by reviewers and authors.

## Prohibited research conduct

- fabricating, hiding, or selectively deleting results;
- changing primary metrics after observing results without disclosure;
- presenting benchmark-specific optimization as general intelligence;
- using private or personal data without authorization;
- bypassing the capability boundaries in `SAFETY.md`.

