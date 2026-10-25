---
id: goal:g7.16.1.11.46.19
mint_id: 5a3a9adce1414b9f98621180e7263f11
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.19
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - V1
season: 3
status: active
title: "G7.16.1.11.46.19: V1 -- refs/id/<mint> per post and kid: a piece tree and a continuity signature chain to a pinned root signer, `id check`, a mint column on config:posts; the M6 store moves to the mint path in the same land"
town: local-maxxing
---
# goal:g7.16.1.11.46.19

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §9, §27. K5: the doc names the genesis (§9: 'v1 is signed by the spawner'; check (3): the birth link is signed by the parent post), so the top of the spawn tree is ONE root signer pinned on the trunk (sp 3). Dependency from goal:g7.16.1.11.46.13's THOUGHT: the M6 store key is ${AGI_MINT:-$AGI_POST}, so the leaf that adds the mint cell moves the store IN THE SAME LAND. Box reading: refs/id/* = 0 today.

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.19 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 2.3 | "identity = composable key over signed pieces, re-hashed on swap, continuity = the history" | target:§9 · decision:§21 #1 |
| 3.5 | "mint id per post and kid; inherit director's slot; different login" | target:§27 |

## Target end-state
- Every post and kid has refs/id/<mint>: a commit per identity version whose tree is the piece set (key.pub role harness model brief card perms slot cred), signed by the previous link's key; the birth link is signed by the spawner; the top of the spawn tree is ONE root signer in the trunk's allowed-signers with valid-after.
- `id check` (~20 lines, ckpt's walker) walks a chain and names the first bad link.
- config:posts carries a `mint` column; a rename is a one-line address change.
- The M6 store lives at ~/.mem/<mint>.git (moved, same tip), in the same land as the mint column.

## Invariants
- A post is alive iff its chain is unbroken to its birth and its tip's piece set passes the row's allowed piece types (§9).
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/id-chain.t.sh` exits 0: a swap of every piece but slot passes; a link signed by a foreign key fails by name; a self-signed birth link (unlisted key) fails by name.
2. After the land, per post: ~/.mem/<post>.git is absent, ~/.mem/<mint>.git has the SAME tip sha as the old store, and `mem: tapped k/m` is unchanged; mutant: a store left at the post path reads RED.
3. Negative: `git for-each-ref refs/id/` lists one chain per config:posts row with boot true; a row without a mint prints its name, rc 1.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
