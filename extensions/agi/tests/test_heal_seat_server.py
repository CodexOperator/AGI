"""goal:g7.31.1.6 -- heal judges, and relaunches, a seat on the seat's OWN tmux server, and reads its owner's registry.

L528 (goal:g7.31.1.5) gave stand-up and heal's empty-pid path the seat's server through its latest launch record.
heal's watch pass still read the CALLER's default server for every pid row, launched a respawn there, and read the
caller's session registry. The build:

  each pid row: the latest launch record joins -> its windows read on ITS server (hit); no join -> judged on the
  caller's default ONLY when this uid owns the row (stat), else skipped, named, counted;
  the respawn launches with `tmux -S <the seat's socket>` (launch_in_window / ensure_tmux_session take it);
  a server GONE (socket absent) is recreated on that socket when this uid owns its dir; RESTARTED (live, another
  identity) is launched on as it stands; a server this uid cannot read is skipped, naming 'run it as <owner>';
  the registry is the socket owner's (another uid's -> its home's .claude/sessions); unread stays UNREAD.

Rows run REAL tmux servers on scratch sockets (the `scratch` fixture of test_stand_up_unread_windows: the conftest
tmux guard passes only calls whose -S path, or default socket, lies in the scratch dir). Only the launcher is fake,
except where a row says the launch is real. Each guard has a source-text mutant that reads RED.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

import heal  # noqa: E402
import mem_cap  # noqa: E402
import rotate  # noqa: E402
from test_stand_up import DEAD_PID, calls, graph  # noqa: E402,F401
from test_stand_up_unread_windows import (  # noqa: E402,F401
    _REAL_RUN, BIN, _default, _identity, _kill_and_wait, _mut, _record, _row, _server, scratch)

pytestmark = pytest.mark.skipif(shutil.which("tmux") is None, reason="tmux is not installed")


@pytest.fixture
def log(monkeypatch):
    lines: list = []
    monkeypatch.setattr(heal, "_watch_log", lines.append)
    return lines


def _launcher(seen: list, real: bool = False):
    """Records each launch and its socket kwarg; `real` opens the window on that socket for real (sleep 300)."""
    def launch(root, name, shell_cmd, window_path=None, cwd=None, **kw):
        seen.append({"name": name, **kw})
        if not real:
            return 424243, "@556"
        rc, wid = rotate.launch_in_window("agi-t", name, "sleep 300", cwd=cwd, root=root,
                                          inline_max=0, timeout_ok=False, socket=kw.get("socket"))
        return (424243 if rc == 0 else 0), wid
    return launch


def _scan(h, graph, seen, *, real=False, pid_alive=lambda p: False, registry_dir=None):
    return h._watch_seats(graph, pid_alive=pid_alive, launcher=_launcher(seen, real), registry_dir=registry_dir)


def _with(m):
    """Run `m` (a mutant heal) as THE heal: rotate and stand_up resolve `heal` through sys.modules."""
    class _Ctx:
        def __enter__(self):
            self.keep = sys.modules["heal"]
            sys.modules["heal"] = m
            return m

        def __exit__(self, *a):
            sys.modules["heal"] = self.keep
    return _Ctx()


def _windows_on(sock) -> list[str]:
    r = _REAL_RUN(["tmux", "-S", str(sock), "list-windows", "-a", "-F", "#{window_name}"],
                  capture_output=True, text=True, timeout=10)
    return r.stdout.split() if r.returncode == 0 else []


@pytest.fixture(autouse=True)
def _no_scope(monkeypatch):
    """A real launch in a row never goes through systemd-run (the guard refuses it): the bare tmux argv."""
    monkeypatch.setattr(mem_cap, "scope_argv", lambda argv, *a, **k: list(argv))


# --- target 1: judged on the seat's own server --------------------------------------------------------------------

def _two_servers(graph, scratch):
    """The seat's server holds @1 (its window); the caller's default is LIVE too and holds only @0."""
    seat = _server(scratch / "seat", windows=2)
    _server(_default(scratch), windows=1)
    _row(graph, window=seat[-1], pid=DEAD_PID)
    _record(graph, window_id=seat[-1], **_identity(scratch / "seat"))
    return seat[-1]


def test_the_seats_window_open_on_its_own_server_is_not_respawned(graph, calls, scratch, log):
    _two_servers(graph, scratch)
    seen: list = []
    _scan(heal, graph, seen)
    assert seen == [], log


def test_mutant_the_pass_list_from_the_callers_default_respawns_RED(graph, calls, scratch, tmp_path, log):
    m = _mut(tmp_path, "heal_mut_passlist", BIN / "heal.py",
             '        r_windows = windows if rs.get("windows") is None else rs["windows"]\n',
             '        r_windows = windows\n')
    _two_servers(graph, scratch)
    seen: list = []
    with _with(m):
        _scan(m, graph, seen)
    assert len(seen) == 1


def test_a_window_closed_on_the_seats_server_respawns_there(graph, calls, scratch, log):
    sock = scratch / "seat"
    _server(sock)
    _row(graph, window="@7", pid=DEAD_PID)
    _record(graph, window_id="@7", **_identity(sock))
    seen: list = []
    _scan(heal, graph, seen)
    assert [s.get("socket") for s in seen] == [str(sock)], log


def test_mutant_the_launch_takes_no_socket_RED(graph, calls, scratch, tmp_path, log):
    m = _mut(tmp_path, "heal_mut_nosock", BIN / "heal.py",
             '    _sk = {"socket": socket} if socket else {}\n', '    _sk = {}\n')
    sock = scratch / "seat"
    _server(sock)
    _row(graph, window="@7", pid=DEAD_PID)
    _record(graph, window_id="@7", **_identity(sock))
    seen: list = []
    with _with(m):
        _scan(m, graph, seen)
    assert [s.get("socket") for s in seen] == [None]


def test_a_launcher_that_takes_no_socket_is_refused_never_retried_on_the_default(graph, calls, scratch, log):
    sock = scratch / "seat"
    _server(sock)
    _row(graph, window="@7", pid=DEAD_PID)
    _record(graph, window_id="@7", **_identity(sock))
    seen: list = []

    def old(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append(name)
        return 1, "@9"
    heal._watch_seats(graph, pid_alive=lambda p: False, launcher=old)
    assert seen == [] and any("takes no socket" in ln for ln in log), log


# --- the real -S launch -------------------------------------------------------------------------------------------

def test_launch_in_window_opens_on_the_named_socket_only(graph, scratch):
    sock = scratch / "seat"
    rc, wid = rotate.launch_in_window("agi-t", "w-x", "sleep 300", cwd=str(scratch), root=graph,
                                      inline_max=0, timeout_ok=False, socket=str(sock))
    assert rc == 0 and wid.startswith("@") and "w-x" in _windows_on(sock)
    assert _windows_on(_default(scratch)) == []                       # the default server never started


def test_mutant_new_window_without_s_RED(graph, scratch, tmp_path):
    m = _mut(tmp_path, "rotate_mut_nos", BIN / "rotate.py",
             '            ["tmux"] + (["-S", socket] if socket else [])\n            + ["new-window",',
             '            ["tmux"]\n            + ["new-window",')
    sock = scratch / "seat"
    rc, _wid = m.launch_in_window("agi-t", "w-x", "sleep 300", cwd=str(scratch), root=graph,
                                  inline_max=0, timeout_ok=False, socket=str(sock))
    assert "w-x" not in _windows_on(sock)


# --- target 3: unreachable, gone, restarted ------------------------------------------------------------------------

@pytest.fixture
def locked(scratch):
    d = scratch / "locked"
    sock = d / "s"
    _server(sock)
    ident = _identity(sock)
    d.chmod(0)
    yield sock, ident
    d.chmod(0o700)


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads a mode-000 dir")
def test_an_unreachable_seat_server_is_skipped_naming_its_owner(graph, calls, locked, log):
    sock, ident = locked
    _row(graph, window="@7", pid=DEAD_PID)
    _record(graph, window_id="@7", **ident)
    seen: list = []
    _scan(heal, graph, seen)
    assert seen == [] and any("skipped" in ln and "run it as" in ln for ln in log), log
    assert any("+ 1 skipped" in ln for ln in log), log


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads a mode-000 dir")
def test_mutant_a_failed_read_launches_RED(graph, calls, locked, tmp_path, log):
    m = _mut(tmp_path, "heal_mut_unreach", BIN / "heal.py",
             '        if sw.reason != "no-server":\n', '        if False:\n')
    sock, ident = locked
    _row(graph, window="@7", pid=DEAD_PID)
    _record(graph, window_id="@7", **ident)
    seen: list = []
    with _with(m):
        _scan(m, graph, seen)
    assert len(seen) == 1


def _gone(graph, scratch):
    """sp's server-gone row: the record names a server whose socket FILE is gone (a reset cleared it), dir present."""
    sock = scratch / "seat"
    _server(sock)
    ident = _identity(sock)
    _kill_and_wait(sock)
    if sock.exists():
        sock.unlink()
    _row(graph, window="@0", pid=DEAD_PID)
    _record(graph, window_id="@0", **ident)
    return sock


