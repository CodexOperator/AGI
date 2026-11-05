"""The boxkit acceptance suite for
hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes.

Rows 1-15, one per clause of the claim, plus lettered sub-rows. THE RULE, not an
inventory: a row is SPECIFIED by the comment above its own test. This docstring is
nevertheless an inventory, and the claim that it is not was refuted by its own bytes
(DH.653 item 5: rows 11, 12 and 13 were named in the file and listed nowhere here).
Rather than delete it, the copy is CHECKED -- row 15 fails if a row the file names is
absent below, so it goes RED instead of stale.

1. every manifest row carries the KIT CONTRACT keys and a known dest_cell;
2. every piece renders with no {{UNFILLED}} surviving;
3. render() refuses an unfilled placeholder BY NAME;
4. no template byte carries a literal host token (owner user, home, repo root,
   guard source) or a literal cgroup UID -- anonymize.py CANNOT do this job (its
   classes are hostname/ip/mac/board/secret; see experiment:a00-5e1ed113 P4);
5. SIZING reproduces the measured knobs by TRUNCATION, never rounding;
6. the FIXTURE is the ANONYMIZED RENDERED bytes, not a copy of the template: the
   template rendered with the measured inputs and the fixed stand-ins, so a changed
   template, sized value or stand-in MOVES it (the old test asserted template ==
   fixture, i.e. X == X); the three no-cascade rows record the LIVE bytes and are
   compared by the drift cell each manifest row carries -- the EXACT set of differing
   lines, not merely "they differ". Every fixture comparison goes through
   _assert_piece_matches_fixture: a row with no drift cell gets an EMPTY delta, so an
   undeclared difference is red;
7. the rendered bytes EQUAL the RECORDED LIVE bytes -- recorded once into an anonymized
   fixture, never read from ~/.config at test time: a committed test that reads a live
   unit is a probe wearing a test's name, green here and red or skipped on every other
   box. The fixture is compared against the render made with the identity tokens the KIT
   derives from the running engine checkout and the committed paths.boxkit.guard_dir
   cell, each token swapped for the stand-in that anonymized it, never tokens the test
   injects. The live comparison itself is a probe the PARENT runs;
7b. the identity roots are DERIVED, not cells: repo_root from the engine's own
   __file__ (through a linked worktree's .git FILE, no git subprocess), guard_dir from
   the committed cell -- and the per-box inputs are ARGUMENTS, refused BY NAME;
7c. every manifest dest_cell resolves against the COMMITTED config (the
   user_systemd_data_dir debt is closed: the director committed that cell);
7d. FIXTURE PROVENANCE: every manifest row carries the fixture_sha256 of its committed
   fixture, and the file on disk still hashes to it -- the strongest tie a committed
   test can make between a fixture and the live bytes it claims to record;
8. install() writes only under a tmp install_root, with the manifest mode;
9. a row whose bytes are NEW TO THE KIT -- authored here, not copied from an
   installed file -- is flagged new_bytes, and is therefore excluded from the
   rendered==live comparison. new_bytes says NOTHING about whether this box carries
   the file: the three no-cascade drop-ins are new to the kit AND have live
   counterparts (row 10 compares them), and agi-survival-conf is new to the kit and has none;
10: the manifest covers EVERY unit goal:g7.33.18's no-cascade row names, read from
    the LIVE goal node (never a copied list), and each no-cascade drop-in is compared
    against its RECORDED LIVE bytes by the DECLARED delta, line for line: a converging
    and a differently-drifting render are both RED, and a row with no recorded live
    bytes is a NAMED skip, never a silent pass.
11: WHOLE-TABLE COVERAGE: the manifest reaches EVERY unit the goal node's table names,
    not just the no-cascade layer, and CELLS is read at CALL time (11g), so a cell
    rename moves the rule instead of inverting it.
12: the leak-root rule is the shape the OLD depth rule got wrong -- the legacy oracle is
    pinned inline so _leak_roots must DISAGREE with it, not merely differ.
13: the ANONYMIZED live render substitutes through the longest-first helper (13b pins
    that at the CALL SITE), so a reverted identity order cannot stay green.
14: THE ENGINE'S OWN GUARD over the kit's bytes. Row 4 is a BESPOKE denylist
    (checkout roots, home, owner, cgroup uid) because anonymize.py's classes
    (hostname/ip/mac/board/secret) do not cover those -- which made the two DISJOINT: a
    template naming this box's hostname, a NIC address, a board serial or a key id
    passes row 4 CLEAN. ONE row runs anonymize.scan -- the guard's own function,
    MIN_TOKEN and CLASSES -- against a FAKE box denylist (this box's values are never
    read into the test): it plants one _fake_value in a COPY of one template and
    asserts scan names the CLASS, and asserts the UNPLANTED kit bytes stay clean. It
    guards a PLANTED COPY: the kit's own bytes could only go red on a real denylist.
15: THIS INVENTORY IS CHECKED: every `row N` the file names must be listed above, or the
    row is red. A claim that no inventory exists was itself the stale copy (DH.653).

Reads: config cells, the goal node, and the committed fixtures. It reads NO live unit
file and calls no systemd: the live-bytes comparison is a probe, run by the parent.
Writes: tmp_path only.
"""
from __future__ import annotations

import collections
import hashlib
import importlib.util
import json
import os
import pwd
import re
import shutil
import subprocess
import sys
import types
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parents[1] / "boxkit"
BIN_DIR = Path(__file__).resolve().parents[1] / "bin"
PROJECT = Path(__file__).resolve().parents[3]
GEOMETRY = PROJECT / ".agi" / "nodes" / ".geometry"
UID = str(os.getuid())

CFG = json.loads((PROJECT / ".agi" / "config.json").read_text(encoding="utf-8"))
CELLS = dict(CFG["paths"]["boxkit"])
# every path this suite touches is a committed paths.boxkit cell, resolved at runtime
TEMPLATES = PROJECT / CELLS["templates_dir"]
FIXTURES = PROJECT / CELLS["fixtures_dir"]
OWNER = pwd.getpwuid(os.getuid()).pw_name

# The per-box inputs are ARGUMENTS, never cells (director rule 5): local-town's
# measured /proc/meminfo, from a fixture, so the suite pins the sizing arithmetic
# without reading a live box.
MEASURED = {k: v for k, v in
            json.loads((FIXTURES / "measurements.json").read_text(encoding="utf-8")).items()
            if not k.startswith("_") and k != "box"}
# The fixed stand-ins a fixture is rendered with (fixtures/boxkit/standins.json): a
# committed fixture must never carry a live host path, so every identity token is a
# constant here -- a second box with the same measurements gets exactly these bytes.
STANDINS = {k: v for k, v in
            json.loads((FIXTURES / "standins.json").read_text(encoding="utf-8")).items()
            if not k.startswith("_")}
CONTRACT_KEYS = {"name", "template", "dest_cell", "dest_rel", "mode", "sudo",
                 "reload", "placeholders", "new_bytes", "fixture_sha256"}


def _load():
    spec = importlib.util.spec_from_file_location("boxkit_render", KIT / "render.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_bin(name):
    """A bin/ module (anonymize.py), loaded the way test_anonymize_guard.py loads
    it: bin/ first on sys.path, because it imports its own siblings."""
    if str(BIN_DIR) not in sys.path:
        sys.path.insert(0, str(BIN_DIR))
    spec = importlib.util.spec_from_file_location(name, BIN_DIR / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


R = _load()
MISSING_CELLS = sorted({p["dest_cell"] for p in R.manifest()["pieces"]} - set(CELLS))
# only for the leak checks (a template or a fixture must not carry a literal root)
# a SHARED root: a bare top-level system directory, shared with every unrelated path and
# a prefix of ordinary command lines, so admitting it makes every leak row match every
# string (the empty-prefix false red, measured as 6). Excluded BY NAME, never by depth.
SHARED_ROOTS = frozenset(("/", "/bin", "/boot", "/data", "/dev", "/etc", "/home", "/lib",
                          "/media", "/mnt", "/opt", "/proc", "/root", "/run", "/sbin",
                          "/srv", "/sys", "/tmp", "/usr", "/var"))


def _leak_roots(project):
    """The host roots a template must not carry literally: the checkout, plus the parents
    that still NAME a directory of their own (residue M2). The checkout root is kept
    UNCONDITIONALLY: the old `len(p.parts) >= 3` rule threw it away on a shallow extract
    ('/a') and made the set EMPTY at top level, so the one leak this row exists for --
    a template naming the checkout -- was not a leak at all."""
    return sorted({str(p) for p in [project] + list(Path(project).parents[1:3])
                   if str(p) not in SHARED_ROOTS})


LEAK_ROOTS = _leak_roots(PROJECT)


# ONE SOURCE for the kit denylist's own tokens (owner, home, the guard dir's own
# fragment); the candidate is DRAWN from this tuple, never re-typed (DH.634 item 4).
# The guard fragment is DRAWN FROM THE CELL paths.boxkit.guard_dir, not re-typed as
# '/.sanctuary/' (DH.653 item 4: a literal there duplicated a committed cell, so
# repointing the cell left row 4 blind). TAIL TWO, not the leaf: 'guard' is a piece name.
GUARD_FRAGMENT = "/".join([p for p in Path(CELLS["guard_dir"]).parts
                           if not p.startswith("{")][-2:])
# the guard dir's OWN PREFIX, from the same cell (DH.653 item 2): narrowing the literal
# '/.sanctuary/' to the tail-two fragment left a sibling byte under .sanctuary/ a leak
# that no row covered. DRAWN, not re-typed -- still one source.
GUARD_PREFIX = "/".join([p for p in Path(CELLS["guard_dir"]).parts
                         if not p.startswith("{")][:1])
KIT_TOKENS = (OWNER, str(Path.home()), GUARD_FRAGMENT, GUARD_PREFIX)
# a fragment absent from the resolved dir can never fire -- refused at the definition
assert GUARD_FRAGMENT in str(R.expand(CELLS, CELLS["guard_dir"], R.engine_checkout())), \
    "paths.boxkit.guard_dir %r yields fragment %r, absent from the resolved dir" % (
        CELLS["guard_dir"], GUARD_FRAGMENT)


def _leaks(text, roots=LEAK_ROOTS):
    return [t for t in (*KIT_TOKENS, *roots) if t and t in text]


# the source and the rule are one: if a token is in KIT_TOKENS it must be DENIED
# by _leaks. RED if the tuple grows and the denylist stops consulting it.
assert all(_leaks("cd %s\n" % t) for t in KIT_TOKENS if t), KIT_TOKENS
# the LOST CLASS, covered: a template naming a sibling under the guard dir's prefix
assert _leaks("cd %s/notes\n" % GUARD_PREFIX), \
    "the guard dir's own prefix class is not denied"

# A probe identity: contract tests need SOME value for REPO_ROOT/GUARD_SRC to render
# at all, and a probe is not the answer -- the wire test below supplies nothing.
# The measured box sets no memory cell in config:guard, so its fixtures render with
# guard-init's defaults: pinned here, never read from THIS box (goal:g7.16.1.5.5.4).
GUARD = {}
PROBE = {"OWNER_USER": "probe", "UID": "4242", "REPO_ROOT": "/probe/repo",
         "GUARD_SRC": "/probe/.sanctuary/guard/guard-init.sh"}


def _v(**over):
    o = dict(PROBE)
    o.update(over)
    return R.values(CFG, MEASURED, o, guard=GUARD)


def _vs(**over):
    """The values a committed fixture is rendered with: the measured inputs plus the
    fixed stand-ins. This is the OFF-BOX comparison -- the bytes a second box gets."""
    o = dict(STANDINS)
    o.update(over)
    return R.values(CFG, MEASURED, o, guard=GUARD)


def _post_cg(tail=""):
    """A cgroup line the POST_CGROUP_RE cell matches, derived FROM that cell (one source; stand-in post `a`)."""
    rx = _vs()["POST_CGROUP_RE"]
    line = rx.lstrip("^").replace("[^/\\n]+", "a").replace("\\.", ".").replace("(/|$)", "") + tail
    assert re.search(rx, line + "\n", re.M), line
    return line


def _payload(text):
    """The FUNCTIONAL bytes of a unit drop-in: everything that is not a comment header."""
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))


# The drift rows are the rows whose manifest row carries a drift cell -- the
# template-render and the RECORDED LIVE file differ by a DELTA THE MANIFEST
# DECLARES, line for line. The set is read from the manifest, never copied here.
PIECES = R.manifest()["pieces"]
DRIFT_ROWS = {p["name"] for p in PIECES if p.get("drift")}


def _declared(piece, key, v):
    """A declared drift line, resolved through the SAME renderer as the template, so
    an identity token in the declaration comes from values/stand-ins, not a literal."""
    name = piece["name"] + ".drift." + key
    return R.render("\n".join(piece["drift"][key]), v, name).splitlines()


# the identity placeholders a stand-in stands in for: the only values a committed
# fixture may differ from a live box on.
IDENTITY = ("OWNER_USER", "UID", "REPO_ROOT", "GUARD_SRC")


def _delta(rendered, recorded):
    """(lines only in the render, lines only in the recorded live bytes), as exact
    multisets -- a duplicated or dropped line is a delta, not a no-op."""
    a, b = (collections.Counter(x.splitlines()) for x in (rendered, recorded))
    return sorted((a - b).elements()), sorted((b - a).elements())

BY_NAME = {p["name"]: p for p in PIECES}
# LIVE = the pieces copied from an INSTALLED file, the ones the kit can falsify
# byte-for-byte against this box. A new_bytes row is new TO THE KIT, so it is excluded;
# whether a live counterpart happens to exist is question 10, not a property of the flag.
LIVE = [p for p in PIECES if not p.get("new_bytes")]
# the LIVE identity tokens, used only to assert a committed fixture does not carry them
HOST_TOKENS = (OWNER, str(Path.home()), str(R.engine_checkout()),
               str(R.expand(CELLS, CELLS["guard_dir"], R.engine_checkout())))


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
    leaks = _leaks(text)
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


# 5b -- goal:g7.16.1.5.5.4: every memory number is config:guard's, through guard-init's
# own arithmetic; values.boxkit keeps none, and the defaults are guard-init's own lines
def test_values_boxkit_carries_no_memory_number():
    assert not set(R.MEMORY) & set(CFG["values"]["boxkit"])
    assert not [k for k in CFG["values"]["boxkit"]
                if re.search(r"OOM_PCT|_high_ratio|_max_ratio|_ratio$", k)]


def test_every_cell_sizing_reads_is_parsed_from_guard_init():
    """A guard-init cell line whose format drifts from CELL drops out of guard_defaults:
    red here, and a named refusal in sizing() -- never a bare KeyError."""
    assert set(R.SIZING_CELLS) <= set(R.guard_defaults())
    g = R.guard_defaults()
    g.pop("SSH_MIN")
    with pytest.raises(R.KitError, match="guard-init cell line\\(s\\) SSH_MIN not parsed"):
        R.sizing(7365, 4095, g)


def test_no_base_blanks_only_the_base_derived_targets():
    out = R.sizing(None, None, R.guard_defaults())
    assert not set(R.FROM_BASE) & set(out) and "USER_SWAP" not in out
    assert (out["SYSTEM_MIN"], out["SSH_MIN"], out["ENGINE_MAX"], out["OOMD_SWAP_PCT"]) == \
        ("128M", "64M", "512M", "90")


