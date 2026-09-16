---
id: hypothesis:l4-dispatch-takes-a-per-round-cap-and-refuses-when-cap-exceeds-pool-headroom
mint_id: 1f7d29ff07194c868cae141a7acd7b0f
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 609e58218014f45c
season: 2
testable_claim: "Measured 2026-09-16 08:37Z (sensei-director dispatching SM.35): dispatch.py has no per-round spend cap flag, so a director told to cap a parent at 2 dollars could only dispatch at the standing 5-dollar provisioning limit and pace by line ceiling instead. Claim: dispatch.py accepts --cap <usd> and mints that round provisioning key at exactly that limit (provisioning.py already mints capped keys per spawn, L4.368); with no flag the standing limit applies unchanged; and before minting, dispatch reads the live pool (the credits endpoint) and REFUSES BY NAME when cap exceeds pool minus the 5-dollar floor minus the sum of caps on rounds already live tree-wide (spawn_budget knows them), printing the three numbers. Tests: cap written to the key limit; no-flag path byte-identical; refusal message names pool, floor, live-cap sum. Ceiling 40 production lines, one kid."
title: L4 dispatch takes a per round cap and refuses when cap exceeds pool headroom
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dispatch-takes-a-per-round-cap-and-refuses-when-cap-exceeds-pool-headroom

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
