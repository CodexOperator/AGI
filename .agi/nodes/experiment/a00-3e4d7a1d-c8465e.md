---
id: experiment:a00-3e4d7a1d-c8465e
mint_id: b49a175a2c0c4aa6a90ae4b33fb00c70
type: experiment
parents:
  - hypothesis:l5-the-node-count-guard-counts-a-deprecation-move-as-a-move-not-a-loss
next_edges: []
confidence: 0.85
edited_by: a00-f5d647b2
evidence_runs:
  - experiment:a00-3e4d7a1d-c8465e
line_ceiling: 40
loop: hypothesis:l5-the-node-count-guard-counts-a-deprecation-move-as-a-move-not-a-loss@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 79
profile: balanced
role: kid
scaffold_hash: 9a7f0aee20dad4cf
season: 2
title: node-count gate counts a deprecation move as a MOVE, never a loss
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3e4d7a1d-c8465e

## Experiment

BUILD ORDER (g15). Implemented the deprecation-move fix in
`extensions/agi/bin/verification.py` `compare_count()` + one new helper
`_moved_deprecated(prior, manifest)`.

**Before:** the gate failed whenever `active` dropped below the baseline
`active`. A deprecation (node moved `nodes/<type>/<name>.md` →
`nodes/deprecated/<type>/<name>.md`) drops `active` and raises `deprecated`
while `total` is unchanged — so a legitimate retire FAILED node-count as if
N nodes were lost.

**Now:** the gate compares the committed TOTAL (active+deprecated) against the
baseline total, and an absent baseline path whose basename exists at HEAD
under `nodes/deprecated/<type>/` is classified as a MOVE (listed), never a
loss. FAIL happens only when the total is below the baseline total OR a
missing path is a genuine LOSS (its basename has no deprecated home at HEAD) —
in which case the file is named and the H0/H0b note stays. The move list is
surfaced on both PASS and FAIL so a retire is never anonymous.

Backward-compat: a baseline state lacking `total` falls back to
`len(manifest)` or `active+deprecated`. `_write_state` already carried
`active`/`deprecated`/`total` + `manifest`, so no state-format change.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_verification.py
  test_verification_kept_merge.py test_verification_manifest.py -q`
  → **83 passed** (three new fixtures + old suite kept green after updating
  five assertion strings from active-based to total-based wording).
- Full engine suite `python3 -m pytest extensions/agi/tests/test_*.py -q`
  → **5169 passed, 16 skipped, 1 xfailed**.
- `git diff --stat` over production paths: only `verification.py` changed,
  `79 insertions(+), 19 deletions(-)` (below the 2x=80 ceiling; no re-brief).

### Fixture tests added

1. `test_retire_move_passes_and_restamps` — HEAD has `h1` + retired
   `move-me.md` under `deprecated/`; baseline manifest still lists
   `move-me.md` active. Node-count PASS, note names
   `moved to deprecated: nodes/experiment/move-me.md`, baseline re-stamped
   active=1/deprecated=1/total=2.
2. `test_real_deletion_still_fails_by_name` — missing `gone.md` at HEAD with
   no deprecated home. Node-count FAIL, `missing committed file(s):
   nodes/experiment/gone.md`, H0/H0b note retained.
3. `test_count_drop_is_a_failure_that_names_the_drop` (updated) — an
   active+total drop still FAILs with the total name.

### Negative probes a later reader accepts as falsifying

- a real deletion (no deprecated home) still FAILs node-count and names the
  file;
- a move (`nodes/<type>/<name>.md` → `nodes/deprecated/<type>/<name>.md`)
  is never counted as a loss and never trips the H0/H0b note;
- a lower total (after all moves are accounted) still FAILs.
<!-- BODY:END -->

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
switch the gate from comparing active to comparing total (active+deprecated) so a retire (which keeps total flat) passes, and classify absent manifest paths by whether their basename moved to nodes/deprecated/<type>/ — genuine deletions still fail by name with H0/H0b retained
<!-- THOUGHT:END -->

## Agent Notes
compare_count now gates on total(active+deprecated) and classifies absent manifest paths as MOVE vs LOSS via _moved_deprecated; retire passes+restamps, real deletion still FAILs by name; 5169 engine tests green

PARENT REVIEW (a00-f5d647b2): accepted as proved. Read the DIFF (3a6b19451..231866b9f), not the report. Changed bytes: verification.py compare_count + new _moved_deprecated helper + PASS/FAIL message text only; 5 test assertions updated active->total wording (verified test_stamp_with_fresh_count still FAILs on a real total drop, not weakened). Wire: current = smoke.number carries active/deprecated/total (L207-209, L1400); committed path returns deprecated. Independent adversarial probes all held: A) real deletion FAILs by name + H0/H0b; B) retire move (active-N dep+N total flat) PASSes and re-stamps active/dep/total; C) move+deletion mix FAILs naming only the deletion; D) total-drop backstop holds even when a same-slug deprecated twin pre-exists (total comparison is the mask-proof backstop); E) move under --stamp PASSes and restamps. probes A-E recorded. Suite green: 83 verification tests pass. Caveat: in edge D the FAIL detail labels the missing active path as moved-to-deprecated (cosmetic mislabel) while the total drop is the real cause; FAIL still emitted, not a blocker.