def test_a_guard_cell_moves_the_render():
    v = R.values(CFG, MEASURED, PROBE, guard={"USER_HIGH_PCT": "95", "ENGINE_MAX": "3G",
                                             "OOMD_LIMIT": "85", "PSI_FULL": "60"})
    user_max = int(v["USER_MAX"].rstrip("M"))
    agi_max = user_max * 70 // 100
    assert v["USER_HIGH"] == "%dM" % (user_max * 95 // 100)
    assert (v["ENGINE_MAX"], v["ENGINE_HIGH"]) == ("3072M", "2304M")
    assert v["WORK_MAX"] == "%dM" % (agi_max - 3072)
    assert (v["USER_OOM_PCT"], v["HEALTH_LIMIT"]) == ("85", "60")


def test_a_guard_cell_sizing_a_unit_out_of_range_is_refused():
    """goal:g7.16.1.5.5.8: the kit refuses what guard-init refuses (range, not shape)."""
    for cells in ({"ENGINE_MAX": "100G"}, {"ENGINE_MAX": "0.5M"}):
        with pytest.raises(R.KitError) as err:
            R.values(CFG, MEASURED, PROBE, guard=cells)
        assert "config:guard sizes" in str(err.value) and \
            ("WORK_MAX" in str(err.value) or "ENGINE_MAX" in str(err.value)), str(err.value)
    with pytest.raises(R.KitError, match="SSH_MIN"):          # MemoryMin > RAM (0 stays legal)
        R.values(CFG, MEASURED, PROBE, guard={"SSH_MIN": "%dM" % (MEASURED["MEM_TOTAL"] + 1)})
    assert R.values(CFG, MEASURED, PROBE, guard={"SSH_MIN": "0"})["SSH_MIN"] == "0M"


def test_guard_none_reads_this_boxs_cells(monkeypatch):
    seen = []
    monkeypatch.setattr(R, "guard_cells", lambda root=None: seen.append(root) or
                        {**R.guard_defaults(), "AGI_MAX_PCT": "60"})
    v = R.values(CFG, MEASURED, PROBE)
    assert seen == [None]
    assert v["AGI_MAX"] == "%dM" % (int(v["USER_MAX"].rstrip("M")) * 60 // 100)


# 6 -- THE FIXTURE IS THE RENDER, NOT A COPY OF THE TEMPLATE. The previous version
# asserted template == fixture, i.e. X == X: it could never fail. A fixture here is the
# ANONYMIZED RENDERED bytes -- template rendered with the measured inputs and the fixed
# stand-ins -- so a changed template, sized value or stand-in moves it. The three
# no-cascade rows record the LIVE bytes (named drift) and are compared on payload.
@pytest.mark.parametrize("piece", PIECES, ids=[p["name"] for p in PIECES])
def test_rendered_bytes_equal_the_anonymized_fixture(piece):
    fix = FIXTURES / (piece["name"] + ".fixture")
    assert fix.is_file(), fix
    _assert_piece_matches_fixture(piece, R.rendered(piece, _vs()),
                                  fix.read_text(encoding="utf-8"), _vs())


def _assert_piece_matches_fixture(piece, got, recorded, v):
    """The ONE fixture comparison, shared by every row that reads a fixture: outside the
    manifest-declared drift delta the kit render must EQUAL the recorded bytes exactly.
    A row with no drift cell gets an EMPTY delta, so an undeclared difference is red;
    a drift row goes through _assert_declared_drift."""
    if piece["name"] in DRIFT_ROWS:
        _assert_declared_drift(piece, got, recorded, v)
    else:
        assert got == recorded, _diff(recorded, got)


def _assert_declared_drift(piece, got, recorded, v):
    """The EXACT-DELTA falsifier for a drift row. "They differ" is not a falsifier: a
    template that lost a whole section still differs, and would keep a `got != want`
    green. So: the payload is equal, and the full multiset of differing lines EQUALS
    the set the manifest declares. A render that CONVERGES (no delta at all) is RED,
    not an improvement: the live file carries the owner's 09-25 survival header and the
    drift cell is the record of that difference. A DIFFERENT drift is RED too."""
    name = piece["name"]
    assert _payload(got) == _payload(recorded), _diff(_payload(recorded), _payload(got))
    extra, missing = _delta(got, recorded)
    want_extra = sorted(_declared(piece, "render_only_lines", v))
    want_missing = sorted(_declared(piece, "live_only_lines", v))
    assert not (not extra and not missing), (
        "%s CONVERGED: the render now equals the recorded live bytes exactly, so the "
        "drift cell describes nothing. The live file carries the owner 09-25 survival "
        "header on purpose: a converging render is a lost declaration." % name)
    assert (extra, missing) == (want_extra, want_missing), (
        "%s drifted DIFFERENTLY than the manifest declares.\n  actual render-only:   %s\n"
        "  declared render-only: %s\n  actual live-only:    %s\n  declared live-only:  %s\n"
        "  why: %s" % (name, extra, want_extra, missing, want_missing, piece["drift"]["why"]))


def _diff(want, got):
    import difflib
    return "\n".join(difflib.unified_diff(want.splitlines(), got.splitlines(),
                                          "fixture", "rendered", lineterm="", n=1))


# 6b -- the anti-circular falsifier: the fixture is a RENDER, so it cannot be a copy
# of the template byte-for-byte wherever an identity token is substituted, and a
# changed measured input must move the rendered bytes away from the fixture.
@pytest.mark.parametrize("piece", PIECES, ids=[p["name"] for p in PIECES])
def test_the_fixture_is_a_render_and_not_a_copy_of_the_template(piece):
    tmpl = (TEMPLATES / piece["template"]).read_text(encoding="utf-8")
    fix = (FIXTURES / (piece["name"] + ".fixture")).read_text(encoding="utf-8")
    if set(piece["placeholders"]) & set(STANDINS):
        assert fix != tmpl, ("%s substitutes %s but its fixture is byte-identical to the "
                             "template: the fixture is a copy, the test is X == X"
                             % (piece["name"], sorted(set(piece["placeholders"]) & set(STANDINS))))
    # a sized input moved by 1M changes every sized byte in the render
    if any(k in piece["placeholders"] for k in ("MEM_TOTAL", "AGI_HIGH", "USER_MAX")):
        moved = R.rendered(piece, _vs(MEM_TOTAL=MEASURED["MEM_TOTAL"] + 1))
        assert moved != R.rendered(piece, _vs())


# 6c -- no committed fixture may carry a live host token (a fixture built from a live
# read is a leak, which is the whole point of the stand-ins).
@pytest.mark.parametrize("piece", PIECES, ids=[p["name"] for p in PIECES])
def test_no_fixture_carries_a_live_host_token(piece):
    fix = (FIXTURES / (piece["name"] + ".fixture")).read_text(encoding="utf-8")
    assert not [t for t in HOST_TOKENS if t and t in fix], piece["name"]


# 6e -- ANONYMIZATION IS A PROPERTY OF THE BYTES, checked over EVERY committed fixture
# (including the recorded live ones): no home path, no repo root, no box user, no
# absolute path outside the kit's own destination cells.
def test_every_committed_fixture_is_anonymized():
    forbidden = {str(Path.home()), OWNER, "/data/work", "/root/"}
    for fix in sorted(FIXTURES.glob("*.fixture")):
        text = fix.read_text(encoding="utf-8")
        bad = sorted(t for t in forbidden | set(HOST_TOKENS) if t and t in text)
        assert not bad, "%s carries %s" % (fix.name, bad)
        assert not re.search(r"^/(home|root)/[^/\s]+", text, re.M), fix.name
        assert "{{" not in text, fix.name


# 6d -- the stand-ins are constants, not this box: a fixture rendered with the LIVE
# host tokens must not be the committed fixture (or the anonymization is a no-op).
def test_the_stand_ins_are_constants_and_not_this_box():
    assert STANDINS["UID"] != UID and STANDINS["OWNER_USER"] != OWNER
    assert STANDINS["REPO_ROOT"] != str(R.engine_checkout())
    piece = BY_NAME["user-slice-guard"]
    assert R.rendered(piece, R.values(CFG, MEASURED, R.host_tokens(CFG), guard=GUARD)) != \
        (FIXTURES / (piece["name"] + ".fixture")).read_text(encoding="utf-8")


# 7 -- THE FALSIFIER: the RECORDED fixture IS what this box renders. The previous
# version never touched the fixture: it rendered twice (host tokens, then stand-ins),
# masked the four identity placeholders on both sides and asserted the renders were
# equal -- X == X for every sized value, green forever. It now READS the committed
# fixture, and it is NOT test 6: test 6 pins the STAND-IN side (a changed stand-in,
# sized value or template moves the render off the fixture), test 7 pins the
# DERIVED-HOST side -- this box's own R.host_tokens() must be non-empty and land EXACTLY
# at the identity placeholder sites, no more and no fewer times, and the bytes that
# leaves must be the recorded ones. That occurrence count is what test 6 cannot make:
# red when a token is empty or fails to reach the render, where test 6 is green. (NOT a
# shape check: a token of the right arity but the wrong shape -- REPO_ROOT with a
# trailing slash -- is substituted back and stays green. Shape: 7b.) Reading a live unit
# is still forbidden; the fixture is tied to the recorded live bytes by its manifest
# fixture_sha256 cell (7d) plus the parent's probe.
@pytest.mark.parametrize("piece", LIVE, ids=[p["name"] for p in LIVE])
def test_rendered_bytes_equal_the_recorded_live_bytes(piece):
    fix = FIXTURES / (piece["name"] + ".fixture")
    assert fix.is_file(), fix
    got = _anonymized_live_render(piece)
    _assert_piece_matches_fixture(piece, got, fix.read_text(encoding="utf-8"), _vs())


def _with_the_whole_stand_in_set(piece, tokens):
    """The bytes a committed fixture IS: this box's values with the stand-in put back
    for EVERY identity key -- one mapping, no partial override. The fixture was rendered
    with all of them, so a comparison may only be made against a render carrying all of
    them. The clean path reaches these bytes by substitution BY VALUE (what the
    occurrence count is for); the collision fallback reaches them by re-rendering here.
    A key with no {{K}} site is harmless: a value no placeholder consumes never lands."""
    return R.rendered(piece, R.values(CFG, MEASURED,
                                      {**tokens, **{k: STANDINS[k] for k in IDENTITY}},
                                      guard=GUARD))


def _anonymized_live_render(piece, tokens=None):
    """This box's own render of the piece, with the stand-in put back where each derived
    identity token landed. Substitution is BY VALUE, not by a marker: a marker replaces
    the token before the render, so a token that never reaches the render would be
    masked away and the comparison would be X == X again. Hence the occurrence count --
    each derived token must appear in the render exactly as many times as the template
    declares {{K}} sites, never fewer. The one fallback is a token that ALSO occurs
    outside its sites (a template literal colliding with this box's uid, e.g. memguard's
    hard -1000): BY-VALUE substitution cannot tell the two apart there, so the whole
    render is redone through _with_the_whole_stand_in_set -- the FULL stand-in set,
    because the fixture was recorded with all of them. No key needs the fallback here;
    row 7f walks it."""
    tokens = R.host_tokens(CFG) if tokens is None else dict(tokens)
    body = (TEMPLATES / piece["template"]).read_text(encoding="utf-8")
    live = R.rendered(piece, R.values(CFG, MEASURED, tokens, guard=GUARD))
    masked, clean = [], {}
    for k in IDENTITY:
        sites = len(re.findall(r"\{\{%s\}\}" % k, body))
        if not sites:
            continue
        assert tokens[k], (piece["name"], k, "the derived identity token is empty")
        seen = live.count(tokens[k])
        assert seen >= sites, (
            "%s declares %d {{%s}} sites but this box's derived token %r appears %d "
            "time(s) in the render -- the host token does not reach the render"
            % (piece["name"], sites, k, tokens[k], seen))
        if seen > sites:
            masked.append((k, seen, sites))   # ambiguous: a literal collides with it
            continue
        clean[k] = tokens[k]
    out = _substitute_longest_first(live, clean)
    if masked:
        out = _with_the_whole_stand_in_set(piece, tokens)
    return out


def _substitute_longest_first(text, mapping):
    """Put the stand-in back for every derived token, LONGEST TOKEN FIRST (residue N1).
    Two identity tokens on one box can overlap: OWNER_USER=/box/agi and
    REPO_ROOT=/box/agi/extensions, where the shorter is a PREFIX of the longer. In
    identity order the short token is replaced first and eats the longer token's prefix,
    so the {{REPO_ROOT}} site is corrupted into a stand-in path carrying the short
    stand-in's home segment -- a fixture comparison red for a reason unrelated to the
    claim. Longest first, every site lands on the stand-in of the token that owns it;
    ties break on the key, so the bytes are deterministic."""
    for k in sorted(mapping, key=lambda k: (-len(mapping[k] or ""), k)):
        if mapping[k]:
            text = text.replace(mapping[k], STANDINS[k])
    return text


# 7f -- THE COLLISION FALLBACK RE-RENDERS WITH THE WHOLE STAND-IN SET (a00-fc6bf436).
# No host token collides with a template literal on this box, so the fallback branch is
# never taken and its bytes were never compared: a branch no test walks is a branch
# nobody has read. This row WALKS it -- tmp only -- by injecting a synthetic identity
# token whose value is a template LITERAL ("python3", which memguard-script uses outside
# every {{OWNER_USER}} site), so the token occurs more often in the render than the
# template declares sites: the ambiguity the fallback exists for. The bytes it must
# produce are the FIXTURE's -- rendered with the stand-in for EVERY identity key -- so a
# fallback re-rendering only the masked key compares mixed host/stand-in bytes against
# all-stand-in bytes: red for a reason unrelated to the claim, green by accident on a box
# whose host values happen to equal the stand-ins.
def test_the_collision_fallback_re_renders_with_the_whole_stand_in_set():
    piece = BY_NAME["memguard-script"]
    collides = "python3"          # a literal in the template, outside every {{OWNER_USER}} site
    tokens = dict(R.host_tokens(CFG))
    tokens["OWNER_USER"] = collides
    body = (TEMPLATES / piece["template"]).read_text(encoding="utf-8")
    sites = len(re.findall(r"\{\{OWNER_USER\}\}", body))
    live = R.rendered(piece, R.values(CFG, MEASURED, tokens, guard=GUARD))
    assert live.count(collides) > sites, (
        "the synthetic collision did not force the fallback: %d occurrence(s) of %r, "
        "%d site(s)" % (live.count(collides), collides, sites))
    got = _anonymized_live_render(piece, tokens)
    fix = (FIXTURES / (piece["name"] + ".fixture")).read_text(encoding="utf-8")
    _assert_piece_matches_fixture(piece, got, fix, _vs())
    # and the render is anonymized end to end: no host identity root survives it
    assert not [t for t in HOST_TOKENS if t and t in got], piece["name"]


# 7g -- goal:g7.16.1.11.40.1: A POST'S SPINE AND HARNESS ARE PROTECTED BY CGROUP + PLACE IN THE UNIT'S TREE.
# The guard's loop is module-level (not importable), so this runs the RENDERED loop for one pass over a FAKE /proc
# tree in tmp (every "/proc" re-pointed at it, one sleep raising to end the pass, os.kill / subprocess.run / the
# priority calls replaced by recorders). The fake post unit has the shape measured on a v5 post:
#   script > sh > TRACER > { poller > sleep, sh > track > grep, HARNESS > { bash > sleep, mcp node, a child named like the harness } }
# where the HARNESS's argv is the tail of the TRACER's, and one ORPHAN tool sits in the cgroup under pid 1.
# Protected: the chain, the tracer's plumbing and the harness, whatever the harness is called. Not protected: every
# descendant of the harness, the orphan, anything outside every post. Nothing is selected by a command name inside a post.
def _fake_proc(tmp_path, rows):
    """rows: pid -> (comm, argv, cgroup line, ppid, start, resident pages)."""
    proc = tmp_path / "proc"; proc.mkdir()
    (proc / "meminfo").write_text("MemTotal: 33554432 kB\nMemAvailable: 33000000 kB\n")
    for pid, (comm, cmd, cg, ppid, start, pages) in rows.items():
        d = proc / str(pid); d.mkdir()
        (d / "comm").write_text(comm + "\n"); (d / "cmdline").write_text(cmd.replace(" ", "\0") + "\0")
        (d / "statm").write_text("10 %d 1 1 0 1 0\n" % pages); (d / "cgroup").write_text(cg + "\n")
        (d / "stat").write_text("%d (%s) S %d %s %d 0 0\n" % (pid, comm, ppid, " ".join(["0"] * 17), start))
        (d / "oom_score_adj").write_text("0")
    return proc


def _guard_pass(tmp_path, rows, passes=1, avails=None, tick=5, real_box=False, over=None, grow=None, flips=None, spawn=None, sysd=None, rewrite=None, no_uptime=False, kill_raises=(), break_log_at=None, fix_log_at=(), popen_raises=False, logger_raises=False, logger_hangs=False, mutate=None, iids=None):
    """Run the RENDERED loop for `passes` passes on a fake clock (`tick` s per pass); avails[i] = MemAvailable in bytes
    for pass i (default: plenty). Returns (adj, stops, runs, ev): the SIGSTOPped pids, the logger/other run() calls and
    ev = what the loop did besides: conts (SIGCONT pids), boxes ([(argv, stdin text)] of every Popen), clock.
    The fake kernel follows the signals (SIGSTOP -> state T in /proc/N/stat, SIGCONT -> S); flips = {pass: [(pid, state, start)]}
    is a hand: state 'S' resumes it, None removes the process, start (optional) is a new start time (a reused pid).
    The fake kernel also keeps nice per pid (ev.nice) and FORKS: spawn = {pass: [(pid, ppid, comm, cmd)]} makes a child in its
    parent's cgroup that INHERITS the parent's oom_score_adj and nice as they are at that moment. sysd = what `systemctl show`
    says for a unit ({unit: "OOMScoreAdjust=..\\nNice=.."}, an Exception instance to fail); every call lands in ev.sysd.
    rewrite = {pass: [(pid, 'cmd', text) | (pid, 'ppid', n)]} changes a process's argv or parent at that pass (a harness that loses its argv, a tree that cannot be read);
    ev.seq = [('log', text) | ('kill', pid, signal)] in the order they happened; kill_raises = pids whose SIGSTOP raises; ev.stopped = the guard's stopped map at the end.
    iids = {unit: InvocationID | [one per call, the last repeats] | Exception} answers the guard's ONE `systemctl show UNITS -p Id -p InvocationID` (default: the same id for every unit, every call); every call lands in ev.inv as (clock, [units]).
    /proc/uptime follows the fake clock, so a process's age is the clock minus its start ticks."""
    piece = BY_NAME["memguard-script"]
    tmp_path.mkdir(parents=True, exist_ok=True)
    proc = _fake_proc(tmp_path, rows)
    src = R.rendered(piece, _vs(MEMGUARD_LOG=str(tmp_path / "guard.log"), **(over or {}))).replace("/proc", str(proc))
    if mutate is not None: src = mutate(src)          # a row's MUTANT: the rendered guard with one site changed
    assert "/var/log" not in src       # log() writes a tmp path here, never the live log
    assert "send.py" not in src        # the retired mail path is gone from the rendered guard
    for c in ("time.sleep(", "time.time()", "os.kill(", "subprocess.Popen(", "os.getpriority(", "os.setpriority(", "subprocess.check_output(", "os.listdir("):
        assert c in src, c
    src = src.replace("time.sleep(", "_sleep(").replace("time.time()", "_now()")
    src = src.replace("os.kill(", "_kill(").replace("subprocess.run(", "_run(")
    src = src.replace("subprocess.Popen(", "_popen(")             # the journal line (logger) is ALWAYS the fake: a real_box run spawns only the real notice children
    src = src.replace("subprocess.check_output(", "_out(").replace("os.listdir(", "_ls(")
    src = src.replace("os.getpriority(", "_gp(").replace("os.setpriority(", "_sp(")   # fake pids may be real ones
    import signal as _sig
    clock, n, ev = [10_000.0], [0], types.SimpleNamespace(conts=[], boxes=[], stops=[], nice={}, sysd=[], sysd_kw=[], order=[], seq=[], stopped={}, largv=[], pend=[], spools=[], inv=[])
    avails = avails or [33_000_000 * 1024]
    def setavail(i):
        a = avails[min(i, len(avails) - 1)]
        if i in fix_log_at and (tmp_path / "guard.log").is_dir(): (tmp_path / "guard.log").rmdir(); (tmp_path / "guard.log").write_text("")
        if i == break_log_at or (isinstance(break_log_at, (set, tuple, list)) and i in break_log_at): (tmp_path / "guard.log").unlink(missing_ok=True); (tmp_path / "guard.log").mkdir()          # the guard's log cannot be appended to from here on (a full disk, EACCES)
        if not no_uptime: (proc / "uptime").write_text("%.2f 0.00\n" % clock[0])
        for pid, what, v in (rewrite or {}).get(i, []):
            if what == "cmd": (proc / str(pid) / "cmdline").write_text(v.replace(" ", "\0") + "\0")
            else:
                f = proc / str(pid) / "stat"; f.write_text(re.sub(r"(\) [A-Za-z] )\d+", lambda m: m.group(1) + str(v), f.read_text(), count=1))
        (proc / "meminfo").write_text("MemTotal: 33554432 kB\nMemAvailable: %d kB\n" % (a // 1024))
        for pid, pages in (grow or {}).get(i, []):          # a process that grows at pass i
            (proc / str(pid) / "statm").write_text("10 %d 1 1 0 1 0\n" % pages)
        for pid, ppid, comm, cmd in (spawn or {}).get(i, []):          # a fork: the child inherits adj + nice as they are NOW
            par = proc / str(ppid); d = proc / str(pid); d.mkdir()
            (d / "comm").write_text(comm + "\n"); (d / "cmdline").write_text(cmd.replace(" ", "\0") + "\0")
            (d / "statm").write_text("10 10 1 1 0 1 0\n"); (d / "cgroup").write_text((par / "cgroup").read_text())
            (d / "stat").write_text("%d (%s) S %d %s %d 0 0\n" % (pid, comm, ppid, " ".join(["0"] * 17), 5000 + pid))
            (d / "oom_score_adj").write_text((par / "oom_score_adj").read_text()); ev.nice[pid] = ev.nice.get(ppid, 0)
        for pid, state, *start in (flips or {}).get(i, []):
            if state is None: shutil.rmtree(proc / str(pid))
            else: setstate(pid, state, *start)
    def setstate(pid, state, start=None):
        f = proc / str(pid) / "stat"; t = f.read_text()
        t = re.sub(r"\) [A-Za-z] ", ") %s " % state, t, count=1)
        if start is not None: t = re.sub(r"( 0){17} \d+ ", lambda m: m.group(0).rsplit(" ", 2)[0] + " %d " % start, t, count=1)
        f.write_text(t)
    setavail(0)
    def _sleep(s):
        clock[0] += tick; n[0] += 1
        if n[0] >= passes: raise SystemExit
        setavail(n[0])
    def _kill(pid, sig):
        glog = tmp_path / "guard.log"; ev.seq.append(("kill", pid, int(sig), glog.read_text() if glog.is_file() else ""))       # + what the guard's file held AT the kill
        if pid in kill_raises and sig == _sig.SIGSTOP: raise ProcessLookupError(pid)
        (ev.stops if sig == _sig.SIGSTOP else ev.conts).append(pid); ev.order.append(("stop" if sig == _sig.SIGSTOP else "cont", pid)); setstate(pid, "T" if sig == _sig.SIGSTOP else "S")
    class _P:
        def __init__(s, argv, **k):
            if popen_raises: raise OSError("no runuser")
            ev.boxes.append([argv, argv[-1]]); ev.seq.append(("popen", argv[-1]))        # [argv, the notice text]: the text is the last argv word, never a shell string
        def poll(s): return 0
        def wait(s, timeout=None): ev.seq.append(("wait", "notice")); return 0
        def communicate(s, *a, **k): ev.seq.append(("wait", "notice")); return (None, None)
    class _L:
        """The journal line: `timeout 30 logger -t agi-memguard MSG`, fire-and-forget (ev.seq 'log'); logger_raises = the spawn itself fails."""
        def __init__(s, argv, **k):
            if logger_raises: raise OSError("no logger")
            ev.largv.append((argv, k)); runs.append((argv[2:],)); ev.seq.append(("log", argv[-1]))
        def poll(s): return None if logger_hangs else 0               # a hung logger stays in the pending list (the real one is killed by `timeout 30`)
        def wait(s, timeout=None): ev.seq.append(("wait", "logger")); return 0            # a WAIT on the logger is an event: row (b) asserts none before the stop
        def communicate(s, *a, **k): ev.seq.append(("wait", "logger")); return (None, None)
    class _S:
        """The alarm spool append (goal:g7.16.1.11.20.2): `timeout 30 runuser -u agi-SEAT -- python3 alarm_spool.py append ... --text TEXT`, fire-and-forget; recorded APART from the notices (ev.spools) so every notice-count row keeps its exact meaning."""
        def __init__(s, argv, **k):
            if popen_raises: raise OSError("no runuser")
            ev.spools.append(argv)
        def poll(s): return 0
        def wait(s, timeout=None): ev.seq.append(("wait", "spool")); return 0
        def communicate(s, *a, **k): ev.seq.append(("wait", "spool")); return (None, None)
    def _popen(argv, **k):
        if argv[2:3] == ["logger"]: return _L(argv, **k)
        if any(str(a).endswith("alarm_spool.py") for a in argv): return _S(argv, **k)
        return _P(argv, **k) if not real_box else subprocess.Popen(argv, **k)
    def _run(*a, **k):                    # a BLOCKING subprocess.run: the guard has none; its one blocking call is baseline()'s `systemctl show` (check_output, timeout 10, at the tick END: _out below), so any entry here is a wait on the stop path
        ev.seq.append(("run", a[0][-1])); runs.append(a)
        if logger_raises: raise OSError("no logger")
    runs = []
    def _out(argv, **k):
        if "InvocationID" in argv:                       # the same-incarnation read: ONE call for every candidate unit, apart from the baseline reads (ev.sysd)
            names = argv[2:argv.index("-p")]; ev.inv.append((clock[0], list(names))); ev.seq.append(("inv", list(names))); blocks = []
            for nm in names:
                got = (iids or {}).get(nm, "inv-1")
                if isinstance(got, list): got = got.pop(0) if len(got) > 1 else got[0]
                if isinstance(got, Exception): raise got
                blocks.append("Id=%s\nInvocationID=%s\n" % (nm, got))
            return "\n".join(blocks)
        ev.sysd.append(argv); ev.sysd_kw.append(k); ev.order.append(("fetch", argv[2])); got = (sysd or {}).get(argv[2], "OOMScoreAdjust=0\nNice=0\n")
        if isinstance(got, list): got = got.pop(0) if len(got) > 1 else got[0]          # a sequence: one answer per call, the last repeats
        if isinstance(got, Exception): raise got
        return got
    ns = {"__name__": "memguard_test", "_kill": _kill, "_out": _out, "_ls": lambda d: sorted(os.listdir(d), key=lambda x: int(x) if x.isdigit() else 0),   # a fixed pid order
           "_run": _run, "_popen": _popen,
          "_gp": lambda w, pid: ev.nice.get(pid, 0), "_sp": lambda w, pid, v: ev.nice.__setitem__(pid, v), "_sleep": _sleep, "_now": lambda: clock[0]}
    with pytest.raises(SystemExit):
        exec(compile(src, "memguard-rendered", "exec"), ns)
    for q in ns.get("pend", []): q.wait(timeout=60)      # only non-empty with real_box: the real children finish
    adj = {pid: int((tmp_path / "proc" / str(pid) / "oom_score_adj").read_text()) for pid in rows if (tmp_path / "proc" / str(pid)).exists()}
    ev.clock = clock[0]; ev.stopped = dict(ns.get("stopped", {})); ev.pend = list(ns.get("pend", []))
    return adj, sorted(ev.stops), runs, ev


def _post_unit(harness_comm="zzz-new", tracee="zzz-new --model m -c go", big=()):
    """The fake post unit; `big` = pids given a huge resident set (over 70% of the fake MemTotal)."""
    cg = _post_cg(); huge = 7_000_000
    def r(comm, cmd, ppid, start, pid, cgl=cg):
        return (comm, cmd, cgl, ppid, start, huge if pid in big else 10)
    rows = {
        10: r("script", "script -qfaO/h/o -c agi-run", 1, 100, 10),
        11: r("sh", "sh -c agi-run", 10, 101, 11),
        12: r("strace", "strace -qqf -b execve -e%file -o|agi-track " + tracee, 11, 102, 12),
        13: r("agi-run", "/bin/sh /h/bin/agi-run", 12, 103, 13), 14: r("sleep", "sleep 300", 13, 104, 14),
        15: r("sh", "sh -c agi-track", 12, 105, 15), 16: r("agi-track", "/bin/sh /h/bin/agi-track", 15, 106, 16),
        17: r("grep", "grep --line-buffered -o x", 16, 107, 17),
        20: r(harness_comm, tracee, 12, 110, 20),
        21: r("bash", "/bin/bash -c tool", 20, 120, 21), 22: r("sleep", "sleep 5", 21, 121, 22),
        23: r("node", "node mcp-server", 20, 122, 23), 24: r("claude", "claude -p child", 20, 123, 24),
        30: r("bash", "/bin/bash -c orphan", 1, 900, 30),
    }
    out = "0::/user.slice/user-1.slice/session-1.scope"
    rows[40] = ("claude", "claude", out, 1, 5, huge if 40 in big else 10)              # outside the posts, by comm as before
    rows[41] = ("node", "/x/.npm-global/bin/pi --model m", out, 1, 6, 10)               # a pi worker outside: +500
    rows[42] = ("pi", "/opt/agi/bin/pi", "0::/agi.slice/agi-postX/agi-post@a.service", 1, 7, 10)   # prefix lookalike
    rows[43] = ("pi", "/opt/agi/bin/pi", "0::/agi.slice", 1, 8, 10)
    return rows


def test_memguard_protects_a_posts_spine_and_harness_by_tree_and_nothing_under_the_harness(tmp_path):
    adj, kills, runs, ev = _guard_pass(tmp_path, _post_unit())
    prot, worker = int(_vs()["PROTECT_OOM_ADJ"]), int(_vs()["PI_OOM_ADJ"])
    assert [adj[p] for p in (10, 11, 12, 13, 14, 15, 16, 17)] == [prot] * 8, adj    # the spine, incl. the tracer's plumbing
    assert adj[20] == prot, adj                       # the harness, under a command name nothing lists
    assert [adj[p] for p in (21, 22, 23)] == [0, 0, 0], adj      # tool descendants: unprotected
    assert adj[24] == 0, adj                          # a child NAMED like a protected comm, under the harness: unprotected
    assert adj[30] == 0, adj                          # an orphan in the cgroup (parent 1): not in the unit's tree
    assert adj[40] == prot, adj                       # claude outside every post: by comm, as before
    assert adj[41] == worker, adj                     # a pi worker outside the posts keeps +500
    assert adj[42] == 0 and adj[43] == 0, adj         # prefix lookalikes do not match
    assert kills == [], kills


def test_memguard_a_new_harness_name_is_protected_and_a_by_name_selector_is_red(tmp_path):
    for comm in ("claude", "pi", "zzz-other"):
        (tmp_path / comm).mkdir()
        adj, _, _, _ = _guard_pass(tmp_path / comm, _post_unit(harness_comm=comm, tracee=comm + " --model m -c go"))
        assert adj[20] == int(_vs()["PROTECT_OOM_ADJ"]) and adj[24] == 0, (comm, adj)


def test_memguard_stops_a_runaway_tool_but_never_a_posts_spine_or_harness(tmp_path):
    # tool 21, harness 20, tracer 12 and the outside process 40 all over 70% of RAM: only the tool and the outsider stop
    adj, kills, runs, ev = _guard_pass(tmp_path, _post_unit(big=(21, 20, 12, 40)))
    assert kills == [21, 40], kills
    assert adj[20] == int(_vs()["PROTECT_OOM_ADJ"]) and adj[21] == 0, adj
    said = [a[0][-1] for a in runs]
    assert sum("spine or harness" in m for m in said) >= 2, said   # the harness and the tracer each alert (journal line), not silence


def _runaway_alone():
    """A post unit plus one unprotected process (50) holding a few pages, outside every post: the low-memory candidate."""
    rows = _post_unit(); rows[50] = ("builder", "/usr/bin/builder x", "0::/user.slice/user-1.slice/session-9.scope", 1, 9, 1000)
    return rows


GIB = 1 << 30


def test_memguard_red_alerts_are_written_to_each_recipients_notice_by_their_own_uid_never_signed(tmp_path):
    v = _vs()
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(big=(21,)))
    assert stops == [21], stops
    tos = v["MEMGUARD_ALERT_TO"].split()
    assert [b[0][4][len("agi-"):] if b[0][4].startswith("agi-") else b[0][4] for b in ev.boxes] == tos, ev.boxes
    for argv, text in ev.boxes:
        assert argv[:4] == ["timeout", "30", "runuser", "-u"] and argv[5] == "--" and argv[6] == "env", argv
        assert argv[7] == "HOME=%s/%s" % (v["MEMGUARD_STORES"], argv[4][len("agi-"):]), argv       # the recipient's own home
        assert argv[8:10] == ["sh", "-c"] and "agi-notice add" in argv[10] and ".notice" in argv[10], argv
        assert text.startswith("[memguard-susp-21] SUSPENDED pid 21") and "unit" in text and " (ev " in text, text
    # a stop line is keyed by its pid: a second stop in the same minute is NOT swallowed (a frozen pid in silence is the failure)
    adj, stops, runs, ev = _guard_pass(tmp_path / "two", _post_unit(big=(21, 23)))
    assert stops == [21, 23] and len(ev.boxes) == 2 * len(tos), (stops, len(ev.boxes))
    assert sorted({b[1].split(" ")[0] for b in ev.boxes}) == ["[memguard-susp-21]", "[memguard-susp-23]"], ev.boxes


def test_memguard_the_rendered_code_holds_no_signing_mail_or_key_path(tmp_path):
    src = R.rendered(BY_NAME["memguard-script"], _vs())
    code = src.split('"""', 2)[2]                       # past the module docstring
    assert not re.search(r"send\.py|\bbox\b|commit|gpg|signingkey|ssh-keygen|\.ssh|git |sudo", code), \
        re.findall(r"send\.py|\bbox\b|commit|gpg|signingkey|ssh-keygen|\.ssh|git |sudo", code)


def test_memguard_a_red_alert_reaches_each_recipients_own_notice_through_the_real_agi_notice_piece(tmp_path, monkeypatch):
    import shutil, subprocess
    if not all(shutil.which(c) for c in ("awk", "timeout", "env", "sh")):
        pytest.skip("needs awk, timeout, env and sh")
    tos = _vs()["MEMGUARD_ALERT_TO"].split(); assert len(tos) >= 2
    stores = tmp_path / "stores"; (tmp_path / "bin").mkdir()
    piece = re.search(r"^### agi-notice \(\d+ B\)\n~~~sh\n(.*?)\n~~~", (GEOMETRY / "engine-post.md").read_text(encoding="utf-8"), re.M | re.S).group(1)
    for i, to in enumerate(tos):                        # the first has the piece in its bin, the second does not (an old unit)
        (stores / to / "bin").mkdir(parents=True)
        if i == 0:
            (stores / to / "bin" / "agi-notice").write_text(piece + "\n"); (stores / to / "bin" / "agi-notice").chmod(0o755)
    (tmp_path / "bin" / "runuser").write_text('#!/bin/sh\n[ "$1" = -u ]&&shift 2;[ "$1" = -- ]&&shift;exec "$@"\n'); (tmp_path / "bin" / "runuser").chmod(0o755)
    monkeypatch.setenv("PATH", "%s:%s" % (tmp_path / "bin", os.environ["PATH"]))
    _guard_pass(tmp_path / "run", _post_unit(big=(21,)), real_box=True, over={"MEMGUARD_STORES": str(stores)})
    for to in tos:
        f = stores / to / ".notice"
        lines = f.read_text().splitlines()
        assert len(lines) == 1 and lines[0].startswith("[memguard-susp-21] SUSPENDED pid 21"), (to, lines)
        assert f.stat().st_uid == os.getuid()            # created by the recipient's uid, not by the guard as root
    out = subprocess.run([str(stores / tos[0] / "bin" / "agi-notice")], env={"PATH": os.environ["PATH"], "HOME": str(stores / tos[0])},
                         capture_output=True, text=True).stdout       # the post's own printer shows it once
    assert out.startswith("[memguard-susp-21] SUSPENDED pid 21"), out
    assert not (stores / tos[0] / ".notice").exists()


def test_memguard_a_low_stop_then_a_size_stop_of_another_pid_inside_the_cooldown_write_both_lines(tmp_path):
    tos = _vs()["MEMGUARD_ALERT_TO"].split()
    avails = [GIB // 2, 3 * GIB, 3 * GIB]                 # pass 0: low memory stops 50; pass 1: 21 grows past 70% (5 s later)
    adj, stops, runs, ev = _guard_pass(tmp_path, _runaway_alone(), passes=3, avails=avails, grow={1: [(21, 7_000_000)]})
    assert stops == [21, 50], stops
    for to in tos:                                       # BOTH lines reach EACH recipient, the second inside the 600 s cooldown
        said = sorted(b[1].split(" ")[0] for b in ev.boxes if b[0][4] == "agi-" + to)
        assert said == ["[memguard-susp-21]", "[memguard-susp-50]"], (to, said)


def test_memguard_a_size_stop_that_stays_stopped_is_named_again_after_the_renotify_interval(tmp_path):
    again = int(_vs()["RENOTIFY_S"]); tos = _vs()["MEMGUARD_ALERT_TO"].split()
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(big=(21,)), passes=6, avails=[3 * GIB] * 6, tick=again // 2 + 1)
    for to in tos:
        said = [b[1].split(" ")[0] for b in ev.boxes if b[0][4] == "agi-" + to]
        assert said[0] == "[memguard-susp-21]" and said.count("[memguard-still-21]") == 2, (to, said)   # at ~1x and ~2x, not every tick
    assert any("STILL STOPPED pid 21" in b[1] and "resume by hand" in b[1] for b in ev.boxes)


def test_memguard_resumes_a_low_memory_stop_after_the_hysteresis_and_names_unit_and_pid(tmp_path):
    avails = [GIB // 2] + [3 * GIB] * 9           # pass 0: below the 1 GiB line, then above 2x for 9 ticks (45 s)
    adj, stops, runs, ev = _guard_pass(tmp_path, _runaway_alone(), passes=10, avails=avails)
    assert stops == [50] and ev.conts == [50], (stops, ev.conts)        # stopped once, CONTed once (after 30 s held)
    texts = [b[1] for b in ev.boxes]
    assert any(m.startswith("[memguard-resume-50] RESUMED pid 50") and "unit session-9.scope" in m for m in texts), texts


def test_memguard_does_not_resume_on_a_flap_or_a_size_stop(tmp_path):
    flap = [GIB // 2, 3 * GIB, 3 * GIB, 3 * GIB, GIB + GIB // 2] + [3 * GIB] * 5   # 15 s held, a dip to 1.5 GiB, 25 s held
    adj, stops, runs, ev = _guard_pass(tmp_path / "flap", _runaway_alone(), passes=10, avails=flap)
    assert stops == [50] and ev.conts == [], (stops, ev.conts)
    adj, stops, runs, ev = _guard_pass(tmp_path / "size", _post_unit(big=(21,)), passes=10, avails=[3 * GIB] * 10)
    assert stops == [21] and ev.conts == [], (stops, ev.conts)          # a size stop stays stopped: resumed by hand
    assert any("resume by hand: kill -CONT 21" in a[0][-1] for a in runs), [a[0][-1] for a in runs]


def _journal(runs): return [a[0][-1] for a in runs if a[0][:1] == ["logger"]]


def test_memguard_a_size_stop_resumed_by_hand_is_dropped_by_the_kernel_state_not_named_still_stopped(tmp_path):
    again = int(_vs()["RENOTIFY_S"])
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(big=(21,)), passes=4, avails=[3 * GIB] * 4, tick=again // 2 + 1,
                                       grow={1: [(21, 10)]}, flips={1: [(21, "S")]})       # a hand CONTs 21 and it shrinks
    assert stops == [21], stops
    assert not any("[memguard-still-21]" in b[1] for b in ev.boxes), [b[1] for b in ev.boxes]     # no false red for a RUNNING process
    assert not any("STILL STOPPED" in m for m in _journal(runs))
    mine = [m for m in _journal(runs) if "pid 21 " in m and "resumed by hand" in m]
    assert len(mine) == 1, _journal(runs)                                                          # ONE journal line ...
    assert not any("resumed by hand" in b[1] for b in ev.boxes)                                    # ... and not a red notice


def test_memguard_a_hog_resumed_by_hand_that_grows_again_is_stopped_again_with_a_fresh_line(tmp_path):
    tos = _vs()["MEMGUARD_ALERT_TO"].split()
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(big=(21,)), passes=3, avails=[3 * GIB] * 3, flips={1: [(21, "S")]})   # 5 s later, huge again
    assert stops == [21, 21], stops                         # the second SIGSTOP is not swallowed by "pid in stopped"
    for to in tos:                                          # and its line is fresh although inside the 600 s cooldown
        said = [b[1].split(" ")[0] for b in ev.boxes if b[0][4] == "agi-" + to]
        assert said.count("[memguard-susp-21]") == 2, (to, said)


def test_memguard_a_low_stop_resumed_by_hand_gets_no_second_sigcont_and_no_false_resumed_line(tmp_path):
    avails = [GIB // 2] + [3 * GIB] * 9
    adj, stops, runs, ev = _guard_pass(tmp_path, _runaway_alone(), passes=10, avails=avails, flips={2: [(50, "S")]})
    assert stops == [50] and ev.conts == [], (stops, ev.conts)           # the guard never CONTs what a hand already CONTed
    assert not any("RESUMED" in b[1] for b in ev.boxes) and not any("RESUMED" in m for m in _journal(runs))
    assert any("pid 50 " in m and "resumed by hand" in m for m in _journal(runs))


def test_memguard_a_reused_pid_that_grows_is_a_new_process_with_its_own_stop_and_its_own_line(tmp_path):
    tos = _vs()["MEMGUARD_ALERT_TO"].split()      # pass 1: pid 21 is another process (start time 9999), huge again, 5 s inside the cooldown
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(big=(21,)), passes=3, avails=[3 * GIB] * 3, flips={1: [(21, "T", 9999)]})
    assert stops == [21, 21], stops
    for to in tos:
        said = [b[1].split(" ")[0] for b in ev.boxes if b[0][4] == "agi-" + to]
        assert said.count("[memguard-susp-21]") == 2, (to, said)


def test_memguard_a_ptrace_stopped_pid_is_still_a_stopped_pid(tmp_path):
    again = int(_vs()["RENOTIFY_S"])           # state t (stopped under a tracer) is the kernel's "stopped" too: still named, never dropped
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(big=(21,)), passes=4, avails=[3 * GIB] * 4, tick=again // 2 + 1,
                                       grow={1: [(21, 10)]}, flips={1: [(21, "t")]})
    assert any("[memguard-still-21]" in b[1] for b in ev.boxes) and not any("resumed by hand" in m for m in _journal(runs))


def test_memguard_a_stopped_pid_that_died_or_was_reused_leaves_the_list_with_its_cooldown_key(tmp_path):
    again = int(_vs()["RENOTIFY_S"])
    for tag, flip, word in (("dead", (21, None), "gone"), ("reused", (21, "T", 9999), "different process")):
        adj, stops, runs, ev = _guard_pass(tmp_path / tag, _post_unit(big=(21,)), passes=4, avails=[3 * GIB] * 4, tick=again // 2 + 1,
                                           grow={1: [(21, 10)]}, flips={1: [flip]})
        assert not any("[memguard-still-21]" in b[1] for b in ev.boxes), (tag, [b[1] for b in ev.boxes])
        assert sum(1 for m in _journal(runs) if "pid 21 " in m and word in m) == 1, (tag, _journal(runs))


def _unit(): return _post_cg().rsplit("/", 1)[-1]
def _child(tmp_path, pid): return int((tmp_path / "proc" / str(pid) / "oom_score_adj").read_text())
_TOOL = [(60, 20, "bash", "/bin/bash -c newtool")]


def test_memguard_a_tool_forked_by_a_protected_harness_ends_unprotected_within_one_tick(tmp_path):
    prot, nice = int(_vs()["PROTECT_OOM_ADJ"]), int(_vs()["PROTECT_NICE"])
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=3, spawn={1: _TOOL})      # born at pass 1 holding the harness's -900 / -5
    assert adj[20] == prot and ev.nice[20] == nice                                                # the harness keeps both
    assert _child(tmp_path, 60) == 0 and ev.nice[60] == 0, (_child(tmp_path, 60), ev.nice[60])   # the tool is back to the unit's own


def test_memguard_the_reset_value_is_what_systemd_says_for_the_unit_never_a_hard_coded_zero(tmp_path):
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=3, spawn={1: _TOOL}, sysd={_unit(): "OOMScoreAdjust=200\nNice=3\n"})
    assert _child(tmp_path, 60) == 200 and ev.nice[60] == 3
    assert ev.sysd == [["systemctl", "show", _unit(), "-p", "OOMScoreAdjust", "-p", "Nice"]], ev.sysd


def test_memguard_reads_the_unit_baseline_lazily_and_caches_it_for_the_refresh_interval(tmp_path):
    adj, stops, runs, ev = _guard_pass(tmp_path / "idle", _post_unit(), passes=3)
    assert ev.sysd == [], ev.sysd                                                                  # nothing inherited: systemd is never asked
    two = [(60, 20, "bash", "/bin/bash -c a")], [(61, 20, "bash", "/bin/bash -c b")]
    adj, stops, runs, ev = _guard_pass(tmp_path / "cached", _post_unit(), passes=4, spawn={1: two[0], 2: two[1]})
    assert len(ev.sysd) == 1, ev.sysd                                                              # two tools, one read inside the interval
    again = int(_vs()["BASELINE_REFRESH_S"]) + 1
    adj, stops, runs, ev = _guard_pass(tmp_path / "stale", _post_unit(), passes=4, tick=again, spawn={1: two[0], 2: two[1]})
    assert len(ev.sysd) == 2 and _child(tmp_path / "stale", 61) == 0, ev.sysd                # past it, read again


def test_memguard_with_no_readable_baseline_leaves_the_child_and_says_so_once_per_unit(tmp_path):
    tos = _vs()["MEMGUARD_ALERT_TO"].split(); prot = int(_vs()["PROTECT_OOM_ADJ"])
    spawn = {1: [(60, 20, "bash", "/bin/bash -c a")], 2: [(61, 20, "bash", "/bin/bash -c b")]}
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=4, spawn=spawn, sysd={_unit(): OSError("no systemctl")})
    assert _child(tmp_path, 60) == prot and _child(tmp_path, 61) == prot              # never a guess: not reset
    for to in tos:
        said = [b[1].split(" ")[0] for b in ev.boxes if b[0][4] == "agi-" + to]
        assert said.count("[memguard-base]") == 1, (to, said)


