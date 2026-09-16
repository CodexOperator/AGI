---
id: hypothesis:workflow-stages-dispatch-as-kids
mint_id: 349ea19efd4a4e87bd74d087d2034b64
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 11e822cb4011291f
season: 2
testable_claim: workflow.py pi and copilot-cli stages execute through dispatch.py child spawns, each with a spawn_budget lease, provisioning credential, session directory under .agi/sessions/iter-<run_key>/, manifest timeout_s, and completion events feeding the shared RunView; fixtures prove one lease and one completion record per stage without minting during tests, and a real merge-up-review copilot-cli dry/live path is observable without a raw pi subprocess.
title: Workflow stages dispatch as kids
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:workflow-stages-dispatch-as-kids

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
