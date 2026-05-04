"""Shared render-token representation (T-060 / renderers R1).

This is the SINGLE source of truth feeding ALL renderers (ASCII, Mermaid,
git-tree, git-diff) AND the embeddings layer. The (x, y) coords default to
zero and are overridden by the embeddings layer (Node2Vec → UMAP).

Acceptance criteria (R1):
- R1.1: RenderToken exposes id, label, type, depth, x, y, edges (7 fields)
- R1.2: Build is deterministic — identical graphs → identical token sequences
- R1.3: Representation accepted by every renderer without conversion shims
- R1.4: Documented contract for external consumers (embeddings)

Contract for consumers:
    Each `RenderToken` is uniquely identified by `id`. `label` is a short
    human-readable string (≤40 chars target). `type` is the schema type.
    `depth` is BFS distance from a root, computed deterministically by
    sorting node ids before traversal. `x, y` default to 0.0 and may be
    overwritten by `embeddings.apply_umap_coords(repr, coords)`.
    `edges` is a list of `(target_id, relation)` tuples.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional

from graph_core.graph import Graph
from graph_core.node import Node


@dataclass
class RenderToken:
    """One token in the shared representation."""

    id: str
    label: str
    type: str
    depth: int
    x: float
    y: float
    edges: list[tuple[str, str]]  # (target_id, relation)


@dataclass
class Representation:
    """Ordered, deterministic token sequence (R1.2)."""

    tokens: list[RenderToken] = field(default_factory=list)

    def by_id(self) -> dict[str, RenderToken]:
        return {t.id: t for t in self.tokens}

    def __iter__(self) -> Iterator[RenderToken]:
        return iter(self.tokens)

    def __len__(self) -> int:
        return len(self.tokens)


def build_representation(graph: Graph, label_fn: Optional[callable] = None) -> Representation:
    """Build a deterministic Representation from a Graph (R1.2 + R1.3).

    `label_fn(node)` produces the short label. Default uses the node id.
    Depth = BFS distance from any root (no parents). Disconnected nodes get
    depth = 0 if they're roots themselves, otherwise -1.
    """
    if label_fn is None:
        label_fn = lambda n: n.id  # noqa: E731

    # 1. Build adjacency and in-degree from the graph's edges (deterministic).
    out_adj: dict[str, list[tuple[str, str]]] = {nid: [] for nid in sorted(graph.node_ids)}
    in_count: dict[str, int] = {nid: 0 for nid in graph.node_ids}
    for e in sorted(graph.edges, key=lambda x: x.triple):
        out_adj.setdefault(e.source_id, []).append((e.target_id, e.relation))
        in_count[e.target_id] = in_count.get(e.target_id, 0) + 1

    # 2. BFS depth from roots (in_degree == 0). Sort root ids for determinism.
    roots = sorted([nid for nid, c in in_count.items() if c == 0])
    depth: dict[str, int] = {nid: -1 for nid in graph.node_ids}
    q = deque()
    for r in roots:
        depth[r] = 0
        q.append(r)
    while q:
        cur = q.popleft()
        for tgt, _rel in sorted(out_adj.get(cur, [])):
            if depth[tgt] == -1:
                depth[tgt] = depth[cur] + 1
                q.append(tgt)

    # 3. Emit tokens in sorted-id order (R1.2 determinism).
    tokens: list[RenderToken] = []
    for nid in sorted(graph.node_ids):
        n = graph.get_node(nid)
        assert n is not None
        tokens.append(
            RenderToken(
                id=nid,
                label=str(label_fn(n))[:40],  # ≤40 char target
                type=n.type,
                depth=depth.get(nid, 0),
                x=0.0,
                y=0.0,
                edges=sorted(out_adj.get(nid, [])),
            )
        )
    return Representation(tokens=tokens)
