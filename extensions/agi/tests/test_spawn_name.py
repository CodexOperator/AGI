"""goal:g15.25 build tests (hypothesis:l4-spawn-without-name-defaults-to-the-
seat-row-name-for-every-non-prime-post): a `spawn --seat X` for a NON-prime
row names the window after the post (one window, no numeral); the prime chain
/ no-seat / unkeyed-row / no-row cases keep deriving the belam numeral; an
explicit `--name` always wins. Each test runs `spawn --dry-run` (no tmux) and
reads the resolved name from the stdout `spawn name: 'X'` line.
"""
import json
from argparse import Namespace

import pytest

import rotate


def _write_seats(root, rows):
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def _spawn_name(tmp_path, monkeypatch, capsys, argv_extra):
    root = tmp_path / "root"
    _write_seats(root, [
        {"name": "director-post", "role": "director", "model": "x"},
        {"name": "prime-win", "role": "prime_director", "model": "y"},
        {"name": "nokey-post"},  # exists but has NO role cell
    ])
    prompt = root / "prompt.md"
    prompt.write_text("Hello {name}")
    windows = root / "windows.txt"
    windows.write_text("belam-S1\n", encoding="utf-8")
    base = dict(name=None, tier="director", model=None, effort=None,
                settings=None, prompt_file=str(prompt), successor_argv=None,
                seat=None, tmux_session="t", window_path=str(windows), pid=None,
                no_autopsy=False, ask_diff=False, dry_run=True)
    base.update(argv_extra)
    rc = rotate.cmd_spawn(Namespace(**base), root)
    out = capsys.readouterr().out
    assert rc == 0, out
    return out, capsys.readouterr().err


def _resolved(out):
    for ln in out.splitlines():
        if ln.startswith("spawn name: "):
            return ln.split("spawn name: ", 1)[1]
    return "<no name line>"


def test_spawn_named_seat_defaults_to_director_row_name(monkeypatch, tmp_path,
                                                        capsys):
    # director (non-prime) seat + no --name -> resolved name == row name
    out, _ = _spawn_name(tmp_path, monkeypatch, capsys,
                         {"seat": "director-post"})
    assert _resolved(out) == "'director-post'"


def test_spawn_prime_seat_keeps_belam_numeral(monkeypatch, tmp_path, capsys):
    # prime_director row + no --name -> belam numeral as today
    out, _ = _spawn_name(tmp_path, monkeypatch, capsys,
                         {"seat": "prime-win"})
    assert _resolved(out) == "'belam-S1-II'"


def test_spawn_no_seat_keeps_derive(monkeypatch, tmp_path, capsys):
    # no --seat -> unchanged derive
    out, _ = _spawn_name(tmp_path, monkeypatch, capsys, {})
    assert _resolved(out) == "'belam-S1-II'"


def test_spawn_explicit_name_wins_over_seat(monkeypatch, tmp_path, capsys):
    # --name always wins even with a non-prime --seat
    out, _ = _spawn_name(tmp_path, monkeypatch, capsys,
                         {"seat": "director-post", "name": "explicit"})
    # explicit --name is trivial, so no `spawn name:` line is printed; the
    # resolved name shows up in the launch line itself
    assert "claude --remote-control explicit" in out