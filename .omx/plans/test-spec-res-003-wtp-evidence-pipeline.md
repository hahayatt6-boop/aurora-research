# Test Spec: RES-003-WTP Evidence Pipeline

## Validation Commands

- `python3 -m unittest discover -s tests -v`
- `python3 scripts/validate_repository.py`
- `python3 scripts/calculate_wtp_psm.py --psm-input research/RES-003-WTP-psm-distribution-template.csv --price-output /tmp/res-003-wtp-price-points.csv --demand-input research/RES-003-WTP-demand-scenario-template.csv --demand-output /tmp/res-003-wtp-demand-scenario.csv`

## Manual Checks

1. Confirm no raw respondent-level CSV or individual records are added.
2. Confirm EVD-035 does not state actual OPP/PMC/PME, high-certainty rates, or demand indices before data exists.
3. Confirm any README entry labels EVD-035 as pending scaffold if added.
4. Confirm RES-003 remains `active`.
5. Confirm no MVP files are created or authorized.

## Pass Criteria

- All validation commands exit 0.
- No privacy scanner findings.
- No unresolved link errors.
- No evidence claim is made without data.

## UltraQA Scope

This work affects research workflow and CLI/script behavior. UltraQA should at minimum adversarially check:

- empty aggregate templates do not create fake WTP results,
- pending EVD-035 cannot reasonably be mistaken as completed evidence,
- privacy boundaries are preserved in all new files.
