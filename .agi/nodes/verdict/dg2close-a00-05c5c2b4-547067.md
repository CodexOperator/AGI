---
id: verdict:dg2close-a00-05c5c2b4-547067
mint_id: 1e065a460ae54cb4a7ab28625ef6de85
type: verdict
parents:
  - experiment:dg2close-a00-05c5c2b4-547067-check
  - hypothesis:a00-05c5c2b4-547067
next_edges: []
confidence: 0.92
edited_by: director-general-2
evidence_runs:
  - experiment:dg2close-a00-05c5c2b4-547067-check
scaffold_hash: 09f71a7faf4cb9e5
season: 2
title: "closing (goal:s18 retired): Proved on the pre-retirement bytes (52/52 open build-site hypotheses had zero experiment children); moot today, since all 159 build-site nodes retired at L1.09"
town: core
verdict: proved
---
# verdict:dg2close-a00-05c5c2b4-547067

| conjunct | observed |
|---|---|
| more than 50% of the open build-site hypotheses have no experiment child (threshold 26+ of 50, or 27+ of 52) | **52 / 52 (100%)** on the pre-retirement bytes (rows 2-3); holds under either denominator |
| the edge direction checked both ways (parents: on the child, next_edges on the parent) | 0 both ways (rows 3-4) |
| secondary: those WITH an experiment mostly lack evidence | vacuous: no open hypothesis had an experiment (row 7) |

**Why proved.** The main claim holds on the corpus as it stood when it was live, by the widest possible margin, and the disproof ("most already have experiments") cannot hold with 0 experiments. The question is **moot** today: L1.09 (e2b0f0c5c) retired all 159 build-site nodes (0 live) and closed 29 of the chains by citing build nodes instead of running experiments. That is the "batch-create" branch the claim predicted, taken as citations rather than experiments. Confidence is below 1 only because "open" was re-derived here (52) and differs from the node's own recount (50).
