---
id: hypothesis:lm-jev-q1-label-is-ambiguous
mint_id: b232490b882446cb9a3faedeab37f26e
type: hypothesis
parents:
  - idea:lm-why-jev-echoes-leaked-verdicts
  - goal:g14
next_edges: []
ceiling: <= 1 USD OpenRouter (parent+kid); 0 API calls; 0 compute; no downloads on ARM4C without an owner yes; runs <= 10 min
edited_by: brainstorm
falsifier: Pair disagreement is at or below 0.05 with a CI excluding 0.15 (the labels are consistent and the q1 gap is real model error, not target noise) OR every disagreeing pair is explained by a documented pre-review vs post-review transition recorded on the nodes (then the label is stale, not ambiguous, and the fix is a label rule, not a new model).
scaffold_hash: 4f44b699ffc32e3c
season: 2
testable_claim: "Build every (verdict node, experiment node) pair where the verdict node names the experiment in parents/evidence_runs AND both carry a recorded verdict class. Measured preliminary: 50 such pairs, 38 agree, 12 disagree = 0.240 disagreement. Claim: the q1 label is self-inconsistent at >= 0.15, so the achievable q1 ceiling is bounded well below 1.0 and the pooled q1 number mixes the experiment self-report with the reviewed verdict. Report the pair count, disagreement rate with a bootstrap CI, a confusion of the disagreements by class pair, and the q1 agreement recomputed against the reviewed-verdict label for the subset where a single reviewed verdict exists."
tests: ONE pi parent + ONE kid, ARM4C-light slot (pure Python, CPU, no network); steps (1) parse all 170 verdict nodes and 1435 experiment nodes, extract verdict class and experiment refs from parents/evidence_runs; (2) join and count pairs, compute disagreement and a 1000-resample bootstrap CI, confusion by class pair; (3) recompute q1 agreement against the reviewed label where a single one exists and compare to the self-label; rows to bench/<utc>.jsonl, kid persists rows after every probe, parent commits promptly, FILE SCOPE .agi/context/local-maxxing/typesafe/, anonymization rule (hosts/IPs/GPU models/locations/key ids never; aliases ARM4C GPU2070S CPU8G EDGE), kid line_ceiling 120
title: "WHY jev echoes, hop 7 (anything better, TARGET): q1 is not one label -- 12 of 50 (24.0 percent) verdict-node/experiment-node pairs disagree on the verdict class, so the pooled q1 agreement is capped by target ambiguity before any model runs"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-q1-label-is-ambiguous

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