def test_a_gone_server_is_recreated_on_its_socket_and_the_seat_opens_there(graph, calls, scratch, log):
    sock = _gone(graph, scratch)
    seen: list = []
    _scan(heal, graph, seen, real=True)
    assert [s.get("socket") for s in seen] == [str(sock)], log
    assert "seat-a" in _windows_on(sock) and _windows_on(_default(scratch)) == []
    assert any("server gone: recreating on" in ln for ln in log), log


def test_mutant_a_gone_server_fails_closed_RED(graph, calls, scratch, tmp_path, log):
    m = _mut(tmp_path, "heal_mut_goneclosed", BIN / "heal.py", "            if not mine:\n", "            if True:\n")
    _gone(graph, scratch)
    seen: list = []
    with _with(m):
        _scan(m, graph, seen, real=True)
    assert seen == []                                    # no seat comes back after a reset


def test_mutant_recreated_on_the_callers_default_RED(graph, calls, scratch, tmp_path, log):
    m = _mut(tmp_path, "heal_mut_godefault", BIN / "heal.py",
             '            "socket": "" if _is_default_socket(sock) else sock, "why": how}\n',
             '            "socket": "", "why": how}\n')
    sock = _gone(graph, scratch)
    seen: list = []
    with _with(m):
        _scan(m, graph, seen, real=True)
    assert "seat-a" not in _windows_on(sock) and "seat-a" in _windows_on(_default(scratch))


