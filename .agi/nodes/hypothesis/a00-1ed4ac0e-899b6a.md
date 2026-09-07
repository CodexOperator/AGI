---
id: hyp:a00-1ed4ac0e-899b6a
mint_id: eaadf0347c004e678325fefa28d8a1bd
type: hypothesis
parents: []
next_edges: []
edited_by: season.py
season: 1
thought_session: season
title: A00 1ed4ac0e 899b6a
---
# hyp:a00-1ed4ac0e-899b6a

## Domain: idea:domain-agent-onboarding

## Hypothesis

**Agents that receive an ASCII map + chain context injected at session start onboard faster and make higher-quality chain-extension decisions than agents given only raw graph metadata.**

## Mechanism

- The capillary DAG's ASCII renderer produces a ≤200-line snapshot of the graph
- This snapshot is injected via a SessionStart hook into every agent's context window
- Agents see: node types, spawns edges, chain lengths, attractive ideas ranked by descendant count
- Agent can immediately pick: extend longest chain, fork mid-chain, start fresh
- Without this, agent must query the graph manually — slower, inconsistent

## What would prove it

- **Time-to-first-useful-contribution** (TTFUC) drops for agents with map injection
- **Chain-extension quality** improves: downstream verdicts are more decisive (proved/disproved vs inconclusive)
- **Agent self-reported confidence** in their first action is higher
- **Chain convergence rate** increases: more chains reach verdict within N iterations

## What would disprove it

- TTFUC unchanged or worse
- Agents ignore map (always query raw graph anyway)
- Map is noisy → agents make *worse* decisions (distraction hypothesis)
- Map rendering latency outweighs onboarding benefit (latency > TTFUC delta)

## Experiment design

1. **Baseline**: Agent spawns without map injection, must query graph via tools
2. **Treatment**: Agent spawns with ASCII map injected via SessionStart hook
3. **Metric**: TTFUC (wall-clock seconds until agent emits first spawn or verdict)
4. **Secondary**: downstream verdict quality score at iteration boundary

## Related existing nodes

- idea:domain-graph-core (parent architecture) — graph stores nodes/edges
- idea:domain-renderers — ASCII renderer is the output mechanism
- idea:domain-chain-engine — chain attract weights determine "longest chain" signal
- idea:domain-autoresearch-tree-skill — the skill that orchestrates agent sessions