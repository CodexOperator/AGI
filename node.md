---
id: hypothesis:a00-309f9215-3bd981
mint_id: 9fe454341da14755b79bb2bae46bf175
type: hypothesis
parents:
  - goal:g7.1
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 2c99e2bc67620087
season: 1
thought_session: season
title: A00 309f9215 3bd981
verdict: pending
---
# hypothesis:a00-309f9215-3bd981

## Hypothesis

Adding referential-integrity enforcement at parent-reference **creation time** (in the generator/spawn logic and kit resolution) prevents the class of unresolvable references that G7.1's post-hoc sweep had to clean up. The check must cover `spawns:` and `next_edges:` in addition to `parents:` — all three fields mint references that can dangle.

**Testable claim:** A pre-write integrity gate on the generator (`level3.py` / `spawn`) that validates every outgoing reference in `parents:`, `spawns:`, and `next_edges:` against the current node index will reject at least one bad reference before it lands on disk, for every generator run that would otherwise produce one.

**What would prove it:** Instrument the generator to catch and report intercept-time rejections. Run the full pipeline over the existing corpus (a cold generation that triggers all `build:` and `spawn:` paths). If ≥1 reference is caught and prevented from landing, the gate worked on real data.

**What would disprove it:** A clean run with zero rejections, followed by a manual sweep that finds new dangling references the gate should have caught but didn't — meaning the gate's scope or position in the pipeline is wrong.


## Agent Notes
Hypothesis: add pre-write integrity gate on generator covering parents, spawns, and next_edges to prevent dangling references at mint-time, closing G7.1's remaining gaps