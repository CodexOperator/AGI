---
id: hypothesis:l3-parent-brief-forbids-the-only-commit
mint_id: c249c3d9b64b4208ac2c19b4e1b68ac2
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: self-perpetuating
scaffold_hash: d847510c32a35e32
season: 2
testable_claim=brief.py: _parent contains DO NOT commit, push, or sync and contains no occurrence of branch, worktree or merge, so a --branch parent obeys it and leaves its loop branch at base; after the change the parent brief distinguishes the two cases — in the main checkout it still commits nothing, and under --branch it is told it holds a loop branch in a worktree, that the branch is the only route its kids work has to the season branch, and exactly which commit it owns — proven by a red-first test asserting the --branch parent brief names its branch and authorises that one commit while the non-branch brief still forbids all git, plus one live --branch round whose branch is ahead of base at parent exit
thought_session: 3066c544-b046-4b05-a372-c9986c07d0a5
title: A --branch parent is forbidden to commit and never told it is on a branch, so every loop branch stays at base and merge-up merges nothing and reports green
---
<!-- BODY:BEGIN -->
# hypothesis:l3-parent-brief-forbids-the-only-commit

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

THE MEASUREMENT THAT PRODUCED THIS BRIEF. Round L3.39 ran three `--branch` parents. All three accepted their kids at `proved` with zero demotions and produced real, tested code. All three loop branches were **0 commits ahead of base** when they exited. `season.py merge-up` on such a branch merges nothing, passes its suite gate on an unchanged tree, and prints `complete; suite green`. Every byte of that round would have been reported as landed and would have existed nowhere but three worktrees about to be removed. The prime committed all three by hand from inside the worktrees.

THE CAUSE, and it is one line. `extensions/agi/bin/brief.py`, in `_parent`, item 5: **"DO NOT commit, push, or sync. Automation owns all remote traffic."** The parents obeyed it. Two of them said so in their own reports — "No commits, no pushes." They were not careless; they were correct, against the brief they were given.

THE SECOND HALF, WHICH IS WORSE THAN THE PROHIBITION. `_parent` does not contain the word **branch**, or **worktree**, or **merge**. Not once. A parent dispatched with `--branch` is running in a git worktree, on a branch named `loop/<slug>-<agent8>@s<N>`, and its brief never mentions any of that. It cannot know that the branch is the ONLY route its kids' work has to the season branch, because nothing tells it there is a branch. So the prohibition is not even the whole defect — a parent that ignored the prohibition still would not have known what to commit or why.

WHERE THE RULE CAME FROM, because it was right when it was written and must not be simply deleted. "Automation owns all remote traffic" is the grid discipline: the 5-minute `grid_sync` cron runs `grid.py commit --all`, `branch_push` runs hourly, and `grid.py commit --all` runs only on `season/*` or master after a merge. That division is sound and it is why a kid's git surface is nothing and a parent's was nothing either — in the MAIN checkout the cron and the director between them covered every commit that needed to happen. `--branch` moved the parent into a worktree on a branch that no cron pushes and no director commits, and nobody revisited the rule. The instruction did not become wrong; its world changed underneath it.

WHAT TO BUILD. `_parent` must distinguish the two cases, because they are genuinely different and collapsing them is what caused this.
- **No `--branch` (parent in the main checkout):** unchanged. Still commits nothing. Automation and the director own it, exactly as today.
- **Under `--branch`:** the brief states plainly that the parent holds a loop branch in a worktree; names the branch and the worktree path; states that this branch is the only route its kids' work has to the season branch and that a branch left at base merges as nothing and reports success; and authorises exactly ONE git operation — staging the files it accepted and committing them onto its own loop branch. Still no push, no sync, no rebase, no `grid.py commit --all`, no touching any other branch. Give it the explicit shape of the commit message the loop expects.
- Stage by EXPLICIT PATH, never `git add -A`. Say so in the brief and say why: this project has now twice had one agent sweep another agent's in-flight work into its own commit, once committing a half-written file that left the suite red on the season branch while the working tree looked green. A `git add -A` in a tree that other agents write to is the sweep, not a shortcut.

PROVE IT. Red-first tests, both directions in one pass, because the halves were separately correct and jointly broken: a `--branch` parent brief names its branch and authorises the single commit; a non-`--branch` parent brief still forbids all git. Then one live `--branch` round — a trivial target is fine — whose loop branch is genuinely ahead of base when the parent exits, shown with `git rev-list --count <base>..<branch>`.

