---
id: experiment:a00-cab4d207-5919f2
mint_id: 9c020242d67c4edd9460e365b544d55b
type: experiment
parents:
  - hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell
next_edges: []
confidence: 0.99
edited_by: a00-a4efedba
evidence_runs: experiment:a00-cab4d207-5919f2
loop: hypothesis:authority-publish-fails-closed-on-an-unreadable-veto-cell@s2
model: stealth/space-bunny-alpha
probes: "\"P1 gate: real_cell_gate_probe.py created a real authority fixture, wrote malformed bytes to nodes/.geometry/vetoes.md, and called _publish_row_to_authority through the real seatsig.veto.read loader; result was 'authority: OK -- 2303fe8ad -> season2/main' and origin/season2/main moved from 71f00154 to 2303fe8a. Then deleting the same real cell returned 'authority: SKIPPED -- no aa row to replace on season2/main', not a named unreadable-veto refusal.\""
production_lines: 4
profile: balanced
role: kid
scaffold_hash: 1e61270ddc8ace6f
season: 2
title: Fail-closed authority publish on veto reader exceptions
town: core
verdict: inconclusive_lean_disproved:0
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"The instruction said, 'an unreadable or missing veto cell stops the publish, refused by name, instead of proceeding; a committed test.' The machine actually does the opposite at extensions/agi/src/seatsig/veto.py:117-127: absent cells return defaults, loader exceptions are swallowed, and non-list values become empty lists; the probe built and ran the real authority fixture and observed both malformed and missing cells permit or skip the publish instead of a named HELD. The near miss is a catch-all around is_frozen: it catches a direct exception from a monkeypatched reader, but real loader exceptions and an absent cell are converted to free defaults below that seam, so the guard cannot see the claim's actual states. This review deviates from 'a kid that passes its own tests' only because the kid itself reported this exact gap; the byte inspection and adversarial probe show its delivered behavior is not the target claim."
<!-- THOUGHT:END -->
