---
id: hypothesis:l2w2-writer-stamps
mint_id: 2a99a78d4eb04952b9fc382b4f7882a4
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: director
scaffold_hash: 86f2075865dfcb02
testable_claim: Every node minted through node_writer.py carries season, loop, model and profile stamped from the ladder node and the spawning environment, and dispatch.py exports that environment to every agent it spawns
thought_session: agi-master-2026-09-06
title: "L2 wave 2: l2w2-writer-stamps"
---
# hypothesis:l2w2-writer-stamps

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILES: extensions/agi/bin/node_writer.py, extensions/agi/bin/dispatch.py (or the adapter that builds the child environment; keep the ANTHROPIC and CLAUDE_CODE scrub intact), tests. RULE: dispatch.py exports AGI_LOOP=<target goal or node id>@s<current_season>, AGI_MODEL=<model string it chose>, AGI_PROFILE=<spawn profile, default balanced>, AGI_TIER=<tier>, AGI_SEASON=<current_season from the ladder node> into each spawned agent's environment. node_writer.py, at mint only (never on update), stamps season from AGI_SEASON else the ladder node else 1, and loop, model, profile from the environment when present; absent means absent, never a fabricated value. Existing nodes are untouched. VERIFY red-first: a mint under a fake environment carries all four; a mint with no environment carries season only; an update to an existing node does not add or change them; suite green. Section 2, Loop ownership. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs to cli.py done, your own experiment id counts), every verify command with its actual output in the body. Engine files are edited in place; suite via python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md
