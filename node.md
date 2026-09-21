---
id: hyp:a00-72d9d3ef-3fdc1e
mint_id: 6a645007dfbf4a048e8c0fcb21e0dfd9
type: hypothesis
parents: []
next_edges:
  - verdict:hypothesis_a00-72d9d3ef-3fdc1e
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
season: 1
status: inconclusive_lean_proved:50
thought_session: season
title: A00 72d9d3ef 3fdc1e
verdict: inconclusive_lean_proved:50
---
# hyp:a00-72d9d3ef-3fdc1e

## Hypothesis

**Claim**: A `task_attractiveness()` scoring function — combining chain depth, domain balance, and task type diversity — produces measurably better agent task selections than the current longest-chain-first heuristic, within a fixed agent-time budget.

**Current gap**: 60 hypotheses, 90 pending tasks, 0 experiments running. Agents default to longest-chain selection, which creates 9 chains at 200 hops but leaves 3 domains (exporters, session-management, test-coverage) with <12 hops. No scoring function exists to balance exploration vs exploitation.

**Testable claim**: A composite attractiveness score `A(t) = α·depth(t) + β·domain_balance(t) + γ·type_diversity(t)` where coefficients are tuned on the live graph, yields higher outcome count than always-extending-longest after N parallel agent-iterations.

**Prove it**: Implement `task_attractiveness()` in `src/chain_engine/attractiveness.py`, run 10 parallel agent-simulations (each taking 5 task selections) using attractiveness-ranked task selection vs longest-chain baseline. Count outcome nodes produced per strategy.

**Disprove it**: Attractiveness-ranked selection produces ≤ the same number of outcome nodes as longest-chain baseline over 5 iterations × 10 parallel agents.

## Implementation Script

```python
#!/usr/bin/env python3
"""Test task_attractiveness vs longest-chain baseline."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains
from chain_engine.attractiveness import task_attractiveness

NODES_DIR = '/home/ubuntu/.hermes/agi-tree/nodes'
ITERATIONS = 5
PARALLEL_AGENTS = 10

graph, _ = load_directory(NODES_DIR)

def longest_chain_heuristic(graph):
    """Return task nodes sorted by chain depth (longest first)."""
    chains = find_chains(graph)
    chain_map = {}
    for chain in chains:
        for node in chain:
            chain_map[node.id] = len(chain)
    tasks = [n for n in graph.nodes if n.type == 'task' and n.status in ('pending', 'open')]
    tasks.sort(key=lambda t: chain_map.get(t.id, 0), reverse=True)
    return tasks

def attractiveness_heuristic(graph):
    """Return task nodes sorted by attractiveness score."""
    tasks = [n for n in graph.nodes if n.type == 'task' and n.status in ('pending', 'open')]
    tasks.sort(key=lambda t: task_attractiveness(t, graph), reverse=True)
    return tasks

def simulate(heuristic_fn, graph, iterations, agents):
    """Simulate N agents selecting M tasks each via heuristic."""
    selected = []
    for _ in range(agents):
        tasks = heuristic_fn(graph)
        # Top-K unique tasks per agent
        selected.extend([t.id for t in tasks[:iterations]])
    return len(set(selected))  # unique tasks selected

baseline_unique = simulate(longest_chain_heuristic, graph, ITERATIONS, PARALLEL_AGENTS)
attractiveness_unique = simulate(attractiveness_heuristic, graph, ITERATIONS, PARALLEL_AGENTS)

print(f"Longest-chain unique tasks: {baseline_unique}")
print(f"Attractiveness unique tasks: {attractiveness_unique}")
print(f"Attractiveness improvement: {attractiveness_unique - baseline_unique:+d}")

METRIC baseline_unique={baseline_unique}
METRIC attractiveness_unique={attractiveness_unique}
METRIC improvement={attractiveness_unique - baseline_unique}

# Prove if attractiveness strictly beats baseline
PROVED = attractiveness_unique > baseline_unique
DISPROVED = attractiveness_unique <= baseline_unique
print(f"\n{'PROVED' if PROVED else 'DISPROVED'}")
```

## Tags

- task-selection
- attractiveness
- chain-engine
- exploration-vs-exploitation
- heuristic

## Notes

- Parent: none (fresh idea at BIG zoom level)
- Zoom: BIG (whole-graph exploration)
- Domain: chain-engine (task selection policy)
- Relates to: idea:domain-chain-engine, hyp:a00-213340cc-61bbbb (cross-domain synthesis)
- Why this matters: 10 parallel agents with random or longest-chain selection will duplicate work and leave domain gaps. A calibrated attractiveness function is the missing "agent brain interface" layer.