def test_memguard_a_pi_worker_inside_a_post_keeps_its_worker_adj_but_loses_the_nice_it_inherited(tmp_path):
    worker = [(62, 20, "node", "/x/.npm-global/bin/pi --model m")]                     # forked by the protected harness: born at adj -900, nice -5
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=3, spawn={1: worker}, sysd={_unit(): "OOMScoreAdjust=0\nNice=3\n"})
    assert _child(tmp_path, 62) == int(_vs()["PI_OOM_ADJ"]), _child(tmp_path, 62)       # the adj is the worker value, not the unit's
    assert ev.nice[62] == 3 and len(ev.sysd) == 1, (ev.nice[62], ev.sysd)               # the nice is the unit's: it was inherited, not the guard's to give
    assert ev.nice[20] == int(_vs()["PROTECT_NICE"])                                    # the harness keeps its own


def test_memguard_proof2_does_not_call_a_pi_worker_wrong_when_the_guard_has_reset_its_inherited_nice(tmp_path):
    worker = [(62, 20, "node", "/x/.npm-global/bin/pi --model m")]
    rc, out = _proof2(tmp_path, spawn={1: worker})
    assert rc == 0 and "62" not in out, out                                              # a false UNDO here would undo a working guard


def _unit_b(): return _unit().replace("agi-post@a", "agi-post@b")


def _two_units():
    """Unit `a` plus a copy `b` (pids + 100, its own cgroup): two posts on one box."""
    rows = _post_unit(); cg = _post_cg()
    sel = [p for p, r in rows.items() if r[2] == cg]
    for p in sel:
        comm, cmd, cgl, ppid, start, pages = rows[p]
        rows[p + 100] = (comm, cmd, cgl.replace("agi-post@a", "agi-post@b"), ppid + 100 if ppid in sel else ppid, start, pages)
    return rows


def test_memguard_the_reset_runs_after_the_stops_in_the_same_tick(tmp_path):
    spawn = {1: [(19, 20, "bash", "/bin/bash -c leaked")]}                     # pid 19 sorts before the runaway: an inline reset would fetch first
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=2, avails=[3 * GIB] * 2, spawn=spawn, grow={1: [(21, 7_000_000)]})
    assert ev.order == [("stop", 21), ("fetch", _unit())], ev.order            # SIGSTOP first, then systemd; a hung systemctl delays only the reset


