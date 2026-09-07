---
id: hyp:a00-4125fa6d-005488
mint_id: 5b0fa6527c794eb9ab599d0b70475925
type: hypothesis
parents: []
next_edges: []
edited_by: season.py
season: 1
thought_session: season
title: A00 4125fa6d 005488
---
# hyp:a00-4125fa6d-005488
## Hypothesis

**Domain**: architecture — agent-spawning via verdict nodes

**Claim**: pi's subagent system can be triggered programmatically via verdict node events.

**Mechanism**: When a verdict node is written to disk with `verdict: proved`, the agent orchestrator can detect this and spawn a builder subagent to implement the next task. The chain-engine's `_spawn_on_verdict()` function checks verdict state and calls subagent dispatch.

**What would prove it**: A script that (1) creates a "proved" verdict node, (2) calls pi's subagent API to spawn a builder, (3) verifies the subagent was dispatched with correct task context.

**What would disprove it**: subagent dispatch requires manual CLI invocation with no programmatic trigger API; pi does not expose verdict-change → agent-spawn as a capability.

**R1 testable criteria**:
- R1.1: `subagent` tool accepts task + agent config and returns a run ID
- R1.2: subagent can be dispatched from within a Python script (not just CLI)
- R1.3: verdict file state can be read and mapped to spawn conditions
- R1.4: spawned agent receives correct chain context (parent node IDs, verdict state)