---
id: hypothesis:l4-branches-are-one-tree-under-the-season
mint_id: 3e9ab17a376b46c3816e94ef09e87266
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L4-VII
scaffold_hash: 4988fa5556a80260
season: 2
testable_claim: "OWNER 2026-09-11 02:0xZ (verbatim in doc:l4-owner-decisions): the GitHub branch list has seat branches at the top level beside season/s2; every branch should descend from the season: \"just s2 at the top level, and all others descend from there ... each town ... just needs s2/town/s1. Seats become s2/seat or s2/town/s1/seat ... Cleans up the web view on github for repo visitors.\" ONE CORRECTION FORCED BY GIT, measured on a scratch repo by the Prime (`fatal: cannot lock ref refs/heads/s2/seat: refs/heads/s2 exists`): a ref cannot be both a branch and a folder, so the trunk of every folder is a LEAF named main. CLAIM: the branch scheme is ONE tree under the season, declared as config and derived everywhere: `master` = the last closed core season (GitHub default, unchanged); `s2/main` = the core trunk for season 2 (was season/s2); `s2/<seat>` = a core seat session branch (was seat/<seat>@s2); `s2/<town>/s1/main` = a town season-1 trunk (was town/<town>@s2 and the planned town/<town>/season/s1, collapsed as the owner asked); `s2/<town>/s1/<seat>` = a seat working in that town; kid loop branches stay LOCAL and unpushed (the web view never sees them) and move under `s2/loop/<iter>-<agent>` so the top level holds exactly master + one folder per season. (1) ladder:ladder declares `branch_scheme` (season prefix, trunk leaf `main`, seat and town templates); a single resolver (season.py or a new branches helper exposed through it) answers trunk_for(season, town), seat_branch(seat, season, town), kid_branch(iter, agent), is_trunk(branch); every one of the ~47 literal `season/`, `seat/`, `loop/` sites in dispatch.py (20), season.py (7), rotate.py (7), send.py (6), hierarchy.py (3), node_writer.py (2), plan_master.py (1), grid.py (1) reads the resolver — grep for the literals after the change returns only the resolver, tests and archived nodes. (2) The grid branch guard allows master and every trunk (is_trunk), never a seat or kid branch, never --allow-branch; the stale-base guard compares a seat against ITS trunk (a town seat against the town trunk). (3) MIGRATION as one rehearsed script `season.py rebranch --dry-run|--apply`: for each live ref `git branch -m old new`, push new, delete old on origin, retarget every worktree under .agi/worktrees/* to its renamed branch, rewrite config (ladder branch_scheme, town_branches, config:seats worktree cells), leave master and the two foreign branches (copilot/*, collaborator-branch) untouched; rehearsed on a CLONE of the repo with all 9 origin refs and 3 worktrees reproduced, node count identical before and after, verify 9/9 on the renamed trunk; the live apply is the PRIME step at the merge-up, with the point and helper PAUSED (no live kid on a loop branch, no merge in flight) and the crons branch-push re-resolving the checked-out branch by itself. (4) FIXTURES ONLY in tests: a temp repo with the old scheme, the migration run, the new scheme asserted; nothing touches this repo or origin during tests. FALSIFIERS: any remaining literal branch prefix outside the resolver; a trunk that is also a folder (the lock error); grid committing on a seat branch after the change; a worktree left on a deleted branch; a rename that changes any node or its count; a test that pushes. DECISION BANKED for the owner in doc:l4-owner-decisions: trunk leaf name `main` (recommended) vs `core`. SERIAL: behind L4.117 towns (it owns town_branches and the town/season recursion); cut only when no kid is live on a loop branch."
thought_session: belam-S1-L4-VII
title: Branches are one tree under the season — s2/main, s2/<seat>, s2/<town>/s1/main, s2/<town>/s1/<seat>; scheme as config, a rehearsed rename, master untouched
---
<!-- BODY:BEGIN -->
# hypothesis:l4-branches-are-one-tree-under-the-season

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DECIDED by the Prime L4-VII 03:3xZ under the owner's 'act independently, use your morals' (verbatim doc:l4-owner-decisions): the trunk leaf is  at every level (s2/main, s2/<town>/s1/main). Reason on the morals: elegant and small — one word that reads as the trunk in every folder;  would collide with the core town's name inside a town folder. The banked decision is closed; the round proceeds on main.

CORRECTION of the note above (its backticked words were eaten by a shell substitution): DECIDED by the Prime L4-VII 03:3xZ under the owner's "act independently, use your morals": the trunk leaf is `main` at every level (s2/main, s2/<town>/s1/main). Reason on the morals: elegant and small — one word that reads as the trunk in every folder; `core` would collide with the core town's name inside a town folder. The banked decision is closed; the round proceeds on main.
