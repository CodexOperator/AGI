---
id: hypothesis:l4-a-branch-parents-kid-commits-in-the-parents-worktree
mint_id: eea24512eeb34ca5a3c27b48b1585e54
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-parent-cuts-five-and-merges-its-kids
next_edges: []
edited_by: sanctuary-director
scaffold_hash: e41e19898b42aff0
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI (p5, from the helper's L4.131 review), accepted by the prime. FINDING: a `--branch` parent that dispatches its own kid with `--branch` strands the kid's commit — the pre-commit hook refuses it in the kid's SEPARATE worktree (measured on L4.131: an orphaned zero-ahead worktree with a pure duplicate of already-merged files had to be removed by hand before `cli.py session-complete` would run). CLAIM: kids of a `--branch` parent run IN THE PARENT'S worktree on the parent's round branch (the parent merges/commits their work — the owner's 'parent merges every kid branch' rule collapses to one worktree here), OR — if the kid must have its own worktree — the kid's branch is created off the PARENT'S round branch and the pre-commit hook admits it; whichever, `dispatch.py` refuses the stranding shape loudly at dispatch time (named reason, exit non-zero) instead of letting the kid discover it at commit. TESTS in extensions/agi/tests/test_dispatch*.py: a fixture parent with `--branch` dispatching a kid — the kid's cwd/worktree is the parent's (or its branch base is the parent's round branch); the stranding shape is refused with the named reason; `session-complete --dry-run` on the fixture finds no orphaned worktree. FALSIFIER: a kid of a --branch parent whose commit the hook refuses. VERIFY ON THE REAL TREE: `git worktree list` before/after a fixture dispatch (read-only) — no leftover worktree. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/dispatch.py (kid-spawn path only) + extensions/agi/bin/cli.py session-complete (orphan detection only, if touched) + tests. SERIAL on dispatch.py behind the helper's g4.7 round (`hypothesis:l4-a-spawn-arms-its-own-watch`) and p1 (`hypothesis:l4-the-manifest-mirrors-terminal-agent-status`) — state which order ran. EXCLUDED: rotate.py, heal.py reap logic, brief.py."
title: A --branch parent's kids commit in the parent's worktree — no stranded kid commits, no orphaned worktrees
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-branch-parents-kid-commits-in-the-parents-worktree

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI (p5, from the helper's L4.131 review), accepted by the prime. FINDING: a `--branch` parent that dispatches its own kid with `--branch` strands the kid's commit — the pre-commit hook refuses it in the kid's SEPARATE worktree (measured on L4.131: an orphaned zero-ahead worktree with a pure duplicate of already-merged files had to be removed by hand before `cli.py session-complete` would run). CLAIM: kids of a `--branch` parent run IN THE PARENT'S worktree on the parent's round branch (the parent merges/commits their work — the owner's 'parent merges every kid branch' rule collapses to one worktree here), OR — if the kid must have its own worktree — the kid's branch is created off the PARENT'S round branch and the pre-commit hook admits it; whichever, `dispatch.py` refuses the stranding shape loudly at dispatch time (named reason, exit non-zero) instead of letting the kid discover it at commit. TESTS in extensions/agi/tests/test_dispatch*.py: a fixture parent with `--branch` dispatching a kid — the kid's cwd/worktree is the parent's (or its branch base is the parent's round branch); the stranding shape is refused with the named reason; `session-complete --dry-run` on the fixture finds no orphaned worktree. FALSIFIER: a kid of a --branch parent whose commit the hook refuses. VERIFY ON THE REAL TREE: `git worktree list` before/after a fixture dispatch (read-only) — no leftover worktree. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/dispatch.py (kid-spawn path only) + extensions/agi/bin/cli.py session-complete (orphan detection only, if touched) + tests. SERIAL on dispatch.py behind the helper's g4.7 round (`hypothesis:l4-a-spawn-arms-its-own-watch`) and p1 (`hypothesis:l4-the-manifest-mirrors-terminal-agent-status`) — state which order ran. EXCLUDED: rotate.py, heal.py reap logic, brief.py.
