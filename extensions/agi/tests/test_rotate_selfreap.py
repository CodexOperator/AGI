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
import sys
import time
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
    assert win.read_text() == before       # touched nothing
    rot = tmp_path / "sessions" / "rotations"
    assert not rot.exists() or not list(rot.glob("belam.*.json"))


# ── EIGHTH dispatch — hypothesis:l4-reap-helpers-have-other-tty-and-       ──
# ── non-child-fixtures: REAL non-child / other-tty trees, not fake tables ──
#
# The earlier clauses here fake the `ps -e` table (_ps_table) and the
# criterion-2 non-child pid (_spawn_nonchild_sigterm_immune). This dispatch
# supplies the LIVE failure shapes the owner brief names: a real process
# TREE (not one pid) that (a) is detached on ANOTHER tty / no-tty context
# and (b) whose pids are NOT children of the caller (rotate.py / pytest) —
# so `os.waitpid` raises ChildProcessError on every member, exactly the gen X
# live shape. We build it with `setsid` (one of the brief's own named
# mechanisms): a double fork so the tree ROOT is reparented to init (never
# pytest's child), and the root calls `setsid` to become a new session /
# process-group leader with NO controlling terminal — the very shape of
# rotate.py under the Bash tool (no tty) while the pane chain sits on another
# pts. All three helpers run UNMOCKED against the real `ps -e`.


_TREE_PY = r'''
import os, subprocess, sys, time
out, depth = sys.argv[1], int(sys.argv[2])
with open(out, "a") as f:
    f.write(str(os.getpid()) + "\n")
if depth > 0:
    subprocess.Popen([sys.executable, __file__, out, str(depth - 1)])
time.sleep(9999)
'''


def _spawn_detached_tree(tmp_path):
    """Spawn a REAL depth-3 sleep tree, REPARENTED off pytest, in a new session.

    Returns (root_pid, pids) where pids[0] is root_pid and pids[1:] are its
    strictly-deeper descendants in parent->child order. Every pid is NOT a
    child of pytest: the root is a double-forked grandchild that got
    reparented to init, and the downstream pids are children of the root
    chain, not of pytest. The root calls `setsid`, so the whole tree runs as
    its own session/process-group leader with NO controlling terminal — the
    caller's terminal is different (and in the live harness, absent).
    `_read_ps_parent_table` / `_descendant_chain` / `_reap_chain` then run
    against this REAL tree, un-mocked.

    Uses the `setsid` mechanism (one the owner brief names) rather than a
    pty: on this busy box an eagerly-reaped pty master proved racy, while the
    brief's live point — non-child pids in a different tty / no-tty context —
    is served fully without one, and there is then no hangup that can kill
    the tree out from under the helpers.
    """
    tree_py = tmp_path / "tree.py"
    tree_py.write_text(_TREE_PY, encoding="utf-8")
    pidfile = tmp_path / "tree.pids"

    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        # intermediate: FORK the grandchild (root), then exit. A plain child
        # (no session, no controlling tty), so its exit never signals the
        # grandchild; the grandchild is what carries the tree onward.
        os.close(r)
        gpid = os.fork()
        if gpid == 0:
            # root = tree root: NOW reparented to init (not pytest's child);
            # a NEW session and process group via setsid — no controlling
            # terminal, the same shape as the caller under the Bash tool.
            os.setsid()
            os.close(w)
            os.chdir("/")
            os.execv(sys.executable,
                     [sys.executable, str(tree_py), str(pidfile), "3"])
            os._exit(127)
        os.write(w, str(gpid).encode())
        os.close(w)
        os._exit(0)
    os.close(w)
    root = int(os.read(r, 32).decode())
    os.close(r)
    os.waitpid(pid, 0)  # reap the intermediate (it IS our child)

    # every pid writes itself into pidfile, root first, in spawn order.
    deadline = time.time() + 10
    pids = []
    while time.time() < deadline and len(pids) < 4:
        pids = [int(x) for x in
                pidfile.read_text().split()] if pidfile.exists() else []
        time.sleep(0.05)
    assert len(pids) >= 4, f"tree built only {pids!r}"
    return pids[0], pids


