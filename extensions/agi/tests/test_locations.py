"""Tests for bin/locations.py — the one path resolver (goal:g11).

The value of this file is mostly in the *layout* fixtures rather than the
assertions: every one of them is a shape the engine has to survive during the
G11 migration, including the half-migrated ones that only exist for a few
commits and are exactly where a resolver goes wrong.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
LIB = Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(BIN))

import locations  # noqa: E402


# --- fixtures --------------------------------------------------------------


def make_legacy(root: Path, name: str = "agi-tree.config.json", **cfg) -> Path:
    """The layout that exists today: the tree IS the project root."""
    root.mkdir(parents=True, exist_ok=True)
    (root / name).write_text(json.dumps(cfg or {"metric_primary": "outcome_coverage"}))
    (root / "nodes").mkdir(exist_ok=True)
    return root


def make_graph_dir(repo: Path, name: str = "config.json", **cfg) -> Path:
    """The goal:g11 layout: `<repo>/.agi/` beside the source it describes."""
    graph = repo / ".agi"
    graph.mkdir(parents=True, exist_ok=True)
    (graph / name).write_text(json.dumps(cfg or {"metric_primary": "outcome_coverage"}))
    (graph / "nodes").mkdir(exist_ok=True)
    return graph


# --- phase 1: the legacy layout still resolves -----------------------------


def test_legacy_root_from_subdir(tmp_path):
    root = make_legacy(tmp_path / "proj")
    deep = root / "nodes" / "goal"
    deep.mkdir(parents=True)
    assert locations.find_project_root(deep) == root


def test_legacy_name_still_accepted(tmp_path):
    root = make_legacy(tmp_path / "proj", name="autoresearch-tree.config.json")
    assert locations.find_project_root(root) == root


def test_canonical_wins_when_both_names_present(tmp_path):
    root = make_legacy(tmp_path / "proj")
    (root / "autoresearch-tree.config.json").write_text("{}")
    assert locations.config_path(root).name == "agi-tree.config.json"


def test_no_project_returns_none(tmp_path):
    (tmp_path / "empty").mkdir()
    assert locations.find_project_root(tmp_path / "empty") is None


# --- phase 0: the G11 layout -----------------------------------------------


def test_graph_dir_resolves_to_the_dot_agi_itself(tmp_path):
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    assert locations.find_project_root(repo) == graph
    assert locations.is_graph_dir(graph)
    assert locations.repo_root(graph) == repo


def test_graph_dir_found_walking_up_from_source(tmp_path):
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    deep = repo / "src" / "engine" / "render"
    deep.mkdir(parents=True)
    assert locations.find_project_root(deep) == graph


def test_bare_config_json_is_a_marker_only_inside_dot_agi(tmp_path):
    """A stray config.json must never make an ordinary repo look like a graph."""
    plain = tmp_path / "someone-elses-repo"
    plain.mkdir()
    (plain / "config.json").write_text("{}")
    assert locations.config_path(plain) is None
    assert locations.find_project_root(plain) is None


def test_dot_agi_without_a_config_is_not_a_project(tmp_path):
    repo = tmp_path / "repo"
    (repo / ".agi").mkdir(parents=True)
    assert locations.find_project_root(repo) is None


# --- the case the interleaved walk exists for ------------------------------


def test_nearest_enclosing_wins_between_two_graphs(tmp_path):
    """A project checkout carries two graphs: its own and the engine clone's.

    Neither needs a flag — the answer falls out of where you are standing,
    which is what keeps goal:g8.2's "the engine never knows which project it
    is running" true under G11.
    """
    repo = tmp_path / "fantasia"
    outer = make_graph_dir(repo)
    inner = make_graph_dir(repo / "agi")

    assert locations.find_project_root(repo) == outer
    assert locations.find_project_root(repo / "agi") == inner
    assert locations.find_project_root(repo / "agi" / "extensions") == inner


def test_graph_dir_beats_legacy_marker_in_the_same_directory(tmp_path):
    """Half-migrated: both markers present. The new layout wins."""
    repo = tmp_path / "proj"
    make_legacy(repo)
    graph = make_graph_dir(repo)
    assert locations.find_project_root(repo) == graph


def test_near_legacy_beats_distant_graph_dir(tmp_path):
    """The regression the single interleaved walk prevents.

    Two separate walks — all of phase 0, then all of phase 1 — would return the
    distant `.agi/` here, inverting "nearest enclosing wins" at exactly the
    moment a repo is half migrated.
    """
    outer = tmp_path / "outer"
    make_graph_dir(outer)
    inner = make_legacy(outer / "sub" / "proj")
    assert locations.find_project_root(inner) == inner


# --- phase 2: descend ------------------------------------------------------


def test_descend_prefers_basename_match(tmp_path):
    start = tmp_path / "fantasia"
    start.mkdir()
    tree = make_legacy(start / "fantasia-tree")
    make_legacy(start / "other-tree")
    assert locations.find_project_root(start) == tree


def test_descend_ambiguous_returns_none(tmp_path):
    start = tmp_path / "work"
    start.mkdir()
    make_legacy(start / "a-tree")
    make_legacy(start / "b-tree")
    assert locations.find_project_root(start) is None


def test_descend_skips_a_tree_dir_with_no_config(tmp_path):
    start = tmp_path / "work"
    start.mkdir()
    (start / "decoy-tree").mkdir()
    tree = make_legacy(start / "real-tree")
    assert locations.find_project_root(start) == tree


# --- source_root -----------------------------------------------------------


def test_source_root_defaults_to_repo_under_graph_dir_layout(tmp_path):
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    assert locations.source_root(graph) == repo


def test_source_root_defaults_to_engine_beside_a_legacy_tree(tmp_path):
    """Today's `agi-tree/agi` symlink and `fantasia/agi` clone, unchanged."""
    root = make_legacy(tmp_path / "proj")
    engine = root / "agi"
    engine.mkdir()
    assert locations.source_root(root) == engine


