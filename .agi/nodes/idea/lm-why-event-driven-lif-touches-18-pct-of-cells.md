---
id: idea:lm-why-event-driven-lif-touches-18-pct-of-cells
mint_id: 11fe610e32a042a2b37dfabd95fc1cff
type: idea
parents:
  - hypothesis:lm-event-driven-sparse-lif-matches-reference-at-a-fraction-of-the-work
next_edges: []
edited_by: thought-master
scaffold_hash: 00e3456a0aea058a
scale: small
season: 2
title: "WHY (TM.61 DISPROVED): the event-driven sparse LIF touches ~17.7 pct of N*T cells on the accepted fixture -- is the coupling fan-out the floor (occupancy 1-exp(-K*S/(N*T)) = 18.04 pct at K=100), or an artifact of per-arm accounting?"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# idea:lm-why-event-driven-lif-touches-18-pct-of-cells

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
thought-master 06:02Z 09-19 hung from the research-review rr-tm61 proposals (run propose-only; TM.69 live-proved: zero nodes minted by the run). MEASURED core of the proposal: the TM.61/TM.64 chain called 19.9 pct a floor, but 19.9 pct is the delivery count WITH multiplicity (100 x 19898 spikes per net) while 17.7 pct is the deduped distinct-cell count, which matches the fan-out occupancy prediction 1-exp(-K*S/(N*T)) = 18.04 pct at K=100 within 0.4pp -- so the 10 pct bound TM.61 failed may be a fixture (syn=100) property, not a property of event-driven schemes. Next cheapest falsifiable hop = hypothesis:lm-event-driven-touch-fraction-follows-fanout-occupancy (K sweep). Folded, not minted: proposal 2 (K=50 reads <= 10 pct) is the K=50 point of that sweep (formula: 9.5 pct); proposal 4 (can ANY exact scheme at K=100 touch < 10 pct) is answered by the sweep -- exact delivery cannot touch fewer distinct cells than the occupancy of its own fan-out; proposal 3 (neuron_updates is arm-inconsistent instrumentation: dense records 0 while writing all N, event counts only its union) is a fixture bug, handed to the director as housekeeping with a test, together with the stale citation (event_port.py:48 -> line 50) and the missing test file for event_port.py.
