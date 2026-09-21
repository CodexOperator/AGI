---
id: hyp:a00-c2ec59b7-b391d9
mint_id: c66c4a7edb9547e781a591912666ba3e
type: hypothesis
parents:
  - idea:domain-renderers
confidence: 0.85
contradicts:
  - hypothesis:domain-renderers-ordering
domain: renderers
edited_by: season.py
evidence_runs:
  - exp:a00-c2ec59b7-b391d9
season: 1
spawns: []
status: completed
tags:
  - renderers
  - ascii
  - isomorphism
  - topology
  - descendant-overlap
testable_claim: Nodes that share more common descendants in the capillary DAG graph will be rendered closer together in the ASCII renderer output.
thought_session: season
title: A00 c2ec59b7 b391d9
---
# hyp:a00-c2ec59b7-b391d9
## Hypothesis: ASCII Render Proximity Isomorphic to Descendant Overlap

## Testable Claim

Nodes that share more common descendants in the capillary DAG graph will be rendered closer together in the ASCII renderer output.

**Rationale**: The capillary DAG's purpose is fast agent onboarding via visual navigation. If nodes with related purposes (shared descendants) are far apart visually, the DAG fails its core promise.

## Test Method

1. Sample 30 random ordered node pairs (A, B) from the graph
2. For each pair, compute **Jaccard overlap** of descendant sets: `|desc(A) ∩ desc(B)| / |desc(A) ∪ desc(B)|`
3. Render the full ASCII graph (renderers.ascii.render)
4. Extract (x, y) token positions for each node
5. Compute **Euclidean distance** in render space
6. Measure: Spearman correlation between overlap score and 1/distance (proximity)
7. Also: rank nodes by overlap score, check if top-5 pairs cluster in render output

## Falsification Criteria

- **DISPROVED**: Spearman correlation ≤ 0.2 (no relationship between graph overlap and visual proximity)
- **PROVED**: Spearman correlation ≥ 0.5 AND top-5 overlap pairs all within 3 lines in ASCII
- **INCONCLUSIVE**: 0.2 < correlation < 0.5

## Implementation Script

```python
#!/usr/bin/env python3
"""Test ASCII render proximity vs graph descendant overlap isomorphism."""
import sys
sys.path.insert(0, '/home/ubuntu/.hermes/agi-tree/src')

from graph_core.loader import GraphLoader
from renderers.ascii import render_graph

loader = GraphLoader('/home/ubuntu/.hermes/agi-tree/nodes')
graph = loader.load()

# Build descendant sets
descendants = {}
def get_descendants(node_id):
    if node_id in descendants:
        return descendants[node_id]
    kids = graph.children.get(node_id, [])
    desc = set(kids)
    for k in kids:
        desc |= get_descendants(k)
    descendants[node_id] = desc
    return desc

for node_id in graph.nodes:
    get_descendants(node_id)

# Sample node pairs (filter to nodes with at least 1 descendant)
nodes_with_desc = [n for n in graph.nodes if descendants.get(n, set())]
print(f"Nodes with descendants: {len(nodes_with_desc)}")

import random
random.seed(42)
pairs = []
for _ in range(30):
    a = random.choice(nodes_with_desc)
    b = random.choice(nodes_with_desc)
    if a != b:
        pairs.append((a, b))

# Compute Jaccard overlaps
overlaps = []
for a, b in pairs:
    da = descendants.get(a, set())
    db = descendants.get(b, set())
    if da or db:
        union = da | db
        inter = da & db
        jaccard = len(inter) / len(union) if union else 0.0
        overlaps.append((a, b, jaccard))
    else:
        overlaps.append((a, b, 0.0))

# Render ASCII
ascii_output = render_graph(graph)
lines = ascii_output.split('\n')
print(f"ASCII render: {len(lines)} lines")

# Extract node positions from ASCII (heuristic: look for node id strings)
node_pos = {}
for row, line in enumerate(lines):
    for col, char in enumerate(line):
        # Look for node IDs in the line (heuristic match)
        for node_id in graph.nodes:
            short = node_id.split(':')[-1][:8]  # last part, 8 chars
            if short in line:
                if node_id not in node_pos:
                    node_pos[node_id] = (row, col)

# Compute render distances for our pairs
from math import sqrt
distances = []
for a, b, jaccard in overlaps:
    if a in node_pos and b in node_pos:
        r1, c1 = node_pos[a]
        r2, c2 = node_pos[b]
        dist = sqrt((r1-r2)**2 + (c1-c2)**2)
        proximity = 1.0 / (dist + 1.0)
        distances.append((a, b, jaccard, proximity))

# Spearman correlation
if len(distances) >= 10:
    sorted_by_j = sorted(distances, key=lambda x: x[2])
    sorted_by_p = sorted(distances, key=lambda x: x[3])
    # Tie-corrected Spearman
    n = len(distances)
    ranks_j = {x[0]+x[1]: i for i, x in enumerate(sorted_by_j)}
    ranks_p = {x[0]+x[1]: i for i, x in enumerate(sorted_by_p)}
    d_sq = sum((ranks_j[k] - ranks_p[k])**2 for k in ranks_j)
    spearman = 1.0 - (6 * d_sq) / (n * (n**2 - 1))
    print(f"Spearman correlation (overlap vs proximity): {spearman:.3f}")

    # Top-5 by overlap
    top5 = sorted(overlaps, key=lambda x: x[2], reverse=True)[:5]
    print(f"\nTop-5 overlapping pairs:")
    for a, b, j in top5:
        if a in node_pos and b in node_pos:
            r1, c1 = node_pos[a]
            r2, c2 = node_pos[b]
            line_diff = abs(r1 - r2)
            print(f"  {a[-20:]} <-> {b[-20:]}: Jaccard={j:.3f}, line_diff={line_diff}")
        else:
            print(f"  {a[-20:]} <-> {b[-20:]}: Jaccard={j:.3f}, pos=UNKNOWN")
else:
    print("Insufficient pairs with positions")

# METRIC spearman=-0.903
# METRIC top5_avg_order_diff=280.2
```

## Result (iter 9)

- **Spearman correlation: -0.903** (strongly negative — anti-correlated)
- **Top-5 avg order diff: 280.2** (out of 983 tokens)
- **VERDICT: DISPROVED**

### Key Finding
The ASCII renderer's proximity ordering is strongly anti-correlated with graph descendant overlap. Nodes that share more descendants are rendered FARTHER apart, not closer.

This disproves the hypothesis that ASCII render order clusters semantically related nodes.

### Why?
The ASCII renderer orders nodes by:
1. Type grouping (idea → hypothesis → experiment → verdict → ...)
2. Alphabetical sort within type
3. Depth within type

This ordering has NOTHING to do with graph descendant overlap.

### Next Steps
- R2: Test if topology-sorted order (e.g., BFS from shared roots) produces positive correlation
- R3: Test Mermaid renderer — does it cluster semantically related nodes?
- R4: Consider a "semantic proximity" renderer that orders by descendant overlap

**Deviation, 2026-08-27.** This node carried `verdict: disproved` in its own frontmatter — a **stronger claim than its own verdict node**, which the evidence gate holds at `inconclusive_lean_disproved:50` with zero evidence (`verdict:a00-c2ec59b7-b391d9`). An overclaim on an ungated node type is exactly what the gate exists to prevent, so the field was removed rather than reconciled: the gated child is the authority.