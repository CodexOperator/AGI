"""agi_algos — Graph algorithms folded from `~/.hermes/agi/` root.

This package houses the core graph algorithm modules that used to live at the
hermes/agi repository root. They are kept distinct from `graph_core` (which is
the harness-side graph framework: nodes, edges, persistence, loaders) because
these modules implement the *algorithms* that operate on built graphs:

- `graph_builder` — builds a hermes-flavoured graph (35 node types) from a
  hermes/agi directory; provides lru-cached warm load.
- `query_engine`  — BFS / Dijkstra / reachable-set / content search over a
  built graph.
- `benchmark`     — perf harness for graph build, query, and serialization.
- `pi_tree_adapter` — type-bridge between hermes node taxonomy and the
  autoresearch-tree node types used by the rest of the harness.
- `asciirender`   — ASCII renderer for the hermes-flavoured 35-type graph
  (separate from `renderers/ascii.py`, which renders the
  autoresearch-tree project graph; both coexist for now per
  cavekit-topology-fold R7; unification deferred to TODO).

Public API exports below mirror the historic root-level imports so existing
callers (hermes scripts, ad-hoc REPL sessions) can still do
`from agi_algos.graph_builder import build_graph` etc.
"""

from .graph_builder import (  # noqa: F401
    build_graph,
    GraphBuilder,
)
from .query_engine import QueryEngine  # noqa: F401
from .pi_tree_adapter import PiTreeAdapter  # noqa: F401
from .asciirender import (  # noqa: F401
    ASCIIRenderer,
    render_to_string,
)

# benchmark.py is a CLI/script-style module (functions: metric, run, type_key);
# import the module itself rather than bind specific names. Callers can do
# `from agi_algos import benchmark` then `benchmark.metric(...)` etc.
from . import benchmark  # noqa: F401

__all__ = [
    "build_graph",
    "GraphBuilder",
    "QueryEngine",
    "PiTreeAdapter",
    "ASCIIRenderer",
    "render_to_string",
    "benchmark",
]
