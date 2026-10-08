---
id: experiment:a00-c4e4aeb6-8cc557
mint_id: c24117e5141d45a987b3702289df87e1
type: experiment
parents:
  - hypothesis:l3-killed-agent-restarts-unattributed
next_edges: []
confidence: 0.8
edited_by: a00-bc39d4be
evidence_runs:
  - experiment:a00-c4e4aeb6-8cc557
loop: hypothesis:l3-killed-agent-restarts-unattributed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 73dac3346c2e4d7e
season: 2
title: A00 c4e4aeb6 8cc557
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-c4e4aeb6-8cc557

## Experiment

Built the fix under `hypothesis:l3-killed-agent-restarts-unattributed`: a
legitimately restarted agent's lease must be attributable to the round it
belongs to, and `iter=None` on a live lease must be loud.

**Root cause found.** In `dispatch._reap_one` (dispatch.py ~L1619) the restart
lease was acquired WITHOUT an iteration id:

    lease = spawn_budget.acquire(root, cap, f"{agent_id}-r{restarts + 1}",
                                 tier=rec.get("tier", "kid"))

so every `-rN` survivor lease carried `iter=None`. `spawn_budget status` reads
`iter` from the lease, which is exactly how the three measured survivors showed
`iter=None` on 2026-09-08 and held the round open invisibly.

**Fix 1 — dispatch.py `_reap_one`:** pass the round's iteration id into the
restart lease so the replacement is attributable (inherits tier + iter):

    iter_n=locations.iteration_id(rec.get("iter", 0) or 0)

**Fix 2 — spawn_budget.py `status`:** `iter=None` on a live lease is now flagged
loudly (`<-- UNATTRIBUTED: iter is None (restarted lease lost its round)`) so
the unattributed state can never silently count toward a round's liveness.

**Test-first (red):** `test_reaper_restart_inherits_the_iteration_id` failed on
the old code with `iter: None` in the restart lease, asserting instead that the
`-rN` lease carries the round's iter. Two `spawn_budget status` tests pin the
loud `UNATTRIBUTED` marker and the clean attribution for an iter'd lease. Full
engine suite: 2108 passed, 1 skipped, no failures.

## Evidence

Red run before the dispatch fix — a `_reap_one` restart left:

    [{'agent_id': 'a00-abc123-r1', 'tier': 'parent', 'iter': None, ...}]
    AssertionError: restart lease must carry the round's iteration

Green after both fixes — 3 targeted tests passed, then the whole suite:

    2108 passed, 1 skipped in 134.62s

Scope: only `dispatch.py` and `spawn_budget.py` touched (the two files the
brief names as mine). `workflow.py`, `rotate.py`, `brief.py`, `cli.py`,
`zoom.py`, seats and every `belam-*` tmux window untouched. The first two
defects from the hypothesis (window-kill does not stop the agent; a supervisor
revives a deliberate kill) are NOT fixed here — the in-scope, demonstrable
piece is attribution, and the deliberate-kill-vs-crash distinction belongs to
supervision, not the lease seam.

## Agent Notes
Restart lease in dispatch._reap_one was acquired without iter_n, so every -rN survivor carried iter=None and was invisible to its round. Fixed attribution (restart inherits round iter via iteration_id(rec[iter])) and made iter=None loud in spawn_budget status. Red-first unit test; 2108 passed.

PARENT REVIEW (a00-bc39d4be, L3.43): accepted. Verified diff touches only dispatch.py + spawn_budget.py + their tests; 86 tests in both files pass locally. Root-cause (restart lease without iter) and both fixes match the hypothesis attribution clause. Lean 80 honest — window-kill and revival defects explicitly scoped out. No demotion needed.
