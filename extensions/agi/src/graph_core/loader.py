"""Directory-walking loader and recursive subgraph support (T-009 + T-011).

T-009 (R5): when a node's frontmatter contains ``subgraph: true``, the body is
treated as nested graph content and the inner graph is exposed via
``loaded_node.subgraph``.

T-011 (R6): walk a directory deterministically (sorted) collecting node files
into a Graph using minted ids.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

from .edge import Edge
from .errors import GraphCoreError
from .graph import Graph
from .identity import IdRegistry, mint_id
from .node import Node
from .persistence import load_node_file
from .persistence.frontmatter import NodeFile

NODE_BODY_DELIM = "---"


class DuplicateIdError(GraphCoreError):
    """Raised by :func:`load_directory` in strict mode (G7.2).

    Two or more files declaring the same ``id`` is content loss, not a
    cosmetic clash: ``load_directory`` keeps the first (sorted-walk order)
    and every later file is silently absent from the graph for every tool
    that reads it. Non-strict callers get a warning per collision and
    keep running with the existing first-wins behaviour; strict callers get
    this exception after the full pass so they can see every collision at
    once, not just the first.
    """

    def __init__(self, duplicates: list[tuple[str, Path, Path]]) -> None:
        self.duplicates = duplicates
        detail = "; ".join(
            f"'{nid}' kept={kept} hidden={hidden}" for nid, kept, hidden in duplicates
        )
        super().__init__(f"{len(duplicates)} duplicate node id(s) found: {detail}")


@dataclass
class LoadedNode:
    """Container for a loaded node + its optional subgraph (T-009 / R5)."""

    node: Node
    body: str
    subgraph: Optional["Graph"] = None
    nested_loaded: list["LoadedNode"] = field(default_factory=list)


def load_node_with_subgraph(
    path: str | Path,
    registry: Optional[IdRegistry] = None,
) -> LoadedNode:
    """Load a node file. If frontmatter has ``subgraph: true``, recursively parse the body."""
    p = Path(path)
    nf = load_node_file(p)
    node = _node_from_frontmatter(nf, source_path=p, registry=registry)
    body = nf.body
    if not nf.frontmatter.get("subgraph", False):
        return LoadedNode(node=node, body=body, subgraph=None, nested_loaded=[])
    inner_graph, nested = _parse_subgraph_body(body, parent_id=node.id, registry=registry)
    return LoadedNode(node=node, body=body, subgraph=inner_graph, nested_loaded=nested)


def _node_from_frontmatter(
    nf: NodeFile,
    source_path: Path,
    registry: Optional[IdRegistry],
) -> Node:
    fm = nf.frontmatter
    nid = fm.get("id")
    if not isinstance(nid, str) or not nid:
        nid = mint_id(
            type_prefix=str(fm.get("type", "node")),
            source_text=str(fm.get("title") or source_path.stem),
            registry=registry,
        )
    type_str = str(fm.get("type", "node"))
    parents = set(fm.get("parents", []) or [])
    children = set(fm.get("children", []) or [])
    tags = set(fm.get("tags", []) or [])
    payload_ref = fm.get("payload_ref")
    origin = fm.get("origin")
    if not isinstance(origin, str):
        origin = None
    return Node(
        id=nid,
        type=type_str,
        payload_ref=payload_ref if isinstance(payload_ref, str) else None,
        parents=parents,
        children=children,
        tags=tags,
        origin=origin,
    )


_SUBGRAPH_LINE_RE = re.compile(
    r"^\s*-\s+(?P<src>[^\s>]+)(?:\s*->\s*(?P<dst>[^\s]+))?(?:\s*\[(?P<rel>[^\]]+)\])?\s*$"
)


def _parse_subgraph_body(
    body: str,
    parent_id: str,
    registry: Optional[IdRegistry],
) -> tuple[Graph, list[LoadedNode]]:
    """Parse a body containing subgraph node lines.

    Recognized line shapes (simple form):
        - id:label
        - id:label -> id2:label2
        - id:label -> id2:label2 [relation]

    Lines that don't match are ignored. Same loader recursion: any LoadedNode
    parsed here can itself have subgraph: true via the ``nested_loaded`` list,
    but for body lines we only build graph nodes/edges (not nested files).
    """
    g = Graph()
    nested: list[LoadedNode] = []
    for raw in body.splitlines():
        m = _SUBGRAPH_LINE_RE.match(raw)
        if not m:
            continue
        src = m.group("src").strip()
        dst = m.group("dst")
        rel = m.group("rel") or "next"
        if not g.has_node(src):
            g.add_node(Node(id=src, type=_split_type(src)))
        if dst:
            dst = dst.strip()
            if not g.has_node(dst):
                g.add_node(Node(id=dst, type=_split_type(dst)))
            try:
                g.add_edge(Edge(source_id=src, target_id=dst, relation=rel.strip()))
            except Exception:
                # Cycles in inner subgraph: skip the offending edge silently.
                pass
    return g, nested


def _split_type(node_id: str) -> str:
    if ":" in node_id:
        return node_id.split(":", 1)[0]
    return "node"


# --- T-011: Directory walk ---


def walk_node_files(directory: str | Path) -> list[Path]:
    """Deterministic walk; returns sorted absolute paths to every .md/.json under ``directory``."""
    base = Path(directory)
    out: list[Path] = []
    for root, dirs, files in os.walk(base):
        # Mutate dirs in place to enforce sort order on subsequent recursion.
        dirs.sort()
        for fname in sorted(files):
            p = Path(root) / fname
            if p.suffix.lower() in {".md", ".json"}:
                out.append(p.resolve())
    return out


def load_directory(
    directory: str | Path,
    registry: Optional[IdRegistry] = None,
    strict: bool = False,
) -> tuple[Graph, list[LoadedNode]]:
    """Load every .md/.json node file under ``directory`` into a Graph (T-011 / R6).

    Recursive subgraphs are loaded as well (T-009 / R5) — each LoadedNode carries
    its inner Graph if frontmatter said so.

    Id uniqueness (G7.2): when two files declare the same ``id``, the first one
    encountered in sorted-walk order is kept (unchanged behaviour); every later
    file is dropped from the returned graph. That drop used to be silent. It no
    longer is: this reuses the single pass this function already makes over the
    corpus (no second directory walk) to record every collision as it is found.

    - Default (``strict=False``): each collision prints one line to stderr —
      ``WARN: duplicate node id '<id>': kept <path>, hidden <path>`` — and
      loading proceeds exactly as before. The loop never breaks on this.
    - ``strict=True``: the same warnings are printed, then :class:`DuplicateIdError`
      is raised once the full pass completes (so a caller sees every collision,
      not just the first one hit).

    Either way, the full list of collisions is also exposed as
    ``graph.duplicate_ids`` — ``list[tuple[id, kept_path, hidden_path]]`` — on
    the returned ``Graph`` instance, without changing this function's 2-tuple
    return shape (callers unpack ``g, loaded = load_directory(...)`` all over
    the codebase; that contract is unchanged).
    """
    g = Graph()
    loaded: list[LoadedNode] = []
    duplicates: list[tuple[str, Path, Path]] = []
    kept_paths: dict[str, Path] = {}
    if registry is None:
        registry = IdRegistry()
    for p in walk_node_files(directory):
        try:
            ln = load_node_with_subgraph(p, registry=registry)
        except Exception:
            continue
        nid = ln.node.id
        if not g.has_node(nid):
            g.add_node(ln.node)
            loaded.append(ln)
            kept_paths[nid] = p
        else:
            kept_path = kept_paths.get(nid)
            duplicates.append((nid, kept_path, p))
            print(
                f"WARN: duplicate node id '{nid}': kept {kept_path}, hidden {p}",
                file=sys.stderr,
            )
    g.duplicate_ids = duplicates
    if strict and duplicates:
        raise DuplicateIdError(duplicates)
    return g, loaded
