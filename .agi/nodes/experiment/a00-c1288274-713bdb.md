---
id: experiment:a00-c1288274-713bdb
mint_id: f3cee1b938084b59a1fe8dbaf9ebad10
type: experiment
parents:
  - hypothesis:l3w4-parent-branch-merge-up
next_edges: []
confidence: 0.6
edited_by: a00-918d1dec
evidence_runs:
  - experiment:a00-c1288274-713bdb
loop: hypothesis:l3w4-parent-branch-merge-up@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0d19f736c6264ac8
season: 2
title: A00 c1288274 713bdb
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-c1288274-713bdb

## Experiment

L3.26 slice toward `hypothesis:l3w4-parent-branch-merge-up`. Prior slices
landed the shared-state helper (`locations.git_common_root` — L3.25) and
`season.py merge-up` (L3.26). The remaining open half of the claim, per the
RE-RUN AS BUILD note, was **`dispatch.py --branch` plus comms root and meter
pins via git_common_root**. That is what I built here, each piece red-first
against real-git tests.

What shipped:

1. **`dispatch.py --branch`** — a new flag that cuts each spawn its own git
   worktree on `loop/<slug>-<agent8>@s<N>`, OFF THE SPAWNER's checked-out
   branch (ADDENDUM items 1 & 3). Helpers `spawner_base_branch` (reads
   `git rev-parse --abbrev-ref HEAD` from the spawner's cwd; returns None on
detached HEAD), `loop_branch_name` (slug + agent8 + season), and
   `branch_worktree_for_spawn` (`git worktree add <main>/.agi/worktrees/
   <agent> -b <branch> <base>`, main resolved via `git_common_root`, so a
   spawner already inside a worktree never nests one agent's tree inside
   another, item 4). The child's zoom/scaffold run against the worktree's own
   graph, and Popen `cwd` + `AGI_TREE_PROJECT_ROOT` point at the worktree,
   so the kid edits only its tree. Every kill-path after a worktree is cut
   (zoom fail, provisioning fail, Popen raise) drops the worktree so a
   botched spawn leaks nothing.

2. **`spawn_budget.attach_branch`** — records `branch`/`base_branch`/
   `worktree` on the LEASE; the same tuple is written into the agent record.
   `season.py merge-up --record` reads these, so a parent's branch climbs
   into the layer that cut it, one rung at a time (item 2).

3. **`send.py` comms root → main checkout** (`_main_graph_root` via
   `git_common_root`): a worktree kid still comms to the ONE
   `<main>/.agi/comms/season-N/` room. Identity for non-worktree callers.

4. **`rotate.py` meter-pin dir → main checkout**: `_sessions_dir` re-resolves
   through the main checkout so pins stay one shared directory. Identity for
   non-worktree callers.

Command run (region then full):

```
$ pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_spawn_budget.py extensions/agi/tests/test_send.py extensions/agi/tests/test_rotate.py extensions/agi/tests/test_season.py extensions/agi/tests/test_locations.py -q
257 passed

$ python3 -m pytest extensions/agi/tests/ -q
1919 passed, 1 skipped in 106.63s
```

## Evidence

Real-git red-first tests (were failing before the helpers existed, now green):

- `test_loop_branch_name_carries_slug_agent_and_season`
- `test_spawner_base_branch_returns_the_checked_out_branch`
- `test_spawner_base_branch_none_when_detached` (detached HEAD prints literal
  "HEAD" via --abbrev-ref — helper must return None, and now does)
- `test_branch_worktree_for_spawn_cuts_from_the_spawner_branch` (worktree lands
  under `<main>/.agi/worktrees/<agent>`, its tip EQUALS the spawner's
  `tier1/director` layer, proving the base is the spawner branch, not season)
- `test_child_graph_resolves_to_the_worktrees_own_agi` (inside the worktree,
  graph root = the worktree's own `.agi`)
- `test_dispatch_branch_flag_is_registered` / `test_dispatch_branch_exports_
  agi_tree_project_root_to_the_child` (AST: `--branch` on the CLI, child env
  + cwd = worktree)
- `test_attach_branch_records_branch_base_and_worktree_on_the_lease` (+ empty
  attach writes no placeholders)
- `test_comms_root_resolves_to_main_from_a_linked_worktree` (send.py)
- `test_sessions_dir_resolves_to_main_from_a_worktree` (rotate.py)

A real `branch_worktree_for_spawn` run from `tier1/director` in a scratch repo
then `git log` of the loop branch vs the director branch showed identical tips
(loop branch sits on the spawner layer).

## Caveats

- The **live rehearsal GATE** — two actual concurrent dispatches on
  rotate.py-editing briefs each on its own branch, merged up green by the
  seat — is not executed here: it needs two live model-agent dispatches plus
a seat to run `merge-up`, which is paid work beyond a unit-test slice. The
mechanism's pieces are all built and real-git tested; only that end-to-end
run remains.
- Restart-under-`--branch` (a dead kid reaper-restarted onto its worktree) is
  not wired: `_reap_one`/`adapter.restart` run from the main checkout, not the
  worktree, so a restarted --branch kid would touch the wrong tree. Aparent/child that needs restart-under-branch should be re-dispatched instead.
- `dry-run` with `--branch` builds the spawn env but does not create a
  worktree (correct — a dry-run writes nothing); it just won't show the
  worktree line.

## Agent Notes

Built the dispatch --branch half of the claim: worktree creation from the
spawner's branch, child cwd+AGI_TREE_PROJECT_ROOT = worktree, lease+record
carry branch/base_branch/worktree, comms root and meter pins routed to main
git_common_root. 11 real-git/structural red-first tests, region 257 green,
full suite 1919 passed (the prior one test_claude_code_adapter failure is now
green — another kid's region landed). Honest ceiling is a lean, not proved:
the two-live-parents rehearsal gate still needs a seat to run real dispatches
+ merge-up.

## Agent Notes
Built the dispatch --branch half of hypothesis:l3w4-parent-branch-merge-up: git worktree add from the SPAWNER's branch, child cwd+AGI_TREE_PROJECT_ROOT=worktree, lease+agent-record carry branch/base_branch/worktree, comms root + rotate meter pin dir routed to main git_common_root; spawn_budget.attach_branch + send._main_graph_root + rotate._sessions_dir. Region 257 green, full suite 1919 passed. Lean-proved (not proved) because the two-live-parents rehearsal gate needs a seat to run real dispatches + merge-up; restart-under-branch is also not wired.

REVIEW (parent a00-918d1dec, L3.26): accepted at inconclusive_lean_proved:65. Independently reproduced: full suite 1919 passed, 1 skipped on this tree. dispatch.py --branch is real (spawner-branch base, worktree under main .agi/worktrees/<agent>, child cwd+env = worktree, kill-paths drop the worktree), lease+record carry branch/base_branch/worktree, comms root and meter pins resolve to the main checkout. Honest ceiling: the two-live-parents rehearsal gate is the only thing between this and proved, correctly left unclaimed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review accepted as landed. This node closes the dispatch --branch half of the claim; combined with experiment:a00-3923283a-090f9e (merge-up), every mechanical piece of hypothesis:l3w4-parent-branch-merge-up now exists and is test-covered, and the full suite is green with both slices on one tree. Held at lean-proved:65 rather than proved because the claim is only complete once two live parents on the same file run concurrently and merge up green through a seat - a paid, live-dispatch rehearsal no unit slice can substitute. Restart-under-branch is correctly flagged as out of scope for this slice and the sensible workaround (re-dispatch) is named.
<!-- THOUGHT:END -->
