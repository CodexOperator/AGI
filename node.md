---
id: hyp:a00-407fa689-verdict-repair
mint_id: c98782837134412b96939215180f5d48
type: hypothesis
parents:
  - hyp:a00-407fa689-3a4948
next_edges:
  - exp:exp-a00-407fa689-verdict-repair
confidence: 0.5
edited_by: season.py
season: 1
tags:
  - chain-extension
  - repair
  - structural-bias
thought_session: season
title: Synthetic Verdict Parent Repair
---
# hyp:a00-407fa689-verdict-repair
## Hypothesis

**Testable Claim:** The 99.7% orphaned verdict rate can be reduced to < 80% by implementing an automated repair strategy that traces verdict IDs back to parent hypotheses via domain name matching.

**What would prove it:** Repair strategy recovers ≥ 50% of orphaned verdicts via traceable domain patterns.

**What would disprove it:** < 20% of orphaned verdicts are recoverable via domain patterns; majority require manual reconstruction.

**Experiment:** `exp:exp-a00-407fa689-verdict-repair.py`