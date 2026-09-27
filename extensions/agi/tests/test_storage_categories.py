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
        "geometry": _cell("source_root", ".geometry", ".geometry config"),
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
