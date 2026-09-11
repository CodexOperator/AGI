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

import subprocess

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
    """Fake the `ps -e -o pid=,ppid=` read `_derive_own_chain` parses.

    L4.122 criterion 1 (merge-up 23): the derivation enumerates ALL
    processes (`ps -e`), never the default same-tty selection. A process
    whose controlling tty differs from the caller's (the live pane chain on
    pts/18 while rotate.py runs on tty ?) MUST be visible to the climb. The
    fake table is the whole system; unrelated OTHER-tty / non-child pids are
    just rows that must not break the climb."""
    lines = "\n".join(f"{pid} {ppid}" for pid, ppid in table) + "\n"

    def fake_run(argv, *a, **k):
        if argv[:2] == ["ps", "-e"] and any("pid=,ppid=" in t for t in argv):
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

# ── L4.122 criterion 1 (merge-up 23): `ps -e` enumerates ALL processes ─────


def test_derive_own_chain_ps_e_sees_other_tty_pid(_fix, monkeypatch):
    """L4.122 criterion 1: the pane chain sits on a DIFFERENT controlling tty
    than the caller — `ps -e` must still see it. The fake table is the whole
    system; unrelated rows (pts/9 busy process, non-child roots) are just
    present, exactly the gen X live shape (pane on pts/18 while the rotate.py
    that climbs runs on tty ?). The old same-tty `ps -o pid=,ppid=` default
    returned [] for this shape on the real gen IX->X rotation."""
    _ps_table(monkeypatch, [
        (1, 0),
        (2000, 1),     # an unrelated busy process on pts/9 (OTHER-tty)
        (500, 1),      # pane bash (pts/18, OTHER-tty than the test caller)
        (600, 500),    # claude wrapper bash
        (700, 600),    # claude
        (900, 700),    # rotate.py's own pid
    ])
    chain = rotate._derive_own_chain(500, own_pid=900)
    # 900's direct parent is 700 (claude) — it is EXCLUDED like the own pid;
    # what remains is [pane bash, wrapper], the OTHER-tty chain `ps -e` saw.
    assert chain == [500, 600]


# ── L4.122 criterion 2: _reap_chain binds wpid + SIGKILLs a TERM-survivor ──


def _spawn_nonchild_sigterm_immune():
    """A grandchild that IGNORES SIGTERM and is NOT our child.

    Double-fork reparents it to PID 1, so `os.waitpid(pid, os.WNOHANG)` in
    `_reap_chain` raises ChildProcessError — the exact ancestor-pid shape of
    L4.122 criterion 2 (pane bash / wrapper / claude surviving SIGTERM). The
    intermediate is reaped here; the grandchild is returned."""
    import time as _t
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:                 # intermediate
        os.close(r)
        gpid = os.fork()
        if gpid == 0:            # the grandchild that refuses TERM
            os.close(w)
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            _t.sleep(9999)
            os._exit(0)
        os.write(w, str(gpid).encode())
        os.close(w)
        os._exit(0)
    os.close(w)
    gpid = int(os.read(r, 32).decode())
    os.close(r)
    os.waitpid(pid, 0)           # reap the intermediate
    return gpid


def test_reap_chain_nonchild_sigterm_immune_sigkilled(_fix):
    """L4.122 criterion 2 (merge-up 23): a chain member that is NOT our child
    (an ancestor) and IGNORES SIGTERM is SIGKILLed after the wait window —
    and `_reap_chain` does NOT raise. Before the fix `wpid` was unbound on the
    first ChildProcessError and the loop raised UnboundLocalError at
    rotate.py:3040, killing the whole self-reap before the SIGKILL."""
    gpid = _spawn_nonchild_sigterm_immune()
    try:
        assert rotate._pid_alive(gpid) is True
        out = rotate._reap_chain([gpid], wait_secs=0.5, kill_survivors=True)
        # survive the wait with TERM ignored -> SIGKILLed; PID 1 reaps it.
        assert out["chain"][0]["gone_after"] is True
        assert rotate._pid_alive(gpid) is False
    finally:
        # a straggler zombie (init slow to reap) is impossible to waitpid
        # (not our child) but harmless; SIGKILL again only if somehow alive.
        if rotate._pid_alive(gpid):
            try:
                os.kill(gpid, signal.SIGKILL)
            except OSError:
                pass


