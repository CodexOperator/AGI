---
id: goal:g7.16.1.11.46.18
mint_id: c784bfc5fb7d4b219ee97abfd757d5ea
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.18
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - G1b-2
season: 3
status: active
title: "G7.16.1.11.46.18: G1b-2 -- the cutover: a land is a split (one commit per changed node on its grid ref), a moved tip is a held merge row, agi-sync becomes recompose, every posts/P reader migrated, rollback kept"
town: local-maxxing
---
# goal:g7.16.1.11.46.18

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §25. Council rows: aio 1 (the land flow reads posts/P: 25 files over extensions, skills and .geometry), aio ROW A (readers outside the repo: SM's gsend.sh [r1p] rev-parse of posts/belam, cited by sha256 in skills/agi-master-gate, and belam's land CAS), sp 5 (the new land check). Depends on .46.17. Owner atom a2 (the git-based renderer) closes HERE (council R1).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.18 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| a2 | "We need to redo the renderer if needed to be a git based graph system that uses the minimal shell code matrix integrated design" | target:W2 brief 2 leaf G1b (compose/split = the git-based renderer) |
| 3.3 | "grid monolith, node = branch, post = slice; spiders under council; red-team" | target:§25, §34.1 |

## Target end-state
- A land writes one commit per changed node on its refs/grid/node/<mint> (ff); a moved tip becomes a held `merge` row, never a whole-tree merge; agi-sync is recompose.
- The master's land check reads: recomposed posts/P tree == the gated tree.
- Every reader of posts/P, in the repo and out of it, reads the new path; each out-of-repo reader's new sha256 is reported where the old one was cited.
- Rollback: the old trunk ref is KEPT, never deleted, and the rollback command is named in the leaf's THOUGHT.

## Invariants
- One real land passes end to end on the new path before the old one stops being written.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/land-split.t.sh` exits 0: a land of k changed nodes makes k grid commits and the recomposed tree == the gated tree; mutant: a split that drops one node's commit -> tree differs -> refused, RED.
2. Reader census: `git grep -l -E 'posts/belam|refs/heads/posts/'` over extensions, skills and .agi/nodes/.geometry lists 0 unmigrated files (each remaining hit named as migrated), plus the out-of-repo readers listed by path + sha256, each migrated.
3. ONE real land lands end to end on the new path (SM's [landed] names it).
4. Negative: the old trunk ref still resolves after the cutover (`git rev-parse --verify` exits 0).

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
