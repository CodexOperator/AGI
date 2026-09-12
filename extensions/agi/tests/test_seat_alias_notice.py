"""test_seat_alias_notice.py — hypothesis:l4-a-seat-is-a-post-everywhere.

Every entry point that carries `--seat`/`--post` must route through ONE shared
argparse action (geometry_config.SeatAction) so a literal `--seat` prints the
deprecated-alias notice at most ONCE per process, `--post` stays silent, and
both set the same dest. The notice goes to STDERR (these parsers feed hooks
and shell callers that parse stdout).

Before this landed (fix-only round 2, KID B) only dispatch.py fired the
notice; rotate.py (13 sites), handoff.py, mail_alert.py, season.py and send.py
carried `--seat` as a plain store, so the alias was silently accepted there.
Regression guard: a NEW `--seat` add_argument that forgets the action fails
the wiring scan below and is silently accepted no more.
"""

import argparse
import ast
import importlib
import sys
from pathlib import Path

import pytest

import geometry_config

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

# (module, argv_to_build_parser, argv_to_parse_with_seat, expected_dest)
# argv_to_build_parser is only used to run the module's main() far enough to
# CONSTRUCT its real parser tree; execution is stopped inside the CLI's own
# parse_args (which must never actually run — dispatch has side effects).
_WIRED_MODULES = [
    # rotate.py — 13 `--seat`/`--post` subcommands; probe one.
    ("rotate", ["meter"], ["meter", "--seat", "alice"], "seat"),
    # handoff.py — dest is "holder", not "seat".
    ("handoff", ["claim", "sec"], ["claim", "sec", "--seat", "bob"], "holder"),
    # mail_alert.py — flat parser.
    ("mail_alert", [], ["--seat", "carol"], "seat"),
    # season.py — merge-up carries the alias.
    ("season", ["merge-up", "branch"], ["merge-up", "branch", "--seat", "dave"], "seat"),
    # send.py — keygen carries the alias.
    ("send", ["keygen"], ["keygen", "--seat", "erin"], "seat"),
]

class _StopParse(Exception):
    """Raised from a parse_args spy to stop main() right after the parser tree
    is built — before any dispatch/side effect runs."""


def _build_parser(module_name: str, argv: list[str]) -> argparse.ArgumentParser:
    """Return the real parser tree a module builds in main() without running
    any dispatch. The first parse_args call inside main() is intercepted."""
    real = argparse.ArgumentParser.parse_args
    state: dict = {}

    def _spy(self, args=None, namespace=None):
        state["parser"] = self
        raise _StopParse()

    argparse.ArgumentParser.parse_args = _spy
    try:
        importlib.import_module(module_name).main(argv)
    except _StopParse:
        pass
    finally:
        argparse.ArgumentParser.parse_args = real
    return state["parser"]


# --- the ONE shared action -------------------------------------------------


def test_seat_notice_once_to_stderr_and_sets_dest(capsys):
    geometry_config._seen_flag = False
    ap = argparse.ArgumentParser()
    ap.add_argument("--seat", "--post", action=geometry_config.SeatAction,
                    dest="x", default=None)

    ns = ap.parse_args(["--seat", "alice"])
    out, err = capsys.readouterr()
    assert ns.x == "alice"
    assert "deprecated" in err and "--post" in err
    assert out == ""  # the notice must never leak to stdout

    # second `--seat` in the SAME process: silent (once-per-process).
    ns2 = ap.parse_args(["--seat", "bob"])
    out2, err2 = capsys.readouterr()
    assert err2 == "" and out2 == ""
    assert ns2.x == "bob"


def test_post_is_silent_and_sets_same_dest(capsys):
    geometry_config._seen_flag = False
    ap = argparse.ArgumentParser()
    ap.add_argument("--seat", "--post", action=geometry_config.SeatAction,
                    dest="x", default=None)

    ns = ap.parse_args(["--post", "carol"])
    out, err = capsys.readouterr()
    assert ns.x == "carol"
    assert err == "" and out == ""


