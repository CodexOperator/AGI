---
id: hypothesis:copilot-cli-remote-control
mint_id: 8115df994dce4feaba519881f3293618
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: f7948c3ba8ccdfab
season: 2
testable_claim: The copilot-cli adapter build command emits --remote on every unified-route spawn path, with the exact argv order copilot --model M --effort E --allow-all --remote -i ..., proven by adapter, dispatch dry-run, rotate dry-run fixtures, and focused tests.
thought_session: sensei-director
title: Copilot CLI posts expose remote control
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:copilot-cli-remote-control

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Added only the owner-ordered --remote flag at the shared Copilot adapter command seam and rotate.py seat command seam. The adapter produces --allow-all --remote before -p; rotation produces --allow-all --remote before -i. Evidence: 306 focused adapter/rotation tests passed and dispatch --dry-run emitted copilot --model auto --allow-all --remote -p.
<!-- THOUGHT:END -->
