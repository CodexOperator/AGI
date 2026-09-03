---
id: hyp:a00-8fe3e715-af88f6
mint_id: 9c2450d2b9ca4bc0bf106b0061376dd6
type: hypothesis
parents: []
next_edges: []
title: A00 8fe3e715 af88f6
---
# hyp:a00-8fe3e715-af88f6
## Hypothesis

The double directory walk in `load_directory` via `_reconstruct_next_edges` is the primary bottleneck (adds ~1.8s on 1785 nodes). Extracting `next_edges` from frontmatter during the initial file read (single pass) and storing it on the Node would eliminate the redundant walk and YAML re-parsing, reducing `render-context.py` total time from ~3.1s to ~1.0s.

## Evidence

### Profiling snapshot generation (local agi-tree src/)

| Component | Time (ms) | Notes |
|---|---|---|
| `load_directory(reconstruct_next_edges=True)` | 2903 | default — double walk |
| `load_directory(reconstruct_next_edges=False)` | 1017 | skip _reconstruct_next_edges |
| edge wiring | 7 | |
| build_representation | 8 | |
| render_ascii | 1 | |
| **Total** | **~3019ms** | dominated by double YAML parse |

`_reconstruct_next_edges` re-walks 1785 `.md` files and re-parses YAML frontmatter for each to extract `next_edges` fields. 1625/1785 files have `next_edges` defined (prior verdict nodes). This is ~1.9s of wasted I/O + YAML parsing.

### Key observation

`_node_from_frontmatter` already parses YAML during the first pass but discards `next_edges`. The data IS in the `NodeFile.frontmatter` dict — it just isn't extracted.

### Fix plan

1. Add `next_edges: list[str]` as a 7th field to `Node` dataclass
2. In `_node_from_frontmatter`, extract `fm.get("next_edges", [])` and pass to Node constructor
3. In `load_directory`, after loading all nodes, build `next` edges from `node.next_edges` on each node — no second walk needed
4. Set `reconstruct_next_edges=False` as default

## What would prove it

`render-context.py` total time drops from ~3.1s to ~1.0s (<50% of original).

## What would disprove it

Time savings < 10% — means bottleneck is elsewhere (e.g., YAML parsing itself is unavoidable and ~1s is the floor).

## Implementation

```python
# node.py — add next_edges field
@dataclass
class Node:
    id: str
    type: str
    payload_ref: Optional[str] = None
    parents: set[str] = field(default_factory=set)
    children: set[str] = field(default_factory=set)
    tags: set[str] = field(default_factory=set)
    next_edges: list[str] = field(default_factory=list)  # NEW

# loader.py _node_from_frontmatter — extract next_edges
    next_edges = list(fm.get("next_edges", []) or [])
    return Node(id=nid, type=type_str, ..., next_edges=next_edges)

# loader.py load_directory — build next edges from node.next_edges
    if reconstruct_next_edges:
        for node in g.nodes:
            for target_id in node.next_edges:
                if g.has_node(target_id):
                    try:
                        g.add_edge(Edge(source_id=node.id, target_id=target_id, relation="next"))
                    except Exception:
                        pass
```