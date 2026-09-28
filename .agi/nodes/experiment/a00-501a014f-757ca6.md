---
id: experiment:a00-501a014f-757ca6
mint_id: 7c32354c08d44819ba58339189b4f246
type: experiment
parents:
  - hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses
next_edges: []
confidence: 0.8
edited_by: a00-501a014f
evidence_runs:
  - experiment:a00-501a014f-757ca6
loop: hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses@s2
model: stealth/space-bunny-alpha
production_lines: 31
profile: balanced
role: kid
scaffold_hash: df18f86a959d702d
season: 2
title: "the two DH.408 halves compose: the registry gate answers first, a registered behind seat merges instead of refusing"
town: core
verdict: proved
---
# experiment:a00-501a014f-757ca6

## What was built

The parent's read: kid 1 (`experiment:a00-183e23e5-066193`) landed the SEQUENTIAL
capture chain in `hooks/rotation_alert.py`; kid 2 (`experiment:a00-70e38375-15d522`)
landed the registry-gate MOVE in `bin/rotate.py`; neither branch carried both, and
kid 2's branch still PINNED the behind-refusal in a test. This round composes the two
halves in `cmd_rotate_self` and un-pins the refusal.

| half | before | after |
|---|---|---|
| (1) gate order (kid 2) | `_geometry_resolution_root` refusal, THEN `_find_seat(_seat_read_root(...))` | registry gate FIRST; the geometry guard and any merge it may perform are unreachable by an unregistered name |
| (2) behind merge (the DH.408 residue) | a REGISTERED seat on a behind CLEAN tree refuses `... is behind origin/season/s2 by N commit(s)` | ONE `_prepare_checks(root, seat, perform=True)` — the merge rotate-self ALREADY performs by default — then re-resolve ONLY at 0 behind |

```
cmd_rotate_self, in order now:
  human gate -> branch guard
  -> seat = args.name ; row = _find_seat(_seat_read_root(root, seat), seat)   # kid 2's move
       (throwaway -> row = {} ; unregistered -> `no seat`, return 1, NOTHING fetched/pushed/merged)
  -> cfg_root, geom_src = _geometry_resolution_root(root)
       None and not --dry-run -> _prepare_checks(root, seat, perform=True)   # the only-behind merge
       re-resolve ONLY if _geometry_behind_count(root) == 0
  -> still None -> the by-name behind refusal, byte for byte (exit 1)
```

`extensions/agi/bin/rotate.py` only: `git diff --numstat` -> **+31 / -17** (a move plus
the merge arm; measured before this node was written). No second merge implementation:
the arm calls the ONE `_prepare_checks(perform=True)` the captive gate already runs, so
its guards (clean tree, `_merge_applies_clean`, abort-on-rc) are the engine's own.
`--dry-run` still performs nothing and keeps the refusal.

## Evidence — the tests, and that they are not vacuous

`extensions/agi/tests/test_rotate_templates.py` (+4):

- `test_registry_gate_runs_before_the_geometry_merge_attempt` — source order: the
  `_find_seat(_seat_read_root(root, seat), seat)` gate precedes `_geometry_resolution_root`,
  and the merge arm is the one `_prepare_checks(root, seat, perform=True)` spelling.
- `test_a_registered_behind_seat_merges_the_geometry_and_rotates` — a real git seat repo
  on `loop/stale` at geometry v1 with a real (bare) `origin` carrying v2: behind == 1.
  After the run: behind == 0, `HEAD == tip` (the merge landed), and the rotation got PAST
  the geometry guard, stopping only at the next gate the test arms (`rc 3`, nothing
  rotated, no window touched). Pre-fix this refused `stale rotation config` at rc 1.
- `test_a_behind_seat_whose_merge_cannot_land_still_refuses_by_name` — no reachable
  origin, so the fetch fails and check 3 reports unmeasured and merges nothing: `rc 1`,
  the behind-count and `git merge --no-edit origin/season/s2` intact, `HEAD` unmoved.
- `test_an_unregistered_behind_seat_refuses_before_any_merge` — the same behind tree with
  `--name no-such-seat`: `no seat` at rc 1, no behind line at all, `HEAD` unmoved.

**Non-vacuity (measured):** the three order/merge tests were re-run against a rebuilt
PRE-composition `cmd_rotate_self` (geometry guard first, no merge arm) -> **3 failed, 1
passed**; the passing one is the refusal-preserved test, which must pass on both sides.
Pre-fix evidence of the residue is also in the tree: the pre-existing
`test_m3_stale_worktree_refuses_by_name_and_sync_cmd` fixture refused a REGISTERED seat
(sanctuary-director) with rc 1, and it still does on the `--dry-run` path.

```
python3 -m pytest extensions/agi/tests/test_rotate_templates.py -q            -> 36 passed
python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_prepare.py \
    extensions/agi/tests/test_rotate_self_registry_and_shield.py \
    extensions/agi/tests/test_rotate_templates.py \
    extensions/agi/tests/test_rotate_alarms_captive.py \
    extensions/agi/tests/test_rotation_alert_capture.py \
    extensions/agi/tests/test_rotation_alert_capture_safety.py -q              -> 459 passed
```

No live seat, no real `rotate.py` subprocess, no tmux: every test drives `rotate.main`
against a throwaway git fixture in `tmp_path`. No git written; one read-only
`git diff --numstat`.

## What this does and does not settle

- Composes both halves on ONE branch, so the next round merges a single diff instead of
  reconciling two siblings, and kid 2's test no longer pins the bug (its pin lived on its
  branch only; this branch asserts the OPPOSITE and it is what will survive a merge).
- The geometry arm deliberately keeps the refusal for every case the merge cannot make
  mechanical (dirty tree, conflicts, no origin, `--dry-run`): only `0 behind` re-resolves.
- Hypothesis conjunct 1 (rotate after a refusing handoff) is kid 1's and stays proved there;
  what this round removes is the OTHER way a due seat silently never rotated — the geometry
  refusal that fires before any merge the rotation had already budgeted for.

## Agent Notes
composed both DH.408 halves in cmd_rotate_self: registry gate first (kid 2), then a registered behind CLEAN seat performs the ONE _prepare_checks(perform=True) only-behind merge and re-resolves only at 0 behind; refusal intact for dirty/conflicting/unreachable/dry-run. +31/-17 production lines, 4 new tests (3 fail on the pre-composition order), 459 passed across the rotate files.
