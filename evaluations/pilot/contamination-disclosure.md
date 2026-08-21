# Pilot evaluation contamination disclosure

Copy this template into every future candidate-system result report.

## System identity

- Model/system name:
- Exact checkpoint or version:
- Provider or source:
- Model and adapter hashes, when available:

## Exposure and tuning

- Were pilot development tasks viewed by system developers?
- Was generator source code used for training, prompting, tool construction, or
  hyperparameter selection?
- Were any validation items or seeds viewed before configuration freeze?
- Is relevant benchmark or synthetic-grammar overlap known or suspected?
- What training-data disclosures are available?

## Configuration freeze

- Preregistration commit:
- Prompt/configuration hash:
- Adapter version:
- Inference budget:
- Tools and memory permissions:
- Samples, retries, and human interventions:

## Post-hoc changes

List every change made after any evaluation result was observed. Label affected
results exploratory and identify the fresh seeds reserved for confirmation.

## Limitations

Explain contamination uncertainty, unavailable training-data information,
interface confounds, exclusions, invalid runs, and any deviation from the
preregistered protocol.