def test_enforces_once_per_process_globally(capsys):
    # two separate parsers, one process: ONE notice total.
    geometry_config._seen_flag = False
    ap = argparse.ArgumentParser()
    ap.add_argument("--seat", "--post", action=geometry_config.SeatAction,
                    dest="x", default=None)
    ap2 = argparse.ArgumentParser()
    ap2.add_argument("--seat", "--post", action=geometry_config.SeatAction,
                     dest="x", default=None)

    ap.parse_args(["--seat", "a"])
    capsys.readouterr()
    ap2.parse_args(["--seat", "b"])
    out, err = capsys.readouterr()
    assert err == ""
    assert ap2.parse_args(["--post", "c"]).x == "c"


# --- wiring: every entry point routes through the shared action ------------


@pytest.mark.parametrize("mod, build_argv, parse_argv, dest",
                         _WIRED_MODULES, ids=[m for m, *_ in _WIRED_MODULES])
def test_real_parser_seat_wires_notice_and_post_silent(capsys, mod, build_argv, parse_argv, dest):
    geometry_config._seen_flag = False
    parser = _build_parser(mod, build_argv)

    # `--post x` first: silent, sets dest.
    post_argv = list(parse_argv)
    post_argv[post_argv.index("--seat")] = "--post"
    ns_post = parser.parse_args(post_argv)
    out, err = capsys.readouterr()
    assert err == "" and out == ""
    assert getattr(ns_post, dest) == parse_argv[-1]

    # `--seat x`: notice once (now the same process has seen the flag), dest set.
    ns_seat = parser.parse_args(parse_argv)
    out, err = capsys.readouterr()
    assert getattr(ns_seat, dest) == parse_argv[-1]
    assert "deprecated" in err
    assert out == ""


# --- static scan: EVERY --seat add_argument routes through the action ------
#
# The dynamic probes above construct each real parser and parse with `--seat`;
# they prove the NOTICE fires. This scan is belt-and-suspenders over the SOURCE
# of every bin module: it finds each `add_argument(..., "--seat", ...)` call by
# PARSING the file (ast), never by substring sniffing, and asserts the call
# routes through geometry_config.SeatAction. A `--seat`-only site (no `--post`
# alias) is a site the old conjunction (`'--seat' in line and '"--post"' in
# line`) skipped entirely — exactly the site most likely to have forgotten the
# action — and a comment or help string that merely mentions `--seat` is not a
# site at all.


def _seat_src_violations(src: str) -> list[tuple[int, str]]:
    """Return [(lineno, line), ...] for every `add_argument(..., "--seat", ...)`
    call in `src` that does NOT route through the shared SeatAction.
    `action=...` is judged by its dotted tail resolving to `SeatAction`, so
    `geometry_config.SeatAction` (and any direct import of the same class) is
    accepted; a plain store -- or no action kwarg at all -- is a violation."""
    tree = ast.parse(src)
    lines = src.splitlines()
    violations = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        is_add_argument = (
            isinstance(func, ast.Attribute) and func.attr == "add_argument"
        ) or (isinstance(func, ast.Name) and func.id == "add_argument")
        if not is_add_argument:
            continue
        opts = [a.value for a in node.args
                if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        if "--seat" not in opts:
            continue
        action = next((kw.value for kw in node.keywords if kw.arg == "action"),
                      None)
        ok = action is not None and "SeatAction" in ast.unparse(action)
        if not ok:
            lineno = node.lineno
            line = lines[lineno - 1].strip() if lineno <= len(lines) else ""
            violations.append((lineno, line))
    return violations


def _seat_modules() -> list[str]:
    """Every bin/*.py that registers the `--seat` option string -- discovered
    by AST so a NEW seat-aware module is auto-covered by the static scan."""
    found = []
    for f in sorted(BIN.glob("*.py")):
        try:
            tree = ast.parse(f.read_text())
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "add_argument"):
                opts = [a.value for a in node.args
                        if isinstance(a, ast.Constant)
                        and isinstance(a.value, str)]
                if "--seat" in opts:
                    found.append(f.name)
                    break
    return found


