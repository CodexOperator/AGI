#!/usr/bin/env python3
"""
_benchmark.py — Autoresearch benchmark for unified graph memory.
Primary: graph_build_time_ms (cold build, lower is better).

Warm load is at noise floor via lru_cache.
Cold build exercises the full parsing pipeline and is the real optimization surface.
"""

import os
import sys
import time

_AGI_SRC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "extensions", "agi", "src"
)
if _AGI_SRC not in sys.path:
    sys.path.insert(0, _AGI_SRC)

from agi_algos.graph_builder import build_graph, _cached_build_builder
from agi_algos.query_engine import QueryEngine
from agi_algos.asciirender import ASCIIRenderer

HERMES_DIR = os.path.expanduser("~/.hermes")
AGI_DIR = os.path.dirname(os.path.abspath(__file__))


def metric(name, value):
    print(f"METRIC {name}={value}", flush=True)


def main():
    # Populate cache (cold build + cache populate — unmeasured)
    build_graph(HERMES_DIR, AGI_DIR, use_gitnexus=False)
    # Now lru_cache is warm

    # 1. Warm build (cache hit — should be ~0.01ms)
    start = time.perf_counter()
    builder, _ = build_graph(HERMES_DIR, AGI_DIR, use_gitnexus=False)
    warm_ms = (time.perf_counter() - start) * 1000

    # 2. Cold build (clear cache, full parse)
    _cached_build_builder.cache_clear()
    start = time.perf_counter()
    builder_cold, _ = build_graph(HERMES_DIR, AGI_DIR, use_gitnexus=False)
    cold_ms = (time.perf_counter() - start) * 1000

    node_count = len(builder_cold.nodes)
    edge_count = len(builder_cold.edges)

    # 3. Path query (unidirectional BFS on cold-built graph)
    qe = QueryEngine(builder_cold)
    section_ids = [n[0] for n in builder_cold.nodes if n[1] == "doc_section"]
    if len(section_ids) >= 2:
        start_q = time.perf_counter()
        qe.find_path_bfs(section_ids[0], section_ids[-1])
        query_ms = (time.perf_counter() - start_q) * 1000
    else:
        query_ms = 0

    # 4. ASCII render
    ar = ASCIIRenderer(builder_cold)
    ascii_out = ar.render_full()
    ascii_lines = len(ascii_out.strip().split('\n'))

    # Primary: cold build time (the real optimization target)
    metric("graph_build_time_ms", round(cold_ms, 2))
    metric("graph_node_count", node_count)
    metric("graph_edge_count", edge_count)
    metric("query_time_ms", round(query_ms, 3))
    metric("ascii_render_lines", ascii_lines)
    metric("warm_build_time_ms", round(warm_ms, 4))

    print(f"\n cold={cold_ms:.2f}ms  warm={warm_ms:.4f}ms  n={node_count}  e={edge_count}")


if __name__ == "__main__":
    main()