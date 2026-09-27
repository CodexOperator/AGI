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

import pytest
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


def _run_cli(root: Path, *extra: str) -> tuple[list[str], str, int]:
    """`locations.py --storage-categories` as (stdout lines, stderr, rc).

    The rc is RETURNED and every caller asserts it: a caller that discards it
    leaves the exit code with no test at all."""
    import contextlib
    import io
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = locations.main([str(root), "--storage-categories", *extra])
    return ([ln for ln in out.getvalue().splitlines() if ln.strip()],
            err.getvalue(), rc)


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


def test_every_live_location_is_a_name_payload_base_accepts():
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
    """The live table, read off the real disk; this test creates NOTHING.

    It used to `mkdir` every target and then assert the targets exist -- an
    assertion that could not fail, so a typo in a live cell passed. A missing
    BASE root means a partial checkout, so that SKIPS naming the path."""
    live = json.loads((REPO / ".agi" / "config.json").read_text(encoding="utf-8"))
    for row in locations.storage_categories(live, REPO / ".agi"):
        base = locations.payload_base(REPO / ".agi", row["location"], live)
        if base is None or not base.is_dir():
            pytest.skip(f"partial checkout: {base} is not a directory")
        target = base / row["prefix"]
        assert target.is_dir(), (
            f"live cell mint.storage_categories.{row['key']}.prefix names "
            f"{row['prefix']!r}, which does not exist at {target}")


def test_a_typo_in_a_cell_value_is_reported_missing_not_created(tmp_path):
    """The check above has teeth only if a wrong prefix shows up as MISSING.
    The good target is created BY the test, the typo target is not."""
    cfg = {"mint": {"storage_categories": {
        "good": _cell("source_root", "extensions/agi/bin", "good"),
        "typo": _cell("source_root", "nodes/.TYPO-does-not-exist", "typo")}}}
    root = _project(tmp_path, cfg)
    (root / "extensions" / "agi" / "bin").mkdir(parents=True)
    rows = {r["key"]: r for r in locations.storage_categories(cfg, root)}
    assert rows["good"]["target_exists"] is True
    assert rows["typo"]["target_exists"] is False
    out = _cli(root)
    assert any("typo" in ln and "MISSING" in ln for ln in out), out
    assert not any(ln.split()[1] == "good" and "MISSING" in ln for ln in out)


def test_a_pick_without_the_list_flag_still_resolves(tmp_path):
    """The residue: --storage-pick used to print the default layout, exit 0,
    and resolve nothing. It implies the list flag now."""
    import contextlib
    import io
    cfg = _seeded()
    root = _project(tmp_path, cfg)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = locations.main([str(root), "--storage-pick", "2", "--tail",
                             "x.py"])
    assert rc == 0
    line = buf.getvalue().strip()
    assert line.split("\t") == ["tests", "source_root",
                                "extensions/agi/tests/x.py"], line
    assert "layout:" not in line


def test_a_tail_without_a_pick_is_refused_with_a_reason(tmp_path):
    import contextlib
    import io
    cfg = _seeded()
    root = _project(tmp_path, cfg)
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = locations.main([str(root), "--tail", "x.py"])
    assert rc == 1
    assert "--storage-pick" in err.getvalue()
    assert out.getvalue().strip() == ""


def test_storage_category_target_agrees_with_the_write_path(tmp_path):
    cfg = _seeded()
    root = _project(tmp_path, cfg)
    row = locations.storage_categories(cfg)[1]
    want = locations.resolve_payload_path(root, row["prefix"], row["location"],
                                          cfg)
    assert locations.storage_category_target(root, row, cfg) == want


def test_a_mistyped_block_is_an_empty_table_the_cli_names(tmp_path):
    """The READER stays TOTAL: printing it never raises.

    A hand-edited config that puts a list where the table belongs used to
    raise AttributeError -- so a pane could not LIST the options, and the one
    thing the block is for (seeing what the config says) was the thing that
    broke. But an empty table PRINTS NOTHING and exited 0: the very silence
    the round set out to remove. So: total reader, NAMED cell, non-zero rc.
    """
    for bad in (["a", "b"], "engine code", 7, None):
        cfg = {"mint": {"storage_categories": bad}}
        assert locations.storage_categories(cfg) == []
        out, err, rc = _run_cli(_project(tmp_path / str(bad), cfg))
        assert rc == 1, f"a mistyped block exited {rc}, not 1"
        assert out == []
        assert "mint.storage_categories" in err, err
        assert "not a table" in err, err
    # a mistyped `mint` is the same failure one level up
    cfg = {"mint": "not a table"}
    assert locations.storage_categories(cfg) == []
    out, err, rc = _run_cli(_project(tmp_path / "mint", cfg))
    assert rc == 1 and out == [] and err.startswith("ERR: mint is"), err


