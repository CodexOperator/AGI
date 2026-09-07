---
id: hypothesis:provisioning-reads-the-workspace-weekly-budget
mint_id: 3499bb0f2ee54e638bb9fe8caa6b355d
type: hypothesis
parents:
  - goal:s34
next_edges: []
edited_by: season.py
scaffold_hash: 83259e94cf139e83
scale: engine
season: 1
testable_claim: provisioning.py reads the OpenRouter workspace weekly budget and its remaining amount before minting, refuses to mint (and dispatch.py reports the slot unadmitted with the reason) when the next key cannot be funded, and a fixture with an exhausted budget makes the refusal test go red when the check is removed
thought_session: season
title: Provisioning reads the workspace weekly budget
---
# hypothesis:provisioning-reads-the-workspace-weekly-budget

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?