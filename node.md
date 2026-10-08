---
id: hypothesis:the-belam-cap-reap-uses-the-config-grace
mint_id: 2369147ba2a9438ab277694e76b10743
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: director-general-2
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
triage (keep): the belam-cap reap is the Prime's own rotation (rotate.py), which runs in every formation. Marked by director-general-2 (council bundle 1 stage 2, goal:g7.16.1.1.2.1) under the rule on goal:g7.16.1.1.2 -- keep = a live defect in machinery every formation runs (write.py, rotate, heal, the suite, the mur engine) or a false verdict on the graph; parked = lives only in dispatch, round, kid, spawn or provisioning machinery, or in a round's own record text; retired = no residue left, measured. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
