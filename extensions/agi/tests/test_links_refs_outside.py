"""hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded.

`links.py schema` reports any node whose `link_ref:`/`payload_ref:` resolves
OUTSIDE the repo tree (the source root enclosing `.agi/`). (The write-side refusal
retired with the node writer, goal:g7.16.1.11.46.23 step 4.) The measured case is
`doc:lm-director-brief-customizations`'s dead-session `/tmp` link_ref.

Report-only on the read half (exit 0, `--fix` untouched); refusal writes nothing.
"""
from __future__ import annotations

import io
import contextlib
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import links  # noqa: E402


def _graph(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "doc").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    return graph


def _graph_with_locations(tmp_path: Path, **locs) -> Path:
    """A graph whose config DECLARES named locations, so a `location:` name
    resolves somewhere other than the default source root."""
    import json

    graph = _graph(tmp_path)
    (graph / "config.json").write_text(json.dumps({"locations": locs}))
    return graph


def _node(graph: Path, node_id: str, **fields) -> Path:
    ntype, slug = node_id.split(":", 1)
    lines = [f"id: {node_id}", f"type: {ntype}"]
    for key, val in fields.items():
        lines.append(f"{key}: {val}")
    path = graph / "nodes" / ntype / f"{slug}.md"
    path.write_text("---\n" + "\n".join(lines) + "\n---\n\nbody\n")
    return path


def _schema(graph: Path) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        links._schema_report(graph)
    return buf.getvalue()


def test_an_inside_ref_is_silent(tmp_path):
    graph = _graph(tmp_path)
    (tmp_path / "notes.txt").write_text("x")
    _node(graph, "doc:inside", link_ref="notes.txt")
    out = _schema(graph)
    assert "outside-ref:" not in out
    assert "0 outside-ref(s)" in out


def test_an_outside_ref_is_one_named_line_and_counted(tmp_path):
    graph = _graph(tmp_path)
    _node(graph, "doc:outside", payload_ref="/tmp/dead-session/notes.md")
    out = _schema(graph)
    lines = [ln for ln in out.splitlines() if ln.startswith("outside-ref:")]
    assert lines == [
        "outside-ref: doc:outside payload_ref -> /tmp/dead-session/notes.md"]
    assert "1 outside-ref(s)" in out