def test_source_root_falls_back_to_the_graph_root(tmp_path):
    root = make_legacy(tmp_path / "proj")
    assert locations.source_root(root) == root


def test_source_root_relative_is_resolved_against_the_graph_root(tmp_path):
    """The 'run against a custom source location' dial.

    Relative means relative to the *graph* root, which is what makes `".."` the
    natural spelling of "the repo I live in" and `"../vendor"` the natural
    spelling of a sibling of the graph directory.
    """
    repo = tmp_path / "repo"
    (repo / "vendor").mkdir(parents=True)
    graph = make_graph_dir(repo, locations={"source_root": ".."})
    assert locations.source_root(graph) == repo

    graph2 = make_graph_dir(repo, locations={"source_root": "../vendor"})
    assert locations.source_root(graph2) == repo / "vendor"


def test_source_root_can_climb_out_of_the_repo(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "elsewhere"
    target.mkdir()
    graph = make_graph_dir(repo, locations={"source_root": "../../elsewhere"})
    assert locations.source_root(graph) == target


def test_source_root_explicit_absolute_override(tmp_path):
    target = tmp_path / "somewhere-else"
    target.mkdir()
    root = make_legacy(tmp_path / "proj", locations={"source_root": str(target)})
    assert locations.source_root(root) == target


def test_source_root_override_beats_the_layout_default(tmp_path):
    repo = tmp_path / "repo"
    (repo / "vendor").mkdir(parents=True)
    graph = make_graph_dir(repo, locations={"source_root": "../vendor"})
    assert locations.source_root(graph) == repo / "vendor"


# --- goals_path ------------------------------------------------------------


def test_goals_render_to_the_repo_root_not_inside_dot_agi(tmp_path):
    """The reason `goals_path` exists at all."""
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    assert locations.goals_path(graph) == repo / "GOALS.md"


def test_goals_stay_at_the_graph_root_under_the_legacy_layout(tmp_path):
    root = make_legacy(tmp_path / "proj")
    assert locations.goals_path(root) == root / "GOALS.md"


def test_goals_file_override_resolves_the_dropin_collision(tmp_path):
    """A repo that already ships its own GOALS.md keeps both documents."""
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo, goals_file="AGI-GOALS.md")
    assert locations.goals_path(graph) == repo / "AGI-GOALS.md"
    assert locations.goals_path(graph).name != "GOALS.md"


def test_goals_file_with_a_separator_is_relative_to_the_graph_root(tmp_path):
    repo = tmp_path / "repo"
    graph = make_graph_dir(repo, goals_file="docs/GOALS.md")
    assert locations.goals_path(graph) == graph / "docs" / "GOALS.md"


def test_goals_file_absolute_is_used_as_is(tmp_path):
    target = tmp_path / "anywhere" / "G.md"
    root = make_legacy(tmp_path / "proj", goals_file=str(target))
    assert locations.goals_path(root) == target