def test_the_cli_reports_a_broken_cell_and_still_prints_the_table(tmp_path):
    """A table with a row `location_ok is False` is the one place a pane can
    learn the config is broken -- it used to report SUCCESS there."""
    cfg = _seeded()
    cfg["mint"]["storage_categories"]["typo"] = _cell("nope_not_a_base", "", "t")
    out, err, rc = _run_cli(_project(tmp_path, cfg))
    assert rc == 1, "a broken cell reported success to the shell"
    assert any("typo" in ln and "BAD LOCATION" in ln for ln in out), out
    assert err.startswith("ERR: ") and "typo" in err and "nope_not_a_base" in err
    # a well-formed table keeps rc 0 and a silent stderr
    out_g, err_g, rc_g = _run_cli(_project(tmp_path / "good", _seeded()))
    assert rc_g == 0, f"a well-formed table exited {rc_g}, not 0"
    assert err_g == "" and len(out_g) == 6, (out_g, err_g)


def test_the_two_accepted_name_lists_are_one():
    """One source per rule: the write path's advice and the picker's advice
    must be the same list, or a pane is told one thing and the write path
    another for the same config."""
    cfg = {"locations": {"zeta": "/z", "alpha": "/a", "repo_root": "/r"}}
    shared = locations.known_payload_locations(cfg)
    with pytest.raises(KeyError) as ei:
        locations.payload_base(Path(__file__).resolve().parents[3], "nope", cfg)
    named = ei.value.args[0].split("use one of: ")[1].rstrip(".")
    assert [n.strip() for n in named.split(",")] == shared
    assert shared == ["source_root", "graph_root", "repo_root", "zeta", "alpha"]


def test_a_mistyped_cell_keeps_its_number_instead_of_vanishing():
    """A cell that is not a mapping used to be `continue`d, so every row below
    it renumbered: "pick 3" then named a different category than the list a
    pane was shown. The bad cell is VISIBLE, keeps its number, and is refused
    by name."""
    cfg = {"mint": {"storage_categories": {
        "engine_code": _cell("source_root", "extensions/agi/bin", "engine"),
        "geometry_typo": "nodes/.geometry",          # not a mapping
        "schemas": _cell("graph_root", "context/schemas", "schemas"),
    }}}
    rows = locations.storage_categories(cfg)
    assert [r["key"] for r in rows] == ["engine_code", "geometry_typo",
                                       "schemas"]
    assert [r["n"] for r in rows] == [1, 2, 3], "a dropped cell renumbers"
    bad = rows[1]
    assert bad["location_ok"] is False
    assert "nodes/.geometry" in bad["location"]
    assert rows[2]["location_ok"] is True
    # and it is refused by name, not resolved to something
    with pytest.raises(ValueError) as ei:
        locations.resolve_storage_category("2", "a.md", cfg)
    assert "geometry_typo" in str(ei.value)


def test_a_location_name_whose_value_payload_base_refuses_is_not_offered():
    """`payload_base` takes a non-empty str and refuses the rest, so the
    picker's name list must too -- otherwise a category gets
    `location_ok: True` and is refused downstream by the write path."""
    cfg = {"locations": {"good": "/g", "blank": "   ", "as_list": ["/l"],
                         "as_dict": {"root": "/d"}},
           "mint": {"storage_categories": {
               "a": _cell("blank", "p", "blank"),
               "b": _cell("as_list", "p", "list"),
               "c": _cell("as_dict", "p", "dict"),
               "d": _cell("good", "p", "good")}}}
    known = locations.known_payload_locations(cfg)
    assert "good" in known
    for refused in ("blank", "as_list", "as_dict"):
        assert refused not in known, f"{refused!r} is not a location"
        with pytest.raises(KeyError):
            locations.payload_base(REPO, refused, cfg)
    ok = {r["key"]: r["location_ok"] for r in locations.storage_categories(cfg)}
    assert ok == {"a": False, "b": False, "c": False, "d": True}


def test_the_cli_prints_err_not_a_traceback_for_a_bad_location_pick(tmp_path):
    """The ValueError `resolve_storage_category` raises used to escape
    `main()`: a pane typing a mistyped cell got a Python traceback instead of
    the `ERR: ...` line every other branch prints."""
    import contextlib
    import io
    cfg = _seeded()
    cfg["mint"]["storage_categories"]["schemas"] = _cell("nope", "p", "bad")
    root = _project(tmp_path, cfg)
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = locations.main([str(root), "--storage-pick", "schemas", "--tail",
                             "a.md"])
    assert rc == 1
    assert "Traceback" not in err.getvalue()
    assert err.getvalue().startswith("ERR: ")
    assert "schemas" in err.getvalue() and "nope" in err.getvalue()
    assert out.getvalue().strip() == ""
