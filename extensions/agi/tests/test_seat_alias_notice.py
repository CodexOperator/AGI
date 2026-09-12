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

_touched = [f"{m}.py" for m, *_ in [tuple(r[:1]) for r in _WIRED_MODULES]]


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


@pytest.mark.parametrize("fname", _touched)
def test_static_scan_every_seat_add_argument_has_the_action(fname):
    """Belt-and-suspenders: any `--seat`/`--post` add_argument that forgot the
    shared action fails the scan — a regression the dynamic probes also flag
    but this names the exact line."""
    src = (BIN / fname).read_text()
    lines = src.splitlines()
    for i, line in enumerate(lines):
        if '--seat' in line and '"--post"' in line:
            assert "SeatAction" in line, (
                f"{fname}:{i + 1} --seat/--post add_argument forgot "
                f"action=geometry_config.SeatAction: {line.strip()}"
            )