---
id: hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated
mint_id: ba5e83a7250f40e39e5f81d391852ef3
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 160ed083cd5824e4
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (5) brief.py:1577 (L4.175) renders the rule for EVERY parent target, and test_brief.py:709 pins that unconditional shape with target `t:1` -- but a non-g15 hypothesis may legitimately be DISPROVED by measurement, and a brief that forbids `disproved` there forbids the scientific outcome. CLAIM: the rule renders only when the target's parent lineage (walk `parents:` up through the graph, bounded) reaches goal:g15; for any other target the block is absent; the test pins BOTH shapes -- a g15-descended fixture target renders the rule, a non-g15 target does not -- and the L4.175 newline assertion moves to the g15 case. FALSIFIER: the rule rendered for a target with no g15 ancestor, or absent for one with. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/brief.py (the rule render + a lineage helper) + test_brief.py. SERIAL on brief.py with l4-the-merge-protocol-block-is-gated-on-the-held-state."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: the parent brief renders THIS KID MUST IMPLEMENT THE FIX only when the target's lineage reaches goal:g15
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (5) brief.py:1577 (L4.175) renders the rule for EVERY parent target, and test_brief.py:709 pins that unconditional shape with target `t:1` -- but a non-g15 hypothesis may legitimately be DISPROVED by measurement, and a brief that forbids `disproved` there forbids the scientific outcome. CLAIM: the rule renders only when the target's parent lineage (walk `parents:` up through the graph, bounded) reaches goal:g15; for any other target the block is absent; the test pins BOTH shapes -- a g15-descended fixture target renders the rule, a non-g15 target does not -- and the L4.175 newline assertion moves to the g15 case. FALSIFIER: the rule rendered for a target with no g15 ancestor, or absent for one with. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/brief.py (the rule render + a lineage helper) + test_brief.py. SERIAL on brief.py with l4-the-merge-protocol-block-is-gated-on-the-held-state.
