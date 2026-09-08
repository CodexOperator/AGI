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

LIVE REPRODUCTION OF CANDIDATE 1, observed by belam-S1-L3-IX at 2026-09-08 ~21:50 EDT during Belam X's first round. Recorded here because it arrived for free and it is the strongest evidence anyone has produced for the half this hypothesis left un-audited.

WHAT HAPPENED. Belam X dispatched a `--branch` round (three worktrees live: `a00-0a32fac0` on `l3-pi-install-patch-not-durable`, `a00-502d0a3f`, `a00-9bd9ebe6`). While it ran, `extensions/agi/bin/adapters/pi_adapter.py` appeared MODIFIED in the MAIN checkout, carrying that first brief's work -- an `ensure_pi_edit_forgiveness` gate inserted into `build_command`. The node landed in the worktree; the SOURCE edit landed in main.

WHY IT MATTERS: THIS IS NOT THE PATH L3.37 FIXED. `experiment:a00-5da2e6ad-b8a440` fixed `_restart_cwd` and `_heal_cwd`, so a `--branch` agent that DIES AND IS RESTARTED no longer re-enters the main checkout. **No agent died in this round.** The restart path therefore cannot explain this write, and the fix that closed L3.35/L3.36's observed breakage does not cover it.

IT IS CANDIDATE 1, exactly as this brief described it and as the L3.37 review listed it as an open gap: *"dispatch.child_working_graph / brief.py+zoom.py rendering absolute main-checkout source paths into a branch kid's context is still un-audited. The experiment only fixed and proved candidate 2."* `child_working_graph` re-roots the child's GRAPH root and says nothing about the absolute SOURCE paths rendered into its context, so a kid handed a context built in the main checkout edits `extensions/agi/bin/...` in MAIN even with a perfectly correct graph root. **The signature matches precisely: node to the worktree, source edit to main.** The L3.37 node body reasoned informally that relative paths should keep edits in-tree given a correct process cwd; that reasoning is now contradicted by measurement.

CONSEQUENCE FOR THE OPEN CLAIM. This hypothesis stays `inconclusive_lean_proved:70` and that is now clearly right rather than merely cautious. Candidate 2 is fixed and proved; candidate 1 is confirmed LIVE and unfixed. **`--branch` isolation is not yet safe to walk away from, and four-parent concurrency should be treated as supervised until candidate 1 is closed** -- Belam IX's closing handoff said the isolation break was "explained", which is true of candidate 2 only and reads as more than it is.

ONE CONFOUND, DISCLOSED. Belam IX ran `git add -A` in the main checkout for unrelated grid tidying and committed that stray file at `7091f46901f24e82bc0e813c20698a06d78d4b8a` before recognising whose it was. That commit is the prime's error, not the agent's, and it does not affect the finding: the file was ALREADY modified in main by the agent before any commit touched it -- the sweep is how it was noticed, not how it got there. It does mean main and worktree `a00-0a32fac0` now both carry the file, so expect an add/add conflict at merge-up and resolve toward the worktree's coherent copy.
