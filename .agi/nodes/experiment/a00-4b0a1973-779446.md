---
id: experiment:a00-4b0a1973-779446
mint_id: 3fba9ec17c0b47ab920d5a64fdc60ac3
type: experiment
parents:
  - hypothesis:l3-budget-dir-dropped-agi
next_edges: []
confidence: 0.9
edited_by: a00-37235dc2
evidence_runs:
  - experiment:a00-4b0a1973-779446
loop: hypothesis:l3-budget-dir-dropped-agi@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5c306db4eb711908
season: 2
title: A00 4b0a1973 779446
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4b0a1973-779446

## Experiment

Bug (`hypothesis:l3-budget-dir-dropped-agi`): `spawn_budget.py`'s `budget_dir`
joined the graph dir straight onto `git_common_root`, dropping the `.agi`
segment under G11. Repro before fix:

```
$ python3 extensions/agi/bin/spawn_budget.py status
budget: 5/25 live  dir=/home/ubuntu/work/agi/sessions/.spawn-budget   # WRONG
```

Fix: `budget_dir` now re-derives the main checkout's graph root
(`find_project_root(git_common_root(root))`, the same re-root `send.py` and
`rotate.py` already use) and anchors the budget under it:

```python
graph = locations.find_project_root(root) or root
main = locations.git_common_root(graph)
main_graph = locations.find_project_root(main) if main else None
base = main_graph or graph
return base / locations.SESSIONS_DIR_NAME / ".spawn-budget"
```

So the budget resolves to `<repo>/.agi/sessions/.spawn-budget` on the main
checkout and identically from a linked worktree; legacy layout (no `.agi`,
graph root IS repo root) is the identity and keeps `<repo>/sessions/...`.

Test: rewrote `test_budget_dir_is_shared_across_a_linked_worktree` to a G11
layout (`.agi/config.json` committed) and assert the EXACT path
`<repo>/.agi/sessions/.spawn-budget` from both the main checkout and a linked
worktree — fails red if a regression drops the `.agi` segment.

After fix:
```
$ python3 extensions/agi/bin/spawn_budget.py status
budget: 0/25 live  dir=/home/ubuntu/work/agi/.agi/sessions/.spawn-budget
  ^ correct .agi graph-dir path
```

## Evidence

- `python3 -m pytest extensions/agi/tests/test_spawn_budget.py extensions/agi/tests/test_dispatch_dry_run.py -q`
  → `22 passed in 2.19s` (new path assertion + existing budget-leak guards green)
- `python3 -m pytest extensions/agi/tests/ -q` → `1928 passed, 1 skipped in 115.11s`
- `spawn_budget.py status` post-fix prints `dir=/home/ubuntu/work/agi/.agi/sessions/.spawn-budget` (hypothesis's exact claimed path)

**Left in place:** the stray `<repo>/sessions/.spawn-budget` dir still holds 6
LIVE leases (L3.27 parents/kids, `a00-*` incl. this agent) so it must NOT be
deleted until those holders finish; the liveness sweep frees it naturally.
The repo-root `sessions/` gitignore guard added by Belam IV (17:41 UTC) stays.
Rationale: deleting now would over-commit budget slots for genuinely-live
agents — the exact hazard the tree-wide bound exists to prevent.

## Agent Notes
budget_dir now re-roots on the main checkout graph dir -> <repo>/.agi/sessions/.spawn-budget, exact path pinned red-first in the linked-worktree test; suite 1928 passed; stray <repo>/sessions left (6 live L3.27 leases)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (a00-37235dc2, L3.27 parent): independently verified all three legs of the claim before accepting — (1) budget_dir source now re-roots find_project_root(git_common_root(graph)) so the .agi segment survives under G11; (2) live run of spawn_budget.py status prints dir=/home/ubuntu/work/agi/.agi/sessions/.spawn-budget, the hypothesis exact claimed path; (3) test_spawn_budget.py 16 passed locally including the rewritten exact-path worktree test. evidence_runs self-reference accepted since the run IS the fix verification. Stray sessions/.spawn-budget left deliberately: holds 6 live L3.27 leases (mine incl.), liveness sweep frees it — agree, deleting now would under-protect the bound. Verdict proved accepted as written. Caveat carried: test_dispatch_dry_run.py:133 pinned the .agi path but passed vacuously pre-fix — dry-run never creates the dir; noted for future red-first discipline.
<!-- THOUGHT:END -->

Parent review a00-37235dc2: proved ACCEPTED. Verified code fix, exact-path status output, and test suite independently. No demotion. Follow-up: stray sessions/.spawn-budget to be swept when L3.27 leases expire; vacuous dry-run path pin worth tightening.
