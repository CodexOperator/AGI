"""goal:g7.16.1.11.46.12 / GATE282 trunk red 2 (council 10-26): prereq_notice's --trunk default is the ladder's CURRENT season of the engine's own tree
(derived through branches.py), so the season rollover moves it; a fixed season number would be the same debt in another spelling."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import prereq_notice  # noqa: E402

SRC = BIN / "prereq_notice.py"


def test_the_default_follows_the_ladders_current_season(monkeypatch):
    for n in (3, 4, 9):
        monkeypatch.setattr(prereq_notice, "_ladder", lambda start, n=n: {"current_season": n})
        assert prereq_notice.default_trunk() == f"refs/heads/core/season{n}/main"


def test_the_live_ladder_gives_the_live_trunk():
    assert prereq_notice.default_trunk() == "refs/heads/core/season3/main"          # the live ladder's current_season today


def test_a_ladder_without_a_current_season_is_loud_never_a_guess(monkeypatch):
    monkeypatch.setattr(prereq_notice, "_ladder", lambda start: {})
    with pytest.raises(SystemExit, match="no current_season"):
        prereq_notice.default_trunk()


def test_the_verbs_resolve_the_default_at_run_time_not_import_time(monkeypatch, tmp_path, capsys):
    seen = []
    monkeypatch.setattr(prereq_notice, "_ladder", lambda start: {"current_season": 7})
    monkeypatch.setattr(prereq_notice, "line", lambda a: seen.append(a.trunk) or "notices: x")
    assert prereq_notice.main(["line", "--repo", str(tmp_path)]) == 0
    assert seen == ["refs/heads/core/season7/main"]
    seen.clear()
    prereq_notice.main(["line", "--repo", str(tmp_path), "--trunk", "refs/heads/x/y"])
    assert seen == ["refs/heads/x/y"]                                                # an explicit --trunk still wins


def _copy(tmp_path, name, edit=None):
    text = SRC.read_text()
    if edit:
        old, new = edit
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    p = tmp_path / f"{name}.py"
    p.write_text(text)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m._ladder = lambda start: {"current_season": 4}                                  # the ladder says season 4
    return m


def test_mutant_the_literal_season_back_does_not_move_with_the_ladder(tmp_path):
    old = 'branches.derive_names("core", int(cur))'
    clean = _copy(tmp_path, "pn_clean")
    mutant = _copy(tmp_path, "pn_mutant", (old, 'branches.derive_names("core", 3)'))
    assert clean.default_trunk() == "refs/heads/core/season4/main"                    # the row's clean side moves with the ladder
    assert mutant.default_trunk() != "refs/heads/core/season4/main", "the mutant ignores the ladder (the rows above would be RED)"
