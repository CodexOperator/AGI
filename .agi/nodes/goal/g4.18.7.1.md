---
id: goal:g4.18.7.1
mint_id: f94512fabe8d426eab1c2c609d343eac
type: goal
parents:
  - goal:g4.18.7
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.7.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 5dbca25c7fd22b72
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.7.1: viewport renders ONE node for both readers -- resolved names, body by the shared row index or a range, payload -- as --emit llm and --emit human from one stream, never a write (row W3a; assigned: director-general-1)"
town: core
---
# goal:g4.18.7.1

## Why this exists
goal:g4.18.7 bullets 2 and 4, placed by goal:g7.16.1.4 row W3. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): VERBS still holds "read" (write.py:543); `viewport.py` has --anchor, --emit human|llm|both and --verify, no single-node body render; grep_live and parked_carriers live in rotation_record.py (:49, :77), imported by write.py:2353 to unpark; the literal teaching form `write.py <id> 'read body|payload` sits in 8 files / 13 lines (10 files on a broader 'read body' grep), the count goal:g4.18.7 now carries (a5848c5a2; its earlier 23 counted a wider scope incl. tests).

## Target end-state
- `viewport.py` renders a single node: its names resolved (goal:g4.18.6.1), its body by goal:g4.18.5.1's row index or a line range, its payload, as --emit llm and --emit human from ONE stream.
- `viewport.py --verify` exits 0; the viewport's no-write self-grep test still passes (goal:g9).

## Invariants
- The render path never gains a write (goal:g9).

## Falsifier
1. `python3 extensions/agi/bin/viewport.py --anchor goal:g4.18.7 --emit llm` (or the single-node flag it grows) prints this node's body, and `viewport.py --verify` exits 0.
2. Negative: the viewport's no-write test fails.

## Out of scope
goal:g4.18.7.3 (the cut)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 4, stage 1, 20:3xZ 09-29) from goal:g4.18.7. Split into render, node-search move and the cut, because the cut repoints teachers only once the render exists. Hypothesis: viewport-renders-one-node-for-both-readers.
<!-- THOUGHT:END -->
