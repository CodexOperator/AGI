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


def _labeled_spawn(tmp_path, monkeypatch, capsys, rows, argv_extra):
    """goal:g15.25 label tests — seed a row set WITH `label_word` cells and
    run `spawn --dry-run`, returning (out, err)."""
    root = tmp_path / "root"
    _write_seats(root, rows)
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


def _label_line(out):
    for ln in out.splitlines():
        if ln.startswith("label: "):
            return ln.split("label: ", 1)[1]
    return None


def test_spawn_labeled_seat_prints_label_and_window_separately(
        monkeypatch, tmp_path, capsys):
    # g15.25 (hypothesis:l4-non-prime-posts-are-generation-less-...): a
    # non-prime row's GUI label is the ROW NAME ALONE even when a
    # `label_word` cell is present (that cell is retired); the tmux WINDOW
    # keeps the plain seat name — read apart on the dry-run lines, no tmux.
    out, _ = _labeled_spawn(
        tmp_path, monkeypatch, capsys,
        [{"name": "director-post", "role": "director", "model": "x",
          "label_word": "main"}],
        {"seat": "director-post"})
    assert _resolved(out) == "'director-post'"     # the tmux window name
    assert _label_line(out) == "'director-post'"


def test_spawn_labeled_seat_without_label_word_prints_bare_label(
        monkeypatch, tmp_path, capsys):
    # no `label_word` cell -> the same ROW NAME (no generation suffix)
    out, _ = _labeled_spawn(
        tmp_path, monkeypatch, capsys,
        [{"name": "director-post", "role": "director", "model": "x"}],
        {"seat": "director-post"})
    assert _resolved(out) == "'director-post'"
    assert _label_line(out) == "'director-post'"


def test_spawn_label_is_never_gen_or_label_word(monkeypatch, tmp_path, capsys):
    """g15.25 conjunct (5) falsifier: a non-prime post's GUI label carries
    NO generation suffix and NO `label_word` — the row name alone."""
    out, _ = _labeled_spawn(
        tmp_path, monkeypatch, capsys,
        [{"name": "post-x", "role": "director", "model": "x",
          "label_word": "main"}],
        {"seat": "post-x"})
    lbl = _label_line(out)
    assert lbl == "'post-x'"
    assert "-g1" not in lbl and "main" not in lbl


def test_spawn_prime_seat_prints_no_label_line(monkeypatch, tmp_path, capsys):
    # a prime_director row has NO label — the chain numeral stays the name and
    # no `label:` line is printed (nothing to decouple).
    out, _ = _labeled_spawn(
        tmp_path, monkeypatch, capsys,
        [{"name": "prime-win", "role": "prime_director", "model": "y"}],
        {"seat": "prime-win"})
    assert _resolved(out) == "'belam-S1-II'"
    assert _label_line(out) is None


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