---
id: bigger_outcome:renderers-r1
mint_id: 8e1e5288a7364a4f871d9e773a26b1a7
type: bigger_outcome
parents:
  - outcome:renderers-r1
next_edges:
  - vision:renderers
edited_by: season.py
judged_against: goal:g9
season: 1
subgraph: false
tags:
  - renderers
  - R1
thought_session: season
title: "renderers/R1: Bigger Outcome"
---
**Broader outcome:** Uniform render representation enables multiple renderer formats (ASCII, Mermaid, Git-tree, Git-diff) all sharing the same token contract. The same representation feeds into the embeddings module (coordinate isomorphism). Adding a new renderer requires zero changes to the representation code.

**Properties achieved:**
- Shared Internal Representation (R1): RenderToken contract
- ASCII Renderer Primary (R2): bounded 200x200 ASCII output
- Mermaid Renderer (R3): valid Mermaid flowchart TD
- Git-Tree Renderer (R4): git log --graph shape
- Git-Diff Renderer (R5): experiment run diffs
- Recursive Rendering (R6): depth-bounded rendering
- Renderer Plugin Contract (R7): pure function guarantees
- Pure Function Guarantees (R8): no side effects in renderers