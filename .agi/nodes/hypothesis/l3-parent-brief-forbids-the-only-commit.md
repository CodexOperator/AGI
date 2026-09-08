---
id: hypothesis:l3-parent-brief-forbids-the-only-commit
mint_id: c249c3d9b64b4208ac2c19b4e1b68ac2
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: quorum-1
scaffold_hash: d847510c32a35e32
season: 2
testable_claim=brief.py: _parent contains DO NOT commit, push, or sync and contains no occurrence of branch, worktree or merge, so a --branch parent obeys it and leaves its loop branch at base; after the change the parent brief distinguishes the two cases — in the main checkout it still commits nothing, and under --branch it is told it holds a loop branch in a worktree, that the branch is the only route its kids work has to the season branch, and exactly which commit it owns — proven by a red-first test asserting the --branch parent brief names its branch and authorises that one commit while the non-branch brief still forbids all git, plus one live --branch round whose branch is ahead of base at parent exit
thought_session: 407c3159-b508-4d42-a723-4bde65ea6d79
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
quorum-1 (vision:self-perpetuating), 2026-09-08. SHARPER ROOT CAUSE: dispatch.py sets AGI_PARENT_BRANCH/WORKTREE/BASE_BRANCH nowhere (grep over dispatch.py: zero hits outside brief.py itself). The L3.40 branch-aware paragraph in brief.py _parent has therefore never reached a live dispatched agent on ANY harness -- the L3.40 evidence was a direct assemble() call and a monkeypatch, not a real dispatch. L3.42's "6/6 pi parents still at zero commits" is fully explained by the paragraph never firing at all; the pi harness is not specifically implicated, and finishing the env-wiring alone would still be a prose instruction a model can silently not act on -- the owner's explicit ask is structural, not a second prose attempt.

BUILD THIS INSTEAD. Move the one authorised commit out of the model's hands into `cli.py cmd_done` (extensions/agi/bin/cli.py, ~L368). Every parent already MUST call `cli.py done <iter> <agent_id> --verdict pending --owns <kid-node-id> ...` to be marked finished (brief.py _parent item 6) -- unconditional, harness-agnostic, already the loop's one mandatory completion choke point. `cmd_done` already loads the agent record dispatch.py wrote at spawn time (`rec = json.loads(ap.read_text())`, ~L466); that record already carries `rec['tier']`, `rec['branch']`, `rec['base_branch']`, `rec['worktree']` whenever dispatch.py cut this parent a branch (dispatch.py ~L1406-1413). Nothing needs threading through the environment -- the seam already exists on disk, unused.

CONCRETE CHANGE in cmd_done: once `rec` is loaded, when `rec.get('tier') == 'parent' and rec.get('branch') and rec.get('worktree')` and that worktree path exists on disk:
 - `git -C <worktree> status --porcelain` -- if empty, print a line and skip; nothing to commit is not an error.
 - else `git -C <worktree> add -A` then `git -C <worktree> commit -m "loop: <branch> -- accepted <owns ids joined>"`.
 - `-A` is deliberate and safe HERE ONLY: this worktree is exclusive to this one parent and its serialized kids (kids inherit it via AGI_TREE_PROJECT_ROOT re-rooting, never their own --branch), so nothing else ever writes into it -- unlike the shared main checkout, where -A has twice swept another agent's in-flight edit into one commit. Say this in a comment so a future reader does not "fix" it back to explicit-path and reintroduce a hazard that does not apply here.
 - never push, sync, rebase, or touch any other branch or the main checkout -- same boundary as before, just enforced in code that always runs instead of prose that can be silently skipped.
 - the existing pre-commit guard (extensions/agi/hooks/agent-git/pre-commit, allows AGI_TIER=parent on loop/* since L3.40/dc743760e) still gates this correctly since cli.py runs inside the parent's own process/env.
 - brief.py's branch-aware item 5 (`_parent`, ~L1034-1060) should be SIMPLIFIED to state a fact, not issue an instruction the model might act on redundantly: "Your accepted work on this branch is committed automatically the moment you call `cli.py done` below. You perform no git operations yourself." Keep git out of the model's hands entirely -- that is the point of moving it into cmd_done.
 - the dead env-only seam (AGI_PARENT_BRANCH etc, brief.py ~L1220-1230; dispatch.py never sets them) can stay inert or be removed -- not load-bearing either way once cmd_done commits directly from the agent record.

PROVE: a red-first test asserting a call to cmd_done's logic (function or subprocess) against a fixture `--branch` parent's agent.json + a dirty worktree leaves that worktree's branch with commits-ahead-of-base > 0, with no git command run by the test itself beyond setup and verification. Then one LIVE round: dispatch a --branch parent on the pi harness (the harness the prose fix was measured to fail on), let it run one kid to completion and call `cli.py done` exactly as briefed -- nothing extra -- then from OUTSIDE the agent, `git rev-list --count <base>..<branch>` > 0. That live number is the gate, not a green test suite.

ALSO, cheap and same neighbourhood, still open from the original brief: `season.py merge-up` should say loudly when the branch it was handed is 0 commits ahead instead of reporting a green merge of nothing. Keep it even though it should now rarely trigger -- it is the tripwire for the next thing shaped like this bug.

FILE LOCK CHECK, done live before writing this (spawn_budget.py status): only 2 agents live, under iter L3.43, target hypothesis:l3w4-seat-sessions-and-tiling, tier parent+kid -- neither touching cli.py/dispatch.py/brief.py/season.py. The old "four other agents hold workflow.py/rotate.py/cli.py/dispatch.py/zoom.py" line in this node's body is from L3.42 and is stale; re-check with spawn_budget.py status before you start rather than trusting either note by the time you read this.
<!-- THOUGHT:END -->
