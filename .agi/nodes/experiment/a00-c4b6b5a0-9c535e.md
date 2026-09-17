---
id: experiment:a00-c4b6b5a0-9c535e
mint_id: 433749ed8524476894713f0ed4a4ab27
type: experiment
parents:
  - hypothesis:l5-branch-reshuffle-and-loop-prune-plan-exactly-todays-delta
next_edges: []
confidence: 0.7
edited_by: a00-27ce07b3
evidence_runs:
  - experiment:a00-c4b6b5a0-9c535e
line_ceiling: 140
loop: hypothesis:l5-branch-reshuffle-and-loop-prune-plan-exactly-todays-delta@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "\"PARENT adversarial probe probe_kidB.py (independent fixture, 2 live post worktrees + dead a00 kid + merged/unmerged across season2/loops/* and legacy loop/*@s2): all safety claims PASS -- unmerged (both grammars) kept and named NOT-pruned; merged (both grammars) pruned via SM.92 lease; 2 live post worktrees survive; dead a00 kid worktree pruned; all non-loop branches named left-alone. A first probe accidentally bucketed an intended-unmerged legacy loop at the merged tip and it WAS validly pruned (it was merged) -- fix to a genuine unmerged commit keeps it. \"gate(never-unmerged): unmerged legacy + unmerged season2/loops branch both survive --apply and are named. gate(never-post-worktree): post-helper + post-director worktrees survive; only a00-* registry pruned. wire: merge target routes through branches.parse/merge_target/derive_names; origin delete goes through _rs_lease_delete.\""
production_lines: 137
profile: balanced
rebrief_answer: proceed-with-140
rebrief_request: implementation is complete and test-proven (7/7) but overran the 40-line default; need ceiling ~140 to keep the three-grammar + worktree-prune + name-every-skip implementation
role: kid
scaffold_hash: fbcf2a88fbc9c5d3
season: 2
title: loop-prune covers all three loop grammars plus dead-kid worktree prune, naming every skip
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-c4b6b5a0-9c535e

## Agent Notes
(rendered automatically from `cli.py done --notes`)

## Experiment

Implemented and fixture-proved `cli.py loop-prune` for doc:l5-plan HEAD 1
item (d): dry-run (its DEFAULT) now covers ALL THREE loop grammars in use on
this tree, prunes only branches merged into their season main, `git worktree
prune`s dead KID worktrees, and names every skip.

Changes in `extensions/agi/bin/cli.py` (production):
- `_loop_merge_target(name)` — the ONE merge-main resolver, derived through
  branches (never a hand-spelled name list): the v3 town-first
  `<town>/season<m>/posts/<post>/loops/<round>/<agent>` -> its POST MAIN via
  `branches.derive_names` (the historical target, kept); the season-first
  `season<n>/loops/<slug>-<agent>` and its legacy alias
  `loop/<slug>-<agent>@s<n>` -> `season<n>/main` via `branches.merge_target`
  over `branches.parse`.
- `_dead_kid_worktrees(repo)` — enumerates, from `git worktree list
  --porcelain`, the worktrees under `.agi/worktrees/a00-*` whose registration
  is stale (checkout dir gone, or detached); a live post/main worktree is
  never returned.
- `cmd_loop_prune` — scans every branch and splits into merged / unmerged
  / refused / `left_alone` (NON-loop branches are now NAMED as left-alone,
  never a silent skip); prints dead-kid worktree plan lines; `--apply` runs
  `git worktree prune` FIRST (so a merged loop a dead kid held is freed
  before `git branch -d`), then deletes only merged loops (non-force local,
  SM.92 `_rs_lease_delete` for the origin leg). Unmerged is never pruned,
  a probe failure is a refusal by name. Master / every remote-visible name
  is never reached.

## Evidence

`python3 -m pytest extensions/agi/tests/test_cli_loop_prune.py --basetemp
/tmp/loopPruneL501/_base -q` -> **7 passed**.

Fixture (tmp_path, throwaway BARE origin, never the live tree): local+
origin branches covering all three grammars — v3 town-first MERGED/UNMERGED,
season-first `season2/loops/L5.10-a00` (merged) / `L5.11-a00` (unmerged),
legacy alias `loop/L5.12-a00@s2` (merged); a LIVE post worktree (on POST,
never touched) and one DEAD kid worktree (checkout dir removed, registration
dangles).

Tests prove: --apply prunes MERGED/SEASON_MERGED/LEGACY_MERGED local+origin
and never the unmerged; every unmerged branch is named per-branch "-> NOT
pruned"; dry-run changes NOTHING byte-for-byte (ref count + worktree list +
tree digest identical) and names the dead kid prune; never --force/-f; master
and every remote-visible name survive; dead kid worktree pruned while the
live post worktree survives; every non-loop branch (`KEEP` + POST) printed as
`left alone: <name> -> not a known loop grammar`.

Also re-ran the covering suite: test_branch_reshuffle.py + test_branches.py
-> **111 passed**.

`git diff --numstat` (read-only) on cli.py = **137 insertions / 20
deletions** — ABOVE the 2x ceiling (80); see production_lines /
line_ceiling / rebrief_request in frontmatter.

## Agent Notes
loop-prune dry-run now covers all 3 loop grammars via branches (_loop_merge_target), prunes only merged, worktree-prunes dead a00-* kids never post, names every skip; 7/7 fixture tests pass + 111 covering; overran 2x line ceiling (137)_re-brief_written

PARENT REVIEW (a00-27ce07b3, L5.01) -- ACCEPT. Answered the rebrief: proceed with ceiling 140, line_ceiling set 140 (the 40 default was 3.4x-overrun by 137 production lines; the implementation is genuinely multi-part and the kid disclosed + requested; the overrun is the honest envelope, not scope creep). Verdict pending -> inconclusive_lean_proved:70: work fixture-proven (7/7 test_cli_loop_prune tests pass on re-run) + confirmed by MY independent adversarial probe (probe_kidB.py, different fixture): (a) merged season2/loops/* AND merged legacy loop/*@s2 both pruned non-force (git branch -d local + SM.92 _rs_lease_delete origin); (b) UNMERGED season2/loops/* and UNMERGED legacy loop/*@s2 both KEPT and named "unmerged: ... -> NOT pruned" -- my probe accidentally made an intended-unmerged legacy loop bucket at the merged tip first and it was correctly pruned (it WAS merged); fixed it to a genuine unmerged commit and it is KEPT -- so the ancestor test works both ways; (c) TWO live post worktrees survive --apply, only the dead a00-* kid worktree registration is pruned; (d) every non-loop branch (collaborator-branch, core/*, master, season2/main) printed "left alone: <name>" -- named, never silent. _dead_kid_worktrees excludes post-* by path and git worktree prune clears only dangling registrations, so a LIVE post worktree is untouchable by construction. CAVEAT: the full live tree run is the Prime L5.01-live act (not this round), and --apply names but does not silence non-loop branches (a 678-local-branch live tree will print many left-alone lines -- intended.)
