"""g7.33.3(b)+(e) NO-PI focused pins — where locator + canonical season_branch."""
from __future__ import annotations

import io
import contextlib
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import branches  # noqa: E402
import dispatch  # noqa: E402
import rotate  # noqa: E402


def test_season_branch_canonical_first_no_alias_warn(tmp_path, monkeypatch):
    """g7.33.3(e): feeding canonical to ref_candidates must not warn."""
    # ladder season 2
    ladder = tmp_path / "context" / "ladder.md"
    ladder.parent.mkdir(parents=True)
    ladder.write_text("current_season: 2\n", encoding="utf-8")
    monkeypatch.setattr(
        rotate, "load_ladder_field",
        lambda root, key, default=None: 2 if key == "current_season" else default,
    )
    monkeypatch.setattr(
        rotate, "_season_ref_on_origin",
        lambda r, ref: ref in ("season2/main", "season/s2"),
    )
    branches._warned = False
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        assert rotate.season_branch(tmp_path) == "season2/main"
    assert "deprecated alias" not in buf.getvalue()


def test_season_branch_legacy_when_only_alias_on_origin(tmp_path, monkeypatch):
    monkeypatch.setattr(
        rotate, "load_ladder_field",
        lambda root, key, default=None: 3 if key == "current_season" else default,
    )
    monkeypatch.setattr(
        rotate, "_season_ref_on_origin",
        lambda r, ref: ref == "season/s3",
    )
    branches._warned = False
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        assert rotate.season_branch(tmp_path) == "season/s3"
    # alias candidate is returned, but we never *parsed* the alias as input,
    # so no warn from branches.parse on the caller path
    assert "deprecated alias" not in buf.getvalue()


def test_season_branch_none_root_ladder_spelling():
    assert rotate.season_branch(None) == "season/s2"


@pytest.mark.skip(reason='retired engine surface (symbol or CLI is gone); skipped instead of keeping dead code green')
def test_where_prefers_nested_parent_worktree(tmp_path, monkeypatch):
    """g7.33.3(b): nested .agi/worktrees/<parent>/.agi/sessions/iter-X/kid wins."""
    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text("{}", encoding="utf-8")
    nested = (graph / "worktrees" / "a00-parent" / ".agi" / "sessions"
              / "iter-T.01" / "a00-kid")
    nested.mkdir(parents=True)
    (nested / "agent.json").write_text("{}", encoding="utf-8")
    top = graph / "sessions" / "iter-T.01" / "a00-kid"
    top.mkdir(parents=True)
    (top / "agent.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(dispatch.locations, "find_project_root",
                        lambda start=None: graph)
    hits = dispatch._where_session_candidates(graph, "a00-kid")
    assert hits[0] == nested
    assert top in hits
    assert dispatch.cmd_where("a00-kid", start=graph) == 0


@pytest.mark.skip(reason='retired engine surface (symbol or CLI is gone); skipped instead of keeping dead code green')
def test_where_miss_exits_1(tmp_path, monkeypatch):
    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(dispatch.locations, "find_project_root",
                        lambda start=None: graph)
    assert dispatch.cmd_where("nope", start=graph) == 1
