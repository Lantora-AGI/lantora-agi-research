# Lantora AGI Research Program

The Lantora AGI Research Program is an open, evidence-driven effort to investigate systems that can learn, reason, plan, transfer knowledge, and act reliably across substantially novel domains while remaining within human-defined boundaries.

This repository is a research program, not a claim that AGI has been achieved or that it will be achieved on a schedule.

## Research principles

- Define claims and success criteria before running experiments.
- Compare against reproducible, compute-matched baselines.
- Keep held-out evaluations and audit benchmark contamination.
- Report negative results, interventions, costs, and failures.
- Require safety review before increasing autonomy or access.
- Treat independent replication as stronger evidence than demonstrations.

## Start here

- [Research roadmap](ROADMAP.md)
- [Research governance](RESEARCH_GOVERNANCE.md)
- [Safety boundaries](SAFETY.md)
- [Evaluation harness](evaluations/README.md)
- [Stage 2 pilot suite](evaluations/pilot/README.md)
- [How to contribute](CONTRIBUTING.md)
- [Security reporting](SECURITY.md)

## Run the evaluation harness

The v0.1 harness is a provider-neutral, local-first foundation for reproducible
experiments. Its three included tasks validate the infrastructure; they are not
AGI benchmarks.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --no-deps -e .
lantora-eval --output runs/example --seed 17
python -m unittest discover -s tests -v
```

The command writes `manifest.json`, `results.json`, and `report.md` into a new
output directory. It refuses to overwrite an existing run bundle.

## How work moves through the project

1. Discuss an idea in GitHub Discussions.
2. Submit a structured research proposal.
3. Complete methodological and safety review.
4. Open a scoped issue with acceptance criteria.
5. Preregister the experiment.
6. Submit methods, artifacts, and results by pull request.
7. Seek independent replication.

## Current status

The program has begun Stage 2: implementing reproducible evaluation infrastructure on top of the Stage 1 definitions. There is no validated AGI system in this repository.

## Licensing

Unless a file states otherwise, software source code is intended to be released under the Apache License 2.0. Research prose, diagrams, and documentation are intended to be released under Creative Commons Attribution 4.0. Datasets, model weights, and third-party materials require their own explicit terms. See [LICENSE](LICENSE) and [LICENSE-DOCS](LICENSE-DOCS).

## Responsible disclosure

Do not publicly post vulnerabilities, leaked credentials, or findings that materially enable dangerous capabilities. Follow [SECURITY.md](SECURITY.md).
