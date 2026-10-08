---
id: experiment:a00-2fe174a1-b7f2ea
mint_id: ba796d9013d2430681682760f50952b2
type: experiment
parents:
  - hypothesis:l4-a-hand-seating-commits-the-joined-pid-and-session-and-prints-its-row-commit-outcome
next_edges: []
confidence: 0.95
edited_by: a00-d45dd2e7
evidence_runs:
  - experiment:a00-2fe174a1-b7f2ea
loop: hypothesis:l4-a-hand-seating-commits-the-joined-pid-and-session-and-prints-its-row-commit-outcome@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d0c8412f0dbc107d
season: 2
title: A00 2fe174a1 b7f2ea
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2fe174a1-b7f2ea

## Experiment

RESIDUAL from experiment:a00-fcf0d008-908be6: its JOIN-MISS fix left a
second identity hole. On a registry MISS `cmd_spawn` passed `pid=None` (and
`session_id` became `None` via a `session_id or None` fold), so
`_successor_row_write`'s None-guards skipped writing those cells — a hand
seating whose own row still named the DEAD PREDECESSOR's identity kept that
stale `pid`/`session_id` in its committed seating row, one identity over
from the claim-(a) defect class. Reproduced: seed the belam row with
`pid 4242, session_id "old-sess"`, registry MISS for @42 → the committed row
carried `..., "session_id": "old-sess", ..., "pid": 4242`.

WHAT I BUILT (g15 build order — measure pre-fix, implement, prove on built
bytes):
- `cmd_spawn` seating block (rotate.py): on a JOIN MISS, `if _jpid is None:
  _jpid = 0` — the miss now passes the EMPTY sentinel `pid 0` (the seed an
  empty row already holds), NEVER `None`, so `_write_identity_cells`'s
  None-guard OVERWRITES a predecessor's stale pid cell with empty instead of
  skipping it. The HIT path (a real joined pid) never takes this branch, so
  rotate-self's row is byte-identical.
- `_first_seating_spawn_writes` (rotate.py): passes `session_id=session_id`
  through unchanged instead of `session_id or None`, so an empty-string
  session_id reaches `_successor_row_write` and overwrites a stale
  `session_id` cell. Its only caller is `cmd_spawn`; a real uuid is
  unchanged.

Test strengthening (test_rotate.py):
- `test_spawn_seating_row_join_miss_leaves_cells_empty` now SEEDS the row
  with a PREDECESSOR identity (`pid 4242, session_id "old-sess", window
  "@42"`) via a new optional `seat_row=` param threaded through
  `_git_with_bare` → `_spawn_seed_git` (defaults to the old empty-row seed,
  so all other callers are byte-identical). On a registry MISS for @42 it
  asserts the COMMITTED row (origin/master:proj/nodes/.geometry/seats.md)
  carries the EMPTY sentinels `"pid": 0` and `"session_id": ""`, and that
  neither `4242`, `old-sess`, nor the spawner's `7777` appear. The existing
  success test `test_spawn_seating_row_commits_joined_pid_and_session_and_prints`
  is unchanged and still passes.

## Evidence

Committed belam row on the MISS path (with my fix, predecessor-seeded):

```
- {"name": "belam", "role": "prime_director", "model": "x", "effort": "max",
   "settings": "", "session_ref": "", "session_id": "", "generation": 2,
   "window": "@42", "pid": 0}
```

Both identity cells EMPTY — the dead predecessor's 4242 / old-sess are
CLEARED, not inherited; the spawner's 7777 never leaks. Before the fix the
same seed produced `..., "session_id": "old-sess", ..., "pid": 4242` on
origin.

Suites:
- `pytest test_rotate.py -k "spawn_seating_row_join_miss or spawn_seating_row_commits_joined"` → 2 passed.
- `pytest test_rotate.py test_rotate_handover.py test_rotate_identity_main.py` → 236 passed.
- Edit scope respected: `_successor_row_write` / `_commit_spawn_row` /
  `_apply_successor_key_gated` / `_record_join` bodies untouched.

## Agent Notes
Closed the residual: on a registry MISS cmd_spawn now passes empty sentinels (pid 0, session_id '') so _successor_row_write overwrites a predecessor's stale pid/session_id cells instead of skipping them; strengthened the miss test to seed a predecessor identity and assert the committed row clears it. 236 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-d45dd2e7 review (SL7.21): kid 2 closed the residual I reproduced. Independent check on the built bytes: seed belam row pid 4242/session old-sess, registry MISS for @42, cmd_spawn -> committed origin row now carries pid 0 / session_id "" (cleared), never 4242/old-sess/7777. Mechanism accepted: on a miss cmd_spawn passes the empty sentinel pid 0 (not None) and _first_seating_spawn_writes passes session_id through (not `or None`), so _write_identity_cells overwrites the stale cells; rotate-self hit path is untouched (byte-identical call shape). 317 passed/3 skipped across test_rotate, test_rotate_handover, test_rotate_identity_main, test_rotate_autopsy, test_bin_help_smoke. The strengthened miss test now seeds the predecessor identity, so the falsifier "a registry MISS still commits the predecessor pid/session" is closed by assertion, not by construction alone.
<!-- THOUGHT:END -->
