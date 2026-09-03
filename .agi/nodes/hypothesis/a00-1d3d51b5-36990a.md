---
id: hyp:a00-1d3d51b5-36990a
mint_id: 9294b410bf484b67986806c56ff50c3c
type: hypothesis
parents:
  - idea:domain-autoresearch-tree-skill
confidence: 0.5
tags:
  - zoom-level
  - agent-routing
  - A00
testable_claim: Agents injected with BIG zoom level (whole-graph exploration mode) will spawn ≥3x more new idea or hypothesis nodes per session than agents injected with SMALL zoom level (mid-chain extension mode).
title: "Zoom-level routing: BIG zoom agents spawn 3x more new ideas than SMALL zoom agents"
verdict:
wired_at: 1777664395
wired_from: a00-1d3d51b5
---
# hyp:a00-1d3d51b5-36990a

## Testable Claim

Agents injected with BIG zoom level (whole-graph exploration mode) will spawn ≥3x more new idea or hypothesis nodes per session than agents injected with SMALL zoom level (mid-chain extension mode).

**Rationale:** The zoom level is the primary steering signal in the SessionStart hook. BIG mode tells the agent "explore broadly, introduce fresh ideas." SMALL mode tells the agent "extend existing chains." If this routing signal is working, BIG agents should produce more top-of-chain nodes (idea, hypothesis) while SMALL agents should produce more mid-chain nodes (experiment, verdict, mvp).

## Methodology

1. Run N=5 BIG-zoom agent sessions against the live graph. Count new `idea:*` and `hypothesis:*` nodes spawned.
2. Run N=5 SMALL-zoom agent sessions against the same graph snapshot. Count new `idea:*` and `hypothesis:*` nodes spawned.
3. Compare: BIG_total / SMALL_total ≥ 3.0

**Controls:** Same graph snapshot, same skill set, same task prompt template.

## What Would Prove It

- BIG zoom agents create ≥3x as many new idea/hypothesis nodes as SMALL zoom agents
- BIG agents create a statistically significant number of brand-new `idea:*` nodes (not just spawn from existing ideas)
- SMALL agents produce proportionally more experiment/verdict/mvp nodes

## What Would Disprove It

- No significant difference in node-type distribution between BIG and SMALL agents
- BIG agents also default to mid-chain extension (routing signal ignored)
- SMALL agents spawn new ideas at equal or greater rate (exploration bias dominates)

## Related Work

- `exp-attractiveness-r1.py`: Tests task_attractiveness vs longest-chain baseline for domain diversity
- `idea:domain-autoresearch-tree-skill`: The parent idea containing all skill-routing hypotheses
- Zoom-level injection is defined in the SessionStart hook (`exp-skill-r10-sessionstart-hook.py`)
- autoresearch.ideas.md: structural-bias flags synthetic verdict generation — agents may ignore zoom signals

## Success Criteria

- [ ] BIG zoom agents spawn ≥3x new idea/hypothesis nodes vs SMALL zoom agents
- [ ] BIG agents produce at least 1 new `idea:*` node per session on average
- [ ] Node-type distribution (idea+hypothesis ratio) differs significantly between zoom levels
- [ ] Effect persists across graph snapshots (not artifact of graph state)


Hypothesis: BIG zoom agents spawn 3x more new ideas than SMALL zoom agents. Routing signal gap identified in zoom-level steering.