---
id: hyp:chain-engine-r9
mint_id: f8344ddba1684850b27284131bb505ac
type: hypothesis
parents:
  - idea:domain-chain-engine
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - chain-engine
  - R9
testable_claim: Chain Query API
thought_session: L1.09
title: "chain-engine/R9: Chain Query API"
---
**Description:** A documented set of queries over chains is available without requiring callers to traverse the graph by hand.

**Acceptance Criteria:**
- [ ] A `longest_n` query returns the top-N chains ranked by attractiveness with score and length
- [ ] A `branching_factor` query returns the average and per-node count of out-edges across chain participants
- [ ] A `mid_chain_candidates` query accepts a minimum chain length and a maximum recency and returns join targets matching both
- [ ] All chain queries are read-only and never mutate the graph

## Out of Scope

- Storage of nodes and edges — see graph-core
- Schema validation of frontmatter for autoresearch types — see schema-registry
- Visual rendering of chains — see renderers
- Vector embedding of chain participants — see embeddings
- Agent dispatch and per-iteration choice between extending, forking, hopping, or starting fresh — see autoresearch-tree-skill

## Cross-References

- See also: cavekit-graph-core.md (DAG substrate)
- See also: cavekit-schema-registry.md (R8 built-in autoresearch schemas)
- See also: cavekit-renderers.md (renders chains as multi-format views)
- See also: cavekit-embeddings.md (embeds nodes including chain participants)
- See also: cavekit-autoresearch-tree-skill.md (consumes chain queries to drive iterations)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r9-by-citation` citing `build:src-chain-engine-queries`: `queries.py` has `longest_n`, `branching_factor` and `mid_chain_candidates` by name, plus `all_chain_queries_pure`.
<!-- THOUGHT:END -->
