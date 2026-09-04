"""ASCII scatter renderer — 2D projection of embeddings via Representation.tokens[].x/.y.

Reads (x, y) coordinates from the shared Representation (populated by the
embeddings layer via ``embeddings.apply_umap_coords``). Each node is placed
at the cell closest to its normalised (x, y) within a bounded grid.

If multiple nodes map to the same cell, the overlap is indicated by a
single digit count (1-9) or '@' for 10+ overlaps. The grid is bounded to
MAX_GRID_W × MAX_GRID_H characters (default 60×30, always ≤200 in each
dimension).

Determinism: input is a sorted-by-id deterministic Representation, so
floating-point normalisation is also deterministic → output is byte-equal
across runs.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Optional

from .representation import Representation

# Bounds — same max as the ASCII renderer's 200×200, but with different
# defaults since a scatter grid is character-per-cell rather than per-line.
MAX_GRID_W = 200
MAX_GRID_H = 200
DEFAULT_GRID_W = 60
DEFAULT_GRID_H = 30
OVERLAP_10PLUS = "@"


def render_scatter(
    representation: Representation,
    grid_width: Optional[int] = None,
    grid_height: Optional[int] = None,
) -> str:
    """Render a 2D scatter projection of the Representation.

    Parameters
    ----------
    representation:
        A Representation whose tokens have ``.x`` and ``.y`` populated
        (by default 0.0; the embeddings layer overwrites them).
    grid_width, grid_height:
        Dimensions of the output character grid. Defaults to 60×30.
        Always clamped to MAX_GRID_W × MAX_GRID_H (200×200).

    Returns
    -------
    A string: a grid of characters with a footer showing the grid bounds
    and an overlap-count legend.
    """
    tokens = list(representation.tokens)
    if not tokens:
        return "(empty scatter — no tokens)\n"

    # ---- clamp grid dimensions ----
    w = min(grid_width or DEFAULT_GRID_W, MAX_GRID_W)
    h = min(grid_height or DEFAULT_GRID_H, MAX_GRID_H)

    # ---- collect coords, handle all-zero degenerate case ----
    xs = [t.x for t in tokens]
    ys = [t.y for t in tokens]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_range = x_max - x_min
    y_range = y_max - y_min
    if x_range == 0.0:
        x_range = 1.0
    if y_range == 0.0:
        y_range = 1.0

    # ---- assign each token to a grid cell ----
    cell_tokens: dict[tuple[int, int], list[str]] = defaultdict(list)
    for t in tokens:
        col = int((t.x - x_min) / x_range * (w - 1))
        row = int((t.y - y_min) / y_range * (h - 1))
        # Clamp to valid range due to floating-point edge cases
        col = max(0, min(col, w - 1))
        row = max(0, min(row, h - 1))
        cell_tokens[(row, col)].append(t.id)

    # ---- build grid rows ----
    overlap_total = 0
    max_overlap = 0
    grid: list[list[str]] = [[" " for _c in range(w)] for _r in range(h)]
    for (row, col), ids in cell_tokens.items():
        n = len(ids)
        if n == 1:
            # Use first character of the single node's id (deterministic)
            ch = ids[0][0] if ids[0] else "."
        elif n < 10:
            ch = str(n)  # digit 2-9
        else:
            ch = OVERLAP_10PLUS
        grid[row][col] = ch
        if n > 1:
            overlap_total += n - 1
            max_overlap = max(max_overlap, n)

    # ---- render grid as string ----
    lines: list[str] = []
    # Top border
    lines.append("┌" + "─" * w + "┐")
    for row in grid:
        lines.append("│" + "".join(row) + "│")
    # Bottom border
    lines.append("└" + "─" * w + "┘")

    # Footer
    lines.append("")
    lines.append(f"Nodes: {len(tokens)}  Grid: {w}×{h}")
    lines.append(
        f"Overlap cells: {len([v for v in cell_tokens.values() if len(v) > 1])}"
    )
    if overlap_total > 0:
        lines.append(
            f"Overlap total: {overlap_total} (max {max_overlap} at one cell)"
        )

    return "\n".join(lines) + "\n"