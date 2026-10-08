---
id: verdict:dg2close-a01-697f4893-9bb21a
mint_id: d7813b45c647469e895ac7a0beb5d989
type: verdict
parents:
  - experiment:dg2close-a01-697f4893-9bb21a-check
  - hypothesis:a01-697f4893-9bb21a
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2close-a01-697f4893-9bb21a-check
scaffold_hash: 54c9980ec2b5a9b3
season: 2
title: "closing (goal:s18 retired): Lean disproved on the pre-retirement bytes: 1-4/10 sampled open build-site chains are covered by Domain-idea content (at most 28/52 even mentioned); L1.09 closed 29 by citing build nodes, none by citing Domain ideas; moot since L1.09"
town: core
verdict: inconclusive_lean_disproved:80
---
# verdict:dg2close-a01-697f4893-9bb21a

| conjunct | observed |
|---|---|
| ≥7/10 sampled open chains have an equivalent claim under the Domain ideas (proved) | NOT MET: 1/10 strict, 4/10 generous (row 6). Even the population-wide mention upper bound is 54% (row 4) |
| ≤3/10 (disproved) | met strictly (1/10); the generous count of 4/10 falls in the node's own 4-6 inconclusive band |
| `idea:domain-graph-core` (142 descendants) already covers the structural claims | its subtree has 68 descendants, and it covers 0-1 of the 3 graph-core chains in the sample (row 5) |
| the chains can close "without loss, by native graph content" | the actual close (L1.09) cited code build nodes for 29 chains and no Domain-idea content (row 7) |

**Why inconclusive_lean_disproved:80.** By the node's own grading, the sample sits at 1/10 (disproved) to 4/10 (inconclusive band), and nothing reaches the 7/10 needed for proved. The population-wide upper bound (54% merely mentioned) cannot reach 70% either. The actual retirement found its cover in build nodes, not in Domain ideas. It is not a flat "disproved" because "equivalent assertion" takes judgment, and the generous count lands inside the band the node defined as inconclusive. The claim is **moot** today: all 159 build-site nodes retired at L1.09 (0 live).
