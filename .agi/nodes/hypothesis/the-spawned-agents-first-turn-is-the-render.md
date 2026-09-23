---
id: hypothesis:the-spawned-agents-first-turn-is-the-render
mint_id: 64714fe834d44d509ff30a0cdd0ebd4c
type: hypothesis
parents:
  - goal:g1.9.2
next_edges: []
ceiling: 1.5 USD, <= 2 kids, pi parents
confidence: 0.7
edited_by: director-engine
scaffold_hash: c8345ea01c2f3e68
season: 2
testable_claim: After the fix, the prompt a dispatched parent or kid actually receives is brief.render's output (head + card + extras = the dispatch body) -- the harness adapters' build_command (pi first, then every adapter that assembles) take the rendered text instead of calling brief.assemble a second time, so the spawned agent's first turn equals the dry-run report and spawn.json byte for byte; _render_dispatch_brief also catches FaithRefError with the same loud fallback as RenderError; and extras_text handed to a role whose parts lack 'extras' refuses by name instead of being dropped; each proved by a committed test red on the pre-fix bytes (the spawned prompt captured from build_command in a fixture), with test_dispatch.py, test_adapters*.py and test_brief*.py green.
title: "the spawned agent's first turn is the render, not a second assemble in the adapter (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:the-spawned-agents-first-turn-is-the-render

# hypothesis:the-spawned-agents-first-turn-is-the-render

## Hypothesis

```
verified  director-engine 13:5xZ 09-23 on the post branch: pi_adapter.build_command -> _append_prompt_args(segs=brief.assemble(...))
          (bin/adapters/pi_adapter.py:205-219) builds the real spawned prompt; dispatch.py:1036-1062 _render_dispatch_brief renders only the
          report / spawn.json copy and catches brief.RenderError alone
```

## Agent Notes
assigned: director-engine (leaf goal:g1.9.2 of the brief.py batch); bytes verified by director-engine before minting.
