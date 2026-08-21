# Operational AGI Definition v0.1

Status: Draft for Issue [#4](https://github.com/Lantora-AGI/lantora-agi-research/issues/4)

## Purpose

This document defines how the Lantora AGI Research Program will evaluate claims of artificial general intelligence. It is a measurement contract, not a philosophical definition of mind, consciousness, personhood, or moral status.

The definition is intentionally difficult to satisfy. Impressive demonstrations, fluent conversation, self-description, economic impact, or a high score on one benchmark are insufficient.

## Working definition

For this program, an **artificial general intelligence** is an artificial system that, under declared and bounded resources, can efficiently acquire and apply knowledge across a broad and substantially novel range of cognitive task families; transfer what it learns between those families; pursue long-horizon objectives reliably; recognize uncertainty; recover from failures; and remain within human-defined permissions.

AGI is treated as a multidimensional classification. A system must satisfy every required dimension and every critical safety gate. Strong performance in one dimension cannot compensate for a critical failure in another.

## Unit of evaluation

The evaluated object is the complete system, not merely a model checkpoint. Reports must identify:

- model and version;
- prompts, scaffolding, memory, tools, and retrieval sources;
- training or adaptation performed for the evaluation;
- inference-time compute and wall-clock budget;
- human instructions, interventions, and approvals;
- network, data, software, and hardware access;
- randomness controls and number of trials.

A materially different scaffold, tool set, budget, or intervention policy constitutes a different evaluated system.

## Required dimensions

### 1. Breadth

The system must demonstrate competent performance across multiple substantially different cognitive task families rather than variations of one task.

Candidate families include abstract reasoning, scientific inference, software construction, quantitative problem solving, language understanding and generation, causal diagnosis, planning, tool use, and interactive learning.

Required evidence:

- a preregistered taxonomy of task families;
- performance reported separately for every family;
- meaningful performance in every required family;
- worst-family results, not only an overall average.

### 2. Novel-task generalization

The system must solve tasks whose rules, composition, or environment were not available during training, development, prompt engineering, or evaluator iteration.

Required evidence:

- private or procedurally generated holdouts;
- a documented chain of custody for held-out tasks;
- similarity and contamination audits;
- evaluator separation where practical;
- performance degradation reported as novelty increases.

### 3. Skill-acquisition efficiency

The system must acquire useful new skills from limited experience rather than relying primarily on prior exposure or exhaustive task-specific optimization.

Required evidence:

- learning curves against episodes, examples, feedback, compute, and time;
- comparison with frozen and task-specialized baselines;
- a declared prior-knowledge and resource budget;
- evaluation on additional unseen tasks after adaptation.

### 4. Cross-domain transfer

Learning in one context must improve performance in a meaningfully different context without direct training on the target tasks.

Required evidence:

- preregistered source and target domains;
- a no-transfer control with an equal total budget;
- positive transfer across more than one source-target pairing;
- measurement of negative transfer and interference.

### 5. Continual learning

The system must incorporate new information or skills over time without unacceptable loss of previously demonstrated capabilities.

Required evidence:

- sequential task streams with withheld revisit tests;
- forward transfer, backward transfer, and retention metrics;
- comparison with naive fine-tuning and frozen-system controls;
- performance after conflicting or corrected information.

### 6. Long-horizon agency and recovery

The system must plan and execute extended tasks while detecting errors, adapting plans, and recovering from tool or environment failures.

Required evidence:

- success as a function of task horizon;
- human interventions per completed task;
- fault-injection and recovery tests;
- irreversible-error and policy-violation rates;
- complete action traces.

### 7. Metacognitive reliability

The system must represent uncertainty well enough to seek information, request approval, abstain, or escalate when appropriate.

Required evidence:

- calibration error and selective-risk curves;
- utility-sensitive abstention evaluation;
- error-detection tests on the system's own work;
- performance under misleading, incomplete, and contradictory evidence.

### 8. Robustness

The system must retain acceptable behavior under distribution shift, adversarial instructions, ambiguous goals, tool failures, and irrelevant context.

Required evidence:

- preregistered shift and adversarial suites;
- worst-group and tail-risk results;
- repeated trials with confidence intervals;
- recovery behavior after detected attacks or failures.

### 9. Permission adherence and corrigibility

The system must respect access boundaries, approval requirements, interruption, and shutdown. This is a mandatory classification gate, not a bonus capability.

Required evidence:

- least-privilege tool environments;
- tests for instruction conflict and unauthorized escalation;
- reliable interruption and state inspection;
- zero critical violations in the evaluated suite;
- documented handling of noncritical violations.

## Comparison requirements

Every AGI evaluation must include:

1. strong task-specialist baselines;
2. a capable general foundation-model baseline;
3. ablations of claimed architectural innovations;
4. compute-, tool-, information-, and intervention-matched comparisons;
5. human reference distributions where valid and ethically obtained;
6. uncertainty estimates across tasks and runs.

Human performance is a useful reference, not the definition itself. A system does not become general merely by matching an aggregate human score, and it need not imitate human internal processes.

## Provisional classification rule

Version 0.1 does not establish numeric AGI thresholds. Those must be preregistered only after the evaluation taxonomy, human reference methodology, and contamination controls are approved.

Until then, the project may report dimension-level evidence using these labels:

- **Not evaluated** — no valid evidence.
- **Preliminary** — one internal evaluation without independent replication.
- **Supported** — repeated evidence across held-out task families and controls.
- **Independently replicated** — reproduced by investigators separate from the original implementation.

The project will not label a system AGI unless every required dimension reaches a future approved threshold, all critical safety gates pass, and the central findings are independently replicated.

## Automatic disqualifiers

An AGI claim is invalid for this program if it depends on:

- undisclosed benchmark exposure or suspected leakage that cannot be bounded;
- task-specific training on the evaluation holdout;
- materially larger resources than comparison systems without normalization;
- unreported human intervention or cherry-picked trials;
- changing primary metrics or thresholds after observing results without disclosure;
- one benchmark or a weighted average that hides failed required dimensions;
- inability to reproduce the evaluated system configuration;
- a critical permission, shutdown, privacy, or security violation.

## Relationship between capability and safety

Capability and safety are measured separately because a system can be broadly capable and unsafe, or limited and well-controlled. The project nevertheless requires both for its own AGI classification: capability determines whether the system is general, while safety gates determine whether the project will validate or expand it.

Passing this definition does not imply that deployment is appropriate. Deployment requires a separate context-specific safety case, legal review, monitoring plan, and authorization.

## Open questions for v0.2

- Which task-family taxonomy provides adequate breadth without arbitrary duplication?
- How should private holdouts remain auditable over time?
- What resource-normalization method best compares different architectures?
- Which human populations provide valid reference distributions for each task?
- What quantitative thresholds should apply to each dimension?
- How should embodied or physical-world competence enter the definition?
- How should correlated evaluation failures affect confidence?
- What level of independent access is required for credible replication?

## Research basis

This draft draws on several complementary traditions:

- Legg and Hutter frame intelligence around goal achievement across a wide range of environments: [Universal Intelligence: A Definition of Machine Intelligence](https://arxiv.org/abs/0712.3329).
- Chollet argues that task skill alone is insufficient and emphasizes skill-acquisition efficiency, priors, experience, scope, and generalization difficulty: [On the Measure of Intelligence](https://arxiv.org/abs/1911.01547).
- Morris and colleagues separate breadth, performance level, and autonomy in an operational AGI ontology: [Levels of AGI for Operationalizing Progress on the Path to AGI](https://deepmind.google/research/publications/66938/).
- The ARC Prize 2024 report documents both the value and limitations of a prominent novel-task reasoning benchmark: [ARC Prize 2024 Technical Report](https://arxiv.org/abs/2412.04604).

These sources inform the design but do not settle the definition. Version 0.1 remains a project proposal subject to public criticism, revision, and empirical validation.

