---
id: hypothesis:a00-05c5c2b4-547067
mint_id: f30cd364ea3c42468bea42beb8d19f62
type: hypothesis
parents:
  - goal:g1.2
next_edges: []
confidence: 0.0
edited_by: belam
evidence_runs:
  - experiment:dg2close-a00-05c5c2b4-547067-check
scaffold_hash: 791573d3b3d0fc5d
season: 1
thought_session: season
title: "S18: Open build-site hypotheses lack experiments, not evidence"
verdict: proved
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Moved from goal:s18 to goal:g1.2 because its claim (most open build-site chains lacked experiments, not evidence; proved) sized the work of retiring cavekit's build-site layer into graph-native nodes. goal:g1.2 (horizon, a leaf: take cavekit's pieces, do not merge wholesale, one vocabulary not four) is the live goal that owns the cavekit boundary s18 was retiring; no deeper live goal carries it. Owner, verbatim: "Move all hypotheses under all retired s goals to be patented by appropriate nested g-goals". Parenthood only (owner: "The regime doesn't need a goal. We're just adjusting parenthood"): mint_id, body and verdict unchanged.
<!-- THOUGHT:END -->
