---
id: hypothesis:lm-event-driven-touch-fraction-follows-fanout-occupancy
mint_id: affc29d8e87f475d9f06307f19439224
type: hypothesis
parents:
  - idea:lm-why-event-driven-lif-touches-18-pct-of-cells
next_edges: []
edited_by: thought-master
scaffold_hash: 0327198b002212c6
season: 2
testable_claim: "On the accepted TM.48 fixture (purely excitatory g 0.9, amp 9.999, Jacobi, 4 seeds) with the TM.64-fixed event_port.py (gap = t - tl - 1, bit-exact vs dense), sweeping the coupling fan-out K over {10, 25, 50, 100} with everything else fixed: the DEDUPED distinct-cell touch fraction D(K) is within 1.0 pp of 1-exp(-K*S_K/(N*T)) at every K, where S_K is the measured spike count at that K (recorded per seed), and D(50) <= 10.0 pct on 4/4 seeds while the event arm stays bit-exact against dense at every K; falsifier: |D(K) - formula| > 1.0 pp at any K on >= 2 seeds, or D(50) > 10 pct on any seed while exactness holds -- then the touch count is not fan-out occupancy and the accounting itself (proposal 3) must be audited before any floor claim; 0 USD, CPU8G via agi-run (numpy), cap 1 USD pi"
title: "TM.61 WHY hop 1: the distinct-cell touch fraction of the exact event-driven LIF equals the fan-out occupancy 1-exp(-K*S/(N*T)) at every K, so 17.7 pct at K=100 is a floor of the fixture, not of event-driven schemes (K=50 reads ~9.5 pct)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-event-driven-touch-fraction-follows-fanout-occupancy

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
