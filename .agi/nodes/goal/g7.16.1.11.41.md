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
4. THE CADENCE (council 24cdb55824, self-perpetuating + all-is-one, measured on their own seats): lag has TWO causes, conflict AND cadence. agi-turn (the Stop hook) never merges the trunk; only agi-flush does, and agi-flush runs at a rotation or restart. posts/self-perpetuating sat on its 02:47Z merge for 2+ hours with NO conflict until a hand agi-flush (f81011e920); posts/all-is-one likewise (hand merge ca9dc62c0d 04:3xZ). So target 3's 'never more than one turn behind' is false today. Fix: the trunk merge runs at EVERY turn end, or the notice fires when posts/<post> is more than N trunk commits behind.

- SEASON-2 CLOSE GATE (owner 19:4xZ 10-11, via belam): the season-2 close waits on this leaf complete, on its falsifier AS WRITTEN. 'Everything must be able to project cleanly' = every landing reaches every post at its next start, extracted from the landed trunk, 0 stale ~/bin pieces (belam's measure (b)).
## Invariants
- AGI_TRUNK in a post's env resolves to a BRANCH (`git rev-parse --symbolic-full-name` = refs/heads/* or refs/remotes/*); anything else is refused by name: a full or ABBREVIATED sha (c70e3ef313 is written that way everywhere), a tag, a detached ref (council, alive). With carry.env's pinned AGI_TRUNK (c70e3ef313; goal:g7.16.1.11.37's carry.env finding), target 1 would run 10-09's pieces. So .37's AGI_BOX-only fix is a PRECONDITION of target 1.
- Extraction reads only signed, landed bytes: no new write path, no key / signing change (the g7.16.1.11.11 HOLD).

## Falsifier
1. LANE: a post whose branch lacks a landed piece -> after the unit's ExecStartPre, ~/bin carries the TRUNK's piece. MUTANT: extract from t/ again = RED. CUT 3 (council 3/3 11:25Z 10-14): the same lane seeds ~/bin with a RETIRED file (agi-link) and a stale copy -> after ExecStartPre ~/bin is EXACTLY the trunk's piece set (the extra is gone, the stale copy is the trunk's bytes). MUTANT: no clear (extract over bin/) = RED. And it FAILS CLOSED AND LOUD: a failing git ls-tree / show, or an extracted set without agi-run -> `[extract-failed] <file>`, exit 255, the old ~/bin byte-equal, no swap. MUTANTS: swap anyway (no agi-run check / show failure ignored / ls-tree failure ignored) = RED.
2. LANE: a post branch that conflicts with the trunk + one agi-flush -> the branch is unmoved, ~/.notice holds the [trunk-conflict] line, and the master's box holds it. MUTANT: the old silent `&&` chain = RED.
3. LANE: AGI_TRUNK set to a 40-hex sha, a 10-hex sha, or a tag in the post env -> the extractor refuses by name. MUTANT: a 10-hex sha accepted = RED.
4. On the box after deploy (belam's read): settings.json's tui is present on all 11 posts, and ~/bin EXTRAS (files not in the trunk's 33 pieces; census 10-14 11:5xZ: agi-link on all 12, signers on 3) are 0 on every post.
5. LANE (cadence): a session that lives K turns while the trunk moves is never more than one turn behind = GREEN. MUTANT: merge only at flush = RED.

## Order
After goal:g7.16.1.11.38 (the notice channel), goal:g7.16.1.11.37's unit tip (the AGI_BOX-only fix) and goal:g7.16.1.11.5.1 (R3b; every engine tip after .38 waits for it). Builder: DG4, who owns the unit tip, so the same file has one hand on it.

## Out of scope
The hand sync of the five branches (done by each post) · the dialog itself (goal:g7.16.1.11.36).

## OWNER 2026-10-11 19:4xZ, verbatim
"Make sure that the projection work is done before season rollover. Everything must be able to project cleanly. Are we making progress through the bundle and the trajectory is staying stable?"
belam's measure at the time (19:2x-19:4xZ): ROOT projection CLEAN (agi-project rendered at the pin 5f5dc2c4be == /run byte for byte, 29 files; the trunk tip renders identically, no pin move owed). POST projection NOT clean: agi-post@'s ExecStartPre still extracts from each post's OWN t/; t HEAD behind trunk DT-1 271 · DG3 264 · DG4 244 · DG5 174 · TM 147 · alive 91 · SM 26 · sp 26 · aio 24 · DG2 24 · DG1 22 · belam 1; ~/bin pieces stale or missing vs the trunk: 1-8 per post. Targets 1-4 were held until .37 and .5.1 landed; both are complete.

## Agent Notes
Assigned to **director-general-5**, with its leaf goal:g7.16.1.11.41.1 (SM placement gen 38, 10-11). The Order section's "Builder: DG4" named who owned the unit tip when this was filed; the goal as a whole is now DG5's.

<!-- THOUGHT:BEGIN -->
10-11 (director-general-5, SM gen 38): what is left once goal:g7.16.1.11.41.1 lands, read from the bytes at trunk 0c99755883. .41.1 (agi-first-start: a landing over a self-installing piece must say what each post gains and loses, refused by name without a `first-start:` line) is NOT one of targets 1-5: it makes a landing's effect on posts SAID, it does not make it ARRIVE. So after .41.1 the whole of this goal is still open:
- Target 1 (extract from the landed trunk): engine-root.md:40 (ExecStartPre) still reads `t/.agi/nodes/.geometry/engine.md` and `engine-[pw]*.md` from the post's own worktree. Open. Falsifier 1 and 3 (the trunk's piece reaches ~/bin; a sha or tag AGI_TRUNK refused by name) wait on it.
- Target 2 ([trunk-conflict] by name): the agi-flush trunk merge (engine-post.md, the `&&` chain ending `update-ref`) is still the silent chain, and the string `trunk-conflict` appears in no engine*.md. Open. Falsifier 2.
- Targets 3 and 4 (the notice repeats once per turn; the merge runs every turn end or a lag notice fires): open, agi-flush is still the only merger. Falsifier 5.
- Falsifier 4 is belam's on-box read after a deploy, not a lane.
- Preconditions: goal:g7.16.1.11.38 (the notice channel) is complete; goal:g7.16.1.11.37 (the AGI_BOX-only unit tip) and goal:g7.16.1.11.5.1 (R3b, "every engine tip after .38 waits for it") are both still active, and the Order puts targets 1-4 after them. So the next buildable step here is none until .37 and .5.1 land; I will not start target 1 ahead of them.
- .41.1 is the one piece that needed neither: it only reads the diff of a range.
<!-- THOUGHT:END -->
