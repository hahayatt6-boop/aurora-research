# PRD: RES-003 WTP Waiver and EXP Execution Readiness

## Objective

Move the repository from "RES-003-WTP pending fieldwork" to "WTP skipped by project-lead ruling; RES-003-EXP is the active next research execution step" without overstating evidence or opening MVP work.

## Acceptance Criteria

1. A durable ruling exists for the WTP waiver.
2. RES-003-WTP is no longer an active/planned blocker and is marked as skipped/superseded.
3. EVD-035 clearly says no survey was run and no WTP results exist.
4. RES-003 documents that WTP is a low-confidence risk acceptance, not empirical satisfaction.
5. RES-003-EXP is marked active and has an execution package covering ethics, prototype scope, data boundaries, aggregate outputs, and stop conditions.
6. ADR-003 next steps no longer imply direct MVP implementation.
7. HYP-003 points to RES-003-EXP execution and retains WTP risk for later MVP gating.
8. Repository validation and tests pass.
9. Keyword scans find no misleading "WTP empirically satisfied" or "MVP authorized" claims.

## Planned Changes

- Add `collaboration/ARV-006-wtp-waiver-ruling.md`.
- Add `research/RES-003-EXP-execution-package.md`.
- Update:
  - `research/RES-003-ai-guide-efficacy.md`
  - `research/RES-003-WTP-pricing-experiment.md`
  - `research/RES-003-EXP-validation-experiment.md`
  - `research/README.md`
  - `evidence/EVD-035-china-parent-wtp-pricing-experiment.md`
  - `evidence/README.md`
  - `collaboration/ARV-004-res-003.md`
  - `collaboration/ARV-005-conditions-ruling.md`
  - `decisions/ADR-003.md`
  - `hypotheses/HYP-003-ai-guide-efficacy.md`

## Risks

- Waiver may be misread as evidence satisfaction.
- EVD-035 may be cited incorrectly as positive WTP evidence.
- ADR-003 may still appear to authorize direct MVP.
- Child validation execution could imply collection of identifiable data unless boundaries are explicit.

## Consensus Gate

Architect and Critic review are required by the Autopilot contract. If native subagent quota blocks those reviews, record the blocker and use local review/validation as fallback evidence, but mark the external-review limitation explicitly.
