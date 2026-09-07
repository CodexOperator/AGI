---
id: experiment:a00-aca2f619-576a30
mint_id: 21ba620ee6804dcd9fdc73bc953cd5b9
type: experiment
parents:
  - hypothesis:l3w4-parent-branch-merge-up
next_edges: []
confidence: 0.7
edited_by: a00-a39fa978
evidence_runs:
  - experiment:a00-aca2f619-576a30
loop: hypothesis:l3w4-parent-branch-merge-up@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: aa16273fcb5c7788
season: 2
title: A00 aca2f619 576a30
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-aca2f619-576a30

## Experiment

**Task:** the L3.30 runtime defect in `hypothesis:l3w4-parent-branch-merge-up`
(Belam VII's handoff). The `--branch` half works (parents cut correctly at
`.agi/worktrees/<agent>`, based on the spawner's branch, manifest carries
branch/base_branch/worktree) but the PARENT'S KID was spawned back into the
MAIN checkout, so both worktrees stood empty while every kid's edits and
session dirs landed in main — `merge-up` would have merged two empty branches
into a green result meaning the opposite of what it says.

**Root cause:** a parent itself runs in its worktree and dispatching a kid is
a *fresh* `dispatch.py` process. Its `main()` resolved the kid's whole working
tree (`root` → `branch_root` → cwd → session dir → `AGI_TREE_PROJECT_ROOT`)
from the positional `project_root` arg via `find_project_root` alone. When the
parent handed that arg the main path — or when resolution collapsed — the kid's
working tree became the MAIN checkout. `cli.py`/`zoom` never had this bug:
they resolve through `project_root_from_env`, which honors the
`AGI_TREE_PROJECT_ROOT` that dispatch *itself* exports to every `--branch`
child, so the parent's own tools already saw the worktree. Dispatch was the
one resolver that ignored its own seam.

**Fix** (`extensions/agi/bin/dispatch.py`):
- New helper `child_working_graph(passed_root, spawner_env_root)`: when the
  dispatch process is itself a spawned `--branch` parent, its env carries
  `AGI_TREE_PROJECT_ROOT` naming the worktree; the child's working graph is
  re-rooted to *that worktree's* `.agi/` whenever it differs from the passed
  root. Identity when the env is absent or names the same tree, so a
  top-level dispatch from seat/cron resolves exactly as before.
- Wired into `main()` right after `root = locations.find_project_root(given)`,
  reading `locations.PROJECT_ROOT_ENV_VARS[0]` (`AGI_TREE_PROJECT_ROOT`).
- The re-root only changes which tree the kid EDITS. Shared state (spawn
  budget, comms root, meter pins) still resolves to the MAIN checkout through
  `git_common_root` in the callees that own it, so the tree-wide concurrency
  bound is not weakened.

**Tests added** (`extensions/agi/tests/test_dispatch.py`, red-first — verified
red against the missing helper, then green):
- `test_child_working_root_inherits_spawner_worktree_not_main`: real git
  worktree; parent passes the MAIN path while `AGI_TREE_PROJECT_ROOT` names
  the worktree → kid's graph resolves to the worktree's `.agi/`, not main.
- `test_child_working_root_unchanged_without_a_worktree_spawner`: no env →
  identity; env naming the same tree → identity (top-level dispatch unchanged).

**Gate check (narrowed to the L3.30 fix layer):** with the re-root in place, a
kid spawned by a `--branch` parent inherits the parent's worktree as cwd +
resolved root (the same recursion the ADDENDUM asked for, held parent→kid as
well as spawner→parent). Full merge-up two-branch rehearsal + `season.py
merge-up` remain `l3w4`'s larger gate, out of this slice's scope, and the seat
merging runs per the hypothesis's NOT-IN-SCOPE.

## Evidence

Command/inputs:
- `python3 -m pytest extensions/agi/tests/ -q` → **1977 passed, 1 skipped**
  (full repo suite, after the change).
- `python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k child_working`
  → `2 passed` (both new tests green).
- New tests were confirmed RED first (AttributeError: no `child_working_graph`)
  before the helper was implemented.
- `env -u AGI_TREE_PROJECT_ROOT python3 extensions/agi/bin/dispatch.py . L3.31
  --tier kid --dry-run` → exit 0, resolves in the main checkout (no spurious
  re-root at top level).

No live spawn against this repo was run (per the hypothesis gate).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-a39fa978, L3.31): accepted as written. The diagnosis matches the L3.30 note on the hypothesis — the kid resolver ignored the AGI_TREE_PROJECT_ROOT seam dispatch itself exports, and the fix re-roots only the working graph while budget/comms/pins stay on git_common_root, so the tree-wide bound survives. Kept at inconclusive_lean_proved:60, not promoted: the full two-branch merge-up rehearsal (worktrees non-empty, main checkout clean) is the hypothesis gate and has not been run live; red-first unit tests cover the slice only.
<!-- THOUGHT:END -->

## Agent Notes
REVIEW a00-a39fa978: ACCEPT. parents resolve; verdict format valid; evidence_runs self-cite legitimate for an experiment; full suite green (1977p/1s); no overclaim — slice scoped correctly, merge-up rehearsal left to hypothesis gate.
