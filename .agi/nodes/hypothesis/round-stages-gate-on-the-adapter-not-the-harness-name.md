---
id: hypothesis:round-stages-gate-on-the-adapter-not-the-harness-name
mint_id: 302bbb6500a5433fbd5618b54e9f485a
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: b2723fffc940da7a
season: 2
testable_claim: round-mur/round-research-review run under --harness pi-free; a claude-code seam still refuses by name; the gate reads harnesses.<h>.adapter; a test fails on 6c403aeb4b
title: "A kind:round stage is gated on the harness ADAPTER cell, not the name pi (assigned: director-engine)"
town: core
---
# hypothesis:round-stages-gate-on-the-adapter-not-the-harness-name

# hypothesis: A kind:round stage is gated on the harness ADAPTER cell, not the name pi (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
workflow.py:2417 (range :2409-2421) `if harness != "pi"` refuses every kind:round stage with rc 6 for --harness pi-free / pi-local although harnesses.<h>.adapter = pi runs the identical _run_round_stage path (PASS 10 c3 verify missed[], c10 template_max YES)

## Testable claim
round-mur/round-research-review run under --harness pi-free; a claude-code seam still refuses by name; the gate reads harnesses.<h>.adapter; a test fails on 6c403aeb4b
