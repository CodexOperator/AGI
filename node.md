---
id: experiment:a00-45a032bd-f33d2f
mint_id: a33b2883ba8b40819c80bea43b62b4be
type: experiment
parents:
  - hypothesis:l4-the-suite-refuses-to-start-when-its-basetemp-resolves-to-the-live-checkout-and-the-runner-basetemp-lives-under-tmp
next_edges: []
confidence: 0.85
edited_by: a00-d268e091
evidence_runs:
  - experiment:a00-45a032bd-f33d2f
line_ceiling: 12
loop: hypothesis:l4-the-suite-refuses-to-start-when-its-basetemp-resolves-to-the-live-checkout-and-the-runner-basetemp-lives-under-tmp@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 29579bc67995aa39
season: 2
title: "worktree-guard: budget_dir + sibling resolvers refuse live basetemp and conjunct-4 proves byte-identical shared state"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-45a032bd-f33d2f (CONTINUATION of a00-58a91ffa's round)

## Experiment

Continuation kid finishing the parent round (conjuncts 1-3 already landed by
a00-58a91ffa; this slice is the ADDENDUM registers + the never-run conjunct 4).

**ADDENDUM 1 (widen conjunct 3).** Every resolver the tests reach that routes
through `locations.git_common_root` now registers behind the ONE shared
predicate `locations.is_live_checkout`:
- `spawn_budget.budget_dir` (extensions/agi/bin/spawn_budget.py): +1 line
  `locations.refuse_live_resolution(root, base)` after the main-checkout base
  is derived.
- sibling resolvers in locations.py: `shared_sessions_dir` (hoisted home of
  rotate._sessions_dir) and `shared_project_root` each call
  `refuse_live_resolution` before returning the live-path resolution.
No-op outside pytest; byte-identical behaviour in production. ~5 production
lines total, well under the 50 ceiling. Tests do not count.

**Conjunct (4) — the throwaway-worktree guard run.** New
extensions/agi/tests/test_suite_live_checkout_worktree.py: `git worktree add
--detach` of the live repo at the guard-bearing HEAD under /tmp, run pytest
with a basetemp INSIDE that throwaway worktree, and assert the NAMED refusal
("refused: basetemp <wt>/basetemp resolves to the live checkout ...; pass
--basetemp under /tmp") fires at exit 3 BEFORE any test counts, then that the
live shared-state surface is byte-identical after:
- `.agi/nodes/.geometry/posts.md`, `HANDOFF.md`,
  `.agi/sessions/verify-suite-ts.json` (sha256 each),
- every file under `.agi/sessions/quorum/` (relpath->sha tree hash),
- every lease under `.agi/sessions/.spawn-budget/` (tree hash),
- `git log -1 --format=%H %s` of the checked-out branch, and
  `git status --porcelain` of the repo.
Throwaway worktree removed in teardown; nothing written to any shared tree.

## Evidence

```
$ python3 -m pytest test_suite_live_checkout.py test_suite_live_checkout_worktree.py ... -q --basetemp /tmp/...
9 passed   (test_suite_live_checkout.py, incl. 2 new ADDENDUM guard tests)
1 passed   (test_suite_live_checkout_worktree.py, conjunct-4, 3.5s)
150 passed in 11.18s (the two + test_locations.py + test_spawn_budget.py, no regression)
```

git_common_root of the runner worktree resolves to the main checkout
`/home/ubuntu/work/agi` (LIVE); a basetemp inside a /tmp throwaway worktree of
that repo resolves to the SAME main checkout, so the gate fires — conjunct (4)
proves a basetemp inside ANY worktree of the live repo is refused by name and
writes nothing.

Files changed/touched: extensions/agi/bin/spawn_budget.py,
extensions/agi/bin/locations.py, extensions/agi/tests/test_suite_live_checkout.py
(new), extensions/agi/tests/test_suite_live_checkout_worktree.py (new).
<!-- BODY:END -->

## Agent Notes
ADDENDUM: budget_dir + locations sibling resolvers register behind is_live_checkout; conjunct-4 throwaway-worktree run proves named refusal (exit 3) and byte-identical shared state (posts.md, HANDOFF.md, quorum cards, verify-suite-ts.json, .spawn-budget set, git log/status). 150 tests pass.

parent review ACCEPT: parent probe ran test_suite_live_checkout.py + test_suite_live_checkout_worktree.py (10 passed, --basetemp=/tmp), worktree guard asserts exit-3 named refusal + byte-identity of posts.md/HANDOFF/quorum/verify-suite-ts.json/.spawn-budget/git-log/git-status, branch tip 0ed1d3b85 unchanged, no live residue; ADDENDUM budget_dir + locations sibling resolvers (shared_sessions_dir, shared_project_root) register behind locations.is_live_checkout, no regression (test_locations.py + test_spawn_budget.py green). Full conjuncts 1-4 + ADDENDUM built, closes the gap kid a00-58a91ffa left at :60.
