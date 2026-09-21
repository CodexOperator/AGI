---
id: hypothesis:a00-05c5c2b4-547067
mint_id: f30cd364ea3c42468bea42beb8d19f62
type: hypothesis
parents:
  - goal:s18
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 791573d3b3d0fc5d
season: 1
thought_session: season
title: "S18: Open build-site hypotheses lack experiments, not evidence"
verdict: pending
---
# hypothesis:a00-05c5c2b4-547067

## Hypothesis

**Claim:** The majority (>50%) of the 50 open build-site hypothesis chains (`origin: build-site`, `type: hypothesis`, no verdict descendant) have never had an experiment defined — no experiment node lists them in `parents:`. This means closing them requires creating and running experiments from scratch, not re-evaluating pre-existing evidence.

**What would prove it:** Audit all 50 open hypotheses and count how many have zero experiment children. If 26+ have no experiment edge, the claim is proved.

**What would disprove it:** If fewer than 26 lack experiments — meaning most open hypotheses already have experiments defined but the experiments were never run or produced inconclusive results — then the bottleneck is not experiment definition but execution.

**Motivation (from goal:s18 THOUGHT):** The owner directed walking these 52 chains and closing them. Knowing whether the blocker is missing experiments or stalled evidence decides the strategy: batch-create experiments vs. batch-run existing ones. If most were never experiments, we batch-spawn them; if most had experiments that went nowhere, we triage the inconclusive ones on their own terms.

**Secondary claim (observable en passant):** Among open hypotheses that DO have an experiment edge, most of those experiments will themselves have no evidence recorded — confirming a two-tier gap (experiment defined but not executed).


## Agent Notes
Hypothesis: most open build-site chains lack experiments, not evidence. Testable: audit the open build-site hypotheses — if a majority have zero experiment children, proved. Motivates: batch-create vs batch-run. Node scaffold filled. 1380/1381 tests pass (1 pre-existing provisioning flake unrelated).

<!-- THOUGHT:BEGIN -->
Parent review, iter 1013 (a01-32fa757d). The kid's claim was sound but it hardcoded the goal's 2026-09-03 snapshot — "52 open" — and the corpus has moved since: counted 2026-09-03 on iter 1013, the 61 `origin: build-site` hypotheses now split 11 verdict-reached / 50 open (verdict reached = a verdict node directly, or via an experiment child). So the denominator is 50, not 52, and the majority threshold is 26+, not 27+. I also reworded "next_edges do not point to any exp:* node" to "no experiment node lists them in parents:", because the corpus stores edges downward as `parents:` on the child — the direction error `experiment:a01-5a8f6fc8-3e72b6` already paid for once. Verdict stays `pending`: no audit run exists yet, and the kid's report (struggles: none) missed that its own denominator was stale — the kid read the goal's number without counting.
<!-- THOUGHT:END -->