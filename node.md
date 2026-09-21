---
id: hypothesis:cc-adapter-refuses-git-handoff-and-dispatch
mint_id: 867b85a5d32b49f0a25812db77b7d912
type: hypothesis
parents:
  - goal:s34
next_edges: []
edited_by: season.py
scaffold_hash: adab5acac217108c
scale: engine
season: 1
testable_claim: claude_code_adapter.build_command disallows every git verb, writes to HANDOFF.md and CLAUDE.md, and running dispatch.py, for both tiers; a spawned CC parent that tries any of them gets a permission denial recorded in permission_denials, and the test goes red when the disallow list is trimmed
thought_session: season
title: Cc adapter refuses git handoff and dispatch
---
# hypothesis:cc-adapter-refuses-git-handoff-and-dispatch

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?