---
id: hypothesis:l3-branch-isolation-partial-break
mint_id: 5790fd977917423d92bcf57f8360c37b
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: da2df61e83457199
season: 2
testable_claim: After the change, every process a --branch parent spawns (its kids, and a healer restart of either) resolves a working directory and a set of rendered source paths that lie INSIDE that parent's worktree, proven by a red-first test that asserts the resolved child cwd and the brief's rendered source paths are all under the worktree root and never under the main checkout; and measured live, one --branch round ends with 'git -C <main checkout> status --porcelain -- extensions/ .agi/nodes/' EMPTY.
thought_session: belam-S1-L3-XI
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

LIVE REPRODUCTION, SECOND INSTANCE, AND A SWEEP NOBODY NOTICED — belam-S1-L3-X, 2026-09-08 round L3.39.

Belam IX recorded one candidate-1 write and flagged a second. There were FOUR, from one kid, and one of the two committed sweeps was invisible to the agent that made it.

THE KID: a00-f8f26cd8, brief hypothesis:l3-pi-install-patch-not-durable, confined by --branch to worktree .agi/worktrees/a00-0a32fac0 on loop/hypothesis-l3-pi-install-patch-n-a00-0a32fac0@s2. No agent died this round, so the restart/healer path fixed at L3.37 cannot explain any of it.

THE FOUR FILES, and where each one actually is:
1. extensions/agi/bin/adapters/pi_adapter.py — modified in BOTH the worktree and main. Main's copy was swept into commit 7091f4690 by Belam IX at 21:50:42 EDT. Belam IX found this one and disclosed it.
2. extensions/agi/bin/pi_edit_forgiveness.py — a NEW file in the worktree, and simultaneously written into main, where it was swept into commit 7934251e6 at 21:49:41 EDT. THIS SWEEP WAS NOT KNOWN TO ITS OWN AUTHOR: 7934251e6 is Belam IX's rotation-fix commit, and its message describes only the tmux fix. `git log --diff-filter=A` names it as the commit that added the file. So a kid's source file entered the graph's history inside a commit about something else entirely, with a message that does not mention it.
3. extensions/agi/tests/test_edit_tool_forgiveness.py — modified in both; main's copy still uncommitted at the time of writing.
4. extensions/agi/tests/test_pi_edit_forgiveness.py — new in both; main's copy still untracked. Belam IX flagged this one and correctly left it alone.

THE SIGNATURE IS EXACT AND IT IS CANDIDATE 1. Every NODE this kid wrote went to the worktree (.agi/nodes/experiment/a00-f8f26cd8-26c4a3.md is untracked in the worktree, absent from main). Every SOURCE edit went to main as well as, or instead of, the worktree. Graph root re-rooted correctly; source paths not re-rooted. That is `dispatch.child_working_graph` doing exactly what it says and nothing more, while brief.py and zoom.py render absolute source paths from the checkout they ran in.

WHY IT IS WORSE THAN A LOST DIFF. The bytes are not lost — they are UNOWNED. Main is a shared mutable surface written by three parents' kids, a live prime and a rotated predecessor at once, with no marking of whose bytes are whose. Twice in one hour an agent committed another agent's in-flight work while sincerely believing the tree was its own: Belam IX swept this kid's files into two commits, and Belam X committed Belam IX's live in-progress rotate.py at 21:47:21 believing it was an abandoned orphan from a closed session. Both agents were careful. Both were wrong in the same way, in opposite directions, within three minutes. The defect is not carelessness, it is that `git status` in the main checkout answers a question nobody can act on: it says WHAT changed and never WHO changed it.

CONSEQUENCE FOR merge-up, concretely. A --branch branch that is missing its source edits merges clean and green and delivers nothing — the L3.30 failure mode, reached by a different road. Resolve toward the WORKTREE copy for files 1 and 2, which are the coherent ones, and never rebase.

CORRECTION, belam-S1-L3-X, after the 50-agent deep-search pinned the mechanism. Earlier notes on this node and in Belam IX's DM named zoom.py alongside brief.py as rendering main-absolute source paths into a kid's context. THAT IS WRONG AND ZOOM IS EXONERATED: the rendered context.md, 16654 bytes, contains ZERO absolute paths — grep -c '/home/ubuntu' returns 0 — and names nodes graph-relative. The real mechanism is argv assembly in dispatch.py and brief.py, pinned with the kid's preserved argv and its own reasoning trace, and is now specified for build at hypothesis:l3-branch-source-paths-never-rerooted. Candidate 1 as originally worded was directionally right and specifically wrong about which module.

HARNESS CONSTRAINT FOR THIS ROUND (Belam XI, 2026-09-08, operational — not part of the claim). The `.env` OpenRouter runtime key is at its cap, so `dispatch.py` refuses every pi spawn with `ERR: runtime key ... below the configured floor`. Spawn your kid on the subscription:

    python3 extensions/agi/bin/dispatch.py . L3.42 --target <this node> --level small --tier kid --harness claude-code

Measured this session: `--harness claude-code` on the PARENT invocation does NOT reach the kid — the parent's own dispatch call falls back to the ladder row's pi harness and is refused. Pass the flag explicitly. Do NOT raise the key limit or edit `.env`; that is the owner's decision and it is banked. Do NOT do the kid's work yourself because the spawn was refused — report `pending` and say so, as two parents correctly did earlier this session.

YOU HOLD A BRANCH. You were dispatched with `--branch`, so you are working in your own git worktree on your own `loop/...@s2` branch, cut from the spawner's tip. Commit your kid's work there — a `--branch` parent that lands nothing leaves `merge-up` merging an empty branch and reporting green, which is exactly the defect fixed at L3.40 and never yet exercised live. You are the live proof of that fix. Do not push, do not merge, do not touch `season/s2`; the director merges.

HARNESS CORRECTION — SUPERSEDES THE claude-code CONSTRAINT NOTE ABOVE (Belam XI, 2026-09-08). Owner instruction, verbatim: "Use openrouter" / "Subscription will get drained". The runtime key cap was raised to $15 (usage $5.02, headroom ~$9.98) and pi spawns resolve again. **Run on pi/OpenRouter, not on the subscription.** Your kid:

    python3 extensions/agi/bin/dispatch.py . L3.42 --target <this node> --level small --tier kid --harness pi

Ignore the earlier paragraph telling you to pass `--harness claude-code`; it was written while the key was at its cap and is no longer true. `dispatch.py` resolves the correct cheap OpenRouter slugs by itself (`~z-ai/glm-flash-latest` parent, `~deepseek/deepseek-v4-flash-latest` kid) — that path was never the leaky one.

DO NOT run `workflow.py run` on the pi harness in this round for any reason. The fail-closed model guard that makes it safe landed minutes ago and is not yet merged into your branch. A workflow run before that guard is what burned an entire monthly key cap on `anthropic/claude-sonnet-4.6` (`hypothesis:l3-workflow-model-crosses-harness-namespace`). Rounds are cheap; workflows currently are not.

The BRANCH paragraph above still applies in full: you hold a worktree, commit your kid's work to your own `loop/...@s2` branch, never push, never touch `season/s2`.
