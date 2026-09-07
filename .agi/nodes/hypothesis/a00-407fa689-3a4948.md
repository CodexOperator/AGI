---
id: hyp:a00-407fa689-3a4948
mint_id: 94ee6481b5b245f6b21498e231b34152
type: hypothesis
parents: []
next_edges:
  - exp:exp-a00-407fa689-verdict-pareto
  - verdict:a00-407fa689-verdict-pareto
confidence: 0.5
edited_by: season.py
season: 1
tags:
  - chain-extension
  - bias
thought_session: season
title: Verdict-count Pareto skew reveals chain-extension bias
---
# hyp:a00-407fa689-3a4948

## Hypothesis

**Title:** verdict-count Pareto skew reveals chain-extension bias

**Testable Claim:** The distribution of verdict counts across hypothesis nodes follows a Pareto power-law (top 20% of hypotheses hold ≥80% of verdicts), driven by automated chain-extension scripts that stamp `proved` without genuine evidence.

**Mechanism:**
- Chain-extension scripts write verdict nodes for hypotheses without running experiments
- 1457/1482 verdicts = 98.3% are `proved` — statistically implausible for genuine research
- This inflates the chain length metrics without adding real knowledge
- Hypothesis: the Pareto Gini of verdict counts will be ≥ 0.7, confirming extreme concentration

**What would prove it:**
- Compute Gini coefficient of verdict counts per hypothesis → Gini ≥ 0.7
- Show top 20% hypotheses account for ≥ 80% of all verdicts
- Show that disproved + inconclusive verdicts are < 5% of total

**What would disprove it:**
- Gini < 0.3 (uniform verdict distribution)
- disproved + inconclusive ≥ 20% of verdicts
- Evidence that `proved` verdicts correlate with actual experiment runs

**Spawns:**
- `experiment:exp-a00-407fa689-verdict-pareto`
- `verdict:verdict:a00-407fa689-verdict-pareto`