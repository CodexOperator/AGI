"""goal:g7.16.1.11.46.23 V8a (council row, alive 22:30:53Z 10-25): the ROW-ABSENT case stays a NAMED SKIP.

A seat with no row in config:posts/seats is not a registered post (a THROWAWAY seat). The two identity-cell
writers in rotate.py return the 'skipped: no seat-registry row ...' line BEFORE config_rows.write_rows is
reached: never a refusal, never a silent pass, never a false 'wrote identity cells'. The refusal is owed
where a row EXISTS and cannot be written (test_rotate_prepare's twin test). One row per site, for both
absent shapes: a graph whose posts.md lacks this seat, and a graph with no config file at all.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import config_rows  # noqa: E402
import rotate  # noqa: E402


def _graph(tmp_path, with_file: bool):
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True)
    f = g / "posts.md"
    if with_file:
        f.write_text('---\nid: config:posts\ntype: config\nposts:\n  - {"name": "someone-else", "role": "director"}\n---\n',
                     encoding="utf-8")
    return root, f


def _assert_skip(out, root, f, with_file):
    """Each cause prints its OWN words (council 22:32Z): never the same line for two shapes."""
    if with_file:
        assert out.startswith(f"skipped: no row for 'throwaway' in {f}"), out
        assert "no config:posts/seats file" not in out
    else:
        assert out.startswith(f"skipped: no config:posts/seats file in {root}"), out
        assert "no row for" not in out
    assert "(throwaway inferred from absence, not marked)" in out


@pytest.fixture(autouse=True)
def _write_rows_must_not_run(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("config_rows.write_rows was reached for a seat with no row")

    monkeypatch.setattr(config_rows, "write_rows", boom)


@pytest.mark.parametrize("with_file", [True, False], ids=["posts.md-lacks-the-seat", "no-config-file"])
def test_successor_row_write_skips_by_name(tmp_path, with_file):
    root, f = _graph(tmp_path, with_file)
    before = f.read_bytes() if with_file else None
    out = rotate._successor_row_write(root, actor="throwaway", seat="throwaway", role="kid",
                                      session_ref="x-1", generation=2, window="w")
    _assert_skip(out, root, f, with_file)
    assert "wrote identity cells" not in out
    assert (f.read_bytes() == before) if with_file else (not f.exists())


@pytest.mark.parametrize("with_file", [True, False], ids=["posts.md-lacks-the-seat", "no-config-file"])
def test_backfill_session_ref_skips_by_name(tmp_path, with_file):
    root, f = _graph(tmp_path, with_file)
    before = f.read_bytes() if with_file else None
    out = rotate._backfill_session_ref(root, seat="throwaway", role="kid", ref="x-1",
                                       session_name="n", session_id=None, pid=None)
    _assert_skip(out, root, f, with_file)
    assert "wrote identity cells" not in out and "back-filled" not in out
    assert (f.read_bytes() == before) if with_file else (not f.exists())


def test_mutant_a_seat_WITH_a_row_does_reach_write_rows(tmp_path, monkeypatch):
    """The skip is not a blanket: a seat that HAS a row reaches write_rows (so the boom fixture is live)."""
    root, f = _graph(tmp_path, True)
    f.write_text('---\nid: config:posts\ntype: config\nposts:\n  - {"name": "real", "role": "director"}\n---\n',
                 encoding="utf-8")
    with pytest.raises(AssertionError, match="was reached"):
        rotate._write_identity_cells(root, seat="real", actor="real", role="director", cells={"pid": 3})
