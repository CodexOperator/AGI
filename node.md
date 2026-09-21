---
id: experiment:a00-de983db0-160e0c
mint_id: 2e1442cf1b2842d792c5337bd1a79b6a
type: experiment
parents:
  - hypothesis:l4-after-join-is-performed-live-by-a-running-watch-or-by-rotate-selfs-own-tail-when-no-watcher-runs
next_edges: []
confidence: 0.92
edited_by: a00-4125554d
evidence_runs:
  - experiment:a00-de983db0-160e0c
loop: hypothesis:l4-after-join-is-performed-live-by-a-running-watch-or-by-rotate-selfs-own-tail-when-no-watcher-runs@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2508cba5485a4f86
season: 2
title: A00 de983db0 160e0c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-de983db0-160e0c

## Experiment

SL7.72 kid 3, same target as kid 1/kid 2: fix the one reviewer-level defect
left on the after-join watch-or-tail mechanism. The heartbeat was written and
read through DIFFERENT resolvers:

- `heal.py:_write_watch_heartbeat` (heal.py:885) wrote via
  `locations.sessions_dir(root)` — the **per-worktree** join `<root>/sessions`.
- `rotate.py:_watch_heartbeat_path` (rotate.py:9240) reads via
  `_sessions_dir` = `locations.shared_sessions_dir(root)` — routed through
  `git_common_root` to the **main checkout**.

They agreed only when the watch ran from the main checkout (the systemd unit's
`--root /home/ubuntu/work/agi`). Linked-worktree-rooted watch → heartbeat in
the worktree's `sessions/` while seats read the main checkout's →
`_watch_alive` False with the watch fully alive → tail performed, record said
`performer: "tail"` while a healthy watch existed. Claim (b) of the target
("when the watch IS alive it stays the performer") silently false in exactly
the layout seats run in.

**What changed** — one line in `heal.py`:
```python
sess = locations.shared_sessions_dir(root)   # was locations.sessions_dir(root)
```
The heartbeat is watch→rotate state, which lives in the shared room by the
same rule as pins/mail/rotation records. One room, one path — no fallback that
reads both, no weakening of either resolver. Best-effort preserved (still
wrapped in try/except; never raises into the watch). No rotate.py changes —
the reviewer-level defect was provably on the heal side, so only the writer
half was edited.

**Regression test** — added
`extensions/agi/tests/test_heal_watch.py::test_heartbeat_lands_in_shared_room_across_worktrees`.
It stubs `locations.git_common_root`/`find_project_root` so the two graph
roots (a worktree and its main checkout) fork into DIFFERENT rooms, calls
`heal._write_watch_heartbeat(wt_graph)`, and asserts the heartbeat lands in
the SHARED room (not the per-worktree fork) AND that `rotate._watch_alive(wt_graph)`
reads it ALIVE from the main-checkout resolver. A test that could only pass
once the writer and reader agree.

Item 3 (recording `deferred_to: watch` in the record) was deliberately skipped:
it would risk changing the `after_join` key semantics, which must stay ABSENT
when nobody performed. Not worth bending (c).

## Evidence

**Before/after resolver disagreement for one worktree root** (stubbed seam):
```
PRE-FIX heal wrote  : /tmp/demo-wt-graph/sessions/reaper.watch.json
rotate always reads : /tmp/demo-main-graph/sessions/reaper.watch.json
agree?  False
POST-FIX heal writes: /tmp/demo-main-graph/sessions/reaper.watch.json
```

**The regression test FAILS on the pre-fix resolver** (proved the defect is
real, not hypothetical):
```
        heal._write_watch_heartbeat(wt_graph)
        hb = shared / "reaper.watch.json"
>       assert hb.exists(), \
            f"heartbeat must land in the SHARED room {shared}, not a worktree fork"
E       AssertionError: heartbeat must land in the SHARED room /tmp/.../main-graph/sessions, not a worktree fork
E       assert False
FAILED test_heal_watch.py::test_heartbeat_lands_in_shared_room_across_worktrees
1 failed, 34 passed in 0.67s
```

**...and PASSES after the fix:**
```
python3 -m pytest extensions/agi/tests/test_heal_watch.py -q
...................................                                      [100%]
35 passed in 0.92s
```

**Full related suite, both files green:**
```
python3 -m pytest extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_heal_watch.py -q
80 passed in 16.63s
```

## Falsifier check

Claim (b) — "when the watch IS alive it stays the performer" — now survives a
worktree layout: the worktree-rooted watch's heartbeat lands in the shared
room the rotation seats read, so `_watch_alive` is True and the tail defers.
The regression test holds the writer and reader to the SAME room, so the two
halves cannot disagree again through this seam.

<!-- THOUGHT:BEGIN -->
One-line fix (sessions_dir → shared_sessions_dir) in the writer half only.
The reviewer's diagnosis landed on heal.py:885; rotate.py was already reading
the shared room, so no second-half edit was needed — editing both would have
re-introduced the two-resolvers hazard. Regression test stubs the git_common_root
seam rather than building a real second worktree (too heavy for a fixture);
the stub forks the two graph roots into genuinely different rooms, so the test
cannot pass unless writer and reader agree. Item 3 skipped: recording a
`deferred_to` would bend the `after_join`-key-absent invariant that kid 2's T5
relies on.
<!-- THOUGHT:END -->

## Agent Notes
Fixed watcher-heartbeat room mismatch: heal._write_watch_heartbeat now writes via shared_sessions_dir (was sessions_dir) so a linked-worktree watch's heartbeat lands where all rotation seats read it; regression test fails pre-fix, passes after; 80 pass across handover+watch.

PARENT REVIEW (a00-4125554d, SL7.72): accepted, verdict proved. I confirmed the defect myself before the kid ran: locations.sessions_dir vs shared_sessions_dir fork for a worktree root (printed both for .agi/worktrees/seat-sensei-director/.agi — per-worktree vs main checkout); pre-fix heal.py:885 wrote the fork, rotate reads the main room. Re-read the fix (heal.py:_write_watch_heartbeat now locations.shared_sessions_dir(root)) and the regression test (test_heal_watch.py:1306) — non-vacuous: it asserts the stubbed seam actually forks the rooms before asserting the heartbeat lands in the shared one and _watch_alive reads it True from the worktree root. Re-ran test_heal_watch.py + test_rotate_handover.py + test_after_join_service.py: 100 passed. Item 3 (recording the deferral decision) correctly skipped — it would have bent the after_join-key-absent invariant.
