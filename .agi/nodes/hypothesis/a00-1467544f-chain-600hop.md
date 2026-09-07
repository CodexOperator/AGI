---
id: hyp:a00-1467544f-chain-600hop
mint_id: 34a607fdc8d8411aa353f276fa53ecb0
type: hypothesis
parents:
  - idea:domain-bootstrap-discovery
next_edges:
  - exp:a00-1467544f-chain-600hop
confidence: 1.0
edited_by: season.py
season: 1
subgraph: false
tags:
  - chain-engine
  - extension
  - 600-hop
thought_session: season
title: "Hypothesis: Extend 6 chains from 502 to 600 hops"
---
**Hypothesis:** Adding 49 verdict→experiment→verdict cycles (cycles 248-296) to the 6 chains currently at 502 hops will produce chains of 600 hops, confirming the capillary DAG formula hops = 2*cycle + 8 holds at cycle 296.

**What would prove it:** After running the extend script, find_chains() reports ≥6 chains at ≥600 hops.

**What would disprove it:** Chains fail to reach 600 hops — indicates a structural limit, graph loader error, or chain-engine bug at high cycle counts.

**Pass threshold:** longest_chain_length ≥ 600 hops

6 chains extended from 502 to 600 hops. Formula hops=2*cycle+8 verified at cycle 296. 20 chains total, 274 tests pass.

**Deviation, 2026-08-27.** This node carried `verdict: proved` in its own frontmatter. `[hypothesis].md` declares no `verdict` field, and `metrics.py` reads `verdict:` on *any* node — so the duplicate registered as an unevidenced decisive verdict and was the sole contributor to `unevidenced_decisive_verdicts=1`. The judgement is unchanged and lives where it belongs: `verdict:a00-1467544f-chain-600hop`, `proved`, backed by `exp:a00-1467544f-chain-600hop`. Only the duplicate was removed.