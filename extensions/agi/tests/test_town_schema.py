"""g15 round I-3b — the [town] schema file itself (hypothesis:l4-a-town-is-a-
super-node-whose-cells-derive-its-branch-names).

Proves the schema loaded through the engine's reader ships the ruling's shape:
  * fields  visions / council / season / season_history / written_by, each with
    a {type: …} mirroring [config].md;
  * validation.required = [visions, council, season];
  * written_by = [prime_director, owner]  (town rows are prime/owner-written);
  * the schema REFUSES `branches:` as a cell BY NAME, and says so in the body
    (branches is DERIVED, never a cell);
  * the spawn parent shape admits exactly one ladder parent.
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


def _town_schema():
    from graph_core.persistence import load_node_file
    import locations
    root = locations.find_project_root(Path(__file__))
    assert root is not None
    p = Path(root) / "context" / "schemas" / "[town].md"
    if not p.exists():
        pytest.skip("no [town].md schema in this tree")
    return load_node_file(p, body=True)


def test_schema_has_town_cells(engine_on_path):
    nf = _town_schema()
    fm = nf.frontmatter
    assert fm["name"] == "town"
    assert set(fm["fields"]) >= {"visions", "council", "season",
                                 "season_history", "written_by"}
    assert fm["fields"]["visions"]["type"] == "list"
    assert fm["fields"]["council"]["type"] == "str"
    assert fm["fields"]["season"]["type"] == "int"
    assert fm["fields"]["season_history"]["type"] == "list"


def test_schema_required_and_written_by(engine_on_path):
    nf = _town_schema()
    fm = nf.frontmatter
    assert fm["validation"]["required"] == ["visions", "council", "season"]
    assert fm["written_by"] == ["prime_director", "owner"]


def test_schema_refuses_branches_cell(engine_on_path):
    """`branches:` is DERIVED, never a cell — the schema declares the refusal
    (fields block + body) and towns.py enforces it at read time."""
    nf = _town_schema()
    fm = nf.frontmatter
    branches = fm["fields"].get("branches")
    assert branches is not None, "schema must declare branches: to refuse it"
    assert "DERIVED" in str(branches) or "derived" in str(branches)
    # The refusal is stated in the schema body too, so nobody re-adds it.
    assert "REFUSE" in nf.body.upper() or "refuses" in nf.body
    assert "DERIVED, NEVER a cell" in nf.body


def test_schema_spawn_takes_one_ladder_parent(engine_on_path):
    nf = _town_schema()
    spawn = nf.frontmatter["spawn"]
    assert spawn["allowed_parents"] == ["ladder"]
    assert spawn["min_parents"] == 1
    assert spawn["max_parents"] == 1