def _restarted(graph, scratch):
    """sp's restarted row (SM's build nit 01:24:24Z): server 1 held @0 and the record names it; killed; server 2 on
    the SAME path holds another window at @0."""
    sock = scratch / "seat"
    (w,) = _server(sock)
    ident = _identity(sock)
    _kill_and_wait(sock)
    assert _server(sock) == [w] and _identity(sock) != ident
    _row(graph, window=w, pid=DEAD_PID)
    _record(graph, window_id=w, **ident)
    return sock


def test_a_restarted_server_is_launched_on_as_it_stands_named(graph, calls, scratch, log):
    sock = _restarted(graph, scratch)
    seen: list = []
    _scan(heal, graph, seen, real=True)
    assert [s.get("socket") for s in seen] == [str(sock)] and "seat-a" in _windows_on(sock), log
    assert any("server restarted" in ln and "launched on that live server" in ln for ln in log), log


def test_mutant_the_restart_read_as_gone_RED(graph, calls, scratch, tmp_path, log):
    m = _mut(tmp_path, "heal_mut_restart", BIN / "heal.py",
             '        if _tmux_socket_state(sock) == "live":\n', '        if False:\n')
    _restarted(graph, scratch)
    seen: list = []
    with _with(m):
        _scan(m, graph, seen, real=True)
    assert not any("launched on that live server" in ln for ln in log)


# --- target 2: a MISS, judged only as the row's own uid --------------------------------------------------------------

