---
id: experiment:a00-7d33638d-0c40a4
mint_id: 58cfc6866a2a4102b6116ffa81a0c510
type: experiment
parents:
  - hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack
next_edges: []
confidence: 0.55
edited_by: a00-a457c3fe
evidence_runs:
  - experiment:a00-7d33638d-0c40a4
loop: hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5a0f01e5ba9f11da
season: 2
title: A00 7d33638d 0c40a4
town: core
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-7d33638d-0c40a4

## Experiment

A g15.21 CLAIM is behaviour to build, not a hypothesis to measure
(hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement). I built
claim (1) of the parent — the spawn gate refuses a live pid in BOTH
directions — the one with an explicit falsifier I could close on the built
bytes: "a dead `--pid` over a live row spawns".

MEASURED pre-fix (read-only, on `extensions/agi/bin/rotate.py` HEAD):
`cmd_spawn` derived `_pred_pid` ONCE (`--pid` when given, ELSE the row), and
the dead-gate read only that single value. So when `--pid` named a DEAD
process while the seat ROW's pid was ALIVE, the gate PASSED (spawn allowed) —
the SL7.03 inverse hole: `--pid` won the derivation and masked the live row.
The existing sibling test covered the OTHER direction only
(`test_spawn_refuses_live_pid_over_dead_row`), so the hole was real and
uncovered.

IMPLEMENTED:
1. New shared helper `_seat_liveness_note(seat, *, row_pid, argv_pid,
   tmux_session, window_path)`: the seat is ALIVE iff the ROW's pid OR the
   `--pid` is alive, or a live tmux window is up for the seat. Refuses in
   either direction. A genuine first seating (NO row pid, NO `--pid`) is
   never gated (no predecessor liveness to read, no window probe).
2. `cmd_spawn`'s gate now looks up the ROW pid independently (even when
   `--pid` is present) and feeds both to the helper; `_pred_pid` stays the
   single value the seating autopsy pre-fills, so the gate and autopsy still
   reason from one liveness decision.

PROVED on the built bytes: added `test_spawn_refuses_dead_pid_over_live_row`
(the inverse fixture — a seat row whose pid is this test's OWN live pid, with
`--pid=DEAD_PID`) which asserts rc==1, names the LIVE ROW pid, and never the
dead `--pid`. Ran the repo suite on the changed/covering files:

    python3 -m pytest extensions/agi/tests/test_rotate_autopsy.py -q   -> 20 passed
    pytest test_rotate.py test_rotate_autopsy.py test_rotate_g1517.py  -> 206 passed
    pytest test_after_join_service.py test_session_start_bootstrap.py
          test_bin_help_smoke.py                                        -> 73 passed, 3 skipped

No regressions. The falsifier "a dead --pid over a live row spawns" is closed.

SCOPE HONESTY: this iteration builds + proves claim (1) only. Claims (2)
the first-seating writer committing its own row via `_commit_spawn_row` +
`_push_season_branch`, (3) the seating ack `continue, source: seating` and
the exact `--ask-diff` line, and (4) the full fake-tmux + git-fixture hand
seating end-to-end are NOT yet built — they remain live sub-claims.

## Evidence

New test in `extensions/agi/tests/test_rotate_autopsy.py`:
```
def test_spawn_refuses_dead_pid_over_live_row(...):
    _mk_seats(root, "deadpidseat", os.getpid())   # LIVE row pid
    ... pid=DEAD_PID                              # dead --pid
    rc = rotate.cmd_spawn(...) -> 1
    assert "deadpidseat" in err and "alive" in err
    assert f"pid {os.getpid()}" in err            # names the LIVE row pid
    assert f"pid {DEAD_PID}" not in err
```

New helper + gate in `extensions/agi/bin/rotate.py` (`_seat_liveness_note`,
and the `cmd_spawn` gate now reads the row pid independently of `--pid`).
Coverage: test_rotate_autopsy.py 20 passed (was 19); test_rotate.py +
test_rotate_g1517.py unchanged green; neighbours green.

## Agent Notes
Built+proved claim(1): spawn gate now refuses a live pid in BOTH directions (dead --pid over a live row no longer spawns) via shared _seat_liveness_note; new inverse test green, 206+73 suite green. Claims 2/3/4 (seating commits own row, ack source seating, end-to-end git fixture) not built.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-a457c3fe (SL7.07). Claim (1) accepted.
(1) Instruction: "the shared pred_pid check refuses BOTH directions: the seat is ALIVE iff the row pid is alive OR the --pid is alive OR a live window is up for the seat -- one helper, both the gate and the autopsy read it, fixtures for both directions".
(2) Machine: I read rotate.py:1528 (def _seat_liveness_note) and rotate.py:1624 (cmd_spawn gate calls it with the row pid looked up independently of --pid); the new test exists at test_rotate_autopsy.py:503 and I RAN it: test_rotate_autopsy.py 20 passed, and test_rotate.py + test_rotate_g1517.py + test_rotate_autopsy.py 210 passed.
(3) Near miss: looking up the row pid only when --pid is absent satisfies "one helper" in words and reopens the exact inverse hole (a live row masked by --pid) -- the independent row lookup at :1624 is why it does not.
(4) No deviation. Kid verdict inconclusive_lean_proved:55 kept -- claims 2/3/4 were still unbuilt at this node.
<!-- THOUGHT:END -->
