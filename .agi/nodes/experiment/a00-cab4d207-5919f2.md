---
id: experiment:a00-cab4d207-5919f2
mint_id: 9c020242d67c4edd9460e365b544d55b
type: experiment
parents:
  - hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell
next_edges: []
confidence: 0.65
edited_by: a00-cab4d207
evidence_runs:
  - experiment:a00-cab4d207-5919f2
loop: hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell@s2
model: stealth/space-bunny-alpha
production_lines: 4
profile: balanced
role: kid
scaffold_hash: 1e61270ddc8ace6f
season: 2
title: Fail-closed authority publish on veto reader exceptions
town: core
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-cab4d207-5919f2

## Experiment

Split the veto exception handling in `_publish_row_to_authority`: an
`ImportError` (the optional `seatsig` subsystem is absent) remains fail-open,
while any exception raised by the present veto seam returns
`authority: HELD -- veto cell is unreadable (...)` before authority ref and push
code. Added an authority fixture test that forces `is_frozen` to raise and
verifies the refusal plus unchanged remote ref, and an import-unavailable
control that still publishes successfully.

Important scope finding: `seatsig.veto.is_frozen` itself does not expose a
malformed-cell exception. Its `read()` deliberately catches loader exceptions
and treats the cell as defaults/free. Therefore the genuinely malformed-file
case is currently swallowed below this seam; the implemented fail-closed
claim covers an exception from the present veto reader, not all malformed
bytes. Fixing that would require changing `veto.read` beyond the assigned
production block.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -q`
  -> `20 passed`.
- `python3 -m pytest extensions/agi/tests/test_veto.py -q`
  -> `18 passed, 2 warnings`.
- Production diff in the assigned block: 4 changed lines (under the 40-line
  ceiling).
- Existing veto documentation explicitly says unreadable cells read as
  defaults (free tree), so the requested file-malformed guarantee is not yet
  established.

## Agent Notes
Split ImportError fail-open from present-veto exception fail-closed; 38 targeted tests pass. veto.read still intentionally swallows malformed-cell loader errors, so raw malformed bytes remain unproven.
