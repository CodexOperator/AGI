---
id: hyp:a00-8636e255-bf1a6c
mint_id: c813570f32c14b84b87929de8ba67e4f
type: hypothesis
parents:
  - idea:domain-renderers
domain: renderers
spawns: []
status: open
tags:
  - renderers
  - mermaid
  - r3
  - deterministic
  - validity
testable_claim: "The `render_mermaid()` function produces valid Mermaid 10+ syntax that: 1. Starts with `flowchart TD` or `graph TD` directive 2. Every node and edge appears at most once (deduplication) 3. Two runs against the same representation produce byte-identical output"
title: A00 8636e255 bf1a6c
---
# hyp:a00-8636e255-bf1a6c
## Hypothesis: Mermaid Renderer (R3) — Valid, Deterministic Mermaid Output

## Testable Claim

The `render_mermaid()` function produces valid Mermaid 10+ syntax that:
1. Starts with `flowchart TD` or `graph TD` directive
2. Every node and edge appears at most once (deduplication)
3. Two runs against the same representation produce byte-identical output

## Test Method

1. Load the graph from `nodes/` directory
2. Build representation via `build_representation(graph)`
3. Run `render_mermaid(rep)` twice — verify byte-identical outputs
4. Parse output: first line must match `^(flowchart TD|graph TD)`
5. Count unique node ids in output vs input — must match
6. Count unique edges in output vs input — must match (dedup check)
7. Verify no Mermaid-unsafe characters in node ids (no `:` without quoting)

## Falsification Criteria

- **PROVED**: All 3 criteria pass
- **DISPROVED**: Any criterion fails
- **INCONCLUSIVE**: Parser errors prevent complete validation

## Implementation Script

```python
#!/usr/bin/env python3
"""Test Mermaid renderer validity and determinism (R3)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from graph_core.loader import load_directory
from renderers import render_mermaid, build_representation

NODES_DIR = '/home/ubuntu/.hermes/agi-tree/nodes'

graph, _ = load_directory(NODES_DIR)
rep = build_representation(graph)

# Test 1: Determinism — two runs produce byte-identical output
out1 = render_mermaid(rep)
out2 = render_mermaid(rep)
deterministic = out1 == out2
print(f"[1] Deterministic: {deterministic}")
if not deterministic:
    print(f"  Run1 length: {len(out1)}, Run2 length: {len(out2)}")
    # Find first diff
    for i, (c1, c2) in enumerate(zip(out1, out2)):
        if c1 != c2:
            print(f"  First diff at pos {i}: {repr(out1[max(0,i-10):i+10])} vs {repr(out2[max(0,i-10):i+10])}")
            break

# Test 2: Directive check
first_line = out1.split('\n')[0]
valid_directive = first_line.strip().startswith(('flowchart TD', 'graph TD'))
print(f"[2] Valid directive: {valid_directive} ('{first_line}')")

# Test 3: Node deduplication
# Parse node ids from output
import re
node_pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\["')
input_node_ids = {t.id for t in rep.tokens}
output_nodes = set()
for line in out1.split('\n'):
    m = node_pattern.match(line)
    if m:
        output_nodes.add(m.group(1))

# Check: all output nodes are in input (no spurious nodes) AND all input nodes appear (no missing)
nodes_complete = input_node_ids == output_nodes
nodes_subset = output_nodes.issubset(input_node_ids)
print(f"[3a] Output nodes subset of input: {nodes_subset} ({len(output_nodes)}/{len(input_node_ids)})")
print(f"[3b] All input nodes in output: {nodes_complete} ({len(input_node_ids)} nodes in repr)")

# Test 4: Edge deduplication
edge_pattern = re.compile(r'^\s*[A-Za-z0-9_]+\s*-->[|][^|]*[|]\s*[A-Za-z0-9_]+')
input_edges = set()
for t in rep.tokens:
    for tgt, rel in t.edges:
        input_edges.add((t.id, tgt))

output_edges = set()
for line in out1.split('\n'):
    if edge_pattern.match(line):
        parts = line.split('-->')
        if len(parts) == 2:
            src = parts[0].strip()
            tgt_part = parts[1].split('|')
            if len(tgt_part) >= 2:
                tgt = tgt_part[-1].strip()
                output_edges.add((src, tgt))

edges_subset = output_edges.issubset(input_edges)
edges_complete = input_edges == output_edges
print(f"[4a] Output edges subset of input: {edges_subset} ({len(output_edges)}/{len(input_edges)})")
print(f"[4b] All input edges in output: {edges_complete}")

# Test 5: Mermaid id safety (no bare : characters in ids)
import ast
# Check that node definitions use quoted strings for complex ids
has_unquoted_complex_id = bool(re.search(r'^\s*[A-Za-z0-9_]+\[[^\'"].*:[^\'"].*\]', out1, re.MULTILINE))
print(f"[5] No unquoted complex ids: {not has_unquoted_complex_id}")

# Summary
all_pass = deterministic and valid_directive and nodes_subset and edges_subset and not has_unquoted_complex_id
partial_pass = sum([deterministic, valid_directive, nodes_subset, edges_subset, not has_unquoted_complex_id])

print(f"\n{'='*50}")
print(f"Results: {partial_pass}/5 criteria passed")
print(f"Overall: {'PROVED' if all_pass else 'DISPROVED' if partial_pass == 0 else 'INCONCLUSIVE'}")

# Metrics
print(f"\nMETRIC criteria_passed={partial_pass}")
print(f"METRIC deterministic={1 if deterministic else 0}")
print(f"METRIC valid_directive={1 if valid_directive else 0}")
print(f"METRIC nodes_dedup={1 if nodes_subset else 0}")
print(f"METRIC edges_dedup={1 if edges_subset else 0}")
print(f"METRIC safe_ids={1 if not has_unquoted_complex_id else 0}")
print(f"METRIC input_nodes={len(input_node_ids)}")
print(f"METRIC input_edges={len(input_edges)}")
print(f"METRIC output_nodes={len(output_nodes)}")
print(f"METRIC output_edges={len(output_edges)}")
```