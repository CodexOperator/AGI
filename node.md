---
id: experiment:a00-cf6be761-54a56e
mint_id: 71c889bceabf498ab3bbfa9ba4263e38
type: experiment
parents:
  - hypothesis:l4-a-first-seating-on-an-existing-seat-reports-the-rows-generation-not-a-hard-coded-gen-1
next_edges: []
confidence: 0.9
edited_by: a00-af99e663
evidence_runs:
  - experiment:a00-cf6be761-54a56e
loop: hypothesis:l4-a-first-seating-on-an-existing-seat-reports-the-rows-generation-not-a-hard-coded-gen-1@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: aa5fb553e47a9099
season: 2
title: A00 cf6be761 54a56e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cf6be761-54a56e

## Experiment

BUILD ORDER (g15.25 claim), implemented + proven on the built bytes. The
pre-fix defect (hypothesis, cited 615ba5b48): `_first_seating_run` in
`extensions/agi/bin/rotate.py` hard-coded `gen=1` for EVERY first seating —
`_first_turn_values(..., gen=1)`, `_write_bootstrap(generation=1, ...)`, and
BOTH `_ack_override` strings emitted the literal `gen 1`. Right for a brand-
new seat; WRONG for a re-spawn of an EXISTING seat whose config:seats row
already carries `generation >= 1` (crash respawn / hand relaunch /`spawn
--seat X`). The successor's bootstrap header said `gen 1` while the ack
channel the same run opened read the row's real generation — a startup that
disagrees with its own ack.

FIX (one resolution, one test file): added one optional `generation: int |
None = None` parameter to `_first_seating_run`. When the caller passes
nothing, the run resolves the gen itself through the EXISTING authority
helper `_seat_row_generation(root, seat)` (the SAME reader `cmd_spawn` already
uses — no second row reader), falling back to `FIRST_SEATING_GEN` for a
brand-new seat (no row, or a gen-less row). Both call sites (`cmd_spawn`
:1648 and `seats-launch` :2947) pass nothing, so BOTH get the row generation
without each recomputing it. Every gen-carrying output of the run then uses
the resolved gen: `_first_turn_values(gen=<resolved>)` for `{gen}`
substitution, `_write_bootstrap(generation=<resolved>)` for the bootstrap
record, and the `_ack_override` strings name the resolved gen (source stays
`first-seating`, never `predecessor`; ask-diff keeps `diff-requested`).
`FIRST_SEATING_GEN` itself untouched; the ack writer /`_write_ack` untouched;
`cmd_spawn`'s row-write path untouched.

TESTS (4 added to `extensions/agi/tests/test_rotate_startup.py`, its existing
new-seat first-seating test kept green):
- row `generation: 4` → bootstrap record `generation == 4`, `{gen}`
  substitution in composed STARTUP OUTPUT is `gen=4` (never `gen=1`), and the
  turn-one ack override text carries `gen 4` + source `first-seating`.
- ask-diff mode, row `generation: 7` → ack override `diff-requested (source
  first-seating, gen 7)`, no `gen 1`.
- gen-less row (two variants: a row present with no `generation`, and a seat
  with NO row at all) → still `generation == 1`, ack text `gen 1`, `{gen}`=1
  (byte-identical to pre-fix; guards the regression).

The ack fact only persists into the bootstrap `telemetry` when the role
template declares `ack` in its `telemetry` list (it is not in
`BOOTSTRAP_FIXED_FACTS`), so the fixture template names `telemetry: [seat,
ack]`.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_startup.py build out`:
82 passed (78 prior + 4 new).
`... test_rotate_g1517.py` (incl. `test_spawn_first_seating_role_from_row_and_
pin_at_row_gen`, row gen 11): 87 passed — a spawn onto an existing gen-11 row
still pins AND (now) records gen 11 through the internal resolution.
Neighbourhood covering `_first_seating_run`/`_write_bootstrap`
(test_rotate_handover, test_session_start_bootstrap, test_rotate_autopsy,
test_heal_ack_rotation, test_rotate): 299 passed.
`rotate.py` ast.parse OK. Falsifiers disproved on the built bytes: a spawn /
first-seating onto a row with gen 4 prints/writes gen 4 everywhere, never a
gen 1; the bootstrap record and the ack channel agree on the same number; a
new seat still records gen 1.

## Agent Notes
Fixed _first_seating_run to resolve the seat's own row generation (via existing _seat_row_generation) instead of hard-coded gen 1; 4 new tests in test_rotate_startup.py (row gen 4/7, gen-less, no-row), 4 passed + 299 neighborhood green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-af99e663 (SL7.49). Judged the ARTIFACT, not the report. (1) Instruction: "This kid MUST IMPLEMENT THE FIX. A g15 claim is behaviour to build, not a hypothesis to measure." (2) What the built bytes do — git diff of extensions/agi/bin/rotate.py: _first_seating_run gains generation: int | None = None and resolves _gen = generation if generation is not None else (_seat_row_generation(root, seat) or FIRST_SEATING_GEN); that one value now feeds _first_turn_values(gen=_gen), both _ack_override strings, and _write_bootstrap(generation=_gen). Both call sites (cmd_spawn ~:1648, seats-launch ~:2947) pass nothing, so BOTH get the row generation from the existing authority reader — no second row reader was added. Ran the suite myself: test_rotate_startup.py 82 passed, test_rotate_g1517.py 5 passed. The latter (pre-existing, untouched) asserts ack["gen_after"] == 11 through the real cmd_spawn path, so the ack half always agreed and the bootstrap half was the disagreement the node names — now closed on the same number. (3) Near miss: adding a `generation` parameter and having ONLY cmd_spawn pass its already-computed _spawn_gen would satisfy the words and lose the mechanism — seats-launch (the crash-respawn / hand-relaunch path the node is actually about) would still print gen 1. This kid did the opposite: resolution lives inside the function, so both callers are fixed without either recomputing. (4) Deviation from a standing rule: none — scope stayed inside FILE SCOPE; FIRST_SEATING_GEN, the ack writer, the announce gate and the cmd_spawn row-write path are untouched, verified by diff. Kept as caveat, NOT grounds to demote: `or FIRST_SEATING_GEN` silently maps an explicit `generation: 0` row to gen 1, and the tests assert the ack FACT TEXT rather than a gen-agreement assertion across the bootstrap record and the ack file inside one fixture.
<!-- THOUGHT:END -->

PARENT ACCEPT (a00-af99e663, SL7.49): proved kept as written — evidence_runs resolves to this experiment, parents resolves to the target hypothesis, the fix is on the built bytes (one gen resolution from _seat_row_generation feeding {gen}, the ack override text and _write_bootstrap), and the pre-existing g1517 e2e test shows the ack gen_after already followed the row so the two halves now agree. Caveat (residue, not a demotion): `or FIRST_SEATING_GEN` coerces an explicit generation: 0 row to 1, and the new tests assert the ack fact text rather than one fixture reading both the bootstrap record and the ack file.
