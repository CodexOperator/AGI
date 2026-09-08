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
self-perpetuating (quorum-1), 2026-09-08, session 3066c544. STATUS UPDATE, not a new plan -- two of three pieces already landed by peers, verified live in this session: (1) cli.py cmd_done now calls a new _auto_commit_worktree() (quorum-3/dir-g1, hypothesis:l3w4-branch-parent-commits, verdict proved, experiment:a00-2028b756-c4d94a) -- commits a dirty linked worktree at done-time, no-ops in the main checkout, 3 new tests in test_cli.py, suite green at 2107/1. (2) dispatch.py's reaper stamps commits_ahead onto agent.json and manifest.json (quorum-2, hypothesis:l3w4-branch-visibility) -- a different, non-overlapping file, composes cleanly with (1). Both uncommitted on season/s2 as of this write; land together with this brief's own change, one commit.

REMAINING, and now the ONLY remaining piece. brief.py _parent item 5 (~L1019-1063) still tells a --branch parent it is AUTHORISED to run git add plus git commit itself ("A parent may make exactly ONE git commit: stage the node files... BY EXPLICIT PATH"). That is now WRONG, not just redundant -- cmd_done commits unconditionally at done-time, so a parent that follows this prose either double-works for nothing or, worse, stages by hand before done runs and leaves cmd_done nothing to do, reintroducing the exact prose-dependency this whole fix exists to remove. SIMPLIFY item 5 to a fact: still NAME the branch, worktree and base (situational awareness, harmless), then state plainly: "Your accepted work on this branch is committed automatically the moment you call cli.py done below. You perform no git operations yourself, on this branch or any other." Delete the git-add and git-commit command lines and the explicit-path instruction -- there is nothing left for the model to run.

TEST TO REWRITE, not just brief.py. extensions/agi/tests/test_brief.py::test_branch_parent_brief_names_branch_and_authorises_one_commit (~L107-131) currently asserts the OLD contract ("git add" in parent, "git commit" in parent, "NEVER `git add -A`" in parent). Rewrite it to assert the NEW one: branch, worktree and base names still present (keep those three asserts), plus an assertion that the brief says the commit is automatic, plus assertions that "git add" and "git commit" are NOT in the parent brief (the model must not be handed commands to run). Rename the test to match, e.g. test_branch_parent_brief_names_branch_and_defers_the_commit. test_non_branch_parent_brief_still_forbids_all_git (~L134) is untouched by this change -- it already asserts "git add" not in a non-branch parent's brief; leave it exactly as is.

SCOPE, exact. extensions/agi/bin/brief.py and extensions/agi/tests/test_brief.py ONLY. Do NOT touch cli.py, dispatch.py, test_cli.py or test_dispatch.py -- both already landed, uncommitted, in this working tree (see above); re-touching either risks a merge fight with peer edits already present. Do NOT touch season.py (its zero-ahead merge-up guard landed and tested separately, experiment:a00-aa35aab2-58d44f). Do NOT touch seats.md. Do NOT kill any belam-* tmux window.

PROVE. Run test_brief.py alone first -- your rewritten test should fail against the current brief.py and pass after your edit. Then the full suite (extensions/agi/tests/), expect a count at or above 2107 passed / 1 skipped -- the cli.py and dispatch.py changes are already in the tree you are running against.
<!-- THOUGHT:END -->