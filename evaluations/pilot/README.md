# Stage 2 pilot evaluation suite

This pilot tests three bounded constructs: abstract reasoning, learning and
transfer, and planning. It is designed to exercise scientific evaluation
methods before any model is integrated. Results apply only to the generated
task distribution and must not be described as an AGI determination.

The design implements [Issue #13](https://github.com/Lantora-AGI/lantora-agi-research/issues/13)
and records the decisions from [Discussion #12](https://github.com/orgs/Lantora-AGI/discussions/12).

Independent contributors should follow the
[replication runbook](REPLICATION.md) and report their evidence in
[Issue #15](https://github.com/Lantora-AGI/lantora-agi-research/issues/15).

## Generate and validate the public development suite

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --no-deps -e .

lantora-pilot generate \
  --seed 13001 \
  --items-per-condition 50 \
  --output runs/pilot-13001

lantora-pilot validate --tasks runs/pilot-13001/tasks
```

There are three families and three conditions, so 50 items per family-condition
pair produces 450 tasks. A generation manifest records every canonical task
hash. The command refuses to overwrite an existing directory.

## Run transparent non-model baselines

```bash
lantora-pilot evaluate \
  --tasks runs/pilot-13001/tasks \
  --adapter heuristic \
  --seed 17 \
  --output runs/pilot-13001-heuristic

lantora-pilot evaluate \
  --tasks runs/pilot-13001/tasks \
  --adapter random \
  --seed 17 \
  --output runs/pilot-13001-random
```

The heuristic baseline uses enumerated rule candidates for reasoning and
learning tasks, and a topological algorithm for planning. The random baseline
is deterministically seeded by task. The oracle baseline is reserved for
pipeline verification because exact-scored tasks may read their gold answers.
The runner removes gold answers before invoking every adapter that is not
explicitly marked as a trusted oracle.

The optional `majority` adapter predicts the most common demonstration label
for learning tasks and abstains elsewhere. Candidate-visible payload rendering
is separate from generation and excludes gold answers and private metadata.

Reports keep every family and condition separate and include 95% Wilson
intervals. They intentionally contain no composite “AGI score.”

Use the study command to quantify variation across five or more seeds:

```bash
lantora-pilot study \
  --seeds 13001 13002 13003 13004 13005 \
  --items-per-condition 50 \
  --adapter heuristic \
  --output runs/pilot-development-study
```

The study summary preserves per-seed result hashes and reports the mean,
population standard deviation, minimum, and maximum success rate for every
family-condition pair. Published development seeds demonstrate the pipeline;
confirmatory evaluation must select fresh validation seeds using the protocol.

## Constructs and conditions

### Abstract reasoning

The task supplies demonstrations of a latent operation over synthetic symbol
sequences and asks for the transformed query. Control uses a single operation;
transfer changes the symbol vocabulary; harder composes two operations. The
generator rejects examples unless exactly one rule in its published grammar is
consistent with the demonstrations.

This measures induction within a tiny transformation grammar. It does not
measure unrestricted mathematical reasoning. Parsing and output-format errors
remain confounds.

### Learning and transfer

The task supplies labelled demonstrations of a hidden Boolean rule over
synthetic attributes. Control uses one relevant attribute; transfer renames
attributes and values; harder adds conjunctive/disjunctive rules and distractor
attributes. Demonstrations must contain both labels and uniquely identify one
rule in the published hypothesis class.

This measures sample-limited rule learning and representation transfer within
that class. It is not continual learning, online adaptation, or general domain
transfer.

### Planning

The task supplies actions and precedence constraints. Control uses a small
static graph; transfer renames and reorders entities; harder asks for a revised
plan after an additional constraint. A graph oracle rejects cyclic instances.
The scorer accepts every permutation that contains each node once and obeys all
constraints, rather than privileging one canonical answer.

This measures formal constraint satisfaction. It is not evidence of real-world
autonomy, causal understanding, or long-horizon reliability.

## Shortcut and validity checks

- Rule demonstrations must identify exactly one candidate.
- Learning demonstrations include both labels.
- Inputs and task identifiers are unique within a generated suite.
- Planning graphs must be acyclic and every oracle plan is rescored through the
  independent constraint-validity scorer.
- Transfer cases alter representation while preserving the latent construct.
- Seeds, generator version, budgets, inputs, outputs, and hashes are recorded.

The public generator permits inspection and therefore cannot prevent a system
from specializing to its grammar. Any such tuning must be disclosed. See
[validation protocol](validation-protocol.md) and
[contamination disclosure template](contamination-disclosure.md).

## Interpretation and deferred work

The 50-item minimum is an engineering target, not a universal power analysis.
Wilson intervals describe binomial uncertainty for each family-condition group;
they do not capture generator misspecification or model-selection bias.
Metacognition is deferred until a calibration/abstention protocol exists, and
knowledge composition is deferred to reduce overlap with abstract reasoning.

No provider adapter or protected audit content is included. Untrusted model or
agent execution still requires an independently reviewed isolation boundary.
