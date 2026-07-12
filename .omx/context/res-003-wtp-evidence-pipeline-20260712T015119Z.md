# RES-003-WTP Evidence Pipeline Context

Created: 2026-07-12T01:51:19Z

## Task Statement

Continue progressing RES-003-WTP without treating absent real survey responses as a current blocker.

## Desired Outcome

Prepare all repository-side artifacts needed so that once aggregate WTP survey results exist, the project can calculate PSM outputs, produce EVD-035, and update RES-003/HYP records without importing respondent-level data into git.

## Known Facts And Evidence

- RES-003 remains `active`.
- ARV-005 ruled ARV-003 condition 2 requires non-literature China WTP pricing evidence.
- RES-003-WTP is `planned` and now has:
  - deployable questionnaire text,
  - aggregate analysis table definitions,
  - independent artifact critique,
  - aggregate-only PSM calculator,
  - blank aggregate CSV templates.
- Repository validation and unit tests passed after the latest WTP aggregate analysis work.
- Current branch is `traycer/quiet-yak`, pushed to origin at `1b6875d`.

## Constraints

- Do not store identifiable child, family, school, contact, health, precise location, or respondent-level survey data in git.
- Do not claim WTP evidence is satisfied until real aggregate results exist.
- Continue safe repository-side preparation without waiting for fieldwork.
- MVP remains blocked until RES-003 conditions are actually satisfied.

## Unknowns / Open Questions

- Actual WTP survey responses do not exist yet.
- Minimum viable monthly fee is not locked by a cost model.
- The survey platform/export shape is not known.

## Likely Codebase Touchpoints

- `research/RES-003-WTP-pricing-experiment.md`
- `research/RES-003-WTP-questionnaire.md`
- `research/RES-003-WTP-analysis-tables.md`
- `research/RES-003-WTP-psm-distribution-template.csv`
- `research/RES-003-WTP-demand-scenario-template.csv`
- `scripts/calculate_wtp_psm.py`
- `tests/test_calculate_wtp_psm.py`
- future `evidence/EVD-035-china-parent-wtp-pricing-experiment.md`
- future updates to `research/RES-003-ai-guide-efficacy.md`, `hypotheses/HYP-002-willingness-to-pay.md`, `hypotheses/HYP-003-ai-guide-efficacy.md`
