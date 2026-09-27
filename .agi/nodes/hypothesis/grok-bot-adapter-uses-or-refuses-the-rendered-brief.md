---
id: hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief
mint_id: 2114058bf27f4aa9a511cd66893b7b96
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: a00-b985fc32
scaffold_hash: b20c178a6f54463c
season: 2
testable_claim: grok_bot_adapter.py (~64) passes the rendered brief to the bot or refuses with a named error, never accepts and discards it; engine-delta-7's verifier read the discard as an intentional stub -- decide which and record it in THOUGHT.
title: "The grok-bot adapter uses the rendered brief or refuses it by name (assigned: director-engine)"
town: core
---
# hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief

# The grok-bot adapter uses the rendered brief or refuses it by name

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source round a-restarted-agent-gets-the-same-render-as-its-first-spawn (demote).

**Testable claim.** grok_bot_adapter.py (~64) passes the rendered brief to the bot or refuses with a named error, never accepts and discards it; engine-delta-7's verifier read the discard as an intentional stub -- decide which and record it in THOUGHT.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The discard was a silent brief loss, not an intentional stub (a00-d9c0ff8e), AND there was a second silent loss beneath it: a falsy rendered_brief with an empty context_file emitted -p EMPTY, an empty prompt, with no name anywhere (P3, a00-b985fc32). Both arms of this claim now hold on the built bytes: the render is spent in argv, or the both-empty state refuses by name naming the harness and both inputs; restart degrades that refusal to None so the goal:g4.7 contract is unbroken. What is still a stub is the SPELLING only: -p is a guessed slot pending goal:g17.14.1.
<!-- THOUGHT:END -->
