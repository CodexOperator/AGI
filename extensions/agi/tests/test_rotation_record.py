"""rotation_record.py's OWN rows (council mur on bundle 3, chunk 1: CM5 CM6 CM8).
The live-node grep fails CLOSED: every hit it cannot read as a node is a named
GrepError, never a silent drop or an escaping exception."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import rotation_record  # noqa: E402


def _node(root: Path, rel: str, text: str) -> None:
    f = root / "nodes" / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, "utf-8")


def test_a_tagged_node_is_a_carrier(tmp_path):
    _node(tmp_path, "goal/g1.md", "---\nid: goal:g1\ntags: [parked:g7.16.2]\n---\nbody\n")
    assert [i for i, _f, _t in rotation_record.parked_carriers(tmp_path, "g7.16.2")] == ["goal:g1"]


def test_a_hit_without_an_id_is_a_named_fail(tmp_path):  # CM5
    _node(tmp_path, "goal/noid.md", "---\ntype: goal\n---\nparked:g7.16.2\n")
    with pytest.raises(rotation_record.GrepError, match="noid.md: frontmatter carries no id"):
        rotation_record.grep_live(tmp_path, "parked:g7.16.2")


def test_a_missing_nodes_dir_is_a_named_fail(tmp_path):  # CM6
    with pytest.raises(rotation_record.GrepError, match="could not run"):
        rotation_record.grep_live(tmp_path, "parked:g7.16.2")


def test_a_string_tags_cell_is_a_named_fail(tmp_path):  # CM8
    _node(tmp_path, "goal/g2.md", "---\nid: goal:g2\ntags: parked:g7.16.2\n---\n")
    with pytest.raises(rotation_record.GrepError, match="goal:g2: `tags` is str"):
        rotation_record.parked_carriers(tmp_path, "g7.16.2")
