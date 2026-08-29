---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r9"
mint_id: 46848272a36349fa948f5feaf908c7ce
origin: build-site
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R9
testable_claim: Agent Timeout and Healing Mechanism
title: "autoresearch-tree-skill/R9: Agent Timeout and Healing Mechanism"
type: hypothesis
---

**Description:** When an agent exceeds the configured timeout, a healer subagent is dispatched to assess the situation, collect partial results, and signal completion with an appropriate verdict state.

**Acceptance Criteria:**
- [ ] An agent process exceeding `agent_timeout_mins` is terminated with SIGTERM, then SIGKILL if unresponsive after 30 seconds
- [ ] A healer subagent dispatched on timeout receives the original task, elapsed time, and any partial output from the session directory
- [ ] The healer produces a verdict node with state `inconclusive_lean_proved:N` where N reflects the proportion of remaining work
- [ ] The iteration continues with remaining agents; partial results from timed-out agents are included in the manifest
- [ ] Timeout handling does not corrupt session state for other running agents

**Dependencies:** chain-engine (R8 verdict taxonomy), skill/R3 (parallel dispatch)

## Cross-References

- See also: cavekit-graph-core.md (R9 portability, R10 bootstrap)
- See also: cavekit-schema-registry.md (R4 validation, R8 built-in schemas)
- See also: cavekit-environment-indexers.md (invoked as part of the loop)
- See also: cavekit-chain-engine.md (R3, R4, R6, R7, R8, R9 — chain ranking, queries, taxonomy, configuration)
- See also: cavekit-renderers.md (selected per iteration to brief agents and humans)
- See also: cavekit-embeddings.md (optional similarity input for dispatch)