def test_a_miss_owned_by_this_uid_is_judged_as_today_CONTROL(graph, calls, scratch, log):
    _row(graph, window="@7", pid=DEAD_PID)                 # no launch record: a MISS
    seen: list = []
    _scan(heal, graph, seen)
    assert len(seen) == 1 and "socket" not in seen[0], log
    assert any(ln.startswith("watch: seat seat-a: MISS (") and ln.endswith("judged as the seat's own uid")
               for ln in log), log


def test_a_miss_owned_by_another_uid_is_skipped_named_counted(graph, calls, scratch, log, monkeypatch):
    _row(graph, window="@7", pid=DEAD_PID)
    me = os.getuid()
    monkeypatch.setattr(heal, "_path_owner", lambda p: (me + 1, "someone-else"))
    seen: list = []
    _scan(heal, graph, seen)
    assert seen == [], log
    assert any("skipped" in ln and "its owner is someone-else, not this uid" in ln for ln in log), log
    assert any("0 MISS judged as the seat's own uid + 1 skipped" in ln for ln in log), log


def test_mutant_the_uid_test_dropped_RED(graph, calls, scratch, log, monkeypatch, tmp_path):
    m = _mut(tmp_path, "heal_mut_uid", BIN / "heal.py",
             "        if uid is not None and uid == os.getuid():\n            return {\"kind\": \"miss-own\"",
             "        if True:\n            return {\"kind\": \"miss-own\"")
    _row(graph, window="@7", pid=DEAD_PID)
    me = os.getuid()
    monkeypatch.setattr(m, "_path_owner", lambda p: (me + 1, "someone-else"))
    seen: list = []
    with _with(m):
        _scan(m, graph, seen)
    assert len(seen) == 1


# --- target 4: the owner's registry ---------------------------------------------------------------------------------

def _owned_by_other(h, monkeypatch, home: Path, sock: Path):
    """The seat's socket dir reads as another uid's whose home is `home` (pwd patched); every other path as ours."""
    me = os.getuid()
    real = h._path_owner
    monkeypatch.setattr(h, "_path_owner",
                        lambda p: (me + 1, "other") if str(p) == str(sock.parent) else real(p))
    import pwd
    real_pw = pwd.getpwuid
    monkeypatch.setattr(pwd, "getpwuid",
                        lambda uid: NS(pw_dir=str(home), pw_name="other") if uid == me + 1 else real_pw(uid))


def _registry_row(graph, scratch, home: Path):
    """The row's window @7 is CLOSED on the seat's server; its OWN session is live at @0 in the owner's registry."""
    sock = scratch / "seat"
    _server(sock)                                         # holds @0
    _row(graph, window="@7", pid=DEAD_PID, session_id="sid-live")
    _record(graph, window_id="@7", **_identity(sock))
    reg = home / ".claude" / "sessions"
    reg.mkdir(parents=True)
    (reg / f"{os.getpid()}.json").write_text(json.dumps(
        {"sessionId": "sid-live", "session_id": "sid-live", "tmux": "agi-rc:@0.%0"}), encoding="utf-8")
    return sock, reg


def test_the_owners_registry_holds_a_live_session_so_not_respawned(graph, calls, scratch, log, monkeypatch, tmp_path):
    sock, _reg = _registry_row(graph, scratch, tmp_path / "home-other")
    _owned_by_other(heal, monkeypatch, tmp_path / "home-other", sock)
    seen: list = []
    _scan(heal, graph, seen, pid_alive=lambda p: p == os.getpid())
    assert seen == [], log


