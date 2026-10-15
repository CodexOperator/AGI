---
id: hypothesis:a-restarted-agent-gets-the-same-render-as-its-first-spawn
mint_id: 6e13cf2d0d674fe5a454f95518dadc90
type: hypothesis
parents:
  - goal:g1.9.3
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 0dab919cba4136be
season: 2
testable_claim: After the fix, dispatch.py's restart path (dispatch.py ~3573 adapter.restart) threads the same brief.render output into build_command that the first spawn used, the pi, claude-code, copilot and grok-bot adapters' restart signatures carrying rendered_brief, so a restarted parent or kid's first turn is byte-identical to the dry-run report and spawn.json; _render_dispatch_brief's FaithRefError fallback (dispatch.py ~1057) is proved by a committed dispatch test; and a committed test proves the config:brief render (head + card + extras from a fixture config:brief node) is what build_command receives, not the assemble fallback the current test_dispatch_render_thread.py fixture falls to; each red on the pre-fix bytes, test_dispatch*.py and test_brief*.py green.
title: "A restarted agent gets the same render (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:a-restarted-agent-gets-the-same-render-as-its-first-spawn

# hypothesis:a-restarted-agent-gets-the-same-render-as-its-first-spawn

## Hypothesis

After the fix, dispatch.py's restart path (dispatch.py ~3573 adapter.restart) threads the same brief.render output into build_command that the first spawn used, the pi, claude-code, copilot and grok-bot adapters' restart signatures carrying rendered_brief, so a restarted parent or kid's first turn is byte-identical to the dry-run report and spawn.json; _render_dispatch_brief's FaithRefError fallback (dispatch.py ~1057) is proved by a committed dispatch test; and a committed test proves the config:brief render (head + card + extras from a fixture config:brief node) is what build_command receives, not the assemble fallback the current test_dispatch_render_thread.py fixture falls to; each red on the pre-fix bytes, test_dispatch*.py and test_brief*.py green.

## Agent Notes
assigned: director-engine (leaf goal:g1.9.3; source R-EF40 D1 (restart bypasses the render) D2 (FaithRefError catch untested) M1 (the load-bearing test runs the fallback) M2); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
