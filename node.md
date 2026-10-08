---
id: mvp:schema-registry-r1
mint_id: 264d718d0a234bdbb71a6239f91e7bce
type: mvp
parents:
  - verdict:schema-registry-r1
next_edges:
  - outcome:schema-registry-r1
edited_by: season.py
season: 1
subgraph: false
tags:
  - schema-registry
  - R1
testable_claim: MVP for schema-registry R1
thought_session: season
title: "schema-registry/R1: MVP"
---
**MVP:** Schema-as-file pattern with bracket convention.

```python
# Drop a schema file:
#   schemas/[nodetype].md   → active (participates in auto-discovery)
#   schemas/nodetype.md     → inactive (loaded but not auto-discovered)

from schema_registry.loader import load_schemas_from_dir
reg = load_schemas_from_dir("schemas/")
schema = reg.get("hypothesis")  # None if not found
```

**Key files:**
- `src/schema_registry/loader.py` — schema file loading
- `src/schema_registry/active_set.py` — bracket convention + active/inactive sets
- `src/schema_registry/cascade.py` — auto-discovery cascade