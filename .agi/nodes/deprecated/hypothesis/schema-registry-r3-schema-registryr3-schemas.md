---
id: hyp:schema-registry-r3
mint_id: 515c3ad16ae94d5aae60aa4b62151e4a
type: hypothesis
parents:
  - idea:domain-schema-registry
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - schema-registry
  - R3
testable_claim: Schemas as Meta-Nodes
thought_session: L1.09
title: "schema-registry/R3: Schemas as Meta-Nodes"
---
**Description:** Every registered schema appears in the graph as a node of type `meta_node` so the graph can describe its own structure.

**Acceptance Criteria:**
- [ ] After load, the graph contains one `meta_node` per registered schema and its id is derived from the schema's name
- [ ] A meta-node's frontmatter exposes the schema's declared fields, defaults, and validation rules
- [ ] Edges from `meta_node` instances to ordinary nodes record which schema validated which node
- [ ] Removing a schema removes its meta-node and the validating edges on next load

**Dependencies:** graph-core (R1 nodes, R2 edges)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r3-by-citation` citing `build:src-schema-registry-meta-nodes`, `build:tests-schema-registry-test-meta-nodes`: `meta_nodes.py` (`schema_to_meta_node`, `synthesize_meta_nodes`, `diff_meta_nodes`) is the schema-as-node surface.
<!-- THOUGHT:END -->