def test_blank_goals_file_falls_back_to_the_default(tmp_path):
    root = make_legacy(tmp_path / "proj", goals_file="   ")
    assert locations.goals_path(root) == root / "GOALS.md"


# --- config loading --------------------------------------------------------


def test_malformed_config_does_not_raise(tmp_path):
    """Half the engine imports this at module scope; it must not die on import."""
    root = tmp_path / "proj"
    root.mkdir()
    (root / "agi-tree.config.json").write_text("{ this is not json")
    assert locations.load_config(root) == {}
    assert locations.find_project_root(root) == root


def test_non_dict_config_is_treated_as_empty(tmp_path):
    root = tmp_path / "proj"
    root.mkdir()
    (root / "agi-tree.config.json").write_text("[1, 2, 3]")
    assert locations.load_config(root) == {}


def test_missing_config_loads_as_empty(tmp_path):
    assert locations.load_config(tmp_path) == {}


# --- env override ----------------------------------------------------------


def test_env_override_wins(tmp_path, monkeypatch):
    root = make_legacy(tmp_path / "proj")
    other = make_legacy(tmp_path / "other")
    monkeypatch.setenv("AGI_TREE_PROJECT_ROOT", str(other))
    assert locations.project_root_from_env(root) == other


def test_legacy_env_spelling_still_read(tmp_path, monkeypatch):
    other = make_legacy(tmp_path / "other")
    monkeypatch.delenv("AGI_TREE_PROJECT_ROOT", raising=False)
    monkeypatch.setenv("AUTORESEARCH_TREE_PROJECT_ROOT", str(other))
    assert locations.project_root_from_env(tmp_path) == other


# --- the two halves agree --------------------------------------------------


def _bash_find_root(start: Path) -> str | None:
    res = subprocess.run(
        ["bash", str(LIB / "find-root.sh"), str(start)],
        capture_output=True, text=True,
    )
    return res.stdout.strip() if res.returncode == 0 else None


@pytest.mark.parametrize("shape", ["legacy", "graph_dir", "nested", "half_migrated",
                                   "descend", "ambiguous", "none"])
def test_bash_and_python_agree(tmp_path, shape):
    """lib/find-root.sh and bin/locations.py implement ONE rule, twice.

    Written as a parametrized cross-check rather than as duplicated assertions
    because the failure this guards against is drift, and drift shows up as
    exactly one shape disagreeing while the rest still pass.
    """
    if shape == "legacy":
        start = make_legacy(tmp_path / "proj")
        expected = start
    elif shape == "graph_dir":
        repo = tmp_path / "repo"
        expected = make_graph_dir(repo)
        start = repo
    elif shape == "nested":
        repo = tmp_path / "fantasia"
        make_graph_dir(repo)
        expected = make_graph_dir(repo / "agi")
        start = repo / "agi"
    elif shape == "half_migrated":
        repo = tmp_path / "proj"
        make_legacy(repo)
        expected = make_graph_dir(repo)
        start = repo
    elif shape == "descend":
        start = tmp_path / "fantasia"
        start.mkdir()
        expected = make_legacy(start / "fantasia-tree")
    elif shape == "ambiguous":
        start = tmp_path / "work"
        start.mkdir()
        make_legacy(start / "a-tree")
        make_legacy(start / "b-tree")
        expected = None
    else:
        start = tmp_path / "empty"
        start.mkdir()
        expected = None

    py = locations.find_project_root(start)
    sh = _bash_find_root(start)

    assert (str(py) if py else None) == (str(expected) if expected else None)
    assert sh == (str(expected) if expected else None), (
        f"bash and python disagree on shape={shape}: bash={sh!r} python={py!r}"
    )


# --- cli -------------------------------------------------------------------


def test_cli_what_prints_one_path(tmp_path, capsys):
    repo = tmp_path / "fantasia"
    make_graph_dir(repo)
    assert locations.main([str(repo), "--what", "goals"]) == 0
    assert capsys.readouterr().out.strip() == str(repo / "GOALS.md")


def test_cli_json_reports_the_layout(tmp_path, capsys):
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    assert locations.main([str(repo), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["layout"] == "graph_dir"
    assert data["root"] == str(graph)
    assert data["source"] == str(repo)


def test_cli_missing_project_exits_nonzero(tmp_path, capsys):
    (tmp_path / "empty").mkdir()
    assert locations.main([str(tmp_path / "empty")]) == 1
    assert "no agi project found" in capsys.readouterr().out
