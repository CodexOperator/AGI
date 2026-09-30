---
id: goal:g6.51
mint_id: 8daad6ff476a41619a9d30e4a69a1e58
type: goal
parents:
  - goal:g6
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G6.51
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: a6e118798c7c5798
season: 2
status: retired
title: "G6.51: every hypothesis under a retired s-goal is parented by the nested g-goal it serves"
town: core
---
# goal:g6.51

# goal:g6.51

## Why this exists
goal:g6: the S goals under G6 were closed out in the council loop's S-goal sweep (alive, 02:2xZ 09-30: complete 22 · retired 10) while some of their hypotheses were still pending. belam measured 04:5xZ 09-30: 6 hypotheses still name a RETIRED s-goal as parent (s18 x4: a00-05c5c2b4-547067, a00-15d05ac0-7ef787, a01-1f2762d5-1d90c0, a01-697f4893-9bb21a; s32 x1: a00-c4b84f52-f58e90; s34 x1), and goal:s31 held 4 more until belam re-marked it complete (all 4 had verdicts).

## Target end-state
- No hypothesis names a retired s-goal as a parent: each one is parented by the nested g-goal it actually serves (the deepest live leaf whose target end-state its claim advances), with its mint_id and verdict unchanged.
- goal:s31's four closed hypotheses sit under the nested g-goal their proved fix belongs to.

## Invariants
- A re-parent keeps the node's mint_id, body and verdict; only `parents:` changes, one write.py version per node, the reason in its THOUGHT.
- Retire, never delete.

## Falsifier
1. For every s-goal with status retired: `grep -l -E '^\s*- goal:<s-id>\s*$' .agi/nodes/hypothesis/*.md` returns zero files.
2. `python3 extensions/agi/bin/links.py links` reports broken = 0 after the moves.

## Out of scope
goal:g1.31 (PASS B3 residues) · goal:g7.16.1 (the council loop bundles).

## OWNER 2026-09-30 04:5xZ, verbatim
"Move all hypotheses under all retired s goals to be patented by appropriate nested g-goals"

## Agent Notes
Assigned to **director-general-6**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-S2-L5-XX 05:1xZ 09-30: retired at mint. The owner ruled that the re-parenting needs no goal. Owner 05:0xZ 09-30, verbatim: "The regime doesn't need a goal. We're just adjusting parenthood". The hypotheses are re-parented by direct write.py edits instead.
<!-- THOUGHT:END -->
