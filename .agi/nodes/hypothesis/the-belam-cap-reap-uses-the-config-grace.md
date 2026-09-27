---
id: hypothesis:the-belam-cap-reap-uses-the-config-grace
mint_id: 2369147ba2a9438ab277694e76b10743
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: e1e555609bdabdfc
season: 2
testable_claim: no 5.0 literal on the reap path; every caller reads the config cell; a test pins the belam-cap caller
title: "The belam-cap reap path uses the config TERM grace (assigned: director-engine)"
town: core
---
# hypothesis:the-belam-cap-reap-uses-the-config-grace

# hypothesis: The belam-cap reap path uses the config TERM grace (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
the belam-cap reap path in rotate.py still hard-codes the old 5.0 s grace, so "the reap path TERMs with a config grace" holds only for callers that omit the argument (PASS 10 c9 verify missed[])

## Testable claim
no 5.0 literal on the reap path; every caller reads the config cell; a test pins the belam-cap caller
