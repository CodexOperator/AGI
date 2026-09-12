"""g15 round I-3b — towns.py loader: the town super node (hypothesis:l4-a-
town-is-a-super-node-whose-cells-derive-its-branch-names).

Proves on FIXTURE graphs (a tmp_path .agi/, never the live tree):
  * the three create lines mint three town nodes that `load_towns` reads back;
  * `town_tuples` returns
      [{core,2,2,council-core}, {streaming-suite,1,2,council-streaming-suite},
       {web-app-suite,1,2,council-web-app-suite}]
    (season = the town's OWN counter, global_season = the fixture ladder's);
  * each of the four refusals fires BY NAME (no visions / council no posts row
    / vision claimed by two towns / a `branches:` cell);
  * `visions: auto` resolves to every vision node no other town claims;
  * the DERIVED branch names equal the ruling's literal table.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import towns


def _write(root: Path, rel: str, content: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def _fm_cell(rows) -> str:
    return "\n".join(f"  - {json.dumps(r)}" for r in rows)


def _ladder():
    return (
        "---\nid: ladder:ladder\n"
        "current_season: 2\n"
        "towns: [core, streaming-suite, web-app-suite]\n"
        "---\nbody\n"
    )


def _choice_vision(vid, title="Vision"):
    return (
        f"---\nid: {vid}\n"
        f"type: vision\ntitle: {json.dumps(title)}\nseason: 2\nstatus: open\n---\n"
        "body\n"
    )


def _town_node(slug, visions, council, season, mint="mint-" + "x" * 12, extra=""):
    vs = json.dumps(visions) if isinstance(visions, list) else json.dumps(visions)
    return (
        f"---\nid: town:{slug}\ntype: town\nmint_id: {mint}_{slug}\n"
        f"visions: {vs}\ncouncil: {json.dumps(council)}\nseason: {season}\n"
        f"season_history: [{{season: 1, global_season: 1, opened: '2026-09-01', closed: ''}}]\n"
        + extra
        + "---\nbody\n"
    )


def _graph(root: Path, visions=("vision:a", "vision:b", "vision:c")) -> Path:
    """A fixture GRAPH ROOT (the dir holding nodes/ directly, like the .agi/
    graph dir): ladder + council posts + 3 vision nodes. Returns the graph root."""
    g = root / ".agi"
    _write(g, "nodes/.geometry/ladder.md", _ladder())
    rows = [
        {"name": "council-core", "role": "council", "town": "core"},
        {"name": "council-streaming-suite", "role": "council", "town": "streaming-suite"},
        {"name": "council-web-app-suite", "role": "council", "town": "web-app-suite"},
    ]
    _write(g, "nodes/.geometry/posts.md",
           f"---\nid: config:posts\nposts:\n{_fm_cell(rows)}\n---\n")
    for v in visions:
        _write(g, f"nodes/vision/{v.split(':')[-1]}.md", _choice_vision(v))
    return g


def _three_towns(g):
    """Mint the three real towns per the create lines (the DELIVERABLE)."""
    _write(g, "nodes/town/core.md",
           _town_node("core", ["vision:a", "vision:b", "vision:c"], "council-core", 2))
    _write(g, "nodes/town/streaming-suite.md",
           _town_node("streaming-suite", ["vision:streaming-suite"],
                      "council-streaming-suite", 1,
                      extra="town: streaming-suite\n"))
    _write(g, "nodes/town/web-app-suite.md",
           _town_node("web-app-suite", ["vision:web-app-suite"],
                      "council-web-app-suite", 1,
                      extra="town: web-app-suite\n"))


def test_three_create_lines_load_and_tuples(tmp_path):
    g = _graph(tmp_path)
    _three_towns(g)
    loaded = towns.load_towns(g)
    by = {t.slug: t for t in loaded}
    assert set(by) == {"core", "streaming-suite", "web-app-suite"}
    assert by["core"].season == 2
    assert by["streaming-suite"].council == "council-streaming-suite"
    assert sorted(by["core"].visions) == ["vision:a", "vision:b", "vision:c"]

    rows = towns.town_tuples(g)
    assert rows == [
        {"town": "core", "season": 2, "global_season": 2, "council": "council-core"},
        {"town": "streaming-suite", "season": 1, "global_season": 2,
         "council": "council-streaming-suite"},
        {"town": "web-app-suite", "season": 1, "global_season": 2,
         "council": "council-web-app-suite"},
    ]


def test_derive_names_equal_ruling_table():
    # The ruling's literal table for core: the derived names fall out of the
    # cells (season 2, post name, round/agent). Prefer branches.derive_names
    # when the parallel I-3a round lands it; else the town's own loader half.
    try:
        from branches import derive_names as _branches_derive  # type: ignore
    except (ImportError, AttributeError):
        _branches_derive = None
    derive = _branches_derive if _branches_derive is not None else towns.derive_names
    got = derive("core", 2, post="belam", loop_round="R7", agent="a00-1234")
    assert got == [
        "core/main",
        "core/season2/main",
        "core/season2/posts/belam/main",
        "core/season2/posts/belam/loops/R7/a00-1234",
    ]
    # A town's own Council main (no post/loop layers) — the base pair.
    assert towns.derive_names("core", 2) == ["core/main", "core/season2/main"]


def test_refusal_no_visions(tmp_path):
    g = _graph(tmp_path)
    _write(g, "nodes/town/core.md",
           _town_node("core", [], "council-core", 2))
    with pytest.raises(towns.TownError) as e:
        towns.load_towns(g)
    assert "no visions" in str(e.value) and "core" in str(e.value)


def test_refusal_council_no_posts_row(tmp_path):
    g = _graph(tmp_path)
    _write(g, "nodes/town/core.md",
           _town_node("core", ["vision:a"], "no-such-council", 2))
    with pytest.raises(towns.TownError) as e:
        towns.load_towns(g)
    assert "council names no config:posts row" in str(e.value)
    assert "town:core" in str(e.value)


def test_refusal_vision_claimed_by_two_towns(tmp_path):
    g = _graph(tmp_path)
    _write(g, "nodes/town/core.md",
           _town_node("core", ["vision:a", "vision:b"], "council-core", 2))
    _write(g, "nodes/town/streaming-suite.md",
           _town_node("streaming-suite", ["vision:a"], "council-streaming-suite", 1))
    with pytest.raises(towns.TownError) as e:
        towns.load_towns(g)
    assert "claimed by two towns" in str(e.value)
    assert "vision:a" in str(e.value)


def test_refusal_branches_cell_present(tmp_path):
    g = _graph(tmp_path)
    # A `branches:` cell is DERIVED, never a cell — refused BY NAME.
    node = _town_node("core", ["vision:a"], "council-core", 2,
                      extra="branches: [core/main]\n")
    _write(g, "nodes/town/core.md", node)
    with pytest.raises(towns.TownError) as e:
        towns.load_towns(g)
    assert "DERIVED, never a cell" in str(e.value)
    assert "branches" in str(e.value)


def test_auto_resolves_unclaimed_visions(tmp_path):
    g = _graph(tmp_path, visions=("vision:a", "vision:b", "vision:c"))
    # streaming-suite claims vision:a and vision:b; core uses `auto`.
    _write(g, "nodes/town/core.md",
           _town_node("core", "auto", "council-core", 2))
    _write(g, "nodes/town/streaming-suite.md",
           _town_node("streaming-suite", ["vision:a", "vision:b"],
                      "council-streaming-suite", 1))
    loaded = towns.load_towns(g)
    by = {t.slug: t for t in loaded}
    assert by["core"].visions_was_auto is True
    # auto = every vision node no other town claims = vision:c
    assert by["core"].visions == ["vision:c"]


def test_deprecated_sibling_still_read(tmp_path):
    """A reader that stops seeing a retired town fails quietly — the loader
    must read nodes/deprecated/town/ live-first after nodes/town/."""
    g = _graph(tmp_path, visions=("vision:a",))
    _write(g, "nodes/deprecated/town/core.md",
           _town_node("core", ["vision:a"], "council-core", 1,
                      mint="oldmint-aaaaaaaaaaaa"))
    loaded = towns.load_towns(g)
    assert [t.slug for t in loaded] == ["core"]
    t = loaded[0]
    assert t.mint_id.startswith("oldmint")
    assert t.council == "council-core"

def test_cli_imports_outside_pytest_and_accepts_either_root(tmp_path):
    """Director regression (L4.333 harvest): the merged towns.py imported
    graph_core without the bin modules' sys.path inserts, so
    `python3 extensions/agi/bin/towns.py <root> --tuples` raised
    ModuleNotFoundError outside pytest; and a project root (the dir holding
    .agi/) read as "no towns" instead of resolving to its graph dir."""
    import subprocess
    import sys as _sys
    g = _graph(tmp_path)
    _three_towns(g)
    cli = Path(towns.__file__).resolve()
    for root in (g, tmp_path):
        r = subprocess.run([_sys.executable, str(cli), str(root), "--tuples"],
                           capture_output=True, text=True, cwd=str(tmp_path),
                           env={"PATH": "/usr/bin:/bin"})
        assert r.returncode == 0, r.stderr
        assert "'town': 'core'" in r.stdout and "'season': 2" in r.stdout
    assert towns.town_tuples(tmp_path) == towns.town_tuples(g)