def test_rotate_self_own_chain_survivor_still_succeeds(_fix, tmp_path,
                                                       monkeypatch):
    """Full cmd_rotate_self with an own-chain member that IGNORES SIGTERM
    (the criterion-2 ancestor shape): the SIGKILL-after-wait happens, the s12
    record is written, the window kill runs, and the signal shield is
    RESTORED — the self-reap never raises UnboundLocalError (pre-fix) and the
    rotation still reaches success."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("@5 adv-alive.gen1\nadv-alive\n", encoding="utf-8")
    monkeypatch.setenv("TMUX_PANE", "")
    gpid = _spawn_nonchild_sigterm_immune()

    def fake_spawn(**kw):        # successor appears under the plain name
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
        belam_prefix=None, own_chain=[gpid], registry_dir=None,
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
    reap = rec["s12_self_reap"]
    assert reap["order"] == "deepest-first"
    # the TERM-immune grandchild survived the wait and was SIGKILLed.
    assert reap["chain"][0]["gone_after"] is True
    assert rotate._pid_alive(gpid) is False
    # the shield was restored (pytest runtime is shared).
    for s in (signal.SIGHUP, signal.SIGTERM, signal.SIGPIPE):
        assert signal.getsignal(s) is old_handlers[s]


def test_rotate_self_s12_skip_names_missing_connection(_fix, tmp_path,
                                                       monkeypatch):
    """L4.122 criterion 3 (merge-up 23): when the pane pid IS present but the
    own pid cannot be climbed to it, the s12 skipped reason NAMES the missing
    input (own pid + pane pid) — not a bare 'no chain' — and the rotation
    still succeeds without TERMing anything."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("@5 adv-alive.gen1\nadv-alive\n", encoding="utf-8")
    monkeypatch.setenv("TMUX_PANE", "%5")
    # pane pid 42 exists, but rotate.py's own pid is NOT under it -> no chain.
    _ps_table(monkeypatch, [(42, 1), (55, 42)])
    monkeypatch.setattr(rotate, "_pane_pid", lambda tmux_pane: 42)

    def fake_spawn(**kw):            # successor under the plain name
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
    skipped = rec["s12_self_reap"].get("skipped", "")
    assert "SKIPPED" in skipped
    assert "own pid" in skipped and "pane pid 42" in skipped


# ── SEVENTH dispatch F2 / F3 — plain-seat planned-then-observations + dry-run ──


def test_plain_seat_own_chain_reap_planned_then_observations(_fix, tmp_path,
                                                             monkeypatch):
    """F2 — a plain-seat rotation proves (a) the OLD behaviour is unchanged
    (the own-chain reap + own-window kill still run on a plain-named seat)
    and (b) the PLANNED s12 evidence is written BEFORE the first TERM, then
    overwritten by the real observations (e): the record ends carrying a real
    chain's gone_after, rc==0, and the own window line is dropped."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("@5 adv-alive.gen1\nadv-alive\n", encoding="utf-8")
    monkeypatch.setenv("TMUX_PANE", "")
    p1 = subprocess.Popen(["sleep", "2000"])
    try:
        def fake_spawn(**kw):            # successor under the plain name
            with open(win, "a", encoding="utf-8") as fh:
                fh.write("adv-alive\n")
            return 0, "echo hi"

        monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
        monkeypatch.setattr(rotate, "_read_ack",
                            lambda *a, **k: {"seat": "adv-alive",
                                             "gen_after": 1,
                                             "answer": "continue"})
        old_handlers = {s: signal.getsignal(s)
                        for s in (signal.SIGHUP, signal.SIGTERM,
                                  signal.SIGPIPE)}
        args = SimpleNamespace(
            name="adv-alive", force=False, timeout=5, debug_file=None,
            model=None, effort=None, settings=None, prompt_file=None,
            tmux_session="t", window_path=str(win), dry_run=False,
            throwaway=False, successor_argv=None, role="parent",
            session_ref=None, successor_transcript=None, own_pid=None,
            belam_prefix=None, own_chain=[p1.pid], registry_dir=None,
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
    finally:
        if rotate._pid_alive(p1.pid):
            os.kill(p1.pid, signal.SIGKILL)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    assert rec["result"] == "success"
    s12 = rec["s12_self_reap"]
    # (e) planned entry carried; observations overwrite it with the real chain
    assert s12.get("planned") is True
    assert s12["chain"][0]["gone_after"] is True
    assert p1.pid in {c["pid"] for c in s12["chain"]}
    # old plain-seat behaviour unchanged: the OWN window is killed by @id
    assert "@5 adv-alive.gen1" not in win.read_text(encoding="utf-8")


def test_plain_seat_dry_run_resolves_own_id_touches_nothing(_fix, tmp_path,
                                                            monkeypatch,
                                                            capsys):
    """g15-11 plain-seat half of the dry-run: on a PLAIN seat the dry-run must
    resolve the own-window @id it WOULD reap from the CURRENT `<seat>` window
    (a tmux rename preserves the @id; the rename target `<seat>.genN` does not
    exist yet at dry-run time), print the @id + the named skip, and touch
    NOTHING. Regression for the defect: the dry-run derived the @id from
    pred_name (.genN) which never resolves -> @id always None."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    # the CURRENT seat window carries the @id (rename-to-.genN preserves it);
    # the .genN rename target is NOT yet present (live step (2) creates it).
    win.write_text("@9 adv-alive\n", encoding="utf-8")
    before = win.read_text()
    args = SimpleNamespace(
        name="adv-alive", force=False, timeout=5, debug_file=None,
        model=None, effort=None, settings=None, prompt_file=None,
        tmux_session="t", window_path=str(win), dry_run=True,
        throwaway=False, successor_argv=None, role="parent",
        session_ref=None, successor_transcript=None, own_pid=None,
        belam_prefix=None, own_chain=None, registry_dir=None,
        registry_poll=None, view_path=None, verification_argv=None,
        grid_commit_legal=True, grid_commit_branch=None, comms_root=None,
        trigger="rotate-self", in_flight=None)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "adv-alive.gen1" in out      # the rename target it WOULD kill
    assert "@9" in out                  # the OWN @id resolved from <seat>
    assert "rename preserves the @id" in out
    assert "SKIPPED: no pane pid" in out  # named skip when chain underivable
    assert win.read_text() == before       # touched nothing (no rename)
    rot = tmp_path / "sessions" / "rotations"
    assert not rot.exists() or not list(rot.glob("adv-alive.*.json"))


