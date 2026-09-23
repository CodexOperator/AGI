"""EF.68 -- two residues for
hypothesis:rotate-self-registry-gate-reads-main-and-the-wrapper-restores-signals.

  (a) REGISTRY GATE. The NON-prepare rotate-self registry gate resolves the
      seat row through `_seat_read_root(root, seat)` exactly like the
      `--prepare` branch, so the WRITER's (MAIN's) row wins over the caller's
      lagging worktree copy. Pre-fix the gate read `_find_seat(cfg_root, ...)`
      -- the worktree itself when its geometry is current -- so a seat that
      exists only in MAIN was refused `no seat`.

  (b) SIGNAL SHIELD. The SIGHUP/SIGTERM/SIGPIPE shield installed for the
      self-reap tail is restored on EVERY exit path, not just the success
      return: an exception raised inside the window must leave the three
      dispositions byte-identical to before the call (core-sync-0923 R5).
      The pytest runtime is shared, so the test restores them in its OWN
      finally on top, whether or not the fix is present.

Fixture-only: a real MAIN checkout + a linked worktree for (a); a scratch
root with the usual rotate-self seams for (b). Never a live seats row, never
a live spawn, never a real claude pid, never a tmux window.
"""
import json
import os
import signal
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import rotate  # noqa: E402


# ── (a) the non-prepare registry gate reads the writer's row ───────────────

def _write_seats(root, rows):
    gp = root / "nodes" / ".geometry"
    gp.mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (gp / "seats.md").write_text(body, encoding="utf-8")


def _make(tmp_path):
    """A MAIN checkout + one linked worktree, each with its own `.agi` graph.
    Returns (main_graph, wt_graph, seat) where the graphs are `.agi` roots."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "season/s1"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    seat = "s-director"
    wt = tmp_path / "wt"
    _write_seats(repo / ".agi", [{"name": seat, "role": "director"}])
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-a@s1", str(wt), "season/s1"],
                   check=True, capture_output=True)
    return repo / ".agi", wt / ".agi", seat


def test_nonprepare_gate_sees_main_only_seat(tmp_path, monkeypatch, capsys):
    """(a) the seat exists in MAIN and NOT in the worktree copy. The
    non-prepare registry gate must read MAIN's row and reach the closeout
    path -- pre-fix it reads the worktree, finds nothing, and refuses
    `no seat` (rc 1)."""
    main, wt, seat = _make(tmp_path)
    _write_seats(main, [{"name": seat, "role": "director"}])
    _write_seats(wt, [{"name": "someone-else", "role": "director"}])
    monkeypatch.setattr(rotate, "_resolve_template",
                        lambda *a, **k: (None, None, "test"))
    monkeypatch.setattr(rotate, "_closeout_form_json",
                        lambda *a, **k: '{"form": "REACHED-CLOSEOUT"}')
    ns = SimpleNamespace(
        name=seat, prepare=False, throwaway=False, role=None,
        template=None, closeout=True, form=None, stops=None, stops_file=None,
        dry_run=False, model=None, effort=None, settings=None)
    rc = rotate.cmd_rotate_self(ns, wt)
    out = capsys.readouterr()
    assert "no seat" not in out.err, (
        "the gate read the worktree copy, not MAIN's row: " + out.err)
    assert "REACHED-CLOSEOUT" in out.out, (
        "the gate must find MAIN's row and reach the closeout path: "
        + out.out)
    assert rc == 0


def test_nonprepare_gate_falls_back_when_main_lacks_the_seat(
        tmp_path, monkeypatch, capsys):
    """(a) the documented per-seat fallback: MAIN has NO row, the worktree
    copy does. The gate still reads the worktree copy (the same fallback the
    `--prepare` tests lock in)."""
    main, wt, seat = _make(tmp_path)
    _write_seats(main, [{"name": "someone-else", "role": "director"}])
    _write_seats(wt, [{"name": seat, "role": "director"}])
    monkeypatch.setattr(rotate, "_resolve_template",
                        lambda *a, **k: (None, None, "test"))
    monkeypatch.setattr(rotate, "_closeout_form_json",
                        lambda *a, **k: '{"form": "REACHED-CLOSEOUT"}')
    ns = SimpleNamespace(
        name=seat, prepare=False, throwaway=False, role=None,
        template=None, closeout=True, form=None, stops=None, stops_file=None,
        dry_run=False, model=None, effort=None, settings=None)
    rc = rotate.cmd_rotate_self(ns, wt)
    out = capsys.readouterr()
    assert "REACHED-CLOSEOUT" in out.out, (
        "the per-seat fallback must still reach the closeout path: "
        + out.err)
    assert rc == 0


# ── (b) the signal shield restores on an exception inside the window ───────

@pytest.fixture
def _fix(tmp_path, monkeypatch):
    """Scratch rotate-self root mirroring test_rotate_selfreap._fix."""
    monkeypatch.setattr(rotate, "DEFAULT_AFTER_JOIN_TIMEOUT_S", 0)
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(rotate, "find_project_root", lambda *a, **k: root)
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent:\n    brief_file: extensions/agi/briefs/parent-successor.md\n"
        "    steps: [handoff, spawn, handover, readback, record, kill]\n"
        "    telemetry: [seed, model, ack]\n---\n\nbody\n",
        encoding="utf-8")
    return root


def _write_seats_sheet(root, rows):
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def test_shield_restored_on_exception_inside_window(_fix, tmp_path,
                                                    monkeypatch):
    """(b) `_commit_rotation_record` raises AFTER the shield is installed and
    BEFORE the success-path `_restore_shield_signals`. The three dispositions
    must equal the pre-call ones -- pre-fix the raise leaks SIG_IGN."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("@5 adv-alive.prev\nadv-alive\n", encoding="utf-8")
    monkeypatch.setenv("TMUX_PANE", "")   # no live pane is ever reached

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                                         "answer": "continue"})

    def boom(*a, **k):
        raise RuntimeError("record commit died inside the shield window")

    monkeypatch.setattr(rotate, "_commit_rotation_record", boom)

    args = SimpleNamespace(
        name="adv-alive", force=False, timeout=5, debug_file=None,
        model=None, effort=None, settings=None, prompt_file=None,
        tmux_session="t", window_path=str(win), dry_run=False,
        throwaway=False, successor_argv=None, role="parent",
        session_ref=None, successor_transcript=None, own_pid=None,
        belam_prefix=None, own_chain=None, registry_dir=None,
        registry_poll=None, view_path=None, verification_argv=None,
        grid_commit_legal=True, grid_commit_branch=None, comms_root=None,
        trigger="rotate-self", in_flight=None)

    sigs = (signal.SIGHUP, signal.SIGTERM, signal.SIGPIPE)
    before = {s: signal.getsignal(s) for s in sigs}
    try:
        try:
            rotate.cmd_rotate_self(args, tmp_path)
            raised = False
        except Exception:  # noqa: BLE001 -- the reap died mid-flight
            raised = True
        assert raised, "the in-window exception did not reach the caller"
        for s in sigs:
            assert signal.getsignal(s) is before[s], (
                f"the shield leaked {signal.Signals(s).name} on the "
                "exception path")
    finally:
        for s in sigs:
            try:
                signal.signal(s, before[s])
            except (ValueError, OSError):
                pass