def test_memguard_asks_systemd_nothing_while_memory_is_under_the_low_line_but_a_cached_value_still_applies(tmp_path):
    tool = lambda pid: [(pid, 20, "bash", "/bin/bash -c t%d" % pid)]
    prot = int(_vs()["PROTECT_OOM_ADJ"])
    adj, stops, runs, ev = _guard_pass(tmp_path / "low", _post_unit(), passes=2, avails=[3 * GIB, GIB // 2], spawn={1: tool(19)})
    assert ev.sysd == [] and _child(tmp_path / "low", 19) == prot, ev.sysd                 # low, no cache: no fetch, left as it is
    adj, stops, runs, ev = _guard_pass(tmp_path / "back", _post_unit(), passes=3, avails=[3 * GIB, GIB // 2, 3 * GIB], spawn={1: tool(19)})
    assert len(ev.sysd) == 1 and _child(tmp_path / "back", 19) == 0                       # memory back: the pending reset happens
    stale = int(_vs()["BASELINE_REFRESH_S"]) + 1
    adj, stops, runs, ev = _guard_pass(tmp_path / "cache", _post_unit(), passes=3, tick=stale, avails=[3 * GIB, 3 * GIB, GIB // 2],
                                       spawn={1: tool(19), 2: tool(18)}, sysd={_unit(): "OOMScoreAdjust=200\nNice=3\n"})
    assert len(ev.sysd) == 1 and _child(tmp_path / "cache", 18) == 200 and ev.nice[18] == 3, ev.sysd   # low + a stale cache: still applied, not refetched


def test_memguard_a_unit_whose_baseline_reads_again_gets_a_fresh_line_for_a_later_failure(tmp_path):
    tos = _vs()["MEMGUARD_ALERT_TO"].split(); stale = int(_vs()["BASELINE_REFRESH_S"]) + 1
    sysd = {_unit(): [OSError("down"), "OOMScoreAdjust=0\nNice=0\n", OSError("down again")]}
    spawn = {1: [(19, 20, "bash", "/bin/bash -c a")], 3: [(18, 20, "bash", "/bin/bash -c b")]}
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=4, tick=stale, spawn=spawn, sysd=sysd)
    for to in tos:
        said = [b[1].split(" ")[0] for b in ev.boxes if b[0][4] == "agi-" + to]
        assert said.count("[memguard-base]") == 2, (to, said)         # fail, read, fail: both failures named (the cooldown, 600 s, has passed)


def test_memguard_base_and_tree_alerts_are_rate_limited_per_unit_not_per_kind(tmp_path):
    tos = _vs()["MEMGUARD_ALERT_TO"].split()
    rows = _two_units(); spawn = {1: [(19, 20, "bash", "/bin/bash -c a"), (119, 120, "bash", "/bin/bash -c b")]}
    adj, stops, runs, ev = _guard_pass(tmp_path / "base", rows, passes=3, spawn=spawn, sysd={_unit(): OSError("x"), _unit_b(): OSError("y")})
    for to in tos:                                                    # two units, one cooldown window: one line EACH
        texts = [b[1] for b in ev.boxes if b[0][4] == "agi-" + to and b[1].startswith("[memguard-base]")]
        assert len(texts) == 2 and _unit() in " ".join(texts) and _unit_b() in " ".join(texts), (to, texts)
    rows = _two_units()
    for pid in (20, 120): rows[pid] = rows[pid][:1] + ("zzz-new --title-rewritten",) + rows[pid][2:]      # no harness found in either
    adj, kills, runs, ev = _guard_pass(tmp_path / "tree", rows, passes=2)
    for to in tos:
        texts = [b[1] for b in ev.boxes if b[0][4] == "agi-" + to and b[1].startswith("[memguard-tree]")]
        assert len(texts) == 2, (to, texts)


# 7h -- goal:g7.16.1.11.40.1.2 (council 3/3 alive 00:48:31Z 10-26, belam GO 00:5xZ): the 'no harness' ALERT fires only on the SECOND consecutive tick
# that finds the SAME incarnation's tracer without a harness. Each row has its MUTANT: the rendered guard with ONE site changed, which must break it.
NOH_STOP = "stop window"
HIDE = (20, "cmd", "zzz-new --title-rewritten")
_STOPW = "no harness for 1 tick, then the unit's cgroup emptied: a stop window"


def _cut(old, new):
    def f(src):
        assert src.count(old) == 1, ("mutant anchor not unique in the rendered guard", old)
        return src.replace(old, new)
    return f


def _alerts(runs): return [a[0][-1] for a in runs if "no harness found" in a[0][-1]]
def _said(runs, text): return [a[0][-1] for a in runs if text in a[0][-1]]


def _noh_same_id(tmp_path, mutate=None):
    """no harness on pass 0 AND pass 1, the same InvocationID: pass 0 is only remembered, pass 1 alerts, once."""
    adj, kills, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=3, rewrite={0: [HIDE]}, mutate=mutate)
    alerts = _alerts(runs)
    assert len(alerts) == 1 and all(len(t) == 1 for t in _tree_lines(ev)), (alerts, _tree_lines(ev))      # one journal line, one notice per recipient
    return ev


def test_memguard_no_harness_alerts_on_the_second_tick_of_the_same_incarnation_not_the_first(tmp_path):
    adj, kills, runs, ev = _guard_pass(tmp_path / "one", _post_unit(), passes=1, rewrite={0: [HIDE]})
    assert _alerts(runs) == [] and _tree_lines(ev) == [[]] * len(_tree_lines(ev)), _alerts(runs)             # the first tick is only remembered
    assert [n for _, n in ev.inv] == [[_unit()]], ev.inv                                                     # ONE read, for the one candidate
    _noh_same_id(tmp_path / "two")
    prot = int(_vs()["PROTECT_OOM_ADJ"])
    assert [adj[p] for p in (10, 11, 12)] == [prot] * 3, adj                                                 # the spine is protected through the pending tick


def test_mutant_no_harness_alerting_on_the_first_tick_reads_red(tmp_path):
    with pytest.raises(AssertionError):
        adj, kills, runs, ev = _guard_pass(tmp_path / "one", _post_unit(), passes=1, rewrite={0: [HIDE]},
                                           mutate=lambda src: _cut("elif i is not None and pending[unit] != i:", "elif i is not None and pending.get(unit, i) != i:")(
                                               _cut("if i is not None and unit not in pending: pending[unit] = i", "if False: pass")(src)))
        assert _alerts(runs) == [], _alerts(runs)


def test_mutant_a_count_that_starts_over_every_tick_never_alerts_and_reads_red(tmp_path):
    with pytest.raises(AssertionError):
        _noh_same_id(tmp_path, mutate=_cut("elif i is not None and pending[unit] != i:", "elif i is not None:"))


def test_memguard_one_tick_then_the_cgroup_empties_is_a_recorded_stop_window_and_not_red(tmp_path):
    gone = [(p, None) for p, r in _post_unit().items() if r[2] == _post_cg()]
    adj, kills, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=4, rewrite={0: [HIDE]}, flips={1: gone})
    assert _alerts(runs) == [] and _tree_lines(ev) == [[]] * len(_tree_lines(ev)), (_alerts(runs), _tree_lines(ev))
    said = _said(runs, NOH_STOP)
    assert len(said) == 1 and said[0].endswith(_STOPW), said                                                  # once per episode
    assert not any(b[1].startswith(("[memguard-tree]", "[memguard-stop")) for b in ev.boxes), [b[1] for b in ev.boxes]   # a line, never a notice
    assert "stop window" in (tmp_path / "guard.log").read_text()                                              # and the guard's own file has it


def test_mutants_the_stop_window_line_missing_or_red_or_never_cleared_read_red(tmp_path):
    gone = [(p, None) for p, r in _post_unit().items() if r[2] == _post_cg()]
    def run(mutate):
        adj, kills, runs, ev = _guard_pass(tmp_path / ("m%d" % run.n), _post_unit(), passes=4, rewrite={0: [HIDE]}, flips={1: gone}, mutate=mutate); run.n += 1
        assert len(_said(runs, NOH_STOP)) == 1 and _tree_lines(ev) == [[]] * len(_tree_lines(ev)), (_said(runs, NOH_STOP), _tree_lines(ev))
    run.n = 0
    run(None)
    for old, new in (("log(f'{unit}: no harness for 1 tick, then {why}: a stop window')", "pass"),                                   # recorded: no line
                     ("log(f'{unit}: no harness for 1 tick, then {why}: a stop window')", "log(f'{unit}: no harness for 1 tick, then {why}: a stop window', red=True, kind='tree')"),   # red
                     ("for unit in [u for u in pending if u not in posts]: cleared(unit, \"the unit's cgroup emptied\")", "pass")):   # an emptied cgroup is not noticed
        with pytest.raises(AssertionError):
            run(_cut(old, new))


def test_memguard_a_restart_that_changes_the_invocation_counts_afresh(tmp_path):
    iids = lambda: {_unit(): ["inc-a", "inc-b"]}                                  # pass 0 reads inc-a, pass 1 and on read inc-b
    adj, kills, runs, ev = _guard_pass(tmp_path / "r", _post_unit(), passes=3, rewrite={0: [HIDE]}, iids=iids())
    assert len(_alerts(runs)) == 1 and len(_said(runs, "the unit restarted: a stop window")) == 1, [a[0][-1] for a in runs]   # pass 1: recorded, not red; pass 2: the new incarnation's 2nd tick
    adj, kills, runs, ev = _guard_pass(tmp_path / "r1", _post_unit(), passes=2, rewrite={0: [HIDE]}, iids=iids())
    assert _alerts(runs) == [], _alerts(runs)                                     # two ticks, two incarnations: no line
    with pytest.raises(AssertionError):                                           # MUTANT: the id compared to nothing = the old noise
        adj, kills, runs, ev = _guard_pass(tmp_path / "m", _post_unit(), passes=2, rewrite={0: [HIDE]}, iids=iids(),
                                           mutate=_cut("elif i is not None and pending[unit] != i:", "elif False:"))
        assert _alerts(runs) == [], _alerts(runs)


def test_memguard_an_invocation_id_that_cannot_be_read_alerts_at_once_loud(tmp_path):
    for tag, bad in (("timeout", OSError("hung")), ("empty", "")):
        adj, kills, runs, ev = _guard_pass(tmp_path / tag, _post_unit(), passes=1, rewrite={0: [HIDE]}, iids={_unit(): bad})
        assert len(_alerts(runs)) == 1 and "InvocationID could not be read" in _alerts(runs)[0], (tag, _alerts(runs))
        assert all(len(t) == 1 for t in _tree_lines(ev)), _tree_lines(ev)
    with pytest.raises(AssertionError):                                           # MUTANT: an unreadable id is remembered as if it were one
        adj, kills, runs, ev = _guard_pass(tmp_path / "m", _post_unit(), passes=1, rewrite={0: [HIDE]}, iids={_unit(): OSError("hung")},
                                           mutate=_cut("if i is not None and unit not in pending: pending[unit] = i", "if unit not in pending: pending[unit] = i"))
        assert len(_alerts(runs)) == 1, _alerts(runs)


def test_memguard_a_young_unit_is_still_not_judged_and_asks_systemd_nothing(tmp_path):
    rows = _youngs(_post_unit(), 3); rows[20] = rows[20][:1] + ("zzz-new --title-rewritten",) + rows[20][2:]
    adj, kills, runs, ev = _guard_pass(tmp_path / "y", rows, passes=2)
    assert _alerts(runs) == [] and ev.inv == [], (_alerts(runs), ev.inv)
    with pytest.raises(AssertionError):                                           # MUTANT: young() no longer consulted
        adj, kills, runs, ev = _guard_pass(tmp_path / "m", rows, passes=2, mutate=_cut("elif young(rows): cleared(unit, 'the unit restarted')", "elif False: pass"))
        assert ev.inv == [], ev.inv


def test_memguard_an_unreadable_tree_is_the_tree_unread_alert_on_its_first_tick(tmp_path):
    cut = [(10, "ppid", 11), (30, "ppid", 21)]
    adj, kills, runs, ev = _guard_pass(tmp_path / "u", _post_unit(), passes=1, rewrite={0: cut})
    assert len(_said(runs, "could not be read")) == 1 and ev.inv == [], ([a[0][-1] for a in runs], ev.inv)    # no pending, no systemctl
    with pytest.raises(AssertionError):                                           # MUTANT: the unread waits for a second tick
        adj, kills, runs, ev = _guard_pass(tmp_path / "m", _post_unit(), passes=1, rewrite={0: cut},
                                           mutate=_cut("if unit not in unread and not young(rows): unread.add(unit)", "if unit not in unread and not young(rows) and unit in pending: unread.add(unit)"))
        assert len(_said(runs, "could not be read")) == 1


def test_memguard_the_invocation_read_is_one_call_for_all_units_after_the_stops_and_the_2_tick_rule_holds_under_a_low_line(tmp_path):
    rows = _two_units()
    for pid in (20, 120): rows[pid] = rows[pid][:1] + ("zzz-new --title-rewritten",) + rows[pid][2:]
    adj, kills, runs, ev = _guard_pass(tmp_path / "two", rows, passes=2)
    assert [sorted(n) for _, n in ev.inv] == [sorted([_unit(), _unit_b()])] * 2 and len(_alerts(runs)) == 2, (ev.inv, _alerts(runs))   # ONE call a tick, not one per unit
    LOWN = "judged under the low line, no InvocationID read"
    low = [GIB // 2] * 2                                                          # two ticks UNDER the low line: the 2-tick rule holds, systemd is asked NOTHING
    adj, kills, runs, ev = _guard_pass(tmp_path / "low", _post_unit(), passes=2, avails=low, rewrite={0: [HIDE]})
    assert ev.inv == [] and len(_alerts(runs)) == 1 and LOWN in _alerts(runs)[0] and all(len(t) == 1 for t in _tree_lines(ev)), (ev.inv, _alerts(runs))
    adj, kills, runs, ev = _guard_pass(tmp_path / "low1", _post_unit(), passes=1, avails=low[:1], rewrite={0: [HIDE]})
    assert _alerts(runs) == [] and ev.inv == [], _alerts(runs)                      # ONE low tick is only remembered
    gone = [(q, None) for q, r in _post_unit().items() if r[2] == _post_cg()]
    adj, kills, runs, ev = _guard_pass(tmp_path / "lowgone", _post_unit(), passes=3, avails=[GIB // 2] * 3, rewrite={0: [HIDE]}, flips={1: gone})
    assert _alerts(runs) == [] and len(_said(runs, NOH_STOP)) == 1 and ev.inv == [], (_alerts(runs), _said(runs, NOH_STOP))   # a cgroup emptied in between: the non-red stop-window line
    adj, kills, runs, ev = _guard_pass(tmp_path / "normal-then-low", _post_unit(), passes=2, avails=[3 * GIB, GIB // 2], rewrite={0: [HIDE]})
    assert len(ev.inv) == 1 and len(_alerts(runs)) == 1 and LOWN in _alerts(runs)[0], (ev.inv, _alerts(runs))
    adj, kills, runs, ev = _guard_pass(tmp_path / "low-then-normal", _post_unit(), passes=2, avails=[GIB // 2, 3 * GIB], rewrite={0: [HIDE]})
    assert len(ev.inv) == 1 and len(_alerts(runs)) == 1 and "first tick was judged under the low line" in _alerts(runs)[0], (ev.inv, _alerts(runs))
    with pytest.raises(AssertionError):                                           # MUTANT (d): the FIRST tick under the low line alerts
        adj, kills, runs, ev = _guard_pass(tmp_path / "md", _post_unit(), passes=1, avails=low[:1], rewrite={0: [HIDE]}, mutate=_cut("elif p is None: pending[unit] = i or ''; continue", "elif False: pass"))
        assert _alerts(runs) == [], _alerts(runs)
    with pytest.raises(AssertionError):                                           # MUTANT (b): an emptied cgroup is not noticed under the low line
        adj, kills, runs, ev = _guard_pass(tmp_path / "mb", _post_unit(), passes=3, avails=[GIB // 2] * 3, rewrite={0: [HIDE]}, flips={1: gone},
                                           mutate=_cut("for unit in [u for u in pending if u not in posts]: cleared(unit, \"the unit's cgroup emptied\")", "pass"))
        assert len(_said(runs, NOH_STOP)) == 1, _said(runs, NOH_STOP)
    for old, new in (("for unit in cand:\n            i = None if low", "for unit in ([] if low else cand):\n            i = None if low"),         # MUTANT: nothing is judged under the low line (the GATE265 defect)
                     ("ids = {} if low else invocations(cand)", "ids = invocations(cand)")):                                                    # MUTANT: systemd is read under the low line
        with pytest.raises(AssertionError):
            adj, kills, runs, ev = _guard_pass(tmp_path / ("m%d" % len(old)), _post_unit(), passes=2, avails=low, rewrite={0: [HIDE]}, mutate=_cut(old, new))
            assert ev.inv == [] and len(_alerts(runs)) == 1, (ev.inv, _alerts(runs))
    grow = {1: [(21, 7_000_000)]}                                                 # a runaway tool in the same tick: its SIGSTOP comes BEFORE the systemctl read
    adj, kills, runs, ev = _guard_pass(tmp_path / "stop", _post_unit(), passes=2, rewrite={0: [HIDE]}, grow=grow)
    order = [e[0] for e in ev.seq if e[0] in ("kill", "inv")]
    assert order.index("kill") < len(order) - 1 and order[-1] == "inv" and order.index("kill") < order.index("inv", order.index("kill")), order


PROOF2 = KIT / "memguard-proof2.py"


def _proof2(tmp_path, over=None, young=None, mut=None, nice=None, edit=None, spawn=None):
    """The guard runs 2 passes on the fake box (it sets the adj values); then the PROOF reads that fake /proc."""
    over = over or {}
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=2, over=over, spawn=spawn)
    proc = tmp_path / "proc"; (proc / "uptime").write_text("10000.00 0.00\n"); hz = os.sysconf("SC_CLK_TCK")
    for d in proc.iterdir():                                             # the fake kernel's nice, as the guard left it, into stat field 19
        if d.name.isdigit():
            t = (d / "stat").read_text(); head, tail = t[:t.rindex(")") + 2], t[t.rindex(")") + 2:].split()
            tail[16] = str((nice or {}).get(int(d.name), ev.nice.get(int(d.name), 0))); (d / "stat").write_text(head + " ".join(tail) + "\n")
    text = R.rendered(BY_NAME["memguard-script"], _vs(MEMGUARD_LOG=str(tmp_path / "g.log"), **over))
    if edit: assert text.count(edit[0]) == 1; text = text.replace(*edit)
    script = tmp_path / "guard.py"; script.write_text(text, encoding="utf-8")
    for pid, age in (young or {}).items():                             # (pid -> its age in s): the start time in stat field 22
        f = proc / str(pid) / "stat"; t = f.read_text()
        f.write_text(re.sub(r"( 0){17} \d+ ", lambda m: m.group(0).rsplit(" ", 2)[0] + " %d " % int((10000 - age) * hz), t, count=1))
    for pid, v in (mut or {}).items(): (proc / str(pid) / "oom_score_adj").write_text(str(v))
    r = subprocess.run([sys.executable, "-I", str(PROOF2), str(script), str(proc)], capture_output=True, text=True)
    return r.returncode, r.stdout


def test_memguard_proof2_exits_0_on_a_box_the_guard_has_classified_and_reads_the_guards_own_functions(tmp_path):
    rc, out = _proof2(tmp_path)
    assert rc == 0 and "0 on the wrong side" in out and "0 pids" not in out, out


def test_memguard_proof2_names_an_old_tool_that_holds_the_protect_value_and_an_old_spine_pid_that_lost_it(tmp_path):
    prot = int(_vs()["PROTECT_OOM_ADJ"])
    rc, out = _proof2(tmp_path / "tool", mut={21: prot})
    assert rc == 1 and "WRONG agi-post@a.service 21 adj %d nice 0 should NOT be protected" % prot in out, out
    rc, out = _proof2(tmp_path / "spine", mut={12: 0})
    assert rc == 1 and "WRONG agi-post@a.service 12 adj 0 nice -5 should be protected" in out, out


def test_memguard_proof2_skips_a_pid_younger_than_the_window_derived_from_the_guards_own_tick(tmp_path):
    prot = int(_vs()["PROTECT_OOM_ADJ"])
    rc, out = _proof2(tmp_path / "young", young={21: 3}, mut={21: prot})                       # 3 s old: not yet the guard's to have reset
    assert rc == 0 and "1 younger than 11 s skipped" in out, out
    rc, out = _proof2(tmp_path / "edge", young={21: 12}, mut={21: prot})                       # 12 s old with a 5 s tick: a real miss
    assert rc == 1 and "should NOT be protected" in out, out
    rc, out = _proof2(tmp_path / "slow", over={"INTERVAL_S": "7"}, young={21: 12}, mut={21: prot})   # the same 12 s with a 7 s tick: window 15, skipped
    assert rc == 0 and "1 younger than 15 s skipped" in out, out


def test_memguard_proof2_also_reads_nice_a_tool_that_inherited_it_and_a_spine_pid_that_lost_it_are_wrong(tmp_path):
    pn = int(_vs()["PROTECT_NICE"])
    rc, out = _proof2(tmp_path / "ok")
    assert rc == 0 and ev_ok(tmp_path / "ok", pn), out                                               # the harness really holds -5 in the fake kernel
    rc, out = _proof2(tmp_path / "tool", nice={21: pn})
    assert rc == 1 and "WRONG agi-post@a.service 21 adj 0 nice %d should NOT be protected" % pn in out, out
    rc, out = _proof2(tmp_path / "spine", nice={12: 0})
    assert rc == 1 and "WRONG agi-post@a.service 12" in out and "nice 0 should be protected" in out, out


def ev_ok(tmp_path, pn):
    t = (tmp_path / "proc" / "20" / "stat").read_text()
    return int(t[t.rindex(")") + 2:].split()[16]) == pn and (tmp_path / "proc" / "20" / "oom_score_adj").read_text() == _vs()["PROTECT_OOM_ADJ"]


def test_memguard_proof2_has_an_outside_witness_a_gutted_classifier_cannot_pass_it(tmp_path):
    prot = _vs()["PROTECT_OOM_ADJ"]
    rc, out = _proof2(tmp_path / "real")
    assert (tmp_path / "real" / "proc" / "20" / "oom_score_adj").read_text() == prot and rc == 0     # the harness (pid 20, by construction) is at the protect value
    rc, out = _proof2(tmp_path / "gutted", edit=("    out = set(chain)\n", "    out = set()\n"))    # a guard whose tree function protects nothing
    assert rc == 1 and all("WRONG agi-post@a.service %d adj %s nice -5 should NOT be protected" % (p, prot) in out for p in (10, 11, 12)), out   # the spine chain, by construction


def test_memguard_proof2_refuses_a_script_that_is_not_a_guard(tmp_path):
    (tmp_path / "x.py").write_text("print(1)\n"); (tmp_path / "proc").mkdir()
    r = subprocess.run([sys.executable, "-I", str(PROOF2), str(tmp_path / "x.py"), str(tmp_path / "proc")], capture_output=True, text=True)
    assert r.returncode == 2 and "NOT A GUARD" in r.stdout, (r.returncode, r.stdout)


def _sh(script, tmp_path, **env):
    """Run one of the committed act scripts under a bare env (a fake `sleep` first on PATH records its argument and returns)."""
    bindir = tmp_path / "fakebin"; bindir.mkdir(exist_ok=True)
    (bindir / "sleep").write_text('#!/bin/sh\necho "$1" >> "$SLEEPLOG"\n'); (bindir / "sleep").chmod(0o755)
    e = {"PATH": "%s:%s" % (bindir, os.environ["PATH"]), "HOME": str(tmp_path), "SLEEPLOG": str(tmp_path / "sleeps.log")}
    e.update({k: str(v) for k, v in env.items()})
    return subprocess.run(["sh", str(KIT / script)], env=e, capture_output=True, text=True)


_STUB_SYSTEMCTL = """#!/bin/sh
case "$*" in
  "is-active "*) echo "$HEALTH_ACTIVE"; [ "$HEALTH_ACTIVE" = active ];;
  *NRestarts*) echo "$HEALTH_NREST";;
  *ActiveEnterTimestamp*) [ -n "$HEALTH_SINCE" ] && echo "$HEALTH_SINCE";;
  *) echo "stub systemctl: $*";;
esac
"""
_STUB_JOURNALCTL = """#!/bin/sh
echo "$*" >> "${JARGS:-/dev/null}"
[ -z "$HEALTH_JEMPTY" ] || exit 0
echo "Oct 11 09:00:00 box systemd[1]: Started agi-memguard.service."
i=0; while [ "$i" -lt "${HEALTH_TB:-0}" ]; do echo "Traceback (most recent call last):"; i=$((i + 1)); done
[ "${HEALTH_JRC:-0}" = 0 ] || { echo "Failed to read the journal: permission denied" >&2; exit "$HEALTH_JRC"; }
"""
GO_SHA = "a" * 40


def _stubs(tmp_path, **health):
    """A healthy guard by default: stub systemctl / journalctl on disk, the health in HEALTH_* (active, NRestarts, tracebacks, since)."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    for n, t in (("systemctl", _STUB_SYSTEMCTL), ("journalctl", _STUB_JOURNALCTL)): (tmp_path / ("stub-" + n)).write_text(t); (tmp_path / ("stub-" + n)).chmod(0o755)
    h = dict(active="active", nrest="0", tb="0", since="Sun 2026-10-11 08:30:00 UTC", jrc="0", jempty=""); h.update(health)
    return dict(SYSTEMCTL=tmp_path / "stub-systemctl", JOURNALCTL=tmp_path / "stub-journalctl", SUDO="", HEALTH_ACTIVE=h["active"], HEALTH_NREST=h["nrest"],
                HEALTH_TB=h["tb"], HEALTH_SINCE=h["since"], HEALTH_JRC=h["jrc"], HEALTH_JEMPTY=h["jempty"], JARGS=tmp_path / "journalctl.args")


def _a2proof(tmp_path, codes, guard="time.sleep(5)\n", health=None, staged=GO_SHA, sha=GO_SHA, a2since=None, **env):
    """codes = the exit code each look of a STUB proof2 gives, in order (None = the proof file is absent)."""
    tmp_path.mkdir(parents=True, exist_ok=True); stage = tmp_path / "stage"; stage.mkdir(); (tmp_path / "guard.py").write_text(guard)
    (stage / "SHA").write_text(staged + "\n")
    if a2since: (stage / "a2.since").write_text(a2since + "\n")
    env = {**_stubs(tmp_path, **(health or {})), **({"SHA": sha} if sha else {}), **env}
    stub = tmp_path / "proof2-stub.py"
    if codes is not None:
        stub.write_text("import sys, pathlib\nc = pathlib.Path(%r)\nn = int(c.read_text()) if c.exists() else 0\nc.write_text(str(n + 1))\nsys.exit(%r[min(n, %d)])\n"
                        % (str(tmp_path / "count"), codes, len(codes) - 1))
    r = _sh("memguard-a2.proof.sh", tmp_path, PROOF_ONLY=2, STAGE=stage, GUARD=tmp_path / "guard.py", PROOF2=stub, **env)
    return r, stage


@pytest.mark.parametrize("codes,verdict,rc", [([0, 0], "PROVEN", 0), ([1, 0], "UNDO A2", 1), ([0, 1], "UNDO A2", 1), ([1, 2], "UNDO A2", 1),
                                              ([2, 2], "NOT PROVEN", 3), ([0, 2], "NOT PROVEN", 3), ([2, 0], "NOT PROVEN", 3), ([7, 0], "NOT PROVEN", 3),
                                              ([137, 0], "NOT PROVEN", 3), ([0, 124], "NOT PROVEN", 3), ([127, 0], "NOT PROVEN", 3),   # killed, timed out, not found
                                              ([10, 0], "NOT PROVEN", 3), ([0, 11], "NOT PROVEN", 3), ([11, 1], "UNDO A2", 1), ([1, 137], "UNDO A2", 1),
                                              (None, "NOT PROVEN", 3)])
def test_memguard_a2_proof_decides_proven_undo_or_not_proven_from_the_two_looks(tmp_path, codes, verdict, rc):
    r, stage = _a2proof(tmp_path, codes)
    assert r.returncode == rc and ("VERDICT: " + verdict) in r.stdout, (r.returncode, r.stdout)
    assert (stage / "not-proven.txt").exists() == (rc == 3)             # a line for the master, kept; and ONLY then
    if rc == 3: assert "UNDO" not in r.stdout.split("VERDICT:")[1].split("\n")[0].replace("NOT undone", "")


def test_memguard_a2_proof_gap_is_derived_from_the_installed_guard_never_a_literal(tmp_path):
    for tick, gap in (("5", "11.000"), ("7", "15.000"), ("0.5", "2.000")):
        r, stage = _a2proof(tmp_path / ("t" + tick), [0, 0], guard="x = 1\ntime.sleep(%s)\n" % tick)
        assert r.returncode == 0, r.stdout
        assert (tmp_path / ("t" + tick) / "sleeps.log").read_text().split() == [gap], tick     # one wait between the two looks (PROOF_ONLY=2)


def test_memguard_a2_proof_is_not_proven_when_the_gap_cannot_be_derived(tmp_path):
    r, stage = _a2proof(tmp_path / "nogap", [0, 0], guard="no tick here\n")
    assert r.returncode == 3 and "a=nogap b=nogap" in r.stdout and not (stage / "proof2a.out").exists(), r.stdout       # the proof is not even run on a guessed gap
    r, stage = _a2proof(tmp_path / "two", [0, 0], guard="time.sleep(5)\ntime.sleep(6)\n")
    assert r.returncode == 3 and "nogap" in r.stdout


def test_memguard_a2_proof_needs_the_go_sha_and_a_proof_from_the_wrong_bytes_proves_nothing_either_way(tmp_path):
    r, stage = _a2proof(tmp_path / "nosha", [0, 0], sha="")
    assert r.returncode == 3 and "set SHA" in r.stdout and not (stage / "proof2a.out").exists(), r.stdout                  # refused before any look; exit 1 stays UNDO's alone
    for i, codes in enumerate(([0, 0], [1, 0], [0, 1], [2, 2])):                                                           # a good, a wrong-side and a dead proof: all NOT PROVEN
        r, stage = _a2proof(tmp_path / ("wrong%d" % i), codes, staged="b" * 40)
        assert r.returncode == 3 and "not the GO sha" in r.stdout, (codes, r.returncode, r.stdout)
    r, stage = _a2proof(tmp_path / "right", [0, 0])
    assert r.returncode == 0 and "VERDICT: PROVEN" in r.stdout, r.stdout


@pytest.mark.parametrize("health", [dict(active="inactive"), dict(active="failed"), dict(active=""), dict(nrest="1"), dict(nrest="5"), dict(nrest=""), dict(tb="1"), dict(tb="3")])
def test_memguard_a2_proof_is_not_proven_when_the_guard_is_not_alive_even_if_proof_2_passes(tmp_path, health):
    r, stage = _a2proof(tmp_path, [0, 0], health=health)                  # a guard that set -900 on tick 1 and then died or crash-loops
    assert r.returncode == 3 and "the guard is not healthy" in r.stdout and (stage / "not-proven.txt").exists(), (health, r.returncode, r.stdout)


@pytest.mark.parametrize("health", [dict(jrc="1"), dict(jrc="2"), dict(jrc="141"), dict(jempty="1")])
def test_memguard_a2_proof_an_unreadable_journal_is_not_zero_tracebacks(tmp_path, health):
    r, stage = _a2proof(tmp_path, [0, 0], health=health)                     # journalctl / sudo fails, or answers nothing at all
    assert r.returncode == 3 and "tracebacks=unreadable" in r.stdout and "the guard is not healthy" in r.stdout, (health, r.returncode, r.stdout)


def test_memguard_a2_proof_reads_the_journal_since_the_a2_act_not_the_units_latest_start(tmp_path):
    r, stage = _a2proof(tmp_path / "act", [0, 0], a2since="2026-10-11T08:10:20Z")        # the unit's ActiveEnterTimestamp (stub) is 08:30:00: a restart moved it
    assert r.returncode == 0, r.stdout
    assert "--since 2026-10-11 08:10:20 UTC" in (tmp_path / "act" / "journalctl.args").read_text(), (tmp_path / "act" / "journalctl.args").read_text()
    r, stage = _a2proof(tmp_path / "unit", [0, 0])                                          # no a2.since: the unit's own start, as before
    assert "--since Sun 2026-10-11 08:30:00 UTC" in (tmp_path / "unit" / "journalctl.args").read_text()


def test_memguard_a2_proof_a_wrong_side_is_still_undo_whatever_the_guards_health(tmp_path):
    r, stage = _a2proof(tmp_path, [1, 0], health=dict(active="inactive"))
    assert r.returncode == 1 and "VERDICT: UNDO A2" in r.stdout, r.stdout


def _staged(tmp_path, tamper=False):
    stage = tmp_path / "stage"; (stage / "out").mkdir(parents=True)
    files = {"agi-memguard.py": "print('guard')\n", "agi-memguard.service": "[Unit]\n"}
    for n, t in files.items(): (stage / "out" / n).write_text(t)
    (stage / "out" / "SHA256SUMS").write_text("".join("%s  %s\n" % (hashlib.sha256(t.encode()).hexdigest(), n) for n, t in files.items()))
    if tamper: (stage / "out" / "agi-memguard.py").write_text("print('changed')\n")
    return stage


def test_memguard_a1_installs_the_staged_bytes_proves_them_and_refuses_a_tampered_stage_or_a_second_run(tmp_path):
    sb, ud = tmp_path / "sbin", tmp_path / "units"; sb.mkdir(); ud.mkdir()
    env = dict(SUDO="env", SBIN=sb, UNITDIR=ud, SYSTEMCTL="true", OWN="")
    stage = _staged(tmp_path)
    r = _sh("memguard-a1.sh", tmp_path, STAGE=stage, **env)
    assert r.returncode == 0 and "A1 OK" in r.stdout and (sb / "agi-memguard.py").stat().st_mode & 0o777 == 0o755 and (ud / "agi-memguard.service").stat().st_mode & 0o777 == 0o644, r.stdout + r.stderr
    r = _sh("memguard-a1.proof.sh", tmp_path, STAGE=stage, SBIN=sb, UNITDIR=ud)
    assert "PROOF A1.1 ok: installed bytes == staged bytes" in r.stdout, r.stdout + r.stderr
    r = _sh("memguard-a1.sh", tmp_path, STAGE=stage, **env)
    assert r.returncode == 1 and "A1 REFUSED: already installed" in r.stdout
    sb2, ud2 = tmp_path / "sbin2", tmp_path / "units2"; sb2.mkdir(); ud2.mkdir()
    (tmp_path / "t").mkdir(); stage2 = _staged(tmp_path / "t", tamper=True)
    r = _sh("memguard-a1.sh", tmp_path / "t", STAGE=stage2, **{**env, "SBIN": sb2, "UNITDIR": ud2})
    assert r.returncode != 0 and not list(sb2.iterdir()) and not list(ud2.iterdir()), r.stdout + r.stderr        # sha256sum -c refuses; nothing installed


def test_memguard_a2_undo_resumes_what_this_a2_stopped_across_a_restart_and_nothing_older(tmp_path):
    import signal, time
    before, crashed, running = (subprocess.Popen(["sleep", "30"]) for _ in range(3))
    try:
        for q in (before, crashed): os.kill(q.pid, signal.SIGSTOP)
        time.sleep(0.3)
        state = lambda p: Path("/proc/%d/stat" % p).read_text().rsplit(")", 1)[1].split()[0]
        assert state(before.pid) == "T" and state(crashed.pid) == "T" and state(running.pid) == "S"
        stage = tmp_path / "stage"; stage.mkdir(); (stage / "a2.since").write_text("2026-10-11T08:30:00Z\n")
        log = tmp_path / "guard.log"
        log.write_text("2026-10-11T08:00:00Z SUSPENDED pid %d (sleep, unit x): an EARLIER A2\n2026-10-11T08:40:00Z SUSPENDED pid %d (sleep, unit x): this A2, before the crash\n"
                       "2026-10-11T08:41:00Z SUSPENDED pid %d (sleep)\n2026-10-11T08:42:00Z SUSPENDED pid 999999 (gone)\n" % (before.pid, crashed.pid, running.pid))
        env = _stubs(tmp_path, since="Sun 2026-10-11 09:00:00 UTC")       # the unit RESTARTED at 09:00, after the stop at 08:40: the guard's own start time would skip it
        r = _sh("memguard-a2.undo.sh", tmp_path, STAGE=stage, LOG=log, **env)
        time.sleep(0.3)
        assert "resuming pid %d" % crashed.pid in r.stdout and "resuming pid %d" % running.pid not in r.stdout and "resuming pid %d" % before.pid not in r.stdout, r.stdout + r.stderr
        assert state(crashed.pid) == "S" and state(before.pid) == "T" and state(running.pid) == "S"      # an earlier A2's stop is left alone
        assert not (stage / "a2.since").exists()                                                     # the next A2 starts its own scope
        r = _sh("memguard-a2.undo.sh", tmp_path, STAGE=stage, LOG=log, **env)                          # no a2.since: nothing resumed, candidates listed
        time.sleep(0.3)
        assert "NOTHING resumed" in r.stdout and "pid %d" % before.pid in r.stdout and state(before.pid) == "T", r.stdout + r.stderr
    finally:
        for q in (before, crashed, running): q.kill(); q.wait()


def test_memguard_a2_writes_the_undo_scope_before_the_first_start_and_keeps_it_on_a_rerun(tmp_path):
    sb, ud = tmp_path / "sbin", tmp_path / "units"; sb.mkdir(); ud.mkdir(); stage = tmp_path / "stage"; stage.mkdir()
    stub = tmp_path / "stub-systemctl"
    stub.write_text('#!/bin/sh\n[ -s "$STAGE/a2.since" ] && echo "since-present-at-start: $*" >> "$LOGF" || echo "since-ABSENT-at-start: $*" >> "$LOGF"\n'); stub.chmod(0o755)
    env = dict(SUDO="", SYSTEMCTL=stub, SBIN=sb, UNITDIR=ud, STAGE=stage, LOGF=tmp_path / "calls.log")
    r = _sh("memguard-a2.sh", tmp_path, **env)
    assert r.returncode == 1 and "A1 has not run" in r.stdout and not (stage / "a2.since").exists(), r.stdout          # refused: nothing written
    (sb / "agi-memguard.py").write_text("x"); (ud / "agi-memguard.service").write_text("x")
    r = _sh("memguard-a2.sh", tmp_path, **env)
    assert r.returncode == 0, r.stdout + r.stderr
    first = (stage / "a2.since").read_text().strip()
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", first), first
    assert (tmp_path / "calls.log").read_text().strip() == "since-present-at-start: enable --now agi-memguard.service"      # written BEFORE the start
    (stage / "a2.since").write_text("2026-10-11T08:00:00Z\n")
    r = _sh("memguard-a2.sh", tmp_path, **env)
    assert (stage / "a2.since").read_text().strip() == "2026-10-11T08:00:00Z", "a re-run keeps the first stamp"


@pytest.mark.parametrize("name", ["a0", "a1", "a1.proof", "a1.undo", "a2", "a2.proof", "a2.undo", "restage"])
def test_memguard_act_scripts_parse(name):
    assert subprocess.run(["sh", "-n", str(KIT / ("memguard-%s.sh" % name))], capture_output=True).returncode == 0


def _mini_repo(tmp_path):
    """A tiny git repo holding what A0 reads (config, boxkit, fixtures, guard-init): MAIN for the A0 rows."""
    repo = tmp_path / "main"; (repo / ".agi").mkdir(parents=True)
    shutil.copy(PROJECT / ".agi" / "config.json", repo / ".agi" / "config.json")
    shutil.copytree(KIT, repo / "extensions/agi/boxkit", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(FIXTURES, repo / CELLS["fixtures_dir"])
    (repo / "extensions/agi/guard").mkdir(parents=True); shutil.copy(PROJECT / "extensions/agi/guard/guard-init.sh", repo / "extensions/agi/guard/guard-init.sh")
    g = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout.strip()
    g("init", "-q"); g("add", "-A"); g("commit", "-qm", "base")
    return repo, g


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_memguard_a0_stages_what_hashes_to_its_fixtures_and_refuses_a_template_that_does_not(tmp_path):
    repo, g = _mini_repo(tmp_path); sha = g("rev-parse", "HEAD")
    stage = tmp_path / "memguard-A0"
    r = _sh("memguard-a0.sh", tmp_path, SHA=sha, STAGE=stage, MAIN=repo)
    assert r.returncode == 0 and "A0 OK" in r.stdout, r.stdout + r.stderr
    assert "C1 memguard-script" in r.stdout and "C1 memguard-service" in r.stdout
    assert (stage / "SHA").read_text().strip() == sha and (stage / "out" / "SHA256SUMS").is_file()
    assert (stage / "src/extensions/agi/boxkit/memguard-proof2.py").is_file() and (stage / "src/extensions/agi/boxkit/memguard-a2.proof.sh").is_file()   # the acts ride the archive
    t = repo / "extensions/agi/boxkit/templates/memguard-script.tmpl"; t.write_text(t.read_text().replace("stays stopped", "stays STOPPED", 1))
    g("commit", "-qam", "tamper"); bad = g("rev-parse", "HEAD")
    r = _sh("memguard-a0.sh", tmp_path, SHA=bad, STAGE=tmp_path / "memguard-A0-bad", MAIN=repo)
    assert r.returncode == 1 and "A0 REFUSED (C1)" in r.stdout and not (tmp_path / "memguard-A0-bad" / "out" / "agi-memguard.py").exists(), r.stdout
    for bogus in ("main", "abc123", "Z" * 40):
        r = _sh("memguard-a0.sh", tmp_path, SHA=bogus, STAGE=tmp_path / "memguard-A0-x", MAIN=repo)
        assert r.returncode == 1 and "A0 REFUSED" in r.stdout, (bogus, r.stdout)
    # rm -rf runs on STAGE: only a directory under HOME named memguard-A0*, no '..', never HOME or / -- and the victim is untouched
    victim = tmp_path / "victim"; victim.mkdir(); (victim / "keep.txt").write_text("x")
    (tmp_path / "memguard-A0" / "inner").mkdir(exist_ok=True)
    for bad_stage in (victim, tmp_path, tmp_path / "memguard-A0" / ".." / "victim", "/tmp/memguard-A0-elsewhere", "/", tmp_path / "other-A0", tmp_path / "x" / "memguard-A0"):
        r = _sh("memguard-a0.sh", tmp_path, SHA=sha, STAGE=bad_stage, MAIN=repo)
        assert r.returncode == 1 and "A0 REFUSED" in r.stdout and "STAGE" in r.stdout, (str(bad_stage), r.stdout)
        assert (victim / "keep.txt").exists() and (tmp_path / "memguard-A0" / "SHA").exists(), str(bad_stage)
    for home in ("/", ""):                                                                    # HOME empty makes "/memguard-A0*" match: that is the check's job
        r = _sh("memguard-a0.sh", tmp_path, SHA=sha, STAGE=Path(home + "/memguard-A0-test"), MAIN=repo, HOME=home)
        assert r.returncode == 1 and "A0 REFUSED" in r.stdout, (home, r.stdout)
    assert (tmp_path / "memguard-A0" / "SHA").exists()


def test_memguard_says_a_tree_it_cannot_read_once_per_unit(tmp_path):
    rows = _post_unit(); rows[10] = rows[10][:3] + (11,) + rows[10][4:]; rows[30] = rows[30][:3] + (21,) + rows[30][4:]   # no process of the unit has a parent outside it
    adj, stops, runs, ev = _guard_pass(tmp_path, rows, passes=3)
    said = [a[0][-1] for a in runs if "could not be read" in a[0][-1]]
    assert len(said) == 1, said


def test_memguard_with_no_harness_found_protects_only_the_spine_chain_and_alerts(tmp_path):
    rows = _post_unit()
    rows[20] = rows[20][:1] + ("zzz-new --title-rewritten",) + rows[20][2:]      # the harness rewrote its argv
    adj, kills, runs, ev = _guard_pass(tmp_path, rows, passes=2)         # the 2nd consecutive tick is the one that alerts (goal:g7.16.1.11.40.1.2)
    prot = int(_vs()["PROTECT_OOM_ADJ"])
    assert [adj[p] for p in (10, 11, 12)] == [prot] * 3, adj     # the chain down to the tracer
    assert [adj[p] for p in (13, 15, 20, 21)] == [0, 0, 0, 0], adj    # nothing else: the harness cannot be told from a tool
    assert any("no harness found" in a[0][-1] for a in runs), [a[0][-1] for a in runs]   # an unidentified harness alerts by name
    assert kills == [], kills



# 7d -- FIXTURE PROVENANCE. By design no committed test may read a live unit, so nothing
# here ties a committed fixture to the bytes it claims to record: the parent probe is the
# only witness, and a probe is not a gate. So every manifest row carries the
# fixture_sha256 of the fixture FILE BYTES AS COMMITTED, and this row says whether the
# file on disk is still those bytes -- computed here, never hand-typed. A fixture edited
# in place is RED. It can only say the file is UNCHANGED: that the unchanged file records
# a live unit stays a probe.
def test_every_committed_fixture_still_hashes_to_its_manifest_cell():
    rows = {p["name"] for p in PIECES}
    stray = sorted(f.stem for f in FIXTURES.glob("*.fixture") if f.stem not in rows)
    assert not stray, ("a fixture on disk with no manifest row carries no declared "
                       "delta and no provenance cell: %s" % stray)
    bad = []
    for piece in PIECES:
        fix = FIXTURES / (piece["name"] + ".fixture")
        assert fix.is_file(), "%s: manifest row names a fixture that is not there" % fix
        got = hashlib.sha256(fix.read_bytes()).hexdigest()
        want = piece["fixture_sha256"]
        if got != want:
            bad.append((piece["name"], want, got))
    assert not bad, "\n".join(
        "%s: manifest fixture_sha256 %s but the committed file hashes to %s -- the "
        "fixture is not the bytes the manifest records; re-record it with the parent "
        "probe or restore the file" % (n, w, g) for n, w, g in bad)
    # a cell that is not a sha256 digest is a lie about the file, not a hash mismatch
    for piece in PIECES:
        assert re.fullmatch(r"[0-9a-f]{64}", piece["fixture_sha256"]), piece["name"]


# 7b -- the identity roots are DERIVED (director rules 2 and 3), never cells: the repo
# is the running engine's checkout (through a linked worktree's .git FILE, no git
# subprocess) and the guard dir is the committed paths.boxkit.guard_dir cell.
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


# 9 -- new_bytes means NEW TO THE KIT: these bytes were authored here, not copied
# from an installed file. It is not a statement about this box, so this test asserts
# neither presence nor absence of a live counterpart -- it asserts only that the flag
# says what it means and steers the one thing it steers: the falsifier's LIVE set.
def test_new_bytes_rows_are_flagged_and_excluded_from_the_live_comparison():
    rows = [p for p in PIECES if p.get("new_bytes")]
    assert {p["name"] for p in rows} == set(DRIFT_ROWS) | {"agi-survival-conf", "agi-vm-sysctl"}
    assert not [p for p in rows if p in LIVE], "a new_bytes row must not be compared as a copy"
    assert len(LIVE) == len(PIECES) - len(rows)
    for p in rows:
        assert ("vm.vfs_cache_pressure = " if p["name"] == "agi-vm-sysctl" else "OOMPolicy=") in R.rendered(p, _v()), p["name"]


# 10 -- the no-cascade coverage closure (kid a00-057a8121). The goal TABLE is the spec,
# read from the live node -- a copied list in this file is the exact defect found.
GOAL = PROJECT / ".agi" / "nodes" / "goal" / "g7.33.18.md"


def _no_cascade_units():
    row = [ln for ln in GOAL.read_text(encoding="utf-8").splitlines()
           if ln.strip().startswith("| no cascade")]
    assert len(row) == 1, "goal:g7.33.18 must carry exactly one no-cascade row"
    col = [c for c in row[0].split("|") if " on " in c]
    assert len(col) == 1, col
    tail = col[0].split(" on ", 1)[1]
    return [u.strip().strip("`") for u in tail.split(",") if u.strip()]


def _user_unit_dir_cell():
    """The committed paths.boxkit cell that resolves to the USER unit dir the goal's own
    world-after line names. A no-cascade drop-in artifact means a file under that dir;
    both the cell and the dir are read, never a literal in this file."""
    m = re.search(r"[\w./~-]*systemd/user\b", GOAL.read_text(encoding="utf-8"))
    assert m, "the goal must name the user unit dir its no-cascade row rides"
    tail = m.group(0).lstrip("~/")
    cells = [c for c, v in CELLS.items() if str(v).endswith(tail)]
    assert cells, "no committed paths.boxkit cell resolves to %s" % tail
    assert len(cells) == 1, ("%s resolves to more than one committed cell (%s); picking "
                             "one silently would check the no-cascade artifacts against a "
                             "dir the goal does not name" % (tail, cells))
    return cells[0]


def _drop_ins_for(unit):
    return [p for p in PIECES if p["dest_rel"].startswith(unit + ".service.d/")]


@pytest.mark.parametrize("unit", _no_cascade_units())
def test_manifest_covers_every_unit_the_goal_no_cascade_row_names(unit):
    rows = _drop_ins_for(unit)
    assert rows, ("goal:g7.33.18 names %s in its no-cascade row but no manifest row "
                  "ships a drop-in for it" % unit)
    v = _v()
    rendered = [R.rendered(row, v) for row in rows]
    # the unit's no-cascade layer rides the CONFIGURED OOM_POLICY, never a literal
    assert any("OOMPolicy=" + CFG["values"]["boxkit"]["OOM_POLICY"] in out for out in rendered), rows
    assert all(p["reload"] in ("system", "user") and p["mode"] == "0644" for p in rows)
    # the no-cascade drop-in lands in the USER unit dir as 10-agi-survival.conf --
    # the name and dir goal:g7.33.18's row carries, not 50- under /etc
    for p in rows:
        if not p.get("new_bytes"):
            continue
        assert p["dest_cell"] == "user_systemd_dir", (p["name"], p["dest_cell"])
        assert p["dest_rel"] == unit + ".service.d/10-agi-survival.conf", (p["name"], p["dest_rel"])
        assert p["reload"] == "user" and p["sudo"] is False, p["name"]


@pytest.mark.parametrize("unit", _no_cascade_units())
def test_no_cascade_drop_in_matches_the_recorded_live_bytes_or_names_its_absence(unit):
    """The coverage closure: every unit goal:g7.33.18's no-cascade row names carries a
    new_bytes drop-in whose RECORDED LIVE bytes (the anonymized fixture) carry the same
    payload the kit renders, and differ from it by EXACTLY the delta the manifest
    declares, line for line. A box with no recorded live bytes is a NAMED skip, never a
    silent pass. This reads FIXTURES only -- the live-unit comparison is the probe."""
    rows = [r for r in _drop_ins_for(unit) if r.get("new_bytes")]
    if not rows:
        pytest.skip("unit %s has no new_bytes no-cascade row in the kit" % unit)
    v = _vs()
    absent = [r["name"] for r in rows if not (FIXTURES / (r["name"] + ".fixture")).is_file()]
    if absent:
        pytest.skip("no RECORDED live bytes for the no-cascade drop-in(s) %s of unit %s "
                    "(the kit is portable); the parent must run the live probe and record them"
                    % (", ".join(absent), unit))
    for row in rows:
        assert row["name"] in DRIFT_ROWS, (row["name"], "a no-cascade drop-in with a recorded "
                                              "live file and no drift cell declares nothing")
        live = (FIXTURES / (row["name"] + ".fixture")).read_text(encoding="utf-8")
        _assert_declared_drift(row, R.rendered(row, v), live, v)
        # the whole live record is accounted for: its only comments are the declared
        # live_only lines, so a new unexplained comment in the live file is RED.
        comments = [ln for ln in live.splitlines() if ln.lstrip().startswith("#")]
        assert comments == _declared(row, "live_only_lines", v), (row["name"], comments)


# 11 -- THE WHOLE-TABLE COVERAGE CLOSURE. Row 10 closes the no-cascade layer alone. The
# CLAIM is wider: "every piece of goal:g7.33.18's table is a template + manifest entry".
# Nothing made that true for the OTHER rows: the manifest lists itself, so DELETING a
# manifest row removes the piece and every other row stays green -- a coverage hole of the
# exact shape the claim is about. This row reads the goal TABLE (the live node row 10
# reads, never a copied list), takes the file-shaped artifacts each shipping row names,
# normalises the goal's literal uid to {{UID}}, and requires a manifest row for each.
def _goal_rows():
    body = [ln for ln in GOAL.read_text(encoding="utf-8").splitlines()
            if ln.strip().startswith("|")]
    assert body and "---" in body[1], "goal:g7.33.18 must carry a markdown table"
    return [[c.strip() for c in ln.split("|")[1:-1]] for ln in body[2:]
            if ln.count("|") >= 4]


# a file or unit a table row can name: an absolute live path, a drop-in under a
# slice/unit dir, a bare unit, or one of the two files this layer ships by name
ARTIFACT = re.compile(
    r"/[\w.@/-]+"                                              # /usr/local/sbin/agi-memguard.py
    r"|(?:[\w@.-]+/)*[\w.@*-]+\.(?:service|slice|conf|py|sh)"  # oomd.conf.d/50-...conf, user.slice
)
# the layers the goal itself records as NOT files the kit installs
NOT_A_FILE = ("already graph-declared", "config cells", "the read-back", "rides ")


def _norm(art):
    """The goal writes the local-town uid literally; the kit carries it as {{UID}}."""
    return re.sub(r"(user[@-])\d+", r"\1{{UID}}", art)


def _required_artifacts():
    """[(row label, artifact)] for every table row that claims the kit ships a FILE."""
    out = []
    for cells in _goal_rows():
        if any(s in cells[2].lower() for s in NOT_A_FILE):
            continue
        for art in ARTIFACT.findall(cells[0] + " " + cells[1]):
            out.append((cells[0], _norm(art.rstrip(".,"))))
    return out


def _shipped_paths(pieces):
    """Every manifest row's LIVE destination, repo-relative and cell-joined: the path a
    rendered piece lands on, the only thing the goal table names. The goal writes the live
    ABSOLUTE path, the cell is repo-relative with a leading /: both forms of one
    destination, so both are compared."""
    out = []
    for p in pieces:
        rel = p["dest_rel"]
        cell = str(CELLS[p["dest_cell"]]).lstrip("/")
        out.append((p, rel, "/".join(x for x in (cell, rel) if x)))
    return out


# a systemd UNIT drop-in dir (`foo.service.d`, `user.slice.d`, `agi-.slice.d`) and a
# systemd unit dir cell. A `*.conf.d` dir (oomd.conf.d) is neither: it lives under a
# config dir -- what the general branch could not see, comparing dest_rel alone.
UNIT_DROPIN = re.compile(r"[\w@{}%.-]+\.(service|slice|timer|scope|mount|socket|target)\.d$")
# a committed paths.boxkit cell that resolves to a systemd UNIT dir: one whose value ends in
# a two-component dir UNDER systemd/. Structure, not a name -- the tails are read from
# CELLS at CALL time (row 11g), so a cell rename moves the rule instead of inverting it.
UNIT_DIR_CELL = re.compile(r"/systemd/(?![\w.@%{}$-]*\.d$)[\w.@%{}$-]+$")


def _unit_dir_tails():
    return frozenset(m.group(0).lstrip("/") for v in CELLS.values()
                     for m in [UNIT_DIR_CELL.search(str(v))] if m)


def _cell_fits_dir(p, art):
    """The CELL side of a relative artifact: a `UNIT.d` dir is shipped under a systemd
    unit dir, any other dir under a config dir. A BARE artifact names no dir."""
    rel = art.lstrip("/")
    return True if "/" not in rel else \
        bool(UNIT_DROPIN.search(rel.split("/")[0])) == \
        str(CELLS[p["dest_cell"]]).lstrip("/").endswith(tuple(_unit_dir_tails()))


def _uncovered(required, pieces):
    """The artifacts no manifest row ships, as (row label, artifact).

    A unit/slice name ships its drop-in DIRECTORY for it (user.slice ->
    user.slice.d/...); a file ships the destination that IS or ENDS with it. A BARE
    filename the goal names PER UNIT (10-agi-survival.conf) ships as a drop-in for one
    of that row's units, in the unit dir the goal NAMES (probe P1).

    The GENERAL branch checks the DESTINATION, not a suffix of it (probe P5), and BOTH
    halves: the artifact is a path RELATIVE to one dir, so a piece satisfies it only
    when its dest_rel IS that path AND its dest_cell is that dir's cell
    (_cell_fits_dir); the old `live.endswith("/" + a)` admitted any dest_cell and any
    deeper rel, and never read the cell. Cells come from _shipped_paths, not literals."""
    out = []
    units = _no_cascade_units()
    for label, art in required:
        a = art.lstrip("/")
        paths = _shipped_paths(pieces)
        if "/" not in a and label.strip().lower().startswith("no cascade"):
            cell = _user_unit_dir_cell()
            hit = any(rel == "%s.service.d/%s" % (u, a) and p["dest_cell"] == cell
                      for p, rel, live in paths for u in units)
        else:
            # a live path the goal writes absolutely is the destination itself; a
            # relative one is the dest_rel, in whatever cell that rel belongs to --
            # a suffix match across cells is what P5 was.
            hit = any(a == live
                      or ((art == rel or rel.startswith((art + "/", art + ".")))
                          and _cell_fits_dir(p, art))
                      for p, rel, live in paths)
        if hit:
            continue
        out.append((label, art))
    return out


def test_manifest_covers_every_file_the_goal_table_names():
    required = _required_artifacts()
    # the extractor is not vacuous: the table names more files than one row, and more
    # than the no-cascade row alone (a parser that found nothing would be green above)
    assert len({a for _, a in required}) >= 10, sorted(a for _, a in required)
    assert {a for _, a in required} >= {
        "user@{{UID}}.service.d/50-sanctuary-guard.conf", "oomd.conf.d/50-sanctuary-guard.conf",
        "user.slice", "user-{{UID}}.slice", "system.slice", "agi.slice",
        "/usr/local/sbin/agi-memguard.py", "agi-memguard.service",
        "10-agi-survival.conf", "/etc/watchdog.conf", "/usr/local/sbin/sanctuary-health"}, \
        sorted(a for _, a in required)
    missing = _uncovered(required, PIECES)
    assert not missing, (
        "goal:g7.33.18's table names %s and no manifest row ships it: the kit does not "
        "cover the whole table the claim names" % missing)


def test_the_whole_table_closure_is_red_when_a_piece_is_removed():
    """The anti-circular proof the closure needs: coverage asserted over a manifest that
    lists ITSELF is green by construction, so the closure must go RED on the manifest it
    would have to read. Dropping every row uncovers every artifact; dropping ONE row
    uncovers exactly what that row carried and nothing else."""
    required = _required_artifacts()
    assert {a for _, a in _uncovered(required, [])} == {a for _, a in required}
    rest = [p for p in PIECES if p["name"] != "oomd-guard"]
    gone = [a for _, a in _uncovered(required, rest)]
    assert gone == ["oomd.conf.d/50-sanctuary-guard.conf"], gone
    assert len(rest) == len(PIECES) - 1


# 11b -- THE PER-UNIT NO-CASCADE CASE: a same-named file under ANOTHER dest_cell must
# not satisfy a bare-filename artifact. The goal names 10-agi-survival.conf PER UNIT (as
# <unit>.service.d/10-agi-survival.conf); a top-level file of that name in any cell is a
# different piece. The suffix match admitted it (experiment:a00-b90527fa, accepted).
def test_a_same_named_file_in_another_dest_cell_does_not_satisfy_a_no_cascade_artifact():
    artifact = "10-agi-survival.conf"
    elsewhere = dict(BY_NAME["agi-survival-conf"], dest_cell="systemd_system_dir")
    assert _uncovered([("no cascade", artifact)], [elsewhere]), (
        "a top-level %s in another dest_cell satisfied the per-unit artifact" % artifact)
    # the row that DOES ship it: the drop-in for a unit the goal names
    assert _uncovered([("no cascade", artifact)],
                      [BY_NAME["claude-remote-control-no-cascade"]]) == []


# 11c -- THE WRONG-CELL DROP-IN DECOY (probe P1). 11b rejected only a TOP-LEVEL
# same-named file in another cell. The surviving shape is a piece whose dest_rel IS the
# per-unit drop-in path while its dest_cell points at the SYSTEM unit dir.
def test_a_drop_in_in_the_wrong_unit_dir_does_not_satisfy_a_no_cascade_artifact():
    artifact = "10-agi-survival.conf"
    unit = _no_cascade_units()[0]
    cell = _user_unit_dir_cell()
    decoy = dict(BY_NAME["claude-remote-control-no-cascade"], dest_cell="systemd_system_dir")
    assert decoy["dest_rel"] == "%s.service.d/%s" % (unit, artifact), decoy["dest_rel"]
    assert cell != "systemd_system_dir", cell
    assert _uncovered([("no cascade", artifact)], [decoy]), (
        "a drop-in for %s in the SYSTEM unit dir satisfied the no-cascade artifact, "
        "which the goal names for the user unit dir (%s)" % (unit, cell))


# 11d -- THE GENERAL BRANCH'S WRONG-CELL / DEEPER-REL DECOY (probe P5). The general
# branch -- the one the whole-table closure leans on -- matched on
# `live.endswith("/" + a)`, admitting ANY dest_cell and any deeper rel: the goal names a
# drop-in path RELATIVE to one directory. The decoy's cell is a committed one from config.
def test_a_deeper_rel_in_another_dest_cell_does_not_satisfy_a_table_artifact():
    artifact = "oomd.conf.d/50-sanctuary-guard.conf"
    decoy = dict(BY_NAME["oomd-guard"], dest_cell="systemd_system_dir")
    decoy["dest_rel"] = "deep/dir/" + decoy["dest_rel"]
    assert decoy["dest_rel"] != BY_NAME["oomd-guard"]["dest_rel"], decoy["dest_rel"]
    assert _uncovered([("oomd row", artifact)], [decoy]), (
        "the same drop-in under a deeper rel in another dest_cell satisfied the table "
        "artifact the goal names under one directory")
    # the row that DOES ship it, exactly where the goal names it
    assert _uncovered([("oomd row", artifact)], [BY_NAME["oomd-guard"]]) == []


# 11f -- THE GENERAL BRANCH'S CELL SIDE. 11d moved the REL; this row holds the rel
# EXACTLY as the goal names it and moves only dest_cell: RED against the branch as it
# stood (checked by restoring it), green now that the branch reads the cell.
def test_the_right_dest_rel_in_the_wrong_dest_cell_does_not_cover_a_table_artifact():
    artifact = "oomd.conf.d/50-sanctuary-guard.conf"
    decoy = dict(BY_NAME["oomd-guard"], dest_cell="systemd_system_dir")
    assert decoy["dest_rel"] == artifact, decoy["dest_rel"]  # the REL is not the variable
    assert _uncovered([("oomd row", artifact)], [decoy]), \
        "the right rel in a systemd UNIT dir covered an artifact of the CONFIG dir"
    assert _uncovered([("oomd row", artifact)], [BY_NAME["oomd-guard"]]) == []
    # the other polarity of the same rule: a UNIT.d dir under a bare config dir
    unit_art = "user.slice.d/50-sanctuary-guard.conf"
    assert _uncovered([("slices row", unit_art)],
                      [dict(BY_NAME["user-slice-guard"], dest_cell="systemd_conf_dir")])
    assert _uncovered([("slices row", unit_art)], [BY_NAME["user-slice-guard"]]) == []


# 11e -- THE cells[0] TIE. _user_unit_dir_cell returned the FIRST committed cell whose
# value ends in the goal's unit dir, so a second cell with the same tail would silently
# change which dir the no-cascade artifacts are checked against. It must refuse BY NAME,
# and the refusal is planted here, not assumed.
def test_the_user_unit_dir_cell_refuses_when_two_committed_cells_share_a_tail(monkeypatch):
    # a config that declares the same dir twice: two cells, one tail
    tied = dict(CELLS)
    tied["shadow_user_unit_dir"] = CELLS[_user_unit_dir_cell()]
    assert len([c for c, v in tied.items() if v == tied["shadow_user_unit_dir"]]) == 2
    monkeypatch.setitem(globals(), "CELLS", tied)
    with pytest.raises(AssertionError):
        _user_unit_dir_cell()


# 11g -- the fit rule is DERIVED from the committed cells, not a literal copy of two
# tails: a rename inverted `_cell_fits_dir` silently (RED against the copy, below).
def test_the_unit_dir_fit_rule_follows_the_committed_cells(monkeypatch):
    tails = _unit_dir_tails()
    assert tails, "no committed cell is a unit dir: the rule would reject every drop-in"
    piece = BY_NAME["user-slice-guard"]                      # a UNIT.d drop-in
    assert _cell_fits_dir(piece, piece["dest_rel"]), piece["dest_cell"]
    # the rule is narrowed to UNIT dirs, not every component under systemd/: a drop-in
    # dir (etc/systemd/system.conf.d) is a CONFIG dir, and reading it as a unit dir would
    # ACCEPT a piece the literal tails rejected (DH.591 item 5).
    monkeypatch.setitem(CELLS, "boxkit_conf_dropin_dir", "etc/systemd/system.conf.d")
    assert "systemd/system.conf.d" not in _unit_dir_tails(), "a drop-in dir read as a unit dir"
    renamed = {c: ("etc/" + str(v).rstrip("/").split("/")[-1]
                   if str(v).endswith(tuple(tails)) else v) for c, v in CELLS.items()}
    monkeypatch.setitem(globals(), "CELLS", renamed)
    assert not _unit_dir_tails(), "a renamed cell is still read as a unit dir"
    assert not _cell_fits_dir(piece, piece["dest_rel"]), "a literal copy of the tails"


# LEGACY_ORACLE, not a live rule: row 12 pins its WRONG answer only to prove _leak_roots.
def _leak_roots_by_depth(project):  # LEGACY_ORACLE -- correcting it reds row 12
    """The OLD `len(p.parts) >= 3` rule, inline: row 12 pins a shape the rules DISAGREE on."""
    return sorted({str(p) for p in [project] + list(Path(project).parents[1:3])
                   if str(p) not in SHARED_ROOTS and len(p.parts) >= 3})


# 12 -- LEAK_ROOTS EXCLUDES SHARED ROOTS BY NAME, NOT BY DEPTH (residue M2). The old
# rule dropped the CHECKOUT'S OWN root on a shallow extract, so the row reported no leak
# in a template that names the checkout. The DISCRIMINATING shape is a ONE-COMPONENT
# checkout (Path("/a").parts == ("/", "a")).
def test_leak_roots_keep_a_shallow_checkout_and_exclude_only_shared_roots():
    shallow, keep = Path("/a"), "/a"
    roots, old = _leak_roots(shallow), _leak_roots_by_depth(shallow)
    assert set(old) != set(roots), (old, roots)
    assert keep in roots and keep not in old, (roots, old)
    # a template naming this checkout IS a leak under the new rule, invisible to the old
    assert _leaks("cd %s and ls\n" % keep, roots) == [keep]
    assert _leaks("cd %s and ls\n" % keep, old) == [], "the old rule's wrong answer"
    for deeper, kept in ((Path("/a/b"), "/a/b"), (Path("/b"), "/b"),
                         (Path("/tmp/extract/agi"), "/tmp/extract/agi")):
        r = _leak_roots(deeper)
        assert kept in r and not [x for x in r if x in SHARED_ROOTS], (str(deeper), r)
        assert _leaks("cd %s and ls\n" % kept, r) == [kept]
    # the empty-prefix false red the shared-root exclusion is for: a bare top-level dir
    # is a prefix of every absolute path, so admitting it makes every template a leak
    benign = "ExecStart=/usr/local/bin/agi-slice start\n"
    assert _leaks(benign, ["/tmp/extract/agi"]) == []
    assert _leaks(benign, ["/tmp/extract/agi", "/tmp", "/"]) != []
    # and the live set for THIS box is free of the shared roots
    assert not [r for r in LEAK_ROOTS if r in SHARED_ROOTS], LEAK_ROOTS


# 13 -- STAND-IN SUBSTITUTION IS LONGEST-FIRST (residue N1). Two identity tokens can
# overlap on one box; the shorter must not eat the longer's prefix. No planted
# overlapping pair existed here, so this row plants one and asserts the RESULT.
def test_stand_in_substitution_is_longest_first_over_overlapping_tokens():
    # two OVERLAPPING derived tokens, neither of which collides with a stand-in
    mapping = {"OWNER_USER": "/srv/owner", "REPO_ROOT": "/srv/owner/ext"}
    text = "prefix /srv/owner/ext/send.py and /srv/owner/home"
    got = _substitute_longest_first(text, mapping)
    assert got == "prefix %s/send.py and %s/home" % (STANDINS["REPO_ROOT"],
                                                      STANDINS["OWNER_USER"]), got
    # the identity order this replaced corrupts the long site -- a falsifier, not a
    # restatement of the helper: if the two orders agreed, this row could not fail
    naive = text
    for k in sorted(mapping):
        naive = naive.replace(mapping[k], STANDINS[k])
    assert naive != got, naive
    assert STANDINS["REPO_ROOT"] not in naive and mapping["REPO_ROOT"] not in naive
    # the shape longest-first cannot fix: a stand-in that collides with a token, which
    # would be a red fixture on a live box rather than a red edit here
    assert not [k for k in mapping if any(mapping[j] in STANDINS[k]
                                          for j in mapping if j != k)], STANDINS
    # the empty/derived token is skipped, never replaced into every string
    assert _substitute_longest_first("unchanged", {"OWNER_USER": ""}) == "unchanged"


# 13b -- N1 AT THE CALL SITE: row 13 walks the helper in isolation, so a call site
# reverted to the naive identity order stayed GREEN.
def test_the_anonymized_live_render_substitutes_through_the_longest_first_helper(monkeypatch):
    seen, real = [], _substitute_longest_first
    monkeypatch.setitem(globals(), "_substitute_longest_first",
                        lambda text, mapping: (seen.append(dict(mapping)),
                                               real(text, mapping))[1])
    piece = BY_NAME["user-slice-guard"]
    got = _anonymized_live_render(piece, R.host_tokens(CFG))
    assert seen, ("the call site substituted the identity tokens itself; the naive "
                  "identity order corrupts an overlapping token (row 13)")
    fix = (FIXTURES / (piece["name"] + ".fixture")).read_text(encoding="utf-8")
    _assert_piece_matches_fixture(piece, got, fix, _vs())


# 14 -- THE ENGINE'S OWN PHYSICAL-TOKEN GUARD over the kit's bytes. Row 4 checks a
# BESPOKE denylist because anonymize.py's classes (hostname/ip/mac/board/secret) cannot
# express "the checkout root" or "the cgroup uid": the two denylists are DISJOINT, so a
# template naming this box's hostname, a NIC address, a board serial or a key id passes
# row 4 CLEAN. This row runs anonymize.scan -- the guard's own function, MIN_TOKEN and
# CLASSES -- against a FAKE box denylist reached through anonymize's own
# AGI_ANONYMIZE_FIXTURE seam, so it reads no physical value of this box and prints none.
# The fake denylist is DERIVED from anonymize.CLASSES -- one obviously synthetic value
# per class, never a typed class list -- so a class added to the guard needs no edit here
# (email arrived after the hand list and reddened row 14). No value is a real host,
# address, email, key or path, and none is an email shape, so a planted one is named
# by its own class alone.
def _fake_value(cls):
    # hardware matches by FRAGMENT (>= 2 words around a >= 3-digit core), so its fake is word-shaped
    return "Boxkit Fake Part 9990" if cls == "hardware" else "boxkit-fake-%s-token" % cls


def _fake_box(classes):
    return {c: [_fake_value(c)] for c in classes}


@pytest.fixture
def anonymize():
    """bin/anonymize.py, loaded INSIDE a fixture, not at import: _load_bin inserts bin/
    on sys.path and binds sys.modules["anonymize"], and at import time that leaked into
    every later test of the session. Both are restored on teardown."""
    saved_path, had = list(sys.path), "anonymize" in sys.modules
    saved_mod = sys.modules.get("anonymize")
    try:
        yield _load_bin("anonymize")
    finally:
        sys.path[:] = saved_path
        if had:
            sys.modules["anonymize"] = saved_mod
        else:
            sys.modules.pop("anonymize", None)


@pytest.fixture
def fake_box(tmp_path, monkeypatch, anonymize):
    p = tmp_path / "boxkit-fake-box.json"
    p.write_text(json.dumps(_fake_box(anonymize.CLASSES)), encoding="utf-8")
    monkeypatch.setenv("AGI_ANONYMIZE_FIXTURE", str(p))
    return p


def _kit_bytes():
    """Every byte the kit ships: the templates, the manifest, and the committed
    fixtures -- the surfaces a box's identity could ride into another box."""
    out = [(TEMPLATES / p.name, (TEMPLATES / p.name).read_text(encoding="utf-8"))
           for p in sorted(TEMPLATES.iterdir()) if p.is_file()]
    out += [(f, f.read_text(encoding="utf-8"))
            for f in sorted(FIXTURES.rglob("*")) if f.is_file()]
    return out


def test_one_planted_kit_copy_goes_red_and_the_kits_own_bytes_stay_clean(
        fake_box, anonymize, tmp_path):
    """Both directions in ONE row. The kit's OWN bytes can only go red on a real box's
    denylist, unreadable here, so ability-to-go-red is shown on a PLANTED COPY of one
    template (one _fake_value, one class) and the clean half on the kit's own bytes."""
    toks = anonymize.box_tokens(PROJECT)
    assert sorted({c for c, _ in toks}) == sorted(anonymize.CLASSES), \
        "the fake denylist did not reach every class; the row would be vacuous"
    cls, value = "ip", _fake_value("ip")
    src = TEMPLATES / BY_NAME["oomd-guard"]["template"]
    clean = src.read_text(encoding="utf-8")
    planted = tmp_path / "planted" / src.name
    planted.parent.mkdir(parents=True)
    planted.write_text(clean + "\n# a planted %s token: %s\n" % (cls, value),
                       encoding="utf-8")
    assert anonymize.scan(planted.read_text(encoding="utf-8"), toks) == [cls], cls
    # the kit's own bytes carry systemd-unit address shapes (user@UID.service):
    # the cell's `anonymize.email_allow` is the ONLY thing that can cover them,
    # so the row reads the CELL and adds NO pattern of its own (dh347 item 4).
    # The landed cell covers them (measured at fc2cc2c6a8), so EVERY template
    # must scan clean: an email-only hit is a red, never a skip (g1.41 PASS B4).
    allow = anonymize._email_allow(PROJECT)
    for path, text in _kit_bytes():   # the kit's OWN bytes, incl. the clean src
        assert anonymize.scan(text, toks, allow) == [], path.name


# 14b -- THE DISJOINTNESS itself, BOTH directions, EVERY class. Direction 1 is per class.
# Direction 2 is NOT: the value must be one the KIT denylist can see and NOT a member of
# LEAK_ROOTS -- naming a leak root made the kit half a TAUTOLOGY (roots are in _leaks by
# construction, so no state could make it false, DH.615 item 1). KIT_TOKEN is DRAWN from
# KIT_TOKENS -- the kit rule's own token source, which _leaks consults independently
# of LEAK_ROOTS -- so the assert is falsifiable and the candidate cannot be a second
# copy of a literal the rule no longer denies (DH.634 item 4). Never a FAKE_BOX value
# either: a planted FAKE_BOX value is invisible to every kit rule by definition, so
# `assert _leaks(planted) == []` could never go red (DH.591 item 1). The kit SEES the
# token; the engine's denylist does NOT. RED when THIS candidate is added to
# anonymize.box_tokens: `scan` then names a class here. NOT the kit's LEAK_ROOTS --
# that mutation cannot fire, because the candidate is drawn precisely from outside
# LEAK_ROOTS (DH.653 item 1; the earlier text named a mutation that was unfalsifiable).
def _kit_token():
    """Row 14b's candidate, resolved at CALL time and REFUSING BY NAME. It was a
    module-level next(): a bare StopIteration AT IMPORT is a COLLECTION error and no
    row in this file runs (measured blast radius: all 198, DH.653 items 3 and 6)."""
    cands = [t for t in KIT_TOKENS if t and t not in LEAK_ROOTS]
    assert cands, ("no kit denylist token outside LEAK_ROOTS: every member of "
                   "KIT_TOKENS %r is a leak root, so row 14b has no falsifiable "
                   "candidate" % ([t for t in KIT_TOKENS if t],))
    return cands[0]

@pytest.mark.parametrize("cls", ["hostname", "ip", "mac", "board", "secret"])
def test_the_kit_denylist_and_the_engine_denylist_are_disjoint_in_both_directions(
        cls, fake_box, anonymize):
    toks = anonymize.box_tokens(PROJECT)
    value, kit = _fake_value(cls), _kit_token()
    clean = (TEMPLATES / BY_NAME["oomd-guard"]["template"]).read_text(encoding="utf-8")
    planted = clean + "\n# a planted %s token: %s\n" % (cls, value)
    assert anonymize.scan(planted, toks) == [cls], cls
    assert kit not in LEAK_ROOTS, "tautology: _leaks carries every leak root by rule"
    assert any(t is kit for t in KIT_TOKENS), \
        "candidate is not a member of the kit denylist's own token source"
    assert _leaks("cd %s\n" % kit), "row 4 does not see its own denylist token"
    assert anonymize.scan("cd %s\n" % kit, toks) == [], "the guard now sees a kit token"


# 15 -- THE INVENTORY IS CHECKED, NOT CLAIMED ABSENT: the header said "no list of row
# names exists" and WAS one (DH.653 item 5). This row is the wide grep -- it sees every
# `row N` mention, so a row added without its entry is RED rather than stale.
def test_the_row_inventory_here_lists_every_row_the_file_names():
    text = Path(__file__).read_text(encoding="utf-8")
    listed = {int(m) for m in re.findall(r"^(\d+)[.:] ", text, re.M)}
    # the DECLARED row comments count as uses too (DH.653 item 1): a row declared only
    # as a bare `# N --` comment, named nowhere in prose, was invisible here and green.
    used = ({int(m) for m in re.findall(r"[Rr]ow (\d+)", text)}
            | {int(m) for m in re.findall(r"^# (\d+)\s", text, re.M)})
    missing = sorted(used - listed)
    assert not missing, ("row(s) %s are named in this file but absent from the docstring "
                         "inventory: add the entry, do not delete the reference" % missing)
    assert listed, "the inventory parse found nothing -- the rule above is now vacuous"
    # the HEADER's own "Rows A-B" is a third copy, and neither regex above reads it:
    # a fully consistent EXTRA row (declared comment + docstring entry) left this
    # row green under a header still saying 15. The declared last number is compared
    # with the highest row the file actually names, so the header cannot go stale.
    declared = re.search(r"^Rows (\d+)-(\d+)", text, re.M)
    assert declared, "the docstring no longer declares a `Rows A-B` header range"
    first, last = int(declared.group(1)), int(declared.group(2))
    highest = max(listed | used)
    assert last == highest, (
        "the header declares rows %d-%d but the highest row this file names is %d: "
        "move the header, do not leave a second copy" % (first, last, highest))


# 14c -- dg355 items 1-3, superseding dg352 item 3's version. (1) it PINS its own
# email_allow, so the owed RFC 2606 pattern in the cell cannot flip its precondition;
# (2) the address is BUILT AT RUNTIME FROM PARTS; (3) it drives the loop ITSELF and
# COUNTS the templates reached, because the old row's `pytest.raises` could not tell
# an early `pytest.skip` (reported `skipped`, not failed) from a real abort.
PINNED_EMAIL_ALLOW = [re.compile(r"[\w.-]+@\d+\.service")]
def test_a_later_non_email_hit_fails_while_an_earlier_email_only_hit_exists(
        fake_box, anonymize, tmp_path, monkeypatch):
    clean = (TEMPLATES / BY_NAME["oomd-guard"]["template"]).read_text(encoding="utf-8")
    addr = "@".join(("ops", ".".join(("fixture", "invalid"))))   # built, never a literal
    email_text = clean + "\n# ops contact: " + addr + "\n"
    monkeypatch.setattr(anonymize, "_email_allow", lambda root=None: PINNED_EMAIL_ALLOW)
    monkeypatch.setattr(sys.modules[__name__], "_kit_bytes", lambda: [
        (Path("early-kit-template"), email_text),
        (Path("late-kit-template"), clean + "\n# %s\n" % _fake_value("ip"))],
        raising=False)
    toks = anonymize.box_tokens(PROJECT)
    assert anonymize.scan(email_text, toks, PINNED_EMAIL_ALLOW) == ["email"], "not email-ONLY; vacuous"
    scanned, emailed, failed = [], [], []
    for path, text in _kit_bytes():
        hits = anonymize.scan(text, toks, PINNED_EMAIL_ALLOW)
        scanned.append(path.name)
        if hits == ["email"]:
            emailed.append(path.name)
            continue      # dg355 item 3 MUTATION POINT: `break` here -> the row FAILS
        failed.append((path.name, hits))
    assert scanned == ["early-kit-template", "late-kit-template"], \
        "the loop never reached every template; it scanned: %s" % (scanned,)
    assert emailed == ["early-kit-template"], emailed
    assert failed == [("late-kit-template", ["ip"])], failed


def _tree_lines(ev, kind="tree"):
    return [[b[1] for b in ev.boxes if b[0][4] == "agi-" + to and b[1].startswith("[memguard-%s]" % kind)] for to in _vs()["MEMGUARD_ALERT_TO"].split()]


def _youngs(rows, age_s, pids=None):
    """Start every process of the unit `age_s` seconds before the fake clock's first reading (10000 s)."""
    hz = os.sysconf("SC_CLK_TCK"); out = dict(rows)
    for p, r in rows.items():
        if r[2] == _post_cg() and (pids is None or p in pids): out[p] = r[:4] + (int((10_000 - age_s) * hz),) + r[5:]
    return out


def test_memguard_asks_systemd_for_one_unit_baseline_per_tick(tmp_path):
    rows = _two_units(); spawn = {1: [(19, 20, "bash", "/bin/bash -c a"), (119, 120, "bash", "/bin/bash -c b")]}
    adj, stops, runs, ev = _guard_pass(tmp_path / "one", rows, passes=2, spawn=spawn)
    assert len(ev.sysd) == 1, ev.sysd                                       # two units owe a read, one tick: ONE systemctl (a hung one costs one timeout, not one per unit)
    adj, stops, runs, ev = _guard_pass(tmp_path / "two", _two_units(), passes=3, spawn=spawn)
    assert len(ev.sysd) == 2 and {a[2] for a in ev.sysd} == {_unit(), _unit_b()}, ev.sysd         # the other unit's turn is the next tick
    assert _child(tmp_path / "two", 19) == 0 and _child(tmp_path / "two", 119) == 0                # and both children are reset in the end


def test_memguard_does_not_judge_a_unit_younger_than_two_ticks_plus_a_second(tmp_path):
    iv = int(_vs()["INTERVAL_S"])
    rows = _post_unit(); rows[20] = rows[20][:1] + ("zzz-new --title-rewritten",) + rows[20][2:]               # no harness found
    fresh = _youngs(rows, iv + 0.5)                                                                             # pass 1 sees 2 ticks + 0.5 s (inside 2 ticks + 1), pass 2 sees 3 ticks + 0.5
    adj, kills, runs, ev = _guard_pass(tmp_path / "young", fresh, passes=2)
    assert not any("no harness found" in a[0][-1] for a in runs) and _tree_lines(ev) == [[]] * len(_tree_lines(ev)), [a[0][-1] for a in runs]
    prot = int(_vs()["PROTECT_OOM_ADJ"])
    assert [adj[p] for p in (10, 11, 12)] == [prot] * 3, adj                                                    # the spine is protected all the same
    adj, kills, runs, ev = _guard_pass(tmp_path / "grown", fresh, passes=4)                        # the window passes: the next tick asks again and says it ONCE
    assert sum("no harness found" in a[0][-1] for a in runs) == 1 and all(len(t) == 1 for t in _tree_lines(ev)), ([a[0][-1] for a in runs], _tree_lines(ev))
    adj, kills, runs, ev = _guard_pass(tmp_path / "old", rows, passes=2)
    assert sum("no harness found" in a[0][-1] for a in runs) == 1                                                # an old unit is judged at once (its 2nd tick)
    one_old = _youngs(rows, 3, pids={20})                                                                       # a young harness under an OLD tracer: the unit's oldest process decides
    adj, kills, runs, ev = _guard_pass(tmp_path / "mixed", one_old, passes=2)
    assert sum("no harness found" in a[0][-1] for a in runs) == 1


def test_memguard_does_not_judge_a_young_unit_whose_tree_cannot_be_read(tmp_path):
    rows = _post_unit(); rows[10] = rows[10][:3] + (11,) + rows[10][4:]; rows[30] = rows[30][:3] + (21,) + rows[30][4:]
    adj, stops, runs, ev = _guard_pass(tmp_path / "young", _youngs(rows, 3), passes=2)
    assert not any("could not be read" in a[0][-1] for a in runs), [a[0][-1] for a in runs]
    adj, stops, runs, ev = _guard_pass(tmp_path / "old", rows, passes=2)
    assert sum("could not be read" in a[0][-1] for a in runs) == 1


def test_memguard_a_unit_that_is_found_again_gets_a_fresh_line_for_a_later_miss(tmp_path):
    tick = int(_vs()["ALERT_COOLDOWN_S"]) + 1
    good = _post_unit()[20][1]
    hide = (20, "cmd", "zzz-new --title-rewritten"); show = (20, "cmd", good)
    adj, kills, runs, ev = _guard_pass(tmp_path / "noh", _post_unit(), passes=5, tick=tick, rewrite={0: [hide], 2: [show], 3: [hide]})
    assert sum("no harness found" in a[0][-1] for a in runs) == 2 and all(len(t) == 2 for t in _tree_lines(ev)), ([a[0][-1] for a in runs], _tree_lines(ev))      # race, found, later miss: two lines; a miss that goes on is still ONE
    adj, kills, runs, ev = _guard_pass(tmp_path / "noh-steady", _post_unit(), passes=4, tick=tick, rewrite={0: [hide], 1: [hide], 2: [hide], 3: [hide]})
    assert sum("no harness found" in a[0][-1] for a in runs) == 1
    cut = [(10, "ppid", 11), (30, "ppid", 21)]; mend = [(10, "ppid", 1), (30, "ppid", 1)]
    adj, kills, runs, ev = _guard_pass(tmp_path / "unread", _post_unit(), passes=4, tick=tick, rewrite={0: cut, 1: mend, 2: cut, 3: cut})
    assert sum("could not be read" in a[0][-1] for a in runs) == 2 and all(len(t) == 2 for t in _tree_lines(ev)), ([a[0][-1] for a in runs], _tree_lines(ev))
    adj, kills, runs, ev = _guard_pass(tmp_path / "unread-steady", _post_unit(), passes=4, tick=tick, rewrite={0: cut, 1: cut, 2: cut, 3: cut})
    assert sum("could not be read" in a[0][-1] for a in runs) == 1


def test_memguard_a_young_unit_is_judged_when_the_age_cannot_be_read(tmp_path):
    rows = _post_unit(); rows[20] = rows[20][:1] + ("zzz-new --title-rewritten",) + rows[20][2:]               # no harness found, in a unit that is young
    fresh = _youngs(rows, 3)
    adj, kills, runs, ev = _guard_pass(tmp_path / "age", fresh, passes=1)
    assert not any("no harness found" in a[0][-1] for a in runs)                                                # the age reads: skipped
    adj, kills, runs, ev = _guard_pass(tmp_path / "noage", fresh, passes=2, no_uptime=True)
    assert sum("no harness found" in a[0][-1] for a in runs) == 1 and all(len(t) == 1 for t in _tree_lines(ev)), [a[0][-1] for a in runs]   # no /proc/uptime: judged, the line fires
    cut = _post_unit(); cut[10] = cut[10][:3] + (11,) + cut[10][4:]; cut[30] = cut[30][:3] + (21,) + cut[30][4:]
    adj, stops, runs, ev = _guard_pass(tmp_path / "noage-unread", _youngs(cut, 3), passes=1, no_uptime=True)
    assert sum("could not be read" in a[0][-1] for a in runs) == 1


def test_memguard_the_two_tree_alerts_of_one_unit_do_not_share_a_cooldown_key(tmp_path):
    hide = (20, "cmd", "zzz-new --title-rewritten"); cut = [(10, "ppid", 11), (30, "ppid", 21)]
    adj, kills, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=3, rewrite={0: [hide], 2: cut})         # pass 0: pending; pass 1: no harness (the 2nd tick); pass 2: the tree unreadable, 5 s later
    assert sum("no harness found" in a[0][-1] for a in runs) == 1 and sum("could not be read" in a[0][-1] for a in runs) == 1, [a[0][-1] for a in runs]
    assert all(len(t) == 2 for t in _tree_lines(ev)), _tree_lines(ev)                                         # both reach the ~/.notice: one cooldown key per fault, not one per unit


_STUB_UNIT_CTL = """#!/bin/sh
echo "$*" >> "$CALLS"
case "$*" in
  "is-active "*) [ -e "$STATE" ]; exit $?;;
  "stop "*) if [ -n "$BREAK_LOG" ]; then rm -f "$LOG"; mkdir "$LOG"; fi; if [ -n "$RACE_PID" ]; then kill -STOP "$RACE_PID"; echo "2026-10-11T09:00:00Z SUSPENDED pid $RACE_PID (sleep): in the window" >> "$LOG"; fi; rm -f "$STATE";;
  "enable --now "*) : > "$STATE";;
  "disable"*) rm -f "$STATE";;
esac
exit 0
"""


def test_memguard_a1_undo_disables_and_removes_the_wants_link_a_hand_stop_leaves_behind(tmp_path):
    sb, ud = tmp_path / "sbin", tmp_path / "units"; (ud / "multi-user.target.wants").mkdir(parents=True); sb.mkdir()
    (sb / "agi-memguard.py").write_text("x"); (ud / "agi-memguard.service").write_text("x")
    (ud / "multi-user.target.wants" / "agi-memguard.service").symlink_to(ud / "agi-memguard.service")       # stopped by hand: still ENABLED
    ctl = tmp_path / "ctl"; ctl.write_text(_STUB_UNIT_CTL); ctl.chmod(0o755)
    env = dict(SUDO="env", SBIN=sb, UNITDIR=ud, SYSTEMCTL=ctl, CALLS=tmp_path / "calls.log", STATE=tmp_path / "active")
    r = _sh("memguard-a1.undo.sh", tmp_path, **env)
    calls = (tmp_path / "calls.log").read_text().splitlines()
    assert r.returncode == 0 and "UNDO A1 ok" in r.stdout, r.stdout + r.stderr
    assert not (sb / "agi-memguard.py").exists() and not (ud / "agi-memguard.service").exists() and not (ud / "multi-user.target.wants" / "agi-memguard.service").is_symlink(), r.stdout
    assert "disable agi-memguard.service" in calls and calls.index("disable agi-memguard.service") < calls.index("daemon-reload"), calls     # systemd is asked to drop its own link too
    (sb / "agi-memguard.py").write_text("x"); (tmp_path / "active").write_text("")                          # an ACTIVE unit: refused by name, nothing removed
    r = _sh("memguard-a1.undo.sh", tmp_path, **env)
    assert r.returncode == 1 and "UNDO A1 REFUSED: the unit is active" in r.stdout and (sb / "agi-memguard.py").exists()


_OLD_GUARD = "old guard\n    for to in 'master belam'.split():\n        x = 'HOME=/stores/' + to\n"                       # the recipients and the stores the real guard source carries
_STUB_NOTICE = "#!/bin/sh\necho \"$1 $2\" >> \"$NOTICES\"\n"


def _restage_world(tmp_path):
    """A MAIN with the real boxkit, a box that already runs an OLDER guard (installed, enabled, active, a2.since = ORIG), and the stub systemctl."""
    repo, g = _mini_repo(tmp_path); sha = g("rev-parse", "HEAD")
    sb, ud = tmp_path / "sbin", tmp_path / "units"; (ud / "multi-user.target.wants").mkdir(parents=True); sb.mkdir()
    (sb / "agi-memguard.py").write_text(_OLD_GUARD); (ud / "agi-memguard.service").write_text("old unit")
    (ud / "multi-user.target.wants" / "agi-memguard.service").symlink_to(ud / "agi-memguard.service")
    stage = tmp_path / "memguard-A0"; stage.mkdir(); (stage / "a2.since").write_text("2026-10-11T08:30:00Z\n")
    ctl = tmp_path / "ctl"; ctl.write_text(_STUB_UNIT_CTL); ctl.chmod(0o755); (tmp_path / "active").write_text("")
    nb = tmp_path / "notice-bin"; nb.write_text(_STUB_NOTICE); nb.chmod(0o755)
    env = dict(SUDO="env", OWN="", LOG=tmp_path / "guard.log", SBIN=sb, UNITDIR=ud, SYSTEMCTL=ctl, CALLS=tmp_path / "calls.log", STATE=tmp_path / "active", STAGE=stage, MAIN=repo,
               NOTICE_BIN=nb, NOTICES=tmp_path / "notices.log", RACE_PID="")
    return repo, g, sha, stage, sb, ud, env


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_memguard_restage_moves_a_running_guard_to_the_new_sha_and_keeps_the_undo_scope(tmp_path):
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path)
    r = _sh("memguard-restage.sh", tmp_path, SHA=sha, **env)
    calls = (tmp_path / "calls.log").read_text().splitlines()
    assert r.returncode == 0 and "RESTAGE OK" in r.stdout, r.stdout + r.stderr
    assert (stage / "a2.since").read_text().strip() == "2026-10-11T08:30:00Z", (stage / "a2.since").read_text()     # the ORIGINAL scope, not the re-stage's stamp
    assert (sb / "agi-memguard.py").read_text() != _OLD_GUARD and (stage / "SHA").read_text().strip() == sha        # the new bytes are in
    assert not (ud / "multi-user.target.wants" / "agi-memguard.service").is_symlink()                                 # a1.undo took the stale wants link
    order = [calls.index(c) for c in ("stop agi-memguard.service", "disable agi-memguard.service", "enable --now agi-memguard.service")]
    assert order == sorted(order) and (tmp_path / "active").exists(), calls                                        # stopped first, running again at the end
    assert "memguard-a1.proof.sh" in r.stdout and "memguard-a2.proof.sh" in r.stdout                               # the proofs are named, not run


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_memguard_restage_refuses_without_a_landed_sha_and_touches_nothing_when_a0_refuses(tmp_path):
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path)
    for bogus in (None, "main", "Z" * 40, "0" * 40):
        r = _sh("memguard-restage.sh", tmp_path, **env, **({"SHA": bogus} if bogus else {}))
        assert r.returncode == 1 and "RESTAGE REFUSED" in r.stdout, (bogus, r.stdout + r.stderr)
    assert not (tmp_path / "calls.log").exists() and (stage / "a2.since").read_text().strip() == "2026-10-11T08:30:00Z" and (tmp_path / "active").exists()
    t = repo / "extensions/agi/boxkit/templates/memguard-script.tmpl"; t.write_text(t.read_text().replace("stays stopped", "stays STOPPED", 1))
    g("commit", "-qam", "tamper"); bad = g("rev-parse", "HEAD")
    r = _sh("memguard-restage.sh", tmp_path, SHA=bad, **env)                                                       # A0's C1 refuses AFTER its rm -rf of the stage
    assert r.returncode == 1 and "RESTAGE STOPPED at A0" in r.stdout and "the guard was not touched" in r.stdout, r.stdout + r.stderr
    assert not (tmp_path / "calls.log").exists() and (tmp_path / "active").exists(), "the guard was never stopped"
    assert (stage / "a2.since").read_text().strip() == "2026-10-11T08:30:00Z"                                      # and the scope A0 wiped is back
    assert (sb / "agi-memguard.py").read_text() == _OLD_GUARD


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_memguard_restage_says_the_guard_is_stopped_when_a_step_fails_after_the_stop(tmp_path):
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path)
    sb.chmod(0o555)                                                                                                 # a1.undo cannot remove the old guard: a failure AFTER the stop
    try:
        r = _sh("memguard-restage.sh", tmp_path, SHA=sha, **env)
    finally: sb.chmod(0o755)
    assert r.returncode == 1 and "RESTAGE FAILED at a1.undo: THE GUARD IS STOPPED" in r.stdout, r.stdout + r.stderr
    assert "stop agi-memguard.service" in (tmp_path / "calls.log").read_text().splitlines() and not (tmp_path / "active").exists()
    assert (stage / "a2.since").read_text().strip() == "2026-10-11T08:30:00Z"


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_memguard_restage_refuses_while_the_guard_holds_stopped_pids_and_touches_nothing(tmp_path):
    import signal, time
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path)
    mine, older, running = (subprocess.Popen(["sleep", "30"]) for _ in range(3))
    try:
        for q in (mine, older): os.kill(q.pid, signal.SIGSTOP)
        time.sleep(0.3)
        log = Path(env["LOG"])                                                         # a2.since is 08:30:00Z
        log.write_text("2026-10-11T08:00:00Z SUSPENDED pid %d (sleep): an EARLIER A2\n2026-10-11T08:41:00Z SUSPENDED pid %d (sleep): this A2, still stopped\n"
                       "2026-10-11T08:42:00Z SUSPENDED pid %d (sleep): this A2, resumed since\n" % (older.pid, mine.pid, running.pid))
        r = _sh("memguard-restage.sh", tmp_path, SHA=sha, **env)
        assert r.returncode == 1 and "RESTAGE REFUSED: the guard holds stopped pids: %d " % mine.pid in r.stdout + " " and str(older.pid) not in r.stdout.split("holds stopped pids:")[1] and str(running.pid) not in r.stdout.split("holds stopped pids:")[1], r.stdout + r.stderr
        assert not (tmp_path / "calls.log").exists() and (tmp_path / "active").exists() and (sb / "agi-memguard.py").read_text() == _OLD_GUARD, "nothing touched"
        said = (tmp_path / "notices.log").read_text().splitlines()
        assert [l.split(" ")[0] for l in said] == ["master", "belam"] and all("[memguard-restage] RESTAGE REFUSED: the guard holds stopped pids:" in l for l in said), said      # a refusal reaches both recipients
        assert (stage / "a2.since").read_text().strip() == "2026-10-11T08:30:00Z" and not (stage / "SHA").exists(), "not even A0 ran"
        os.kill(mine.pid, signal.SIGCONT); time.sleep(0.3)                             # resumed: only an EARLIER A2's stopped pid is left, which is not this A2's to continue
        r = _sh("memguard-restage.sh", tmp_path, SHA=sha, **env)
        assert r.returncode == 0 and "RESTAGE OK" in r.stdout, r.stdout + r.stderr
    finally:
        for q in (mine, older, running): q.kill(); q.wait()
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path / "w2")             # a log that exists and cannot be read is not an empty one
    (tmp_path / "w2" / "guard.log").mkdir()
    r = _sh("memguard-restage.sh", tmp_path / "w2", SHA=sha, **env)
    assert r.returncode == 1 and "cannot be read" in r.stdout and not (tmp_path / "w2" / "calls.log").exists(), r.stdout + r.stderr
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path / "w3")             # a regular file whose read FAILS (awk exits non-zero) is not an empty one either
    (tmp_path / "w3" / "guard.log").write_text("2026-10-11T08:41:00Z SUSPENDED pid 1 (x)\n")
    fb = tmp_path / "w3" / "fakebin"; fb.mkdir(); (fb / "awk").write_text("#!/bin/sh\nexit 2\n"); (fb / "awk").chmod(0o755)
    r = _sh("memguard-restage.sh", tmp_path / "w3", SHA=sha, **env)
    assert r.returncode == 1 and "cannot be read" in r.stdout and not (tmp_path / "w3" / "calls.log").exists(), r.stdout + r.stderr


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_memguard_restage_resumes_a_pid_the_old_guard_stops_in_the_window_before_its_stop_and_says_so(tmp_path):
    import signal, time
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path)
    racer = subprocess.Popen(["sleep", "30"])
    state = lambda p: Path("/proc/%d/stat" % p).read_text().rsplit(")", 1)[1].split()[0]
    try:
        r = _sh("memguard-restage.sh", tmp_path, SHA=sha, **{**env, "RACE_PID": racer.pid})          # the stub `systemctl stop` SIGSTOPs the pid and logs it: the first check saw nothing
        time.sleep(0.3)
        assert r.returncode == 0 and "RESTAGE OK" in r.stdout and "RESTAGE RESUMED pid %d" % racer.pid in r.stdout, r.stdout + r.stderr
        assert state(racer.pid) == "S", state(racer.pid)                                          # THE FALSIFIER: after the script returns, no pid the old guard stopped is still T/t
        said = (tmp_path / "notices.log").read_text().splitlines()
        assert [l.split(" ")[0] for l in said] == ["sanctuary-master", "belam"] and all("RESUMED pid %d" % racer.pid in l and "kill -CONT %d" % racer.pid in l for l in said), said
        assert (stage / "a2.since").read_text().strip() == "2026-10-11T08:30:00Z"
    finally:
        racer.kill(); racer.wait()
    # a pid that CANNOT be resumed is named WITH its resume command (the falsifier's other arm), and the restage goes on
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path / "w2")
    fb = tmp_path / "w2" / "fakebin"; fb.mkdir(parents=True); (fb / "kill").write_text("#!/bin/sh\nexit 1\n"); (fb / "kill").chmod(0o755)        # `env kill -CONT` finds this one first
    racer = subprocess.Popen(["sleep", "30"])
    try:
        r = _sh("memguard-restage.sh", tmp_path / "w2", SHA=sha, **{**env, "RACE_PID": racer.pid})
        time.sleep(0.3)
        assert r.returncode == 0 and "RESTAGE COULD NOT RESUME pid %d" % racer.pid in r.stdout and "RESTAGE OK" in r.stdout, r.stdout + r.stderr
        assert state(racer.pid) == "T"                                                                # still stopped: so the line must carry the command
        said = (tmp_path / "w2" / "notices.log").read_text().splitlines()
        assert len(said) == 2 and all("STILL STOPPED" in l and "resume it by hand: kill -CONT %d" % racer.pid in l for l in said), said
    finally:
        os.kill(racer.pid, signal.SIGCONT); racer.kill(); racer.wait()
    # a failure AFTER the stop reaches the recipients too
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path / "w3"); (tmp_path / "w3" / "sbin").chmod(0o555)
    try:
        r = _sh("memguard-restage.sh", tmp_path / "w3", SHA=sha, **env)
    finally: (tmp_path / "w3" / "sbin").chmod(0o755)
    said = (tmp_path / "w3" / "notices.log").read_text().splitlines()
    assert r.returncode == 1 and len(said) == 2 and all("THE GUARD IS STOPPED" in l for l in said), (r.stdout, said)
    # the log readable at the first check and NOT after the stop: the stopped pids are unknown, THE GUARD IS STOPPED is said to the recipients, nothing is guessed
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path / "w4"); Path(env["LOG"]).write_text("")
    r = _sh("memguard-restage.sh", tmp_path / "w4", SHA=sha, **{**env, "BREAK_LOG": "1"})
    said = (tmp_path / "w4" / "notices.log").read_text().splitlines()
    assert r.returncode == 1 and "RESTAGE FAILED after the stop: THE GUARD IS STOPPED and" in r.stdout and len(said) == 2 and "memguard-a2.undo.sh" in said[0], (r.stdout, said)


