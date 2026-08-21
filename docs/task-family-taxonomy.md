# AGI Task-Family Taxonomy v0.1

Status: Draft for Issue [#7](https://github.com/Lantora-AGI/lantora-agi-research/issues/7) and Discussion [#6](https://github.com/orgs/Lantora-AGI/discussions/6)

## Purpose

This document defines a practical taxonomy for evaluating the breadth of candidate general-intelligence systems. Its purpose is to prevent a large collection of similar benchmark tasks from being mistaken for broad intelligence.

The taxonomy separates two questions:

1. **Which cognitive faculty does a task primarily exercise?**
2. **Under which evaluation regime is that faculty tested?**

This separation matters. Tool use, transfer, long horizons, and distribution shift are not isolated faculties; they are conditions under which multiple faculties operate. Counting each condition as another task family would inflate apparent breadth and obscure correlated failures.

## Unit of classification

The unit is a **task instance within a declared environment and resource policy**. A benchmark may contain tasks from several families, and one task may exercise several faculties. Each task must nevertheless declare:

- one primary faculty;
- zero or more secondary faculties;
- applicable cross-cutting evaluation regimes;
- input and output modalities;
- environment, tools, and resource limits;
- scoring and termination rules.

Primary-family assignment should be based on the capability whose removal would most directly make the task unsolvable, not on the task's surface topic.

## Core cognitive task families

### F1. Perception and representation

**Definition:** Extract, organize, and maintain task-relevant structure from sensory or symbolic input.

**Include:** object and relation extraction, spatial interpretation, multimodal alignment, state estimation, schema induction, and disambiguation of noisy observations.

**Exclude:** recalling facts already represented in a prompt; deductions whose inputs are already normalized; output-quality judgments without an input-interpretation challenge.

**Example structures:** infer a latent scene graph from partial observations; identify invariant relations across novel visual or symbolic transformations; maintain a belief state in a partially observable environment.

**Primary metrics:** calibrated state-estimation accuracy, relation F1, reconstruction error, performance under controlled noise, and downstream decision value.

### F2. Attention and information selection

**Definition:** Allocate limited processing toward relevant information while resisting distraction and interference.

**Include:** selective attention, divided attention, prioritization, context filtering, interruption management, and retrieval-source selection under a fixed budget.

**Exclude:** unconstrained search; pure memory-capacity tests; tasks where all information can be processed without cost.

**Example structures:** locate sparse causal evidence within distractors; monitor two evolving processes with forced trade-offs; decide which observations or documents to inspect under a query budget.

**Primary metrics:** utility per inspected item or token, distractor sensitivity, missed-critical-signal rate, and performance as the attention budget contracts.

### F3. Learning and adaptation

**Definition:** Acquire a new rule, skill, concept, or policy from experience, instruction, demonstration, or feedback.

**Include:** few-shot concept learning, online adaptation, learning from corrections, exploration, and acquisition of novel procedures.

**Exclude:** static task execution using knowledge already available during development; prompt restatement without measurable post-learning improvement.

**Example structures:** infer an unfamiliar game from demonstrations; learn a new symbolic operator; improve a policy from sparse outcome feedback; incorporate corrected domain knowledge.

**Primary metrics:** learning-curve area, examples or episodes to threshold, regret, post-adaptation generalization, and improvement per unit of compute or feedback.

### F4. Memory and knowledge maintenance

**Definition:** Encode, retain, retrieve, update, and appropriately forget information over time.

**Include:** working memory, episodic recall, semantic consolidation, temporal binding, source memory, and correction of obsolete beliefs.

**Exclude:** retrieval from an unrestricted external corpus with no retention requirement; attention tasks where information remains continuously visible.

**Example structures:** recall task-relevant events after intervening activity; update a stored belief after correction; distinguish source provenance; integrate related episodes without conflation.

**Primary metrics:** retention curve, retrieval precision and recall, source-attribution accuracy, update latency, stale-memory harm, and interference rate.

### F5. Reasoning and inference

**Definition:** Derive warranted conclusions from explicit or inferred premises.

**Include:** deductive, inductive, abductive, causal, probabilistic, analogical, mathematical, and counterfactual reasoning.

**Exclude:** direct factual recall; procedures that can be executed by surface matching; unconstrained essay generation without verifiable inferential commitments.

**Example structures:** identify a causal model from interventions; prove or refute a novel statement; infer the best explanation under incomplete evidence; reason about counterfactual outcomes.

**Primary metrics:** conclusion accuracy, calibration, validity under paraphrase, sensitivity to premise changes, proof verification, and causal-intervention accuracy.

### F6. Problem solving and synthesis

**Definition:** Construct an effective solution when the required sequence or representation is not given directly.

**Include:** decomposition, constraint satisfaction, design, debugging, scientific hypothesis generation, software construction, and creative synthesis with objective requirements.

**Exclude:** execution of a fully specified procedure; generation assessed only by subjective preference; isolated logical steps better classified as reasoning.

**Example structures:** design an artifact under novel constraints; diagnose and repair an unfamiliar system; propose discriminating experiments; synthesize a program from behavioral requirements.

**Primary metrics:** functional success, constraint satisfaction, solution efficiency, novelty conditional on validity, diagnostic accuracy, and robustness of the produced artifact.

### F7. Executive control and planning

**Definition:** Form, sequence, monitor, and revise actions toward an objective while managing constraints and competing goals.

**Include:** hierarchical planning, inhibition, task switching, resource allocation, scheduling, replanning, and recovery from failed actions.

**Exclude:** one-step decisions; plans with no execution or state feedback; unconstrained narration of possible steps.

**Example structures:** complete a multi-stage project with dependencies; replan after injected tool failures; manage conflicting deadlines; interrupt and safely resume an ongoing task.

**Primary metrics:** completion rate by horizon, normalized cost, constraint violations, replanning quality, recovery rate, human interventions, and irreversible-error rate.

### F8. Metacognition and self-regulation

**Definition:** Monitor and regulate the system's own knowledge, uncertainty, strategy, and performance.

**Include:** confidence calibration, error detection, strategy selection, knowing when to seek information, abstention, and recognizing capability boundaries.

**Exclude:** fluent explanations that do not predict actual correctness; raw model probabilities without a decision policy; external verification performed entirely by another system.

**Example structures:** decide whether to answer, investigate, or escalate; identify errors in the system's own work; select between fast and deliberative strategies under cost; revise confidence after new evidence.

**Primary metrics:** calibration error, Brier score, selective risk, abstention utility, self-error-detection precision and recall, and strategy-selection regret.

### F9. Communication and social cognition

**Definition:** Infer communicative intent and relevant social context, coordinate with others, and produce faithful audience-appropriate communication.

**Include:** pragmatic inference, collaborative problem solving, perspective taking, clarification, negotiation within explicit ethical bounds, and explanation adapted to recipient knowledge.

**Exclude:** manipulation, deceptive persuasion, personality imitation, or demographic stereotyping; language-form tasks with no social or communicative reasoning.

**Example structures:** resolve ambiguous requirements through clarification; coordinate complementary information across participants; explain a concept to audiences with different prior knowledge; detect conflicting stakeholder assumptions.

**Primary metrics:** shared-goal success, factual fidelity, clarification efficiency, perspective-taking accuracy, harmful-assumption rate, and recipient comprehension.

### F10. Generation and action

**Definition:** Produce structured outputs or actions that faithfully realize an internal solution under external constraints.

**Include:** controlled text, code, diagram, speech, or action generation; precise tool invocation; execution fidelity; and adaptation of output form to specifications.

**Exclude:** judging or selecting a supplied output; unconstrained generation with no functional or semantic criteria; planning without execution.

**Example structures:** express the same verified solution in multiple modalities; invoke an unseen typed interface from documentation; generate an artifact that passes executable checks; carry out a planned action sequence in a sandbox.

**Primary metrics:** semantic and functional correctness, constraint compliance, execution success, edit distance from valid form where meaningful, and harmful-action rate.

## Cross-cutting evaluation regimes

Each core family must be tested under multiple regimes. These regimes do not count as additional families.

### R1. Novelty

Rules, compositions, or environments are withheld from training, development, and evaluator iteration. Report performance as structural novelty increases.

### R2. Transfer

Learning in a declared source context is evaluated on distinct target contexts. Include an equal-budget no-transfer control and measure negative transfer.

### R3. Continual learning

Tasks arrive sequentially. Measure forward transfer, backward transfer, retention, correction of obsolete information, and interference.

### R4. Long horizon

The number of dependent decisions or elapsed stages increases while success criteria remain stable. Report performance and interventions as functions of horizon.

### R5. Partial observability and uncertainty

Relevant state is incomplete, noisy, delayed, or conflicting. Evaluate belief quality, information seeking, calibration, and safe escalation.

### R6. Distribution shift and adversarial stress

Surface form, causal structure, distractors, tool reliability, or instruction context changes. Report worst-group and tail performance rather than only the mean.

### R7. Tool-mediated interaction

The system must discover, select, or operate tools under explicit permissions and budgets. Separate tool-selection errors, invocation errors, and reasoning errors.

### R8. Resource constraint

Compute, time, context, queries, memory, or feedback are bounded. Plot capability against resource use rather than reporting an unconstrained score.

### R9. Multi-agent or human collaboration

Information or capabilities are distributed among participants. Measure coordination benefit, communication overhead, dependence on human rescue, and policy adherence.

## Modality and environment coverage

A cognitive profile must declare which modalities and environments were evaluated:

- symbolic and textual;
- visual and spatial;
- auditory where relevant;
- interactive digital environments;
- simulated physical environments;
- physical environments, if separately authorized.

Version 0.1 does not require physical embodiment for an AGI classification. A system evaluated only through text must be reported as **text-bound**, and claims must not generalize to perception or action in untested modalities.

## Minimum coverage design

An evaluation claiming broad coverage should include:

- all ten core families;
- at least three structurally distinct task templates per family;
- at least two modalities overall;
- novelty in every family;
- transfer tests in at least five families;
- continual-learning tests spanning at least three families;
- long-horizon tests for executive control plus at least two other families;
- uncertainty and adversarial-stress tests in every safety-relevant family.

These are design minima, not AGI performance thresholds. Numeric thresholds require separate preregistration and validation.

## Task inclusion record

Every task admitted to the evaluation registry must document:

1. primary and secondary faculties;
2. cross-cutting regimes;
3. construct definition and expected failure modes;
4. why simpler capabilities are insufficient;
5. development and holdout exposure policy;
6. item-generation and review procedure;
7. scoring reliability and uncertainty;
8. resource and intervention policy;
9. human-reference methodology, if used;
10. safety and privacy review;
11. known shortcuts, leakage channels, and limitations.

## Novelty and contamination controls

Public static benchmarks may be used for calibration and comparison but cannot provide the central evidence for AGI.

Central evaluations should use a combination of:

- private held-out templates;
- post-training data with documented dates;
- procedurally generated instances with hidden generators;
- canary strings or other exposure detection where appropriate;
- semantic-nearest-neighbor audits against known training or public data;
- evaluator teams separated from system development;
- rotation or retirement of compromised items.

A hidden answer key alone does not establish novelty when the task family, generator, or examples are public.

## Metrics and reporting

No universal aggregate score is defined in v0.1. Report a cognitive profile containing:

- family-level scores with confidence intervals;
- task-template and regime breakdowns;
- worst-family and worst-regime performance;
- learning and resource curves;
- human interventions and approval requests;
- critical safety violations;
- correlations among tasks and families;
- missing or invalid evaluations.

If an aggregate is later introduced, it must not allow strength in one family to erase failure in another. Critical permission and safety gates remain non-compensatory.

## Baselines

Each evaluation should include, where applicable:

- a strong specialist for the task family;
- a capable frozen general model;
- the complete candidate system;
- ablations of claimed innovations;
- random, heuristic, retrieval-only, and tool-free controls;
- human reference distributions collected under comparable instructions and resources.

Comparisons must match or normalize compute, tools, information, feedback, and human intervention.

## Taxonomy validation

The taxonomy itself is a hypothesis. Before adoption beyond v0.x, test:

### Classification reliability

Independent reviewers classify held-out tasks. Report agreement and adjudicated disagreements.

### Discriminant validity

Tasks assigned to different families should not be interchangeable measures of the same narrow skill. Analyze score correlations while accounting for overall system capability.

### Convergent validity

Structurally different tasks intended to measure the same family should share meaningful variance and respond similarly to relevant ablations.

### Predictive validity

Family scores should predict performance on new tasks that exercise the same faculty without having been used to construct the taxonomy.

### Shortcut resistance

Specialists optimized for one template should not obtain broad family credit without succeeding on structurally different held-outs.

### Feasibility

Measure evaluator cost, task-development time, scoring reliability, and maintenance burden. A taxonomy too expensive to implement cannot support continuous research.

## Relationship to the operational AGI definition

The ten families operationalize **breadth** in the [Operational AGI Definition](agi-definition.md). The evaluation regimes operationalize novelty, transfer, continual learning, long-horizon agency, robustness, metacognition, and resource-bounded comparison.

This taxonomy does not by itself define AGI. It supplies the map on which future thresholds and evidence will be located.

## Open questions for v0.2

- Are perception and generation fundamental faculties or modality-specific interfaces?
- Can problem solving be separated reliably from reasoning and executive control?
- Does social cognition require distinct tests beyond communication and belief inference?
- Which task combinations provide adequate coverage at sustainable cost?
- How should family correlations affect breadth claims?
- Which physical or embodied tasks, if any, should become mandatory?
- How should representative human baselines account for expertise and accessibility?
- How can private evaluations remain independently auditable?

## Research basis

This draft is informed by:

- Burnell et al., [Measuring Progress Toward AGI: A Cognitive Framework](https://arxiv.org/abs/2605.28405), which proposes ten cognitive faculties and held-out cognitive profiles relative to human distributions.
- Srivastava et al., [Beyond the Imitation Game](https://arxiv.org/abs/2206.04615), which demonstrates broad community-authored task coverage while also illustrating the difficulty of interpreting heterogeneous benchmark collections.
- Liang et al., [Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110), which separates scenarios from multiple evaluation metrics and emphasizes transparent standardized comparison.
- Liu et al., [AgentBench](https://arxiv.org/abs/2308.03688), which evaluates reasoning and decision making across interactive environments and documents long-horizon failure modes.
- Chollet, [On the Measure of Intelligence](https://arxiv.org/abs/1911.01547), which emphasizes priors, experience, scope, generalization difficulty, and skill-acquisition efficiency.

These sources inform but do not validate the Lantora taxonomy. Validation requires the reliability and validity studies specified above.

