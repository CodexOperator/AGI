"""goal:g12.3 — the ladder node loads through the engine's node reader.

`hypothesis:l2w1-ladder-node`'s VERIFY section required one test that loads
`.agi/nodes/.geometry/ladder.md` through the engine's node reader and asserts
`current_season == 1` and `director_rotate_at == 0.35`. The kid
(experiment:a00-fc43bb62-4500f1) verified both inline but never added the
test; parent a00-0338943a supplied it on review (L2.01, 2026-09-06).
"""
from __future__ import annotations

from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
BIN_DIR = TESTS_DIR.parent / "bin"
SRC_DIR = TESTS_DIR.parent / "src"


@pytest.fixture()
def engine_on_path(monkeypatch):
    monkeypatch.syspath_prepend(str(BIN_DIR))
    monkeypatch.syspath_prepend(str(SRC_DIR))
    yield


def _ladder_node_file():
    import locations
    from graph_core.persistence import frontmatter

    root = locations.find_project_root(Path(__file__))
    assert root is not None, "no project root found from the test file"
    path = Path(root) / "nodes" / ".geometry" / "ladder.md"
    if not path.exists():
        pytest.skip("no .geometry/ladder.md in this tree (engine checkout without the graph)")
    return frontmatter.load_node_file(path)


def test_ladder_node_current_season(engine_on_path):
    nf = _ladder_node_file()
    assert nf.frontmatter["current_season"] == 1


def test_ladder_node_director_rotate_at(engine_on_path):
    nf = _ladder_node_file()
    assert nf.frontmatter["director_rotate_at"] == 0.35


def test_ladder_node_has_four_tiers(engine_on_path):
    nf = _ladder_node_file()
    assert [t["tier"] for t in nf.frontmatter["tiers"]] == [0, 1, 2, 3]