def _kill_at(ev, pid):
    ks = [i for i, e in enumerate(ev.seq) if e[0] == "kill" and e[1] == pid and e[2] == int(__import__("signal").SIGSTOP)]
    assert len(ks) == 1, (pid, ev.seq)
    return ks[0]


def test_memguard_writes_the_suspended_line_before_the_sigstop_and_forks_nothing_before_it(tmp_path):
    rows = _post_unit()
    for name, kw, want in (("size", dict(avails=[3 * GIB] * 2, grow={1: [(30, 7_000_000)]}), 30), ("low", dict(avails=[GIB // 2]), None)):
        adj, stops, runs, ev = _guard_pass(tmp_path / name, rows, passes=2 if name == "size" else 1, **kw)
        pid = want or stops[0]; assert stops == [pid], stops
        k = _kill_at(ev, pid); text = ev.seq[k][3]
        assert "SUSPENDED pid %d " % pid in text and "start %s" % rows[pid][4] in text, text                       # the line is in the FILE when the SIGSTOP goes out, with the pid's start time
        assert not any(e[0] in ("log", "popen", "run") for e in ev.seq[:k]), ev.seq[:k]                                  # and nothing was forked before it: no logger, no notice (the stop never waits on a spawn)
        after = ev.seq[k + 1:]
        assert any(e[0] == "log" and "SUSPENDED pid %d " % pid in e[1] for e in after) and any(e[0] == "popen" and "SUSPENDED pid %d " % pid in e[1] for e in after), after      # the journal line and the notices follow


def test_memguard_a_sigstop_that_fails_leaves_the_line_in_the_file_and_no_stopped_pid_and_says_so(tmp_path):
    tos = _vs()["MEMGUARD_ALERT_TO"].split()
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=3, avails=[3 * GIB] * 3, grow={1: [(30, 7_000_000)]}, kill_raises={30})
    said = [a[0][-1] for a in runs]; filed = (tmp_path / "guard.log").read_text().splitlines()
    assert sum("SUSPENDED pid 30 " in l for l in filed) == sum("the SIGSTOP failed" in m for m in said) >= 1, (filed, said)     # every attempt: the line in the file, the failure in the journal
    assert not any("SUSPENDED pid 30 " in m for m in said), said                                                      # no journal line claims a stop that did not happen
    assert 30 not in ev.stopped and stops == [], (ev.stopped, stops)                                                  # no pid is tracked as stopped
    assert not any("no longer tracked as stopped" in m for m in said), said                                           # and the next tick has nothing to prune
    for to in tos:
        kinds = [b[1].split(" ")[0] for b in ev.boxes if b[0][4] == "agi-" + to]
        assert kinds.count("[memguard-susp-30]") == 0 and kinds.count("[memguard-stopfail-30]") == 1, (to, kinds)       # the master reads the failure, not a false SUSPENDED


def _start_of(pid): return Path("/proc/%d/stat" % pid).read_text().rsplit(")", 1)[1].split()[19]


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_memguard_restage_and_a2_undo_never_continue_a_reused_pid(tmp_path):
    import signal, time
    repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path)
    mine, reused = (subprocess.Popen(["sleep", "30"]) for _ in range(2))
    state = lambda p: Path("/proc/%d/stat" % p).read_text().rsplit(")", 1)[1].split()[0]
    try:
        for q in (mine, reused): os.kill(q.pid, signal.SIGSTOP)
        time.sleep(0.3)
        log = Path(env["LOG"])
        log.write_text("2026-10-11T08:41:00Z SUSPENDED pid %d (sleep, unit x, start 1): the guard stopped ANOTHER process under this pid, long ago\n" % reused.pid)
        r = _sh("memguard-restage.sh", tmp_path, SHA=sha, **env)                                      # the pid is stopped now, but it is not the process the guard stopped
        assert r.returncode == 0 and "RESTAGE OK" in r.stdout and state(reused.pid) == "T", r.stdout + r.stderr          # not held: restage goes on and does not touch it
        repo, g, sha, stage, sb, ud, env = _restage_world(tmp_path / "w2")
        Path(env["LOG"]).write_text("2026-10-11T08:41:00Z SUSPENDED pid %d (sleep, unit x, start %s): this one\n" % (mine.pid, _start_of(mine.pid)))
        r = _sh("memguard-restage.sh", tmp_path / "w2", SHA=sha, **env)
        assert r.returncode == 1 and "holds stopped pids: %d " % mine.pid in r.stdout + " ", r.stdout + r.stderr         # the matching start time: held, refused
        stg = tmp_path / "undo"; stg.mkdir(); (stg / "a2.since").write_text("2026-10-11T08:30:00Z\n")
        ulog = tmp_path / "undo.log"
        ulog.write_text("2026-10-11T08:40:00Z SUSPENDED pid %d (sleep, unit x, start %s): ours\n2026-10-11T08:41:00Z SUSPENDED pid %d (sleep, unit x, start 1): another process then\n" % (mine.pid, _start_of(mine.pid), reused.pid))
        r = _sh("memguard-a2.undo.sh", tmp_path / "undo", STAGE=stg, LOG=ulog, **_stubs(tmp_path / "undo", since="Sun 2026-10-11 09:00:00 UTC"))
        time.sleep(0.3)
        assert "resuming pid %d" % mine.pid in r.stdout and "NOT resuming pid %d" % reused.pid in r.stdout and "a reused pid" in r.stdout, r.stdout + r.stderr
        assert state(mine.pid) == "S" and state(reused.pid) == "T", (state(mine.pid), state(reused.pid))
    finally:
        for q in (mine, reused): q.kill(); q.wait()


def test_memguard_stops_the_runaway_anyway_when_the_log_append_raises_and_says_it_could_not_log_it(tmp_path):
    tos = _vs()["MEMGUARD_ALERT_TO"].split()
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=2, avails=[3 * GIB] * 2, grow={1: [(30, 7_000_000)]}, break_log_at=1)
    assert stops == [30], stops                                                                          # the SIGSTOP went out although the append raised, and the guard did not die
    said = [a[0][-1] for a in runs]
    assert sum("STOPPED WITHOUT a log line" in m and "kill -CONT 30" in m and "restage and a2.undo cannot see it" in m for m in said) == 1, said     # and one journal line names the pid, the error and the resume command
    assert not any(m.startswith("SUSPENDED pid 30 ") for m in said), said                                # no ordinary line claims a log that does not exist
    assert 30 in ev.stopped, ev.stopped                                                                  # it IS stopped, and the guard knows
    for to in tos:
        texts = [b[1] for b in ev.boxes if b[0][4] == "agi-" + to and b[1].startswith("[memguard-susp-30]")]
        assert len(texts) == 1 and "STOPPED WITHOUT a log line" in texts[0] and "kill -CONT 30" in texts[0], (to, texts)      # the master reads it


def test_memguard_an_unwritable_log_never_costs_a_stop_and_is_said_once_per_episode(tmp_path):
    tos = _vs()["MEMGUARD_ALERT_TO"].split()
    hide = {0: [(20, "cmd", "zzz-new --title-rewritten")]}                       # a SECOND red alert (no harness found) in the same tick
    # ONE tick holds a SPIKE (30 -> 20 GiB), the no-harness alert and a runaway; the log is a directory since the tick began
    adj, stops, runs, ev = _guard_pass(tmp_path / "a", _post_unit(), passes=2, avails=[30 * GIB, 20 * GIB], grow={1: [(30, 7_000_000)]}, rewrite=hide, break_log_at=1)
    assert stops == [30], stops                                                       # the runaway was stopped although the first red alerts of the tick could not be logged
    said = [a[0][-1] for a in runs]
    assert any(m.startswith("SPIKE") for m in said) and any("no harness found" in m for m in said), said          # the other alerts still reached the journal
    assert sum("[memguard-log] unwritable" in m for m in said) == 1, said                 # and the unwritable log is said ONCE for the episode, not once per failed line
    for to in tos:
        kinds = [b[1].split(" ")[0] for b in ev.boxes if b[0][4] == "agi-" + to]
        assert kinds.count("[memguard-log]") == 1 and kinds.count("[memguard-spike]") == 1, (to, kinds)
    # an episode ends at the first good write: broken at pass 1, repaired and written at pass 2, broken again at pass 3 = a SECOND line
    adj, stops, runs, ev = _guard_pass(tmp_path / "b", _post_unit(), passes=4, avails=[30 * GIB, 20 * GIB, 15 * GIB, 8 * GIB], break_log_at={1, 3}, fix_log_at={2})        # a SPIKE at every pass but the first
    said = [a[0][-1] for a in runs]
    assert sum(m.startswith("SPIKE") for m in said) == 3, said                         # pass 2's line is WRITTEN (the good write that ends the episode), passes 1 and 3 are not
    for to in tos:
        kinds = [b[1].split(" ")[0] for b in ev.boxes if b[0][4] == "agi-" + to]
        assert kinds.count("[memguard-log]") == 2, (to, kinds)
    # and when the notice cannot even be SPAWNED (runuser missing) while the log is unwritable: the failed-notice line goes through the same best-effort write
    adj, stops, runs, ev = _guard_pass(tmp_path / "c", _post_unit(), passes=2, avails=[30 * GIB, 20 * GIB], grow={1: [(30, 7_000_000)]}, break_log_at=1, popen_raises=True)
    assert stops == [30], stops


def test_memguard_the_stop_neither_waits_on_logger_nor_dies_of_it(tmp_path):
    spike = dict(avails=[30 * GIB, 20 * GIB], grow={1: [(30, 7_000_000)]})            # ONE tick: a SPIKE (its line is logged BEFORE the stop sites) and a runaway
    # (a) logger cannot be spawned (fork EAGAIN, logger missing): the tick lives, the runaway is stopped, the journal failure is written to the file
    adj, stops, runs, ev = _guard_pass(tmp_path / "a", _post_unit(), passes=2, logger_raises=True, **spike)
    assert stops == [30], stops
    filed = (tmp_path / "a" / "guard.log").read_text()
    assert "SPIKE" in filed and "SUSPENDED pid 30 " in filed and "journal line not written" in filed, filed
    assert any(b[1].startswith("[memguard-spike]") for b in ev.boxes) and any(b[1].startswith("[memguard-susp-30]") for b in ev.boxes), [b[1][:30] for b in ev.boxes]      # the notices still go out
    # (b) logger HANGS (journald's /dev/log slow under the reclaim): no call in the guard WAITS on it, so the stop is in the same tick, and the hung child is only held in the pending list
    adj, stops, runs, ev = _guard_pass(tmp_path / "b", _post_unit(), passes=2, logger_hangs=True, **spike)
    assert stops == [30], stops
    assert not any(e[0] == "run" for e in ev.seq), [e for e in ev.seq if e[0] == "run"]          # no blocking subprocess.run anywhere: a hung logger cannot hold the tick
    k = _kill_at(ev, 30)
    assert any(e[0] == "log" and e[1].startswith("SPIKE") for e in ev.seq[:k]), ev.seq[:k]         # the SPIKE line WAS spawned before the stop, and the stop did not wait for it
    assert not any(e[0] == "wait" for e in ev.seq[:k]), [e for e in ev.seq[:k] if e[0] == "wait"]      # council 3/3 00:31Z remark: no wait()/communicate() on any child, logger included, before the SIGSTOP
    assert ev.largv and all(a[:3] == ["timeout", "30", "logger"] for a, kw in ev.largv), ev.largv          # a hung logger is killed at 30 s ...
    assert all(kw.get("stdin") is subprocess.DEVNULL and kw.get("stdout") is subprocess.DEVNULL and kw.get("stderr") is subprocess.DEVNULL for a, kw in ev.largv)      # ... and owns no pipe of the guard
    held = [q for q in ev.pend if type(q).__name__ == "_L"]
    assert len(held) >= 1 and all(q.poll() is None for q in held), ev.pend                          # ... and is REAPED through the pending list, not forgotten (the hung ones are still in it)


def test_memguard_a_wait_on_the_logger_before_the_stop_is_red_on_row_b(tmp_path):
    """MUTANT of row (b): the journal line is waited on (p.wait()) right after its Popen. The fake logger records the wait, and the stop's tick shows it BEFORE the SIGSTOP."""
    old = "pend.append(subprocess.Popen(['timeout', '30', 'logger', '-t', 'agi-memguard', msg], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))"
    src = R.rendered(BY_NAME["memguard-script"], _vs())
    assert src.count(old) == 1, old
    spike = dict(avails=[30 * GIB, 20 * GIB], grow={1: [(30, 7_000_000)]})
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=2, logger_hangs=True, mutate=lambda t: t.replace(old, old[:-1] + "); pend[-1].wait(" + ")"), **spike)
    assert stops == [30], stops
    assert any(e[0] == "wait" and e[1] == "logger" for e in ev.seq[:_kill_at(ev, 30)]), ev.seq      # the mutant waits before the stop: row (b)'s predicate sees it


