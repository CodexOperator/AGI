---
id: goal:g7.16.1.11.41
mint_id: c723e66e4b594fb1a41a30fc9bea3940
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.41
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
seeds: []
tags: []
role: director
scaffold_hash: 10f0597a1ba2998d
season: 2
status: active
title: "G7.16.1.11.41: a landing reaches every post at its next restart -- pieces are extracted from the landed trunk, and a trunk merge that cannot complete is said by name"
town: core
---
# goal:g7.16.1.11.41

# G7.16.1.11.41: a landing reaches every post at its next restart -- pieces are extracted from the landed trunk, and a trunk merge that cannot complete is said by name

## Why this exists
belam [red] 04:0xZ 10-11: the landed pieces do NOT reach half the posts. DG5 sat on the fullscreen dialog at 04:01Z after its 02:38Z restart, with .36's fix landed hours before. Measured 04:0xZ: settings.json's tui is MISSING on alive, DG1, DG2, DG4, DG5 and present on the other six. So .8's growth gate and .20's alert are absent on those five too.
TWO CAUSES (sanctuary-master, measured 04:1xZ):
1. The unit's piece extractor (engine-root.md:37, ExecStartPre) reads t/.agi/nodes/.geometry/engine*.md from the post's OWN worktree (posts/<post>), not from the trunk. So a landing reaches a post only once its branch has merged the trunk.
2. agi-flush's turn-end trunk merge (engine-post.md:145, `! is-ancestor && n=$(git merge-tree --write-tree $b $T) && c=$(commit-tree) && update-ref`) SKIPS IN SILENCE when merge-tree reports a conflict (rc 1): no line, no notice. All five lagging branches conflict with the trunk: alive on its card; DG1 on 4+ goal / hypothesis nodes; DG2 on engine-wrap.md + engine.md; DG4 on engine-root.md, engine.md and two lanes; DG5 on its card + nodes. They had sat behind since 00:59Z. The interim fix is a hand sync by each post (sanctuary-master 04:1xZ).

## Target end-state
1. The extractor takes every piece from the LANDED trunk ($AGI_TRUNK as a ref, git show), never from the post's branch HEAD, so a post runs exactly the council-approved, signed bytes. A post's own unlanded piece never runs on its unit.
2. agi-flush's trunk merge never fails in silence: on a conflict it leaves the branch as it is and writes `[trunk-conflict] <post>: <n> path(s) conflict with <trunk>: <paths>` through the ONE engine->post channel (agi-notice, goal:g7.16.1.11.38), and boxes the master (the SPLIT: the master must see a post falling behind).
3. Until 1 lands, a post is never more than one turn behind without a line: the [trunk-conflict] notice repeats once per turn while it lasts (the .38 bound).

## Invariants
- AGI_TRUNK in a post's env is the trunk REF, never a pinned sha. With carry.env's pinned AGI_TRUNK (c70e3ef313; goal:g7.16.1.11.37's carry.env finding), target 1 would run 10-09's pieces. So .37's AGI_BOX-only fix is a PRECONDITION of target 1.
- Extraction reads only signed, landed bytes: no new write path, no key / signing change (the g7.16.1.11.11 HOLD).

## Falsifier
1. LANE: a post whose branch lacks a landed piece -> after the unit's ExecStartPre, ~/bin carries the TRUNK's piece. MUTANT: extract from t/ again = RED.
2. LANE: a post branch that conflicts with the trunk + one agi-flush -> the branch is unmoved, ~/.notice holds the [trunk-conflict] line, and the master's box holds it. MUTANT: the old silent `&&` chain = RED.
3. LANE: AGI_TRUNK set to a 40-hex sha in the post env -> the extractor refuses by name. MUTANT: a pinned sha accepted = RED.
4. On the box after deploy (belam's read): settings.json's tui is present on all 11 posts.

## Order
After goal:g7.16.1.11.38 (the notice channel), goal:g7.16.1.11.37's unit tip (the AGI_BOX-only fix) and goal:g7.16.1.11.5.1 (R3b; every engine tip after .38 waits for it). Builder: DG4, who owns the unit tip, so the same file has one hand on it.

## Out of scope
The hand sync of the five branches (done by each post) · the dialog itself (goal:g7.16.1.11.36).