def test_mutant_the_callers_registry_reads_it_dead_RED(graph, calls, scratch, log, monkeypatch, tmp_path):
    m = _mut(tmp_path, "heal_mut_reg", BIN / "heal.py",
             "    if uid == os.getuid():\n        return registry_dir\n",
             "    if True:\n        return registry_dir\n")
    sock, _reg = _registry_row(graph, scratch, tmp_path / "home-other")
    _owned_by_other(m, monkeypatch, tmp_path / "home-other", sock)
    seen: list = []
    with _with(m):
        _scan(m, graph, seen, pid_alive=lambda p: p == os.getpid())
    assert len(seen) == 1


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads a mode-000 dir")
def test_an_unread_owner_registry_holds_the_respawn_named(graph, calls, scratch, log, monkeypatch, tmp_path):
    sock, reg = _registry_row(graph, scratch, tmp_path / "home-other")
    _owned_by_other(heal, monkeypatch, tmp_path / "home-other", sock)
    reg.chmod(0)
    try:
        seen: list = []
        _scan(heal, graph, seen, pid_alive=lambda p: p == os.getpid())
    finally:
        reg.chmod(0o700)
    assert seen == [] and any("registry unreadable" in ln for ln in log), log


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads a mode-000 dir")
def test_mutant_an_unlistable_registry_reads_no_sessions_RED(graph, calls, scratch, log, monkeypatch, tmp_path):
    m = _mut(tmp_path, "heal_mut_reglist", BIN / "heal.py", "        os.listdir(reg)\n", "        pass\n")
    sock, reg = _registry_row(graph, scratch, tmp_path / "home-other")
    _owned_by_other(m, monkeypatch, tmp_path / "home-other", sock)
    reg.chmod(0)
    try:
        seen: list = []
        with _with(m):
            _scan(m, graph, seen, pid_alive=lambda p: p == os.getpid())
    finally:
        reg.chmod(0o700)
    assert len(seen) == 1


# --- CONTROL: the seat's own uid, its server the caller's default ---------------------------------------------------

@pytest.mark.parametrize("open_", [True, False])
def test_the_seats_server_is_the_callers_default_verdicts_as_before_CONTROL(graph, calls, scratch, log, open_):
    d = _default(scratch)
    ids = _server(d)
    w = ids[0] if open_ else "@7"
    _row(graph, window=w, pid=DEAD_PID)
    _record(graph, window_id=w, **_identity(d))
    seen: list = []
    _scan(heal, graph, seen)
    assert len(seen) == (0 if open_ else 1), log
    assert all("socket" not in s for s in seen)             # the default server: the launch as before


# --- AMEND (SM 03:35:57Z on alive 03:35:32Z NIT; and the reset that removes the socket's DIR) ---------------------

def _hit_closed(graph, scratch):
    sock = scratch / "seat"
    _server(sock)
    _row(graph, window="@7", pid=DEAD_PID)
    _record(graph, window_id="@7", **_identity(sock))
    return sock


def test_an_unread_registry_owner_holds_the_respawn_never_the_callers(graph, calls, scratch, log, monkeypatch):
    """alive's row: the socket dir's owner cannot be read -> UNREAD (held, named), never the caller's sessions."""
    sock = _hit_closed(graph, scratch)
    assert heal._owner_registry(str(sock), "/CALLERS/registry") == "/CALLERS/registry"      # ours: as before
    monkeypatch.setattr(heal, "_path_owner", lambda p: (None, ""))
    assert heal._owner_registry(str(sock), "/CALLERS/registry") is heal.REG_OWNER_UNREAD
    seen: list = []
    _scan(heal, graph, seen)
    assert seen == [] and any("is unread: registry unreadable" in ln for ln in log), log
    assert any("respawn held: registry unreadable" in ln for ln in log), log


def test_mutant_an_unread_owner_reads_the_callers_registry_RED(graph, calls, scratch, log, monkeypatch, tmp_path):
    m = _mut(tmp_path, "heal_mut_regnone", BIN / "heal.py",
             "    if uid is None:\n        try:\n            os.lstat(d)\n",
             "    if uid is None:\n        return registry_dir\n        try:\n            os.lstat(d)\n")
    _hit_closed(graph, scratch)
    monkeypatch.setattr(m, "_path_owner", lambda p: (None, ""))
    seen: list = []
    with _with(m):
        _scan(m, graph, seen)
    assert len(seen) == 1


def _gone_dir(graph, scratch):
    """A reset cleared /tmp: the record's socket AND its tmux-<uid> dir are gone (measured 03:36Z: tmux -S never
    creates the parent: 'error creating ... (No such file or directory)', rc 0)."""
    d = scratch / f"tmux-{os.getuid()}"                    # this uid's OWN tmux dir (TMUX_TMPDIR = scratch), by full path
    sock = d / "seat"
    _server(sock)
    ident = _identity(sock)
    _kill_and_wait(sock)
    shutil.rmtree(d)
    _row(graph, window="@0", pid=DEAD_PID)
    _record(graph, window_id="@0", **ident)
    return sock


