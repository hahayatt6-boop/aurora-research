# Test Spec: RES-003 WTP Waiver and EXP Execution Readiness

## Required Checks

1. `python3 -m unittest discover -s tests -v`
2. `python3 scripts/validate_repository.py`
3. `git diff --check`
4. Status scan:
   - RES-003 remains `active`
   - RES-003-WTP is `superseded`
   - RES-003-EXP is `active`
   - EVD-035 remains reliability `low`
5. Misleading-claim scan:
   - No claim that WTP has real survey results
   - No claim that condition 2 is empirically satisfied
   - No `authorizes_mvp: true`
   - No new MVP blueprint files
6. Privacy scan:
   - No identifiable child/family/school/contact data
   - EXP execution package keeps raw child data outside the repo
7. Link validation through `scripts/validate_repository.py`.

## Review Focus

- ARV-006 must be represented as a project-lead ruling and risk acceptance, not evidence.
- EVD-035 must be no-result/skipped, not pending support.
- ADR-003 must not imply direct implementation.
- RES-003-EXP execution package must be research-only and privacy-bounded.

## UltraQA

Docs-only/research-status change. UltraQA may be recorded as passed through adversarial static scans rather than runtime e2e, because no application behavior changed.
