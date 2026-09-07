---
id: mvp:renderers-r1
mint_id: c4c4999ffaa34ae5ab3a29db5a265273
type: mvp
parents:
  - verdict:renderers-r1
next_edges:
  - outcome:renderers-r1
edited_by: season.py
season: 1
subgraph: false
tags:
  - renderers
  - R1
testable_claim: MVP for renderers R1
thought_session: season
title: "renderers/R1: MVP"
---
**MVP:** Shared RenderToken representation.

```python
from renderers.representation import RenderToken, build_representation
from renderers.ascii_renderer import render_ascii

# RenderToken: 7-field contract
tok = RenderToken(id="x", label="X", type="idea", depth=0, x=0.0, y=0.0, edges=[])
# Build from graph
repr = build_representation(graph)
# Any renderer accepts it
output = render_ascii(repr)
```

**Key files:**
- `src/renderers/representation.py` — RenderToken dataclass + build_representation()
- `src/renderers/ascii_renderer.py` — ASCII renderer (primary)
- `src/renderers/mermaid_renderer.py` — Mermaid renderer
- `src/renderers/git_diff_renderer.py` — Git-diff renderer