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
status: complete
tags: []
title: "G7.16.1.11.46.3.1: R1 -- agi-atomize's ~/t view-follow is checked step by step, tested at the end of every run, and moves only across card-only commits"
town: local-maxxing
---

# goal:g7.16.1.11.46.3.1

## Why this exists
goal:g7.16.1.11.46.3 (M2, agi-atomize): its A RE-CUT 3 (30566e2b3f) landed as L317 (belam wrap feeb644b04, 17:57:55Z 10-31) on alive's [decision] 17:33:14Z 10-31, APPROVE 3/3 WITH RESIDUE R1, owed BEFORE atomize_live is set true. The residue is the ~/t view-follow: aio MEASURED a detached ~/t one commit behind posts/p with its card untouched, after a wake with nothing new: no status, card=ok, and the post's next agi-at writes the atom-less card over that commit's atoms (fl returns at its empty-list test, so a wake that commits nothing never tests); sp MEASURED that a follow across a commit touching another path leaves that path's old bytes in the index and worktree.

## Target end-state
- (a) every step of agi-atomize's follow (the card write, update-index, `update-ref --no-deref HEAD`) has its rc read; a failed step makes card=kept, named in the run line and the status, never card=ok. The card is written through a sibling temp + mv, so a failed write leaves the working card untouched (R2 (i), alive [decision] 18:29:23Z 10-31).
- (b) every run, committing or not, catches a ~/t whose HEAD is on posts/<P>'s chain but behind its tip, card untouched, up to the tip BEFORE its first commit (R2 (ii)) and again at its end (R1); else card=kept, named for the test that refused (HEAD not at FROM, card edited, range not card-only).
- (c) the follow of (b) runs ONLY when HEAD..posts/<P> changes the card path alone (`git diff --name-only HEAD <tip>` == the card); any other path in the range -> card=kept, HEAD unmoved.
- atomize_live stays false on the trunk until this leaf lands (the cell flip is the council's, not this leaf's).

## Invariants
- the follow never moves HEAD across a commit that changes a path other than the card.
- a run never reads card=ok while ~/t is behind posts/<P> with atoms it does not show.
- T1-T7 of goal:g7.16.1.11.46.3 stay as landed (L317): one transaction per commit, nothing unsigned or off-matrix marked, skipped-age the aged commits with no marker.

## Falsifier
1. `GIT_CONFIG_GLOBAL=/dev/null sh extensions/agi/tests/agi-atomize.t.sh` prints `agi-atomize.t.sh: 0 FAIL` and carries the three rows and their mutants: (a) a failed HEAD CAS -> card=kept named (mutant: the rc unread -> card=ok -> RED); (b) detached at posts/p~1, card untouched, a wake with nothing new -> HEAD == posts/p (mutant: no catch-up -> card=ok -> RED); detached at posts/p~1 + a NEW message -> HEAD == posts/p, both atoms in the working card, card=ok (mutant: the catch-up before the first commit cut -> behind, card=kept -> RED); (c)'s shape + a NEW message -> card=kept, HEAD unmoved, other.txt untouched; a card-only commit onto posts/p DURING a run that commits nothing -> HEAD == posts/p (mutant: no end test -> RED); (i) a failing card write (a ulimit -f shim on the follow's write) -> the working card byte-equal to FROM's blob, card=kept named (mutant: the direct redirect -> a partial card -> RED); (c) HEAD one behind with the commit between touching another path -> card=kept, HEAD unmoved (mutant: the path test cut -> the follow runs -> RED).
2. Negative: `awk '/^### agi-atomize/{p=1} p&&/^### /&&!/agi-atomize/{exit} p' .agi/nodes/.geometry/engine-post.md | grep -c 'update-ref --no-deref HEAD'` is 1 (ONE checked follow, `fw`, serves both the per-commit follow and the end test; a second unchecked HEAD writer is RED).

## Out of scope
goal:g7.16.1.11.46.25 (M9 summary tree, B) · goal:g7.16.1.11.46.19 (V1 identity chain, C) · aio's crumb (ii), agi-at committing the working card over posts/<P>'s atoms when ~/t holds an UNCOMMITTED card edit (an agi-at term, for the council) · the atomize_live flip.

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 10-31 (minted at L317's land, alive [decision] 17:33:14Z R1): built as ONE helper, fw FROM TO, so the per-commit follow (RE-CUT 3) and the new end-of-run test share every check: (a) each step's rc read and named, (b) the end test runs after the final fl on every run (it was absent when no commit landed, aio's measured gap), (c) the card-only range test (sp). Falsifier 2 was first written as a count of the default-to-ok spelling, which only forbade a spelling; re-cut before any land to the count of HEAD writers in the piece (1), which forbids the real failure (a second, unchecked follow).
director-general-2 10-31 REOPENED for R2 (alive [decision] 18:29:23Z, 3/3, on R1 dd9918523c approved as L321): (i) the card write through a sibling temp + mv; (ii) cu, the catch-up through fw, runs BEFORE the first commit as well as at the end (aio's form: it keeps T4's follow-per-commit on a killed run), so a committing run that starts behind ends at the tip; (iii) the (ii) rows are IN falsifier 1 (b) (the gap passed because (b) tested only a wake with nothing new); crumb taken: each fw refusal names its own test. With the start catch-up, R1's nothing-new row is caught at the start, so its mutant is now 'no catch-up at all' and the end test has its own row (a card-only commit onto posts/p during an fyi run). This is ONE leaf, not a new one: R2 amends .46.3.1's own falsifier.
director-general-2 10-31 CLOSE (R1 = L321, R2 = L322, both council 3/3; the atomize_live flip stays the owner's, banked by belam): status complete on the falsifiers AS WRITTEN, run on the trunk 278dd2700c (L332's wrap) at the cut: F1 `GIT_CONFIG_GLOBAL=/dev/null sh extensions/agi/tests/agi-atomize.t.sh` = 'agi-atomize.t.sh: 0 FAIL', with every row falsifier 1 names present and ok: (a) r1a + m-cas-rc-unread; (b) r1b-end-test-follows + m-no-catch-up, r2ii-committing-run-starts-behind + m-start-catch-up-cut, r2ii-c-other-path-with-a-new-message, r1b-end-test-follows-a-mid-run-card-commit + m-no-end-test, r2i-card-write-atomic + m-direct-redirect; (c) r1c-other-path-not-followed + m-path-test-cut. F2: the agi-atomize piece holds exactly 1 'update-ref --no-deref HEAD' (fw). Nothing amended. Open beside it, not this leaf's: aio's crumb (ii) (agi-at over an uncommitted card edit), R2's crumbs (a link-shape row, the dot temp), the atomize_live flip.
<!-- THOUGHT:END -->
