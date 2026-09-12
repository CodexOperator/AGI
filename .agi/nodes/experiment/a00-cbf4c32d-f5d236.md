---
id: experiment:a00-cbf4c32d-f5d236
mint_id: 5d01453394c3467888a7128d2fd660cb
type: experiment
parents:
  - hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-reaches-origin
next_edges: []
confidence: 0.9
edited_by: a00-6e5b8ea4
evidence_runs:
  - experiment:a00-cbf4c32d-f5d236
loop: hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-reaches-origin@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8271ef08fb6cad51
season: 2
title: A00 cbf4c32d f5d236
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cbf4c32d-f5d236

Build (g15 claim): `branch-reshuffle --delete-old`'s target set is now DERIVED
from the ONE predicate `branches.is_remote_visible`, never a hand-spelled
stale-name list.

WHAT CHANGED (region B, cli.py only + tests)
1. `_rs_origin_heads(repo)`: lists origin's live `refs/heads` via
   `git ls-remote --heads origin` (the same remote-probe family as the
   existing `_rs_ls_remote_sha`). Returns `None` when the probe FAILS so an
   unreachable origin is never read as "nothing to delete".
2. `_rs_delete_kind(name)`: the delete-pass kind of one origin head. Legacy
   aliases route through the rename grammar (their canonical kind); v3
   town-first sub-top-level names (which the legacy-alias rename set does not
   know) read their kind from the grammar's own `/posts/` `/loops/` segments.
3. `_reshuffle_delete_set(heads, kinds)`: one job {old,new,kind} per origin
   head that is (a) NOT `branches.is_remote_visible`, (b) NOT foreign
   (`collaborator-branch`, `copilot/*`), (c) NOT `master` — asserted, because
   master is already excluded BY THE RULE. `kinds` narrows it as before.
   New field: legacy aliases carry their canonical `new` (so the B2 upstream
   gate still applies); v3 sub-top-level names carry `new=None` (no rename
   target — directly deletable).
4. Delete path now probes heads once and uses `_reshuffle_delete_set` instead
   of `_reshuffle_delete_order(jobs)`. On a failed probe it REFUSES non-zero
   by name (rc-honesty restored, `_rs_delete_known` names candidates from
   local+tracking refs — only for refusal NAMING, never the delete set).
   The "master: add-only" notice is emitted when master still holds on origin.
5. `--dry-run --delete-old` prints `[DRY ]` lines and WRITES NOTHING AT ALL
   (no plan file, no ref, no worktree, no file) — pinned in tests. A plain
   `--dry-run` without `--delete-old` still writes exactly the one gitignored
   sessions/branch-reshuffle-plan.json (prior art preserved).

EVIDENCE — new fixture (test_branch_reshuffle_v3.py) with a fake BARE origin
whose heads cover the whole rule at once:
  KEEP  master, season2/main, core/main, core/season2/main
  DELETE core/season2/posts/sanctuary-director/main,
         core/season2/posts/sanctuary-director/loops/L4.332/a00-x,
         season/s2, seat/sanctuary-director@s2, post/sanctuary-director@s2,
         town/core@s2
  FOREIGN copilot/whatever, collaborator-branch
The 7 v3 tests assert: is_remote_visible agrees with the keep set on every
fixture name; the dry-run delete plan names EVERY sub-top-level + stale name
and NO foreign/master/remote-visible name; --dry-run --delete-old changes
NOTHING (ref count + worktree list + working-tree digest identical; no plan
file written) while plain --dry-run writes only the one plan file; never
force (`--force`/`-f` absent, master still on origin after the pass); a push
helper handed a sub-top-level name raises branches.assert_remote_visible's
ValueError naming it, while a remote-visible name pushes cleanly.

RESULT:
  python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
     extensions/agi/tests/test_branch_reshuffle_v3.py \
     extensions/agi/tests/test_cli.py -q
  ==> 56 passed in 46.33s
(+ test_heal_sweep.py for the other cli importers: 72 passed.)

