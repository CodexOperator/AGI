---
id: hypothesis:verify-runs-grid-commit-before-smoke
mint_id: ecc756a2b9024f418c458ae50c33b92e
type: hypothesis
parents:
  - goal:s34
next_edges: []
edited_by: season.py
scaffold_hash: 68096291cfd1c1dc
scale: engine
season: 1
testable_claim: The declared verify workflow in command:commands orders grid-commit before smoke so the evidence gate has run before the metric is read; unevidenced_decisive_verdicts printed by verify is 0 whenever grid commit demoted everything, and a test that inserts an unevidenced proved verdict then runs verify goes red if the order is reverted
thought_session: season
title: Verify runs grid commit before smoke
---
# hypothesis:verify-runs-grid-commit-before-smoke

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?