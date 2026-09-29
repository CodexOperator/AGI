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
    _cell(groot, "doc:council-loop")
    r = verification.check_formation(groot)
    assert (r.status, r.number) == ("PASS", {"wake": 0})
