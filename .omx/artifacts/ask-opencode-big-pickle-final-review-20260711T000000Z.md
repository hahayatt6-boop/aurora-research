# opencode big-pickle final review attempt

## Original user task

Use an available fallback when the requested Claude/CloudOps model cannot run; specifically use `opencode/big-pickle` if Claude Opus 4.8 is unavailable.

## Backend and prompt

- Backend: local `opencode` CLI
- Requested fallback model: `opencode/big-pickle`
- Mode: read-only final review
- Scope: current uncommitted Aurora research/validator changes, including ADR authorization, ARV independence, MVP gate, privacy boundary, model fallback disclosure, and RES-002/HYP-002/ADR-002 consistency.

## Raw outcome

The CLI started and performed read-only inspection, but the available output mixed in fields/functions and file facts that do not exist in the current repository, then reported that the review was interrupted before final findings. The session stdin was closed, so it could not be corrected in-place.

## Summary

This attempt is not reliable enough to count as a clean code-review gate. It is recorded as a failed/untrusted fallback attempt, not as approval.

## Action items

- Do not represent this as an APPROVE/CLEAR review.
- Use a fresh, current-repo-only review lane for the final gate.
- Keep the model fallback rule: unavailable requested models may downgrade, but the downgrade output must be disclosed and must not be accepted if it is internally inconsistent.
