"""ASCII renderer (T-061 / renderers R2).

Hierarchical depth-driven layout. Bounded at 200 lines × 200 cols.
On overflow:
- truncate at column 200 with ``... [line cut]`` suffix
- truncate at line 200 with ``... [truncated, N more nodes]`` final line

Determinism: input is a sorted-by-id deterministic Representation, so output is
byte-equal across runs.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .representation import RenderToken, Representation

MAX_LINES = 200
MAX_COLS = 200
LINE_CUT_MARKER = " ... [line cut]"
TRUNC_MARKER_FMT = "... [truncated, {n} more nodes]"


def render_ascii(representation: Representation) -> str:
    """Render a Representation as bounded ASCII text."""
    tokens = list(representation.tokens)
    lines: list[str] = []

    # Header summary (always 3 lines: graph count, types, separator).
    type_counts: dict[str, int] = defaultdict(int)
    for t in tokens:
        type_counts[t.type] += 1
    summary = f"# graph: {len(tokens)} nodes"
    type_line = "# types: " + ", ".join(
        f"{k}={v}" for k, v in sorted(type_counts.items())
    )
    lines.append(_truncate_line(summary))
    lines.append(_truncate_line(type_line))
    lines.append(_truncate_line("#"))

    # Pre-build footer so we know how many lines it occupies.
    footer_lines: list[str] = []
    if tokens:
        edge_counts: dict[str, int] = defaultdict(int)
        for t in tokens:
            for _tgt, rel in t.edges:
                edge_counts[rel] += 1
        footer_lines.append("----")
        footer_lines.append(
            "Types: " + ", ".join(f"{k}={v}" for k, v in sorted(type_counts.items()))
        )
        if edge_counts:
            footer_lines.append(
                "Edges: " + ", ".join(f"{k}={v}" for k, v in sorted(edge_counts.items()))
            )

    # Budget: reserve 1 line for truncation marker + footer lines.
    footer_size = len(footer_lines)
    # body_limit is the max lines index before we must emit truncation marker.
    # We need room for: current lines (header=3) + body + trunc_marker(1) + footer.
    # So max body lines = MAX_LINES - 3 (header) - 1 (trunc marker) - footer_size.
    # But if no truncation needed, no trunc marker line is used.

    rendered_count = 0
    truncated = False
    for t in tokens:
        # Lines so far + 1 (this node) + footer_size must stay <= MAX_LINES.
        # Also need 1 spare for truncation marker if there are still nodes left.
        remaining_after = len(tokens) - rendered_count - 1
        need_trunc_slot = remaining_after > 0
        slots_needed = 1 + (1 if need_trunc_slot else 0) + footer_size
        if len(lines) + slots_needed > MAX_LINES:
            remaining = len(tokens) - rendered_count
            lines.append(_truncate_line(TRUNC_MARKER_FMT.format(n=remaining)))
            truncated = True
            break
        indent = "  " * max(t.depth, 0)
        edge_summary = ""
        if t.edges:
            edge_strs = [f"{rel}->{tgt}" for tgt, rel in t.edges[:3]]
            extra = f" (+{len(t.edges) - 3})" if len(t.edges) > 3 else ""
            edge_summary = " [" + ", ".join(edge_strs) + extra + "]"
        line = f"{indent}{t.label} :: {t.type}{edge_summary}"
        lines.append(_truncate_line(line))
        rendered_count += 1

    # Append footer (after truncation marker if present, or after body).
    for fl in footer_lines:
        lines.append(_truncate_line(fl))

    return "\n".join(lines) + "\n"


def _truncate_line(line: str) -> str:
    if len(line) <= MAX_COLS:
        return line
    cut_at = MAX_COLS - len(LINE_CUT_MARKER)
    if cut_at < 0:
        cut_at = 0
    return line[:cut_at] + LINE_CUT_MARKER