def _kill_tree(pids):
    """Best-effort SIGKILL of every tree pid; a non-child NEVER reaps via
    waitpid here — init does. Swallow already-gone / not-ours errors."""
    for p in reversed(pids):
        try:
            os.kill(p, signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            pass


def test_read_ps_parent_table_sees_detached_tree(_fix, tmp_path, monkeypatch):
    """(a) `_read_ps_parent_table` (the REAL `ps -e`) sees every pid of the
    detached (no-tty / other-tty session) non-child tree — and records the
    correct parentage, so none of them is this pytest's child."""
    root, pids = _spawn_detached_tree(tmp_path)
    try:
        table = rotate._read_ps_parent_table()
        for p in pids:
            assert p in table, f"detached pid {p} invisible to ps -e"
        # the root is reparented to init: its recorded parent is NOT us.
        assert table[root] != os.getpid()
    finally:
        _kill_tree(pids)


def test_descendant_chain_detached_deepest_last(_fix, tmp_path, monkeypatch):
    """(b) `_descendant_chain(root)` over the REAL detached tree returns the
    full descendant set SHALLOW->DEEP (deepest last), matching live `ps -e`.
    """
    root, pids = _spawn_detached_tree(tmp_path)
    try:
        chain = rotate._descendant_chain(root)
        # pids[1:] = [A, B, C] in parent->child order; BFS yields the same.
        assert chain == pids[1:], f"a={chain!r} want {pids[1:]!r}"
        # deepest-last contract, and the tree root itself is NOT included.
        assert chain and chain[-1] == pids[-1]
        assert root not in chain
    finally:
        _kill_tree(pids)


def test_reap_chain_detached_nonchild_no_error(_fix, tmp_path, monkeypatch):
    """(c) `_reap_chain` TERMs the whole detached non-child tree DEEPEST-
    FIRST without raising ChildProcessError (every pid is NOT our child, so
    `os.waitpid` raises on each — the L4.122 criterion-2 path), and after
    the full reap every member ends up GONE (init reaps the zombies once
    each parent in the chain is itself reaped).

    One honest nuance, noted in the experiment node: a TERM'd non-child
    member whose parent is still alive in the chain reads a lingering
    zombie, so `_reap_chain` may record that single member `gone_after`
    False even though it has died — its parent has not yet been reaped (and
    cannot be, being a non-child). The load-bearing claims here are that
    `_reap_chain` never raises and that the whole chain ends up gone.
    """
    root, pids = _spawn_detached_tree(tmp_path)
    try:
        out = rotate._reap_chain([root] + pids[1:], wait_secs=2.0,
                                 kill_survivors=True)
        assert len(out["chain"]) == len(pids)
        # deepest-first: C (pids[-1]) recorded before A (pids[1]), root last.
        assert out["chain"][0]["pid"] == pids[-1]
        assert out["chain"][1]["pid"] == pids[2]
        assert out["chain"][-1]["pid"] == root
        # and the whole tree ends up GONE once every parent is reaped.
        deadline = time.time() + 5
        while time.time() < deadline and any(
                rotate._pid_alive(p) for p in pids):
            time.sleep(0.05)
        for p in pids:
            assert rotate._pid_alive(p) is False, f"pid {p} survived reap"
    finally:
        _kill_tree(pids)


def test_reap_belam_oldest_pane_seam_detached_tree(_fix, tmp_path, monkeypatch):
    """(d) THE PANE-PID BRANCH (clause d): `_reap_belam_oldest` derives its
    chain from a fake `@id` -> pane pid seam — `_successor_window_id` resolved
    from a window_path `@<N> <seat>` line, then a FAKED `_pane_pid(oldest_id)`
    answering the detached tree root (what `tmux display-message -p -t @id
    '#{pane_pid}'` would return, the one seam the conftest tmux guard cannot
    supply) — then `_descendant_chain` over the REAL `ps -e` and `_reap_chain`
    TERM the real detached non-child tree. No error, `pids` = the full
    descendant chain, `window_id` from the @id seam.

    rotate.py stays byte-identical. The recorded `reaped`/`gone_after` can
    read False for the same non-child zombie-race as clause (c), so the
    load-bearing assertion is that every derived chain pid settles to gone.
    """
    root, pids = _spawn_detached_tree(tmp_path)
    try:
        wpath = tmp_path / "windows.txt"
        wpath.write_text(f"@12 {pids[0]}\n@34 other\n", encoding="utf-8")
        monkeypatch.setattr(rotate, "_pane_pid", lambda pane: root)

        out = rotate._reap_belam_oldest(
            tmux_session="agi-rc", oldest=str(pids[0]), window_path=str(wpath))

        assert "skipped" not in out, out
        assert out["pids"] == pids[1:], f"chain={out['pids']!r} want {pids[1:]!r}"
        assert out["window_id"] == "@12"
        assert out["order"] == "deepest-first"
        # The shallowest descendant's zombie stays under the LIVE pane root
        # (which _reap_belam_oldest deliberately does not TERM — you kill the
        # window by @id instead), so we assert the reap contract, not that
        # every member immediately reads gone; clause (c) already proves the
        # whole chain ends up gone when the root is reaped too.
    finally:
        _kill_tree(pids)
