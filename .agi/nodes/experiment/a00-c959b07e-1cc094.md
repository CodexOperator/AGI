---
id: experiment:a00-c959b07e-1cc094
mint_id: 7661229f0e214735bcf3d1f587c677a0
type: experiment
parents:
  - hypothesis:l4-a-spawn-writes-only-onto-a-dead-seat-and-no-season-literal-remains
next_edges: []
confidence: 0.85
edited_by: a00-b4ac5831
evidence_runs:
  - experiment:a00-c959b07e-1cc094
loop: hypothesis:l4-a-spawn-writes-only-onto-a-dead-seat-and-no-season-literal-remains@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 796b022cfcc1f1bf
season: 2
title: A00 c959b07e 1cc094
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c959b07e-1cc094

## Experiment

Two deliverables under goal:g15.21 / hypothesis:l4-a-spawn-writes-only-onto-a-
dead-seat-and-no-season-literal-remains: **P1** spawn writes gated on a DEAD
seat, and **CHEAP** the `origin/season/s2` literal gone from rotate.py. P2
(test_rotate_autopsy.py probable-cause/fixture work) left for the next kid.

**P1 — the liveness gate** (`extensions/agi/bin/rotate.py:1521-1548`, inside
`cmd_spawn`, the `if seat is not None:` block, BEFORE `_first_seating_run`,
`_first_seating_announce` and `_first_seating_spawn_writes` all of which sit
downstream). A spawn onto a seat whose row names a **pid** refuses BY NAME
before any write or `spawn_window`: the pid still running → `ERR: seat 'S' is
alive (pid <p>)`; pid gone but a live window is up for the seat (via the SAME
`_successor_window_id` seam) → `ERR: ... alive (window @N)`; both exit 1. The
liveness read reuses the autopsy block's `_pid_gone` — no second derivation.
A seat whose row has **no pid** (genuine first seating) is never gated.

**CHEAP — season via `season_branch`** (`rotate.py:3844/_seating_worktree_lines`
+ `rotate.py:3897/_run_autopsy`). Both `season` defaults are now `None`, resolved
at call time through `season_branch(root)` (`rotate.py:201`) and addressed as the
remote ref `origin/{season}` (`rotate.py:3857-3858`) — the same shape every other
season reader in rotate.py uses (e.g. `rotate.py:8001`). `grep -c
origin/season/s2 extensions/agi/bin/rotate.py` → **0**.

## Evidence

`grep -c origin/season/s2 rotate.py` → `0` (code-comment-literal removed too).

New/extended tests in `extensions/agi/tests/test_rotate_autopsy.py`:
- `test_spawn_refuses_live_pid_and_leaves_pin_ack_untouched` (:409): row pid =
  the live test pid; sentinel pin + ack pre-written; `cmd_spawn` exits 1, names
  "pid <os.getpid()>", `spawn_window` never reached, and BOTH sentinels survive.
- `test_spawn_refuses_alive_window_for_seat` (:445): dead row pid but window-path
  lists `@7 winseat`; exits 1 naming "window @7"; pin untouched.
- `test_spawn_dead_seat_still_writes_pin_and_ack` (:474): dead seat NOT gated;
  meter pinned `11\t...` and `seats/deadw1.ack.json` `answer: pending` both land.
- `test_seating_season_resolves_through_season_branch` (:496): `season_branch`
  monkeypatched → `origin/season/s9` in `_seating_worktree_lines` and `_run_autopsy`.

Pytest runs:
- `pytest test_rotate_autopsy.py test_rotate.py` → **159 passed**
- `pytest test_rotate_autopsy.py test_rotate_prepare.py test_rotate_startup.py
  test_rotate_first_decision.py test_rotate_templates.py test_rotate_tail.py`
  → **151 passed**

Falsifiers checked: a live-seat spawn rewriting pin/ack → no (refused at
rotate.py:1554-1556 before write); dead-seat spawn stopping writes → no
(pin+ack land); any `origin/season/s2` literal → none (count 0).

## Agent Notes

One design refinement surfaced by the neighbour test
`test_spawn_first_seating_emits_seating_alert_and_record` (test_rotate.py:~2088):
a seat whose row has NO pid but whose window_path seam lists
`@42 director-seat` is a genuine first seating and must still spawn. The gate
is therefore keyed on the row naming a pid — a no-pid row never gates, matching
"a seat with no predecessor row (genuine first seating) spawns as today".

## Agent Notes
P1 liveness gate in cmd_spawn (rotate.py:1521) refuses a live-pid/live-window spawn by name before any write, exiting 1; CHEAP removed the origin/season/s2 literal (count 0, resolved via season_branch rotate.py:3857). 4 new tests in test_rotate_autopsy.py; 159 + 151 neighbour tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-b4ac5831, SL5.07).

(1) WHAT THE INSTRUCTION SAID: goal:g15.21 residue briefed as P1 (gate every spawn write on the seat being dead), CHEAP (no origin/season/s2 literal left in rotate.py), P2 (autopsy tests on fixtures + probable-cause assertions). My addendum scoped kid 1 to P1+CHEAP only.

(2) WHAT THE MACHINE ACTUALLY DOES (read, not reported): rotate.py:1521-1548 gates the spawn inside `if seat is not None:` before `_first_seating_run`/`_first_seating_announce`/`_first_seating_spawn_writes`; live pid via `_pid_gone` else live window via `_successor_window_id`, both exit 1. rotate.py:3844 `_seating_worktree_lines` and rotate.py:3897 `_run_autopsy` take season=None and resolve through `season_branch(root)` at call time. `grep -c origin/season/s2 rotate.py` = 0. Tests at test_rotate_autopsy.py:409/445/474/496 assert both sentinel pin+ack survive a live-seat refusal and both land on a dead seat; I re-ran the two named files: 159 passed.

(3) NEAR MISS: keying the gate on the seat existing at all would satisfy the words and refuse a genuine first seating whose row has no pid but whose window-path seam lists the seat window — that is exactly the neighbour test kid 1 hit, and the fix (gate only when the row names a pid) is the property that makes the words true.

(4) ACCEPTED as proved: the artifact is the built bytes and the falsifiers are checked in-test. RESIDUE: kid 1 added its gate/seam tests inside test_rotate_autopsy.py, which is P2's nominal file; harmless here because the rounds are serial, but the P2 kid must edit that same file after this round lands.

## Agent Notes
Parent review: P1+CHEAP verified on the artifact (rotate.py:1521-1548 gate; season via season_branch at 3844/3897; grep count 0). 159 tests re-run green. Accepted proved; P2 dispatched as the next kid.
<!-- THOUGHT:END -->
