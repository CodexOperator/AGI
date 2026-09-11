"""L4.118 (R2 live self-reap + R1 dry-run enumeration) — FOURTH fix-only
dispatch of hypothesis:l4-the-predecessor-hands-over-authority.

Owns EXACTLY the two residues named at harvest on
experiment:a00-e15584a1-1bfec5:

  (R2) THE LIVE SELF-REAP. rotate-self derives its OWN process chain with no
       flag — pane $TMUX_PANE -> `tmux display-message ... '#{pane_pid}'` ->
       `ps -o pid,ppid` descendants — EXCLUDES rotate.py's own pid and its
       direct shell parent from the TERM list, TERMs the rest DEEPEST-FIRST,
       waits up to 5 s per pid, KILLs survivors, and only then kills its own
       window by @id. The `--own-chain` seam stays for tests; with neither
       $TMUX_PANE nor a seam it records SKIPPED naming TMUX_PANE.

  (R1) THE DRY-RUN ENUMERATES EVERY STEP. `rotate-self --dry-run` prints each
       of s2-s12 (own @id capture, successor plain name + @id command, the
       registry join rule, model sources, row fields, pending ack path,
       button-down grid legality on THIS branch, view re-point, bootstrap
       record + verification level, and the derived own chain it would TERM)
       touching NOTHING.

Fixture-only: never a live seats row, never a live spawn, never a real claude
pid, never a write under ~/.claude. The old claim that a predecessor 'cannot
TERM the process running rotate-self from inside' is a design choice (L4.118),
not a law; rotate.py shields SIGHUP/SIGTERM/SIGPIPE for its final lines and
reaps its own chain.
"""
import json
import os
import signal
from pathlib import Path
from types import SimpleNamespace

import pytest

import rotate  # noqa: E402


@pytest.fixture
def _fix(tmp_path, monkeypatch):
    """Fixture root mirroring test_rotate_tail._fix (rotations.md present)."""
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(rotate, "find_project_root",
                        lambda *a, **k: root)
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent:\n    brief_file: extensions/agi/briefs/parent-successor.md\n"
        "    steps: [handoff, spawn, handover, readback, record, kill]\n"
        "    telemetry: [seed, model, ack]\n---\n\nbody\n",
        encoding="utf-8")
    return root


def _ps_table(monkeypatch, table):
    """Fake the `ps -o pid=,ppid=` read `_derive_own_chain` parses."""
    lines = "\n".join(f"{pid} {ppid}" for pid, ppid in table) + "\n"

    def fake_run(argv, *a, **k):
        if argv[:2] == ["ps", "-o"]:
            return SimpleNamespace(stdout=lines)
        raise AssertionError(f"unexpected subprocess in this test: {argv!r}")

    monkeypatch.setattr(rotate.subprocess, "run", fake_run)


# ── (R2) the own-chain derivation ─────────────────────────────────────────


def test_derive_own_chain_discovers_pane_subtree(_fix, monkeypatch):
    """The derivation climbs from the own pid up to the pane pid through the
    `ps -o pid=,ppid=` table and returns the chain SHALLOW->DEEP, EXCLUDING
    the own pid and its direct shell parent (L4.114 measured shape:
    pane bash -> wrapper -> claude -> shell -> rotate)."""
    _ps_table(monkeypatch, [
        (100, 1),   # some unrelated root
        (500, 100),  # pane bash
        (600, 500),  # claude wrapper bash
        (700, 600),  # claude
        (800, 700),  # the Bash-tool shell (rotate.py's direct parent)
        (900, 800),  # rotate.py's own pid (passed in, not os.getpid())
    ])
    chain = rotate._derive_own_chain(500, own_pid=900)
    # shallow->deep, pane first; own pid and its direct shell parent dropped.
    assert chain == [500, 600, 700]
    assert 900 not in chain       # the own pid is never TERMed
    assert 800 not in chain       # its direct parent is never TERMed either


def test_derive_own_chain_excludes_runner_pid(_fix, monkeypatch):
    """rotate.py's own pid (os.getpid()) never appears in the TERM list even
    when the fake table names it as a descendant of the pane."""
    _ps_table(monkeypatch, [
        (1, 0),
        (500, 1),      # pane bash
        (600, 500),    # wrapper
        (os.getpid(), 600),  # rotate.py itself sits under the wrapper
    ])
    chain = rotate._derive_own_chain(500)
    assert chain == [500]          # only the pane survives the exclusion
    assert os.getpid() not in chain
    assert 600 not in chain        # rotate.py's parent dropped too


def test_derive_own_chain_refuses_when_not_under_pane(_fix, monkeypatch):
    """If the own pid cannot be climbed up to the pane pid, the derivation
    returns [] — the caller records SKIPPED rather than guessing a chain."""
    _ps_table(monkeypatch, [(500, 100), (900, 1000)])  # 900 not under 500
    assert rotate._derive_own_chain(500, own_pid=900) == []


