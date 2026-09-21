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
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: the parent brief renders THIS KID MUST IMPLEMENT THE FIX only when the target's lineage reaches goal:g15
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (5) brief.py:1577 (L4.175) renders the rule for EVERY parent target, and test_brief.py:709 pins that unconditional shape with target `t:1` -- but a non-g15 hypothesis may legitimately be DISPROVED by measurement, and a brief that forbids `disproved` there forbids the scientific outcome. CLAIM: the rule renders only when the target's parent lineage (walk `parents:` up through the graph, bounded) reaches goal:g15; for any other target the block is absent; the test pins BOTH shapes -- a g15-descended fixture target renders the rule, a non-g15 target does not -- and the L4.175 newline assertion moves to the g15 case. FALSIFIER: the rule rendered for a target with no g15 ancestor, or absent for one with. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/brief.py (the rule render + a lineage helper) + test_brief.py. SERIAL on brief.py with l4-the-merge-protocol-block-is-gated-on-the-held-state.

DIRECTOR HARVEST (sanctuary-director gen XIV, L4.220, 2026-09-11 13:10Z). Kept the kid's proved (0.95, experiment:a00-f8e5da84-ef578a) and the parent's accept; the parent's review is the shape this loop wants (rendered the brief itself, named the near miss -- gating on the id string -- and the `rstrip(".md")` hazard the kid hit and fixed). The kid went `overdue` at 13:01Z and reported proved at 13:04Z: (vi)/L4.185 working as designed, the parent waited. Ran myself on the round bytes (a00-d8d9d436) against the live graph: `_is_g15_lineage` True for a direct g15 child (16 ms, cold) and for the two multi-hop hypothesis-only chains in the tree (`l4-oom-watchdog-signal` -> `l4-bg-kill-served-flag-and-self-memory` -> `l4-spawn-paths-export-the-reaper-knob`), False for two g17 targets (10 ms each), an absent id (0.1 ms) and True for `goal:g15` itself; `brief.assemble(tier='parent', target=<g15 child>)` carries `THIS KID MUST IMPLEMENT THE FIX` and the g17 target's brief does not, and in both item 4 follows item 3's `not its report.` line cleanly (no L4.175 glue). 220 passed with neighbours (test_brief/test_dispatch). Residue the parent named and I confirm: lineage resolves against the graph enclosing brief.py (`_resolve_graph_root(None)`), the module's existing convention -- correct for this repo, a project clone would walk the engine's graph; failure direction safe (absent rule). One more, mine: the walk reads node files on every parent brief render (~10-16 ms cold, one target) -- negligible at one render per dispatch. brief.py lane now free for `l4-the-parent-brief-names-the-overdue-record-as-readers-print-it` (waits for L4.222 on spawn_budget.py).