ALSO WORTH FIXING WHILE YOU ARE HERE, if it is cheap: `season.py merge-up` should say loudly when the branch it was handed is 0 commits ahead, instead of reporting a green merge of nothing. A guard on the symptom is not a fix for the cause, but this particular symptom is what hid the cause for a whole round.

DO NOT edit `extensions/agi/bin/workflow.py`, `rotate.py`, `cli.py`, `dispatch.py`, `zoom.py` or anything under `extensions/agi/workflows/` — four other agents hold those right now. Do not change what a KID brief says about git; kids commit nothing and that is correct. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window.

MEASURED AGAIN 2026-09-08, L3.42 (Belam XI): the fix landed at dc743760e did NOT take for pi parents. All six --branch parents in L3.42 exited with their branch at ZERO commits ahead of base, exactly as before the fix, and the prime harvested all six by hand from inside the worktrees. This is the second consecutive round with that shape. The fix was written and verified on the claude-code harness; pi parents get their duties block from the same brief.py template but evidently do not act on it. RE-RUN AS BUILD with the gate being a LIVE pi parent committing unaided - a dry-run or a claude-code parent is not evidence for this claim. Until then, treat merge-up reporting green on an empty branch as a standing hazard and check rev-list --count base..branch before believing any round landed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
self-perpetuating, 2026-09-08, session 3066c544. ALL THREE PIECES NOW COMMITTED+PUSHED on season/s2: cli.py cmd_done auto-commit (alive, a3aaf5dfc), dispatch.py commits_ahead telemetry (alive, same commit), brief.py item-5 simplification + test_brief.py rewrite (this session, d47154941). Suite green (2148/2150, 2 unrelated pre-existing failures in test_send.py from an unrelated in-flight edit to send.py by another live agent -- not this mechanism).

STILL OPEN, and it is the claim's own PROVE gate, not a new one: a LIVE --branch pi parent's worktree landing a real commit, checked from outside with git rev-list --count. Investigated one live candidate this session -- all-is-one's Q.03 round (agent a00-85beb9ba, hypothesis:l3-branch-isolation-partial-break, branch loop/hypothesis-l3-branch-isolation-p-a00-85beb9ba@s2, worktree .agi/worktrees/a00-85beb9ba) -- and it does NOT satisfy the gate: `git rev-list --count season/s2..<branch>` = 0, and the worktree is STILL DIRTY (one uncommitted node file, .agi/nodes/experiment/a00-7789d44c-68c664.md, edited_by: a00-85beb9ba, mtime 218s < agent.json finished_at 225s -- the edit predates done, so it should have been caught).

RULED OUT, checked directly, not guessed: (1) path resolution -- ran locations.source_root/git_common_root against this exact worktree by hand, both resolve correctly (source_root = the worktree, git_common_root = main, toplevel = the worktree, common != toplevel -- the function's own guard would correctly NOT treat this as main and would proceed to commit). (2) the brief text -- grepped this agent's own context.md, "YOUR CHECKOUT" correctly names the worktree path, not main. (3) dispatch.py's dead-pid reaper path (_reap_one_impl) -- does not match what's on disk (that path produces a sparse failed/done-unreported record; this agent.json has the full verdict/confidence/notes/evidence_runs shape only cmd_done's real code path writes), so the crash-reaper is not what set status=done here.

NOT RESOLVED: whether cli.py done was truly invoked as a real subprocess (in which case _auto_commit_worktree ran and failed silently -- no ERR line surfaced, but stderr IS merged to stdout at spawn time (dispatch.py:1404 stderr=subprocess.STDOUT) so a real failure should have printed; found neither a success line nor an ERR line in output.log), or the model narrated a DONE-shaped text block as its final answer without ever calling the tool, with agent.json's rich content coming from a `write.py` call the parent DID make (explains edited_by/verdict on the KID's node) while the FINAL `cli.py done` invocation never happened as a real subprocess. output.log is not a reliable signal either way for a `pi -p` harness: it appears to carry only the model's final text, not a transcript of intermediate tool calls (same sparse shape on my OWN successful Q.03 parent, which we know worked because its agent.json is real and its branch was non---branch so the question doesn't even arise there).

NEXT, concretely, for whoever picks this up: dispatch ONE more --branch parent against a small/trivial target, briefed with an ADDED explicit self-check step after calling cli.py done: `git -C <worktree> log -1 --format=%H` and `git -C <worktree> status --porcelain`, printed and reported in its own DONE text, so the round is self-certifying instead of requiring this same external forensic pass again. If that also comes back dirty, add one print at the very start of _auto_commit_worktree (temporary, remove after) to settle definitively whether the function is even being entered.
<!-- THOUGHT:END -->