def test_static_scan_reports_site_count_and_names():
    """Document the current whole-tree census: how many `--seat` add_argument
    sites bin/ registers and where. The count is asserted so a NEW seat-aware
    site surfaces here (this test is the pointer, the parametrized scan below
    is the gate; both must be updated together)."""
    sites = []
    for f in sorted(BIN.glob("*.py")):
        try:
            tree = ast.parse(f.read_text())
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "add_argument"):
                opts = [a.value for a in node.args
                        if isinstance(a, ast.Constant)
                        and isinstance(a.value, str)]
                if "--seat" in opts:
                    sites.append(f"{f.name}:{node.lineno}")
    assert len(sites) == 21, sites


@pytest.mark.parametrize("fname", _seat_modules())
def test_static_scan_every_seat_add_argument_has_the_action(fname):
    """Belt-and-suspenders: EVERY `--seat` add_argument in bin/ routes through
    the shared SeatAction. A regression that forgets the action -- or a
    `--seat`-only site that never received the `--post` alias -- fails here and
    names the exact line. The dynamic probes also flag most of these; this one
    needs no parser construction and catches every site in the tree."""
    bad = _seat_src_violations((BIN / fname).read_text())
    assert bad == [], (
        f"{fname} has a --seat add_argument that forgot "
        f"action=geometry_config.SeatAction: {bad}"
    )


def test_static_scan_bites_when_action_removed_in_fixture_copy(tmp_path):
    """The falsifier, exercised on a COPY (never in the tree): strip the shared
    action off ONE real --seat site and the scan MUST flag it. A scan never
    shown to fail on a defective input is vacuous."""
    # A single-site module gives the cleanest removal to prove.
    victim = None
    src = None
    for f in sorted(BIN.glob("*.py")):
        s = f.read_text()
        if (len(_seat_src_violations(s)) == 0
                and s.count('"--seat", "--post"') == 1
                and "action=geometry_config.SeatAction" in s):
            victim, src = f, s
            break
    assert victim is not None, "no single-site module to seed a defect in"
    # the seed module must itself be clean, else the remove-replace confuses
    assert _seat_src_violations(src) == []
    # locate the (single) --seat site's line via AST
    seat_site_line = next(
        node.lineno
        for node in ast.walk(ast.parse(src))
        if (isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_argument"
            and "--seat" in [a.value for a in node.args
                             if isinstance(a, ast.Constant)
                             and isinstance(a.value, str)])
    )
    broken = src.replace("action=geometry_config.SeatAction",
                         'action="broken"', 1)
    copy = tmp_path / f"{victim.stem}.py"
    copy.write_text(broken)
    bad = _seat_src_violations(copy.read_text())
    assert bad, f"scan failed to flag the seeded defect in {copy.name}"
    assert bad[0][0] == seat_site_line, bad


def test_static_scan_ignores_prose_that_mentions_seat():
    """Parsing the source (not substring sniffing) is what keeps a comment or
    help string that mentions `--seat` from counting as a site."""
    src = (
        '"""Whois may be given --seat to resolve a row."""\n'
        '# a comment: run --seat --post with SeatAction here\n'
        'p = argparse.ArgumentParser()\n'
        'p.add_argument("--post", default=None, help="canonical seat name")\n'
    )
    assert _seat_src_violations(src) == []


def test_static_scan_legit_post_only_not_flagged_but_bare_seat_is():
    """A `--post`-only registration is the intended shape and must NOT fire;
    a conforming `--seat`/`--post` pair must not fire; a bare `--seat` store
    (the defect the old conjunction skipped) MUST fire."""
    post_only = 'p.add_argument("--post", default=None)\n'
    assert _seat_src_violations(post_only) == []
    conforming = ('p.add_argument("--seat", "--post", '
                  'action=geometry_config.SeatAction, default=None)\n')
    assert _seat_src_violations(conforming) == []
    bare = 'p.add_argument("--seat", default=None)\n'
    bad = _seat_src_violations(bare)
    assert bad and "SeatAction" not in bare