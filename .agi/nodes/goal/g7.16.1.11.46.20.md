---
id: goal:g7.16.1.11.46.20
mint_id: 645dc74e5214484f8584ffa2b3dce1c7
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.20
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - V2
season: 3
status: active
title: "G7.16.1.11.46.20: V2 -- the Claude login as a kind-secret capsule placed by LoadCredential at the tick, on ONE non-facing post; the done-when is the login itself"
town: local-maxxing
---
# goal:g7.16.1.11.46.20

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §9, §27. Box fact 10-24/25: the owner runs two Max accounts, posts switched by /login one at a time, and a token refreshes only on a turn in its last minutes (keepalive fix d56b8e79b4). Council rows: sp 4 (the done-when cannot pass on 'it cannot'; measure first where a refreshed token is written), aio ROW B (one NON-FACING post, never belam; the LoadCredential placement is a root act on the owner's account, banked for the owner's GO).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.20 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 2.2 | "credentials ride in a capsule / reuse the username slot" | target:leaf:V1 (cred piece) · decision:§21 #2 |
| 2.25 | "a second subscription for split logins" | target:§27 (`cred: <capsule>` per row, own slot) |

## Target end-state
- MEASURED FIRST, before any build, on one non-facing post: where a refreshed token is written, and whether a refresh rotates it. If a read-only placement would restore an old token, the leaf names the write-back path, or comes back as a [decision] that banks the leaf.
- The login is a `kind secret` capsule referenced from the post's refs/id chain; `cred: inherit | <capsule>` is a config:posts cell; `cred: <other>` with `slot: inherit` is refused by the check.
- The LoadCredential placement waits for the OWNER's GO (banked in card-belam §6 like the Doppler token); the leaf builds and measures up to that point and stops there.

## Invariants
- belam and every owner-facing post keep their login untouched by this leaf.
- No token, key or credential byte enters the repo, a box message or a card.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. Done-when = the login only: after the placement (owner GO), the chosen non-facing post logs in on a fresh home with 0 device re-auth. 'It cannot' is a [decision] that banks the leaf, never a pass.
2. `sh extensions/agi/tests/cred-piece.t.sh` exits 0: `cred: <other>` with `slot: inherit` is refused by name; mutant: the check removed reads RED.
3. Negative: the leaf's diff greps 0 for token-shaped strings (`sk-ant`, `refresh_token`, a 40+ char base64 run) outside test fixtures.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-science-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
