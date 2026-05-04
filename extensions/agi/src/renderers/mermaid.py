"""Mermaid renderer (T-063 / renderers R3).

Outputs ``flowchart TD\n`` followed by node and edge declarations. Deduplicates
nodes by id and edges by (source, target, relation). Output is byte-equal across
runs over identical input.

Mermaid 10+ syntax. Node ids are sanitized: Mermaid identifiers can be tokens or
quoted strings. We sanitize ``:`` (used in our id scheme) by replacing it with
underscore for the ``mermaid_id``, then quoting the human label.
"""

from __future__ import annotations

import re

from .representation import Representation


_MERMAID_ID_RE = re.compile(r"[^A-Za-z0-9_]")


def _mermaid_id(node_id: str) -> str:
    """Mermaid-safe identifier (R3.2)."""
    return _MERMAID_ID_RE.sub("_", node_id) or "_"


def _escape_label(label: str) -> str:
    return label.replace('"', "'").replace("\n", " ")


def render_mermaid(representation: Representation) -> str:
    """Render representation as Mermaid flowchart TD."""
    seen_nodes: set[str] = set()
    seen_edges: set[tuple[str, str, str]] = set()

    out: list[str] = ["flowchart TD"]

    for t in representation.tokens:
        if t.id in seen_nodes:
            continue
        seen_nodes.add(t.id)
        mid = _mermaid_id(t.id)
        label = _escape_label(t.label)
        out.append(f'    {mid}["{label}"]:::type_{_escape_class(t.type)}')

    for t in representation.tokens:
        for tgt, relation in t.edges:
            triple = (t.id, tgt, relation)
            if triple in seen_edges:
                continue
            seen_edges.add(triple)
            src_mid = _mermaid_id(t.id)
            tgt_mid = _mermaid_id(tgt)
            rel = _escape_label(relation)
            out.append(f'    {src_mid} -->|{rel}| {tgt_mid}')

    # Class defs for visual differentiation by type (optional for parsing, helps tooling).
    type_set = sorted({t.type for t in representation.tokens})
    for ty in type_set:
        out.append(f"    classDef type_{_escape_class(ty)} fill:#eef,stroke:#446")

    return "\n".join(out) + "\n"


def _escape_class(s: str) -> str:
    return _MERMAID_ID_RE.sub("_", s) or "_"
