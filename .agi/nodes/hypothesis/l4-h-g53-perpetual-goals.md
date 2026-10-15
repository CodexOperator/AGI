---
id: hypothesis:l4-h-g53-perpetual-goals
mint_id: 452adb72f05f47d48db286705f6d880f
type: hypothesis
parents:
  - idea:l4-g53-perpetual-goals
  - goal:g5.3
next_edges: []
edited_by: a00-8f32f863
loop: hypothesis:l4-chains-for-the-mapped-subgoals@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 55ae3ec3df1cc5c8
season: 2
testable_claim: "Twelve top-level gN goals flip to goal_kind: perpetual; goal:g11 does NOT flip. Node count is unchanged. Proved: run the flip, then snapshot-goals.py --render --check exits 0 (byte-identical round trip) and GOALS.md moves the twelve goals into its ## Perpetual section while goal:g11 stays out."
thought_session: iter-L4.28
title: L4.07 flips twelve gN goals to perpetual, never goal:g11
---
<!-- BODY:BEGIN -->
# hypothesis:l4-h-g53-perpetual-goals

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