def test_chain_seat_dry_run_prints_fifo_plan_touches_nothing(_fix, tmp_path,
                                                             monkeypatch,
                                                             capsys):
    """F3 — --dry-run on the prime-shaped fixture prints the successor numeral
    name, the s12 GATING and the Belam FIFO plan (ps -e) and touches NOTHING:
    no window-file write, no reap, no rotation record."""
    _write_seats_sheet(tmp_path,
                       [{"name": "belam", "role": "prime_director",
                         "model": "x", "effort": "max", "settings": ""}])
    # the _fix fixture's rotations.md names only the parent template; give
    # the chain-seat dry-run its prime_director template so it resolves.
    g = tmp_path / "nodes" / ".geometry"
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  prime_director:\n    brief_file: "
        "extensions/agi/briefs/prime-director-successor.md\n"
        "    steps: [handoff, spawn]\n    telemetry: [seed, model, ack]\n"
        "---\n\nbody\n", encoding="utf-8")
    win = tmp_path / "windows.txt"
    win.write_text("@10 belam-S1-L4-I\n@11 belam-S1-L4-II\n"
                   "@12 belam-S1-L4-III\n@13 belam-S1-L4-IV\n"
                   "@14 belam-S1-L4-V\n@15 belam-S1-L4-VI\n",
                   encoding="utf-8")
    before = win.read_text()
    args = SimpleNamespace(
        name="belam", force=False, timeout=5, debug_file=None,
        model=None, effort=None, settings=None, prompt_file=None,
        tmux_session="t", window_path=str(win), dry_run=True,
        throwaway=False, successor_argv=None, role="prime_director",
        session_ref=None, successor_transcript=None, own_pid=None,
        belam_prefix=None, own_chain=None, registry_dir=None,
        registry_poll=None, view_path=None, verification_argv=None,
        grid_commit_legal=True, grid_commit_branch=None, comms_root=None,
        trigger="rotate-self", in_flight=None)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "belam-S1-L4-VII" in out        # the successor numeral name derived
    assert "GATES this off" in out         # s12 gating for a numeral-chain seat
    assert "ps -e" in out                  # (w) the dry-run says ps -e
    # g15-11: the dry-run NAMES the OLDEST it would reap, its @id, and the
    # named skip when the chain cannot be derived (no tmux pane pid here).
    assert "belam-S1-L4-I" in out          # the OLDEST predecessor to reap
    assert "@10" in out                    # its window @id
    assert "SKIPPED: no pane pid" in out   # named skip when chain underivable
    assert win.read_text() == before       # touched nothing
    rot = tmp_path / "sessions" / "rotations"
    assert not rot.exists() or not list(rot.glob("belam.*.json"))