def test_memguard_the_one_blocking_call_is_the_systemctl_show_at_the_tick_end_with_timeout_10(tmp_path):
    """The council's correction (00:31Z 10-12, goal:g7.16.1.11.40.1): 'the guard has NO blocking child call' was false. baseline()'s `systemctl show` is check_output with timeout=10, ONE per tick, and it runs AFTER every stop of its tick: a size stop in the NEXT tick can wait at most 10 s behind it, a low stop never (fetches never run below the low line)."""
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(big=(21,)), passes=3, spawn={1: _TOOL}, sysd={_unit(): "OOMScoreAdjust=200\nNice=3\n"})
    assert stops == [21], stops
    assert len(ev.sysd) == 1 and ev.sysd_kw[0].get("timeout") == 10, (ev.sysd, ev.sysd_kw)           # one fetch, bounded at 10 s
    kinds = [o[0] for o in ev.order]
    assert "stop" in kinds and "fetch" in kinds and kinds.index("stop") < kinds.index("fetch"), ev.order       # the stop of the tick is out before the fetch begins
    assert not any(e[0] == "run" for e in ev.seq), ev.seq                                                  # and no subprocess.run anywhere


# --- goal:g7.16.1.11.20.2 C3: every alert is ALSO one alarm line in the sending seat's spool; root signs nothing ----------