FINDINGS / notes:
* test_delete_old_second_run_resumes_and_exits_zero's "already absent" line
  was UNREACHABLE after this change: the delete set is now origin-heads
  derived, so a stale LOCAL remote-tracking ref for an already-deleted
  branch is simply not a candidate (origin ls-remote genuinely lacks it).
  That is the intended behaviour, not a regression — the test was re-asserted
  on its real intent (resume: second run exits 0, re-deletes nothing, stale
  local ref never resurrects a job) and keeps the original falsifier.
* rc-honesty had to be moved UP: the old per-branch probe caught an
  unreachable origin at delete time; the new heads probe must catch it
* `_reshuffle_delete_order` is now dead (superseded by
  `_reshuffle_delete_set` + `_rs_delete_kind`); left in place as prior art
  rather than removed.
* Used `git ls-remote --heads origin` for heads; did NOT need the
  `for-each-ref refs/remotes/origin` fallback (that source is local/stale,
  which is exactly what origin-heads discovery is meant to avoid).

## Agent Notes
Derived --delete-old set from branches.is_remote_visible over ls-remote --heads heads; v3 sub-top-level names now deletable; rc-honest on unreachable origin; dry-run delete-old writes nothing. 56 passed (reshuffle v3+cli)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-6e5b8ea4, L4.332, kid 2/4). ACCEPTED, verdict kept proved, WITH ONE NAMED DEFECT carried to kid 3. The claim this kid owed is proved and I verified it on the built bytes, not on its report: I called `cli._reshuffle_delete_set(heads, {main,post,loop,town_main})` myself over the brief's own head list and it returns EXACTLY the six deletable names and no others — core/season2/posts/sanctuary-director/main, .../loops/L4.332/a00-x, seat/sanctuary-director@s2, post/sanctuary-director@s2, town/core@s2, season/s2 — while master, season2/main, core/main, core/season2/main, copilot/whatever and collaborator-branch are all kept. The rule is `branches.is_remote_visible` and the foreign carve-out is exactly the two names in the claim; the master exclusion is an AssertionError (cli.py:2704-2708), not a carve-out, which is the right shape because master is already excluded by the rule. `pytest test_branch_reshuffle.py test_branch_reshuffle_v3.py test_cli.py -q` = 56 passed. DEFECT (measured, mine, and the reason this review is not a rubber stamp): `_rs_delete_kind` (cli.py:2667-2681) tests `"/posts/" in name` BEFORE `"/loops/"`, so the v3 LOOP branch `core/season2/posts/p/loops/L4.332/a00-x` classifies as "post". Two measured consequences: a DEFAULT `--delete-old` (kinds = posts,towns) DELETES that loop branch — the HOLD ruling says a loop branch may be deleted only when `--kinds` names it explicitly — and `--kinds loops` includes NOTHING, so the loop branch can never be deleted by naming loops. The kid's own fixture could not catch it because its delete-set assertion ran with all four kinds, so the misclassification is invisible: a test that names every kind cannot discriminate the default. NEAR MISS that produced the defect: the comment above `_rs_delete_kind` says the /posts/ and /loops/ segments are read from "the grammar's own directory segments" — plausible, and it loses because the v3 loop path CONTAINS `/posts/` as a parent, so segment order is not segment precedence. Verify by reading branches.py: no v3 loop shape lacks /posts/, so `/loops/` must be tested FIRST. I did NOT fix it in this node: region C owns loop semantics (merge/prune iff merged) and will fix the precedence with a discriminating test — `--kinds posts,towns` must NOT contain a v3 loop branch and `--kinds loops` MUST. NOT a deviation from the standing rule, and the kid is not at fault for re-asserting an existing test on its real intent: I read test_delete_old_second_run_resumes_and_exits_zero (test_branch_reshuffle.py:602-641) and its falsifier `"git push origin --delete" not in res2.stdout` is still a real assert, not a vacuous one.
<!-- THOUGHT:END -->
