"""goal:g15.25 SM.32 claim (4) — readers treat rows by their REAL town.

Until the Prime's 0a town-cell lines land one row per rotation boundary, the
six director rows still spell `town: all`. Readers must treat EVERY
perpetual post row — the keep (sanctuary-master, master-sensei,
sensei-director) AND the prime + point + review (belam, sanctuary-director,
sanctuary-helper) — as `sanctuary` NOW (owner ruling relayed 2026-09-16
18:12Z: a perpetual agent post's HOME town is sanctuary by definition; the
PROJECT town it builds on is the branch prefix, a separate axis) — through
`towns.row_town`, whose transitional map is DATA in the
`[config]` schema, never a literal town name in `bin/*.py`
(`test_no_literal_town.py`). A declared cell always wins over the map, so the
reader self-retires as the cells move.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

LIVE_SCHEMA = (Path(__file__).resolve().parents[3] / ".agi" /
               "context" / "schemas" / "[config].md")

#: name -> the REAL town the reader must report while the cell is `all`.
EXPECTED = {
    "sanctuary-master": "sanctuary",
    "master-sensei": "sanctuary",
    "sensei-director": "sanctuary",
    "belam": "sanctuary",
    "sanctuary-director": "sanctuary",
    "sanctuary-helper": "sanctuary",
}


def _write_posts_node(project, rows):
    d = project / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    body = "\n".join(f"  - {json.dumps(r)}" for r in rows)
    (d / "posts.md").write_text(
        "---\nid: config:posts\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nparents:\n  - goal:g17\nposts:\n" + body +
        "\n---\n\n# config:posts\n\nfixture body\n", encoding="utf-8")


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    agi = tmp_path / ".agi"
    agi.mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    sd = agi / "context" / "schemas"
    sd.mkdir(parents=True)
    (sd / "[config].md").write_text(LIVE_SCHEMA.read_text(encoding="utf-8"))
    rows = [{"name": n, "role": "director", "town": "all"} for n in EXPECTED]
    _write_posts_node(agi, rows)
    return agi


def test_row_town_resolves_the_six_rows_while_cell_says_all(project):
    """The keep rows read sanctuary; prime + point + review read core."""
    import towns
    rows = {
        "sanctuary-master": {"name": "sanctuary-master", "town": "all"},
        "master-sensei": {"name": "master-sensei", "town": "all"},
        "sensei-director": {"name": "sensei-director", "town": "all"},
        "belam": {"name": "belam", "town": "all"},
        "sanctuary-director": {"name": "sanctuary-director", "town": "all"},
        "sanctuary-helper": {"name": "sanctuary-helper", "town": "all"},
    }
    for name, row in rows.items():
        assert towns.row_town(project, row) == EXPECTED[name], name


def test_row_town_never_returns_all(project):
    """`all` is retired: it is never returned as a town."""
    import towns
    assert towns.row_town(project, {"name": "belam", "town": "all"}) != "all"


def test_declared_cell_wins_over_the_transitional_map(project):
    """Once a row's real cell lands, the cell wins — the map self-retires."""
    import towns
    row = {"name": "belam", "town": "streaming-suite"}
    assert towns.row_town(project, row) == "streaming-suite"
    # a row not in the map still resolves its declared cell
    assert towns.row_town(
        project, {"name": "council-core", "town": "core"}) == "core"


def test_seat_status_carries_the_row_town(project):
    """`seat_status.collect` reports each row's REAL town."""
    import seat_status
    view = seat_status.collect(project, {})
    by_name = {s["name"]: s for s in view.seats}
    for name, town in EXPECTED.items():
        assert by_name[name]["town"] == town, name


def test_keep_view_frame_carries_the_row_town(project):
    """`viewport.sanctuary_frame` groups the rows by that same town."""
    import viewport
    import seat_status
    rows = seat_status.collect(project, {}).seats
    scene = viewport.sanctuary_frame(rows, [], None)
    got = {r["name"]: r["town"] for r in list(scene.spirits) + list(scene.probes)}
    for name, town in EXPECTED.items():
        assert got[name] == town, name


def test_audience_quorum_still_resolves_from_a_director_row(tmp_path):
    """A director row's `audience quorum` ask still lands — no town gate on it."""
    import send as send_mod
    comms = tmp_path / "comms"
    path = send_mod.audience_quorum(comms, "who owns the keep?",
                                    "sanctuary-director")
    assert path == comms / "room" / "quorum-requests.md"
    text = path.read_text()
    assert "[ask] who owns the keep?" in text
    assert "from: sanctuary-director" in text


def test_rename_boundary_never_derives_a_branch_from_the_row_town(project):
    """SM.62: the rename surface's branch is the REAL local ref, never a
    town spelled from the row home town. A fixture with no readable local
    refs has NO branch surface at all -- the derived-spelling fallback is
    DELETED, so `towns.row_town` no longer feeds the branch spelling on this
    path (it is read for the new-name home-town refusal, and nothing else)."""
    import rotate
    _write_posts_node(project, [
        {"name": "belam", "role": "director", "town": "all"},
        {"name": "declared-post", "role": "director", "town": "sanctuary"},
    ])
    for old in ("belam", "declared-post"):
        kinds = {s["kind"] for s in
                 rotate._rename_surfaces(project, old, old + "2")}
        assert "branch" not in kinds, kinds
        assert "branch (origin)" not in kinds, kinds
