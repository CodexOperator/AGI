"""Tests for bin/zoom.py — the numeric 1..5 zoom axis + legacy big/small aliases.

Two things matter more than any single level's exact wording:

1. **No code path may fall back to the whole graph.** zoom.py used to have
   three `except` branches (graph_core import, sqlite backend, filesystem
   loader) plus a target-not-found branch that all silently served
   `_compose_big` (the entire corpus) instead of the bounded view the caller
   asked for. All four are now `ZoomUnavailable` -> non-zero exit. This file
   asserts that behaviour directly (missing target at every level, a broken
   sqlite backend) AND with a static source guard that the exact defect
   pattern (`return _compose_big(...)` as a fallback) never reappears.

2. **Legacy `--level big`/`--level small` keep their original CONTENT**, not
   the new type-filtered rendering — dispatch.py's live research pipeline
   calls `small` with hypothesis/experiment targets, and collapsing that
   through the level-3 (code-only) filter would silently break it. They are
   documented (stderr deprecation note) as closest to levels 1 and 3
   respectively, but that mapping is for migration guidance only.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ZOOM = BIN / "zoom.py"
SOURCE = ZOOM.read_text(encoding="utf-8")


def _node(root: Path, ntype: str, slug: str, parents=(), fm_extra: str = "", body: str = "body text") -> None:
    d = root / "nodes" / ntype
    d.mkdir(parents=True, exist_ok=True)
    lines = ["---", f'id: "{ntype}:{slug}"', f"type: {ntype}", f'title: "{ntype} {slug} title"']
    if parents:
        lines.append("parents:")
        lines += [f"  - {p}" for p in parents]
    if fm_extra:
        lines.append(fm_extra.rstrip())
    lines += ["---", "", body, ""]
    (d / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")


def run(project: Path, iter_n: int, agent_id: str, *extra_args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ZOOM), str(project), str(iter_n), agent_id, *extra_args],
        capture_output=True, text=True,
    )


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    (tmp_path / "agi-tree.config.json").write_text('{"metric_primary": "outcome_coverage"}')
    (tmp_path / "context").mkdir()
    (tmp_path / "context" / "INJECTION.md").write_text(
        "# injection\nINJECTION-MARKER-TEXT\n", encoding="utf-8"
    )

    # Level 1: a two-goal skill-tree.
    _node(tmp_path, "goal", "g1")
    _node(tmp_path, "goal", "g1.1", parents=["goal:g1"])

    # Level 2: one census idea (has unit_path) + one non-census idea (doesn't)
    # under the same parent goal, so BFS reaches both but only one should
    # ever be shown at level 2.
    _node(tmp_path, "idea", "engine-foo", parents=["goal:g1"], fm_extra="unit_path: bin/foo.py")
    _node(tmp_path, "idea", "domain-bar", parents=["goal:g1"])

    # Level 3: one code node, child of the census idea.
    _node(
        tmp_path, "level3", "bin-foo", parents=["idea:engine-foo"],
        fm_extra="payload_ref: bin/foo.py",
    )
    return tmp_path


def _ctx_path(proc: subprocess.CompletedProcess) -> Path:
    return Path(proc.stdout.strip())


# --------------------------------------------------------------------------
# basic plumbing: project validation, output path, argparse
# --------------------------------------------------------------------------

def test_not_a_project_root_refuses(tmp_path):
    proc = run(tmp_path, 1, "a00", "--level", "1")
    assert proc.returncode == 1
    assert "not a project root" in proc.stderr


def test_invalid_level_value_rejected(project):
    proc = run(project, 1, "a00", "--level", "6")
    assert proc.returncode != 0


def test_output_path_matches_sessions_convention(project):
    proc = run(project, 7, "a03-xyz", "--level", "1")
    assert proc.returncode == 0, proc.stderr
    expected = project / "sessions" / "iter-007" / "a03-xyz" / "context.md"
    assert _ctx_path(proc) == expected
    assert expected.is_file()


# --------------------------------------------------------------------------
# numeric levels 1-3: correct type filtering + level meaning stated
# --------------------------------------------------------------------------

def test_level1_shows_goal_tree_and_states_its_meaning(project):
    proc = run(project, 1, "a00", "--level", "1", "--target", "goal:g1")
    assert proc.returncode == 0, proc.stderr
    text = _ctx_path(proc).read_text()
    assert "Zoom Level: 1 — Goals" in text
    assert "skill-tree of general nodes" in text  # states what the level means
    assert "goal:g1.1" in text
    # idea nodes are 1 hop away but must NOT leak into the level-1 listing
    assert "### Goals in scope" in text
    scope = text.split("### Goals in scope", 1)[1].split("## Your Task", 1)[0]
    # goal:g1 (the target) legitimately lists its idea children in its own
    # "children:" context line — that's useful, not a type leak. What must
    # NOT happen is an idea node being *rendered as its own bullet* (title
    # suffix only ever appears on a rendered bullet, never a bare id ref).
    assert "idea engine-foo title" not in scope
    assert "idea domain-bar title" not in scope


def test_level1_no_target_shows_whole_goal_census(project):
    proc = run(project, 1, "a00", "--level", "1")
    assert proc.returncode == 0, proc.stderr
    text = _ctx_path(proc).read_text()
    assert "goal:g1" in text and "goal:g1.1" in text


def test_level2_excludes_noncensus_ideas(project):
    proc = run(project, 1, "a00", "--level", "2", "--target", "goal:g1")
    assert proc.returncode == 0, proc.stderr
    text = _ctx_path(proc).read_text()
    assert "Zoom Level: 2 — Sub-systems" in text
    assert "sub-systems and their relationships" in text
    assert "idea:engine-foo" in text
    assert "bin/foo.py" in text  # unit_path shown
    assert "idea:domain-bar" not in text  # no unit_path -> not a census node


def test_level3_shows_payload_ref_and_states_its_meaning(project):
    proc = run(project, 1, "a00", "--level", "3", "--target", "idea:engine-foo")
    assert proc.returncode == 0, proc.stderr
    text = _ctx_path(proc).read_text()
    assert "Zoom Level: 3 — Code nodes" in text
    assert "level3:bin-foo" in text
    assert "bin/foo.py" in text
    assert "payload_ref" in text or "IO contract" in text  # explains what level 3 is


def test_level3_no_target_shows_whole_level3_census(project):
    proc = run(project, 1, "a00", "--level", "3")
    assert proc.returncode == 0, proc.stderr
    text = _ctx_path(proc).read_text()
    assert "level3:bin-foo" in text


# --------------------------------------------------------------------------
# levels 4/5: honest refusal, never a fallback grain
# --------------------------------------------------------------------------

@pytest.mark.parametrize("level", ["4", "5"])
def test_levels_4_and_5_refuse_without_touching_the_graph(project, level):
    proc = run(project, 1, f"a{level}", "--level", level)
    assert proc.returncode == 1
    assert "not yet available" in proc.stderr
    # must not silently serve any other grain's content
    assert "goal:g1" not in proc.stderr
    assert "idea:engine-foo" not in proc.stderr
    out = project / "sessions" / "iter-001" / f"a{level}" / "context.md"
    assert not out.exists()


def test_level4_names_what_would_need_to_exist(project):
    proc = run(project, 1, "a04", "--level", "4")
    assert "level4" in proc.stderr
    assert "call graph" in proc.stderr or "call-level" in proc.stderr


def test_level5_names_what_would_need_to_exist(project):
    proc = run(project, 1, "a05", "--level", "5")
    assert "level5" in proc.stderr
    assert "built-in" in proc.stderr.lower()


# --------------------------------------------------------------------------
# safety property: nothing falls back to the whole graph
# --------------------------------------------------------------------------

@pytest.mark.parametrize("level", ["1", "2", "3", "small"])
def test_missing_target_refuses_instead_of_falling_back(project, level):
    extra = ["--level", level, "--target", "nonexistent:ghost"]
    proc = run(project, 2, f"m{level}", *extra)
    assert proc.returncode == 1
    assert "ERR" in proc.stderr
    assert "Refusing to fall back to the whole graph" in proc.stderr
    out = project / "sessions" / "iter-002" / f"m{level}" / "context.md"
    assert not out.exists()


def test_small_without_target_is_still_required(project):
    proc = run(project, 1, "a00", "--level", "small")
    assert proc.returncode == 1
    assert "--target required" in proc.stderr


def test_broken_sqlite_backend_refuses_rather_than_falls_back(tmp_path):
    blocker = tmp_path / "blocker"
    blocker.write_text("i am a file, not a directory")
    (tmp_path / "agi-tree.config.json").write_text(
        '{"persistence": {"type": "sqlite", "path": "blocker/db.sqlite"}}'
    )
    (tmp_path / "context").mkdir()
    (tmp_path / "context" / "INJECTION.md").write_text("x\n")
    proc = run(tmp_path, 1, "a00", "--level", "1")
    assert proc.returncode == 1
    assert "Refusing to fall back to the whole graph" in proc.stderr


def test_source_never_returns_compose_big_as_a_fallback():
    """Static regression guard for the exact defect class this file fixes.

    Previously: `return _compose_big(inject_text, args).replace(...)` inside
    the target-not-found branch of small-zoom. `_compose_big` must only ever
    be called from the one place that legitimately means "give me the whole
    graph": the --level big branch in main().
    """
    assert "return _compose_big" not in SOURCE
    call_sites = [
        line for line in SOURCE.splitlines()
        if "_compose_big(" in line and not line.strip().startswith("def ")
    ]
    assert len(call_sites) == 1, call_sites


# --------------------------------------------------------------------------
# legacy big/small: unchanged content + deprecation note + numeric mapping
# --------------------------------------------------------------------------

def test_legacy_big_keeps_original_whole_graph_content(project):
    proc = run(project, 1, "a00", "--level", "big")
    assert proc.returncode == 0, proc.stderr
    assert "DEPRECATION" in proc.stderr
    assert "level 1" in proc.stderr
    text = _ctx_path(proc).read_text()
    assert "Zoom Level: BIG" in text
    assert "INJECTION-MARKER-TEXT" in text  # full INJECTION.md still embedded
    assert "cli.py done" in text


def test_legacy_small_keeps_original_any_type_content(project):
    proc = run(project, 1, "a00", "--level", "small", "--target", "goal:g1")
    assert proc.returncode == 0, proc.stderr
    assert "DEPRECATION" in proc.stderr
    assert "level 3" in proc.stderr
    text = _ctx_path(proc).read_text()
    assert "Zoom Level: SMALL" in text
    # unlike numeric level 1, legacy small shows every node type it finds
    assert "goal:g1.1" in text
    assert "idea:engine-foo" in text
    assert "idea:domain-bar" in text


def test_legacy_and_numeric_targeting_the_same_node_differ_in_scope(project):
    """The exact behavior change this file makes: small (any type) vs level 1 (goal only)."""
    small = run(project, 3, "small-cmp", "--level", "small", "--target", "goal:g1")
    lvl1 = run(project, 3, "lvl1-cmp", "--level", "1", "--target", "goal:g1")
    assert small.returncode == 0 and lvl1.returncode == 0
    small_text = _ctx_path(small).read_text()
    lvl1_text = _ctx_path(lvl1).read_text()
    assert "idea:engine-foo" in small_text
    assert "idea engine-foo title" not in lvl1_text.split("### Goals in scope", 1)[1]
