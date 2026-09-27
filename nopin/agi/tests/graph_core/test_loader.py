"""Tests for graph_core.loader.load_directory's duplicate-id detection (G7.2).

G7.2: two files declaring the same `id` used to be dropped by `load_directory`
with zero signal — the second file just silently never made it into the
graph. These tests pin the fix: detection happens in the load_directory pass
that already walks the corpus (no second pass), warns by default without
raising, exposes the collisions on `graph.duplicate_ids`, and only raises
under `strict=True`.
"""

from pathlib import Path

import pytest

from graph_core.errors import GraphCoreError
from graph_core.loader import DuplicateIdError, load_directory


def _seed(d: Path, files: dict[str, str]) -> None:
    for name, content in files.items():
        p = d / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)


def test_no_duplicates_is_a_noop(tmp_path: Path) -> None:
    """The common case: distinct ids, nothing reported."""
    _seed(tmp_path, {
        "a.md": "---\nid: a\n---\n",
        "b.md": "---\nid: b\n---\n",
    })
    g, loaded = load_directory(tmp_path)
    assert len(loaded) == 2
    assert g.duplicate_ids == []


def test_duplicate_id_keeps_first_sorted_file_unchanged_behaviour(tmp_path: Path) -> None:
    """First file in sorted-walk order still wins — detection must not change this."""
    _seed(tmp_path, {
        "a_first.md": "---\nid: dup\n---\nfirst body\n",
        "z_second.md": "---\nid: dup\n---\nsecond body\n",
    })
    g, loaded = load_directory(tmp_path)
    assert len(loaded) == 1
    assert loaded[0].body.strip() == "first body"
    assert g.get_node("dup") is not None


def test_duplicate_id_recorded_on_graph(tmp_path: Path) -> None:
    """The dropped file is no longer invisible: it shows up in duplicate_ids."""
    _seed(tmp_path, {
        "a_first.md": "---\nid: dup\n---\n",
        "z_second.md": "---\nid: dup\n---\n",
    })
    g, loaded = load_directory(tmp_path)
    assert len(g.duplicate_ids) == 1
    nid, kept_path, hidden_path = g.duplicate_ids[0]
    assert nid == "dup"
    assert kept_path.name == "a_first.md"
    assert hidden_path.name == "z_second.md"


def test_duplicate_id_warns_to_stderr_by_default(tmp_path: Path, capsys) -> None:
    _seed(tmp_path, {
        "a_first.md": "---\nid: dup\n---\n",
        "z_second.md": "---\nid: dup\n---\n",
    })
    load_directory(tmp_path)
    err = capsys.readouterr().err
    assert "WARN" in err
    assert "duplicate node id 'dup'" in err
    assert "a_first.md" in err
    assert "z_second.md" in err


def test_default_mode_never_raises(tmp_path: Path) -> None:
    """The loop must never break on this by default (mirrors snapshot-goals.py)."""
    _seed(tmp_path, {
        "a_first.md": "---\nid: dup\n---\n",
        "z_second.md": "---\nid: dup\n---\n",
    })
    g, loaded = load_directory(tmp_path)  # must not raise
    assert len(loaded) == 1


def test_strict_raises_duplicate_id_error(tmp_path: Path) -> None:
    _seed(tmp_path, {
        "a_first.md": "---\nid: dup\n---\n",
        "z_second.md": "---\nid: dup\n---\n",
    })
    with pytest.raises(DuplicateIdError) as excinfo:
        load_directory(tmp_path, strict=True)
    assert excinfo.value.duplicates[0][0] == "dup"
    assert isinstance(excinfo.value, GraphCoreError)


def test_strict_reports_every_collision_not_just_first(tmp_path: Path) -> None:
    _seed(tmp_path, {
        "a1.md": "---\nid: dup1\n---\n",
        "a2.md": "---\nid: dup1\n---\n",
        "b1.md": "---\nid: dup2\n---\n",
        "b2.md": "---\nid: dup2\n---\n",
    })
    with pytest.raises(DuplicateIdError) as excinfo:
        load_directory(tmp_path, strict=True)
    ids = {d[0] for d in excinfo.value.duplicates}
    assert ids == {"dup1", "dup2"}


def test_strict_with_no_duplicates_does_not_raise(tmp_path: Path) -> None:
    _seed(tmp_path, {"a.md": "---\nid: a\n---\n", "b.md": "---\nid: b\n---\n"})
    g, loaded = load_directory(tmp_path, strict=True)
    assert len(loaded) == 2


def test_load_directory_still_returns_a_two_tuple(tmp_path: Path) -> None:
    """Callers all over the codebase do `g, loaded = load_directory(...)` — signature must hold."""
    _seed(tmp_path, {"a.md": "---\nid: a\n---\n"})
    result = load_directory(tmp_path)
    assert isinstance(result, tuple)
    assert len(result) == 2
