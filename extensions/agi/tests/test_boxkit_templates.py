"""The boxkit acceptance suite for
hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes.

Nine rows, one per clause of the claim:

1. every manifest row carries the KIT CONTRACT keys and a known dest_cell;
2. every piece renders with no {{UNFILLED}} surviving;
3. render() refuses an unfilled placeholder BY NAME;
4. no template byte carries a literal host token (owner user, home, repo root,
   guard source) or a literal cgroup UID -- anonymize.py CANNOT do this job
   (its classes are hostname/ip/mac/board/secret; see experiment:a00-5e1ed113 P4);
5. SIZING reproduces the measured knobs by TRUNCATION, never rounding;
6. each template IS the committed ANONYMIZED copy of the live bytes (for a
   new_bytes row -- no live file on any box yet -- the fixture is the template's
   own self-render, so the row is pinned either way);
7. the rendered bytes EQUAL the live bytes on a box that has the guard
   (skipped, not silently passed, where the live file is absent) -- with the
   identity tokens the KIT derives from the running engine checkout and the
   committed paths.boxkit.guard_dir cell, never tokens the test injects;
7b. the identity roots are DERIVED, not cells: repo_root comes from the engine's
   own __file__ (through a linked worktree's .git FILE, no git subprocess) and
   guard_dir from the committed cell -- and the per-box inputs are ARGUMENTS,
   refused BY NAME when absent;
7c. every manifest dest_cell resolves against the COMMITTED config (the
   user_systemd_data_dir debt is closed: the director committed that cell);
8. install() writes only under a tmp install_root, with the manifest mode;
9. a row whose bytes do not exist on this box is flagged new_bytes;
10. the manifest covers EVERY unit goal:g7.33.18's no-cascade row names, read from
   the LIVE goal node (never a copied list), and a unit with no live drop-in on
   this box is a NAMED skip, never a silent pass.

Reads: config cells, the per-box measurement fixture, and the live files (read-only).
Writes: tmp_path only.
"""
from __future__ import annotations

import importlib.util
import json
import os
import pwd
import re
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parents[1] / "boxkit"
TEMPLATES = KIT / "templates"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "boxkit"
PROJECT = Path(__file__).resolve().parents[3]
UID = str(os.getuid())
OWNER = pwd.getpwuid(os.getuid()).pw_name

# The per-box inputs are ARGUMENTS, never cells (director rule 5): local-town's
# measured /proc/meminfo, from a fixture, so the suite pins the sizing arithmetic
# without reading a live box. A box with no guard passes its own measurements.
MEASURED = {k: v for k, v in
            json.loads((FIXTURES / "measurements.json").read_text(encoding="utf-8")).items()
            if not k.startswith("_") and k != "box"}
CONTRACT_KEYS = {"name", "template", "dest_cell", "dest_rel", "mode", "sudo",
                 "reload", "placeholders"}


