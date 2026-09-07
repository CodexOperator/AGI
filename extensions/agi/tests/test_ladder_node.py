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
    # The live ladder rolls over (season 1 -> 2 on 2026-09-07); the test pins
    # the shape, not the season number: a positive int, and every named
    # (closed) season lies strictly before the current one.
    cs = nf.frontmatter["current_season"]
    assert isinstance(cs, int) and cs >= 1
    names = nf.frontmatter.get("season_names") or {}
    assert all(int(k) < cs for k in names), (cs, names)


def test_ladder_node_director_rotate_at(engine_on_path):
    nf = _ladder_node_file()
    assert nf.frontmatter["director_rotate_at"] == 0.35


def test_ladder_node_has_four_tiers(engine_on_path):
    nf = _ladder_node_file()
    assert [t["tier"] for t in nf.frontmatter["tiers"]] == [0, 1, 2, 3]


def test_ladder_node_declares_roles_table(engine_on_path):
    """hypothesis:l3w0-ladder-roles-table — the ladder node must declare a
    roles table (tier x role -> harness, model, effort, settings)."""
    rows = _ladder_node_file().frontmatter.get("roles")
    assert isinstance(rows, list) and rows, "ladder declares an empty roles table"
    prime = next(r for r in rows
                 if r.get("tier") == 3 and r.get("role") == "prime_director")
    assert prime.get("harness") == "claude-code"
    assert prime.get("model") == "claude-fable-5-1"
    assert prime.get("effort") == "max"
    assert prime.get("settings") == "ultracode"
    # every role the graph knows is resolvable through the table
    roles = {r.get("role") for r in rows}
    assert {"kid", "parent", "director", "prime_director"} <= roles


def test_ladder_node_declares_season_names(engine_on_path):
    """hypothesis:l3w0-ladder-roles-table — season 1 is named 'genesis' on
the ladder (written at rollover, looking back)."""
    fm = _ladder_node_file().frontmatter
    assert fm.get("season_names", {}).get(1) == "genesis"


def test_ladder_node_declares_mantles(engine_on_path):
    """hypothesis:l3w0-ladder-roles-table — the mantle (Belam) is declared on
the ladder, derived into heads, never hardcoded in brief.py."""
    fm = _ladder_node_file().frontmatter
    mantles = fm.get("mantles", {}) or {}
    assert mantles.get("prime_director") == "Belam"
