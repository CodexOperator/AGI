"""The boxkit acceptance suite for
hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes.

Rows 1-13, one per clause of the claim (12 = the leak-root floor, 13 = the stand-in
substitution order; both were residues of an earlier probe):

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
   counterparts (test 10b), and agi-survival-conf is new to the kit and has none;
10: the manifest covers EVERY unit goal:g7.33.18's no-cascade row names, read from
    the LIVE goal node (never a copied list), and each no-cascade drop-in is compared
    against its RECORDED LIVE bytes by the DECLARED delta, line for line: a converging
    and a differently-drifting render are both RED, and a row with no recorded live
    bytes is a NAMED skip, never a silent pass.
14: THE ENGINE'S OWN GUARD over the kit's bytes. Row 4 is a BESPOKE denylist
    (checkout roots, home, owner, cgroup uid) because anonymize.py's classes
    (hostname/ip/mac/board/secret) do not cover those -- which made the two DISJOINT: a
    template naming this box's hostname, a NIC address, a board serial or a key id
    passes row 4 CLEAN. ONE row runs anonymize.scan -- the guard's own function,
    MIN_TOKEN and CLASSES -- against a FAKE box denylist (this box's values are never
    read into the test): it plants one FAKE_BOX value in a COPY of one template and
    asserts scan names the CLASS, and asserts the UNPLANTED kit bytes stay clean. It
    guards a PLANTED COPY: the kit's own bytes could only go red on a real denylist.

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
import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parents[1] / "boxkit"
BIN_DIR = Path(__file__).resolve().parents[1] / "bin"
PROJECT = Path(__file__).resolve().parents[3]
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


def _leaks(text, roots=LEAK_ROOTS):
    return [t for t in (OWNER, str(Path.home()), *roots, "/.sanctuary/")
            if t and t in text]

# A probe identity: contract tests need SOME value for REPO_ROOT/GUARD_SRC to render
# at all, and a probe is not the answer -- the wire test below supplies nothing.
PROBE = {"OWNER_USER": "probe", "UID": "4242", "REPO_ROOT": "/probe/repo",
         "GUARD_SRC": "/probe/.sanctuary/guard/guard-init.sh"}


def _v(**over):
    o = dict(PROBE)
    o.update(over)
    return R.values(CFG, MEASURED, o)


def _vs(**over):
    """The values a committed fixture is rendered with: the measured inputs plus the
    fixed stand-ins. This is the OFF-BOX comparison -- the bytes a second box gets."""
    o = dict(STANDINS)
    o.update(over)
    return R.values(CFG, MEASURED, o)


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
# whether a live counterpart happens to exist is question 10b, not a property of the flag.
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
    assert R.rendered(piece, R.values(CFG, MEASURED, R.host_tokens(CFG))) != \
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
                                      {**tokens, **{k: STANDINS[k] for k in IDENTITY}}))


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
    live = R.rendered(piece, R.values(CFG, MEASURED, tokens))
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
    live = R.rendered(piece, R.values(CFG, MEASURED, tokens))
    assert live.count(collides) > sites, (
        "the synthetic collision did not force the fallback: %d occurrence(s) of %r, "
        "%d site(s)" % (live.count(collides), collides, sites))
    got = _anonymized_live_render(piece, tokens)
    fix = (FIXTURES / (piece["name"] + ".fixture")).read_text(encoding="utf-8")
    _assert_piece_matches_fixture(piece, got, fix, _vs())
    # and the render is anonymized end to end: no host identity root survives it
    assert not [t for t in HOST_TOKENS if t and t in got], piece["name"]


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
    assert {p["name"] for p in rows} == set(DRIFT_ROWS) | {"agi-survival-conf"}
    assert not [p for p in rows if p in LIVE], "a new_bytes row must not be compared as a copy"
    assert len(LIVE) == len(PIECES) - len(rows)
    for p in rows:
        assert "OOMPolicy=" in R.rendered(p, _v()), p["name"]


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
UNIT_DIR_CELL = re.compile(r"/systemd/[\w.@%{}$-]+$")


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
FAKE_BOX = {"hostname": ["boxkit-fake-host"], "ip": ["198.51.100.7"],
            "mac": ["02:00:5e:10:00:01"], "board": ["BOXKIT-FAKE-BOARD"],
            "secret": ["sk-boxkit-fake-key"]}


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
def fake_box(tmp_path, monkeypatch):
    p = tmp_path / "boxkit-fake-box.json"
    p.write_text(json.dumps(FAKE_BOX), encoding="utf-8")
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
    template (one FAKE_BOX value, one class) and the clean half on the kit's own bytes."""
    toks = anonymize.box_tokens(PROJECT)
    assert sorted({c for c, _ in toks}) == sorted(anonymize.CLASSES), \
        "the fake denylist did not reach every class; the row would be vacuous"
    cls, value = "ip", FAKE_BOX["ip"][0]
    src = TEMPLATES / BY_NAME["oomd-guard"]["template"]
    clean = src.read_text(encoding="utf-8")
    planted = tmp_path / "planted" / src.name
    planted.parent.mkdir(parents=True)
    planted.write_text(clean + "\n# a planted %s token: %s\n" % (cls, value),
                       encoding="utf-8")
    assert anonymize.scan(planted.read_text(encoding="utf-8"), toks) == [cls], cls
    # the fixture's sys.path restore is a NO-OP in a session: conftest.py:408-411 already
    # put bin/ there (measured in-session, experiment:a00-19870cd0)
    assert str(BIN_DIR) in sys.path and sys.modules["anonymize"] is anonymize
    for path, text in _kit_bytes():   # the kit's OWN bytes, incl. the clean src
        assert anonymize.scan(text, toks) == [], path.name


# 14b -- THE DISJOINTNESS itself, BOTH directions, EVERY class: row 14 walked the `ip`
# class alone, so merging the two denylists was again a silent no-op. RED if merged.
@pytest.mark.parametrize("cls", ["hostname", "ip", "mac", "board", "secret"])
def test_the_kit_denylist_and_the_engine_denylist_are_disjoint_in_both_directions(
        cls, fake_box, anonymize):
    toks = anonymize.box_tokens(PROJECT)
    value, root = FAKE_BOX[cls][0], str(R.engine_checkout())
    clean = (TEMPLATES / BY_NAME["oomd-guard"]["template"]).read_text(encoding="utf-8")
    planted = clean + "\n# a planted %s token: %s\n" % (cls, value)
    assert anonymize.scan(planted, toks) == [cls], cls
    assert _leaks(planted) == [], "row 4 covers %s: the denylists are MERGED" % cls
    assert anonymize.scan("cd %s\n" % root, toks) == [], "the guard now sees the root"
