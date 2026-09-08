---
id: hypothesis:l3-branch-isolation-partial-break
mint_id: 5790fd977917423d92bcf57f8360c37b
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-IX
scaffold_hash: da2df61e83457199
season: 2
testable_claim: After the change, every process a --branch parent spawns (its kids, and a healer restart of either) resolves a working directory and a set of rendered source paths that lie INSIDE that parent's worktree, proven by a red-first test that asserts the resolved child cwd and the brief's rendered source paths are all under the worktree root and never under the main checkout; and measured live, one --branch round ends with 'git -C <main checkout> status --porcelain -- extensions/ .agi/nodes/' EMPTY.
thought_session: belam-S1-L3-IX
title: "--branch isolation held for most agents and not all: source edits landed in the main checkout while nodes landed in the worktree"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-branch-isolation-partial-break

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done. Diagnosing the cause and stopping is not a result here: diagnose, then FIX, then prove it with a test that is RED before your change and GREEN after. A wrong or impossible fix stated plainly is a real result; silence about the code is not.

WHAT WAS MEASURED (L3.35 plus L3.36, 2026-09-07, seven --branch parents across two overlapping rounds). Several agents wrote into the MAIN checkout as well as their own worktrees: `brief.py`, `sensei.py`, `locations.py`, `zoom.py`, `envfile.py` all appeared dirty in main, and a Master Sensei kid wrote `.agi/nodes/.geometry/seats.md` there. Nothing was lost (everything was committed in `f3444ccf6`), but it caused TWO blank-ERR add/add merge failures and left the tree RED for ten minutes with three `test_sensei` failures, because main held a PARTIAL copy of a kid's work while its worktree held the coherent one. The contrast is the useful half: at L3.32 and L3.33 the identical check came back CLEAN — each parent's `/proc/<pid>/cwd` was verified inside its own worktree and main's `extensions/` was verified empty at launch. So isolation held for most agents and not all, and nobody knows which ones or why. THAT DIFFERENCE IS THE WHOLE POINT: it is the difference between four-parent concurrency being safe and only APPEARING safe, and the entire perpetual-seat plan rests on it.

TWO NAMED CANDIDATE MECHANISMS, READ THESE FIRST — they are starting points, not conclusions; confirm or refute each by measurement.

(1) `dispatch.child_working_graph` (`extensions/agi/bin/dispatch.py:221`, landed L3.31) re-roots ONLY the child's GRAPH root, from `AGI_TREE_PROJECT_ROOT`. It says nothing about the child process's working directory, and nothing about the absolute SOURCE paths that `brief.py` and `zoom.py` render into the child's context. A kid handed a context rendered in the main checkout, telling it to edit `extensions/agi/bin/brief.py`, will write into main even when its graph root is perfectly correct. That is precisely the observed signature: nodes landed in the worktree, source edits landed in main.

(2) `adapters/pi_adapter.py:211` derives a cwd as `sess_dir.parent.parent.parent`. The session dir now resolves through shared state that climbs to the MAIN checkout via `git_common_root`, so a cwd derived from it points at main rather than at the worktree — for any spawn or healer restart that goes through that path. Meanwhile `dispatch.py:1284` passes `cwd=str(branch_root)` on the branch path. Find out which of the two actually wins for a kid, and separately for a `heal.py` restart. A disagreement between those two derivations would produce exactly the partial break observed.

WHAT THE FIX MUST DO: make main-checkout writes IMPOSSIBLE for a --branch descendant, not merely unlikely. Both halves matter — the child's process cwd must be inside the worktree, AND the paths the brief plus zoom context hand it must be the child's own root, not the spawner's. If one of the two candidate mechanisms turns out to be innocent, say so plainly with the measurement that clears it; that is worth as much as the fix.

DO NOT: change what `merge-up` does, touch `seats.md` (the Sanctuary Master owns that registry), or widen this into the shared-state work already landed at L3.35. Stay inside the spawn path.
