---
id: goal:g7.16.1.11.46.3.1
mint_id: 088cc24d91c44f428ac781b4f34dedb0
type: goal
parents:
  - goal:g7.16.1.11.46.3
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.3.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 8696b095cb9f5739
season: 3
seeds: []
status: active
tags: []
title: "G7.16.1.11.46.3.1: R1 -- agi-atomize's ~/t view-follow is checked step by step, tested at the end of every run, and moves only across card-only commits"
town: local-maxxing
---

# goal:g7.16.1.11.46.3.1

## Why this exists
goal:g7.16.1.11.46.3 (M2, agi-atomize): its A RE-CUT 3 (30566e2b3f) landed as L317 (belam wrap feeb644b04, 17:57:55Z 10-31) on alive's [decision] 17:33:14Z 10-31, APPROVE 3/3 WITH RESIDUE R1, owed BEFORE atomize_live is set true. The residue is the ~/t view-follow: aio MEASURED a detached ~/t one commit behind posts/p with its card untouched, after a wake with nothing new: no status, card=ok, and the post's next agi-at writes the atom-less card over that commit's atoms (fl returns at its empty-list test, so a wake that commits nothing never tests); sp MEASURED that a follow across a commit touching another path leaves that path's old bytes in the index and worktree.

## Target end-state
- (a) every step of agi-atomize's per-commit follow inside fl (the card write, update-index, `update-ref --no-deref HEAD`) has its rc read; a failed step makes card=kept, named in the run line and the status, never card=ok.
- (b) every run, committing or not, ends with ONE test: ~/t's HEAD on posts/<P>'s chain but not at its tip, its card untouched since HEAD -> the view follows to the tip; else card=kept, named.
- (c) the follow of (b) runs ONLY when HEAD..posts/<P> changes the card path alone (`git diff --name-only HEAD <tip>` == the card); any other path in the range -> card=kept, HEAD unmoved.
- atomize_live stays false on the trunk until this leaf lands (the cell flip is the council's, not this leaf's).

## Invariants
- the follow never moves HEAD across a commit that changes a path other than the card.
- a run never reads card=ok while ~/t is behind posts/<P> with atoms it does not show.
- T1-T7 of goal:g7.16.1.11.46.3 stay as landed (L317): one transaction per commit, nothing unsigned or off-matrix marked, skipped-age the aged commits with no marker.

## Falsifier
1. `GIT_CONFIG_GLOBAL=/dev/null sh extensions/agi/tests/agi-atomize.t.sh` prints `agi-atomize.t.sh: 0 FAIL` and carries the three rows and their mutants: (a) a failed HEAD CAS -> card=kept named (mutant: the rc unread -> card=ok -> RED); (b) detached at posts/p~1, card untouched, a wake with nothing new -> HEAD == posts/p or card=kept named (mutant: no end test -> card=ok -> RED); (c) HEAD one behind with the commit between touching another path -> card=kept, HEAD unmoved (mutant: the path test cut -> the follow runs -> RED).
2. Negative: `awk '/^### agi-atomize/{p=1} p&&/^### /&&!/agi-atomize/{exit} p' .agi/nodes/.geometry/engine-post.md | grep -c 'update-ref --no-deref HEAD'` is 1 (ONE checked follow, `fw`, serves both the per-commit follow and the end test; a second unchecked HEAD writer is RED).

## Out of scope
goal:g7.16.1.11.46.25 (M9 summary tree, B) · goal:g7.16.1.11.46.19 (V1 identity chain, C) · aio's crumb (ii), agi-at committing the working card over posts/<P>'s atoms when ~/t holds an UNCOMMITTED card edit (an agi-at term, for the council) · the atomize_live flip.

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 10-31 (minted at L317's land, alive [decision] 17:33:14Z R1): built as ONE helper, fw FROM TO, so the per-commit follow (RE-CUT 3) and the new end-of-run test share every check: (a) each step's rc read and named, (b) the end test runs after the final fl on every run (it was absent when no commit landed, aio's measured gap), (c) the card-only range test (sp). Falsifier 2 was first written as a count of the default-to-ok spelling, which only forbade a spelling; re-cut before any land to the count of HEAD writers in the piece (1), which forbids the real failure (a second, unchecked follow).
<!-- THOUGHT:END -->
