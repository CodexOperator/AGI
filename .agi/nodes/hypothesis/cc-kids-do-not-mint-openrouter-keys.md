---
id: hypothesis:cc-kids-do-not-mint-openrouter-keys
mint_id: 65669ccda725497bbf938fbbeeea5cdd
type: hypothesis
parents:
  - goal:s34
next_edges: []
edited_by: director
scaffold_hash: ad15b022ca7c6108
scale: engine
testable_claim: dispatch.py mints a provider credential only for harnesses whose adapter declares it needs one (pi does, claude-code does not); provisioning status after a CC-only wave shows engine_minted unchanged, and the test goes red when the harness check is removed
thought_session: L1.12
title: Cc kids do not mint openrouter keys
---
# hypothesis:cc-kids-do-not-mint-openrouter-keys

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
