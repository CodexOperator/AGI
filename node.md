---
id: experiment:a00-35abe797-d129d3
mint_id: 90b764625ba747668d6a49db7b8bdf13
type: experiment
parents:
  - hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-lands-inert
next_edges: []
confidence: 0.7
edited_by: a00-b1d92d36
evidence_runs:
  - experiment:a00-35abe797-d129d3
loop: hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-lands-inert@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fb14374958b0e11b
season: 2
title: A00 35abe797 d129d3
town: core
verdict: inconclusive_lean_proved:70
---
## Experiment

I-3a-2 Region A: the v3 TOWN-FIRST **planning** for `cli.py branch-reshuffle --kinds main,towns,posts` (extensions/agi/bin/cli.py). Built these helpers in the branch-reshuffle region:

- `_rs_town_set(root)` (cli.py:3020) — TOWN SET. Uses `towns.town_tuples(root)` when a `town:*` node exists; on ONLY `towns.TownError` falls back to the **ladder.md `towns:`** list derived via `_rs_ladder_towns` (cli.py:3000), town_season core=2 / every other town=1, global_season from ladder `current_season`. Prints which source ("town set: ..."). Any other exception re-raises. App-town names are NEVER hardcoded (satisfies goal:g8.2 / test_no_literal_town — the guard failed my first literal-table version and forced this).
- `_rs_v3_towns_plan` (cli.py:3054) — per tuple the trunk-pair CREATE pairs `<town>/main`, `<town>/season<s>/main`, every target through `branches.derive_names`, tip = the town's live v2 main (core → season<gs>/main; other towns → season<gs>/<town>/season<s>/main).
- `_rs_v3_town_push` (cli.py:3102) — the push line: `branches.assert_remote_visible(name)` is called FIRST and raises BY NAME on a non-visible name, then prints `git push -u origin <name>`. The falsifier.
- `_rs_v3_posts_renames` (cli.py:3074) — live `season<n>/posts/<p>` → `<core>/season<n>/posts/<p>/main` local-only renames (derive_names post_main), NO push, upstream UNSET line.
- `_rs_v3_run` (cli.py:3116) — emits the whole main/towns/posts plan ([DRY ] in dry mode; performs in apply mode). Wired into cmd_branch_reshuffle: dry-only call in the plan section + in the no-legacy-branches early-return (so the v3 plan still prints when there are no legacy rename jobs); the v3 APPLY execution is deliberately deferred (planning-only this round — the parent/Prime applies the v3 tree).
- `--dry-run WRITES NOTHING`: replaced the dry-run `_rs_save_plan` write with an apply-only + explicit-new-`--plan-out PATH` model (`_rs_write_plan_file` cli.py:2955, writes the plan to the named FILE path atomically). `--apply`: baselined to apply-only; `--plan-out` honored even with zero legacy jobs.
- Kept: `--dry-run --apply` refused; blank/empty `--kinds` refused by name; `master` add-only in main; `--delete-old` set unchanged (derived from is_remote_visible + foreign/master carve-outs).

Fixture repo (real git + fake bare origin + graph root) with **both** town-set sources: a `town:*` node fixture (core/streaming-suite/web-app-suite) and a no-town ladder fallback. Season2/main + two season2/<town>/season1/main + two season2/posts/<p> heads on origin.

## Evidence

Commands + results (from the round's worktree, all git cwd-bound to tmp fixtures):

```
python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_branch_reshuffle_v3.py extensions/agi/tests/test_branches.py extensions/agi/tests/test_branches_v3.py extensions/agi/tests/test_branch_spelling_grep.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_towns.py extensions/agi/tests/test_no_literal_town.py -q
=> 175 passed in 24.39s
```

Representative dry-run plan (no-town fixture, `--kinds main,towns,posts`):

```
  town set: town:* nodes (3 towns)          # or "ladder fallback (3 towns; no town:* node)"
  v3 town creates (3 towns):
    [DRY ] branch create (v3): git branch core/main season2/main
[DRY ] branch push (new): git push -u origin core/main
    [DRY ] branch create (v3): git branch core/season2/main season2/main
...
    [DRY ] branch create (v3): git branch streaming-suite/main season2/streaming-suite/season1/main
    [DRY ] branch create (v3): git branch web-app-suite/main season2/web-app-suite/season1/main
  v3 post renames (local, no push, 2 branch(es)):
    [DRY ] branch rename (local, v3): git branch -m season2/posts/sanctuary-director core/season2/posts/sanctuary-director/main
    [DRY ] branch upstream (unset, v3): git branch --unset-upstream core/season2/posts/sanctuary-director/main
  v3 main: season<n>/main stays (remote-visible); master add-only, kept (frozen season-1 name)
```

New hermetic tests added to test_branch_reshuffle_v3.py: town-set source (both paths), planned names == derive_names outputs, every planned push names a remote-visible branch, post renames local-only derive_names targets with upstream unset and NO push lines, main keep line, and `--dry-run` writes NOTHING while `--plan-out` writes exactly the named file. Test 4 rewritten (old `test_plain_dry_run_writes_only_the_plan_file` → `test_plain_dry_run_writes_nothing`). Two v2 origin-moved tests updated to capture their baseline via `--plan-out` (the new explicit path).

## Agent Notes

## Agent Notes
Region A v3 town-first PLANNING landed (cli.py _rs_town_set/_rs_v3_towns_plan/_rs_v3_posts_renames/_rs_v3_town_push/_rs_v3_run + --plan-out, --dry-run writes nothing). 175 tests green incl 7 new hermetic fixture tests. v3 APPLY + live (b) proof deferred to parent; crons mirror is region C.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (L4.334): accepted lean_proved:70, NOT proved. (1) WHAT THE BRIEF SAID: region A only -- v3 town-first planning for kinds main/towns/posts, town set from towns.town_tuples with a ladder fallback, every target through branches.derive_names, assert_remote_visible before every push, --dry-run writes nothing, plus fixture tests. (2) WHAT THE MACHINE ACTUALLY DOES: the parent re-ran the kid 45-test set (test_branch_reshuffle.py + test_branch_reshuffle_v3.py: 45 passed in 21.38s) and re-ran the real-tree `cli.py branch-reshuffle --dry-run --kinds main,towns,posts` in this worktree -- it printed "town set: ladder fallback (3 towns; no town:* node)", the six trunk-pair creates with every push line gated by branches.assert_remote_visible, the three local post renames to core/season2/posts/<p>/main with upstream unset, and no sessions/*.json appeared (dry-run wrote nothing). (3) THE NEAR MISS: a plan that prints the v3 names but keeps the OLD dry-run write of sessions/branch-reshuffle-plan.json would satisfy "plans the tree" in words and lose the "writes nothing" clause; the kid removed that write and updated the test that had asserted it, and the parent confirmed the sessions dir stayed clean. Likewise a push line that prints `git push` without calling assert_remote_visible first would look right and lose the falsifier; the fixture test parses every push line back through branches.is_remote_visible. (4) WHAT IS NOT DONE: --apply does NOT perform the v3 plan (kid deferred it, and the node says so), so the target PROOF item "--apply on the fixture yields exactly the planned refs / worktree HEADs follow / no upstream" is unmet; region B (loops) and region C (crons mirror) untouched. That gap is exactly why this is 70 and not proved, and kid B is re-briefed to close item (1).
<!-- THOUGHT:END -->
