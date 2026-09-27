"""Storage categories are CONFIG cells; the resolver is only their reader.

`hypothesis:mint-offers-storage-categories-from-config-cells` (goal:g4.18.1.3).

Every test here builds its own temp project under `tmp_path` and writes a temp
config. The live config is never written by a test, and never read as a list:
the live table is a *shape* check, the behaviour check is the temp one.
"""
from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import locations  # noqa: E402


def _cell(location: str, prefix: str, label: str) -> dict:
    return {"location": location, "prefix": prefix, "label": label}


def _seeded() -> dict:
    """The table as the hypothesis names it, insertion order preserved."""
    return {"mint": {"storage_categories": {
        "engine_code": _cell("source_root", "extensions/agi/bin", "engine code"),
        "tests": _cell("source_root", "extensions/agi/tests", "tests"),
        "skills": _cell("source_root", "skills", "skills"),
        "geometry": _cell("graph_root", "nodes/.geometry", ".geometry config"),
        "schemas": _cell("graph_root", "context/schemas", "schemas"),
        "context_templates": _cell("graph_root", "context", "context templates"),
    }}}


def _project(tmp_path: Path, cfg: dict) -> Path:
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
    return root


def _cli(root: Path, *extra: str) -> list[str]:
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = locations.main([str(root), "--storage-categories", *extra])
    assert rc == 0, f"locations.py --storage-categories exited {rc}"
    return [ln for ln in buf.getvalue().splitlines() if ln.strip()]


# --- conjunct 1: the table is a config cell ---------------------------------

def test_live_config_seeds_the_named_categories():
    cfg = json.loads((REPO / ".agi" / "config.json").read_text(encoding="utf-8"))
    rows = locations.storage_categories(cfg)
    keys = [r["key"] for r in rows]
    for want in ("engine_code", "tests", "skills", "geometry", "schemas",
                 "context_templates"):
        assert want in keys, f"live config is missing category {want!r}: {keys}"


def test_every_live_location_is_a_name_payload_base_accepts(tmp_path):
    cfg = json.loads((REPO / ".agi" / "config.json").read_text(encoding="utf-8"))
    root = REPO / ".agi"
    for row in locations.storage_categories(cfg):
        # raises KeyError if the name is not one payload_base knows
        assert locations.payload_base(root, row["location"], cfg) is not None


def test_numbering_follows_cell_order_not_alphabet(tmp_path):
    cfg = {"mint": {"storage_categories": {
        "zzz": _cell("source_root", "z", "z"), "aaa": _cell("source_root", "a", "a"),
    }}}
    rows = locations.storage_categories(cfg)
    assert [r["key"] for r in rows] == ["zzz", "aaa"]
    assert [r["n"] for r in rows] == [1, 2]


# --- conjunct 2: one resolver, pick + tail -> (location, payload_ref) --------

def test_pick_by_number_and_by_key_agree():
    cfg = _seeded()
    by_n = locations.resolve_storage_category("3", "mvp-x.md", cfg)
    by_k = locations.resolve_storage_category("skills", "mvp-x.md", cfg)
    assert (by_n["location"], by_n["payload_ref"]) == ("source_root",
                                                        "skills/mvp-x.md")
    assert by_n["custom"] is False and by_k["payload_ref"] == by_n["payload_ref"]


def test_tail_joins_under_the_prefix_without_a_double_slash():
    cfg = _seeded()
    row = locations.resolve_storage_category("tests", "/test_x.py", cfg)
    assert row["payload_ref"] == "extensions/agi/tests/test_x.py"
    assert row["location"] == "source_root"


def test_custom_path_is_flagged_never_raised():
    row = locations.resolve_storage_category("docs/other/thing.md", None, _seeded())
    assert row["custom"] is True
    assert row["payload_ref"] == "docs/other/thing.md"
    assert row["location"] == locations.DEFAULT_PAYLOAD_LOCATION


def test_pick_outside_the_table_is_flagged_custom_not_raised():
    for pick in ("99", "no_such_category"):
        row = locations.resolve_storage_category(pick, None, _seeded())
        assert row["custom"] is True, pick


def test_resolver_carries_no_storage_path_literal():
    src = inspect.getsource(locations.storage_categories) + \
        inspect.getsource(locations.resolve_storage_category)
    for bad in ('"extensions/', '"skills/', '".agi/', '"context/',
                "'.geometry'"):
        assert bad not in src, f"storage path literal {bad!r} in the resolver"


# --- conjunct 3: one CLI line; one new cell = one new option ----------------

def test_one_extra_cell_adds_exactly_one_option(tmp_path):
    base = _project(tmp_path / "a", _seeded())
    before = _cli(base)

    extended = _seeded()
    extended["mint"]["storage_categories"]["extra_thing"] = _cell(
        "repo_root", "elsewhere", "extra")
    after = _cli(_project(tmp_path / "b", extended))

    assert len(after) == len(before) + 1
    assert [ln.split()[1] for ln in after][-1] == "extra_thing"
    # the existing options are untouched: no code edit, no renumbering
    assert [ln.split()[1] for ln in after[:-1]] == [ln.split()[1] for ln in before]


def test_cli_prints_a_picked_row(tmp_path):
    root = _project(tmp_path, _seeded())
    out = _cli(root, "--storage-pick", "schemas", "--tail", "hyp.md")
    assert len(out) == 1
    assert out[0].split("\t") == ["schemas", "graph_root",
                                  "context/schemas/hyp.md"]


