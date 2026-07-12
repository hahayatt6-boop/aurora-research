# PRD: RES-003-WTP Evidence Pipeline

## Objective

Make RES-003-WTP ready to convert real aggregate survey outputs into validated repository evidence without importing respondent-level data or overstating WTP conclusions.

## User Need

The research lead wants to keep progressing while fieldwork is not yet available. Repository-side work should reduce future friction and prevent analysis mistakes once aggregate data arrives.

## Requirements

1. Add an EVD-035 draft template that is explicitly pending real aggregate WTP results.
2. Add a fill-in checklist for survey launch and aggregate data handoff.
3. Ensure the PSM calculation workflow is documented from aggregate CSV templates to result CSVs.
4. Preserve privacy boundaries:
   - no respondent-level data,
   - no exact location, school, contact, health, or child-identifying fields,
   - small-cell suppression remains required.
5. Preserve evidence integrity:
   - no fabricated results,
   - no claim that ARV-005 condition 2 is satisfied,
   - no RES-003 status escalation.

## Proposed Deliverables

- `evidence/EVD-035-china-parent-wtp-pricing-experiment.md` with status/context showing planned/pending result fields rather than evidence claims.
- `research/RES-003-WTP-launch-checklist.md` covering launch, platform settings, aggregation, privacy review, and EVD-035 update steps.
- Updates to `research/RES-003-WTP-pricing-experiment.md` and `evidence/README.md` only if needed to link pending scaffolds clearly.

## Acceptance Criteria

- Repository validator passes.
- Unit tests pass.
- The new EVD-035 draft must not be misread as completed evidence.
- Links are valid.
- The checklist gives enough operational detail for a future researcher to run the handoff without reinterpreting the plan.

## Risks

- A placeholder EVD file may be mistaken for actual evidence.
- Validator may require EVD fields that make a pending evidence note look too final.
- Adding too much operational process may obscure the existing WTP plan.

## Risk Controls

- Use `published: unknown`, `source_type: primary-research`, `reliability: low`, and repeated "pending real aggregate results" language.
- In README, label EVD-035 as pending scaffold, not result evidence.
- Keep launch checklist concise and action-oriented.
