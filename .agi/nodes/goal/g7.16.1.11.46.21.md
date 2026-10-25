---
id: goal:g7.16.1.11.46.21
mint_id: c65d0da6e7394179b3891a73b163b141
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.21
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - U3
season: 3
status: active
title: "G7.16.1.11.46.21: U3 -- ONE spawn verb, agi-in <capsule>, with a MANIFEST (scope · reach · at · pull · atoms); agi-kid and the dispatch skill's spawn collapse into it"
town: local-maxxing
---
# goal:g7.16.1.11.46.21

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §3, §24, §39. Council rows: sp 6 (the falsifier is the behavior, since a grep for `case.*K[12]` passes on a rename), aio 5 (it reads the repo bytes, never one host's home). The atoms: MANIFEST line was specified by M3 (goal:g7.16.1.11.46.4); this leaf fills it from the pack route.

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.21 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 1.2 | "simplify / unify" | target:§0 (every rule = a cell), §24 (one spawn path) |
| 1.9 | "mathematical guardrails: scope/graph packs, parent/kid inheritance" | target:§2 (§Z1/§Z2), §24 (`scope ⊆ director's`) |
| 2.9 | "workflows ARE spawns ARE subagents ARE posts" | target:§24, §27, §29 (flow = chain = post node) |
| 3.2 | "one spawn/dispatch path; pull setting" | target:§24 |

## Target end-state
- `agi-in <capsule>` is the one spawn path; its MANIFEST carries scope, `reach closed|open`, at, `pull: graph|director|none`, and `atoms:`.
- `agi-wt pull` refuses a mint outside a closed reach by name.
- agi-kid is absent from the installed set; the dispatch skill names agi-in.

## Invariants
- Spawns stay under the spawn bound and the memory guard (W1 K7).
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/agi-in.t.sh` exits 0: agi-in spawns exactly once per pull value (graph, director, none) against a stub harness; an out-of-reach mint is refused by name; mutant: reach open on a closed capsule reads RED.
2. Negative, over the REPO bytes (.agi/nodes/.geometry pieces and the installed set's sha256 matching them): no piece named agi-kid is installed, and no skill names agi-kid as a spawn route.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-goals-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