def test_a_gone_server_whose_dir_is_gone_is_recreated_dir_and_all(graph, calls, scratch, log):
    """MEASURED in this row: tmux makes its OWN ${TMUX_TMPDIR}/tmux-<uid> dir itself (and heal's own default read
    already has by the registry read), so rotate's makedirs and _owner_registry's absent-own branch are guards no
    live path reaches today: no mutant of either can read RED here, and none is claimed."""
    sock = _gone_dir(graph, scratch)
    seen: list = []
    _scan(heal, graph, seen, real=True)
    assert [s.get("socket") for s in seen] == [str(sock)] and "seat-a" in _windows_on(sock), log
    assert oct(sock.parent.stat().st_mode & 0o777) == "0o700"


def test_an_absent_dir_named_tmux_uid_elsewhere_is_not_ours_skipped_named(graph, calls, scratch, log):
    """(B), aio + sp: the own dir is read by FULL path, never the basename: tmux-<uid> under another root is skipped."""
    d = scratch / "r" / f"tmux-{os.getuid()}"
    sock = d / "seat"
    _server(sock)
    ident = _identity(sock)
    _kill_and_wait(sock)
    shutil.rmtree(d)
    _row(graph, window="@0", pid=DEAD_PID)
    _record(graph, window_id="@0", **ident)
    seen: list = []
    _scan(heal, graph, seen, real=True)
    assert seen == [] and any("server gone on" in ln and "not this uid's" in ln for ln in log), log


def test_mutant_the_own_dir_read_by_basename_RED(graph, calls, scratch, log, tmp_path):
    m = _mut(tmp_path, "heal_mut_basename", BIN / "heal.py",
             "                    else os.path.abspath(d) == os.path.abspath(_own_tmux_dir()))\n",
             '                    else os.path.basename(d) == f"tmux-{os.getuid()}")\n')
    d = scratch / "r" / f"tmux-{os.getuid()}"
    sock = d / "seat"
    _server(sock)
    ident = _identity(sock)
    _kill_and_wait(sock)
    shutil.rmtree(d)
    _row(graph, window="@0", pid=DEAD_PID)
    _record(graph, window_id="@0", **ident)
    seen: list = []
    with _with(m):
        _scan(m, graph, seen)
    assert not any("not this uid's" in ln for ln in log)      # the lookalike dir read as ours


@pytest.fixture
def uncreatable(graph, scratch):
    """A gone server whose dir is ours but not writable (0500): `tmux -S` new-session makes nothing and exits 0."""
    d = scratch / "ro"
    sock = d / "seat"
    _server(sock)
    ident = _identity(sock)
    _kill_and_wait(sock)
    if sock.exists():
        sock.unlink()
    d.chmod(0o500)
    _row(graph, window="@0", pid=DEAD_PID)
    _record(graph, window_id="@0", **ident)
    yield sock
    d.chmod(0o700)


@pytest.mark.skipif(os.geteuid() == 0, reason="root writes a 0500 dir")
def test_a_recreate_that_made_no_server_is_named_failed(graph, calls, uncreatable, log):
    seen: list = []
    _scan(heal, graph, seen, real=True)
    assert len(seen) == 1 and _windows_on(uncreatable) == [], log
    assert any(f"server on {uncreatable} NOT recreated" in ln for ln in log), log
    assert not any("recreated on" in ln for ln in log), log


@pytest.mark.skipif(os.geteuid() == 0, reason="root writes a 0500 dir")
def test_mutant_a_failed_recreate_not_named_RED(graph, calls, uncreatable, log, tmp_path):
    m = _mut(tmp_path, "heal_mut_unnamed", BIN / "heal.py",
             "        if socket and _server_identity(socket) is None:\n",
             "        if False:\n")
    seen: list = []
    with _with(m):
        _scan(m, graph, seen, real=True)
    assert not any("NOT recreated" in ln for ln in log)