def test_cli_resolver_location_is_accepted_by_payload_base(tmp_path):
    cfg = _seeded()
    root = _project(tmp_path, cfg)
    for row in locations.storage_categories(cfg):
        assert locations.payload_base(root, row["location"], cfg) is not None


# --- falsifier 4: the resolver never returns a name payload_base refuses ---

def test_bad_cell_location_is_refused_by_name_not_passed_through():
    """The falsifier the parent review said FIRES, closed."""
    cfg = {"mint": {"storage_categories": {
        "tests": _cell("source_root", "t", "tests"),
        "typo": _cell("no_such_place", "b", "typo"),
    }}}
    try:
        row = locations.resolve_storage_category("typo", "x.py", cfg)
    except ValueError as exc:
        msg = str(exc)
        assert "typo" in msg and "no_such_place" in msg, msg
    else:
        raise AssertionError(f"resolver returned an unvalidatable row: {row}")


def test_no_row_of_any_table_carries_a_name_payload_base_refuses(tmp_path):
    """The property, over the bad cell AND a pick by number."""
    cfg = {"mint": {"storage_categories": {
        "ok": _cell("source_root", "a", "ok"),
        "typo": _cell("no_such_place", "b", "typo"),
    }}, "locations": {"extra_root": "rel/dir"}}
    root = _project(tmp_path, cfg)
    known = locations.known_payload_locations(cfg)
    assert known[-1] == "extra_root"
    for row in locations.storage_categories(cfg):
        assert row["location_ok"] is (row["location"] in known)
    for pick in ("typo", "2"):
        try:
            row = locations.resolve_storage_category(pick, "x.py", cfg)
        except ValueError:
            continue
        assert locations.payload_base(root, row["location"], cfg)


def test_a_declared_locations_cell_makes_a_bad_cell_acceptable(tmp_path):
    """Fix the config, not the code: the option becomes resolvable."""
    cfg = {"mint": {"storage_categories": {
        "docs": _cell("docset", "notes", "docs")}},
        "locations": {"docset": "notes"}}
    row = locations.resolve_storage_category("docs", "a.md", cfg)
    assert row["location"] == "docset" and row["custom"] is False
    assert (locations.payload_base(_project(tmp_path, cfg), "docset", cfg)
            / row["payload_ref"]).name == "a.md"


# --- the target, not just the name -------------------------------------------

def test_target_exists_is_none_without_a_root_and_a_bool_with_one(tmp_path):
    cfg = _seeded()
    assert all(r["target_exists"] is None
               for r in locations.storage_categories(cfg))
    root = _project(tmp_path, cfg)
    for row in locations.storage_categories(cfg, root):
        assert isinstance(row["target_exists"], bool)
        assert row["target_exists"] == (
            locations.storage_category_target(root, row, cfg).is_dir())


def test_a_good_name_with_a_mistyped_prefix_is_stamped_missing(tmp_path):
    """The residue: `location_ok` is a NAME check, so a cell can pass it and
    still point nowhere. A temp project creates only the two directories."""
    cfg = _seeded()
    root = _project(tmp_path, cfg)
    (root / "extensions" / "agi" / "bin").mkdir(parents=True)
    rows = {r["key"]: r for r in locations.storage_categories(cfg, root)}
    assert rows["engine_code"]["location_ok"] is True
    assert rows["engine_code"]["target_exists"] is True
    missing = [k for k, r in rows.items() if not r["target_exists"]]
    assert "engine_code" not in missing and len(missing) == 5, missing


def test_the_cli_marks_a_row_whose_target_is_missing(tmp_path):
    # the CLI resolves the graph root itself, so the graph-located prefixes
    # live under <proj>/.agi here, not under <proj>.
    cfg = _seeded()
    root = _project(tmp_path, cfg)
    (root / ".agi" / "context").mkdir(parents=True)
    out = _cli(root)
    for line in out:
        assert ("MISSING" in line) == (line.split()[1] != "context_templates"), line


def test_a_resolved_pick_carries_the_stamp_and_a_custom_row_does_not_claim_one(
        tmp_path):
    cfg = _seeded()
    root = _project(tmp_path, cfg)
    (root / "context").mkdir(parents=True)
    hit = locations.resolve_storage_category("context_templates", "a.md", cfg,
                                             root)
    assert hit["target_exists"] is True
    assert locations.resolve_storage_category(
        "nowhere/at/all.md", config=cfg, root=root)["target_exists"] is None


def test_live_seeded_cells_all_point_at_a_directory_that_exists():
    """Every option the live picker offers is usable in THIS checkout."""
    root = locations.find_project_root(REPO)
    cfg = locations.load_config(root)
    rows = locations.storage_categories(cfg, root)
    assert rows and all(r["target_exists"] for r in rows), [
        (r["key"], r["location"], r["prefix"])
        for r in rows if not r["target_exists"]]


def test_storage_category_target_agrees_with_the_write_path(tmp_path):
    cfg = _seeded()
    root = _project(tmp_path, cfg)
    row = locations.storage_categories(cfg)[1]
    want = locations.resolve_payload_path(root, row["prefix"], row["location"],
                                          cfg)
    assert locations.storage_category_target(root, row, cfg) == want
