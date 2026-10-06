"""goal:g5.4.1.4.6.1 — committed behavioral+help coverage for boxes.py.

Covers the named owe for gate-u U1: `__main__` help smoke, `this_box` /
`default_box`, `row_is_local`, and `box_cells` / `graph_root` (plus
`require_box_cells` happy + error paths). Temp graphs only — never live MAIN.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import boxes  # noqa: E402

BOXES_PY = BIN / "boxes.py"

# Minimal [box].md declaring the four cell names (same shape as the live schema).
_BOX_SCHEMA = """\
---
name: box
structural: true
fields:
  root: {type: str}
  logs_dir: {type: str}
  tmux_session: {type: str}
  user: {type: str}
placeholders:
  root: root
  logs: logs_dir
  tmux: tmux_session
  user: user
---

# box

fixture schema for test_boxes.py
"""


def _graph(
    tmp_path: Path,
    *,
    env_box: str | None = "local-town",
    default_box: str | None = "core-town",
    box_cells: dict | None = None,
    with_schema: bool = True,
    schema_fields: bool = True,
) -> Path:
    """Temp `.agi` graph: config.json + posts.md + optional [box].md + .env."""
    agi = tmp_path / ".agi"
    (agi / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (agi / "context" / "schemas").mkdir(parents=True, exist_ok=True)

    cells = box_cells if box_cells is not None else {
        "root": "/tmp/fixture-root",
        "logs_dir": "/tmp/fixture-logs",
        "tmux_session": "agi-fixture",
        "user": "fixture",
    }
    (agi / "config.json").write_text(
        json.dumps({"box": cells}), encoding="utf-8")

    if with_schema:
        if schema_fields:
            (agi / "context" / "schemas" / "[box].md").write_text(
                _BOX_SCHEMA, encoding="utf-8")
        else:
            (agi / "context" / "schemas" / "[box].md").write_text(
                "---\nname: box\n---\n\n# box\n\nno fields\n",
                encoding="utf-8")

    head = (
        "---\nid: config:posts\n"
        "mint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nparents:\n  - goal:g17\n"
    )
    if default_box is not None:
        head += f"default_box: {default_box}\n"
    (agi / "nodes" / ".geometry" / "posts.md").write_text(
        head + "posts: []\n---\n\n# config:posts\n\nfixture\n",
        encoding="utf-8")

    if env_box is not None:
        (tmp_path / ".env").write_text(f"AGI_BOX={env_box}\n", encoding="utf-8")
    return agi


@pytest.fixture(autouse=True)
def _no_inherited_box(monkeypatch):
    monkeypatch.delenv("AGI_BOX", raising=False)


# --------------------------------------------------------------------------
# __main__ / CLI help smoke
# --------------------------------------------------------------------------

def test_boxes_cli_help_exits_zero_with_stdout():
    """boxes.py --help must exit 0 with non-empty stdout (bin help smoke)."""
    result = subprocess.run(
        [sys.executable, str(BOXES_PY), "--help"],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, (
        f"boxes.py --help exited {result.returncode}.\n"
        f"stderr: {result.stderr[:500]}"
    )
    assert len(result.stdout.strip()) > 0
    # Description comes from the module docstring first line.
    assert "box" in result.stdout.lower()


# --------------------------------------------------------------------------
# graph_root / box_cells / require_box_cells
# --------------------------------------------------------------------------

def test_graph_root_returns_root_when_config_json_present(tmp_path):
    root = _graph(tmp_path)
    assert boxes.graph_root(root) == root.resolve()


def test_graph_root_unchanged_when_no_enclosing_graph(tmp_path):
    bare = tmp_path / "not-a-graph"
    bare.mkdir()
    # No config.json and no enclosing project — returns start unchanged.
    assert boxes.graph_root(bare) == bare.resolve()


def test_box_cells_reads_declared_fields(tmp_path):
    root = _graph(tmp_path, box_cells={
        "root": "/r", "logs_dir": "/l", "tmux_session": "s", "user": "u",
        "extra_ignored": "x",
    })
    cells = boxes.box_cells(root)
    assert cells == {
        "root": "/r",
        "logs_dir": "/l",
        "tmux_session": "s",
        "user": "u",
    }
    assert "extra_ignored" not in cells


def test_require_box_cells_happy_path(tmp_path):
    root = _graph(tmp_path)
    names = boxes.require_box_cells(root)
    assert names == ("root", "logs_dir", "tmux_session", "user")


def test_require_box_cells_refuses_absent_or_empty_schema(tmp_path):
    """Error path: absent fields (or absent schema) → BoxSchemaError."""
    root = _graph(tmp_path, with_schema=False)
    with pytest.raises(boxes.BoxSchemaError) as ei:
        boxes.require_box_cells(root)
    assert "declares no box cells" in str(ei.value)

    root2 = _graph(tmp_path / "empty-fields", schema_fields=False)
    with pytest.raises(boxes.BoxSchemaError):
        boxes.require_box_cells(root2)


# --------------------------------------------------------------------------
# this_box / default_box
# --------------------------------------------------------------------------

def test_this_box_reads_agi_box_from_env(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "sanctuary")
    root = _graph(tmp_path, env_box=None)
    assert boxes.this_box(root) == "sanctuary"


def test_this_box_refuses_when_agi_box_unset(tmp_path):
    root = _graph(tmp_path, env_box=None)
    with pytest.raises(RuntimeError) as ei:
        boxes.this_box(root)
    msg = str(ei.value)
    assert "AGI_BOX" in msg
    assert "default_box" in msg  # named as documentation, never a fallback


def test_default_box_reads_posts_frontmatter(tmp_path):
    root = _graph(tmp_path, default_box="core-town")
    assert boxes.default_box(root) == "core-town"


def test_default_box_empty_when_undeclared(tmp_path):
    root = _graph(tmp_path, default_box=None)
    assert boxes.default_box(root) == ""


# --------------------------------------------------------------------------
# row_is_local
# --------------------------------------------------------------------------

def test_row_is_local_when_row_box_matches_this_box(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "local-town")
    root = _graph(tmp_path, env_box=None)
    assert boxes.row_is_local(root, {"name": "x", "box": "local-town"})
    assert not boxes.row_is_local(root, {"name": "x", "box": "sanctuary"})


def test_row_is_local_empty_or_unknown_never_local(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "local-town")
    root = _graph(tmp_path, env_box=None, default_box="local-town")
    assert not boxes.row_is_local(root, {"name": "x"})
    assert not boxes.row_is_local(root, {"name": "x", "box": ""})
    assert not boxes.row_is_local(root, {"name": "x", "box": "(default)"})
    assert not boxes.row_is_local(root, {"name": "x", "box": "nonesuch"})


def test_row_is_local_fail_open_on_undeclared_box_graph(tmp_path):
    """A graph with no AGI_BOX at all: empty-box rows stay local (single-box)."""
    root = _graph(tmp_path, env_box=None)
    assert boxes.row_is_local(root, {"name": "x"})
    assert not boxes.row_is_local(root, {"name": "x", "box": "sanctuary"})
