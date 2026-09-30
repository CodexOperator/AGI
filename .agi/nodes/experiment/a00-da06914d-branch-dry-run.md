---
id: experiment:a00-da06914d-branch-dry-run
type: experiment
parents:
  - hypothesis:a00-da06914d-d133b6
edited_by: a00-da06914d
loop: goal:g1.31.4.1@s2
title: A --branch dry run names the branch, base and worktree, resolved not re-derived
---
# experiment:a00-da06914d-branch-dry-run

The run behind hypothesis:a00-da06914d-d133b6. Bytes, not prose:

| probe | how it was run | result |
|---|---|---|
| wire | `test_dry_run_names_branch` — printed branch re-derived through `dispatch.loop_branch_name(target, agent, 2)`; worktree through `dispatch.branch_worktree_link`; base through `dispatch.spawner_base_branch(cwd)` | pass (a changed resolver fails the assertion) |
| gate | same dry run without `--branch` | no `  branch: ` line — not decoration |
| auth | scratch `git init` + `checkout --detach <sha>`, dispatch run with that cwd | exit 0, `base=NONE (detached HEAD — a live --branch spawn would refuse)`, premise asserted (resolver is None there) |
| no side effect | `test_dry_run_branch_creates_no_worktree` — `.agi` listing unchanged, no `.agi/worktrees/` | pass |
| live | `dispatch.py . DG5.01 --tier kid --target hypothesis:a00-da06914d-d133b6 --branch --dry-run` | `branch: season2/loops/hypothesis-a00-da06914d-d133b6-dry00-8411b9a2 base=season2/loops/goal-g1.31.4.1-a00-1c745a92 worktree=/data/work/agi/.agi/worktrees/dry00-8411b9a2`, exit 0 |

Suites: `test_dispatch_dry_run.py` 30 passed; with `test_ram_worktrees.py`,
`test_dispatch.py`, `test_dispatch_alarms.py`, `test_shared_state_worktree.py`,
`test_suite_live_checkout_worktree.py`, `test_rotate_spawn_worktree_cwd.py` —
205 passed. production_lines 38 / ceiling 40.