def _spool_argv(v, text):
    seat = v["MEMGUARD_ALARM_SEAT"]
    return ["timeout", "30", "runuser", "-u", "agi-" + seat, "--", "python3", v["ALARM_SPOOL_PY"], "append", "--job", "memguard", "--to", v["MEMGUARD_ALARM_TO"],
            "--max-lines", v["ALARM_SPOOL_MAX"], "--spool", "%s/%s/alarm.spool" % (v["MEMGUARD_STORES"], seat), "--text", text]


def _one_append_per_alert(ev):
    """True when the alerts of the run produced exactly ONE spool append each (the notices go to every recipient, the alarm to ONE reader)."""
    return len(ev.spools) > 0 and len(ev.boxes) == len(ev.spools) * len(_vs()["MEMGUARD_ALERT_TO"].split())


def test_memguard_a_red_alert_is_one_plain_spool_append_as_the_sending_seat(tmp_path):
    v = _vs()
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(big=(21,)))
    assert stops == [21], stops
    (argv,) = ev.spools                                                              # ONE line, though the notice went to every recipient
    assert argv == _spool_argv(v, argv[-1]), argv                                    # runuser AS the sending seat, a plain append, no env, no key, no box
    assert argv[-1].startswith("[memguard-susp-21] SUSPENDED pid 21") and " (ev " in argv[-1], argv[-1]
    assert argv[-1] == ev.boxes[0][1], "the spool line and the notice are the same alert"
    assert _one_append_per_alert(ev)
    # a second stop in the same minute is its own alert, its own line
    adj, stops, runs, ev = _guard_pass(tmp_path / "two", _post_unit(big=(21, 23)))
    assert sorted(a[-1].split(" ")[0] for a in ev.spools) == ["[memguard-susp-21]", "[memguard-susp-23]"], ev.spools


