"""goal:g7.16.1.11.13.2 -- the shared fixture helper for the veto cell.

The gated acts (the closeout merge-up and push, a push to a trunk branch, the
rotation of another post, the authority publish, a config-row edit outside
self_row) read the veto cell STRICT, so a fixture graph root with no
``nodes/.geometry/vetoes.md`` now HOLDS by name. A fixture that is not about
the veto calls ``write_free_veto`` to get a well-formed FREE cell. The tests of
the veto itself (test_veto.py, test_veto_fail_closed.py,
test_write_veto_gate.py) keep their own cells.
"""
from __future__ import annotations

from pathlib import Path

FREE_VETO_CELL = (
    "---\nid: config:vetoes\nmint_id: 5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a\n"
    "type: config\nparents: []\nactive_gates: []\nvetoes: []\n---\n\n"
    "# config:vetoes\n")


def write_free_veto(geometry_dir) -> Path:
    """Write a well-formed FREE ``vetoes.md`` into ``geometry_dir`` (the
    ``<graph root>/nodes/.geometry`` directory), creating the directory when it
    is absent. An existing cell is never overwritten. Returns the cell path."""
    d = Path(geometry_dir)
    d.mkdir(parents=True, exist_ok=True)
    cell = d / "vetoes.md"
    if not cell.exists():
        cell.write_text(FREE_VETO_CELL, encoding="utf-8")
    return cell
