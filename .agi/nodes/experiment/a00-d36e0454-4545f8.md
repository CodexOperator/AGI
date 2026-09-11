---
id: experiment:a00-d36e0454-4545f8
mint_id: d3aad29ca78040f5baff644799b842dc
type: experiment
parents:
  - hypothesis:l4-stall-candidate-measures-an-api-bound-parent-honestly
next_edges: []
confidence: 0.9
edited_by: a00-ca59f20b
evidence_runs:
  - experiment:a00-d36e0454-4545f8
loop: hypothesis:l4-stall-candidate-measures-an-api-bound-parent-honestly@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3fd5b663dcffb54e
season: 2
title: "Window-paid-once: 3-row round finishes in one sample window"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d36e0454-4545f8

## Experiment

The defect (inherited from the parent's measurement): `_round_status` in
`extensions/agi/bin/spawn_budget.py:610-624` slept inside the per-row loop
(`time.sleep(_STATUS_SAMPLE_SECONDS)` per row), so the tick-sample window was
paid once PER ROW. A 2-row round cost 16 s wall, a 5-agent round 40 s — and
`status --iter` is the very command the director runs when a round may be
stalled. This experiment fixes that, minimal and verdict-identical.

Change (file scope: `_round_status` only): take `t0 = _pid_ticks(pid)` for
ALL rows first, sleep `_STATUS_SAMPLE_SECONDS` ONCE, then re-read all rows
and compute each delta. No threads, no subprocesses — a pure reordering.
Every pid still sits under the full window, so the claim the target makes
("the tick sample is 8 s") stays true. Verdict logic, helpers, and the
printed line format untouched. Net wall time = one window regardless of
round size.

```python
pids = [int(rec.get("agent_pid") or rec.get("holder_pid") or 0)
        for rec in rows]
t0s = [_pid_ticks(pid) for pid in pids]
time.sleep(_STATUS_SAMPLE_SECONDS)
deltas = [max(0, _pid_ticks(pid) - t0) for pid, t0 in zip(pids, t0s)]
for rec, pid, ticks in zip(rows, pids, deltas):
    ...  # unchanged: sockets, status, totals, print line
```

New test added to `extensions/agi/tests/test_spawn_budget.py`:
`test_status_iter_samples_tick_window_once_for_many_rows` — a round of 3
live fixture rows with `_STATUS_SAMPLE_SECONDS` left at a real 0.2 s (not
the near-zero seam) must complete in `< 2 * window` (0.4 s). Pre-fix serial
code costs 3 * 0.2 = 0.6 s and fails; concurrent code costs ~0.21 s.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q
................................
32 passed in 1.35s
```

All 31 pre-existing tests green (including the two falsifiers —
`ticks>0` and `sockets>0` both print `reviewing`, never STALL-CANDIDATE),
plus the one new timing test = 32 total. The concurrent fix passes wall
clock well under the 2x-window bound because the single shared sleep is
paid once; a serial re-run of the same 3-row round would take 3 windows
and trip the assertion, which is how the test proves the fix.

## Agent Notes
Reordered _round_status tick sampling to pay the 8s window ONCE per round; 3-row timing test proves <2x window; 32/32 tests green

PARENT REVIEW (a00-ca59f20b, L4.177) — ACCEPTED, verdict proved stands. Artifact check: spawn_budget.py:610-624 now takes `t0s = [_pid_ticks(pid) for pid in pids]`, then ONE `time.sleep(_STATUS_SAMPLE_SECONDS)`, then `deltas = [...]` — a pure reordering of _round_status, no threads/subprocesses, verdict logic and line format untouched. Ran `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q` -> 32 passed in 1.29s; both prior falsifiers still green. The new test at :635 is a real discriminator: 3 live rows under a 0.2 s window must finish in < 0.4 s; pre-fix serial sleeps cost 0.6 s and trip the assertion. Scope check by mtime: only spawn_budget.py, test_spawn_budget.py and the node changed. No demotion, no caveat carried forward.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION DIFFERS FROM THE KID'S: the kid proved its own fix on its own test; this version carries the parent's independent check of the reordering and confirms no regression in the sibling claim. (1) THE INSTRUCTION SAID: the target claims the tick sample is 8 s and a reviewing parent is not called a STALL-CANDIDATE; the parent measured that the delivered _round_status paid that window once PER ROW (2 rows = 16 s wall), so a 5-agent round cost 40 s exactly when a stall is being investigated. (2) THE MACHINE ACTUALLY DOES: verified at spawn_budget.py:610-624 — all t0 reads first, one shared sleep, then all t1 reads; ran the suite, 32 passed, and the new test at :635 fails if the sleeps are serial (< 0.4 s bound vs 0.6 s serial). Every pid still sits under the full 8 s window, so the target's own claim is preserved rather than traded away. (3) THE NEAR MISS: an implementation that "fixes the cost" by shortening the window to 8/NN s, or by sampling only the parent, would satisfy the words "status --iter is fast" and lose the mechanism — the window IS the director's stall definition, and shrinking it reintroduces the very false-CANDIDATE class this target exists to kill. The kid did not do that; it kept the window and removed the repetition. (4) DEVIATION FROM A STANDING RULE: none — fix-only, file scope respected, no git run. WHAT IS STILL WEAK: the timing test asserts wall-clock, so on a machine loaded past 0.4 s it could flake; the margin (2x the window) is generous but not machine-independent.
<!-- THOUGHT:END -->
