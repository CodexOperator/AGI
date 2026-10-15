---
id: hypothesis:grok-bot-live-config-row-has-a-pytest
mint_id: 67dfbd7b92ca46b5a6862b11915344a2
type: hypothesis
parents:
  - goal:g7.25.3
next_edges: []
confidence: 0.8
edited_by: belam
scaffold_hash: 61faf59e0b279847
season: 2
testable_claim: test_grok_bot_adapter.py loads the real project .agi/config.json and adapters.resolve(cfg, grok-bot) returns adapter=grok_bot with bin equal to the live harnesses.grok-bot.bin cell; peers pi and copilot-cli still resolve; dispatch.py still has zero grok hits.
thought_session: parent-residue-g14-g17-remap
title: Live .agi/config.json grok-bot row is asserted by pytest
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:grok-bot-live-config-row-has-a-pytest

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
