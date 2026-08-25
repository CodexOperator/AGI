---
confidence: 0.5
id: "hyp:renderers-r8"
mint_id: 959082b110414a08833982915c662094
origin: build-site
parents:
  - idea:domain-renderers
subgraph: false
tags:
  - renderers
  - R8
testable_claim: Pure Function Guarantee
title: "renderers/R8: Pure Function Guarantee"
type: hypothesis
---

**Description:** Every renderer is a pure function over the representation: it never mutates input, never reads external state, and never writes outside the returned string.

**Acceptance Criteria:**
- [ ] A renderer invoked twice with the same representation produces equal outputs
- [ ] A renderer's input representation is unchanged after the call
- [ ] No renderer reads environment variables, files, or network resources during render
- [ ] No renderer writes any file or process state during render

## Out of Scope

- Generating the embedding vectors that drive coordinates in the shared representation — see embeddings (note: coordinates produced there flow into this kit's representation)
- Building the graph from sources — see graph-core and environment-indexers
- Choosing which renderer to invoke at which moment of the autoresearch loop — see autoresearch-tree-skill
- Interactive or animated renderers — only static text outputs are required by this kit

## Cross-References

- See also: cavekit-graph-core.md (R1 nodes, R2 edges, R5 recursive bodies)
- See also: cavekit-embeddings.md (provides the coordinate values consumed in R1 tokens)
- See also: cavekit-chain-engine.md (chain shapes consumed by R4 and R5)
- See also: cavekit-autoresearch-tree-skill.md (selects renderers per iteration)