def _load():
    spec = importlib.util.spec_from_file_location("boxkit_render", KIT / "render.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = _load()
CFG = json.loads((PROJECT / ".agi" / "config.json").read_text(encoding="utf-8"))
CELLS = dict(CFG["paths"]["boxkit"])
MISSING_CELLS = sorted({p["dest_cell"] for p in R.manifest()["pieces"]} - set(CELLS))
# only for the leak check (a template must not carry a literal root); never a token source
LEAK_ROOTS = sorted({str(p) for p in [PROJECT] + list(Path(PROJECT).parents[1:3])})

# A probe identity: contract tests need SOME value for REPO_ROOT/GUARD_SRC to render
# at all, and a probe is not the answer -- the wire test below supplies nothing.
PROBE = {"OWNER_USER": "probe", "UID": "4242",
         "REPO_ROOT": "/probe/repo", "GUARD_SRC": "/probe/.sanctuary/guard/guard-init.sh"}


def _v(**over):
    o = dict(PROBE)
    o.update(over)
    return R.values(CFG, MEASURED, o)


PIECES = R.manifest()["pieces"]
BY_NAME = {p["name"]: p for p in PIECES}
LIVE = [p for p in PIECES if not p.get("new_bytes")]


# 1 -- manifest schema
@pytest.mark.parametrize("piece", PIECES, ids=[p["name"] for p in PIECES])
def test_manifest_row_is_contract_shaped(piece):
    assert CONTRACT_KEYS <= set(piece), sorted(CONTRACT_KEYS - set(piece))
    assert piece["dest_cell"] in CELLS, piece["dest_cell"]
    assert (TEMPLATES / piece["template"]).is_file()
    assert re.fullmatch(r"0[0-7]{3}", piece["mode"]), piece["mode"]
    assert piece["reload"] in ("system", "user", "none")
    assert isinstance(piece["placeholders"], list) and piece["placeholders"]
    # falsifier (c) both ways: no UNLISTED placeholder, no UNUSED manifest entry
    used = set(re.findall(r"\{\{([A-Z][A-Z0-9_]*)\}\}",
                          (TEMPLATES / piece["template"]).read_text(encoding="utf-8")))
    assert used == set(piece["placeholders"]), sorted(used ^ set(piece["placeholders"]))


# 2 -- every piece renders, nothing left unfilled
@pytest.mark.parametrize("piece", PIECES, ids=[p["name"] for p in PIECES])
def test_piece_renders_without_an_unfilled_placeholder(piece):
    out = R.rendered(piece, _v())
    assert "{{" not in out, piece["name"]
    assert out == R.rendered(piece, _v())


# 3 -- the refusal names the placeholder
def test_render_refuses_an_unfilled_placeholder_by_name():
    with pytest.raises(R.KitError) as err:
        R.render("MemoryMax={{NOT_A_CELL}}M", _v(), "probe")
    assert "NOT_A_CELL" in str(err.value)
    with pytest.raises(R.KitError) as err:
        R.destination(BY_NAME["agi-slice"], {}, _v())
    assert "user_systemd_data_dir" in str(err.value)
    # the per-box inputs are arguments, not cells: absent means refused BY NAME
    with pytest.raises(R.KitError) as err:
        R.values(CFG, {"MEM_TOTAL": 1})
    assert all(k in str(err.value) for k in ("SYS_RESERVE", "HELD_OUT", "SWAP_TOTAL"))


# 4 -- no literal host token in any template byte
@pytest.mark.parametrize("piece", PIECES, ids=[p["name"] for p in PIECES])
def test_template_carries_no_literal_host_token(piece):
    text = (TEMPLATES / piece["template"]).read_text(encoding="utf-8")
    leaks = [t for t in (OWNER, str(Path.home()), *LEAK_ROOTS, "/.sanctuary/")
             if t and t in text]
    assert not leaks, "%s leaks %s" % (piece["name"], leaks)
    # the UID may only arrive as a placeholder: no literal cgroup identity.
    assert not re.search(r"(user[@-]|UID=)%s\b" % UID, text), piece["name"]


# 5 -- SIZING reproduces the measured knobs, truncating
def test_sizing_reproduces_the_measured_knobs():
    v = _v()
    assert (v["USER_MAX"], v["USER_HIGH"], v["USER_SWAP"]) == ("7365M", "6628M", "2047M")
    assert (v["AGI_HIGH"], v["AGI_MAX"]) == ("4639M", "5155M")
    assert (v["WORK_HIGH"], v["WORK_MAX"]) == ("4178M", "4643M")
    mib = {k: int(v[k].rstrip("M")) for k in ("USER_MAX", "USER_HIGH", "USER_SWAP",
                                             "AGI_HIGH", "AGI_MAX", "WORK_HIGH", "WORK_MAX")}
    assert mib["USER_MAX"] == (MEASURED["MEM_TOTAL"] - MEASURED["SYS_RESERVE"]
                               - MEASURED["HELD_OUT"])
    # truncation, never rounding: int(0.70 * 7365) is 5155, round() would say 5156
    assert mib["AGI_MAX"] == int(0.70 * mib["USER_MAX"]) != round(0.70 * mib["USER_MAX"])


# 6 -- the template IS the committed anonymized copy of the live bytes
@pytest.mark.parametrize("piece", PIECES, ids=[p["name"] for p in PIECES])
def test_template_equals_the_anonymized_fixture(piece):
    fix = FIXTURES / (piece["name"] + ".fixture")
    assert fix.is_file(), fix
    assert (TEMPLATES / piece["template"]).read_text(encoding="utf-8") == fix.read_text(encoding="utf-8")


# 7 -- THE FALSIFIER: rendered bytes == the live bytes on this box, with the
# identity tokens the KIT derives. No candidate search, no injected root: a worktree
# is not the checkout the live kit came from, so a walk renders the wrong bytes in
# every worktree. This goes RED, naming the cell, until the director commits it.
@pytest.mark.parametrize("piece", LIVE, ids=[p["name"] for p in LIVE])
def test_rendered_bytes_equal_the_live_bytes(piece):
    v = R.values(CFG, MEASURED, R.host_tokens(CFG))
    dest = R.destination(piece, CELLS, v, "/")
    if not dest.is_file():
        pytest.skip("no live %s on this box (the kit is portable; nothing to falsify here)" % dest)
    assert R.rendered(piece, v) == dest.read_text(encoding="utf-8")


# 7b -- the identity roots are DERIVED (director rules 2 and 3), never cells: the repo
# is the running engine's checkout (resolved through a linked worktree's .git FILE,
# with no git subprocess) and the guard directory is the committed paths.boxkit.guard_dir
# cell, expanded at read time.
def test_host_tokens_derives_the_engine_checkout_and_the_guard_dir_cell():
    t = R.host_tokens(CFG)
    assert t["REPO_ROOT"] == str(R.engine_checkout())
    assert t["GUARD_SRC"] == str(R.expand(CELLS, CELLS["guard_dir"],
                                          R.engine_checkout()) / "guard-init.sh")
    assert t["UID"] == UID and t["OWNER_USER"] == OWNER
    # an explicit root is honoured (another box, a probe) and never silently re-derived
    assert R.host_tokens(CFG, repo_root="/probe/repo")["REPO_ROOT"] == "/probe/repo"
    assert R.host_tokens(CFG, guard_dir="/probe/guard")["GUARD_SRC"] == "/probe/guard/guard-init.sh"
    # repo_root / guard_root are NOT cells any more: a config that still carries them is ignored
    stale = json.loads(json.dumps(CFG))
    stale["values"].setdefault("boxkit", {}).update({"repo_root": "/wrong", "guard_root": "/wrong"})
    assert R.host_tokens(stale) == t
    assert not (KIT / "defaults.json").exists(), "defaults.json is a second source; delete it"


# 7c -- every dest_cell resolves against the COMMITTED config (the debt is closed)
def test_every_manifest_dest_cell_resolves_against_the_committed_config():
    assert not MISSING_CELLS, MISSING_CELLS
    assert CELLS["user_systemd_data_dir"] == "{home}/.local/share/systemd/user"


# 8 -- the fence: install writes only under the tmp install_root
def test_install_writes_under_a_tmp_install_root_only(tmp_path):
    out = R.install(LIVE, _v(), CELLS, tmp_path)
    assert len(out) == len(LIVE)
    for piece in LIVE:
        dest = out[piece["name"]]
        assert str(dest).startswith(str(tmp_path))
        assert dest.is_file() and dest.stat().st_mode & 0o777 == int(piece["mode"], 8)
    assert not (tmp_path / "etc" / "systemd" / "system" / "10-agi-survival.conf").exists()


# 9 -- a row with no live bytes on this box says so
def test_new_bytes_row_is_flagged_and_has_no_live_counterpart():
    row = BY_NAME["agi-survival-conf"]
    assert row["new_bytes"] is True
    assert not R.destination(row, CELLS, _v(), "/").exists()
    assert "OOMPolicy" in R.rendered(row, _v())


# 10 -- the no-cascade coverage closure (kid a00-057a8121, probe 5 of the previous
# round). The goal TABLE is the spec, read from the live node -- a copied list in
# this file is the exact defect the probe found.
GOAL = PROJECT / ".agi" / "nodes" / "goal" / "g7.33.18.md"


def _no_cascade_units():
    row = [ln for ln in GOAL.read_text(encoding="utf-8").splitlines()
           if ln.strip().startswith("| no cascade")]
    assert len(row) == 1, "goal:g7.33.18 must carry exactly one no-cascade row"
    col = [c for c in row[0].split("|") if " on " in c]
    assert len(col) == 1, col
    tail = col[0].split(" on ", 1)[1]
    return [u.strip().strip("`") for u in tail.split(",") if u.strip()]


def _drop_ins_for(unit):
    return [p for p in PIECES if p["dest_rel"].startswith(unit + ".service.d/")]


@pytest.mark.parametrize("unit", _no_cascade_units())
def test_manifest_covers_every_unit_the_goal_no_cascade_row_names(unit):
    rows = _drop_ins_for(unit)
    assert rows, ("goal:g7.33.18 names %s in its no-cascade row but no manifest "
                  "row ships a drop-in for it" % unit)
    v = _v()
    rendered = [R.rendered(row, v) for row in rows]
    # the unit's no-cascade layer rides the CONFIGURED OOM_POLICY, never a literal
    assert any("OOMPolicy=" + CFG["values"]["boxkit"]["OOM_POLICY"] in out for out in rendered), rows
    assert all(p["reload"] in ("system", "user") and p["mode"] == "0644" for p in rows)


@pytest.mark.parametrize("unit", _no_cascade_units())
def test_no_cascade_drop_in_matches_the_live_bytes_or_names_its_absence(unit):
    rows = _drop_ins_for(unit)
    v = R.values(CFG, MEASURED, R.host_tokens(CFG))
    absent = [row["name"] for row in rows
              if not R.destination(row, CELLS, v, "/").is_file()]
    if absent:
        pytest.skip("no live bytes on this box for the no-cascade drop-in(s) %s of unit %s "
                    "(the unit carries no such drop-in here), so there is nothing to falsify "
                    "against -- the kit is portable" % (", ".join(absent), unit))
    for row in rows:
        assert R.rendered(row, v) == R.destination(row, CELLS, v, "/").read_text(encoding="utf-8")
