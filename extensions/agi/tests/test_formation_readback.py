"""goal:g7.16.1.1.5 · hypothesis:one-cell-activates-one-formation-and-reads-back-one.

verification.check_formation: 0 active -> FAIL · 1 -> PASS · 2 -> FAIL; no cell
-> SKIP. The wake list reads the park mark inside the THOUGHT block only: a
node that merely MENTIONS the mark in its body never wakes (9 such nodes, 09-29).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import verification  # noqa: E402

_T = "<!-- THOUGHT:BEGIN -->\n{}\n<!-- THOUGHT:END -->\n"


def _node(root: Path, rel: str, nid: str, body: str = "") -> None:
    f = root / "nodes" / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(f"---\nid: {nid}\ntype: {nid.split(':')[0]}\n---\n{body}", "utf-8")


@pytest.fixture
def groot(tmp_path):
    root = tmp_path / ".agi"
    _node(root, "doc/council-loop.md", "doc:council-loop")
    _node(root, "doc/two-step.md", "doc:two-step")
    _node(root, "goal/g1.md", "goal:g1", _T.format("keep; parked: formation g7.16.2"))
    _node(root, "goal/g2.md", "goal:g2", "a body naming `parked: formation g7.16.2`\n")
    _node(root, "goal/g3.md", "goal:g3", _T.format("parked: formation g7.16.20"))
    _node(root, "deprecated/goal/g4.md", "goal:g4", _T.format("parked: formation g7.16.2"))
    return root


def _cell(root: Path, active: str) -> None:
    (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / "nodes" / ".geometry" / "formations.md").write_text(
        "---\nid: config:formations\ntype: config\n"
        f"active: {active}\n"
        "templates: {doc:council-loop: g7.16.1, doc:two-step: g7.16.2}\n---\n", "utf-8")


def test_no_cell_is_a_skip(groot):
    assert verification.check_formation(groot).status == "SKIP"


@pytest.mark.parametrize("active", ["''", "[doc:council-loop, doc:two-step]",
                                    "doc:not-registered"])
def test_zero_or_two_active_fails(groot, active):
    _cell(groot, active)
    assert verification.check_formation(groot).status == "FAIL"


def test_one_active_passes_and_wakes_only_the_thought_mark(groot):
    _cell(groot, "doc:two-step")
    r = verification.check_formation(groot)
    assert (r.status, r.note, r.message) == ("PASS", "active doc:two-step g7.16.2",
                                             "wake goal:g1")


def test_switching_is_one_cell_and_changes_the_wake_list(groot):
    _cell(groot, "doc:two-step")
    assert verification.check_formation(groot).number == {"wake": 1}
    _cell(groot, "doc:council-loop")
    r = verification.check_formation(groot)
    assert (r.status, r.number) == ("PASS", {"wake": 0})


# --- goal:g7.16.1.2.5 · hypothesis:formation-check-refuses-a-deprecated-template
# (council bundle 2, director-general-2)
def _cell_with(root: Path, active: str, templates: str) -> None:
    (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / "nodes" / ".geometry" / "formations.md").write_text(
        f"---\nid: config:formations\ntype: config\nactive: {active}\n"
        f"templates: {templates}\n---\n", "utf-8")


# RED on the trunk at 82d64ffe7 -- find_node_file resolves nodes/deprecated/,
# so a retired template passed; green since director-general-3's build.
def test_a_retired_template_fails_the_check(groot):
    _node(groot, "deprecated/doc/retired.md", "doc:retired")
    _cell_with(groot, "doc:retired", "{doc:council-loop: g7.16.1, doc:retired: g7.16.9}")
    assert verification.check_formation(groot).status == "FAIL"


def test_the_switch_runs_through_write_py(groot):
    """The ONE act that switches a formation is `write.py config:formations
    'set active <doc>'` -- driven here in the tmp project, then read back."""
    import subprocess
    (groot / "config.json").write_text("{}\n", "utf-8")
    _cell(groot, "doc:council-loop")
    wp = Path(__file__).resolve().parents[1] / "bin" / "write.py"
    r = subprocess.run([sys.executable, str(wp), "config:formations", "set active doc:two-step",
                        "--actor", "test", "--role", "director"],
                       cwd=groot.parent, capture_output=True, text=True, timeout=120,
                       env={k: v for k, v in __import__("os").environ.items() if not k.startswith(("TMUX", "AGI_"))})
    assert r.returncode == 0, r.stderr[-400:]
    res = verification.check_formation(groot)
    assert res.status == "PASS" and "doc:two-step" in (res.note or "")


# --- goal:g7.16.1.2.6 · hypothesis:park-is-a-tag-that-set-active-drops
# (council bundle 2, director-general-2). Strict xfail: RED on the trunk at
# 82d64ffe7 -- the park is THOUGHT text and `set active` drops nothing.
@pytest.mark.xfail(strict=True, reason="hypothesis:park-is-a-tag-that-set-active-drops")
def test_set_active_drops_that_formations_park_tag(groot):
    import os, subprocess
    (groot / "config.json").write_text("{}\n", "utf-8")
    _cell(groot, "doc:council-loop")
    f = groot / "nodes" / "hypothesis" / "h.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("---\nid: hypothesis:h\ntype: hypothesis\ntitle: h\ntestable_claim: c\n"
                 "tags:\n  - parked:g7.16.2\n  - keep-me\n---\nbody\n", "utf-8")
    wp = Path(__file__).resolve().parents[1] / "bin" / "write.py"
    r = subprocess.run([sys.executable, str(wp), "config:formations", "set active doc:two-step",
                        "--actor", "test", "--role", "director"], cwd=groot.parent,
                       capture_output=True, text=True, timeout=120,
                       env={k: v for k, v in os.environ.items() if not k.startswith(("TMUX", "AGI_"))})
    assert r.returncode == 0, r.stderr[-400:]
    text = f.read_text("utf-8")
    assert "parked:g7.16.2" not in text and "keep-me" in text


# --- goal:g7.16.1.2.8 · hypothesis:formations-are-one-registry-with-one-home
# The LIVE registry (a corpus row, like the thought-hygiene corpus test): every
# registered template maps to a goal and lives in the one formations home.
# Strict xfail: RED on the trunk at 82d64ffe7 -- 4 of 6 map to "", and
# doc:council-loop sits under nodes/doc/ (council bundle 2, director-general-2).
@pytest.mark.xfail(strict=True, reason="hypothesis:formations-are-one-registry-with-one-home")
def test_the_live_registry_maps_every_template_to_a_goal_in_one_home():
    import locations, node_writer, yaml
    root = locations.find_project_root(Path(__file__).resolve())
    if root is None:
        pytest.skip("not running inside an agi project checkout")
    cell = node_writer.find_node_file(root, "config:formations")
    fm = yaml.safe_load(cell.read_text("utf-8").split("---", 2)[1])
    table = fm.get("templates") or {}
    assert table and all(str(g).startswith("g") for g in table.values()), table
    home = root / "nodes" / ".geometry" / "formations"
    for doc in table:
        path = node_writer.find_node_file(root, doc)
        assert path is not None and path.parent == home, doc