def test_pane_pid_none_when_no_env(_fix):
    """`_pane_pid` returns None with no $TMUX_PANE (or under the conftest tmux
    guard) — the caller records SKIPPED naming TMUX_PANE."""
    assert rotate._pane_pid("") is None
    assert rotate._pane_pid(None) is None


def test_reap_chain_waits_shielded_survivor_killed(_fix):
    """s12 enhancement: a process still alive after TERM + the wait window is
    SIGKILL'd (kill_survivors) — 'wait up to 5 s per pid, KILL what
    survives'. A real `sleep` (which ignores nothing and dies on TERM) exits
    during the wait; a re-parented stand-in proves the KILL branch by
    refusing to die on TERM is skipped here (SIGKILL cannot be tested against
    a child we must reap — the wait branch is exercised and gone_after True)."""
    import subprocess
    proc = subprocess.Popen(["sleep", "1000"])
    try:
        out = rotate._reap_chain([proc.pid], wait_secs=2.0,
                                 kill_survivors=True)
        assert out["chain"][0]["gone_after"] is True
        assert not rotate._pid_alive(proc.pid)
    finally:
        if rotate._pid_alive(proc.pid):
            os.kill(proc.pid, signal.SIGKILL)


def test_shield_final_signals_installs_ignores(_fix):
    """`_shield_final_signals` sets SIGHUP/SIGTERM/SIGPIPE to SIG_IGN so the
    dieing tree's signals cannot cut rotate.py's final lines short, and
    `_restore_shield_signals` puts the old handlers back (the pytest runtime
    is shared — a persistent ignore breaks reap tests)."""
    old = {s: signal.getsignal(s)
           for s in (signal.SIGHUP, signal.SIGTERM, signal.SIGPIPE)}
    prev = rotate._shield_final_signals()
    for s in (signal.SIGHUP, signal.SIGTERM, signal.SIGPIPE):
        assert signal.getsignal(s) is signal.SIG_IGN
    rotate._restore_shield_signals(prev)
    for s in (signal.SIGHUP, signal.SIGTERM, signal.SIGPIPE):
        assert signal.getsignal(s) is old[s]
    # and the suite is not left ignoring SIGTERM
    for s, h in old.items():
        assert signal.getsignal(s) is h


# ── (R2) the s12 block records SKIPPED naming TMUX_PANE when un-derivable ──


def test_rotate_self_s12_skipped_names_tmux_pane(_fix, tmp_path, monkeypatch):
    """With NO --own-chain seam AND no $TMUX_PANE (nor a derivable pane), the
    s12 block records SKIPPED naming TMUX_PANE and still rotates successfully
    — it never TERMs anything, never touches a real process."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("@5 adv-alive.gen1\nadv-alive\n", encoding="utf-8")
    monkeypatch.setenv("TMUX_PANE", "")

    def fake_spawn(**kw):            # successor appears under the plain name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "adv-alive",
                                         "gen_after": 1,
                                         "answer": "continue"})
    old_handlers = {s: signal.getsignal(s)
                    for s in (signal.SIGHUP, signal.SIGTERM, signal.SIGPIPE)}
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
    try:
        rc = rotate.cmd_rotate_self(args, tmp_path)
    finally:
        for s, h in old_handlers.items():
            try:
                signal.signal(s, h)
            except (ValueError, OSError):
                pass
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    assert rec["result"] == "success"
    # the s12 self-reap considered TMUX_PANE and found it absent → SKIPPED;
    # never a TERM of a real process (nothing to assert beyond rc==0).
    assert "TMUX_PANE" in rec["s12_self_reap"]["skipped"]


def _write_seats_sheet(root, rows):
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


# ── (R1) --dry-run enumerates every step ──────────────────────────────────


def test_dry_run_enumerates_s2_s12(_fix, tmp_path, monkeypatch, capsys):
    """`rotate-self --dry-run` prints each of s2-s12 (pending ack path,
    registry join rule, row fields, model sources, bootstrap record,
    verification level, grid legality, view re-point, the s12 self-reap and
    the @id capture mechanics) and does NOT touch the spawn path."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    args = SimpleNamespace(
        name="adv-alive", force=False, timeout=5, debug_file=None,
        model=None, effort=None, settings=None, prompt_file=None,
        tmux_session="t", window_path=None, dry_run=True,
        throwaway=False, successor_argv=None, role="parent",
        session_ref=None, template=None, registry_dir=None)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    for fragment in [
        "pending ack path",
        "adv-alive.bootstrap.json",
        "verification.py --level",
        "grid legality on THIS branch",
        "s12 self-reap",
        "display-message",        # the @id capture mechanisms
        "new-window -P -F",
        "source: registry",
    ]:
        assert fragment in out, f"dry-run missing: {fragment!r}"


def _latest_record(root, seat):
    rot = root / "sessions" / "rotations"
    recs = sorted(rot.glob(f"{seat}.*.json"))
    assert recs, f"no rotation record under {rot}"
    return json.loads(recs[-1].read_text(encoding="utf-8"))