def test_memguard_the_spool_follows_the_notice_cooldown_exactly(tmp_path):
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=4, avails=[30 * GIB, 20 * GIB, 15 * GIB, 8 * GIB])      # a SPIKE at every pass but the first, inside one cooldown
    assert ev.spools and _one_append_per_alert(ev), (len(ev.spools), len(ev.boxes))
    kinds = [a[-1].split(" ")[0] for a in ev.spools]
    assert kinds.count("[memguard-spike]") == 1, kinds                                # not one line per pass


def test_memguard_a_spool_that_cannot_be_spawned_is_written_and_never_stops_the_stop(tmp_path):
    adj, stops, runs, ev = _guard_pass(tmp_path, _post_unit(), passes=2, avails=[30 * GIB, 20 * GIB], grow={1: [(30, 7_000_000)]}, popen_raises=True)
    assert stops == [30], stops
    filed = (tmp_path / "guard.log").read_text()
    assert "alarm spool for %s not appended" % _vs()["MEMGUARD_ALARM_SEAT"] in filed and "SUSPENDED pid 30 " in filed, filed


@pytest.mark.parametrize("old,new", [
    ("notice(line); spool(line)", "notice(line); spool(line); spool(line)"),          # M1: the alarm doubled
    ("notice(line); spool(line)", "notice(line)"),                                    # M2: root never appends: the alarm is lost
    ("notice(line); spool(line)", "notice(line); [spool(line) for _ in '{{MEMGUARD_ALERT_TO}}'.split()]".replace("{{MEMGUARD_ALERT_TO}}", "sanctuary-master belam")),   # M3: one line per notice recipient
])
def test_memguard_each_spool_mutant_is_red_on_the_one_append_row(tmp_path, old, new):
    marker = "notice(line); spool(line)"
    probe = _guard_pass(tmp_path / "real", _post_unit(big=(21,)))[3]
    assert _one_append_per_alert(probe)                                              # GREEN on the real render
    def mutate(src):
        assert src.count(old) == 1, old                                               # anchor: 0 or 2 matches prove nothing
        return src.replace(old, new)
    ev = _guard_pass(tmp_path / "mut", _post_unit(big=(21,)), mutate=mutate)[3]
    assert not _one_append_per_alert(ev), f"mutant {new!r} survived: {len(ev.spools)} appends for {len(ev.boxes)} notices"


# --- goal:g7.16.1.11.40.1.1 target 3a: the vfs_cache_pressure stopgap lives in /etc/sysctl.d as BYTES (a node), not a hand-typed sysctl -----------

def test_the_sysctl_row_is_a_conf_in_sysctl_d_carrying_the_configured_value_only():
    piece = BY_NAME["agi-vm-sysctl"]
    assert piece["dest_cell"] == "sysctl_d_dir" and piece["dest_rel"] == "60-agi-vm.conf" and piece["mode"] == "0644" and piece["placeholders"] == ["VFS_CACHE_PRESSURE"]
    assert CELLS["sysctl_d_dir"] == "etc/sysctl.d"
    v = _vs()
    got = R.rendered(piece, v)
    live = [l for l in got.splitlines() if l and not l.startswith("#")]
    assert live == ["vm.vfs_cache_pressure = " + v["VFS_CACHE_PRESSURE"]], live                   # one setting, no stray key
    assert 100 < int(v["VFS_CACHE_PRESSURE"]) <= 500                                               # above the default, inside the council's 200-500
    assert R.rendered(piece, {**v, "VFS_CACHE_PRESSURE": "350"}).splitlines()[-1] == "vm.vfs_cache_pressure = 350"   # the value is the cell, none in the template
