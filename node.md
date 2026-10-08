---
id: experiment:a00-eb9efa69-da529e
mint_id: d11750bc525340af85abf32207588dc4
type: experiment
parents:
  - hypothesis:key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post
next_edges: []
confidence: 0.98
edited_by: a00-eb9efa69
evidence_runs:
  - experiment:a00-eb9efa69-da529e
loop: hypothesis:key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post@s2
model: stealth/space-bunny-alpha
production_lines: 20
profile: balanced
role: kid
scaffold_hash: ac764974a1704315
season: 2
title: Authority publish preserves Prime policy cells
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-eb9efa69-da529e

## Experiment

Implemented the cell-level splice in `extensions/agi/bin/rotate.py` and added a regression fixture to `extensions/agi/tests/test_rotate_key_authority.py`. The helper now parses the matching seat rows, retains the authority row's policy cells, and overlays only the measured rotation-owned cells: `pubkey`, `key_history`, `session_id`, `session_ref`, `session_name`, `session_label`, `pid`, `window`, and `generation`. Missing cells in `new` do not delete base cells; malformed rows fail closed by returning `base`; foreign rows remain byte-identical.

The splice set is grounded in the two observed generation diffs (the differing cells were exactly these nine) and in the rotation writer: `_successor_row_write` / `_write_identity_cells` set the identity cells and key cells on the one successor-row write. The writer also copies `sig_scheme` from the current row (or the minted scheme), but the measured generations showed it unchanged, so it remains policy-preserved here.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -q` → `19 passed in 2.84s` (the tier-gate emitted four stale phantom-record notices, then the 19 tests passed).
- Production diff measurement: `git diff --numstat -- extensions/agi/bin/rotate.py extensions/agi/tests/test_rotate_key_authority.py` → `20 5 extensions/agi/bin/rotate.py` and `30 0 extensions/agi/tests/test_rotate_key_authority.py`; production is 20 changed lines (within the 40-line ceiling).
- The new fixture sets base `model=prime-model` and `effort=high`, while new has stale `model=stale-model` and `effort=low`; it asserts both policy values survive, all nine rotation cells land, and the foreign `bb` row is byte-identical.

## Agent Notes
Cell-level authority splice preserves Prime policy cells and lands the nine measured rotation-owned cells; 19 authority tests pass; production diff 20 lines.
