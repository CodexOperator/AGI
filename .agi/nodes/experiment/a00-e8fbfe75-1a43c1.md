---
id: experiment:a00-e8fbfe75-1a43c1
mint_id: e45fb05738c343789bfd68856913f90e
type: experiment
parents:
  - hypothesis:l4-a-finished-rounds-worktree-is-removed-after-harvest
next_edges: []
confidence: 0.9
edited_by: a00-300b7907
evidence_runs:
  - experiment:a00-e8fbfe75-1a43c1
loop: hypothesis:l4-a-finished-rounds-worktree-is-removed-after-harvest@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 009b7779b90d12e3
season: 2
title: A00 e8fbfe75 1a43c1
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e8fbfe75-1a43c1

## Experiment

Parent correction (a00-300b7907): the previous kid's `_sweep_finished_worktrees` liveness guard was fail-OPEN. heal.py had:

    try:
        live_ids = {r.get("agent_id") for r in
                    spawn_budget.live_agents(root) if r.get("agent_id")}
    except Exception:  # unreadable budget -> keep everything
        live_ids = set()

`live_ids = set()` treats every agent as dead, so EVERY worktree (including a
merged+clean+grace-old LIVE one) proceeds past condition (1) into the removal
decision — the opposite of the comment. `spawn_budget._budget_lock` can raise
OSError on a read-only/full/permission-denied budget dir, so the except IS
reachable. This is the exact falsifier: a worktree removed while its lease is
live, when the budget read transiently fails.

Fix (fail-CLOSED): on any exception reading `spawn_budget.live_agents(root)`, log
`[sweep] skipped: budget unreadable (<exc>)` and return `(0, 0, 0)` — the whole
sweep is skipped this pass, every worktree stays. No `live_ids = set()`; no
removal window. Nothing else in the five conditions, the `--dry-run` path, the
`sweep` subcommand, or the `_watch` hook site changed.

Test added to `extensions/agi/tests/test_heal_sweep.py`:
`test_sweep_unreadable_budget_fails_closed` monkeypatches
`heal.spawn_budget.live_agents` (the module object heal bound at its import
— not the test's separately-loaded `spawn_budget`) to raise RuntimeError, runs the
sweep over the four-worktree fixture with zero grace, and asserts `(0,0,0)`, that
the merged+clean+homed `a00-aaaa11` worktree is STILL PRESENT, its loop branch
`loop/n-A@2` still exists, and that a `[sweep] skipped: budget unreadable (` line
was logged.

## Evidence

    python3 -m pytest extensions/agi/tests/test_heal_sweep.py -q
    .....  [100%]    -> 5 passed
    python3 -m pytest extensions/agi/tests/test_heal.py extensions/agi/tests/test_heal_sweep.py -q
    ... 19 passed
    python3 -m pytest extensions/agi/tests/test_heal_watch.py -q
    ... 15 passed

All heal-suite tests green; the new failure-mode test proves the falsifier is
neutralized (live-lease worktree survives an unreadable budget).

## Agent Notes
fail-closed liveness guard: unreadable spawn-budget now skips whole sweep via [sweep] skipped + return (0,0,0); new test proves a00-aaaa11 survives with branch intact. test_heal_sweep 5p, test_heal 19p, test_heal_watch 15p all green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW a00-300b7907 (parent, L4.253). Kept at proved. WHAT THE CORRECTION SAID (quoted from the re-brief): "make an unreadable budget fail-CLOSED: when spawn_budget.live_agents(root) raises, SKIP the entire sweep for this pass -- log one line [sweep] skipped: budget unreadable (<exc>) and return (0, 0, 0)." WHAT THE MACHINE DOES (heal.py:560-570, read after the kid): the except now logs a skipped line and returns (0, 0, 0); no live_ids=set() path survives. The five conditions, the --dry-run path, the sweep subcommand and the _watch hook site (after _run_pending_after_joins, before the once check) are unchanged. THE EVIDENCE, RUN BY THE PARENT, NOT TAKEN ON REPORT: python3 -m pytest test_heal_sweep.py test_heal_watch.py -q -> 20 passed. The new test_sweep_unreadable_budget_fails_closed monkeypatches heal.spawn_budget.live_agents (the module object heal bound at import -- the right one, not the test file separately-loaded copy) to raise, runs the sweep over the four-worktree fixture, and asserts (0,0,0) plus that a00-aaaa11 and its loop/n-A@2 branch survive. NEAR MISS avoided here: patching the test file own spawn_budget copy would leave the sweep binding untouched and the test would pass vacuously; the test names the aliasing trap in its own comment. Falsifier (a worktree removed while its lease is live) now neutralized for the reachable transient-budget-failure path.
<!-- THOUGHT:END -->
