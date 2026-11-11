"""goal:g7.31.1.5 -- a hand stand-up reads the seat's windows on the seat's OWN tmux server, and refuses what it can't prove.

L519 (goal:g7.31.1.4) wrote a missed grok join's pid EMPTY; `rotate.cmd_stand_up` then read the CALLER's default tmux
server, so a stand-up from another uid, or after a hiccup, launched a second harness on a live seat. The build:

  the launch record carries the server: tmux_socket + tmux_server_start + tmux_server_pid (one helper, both writers),
  and the harness pid's start time (/proc/<pid>/stat field 22);
  stand-up joins the seat's LATEST LAUNCH record (never a detected one) on window == the row's window;
  a hit reads `tmux -S <socket>` ALWAYS; another start time/pid on the socket = 'server restarted' = no-server;
  absent / stale = no-server (proceeds); live-and-failed / unstat-able = read-failed (refuses, owner named);
  a MISS: pid > 0 -> the caller's default, named; EMPTY pid -> refused, naming `--window-closed`, the way out;
  the pid read: start time == the record's = alive (another uid included); another = reused = dead, named.

Rows run REAL tmux servers on scratch sockets under /tmp (a unix socket path is capped near 108 bytes). The suite's
tmux guard (conftest `_no_real_tmux`) answers every tmux call rc 1; `scratch` lets through ONLY calls whose `-S` path,
or whose default socket ($TMUX_TMPDIR, $TMUX unset), lies in the scratch dir. Only the launcher is fake. Each guard
has a source-text mutant that reads RED.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

import heal  # noqa: E402
import rotate  # noqa: E402
from test_stand_up import _launcher, calls, graph  # noqa: E402,F401

_REAL_RUN = subprocess.run          # bound at import, before the conftest guard patches subprocess.run per test
BIN = Path(rotate.__file__).resolve().parent
pytestmark = pytest.mark.skipif(shutil.which("tmux") is None, reason="tmux is not installed")


@pytest.fixture
def scratch(monkeypatch):
    """A scratch dir for sockets; the caller's default socket points INTO it (absent until a test starts it)."""
    d = Path(tempfile.mkdtemp(prefix="g5-", dir="/tmp"))
    monkeypatch.setenv("TMUX_TMPDIR", str(d))
    for k in ("TMUX", "TMUX_PANE", heal.WINDOW_PATH_ENV):
        monkeypatch.delenv(k, raising=False)
    guarded = subprocess.run

    def run(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
            sock = cmd[cmd.index("-S") + 1] if "-S" in cmd else os.path.join(
                os.environ.get("TMUX_TMPDIR", ""), f"tmux-{os.getuid()}", "default")
            if sock.startswith(str(d) + "/") and not os.environ.get("TMUX"):
                return _REAL_RUN(cmd, *a, **k)
        return guarded(cmd, *a, **k)
    monkeypatch.setattr(subprocess, "run", run)
    yield d
    for s in d.rglob("*"):
        if s.is_socket():
            _REAL_RUN(["tmux", "-S", str(s), "kill-server"], capture_output=True, timeout=10)
    shutil.rmtree(d, ignore_errors=True)


def _server(sock: Path, windows: int = 1) -> list[str]:
    """Start a server on `sock` holding `windows` windows; their @ids."""
    sock.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    out = _REAL_RUN(["tmux", "-S", str(sock), "new-session", "-d", "-s", "s", "-P", "-F", "#{window_id}",
                     "sleep 300"], capture_output=True, text=True, timeout=10, check=True).stdout.split()
    for _ in range(windows - 1):
        out += _REAL_RUN(["tmux", "-S", str(sock), "new-window", "-t", "s:", "-P", "-F", "#{window_id}",
                          "sleep 300"], capture_output=True, text=True, timeout=10, check=True).stdout.split()
    return out


def _identity(sock: Path) -> dict:
    o = _REAL_RUN(["tmux", "-S", str(sock), "list-sessions", "-F", "#{start_time}\t#{pid}"],
                  capture_output=True, text=True, timeout=10, check=True).stdout.split()
    return {"tmux_socket": str(sock), "tmux_server_start": o[0], "tmux_server_pid": o[1]}


def _default(d: Path) -> Path:
    return d / f"tmux-{os.getuid()}" / "default"


def _row(graph, **cells):
    p = graph / "nodes" / ".geometry" / "seats.md"
    row = {"name": "seat-a", "role": "director", "pid": "", "window": "@50", "generation": 2, "model": "m-1"}
    row.update(cells)
    p.write_text("---\nid: config:seats\nseats:\n  - " + json.dumps(row) + "\n---\n", encoding="utf-8")


def _record(graph, name="seat-a.20261111T000001Z.json", **rec):
    rot = graph / "sessions" / "rotations"
    rot.mkdir(parents=True, exist_ok=True)
    base = {"rotation": "crash-recovery", "seat": "seat-a", "result": "respawned",
            "recorded_at": "2026-11-11T00:00:01Z", "respawn_outcome": {"pid": 0}}
    base.update(rec)
    (rot / name).write_text(json.dumps(base))


def _stand_up(graph, rot=rotate, **flags):
    launched: list = []
    rc = rot.cmd_stand_up(NS(post="seat-a", window_path=None, **flags), graph, launcher=_launcher(launched))
    return rc, launched


def _mut(tmp_path, name, path, old, new):
    src = path.read_text()
    assert src.count(old) == 1, old
    dd = tmp_path / "mut"
    dd.mkdir(exist_ok=True)
    (dd / f"{name}.py").write_text(src.replace(old, new))
    spec = importlib.util.spec_from_file_location(name, dd / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m                       # cmd_stand_up resolves itself via sys.modules[__name__]
    spec.loader.exec_module(m)
    return m


# --- the classification: the socket's state, by errno, never tmux's words -----------------------------------------

def test_an_absent_socket_reads_no_server_though_tmux_never_says_so(scratch):
    w = heal._all_windows(socket=str(scratch / "gone"))
    assert w == [] and w.reason == "no-server" and w.detail.startswith("socket absent: "), w.detail
    assert "no server running" not in w.detail.lower()


def test_a_stale_socket_reads_no_server(scratch):
    p = scratch / "stale"
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(str(p))
    s.close()
    w = heal._all_windows(socket=str(p))
    assert w == [] and w.reason == "no-server" and w.detail.startswith("socket stale: "), w.detail


def test_an_unstatable_socket_reads_read_failed_and_names_its_owner(scratch, monkeypatch):
    """aio 12:10:55Z: EACCES on another uid's 0700 dir; os.path.exists reads False there, so the errno decides."""
    real_lstat = os.lstat

    def lstat(p, *a, **k):
        if str(p).endswith("/locked/default"):
            raise PermissionError(13, "Permission denied", str(p))
        return real_lstat(p, *a, **k)
    monkeypatch.setattr(heal.os, "lstat", lstat)
    (scratch / "locked").mkdir()
    w = heal._all_windows(socket=str(scratch / "locked" / "default"))
    assert w.reason == "read-failed" and w.detail.startswith("socket unstatable: ")
    assert w.detail.endswith(f"run it as {__import__('pwd').getpwuid(os.getuid()).pw_name}"), w.detail


def test_mutant_unstatable_classed_by_exists_reads_absent_RED(scratch, monkeypatch, tmp_path):
    m = _mut(tmp_path, "heal_mut_exists", BIN / "heal.py",
             "    try:\n        os.lstat(path)\n    except FileNotFoundError:\n        return \"absent\"\n"
             "    except OSError:\n        return \"unstatable\"\n",
             "    if not os.path.exists(path):\n        return \"absent\"\n")
    monkeypatch.setattr(m.os.path, "exists", lambda p: False)       # what EACCES looks like to exists()
    assert m._tmux_socket_state(str(scratch / "locked" / "default")) == "absent"


def test_mutant_no_server_keyed_on_the_phrase_alone_refuses_the_reboot_case_RED(scratch, tmp_path):
    m = _mut(tmp_path, "heal_mut_phrase", BIN / "heal.py",
             '    if state in ("absent", "stale"):\n        return WindowsUnread("no-server", detail)\n',
             '    if "no server running" in (said or "").lower():\n        return WindowsUnread("no-server", detail)\n')
    assert m._all_windows(socket=str(scratch / "gone")).reason == "read-failed"


# --- the join: the LATEST LAUNCH record, window == the row's ----------------------------------------------------

def test_the_join_reads_the_launch_record_past_a_newer_detected_one(graph, scratch):
    sock = scratch / "seat"
    (w,) = _server(sock)
    _row(graph, window=w)
    _record(graph, window_id=w, **_identity(sock))
    _record(graph, name="seat-a.20261111T000009Z.json", result="detected", recorded_at="2026-11-11T00:00:09Z",
            window_id="")
    srv, why = heal._seat_socket_join(graph, "seat-a", {"window": w}, rotate)
    assert srv["tmux_socket"] == str(sock) and why == ""


def test_mutant_latest_over_all_records_lets_detected_win_RED(graph, scratch, tmp_path):
    m = _mut(tmp_path, "heal_mut_latest", BIN / "heal.py",
             "                or not _is_launch_record(rec)):\n", "                or False):\n")
    sock = scratch / "seat"
    (w,) = _server(sock)
    _record(graph, window_id=w, **_identity(sock))
    _record(graph, name="seat-a.20261111T000009Z.json", result="detected", recorded_at="2026-11-11T00:00:09Z",
            window_id="")
    srv, why = m._seat_socket_join(graph, "seat-a", {"window": w}, rotate)
    assert srv == {} and "names window -" in why


def test_a_stale_record_with_the_same_id_behind_a_newer_window_is_a_miss(graph, scratch):
    """SM 12:15Z: the LATEST launch names @5; an older one names the row's @0 on another socket -> MISS, never a scan."""
    _record(graph, window_id="@0", tmux_socket="/old", tmux_server_start="1", tmux_server_pid="2")
    _record(graph, name="seat-a.20261111T000009Z.json", recorded_at="2026-11-11T00:00:09Z", window_id="@5",
            tmux_socket="/new", tmux_server_start="3", tmux_server_pid="4")
    srv, why = heal._seat_socket_join(graph, "seat-a", {"window": "@0"}, rotate)
    assert srv == {} and "names window @5, the row @0" in why


def test_both_writers_record_the_whole_identity_set_from_one_helper(graph, scratch, monkeypatch):
    sock = scratch / "seat"
    (w,) = _server(sock)
    ident = _identity(sock)
    monkeypatch.setattr(heal, "_window_server", lambda wid: dict(ident) if wid == w else {})
    heal._write_crash_recovery(graph, "seat-a", "x", {"pid": 0}, rotate, 0.0,
                               {"respawned": True, "window": w, "pid": os.getpid(), "name": "seat-a"})
    rec = json.loads(sorted((graph / "sessions" / "rotations").glob("seat-a.*.json"))[-1].read_text())
    assert {k: rec[k] for k in ident} == ident and rec["pid_starttime"] == heal._proc_starttime(os.getpid())
    src = (BIN / "rotate.py").read_text()
    assert src.count("rec.update(_h._window_server(window_id))") == 1        # rotate's writer: the SAME helper


def test_mutant_heal_records_the_socket_but_not_its_start_RED(graph, scratch, monkeypatch, tmp_path):
    m = _mut(tmp_path, "heal_mut_nostart", BIN / "heal.py",
             '           | (_window_server(outcome.get("window") or "") if res == "respawned" else {})),\n',
             '           | {k: v for k, v in (_window_server(outcome.get("window") or "") if res == "respawned" '
             'else {}).items() if k != "tmux_server_start"}),\n')
    sock = scratch / "seat"
    (w,) = _server(sock)
    ident = _identity(sock)
    monkeypatch.setattr(m, "_window_server", lambda wid: dict(ident))
    m._write_crash_recovery(graph, "seat-a", "x", {"pid": 0}, rotate, 0.0,
                            {"respawned": True, "window": w, "pid": 0, "name": "seat-a"})
    srv, why = heal._seat_socket_join(graph, "seat-a", {"window": w}, rotate)
    assert srv == {} and "names no tmux server" in why


# --- stand-up on the seat's own server -----------------------------------------------------------------------------

def test_the_seat_window_open_on_its_own_server_refuses_though_the_caller_has_none(graph, calls, scratch, capsys):
    """alive's row: the caller's default ABSENT; the seat's server holds its window -> refused."""
    sock = scratch / "seat"
    (w,) = _server(sock)
    _row(graph, window=w)
    _record(graph, window_id=w, **_identity(sock))
    rc, launched = _stand_up(graph)
    assert rc == 1 and launched == [] and f"window {w} is open" in capsys.readouterr().err


def test_mutant_no_server_judged_on_the_callers_default_launches_RED(graph, calls, scratch, tmp_path):
    m = _mut(tmp_path, "heal_mut_caller", BIN / "heal.py",
             "    return (_all_windows(window_path, socket=sock),\n", "    return (_all_windows(window_path),\n")
    sock = scratch / "seat"
    (w,) = _server(sock)
    _row(graph, window=w)
    _record(graph, window_id=w, **_identity(sock))
    sys.modules["heal"], keep = m, sys.modules["heal"]
    try:
        rc, launched = _stand_up(graph)
    finally:
        sys.modules["heal"] = keep
    assert rc == 0 and len(launched) == 1


@pytest.mark.parametrize("on_seat", [True, False])
def test_two_live_servers_the_seats_decides(graph, calls, scratch, capsys, on_seat):
    """sp's row: the caller's default is a LIVE server too, and @ids are per server. The seat's server alone decides:
    seat holds the window -> refused; seat lacks it (the caller's server has that @N) -> stands up."""
    seat_ids = _server(scratch / "seat", windows=2 if on_seat else 1)
    caller_ids = _server(_default(scratch), windows=1 if on_seat else 2)
    w = seat_ids[-1] if on_seat else caller_ids[-1]
    _row(graph, window=w, pid=99_999_999)
    _record(graph, window_id=w, **_identity(scratch / "seat"))
    rc, launched = _stand_up(graph)
    assert (rc, len(launched)) == ((1, 0) if on_seat else (0, 1)), capsys.readouterr().err


def test_a_restarted_seat_server_reads_no_server_and_stands_up(graph, calls, scratch, capsys):
    """sp 12:19Z: one socket path, server 1 held @N; killed; server 2 on the SAME path holds another window at @N."""
    sock = scratch / "seat"
    (w,) = _server(sock)
    ident = _identity(sock)
    _REAL_RUN(["tmux", "-S", str(sock), "kill-server"], capture_output=True, timeout=10)
    import time
    time.sleep(1.1)                                                   # start_time is whole seconds
    assert _server(sock) == [w]                                       # the same @id, another window
    _row(graph, window=w)
    _record(graph, window_id=w, **ident)
    rc, launched = _stand_up(graph)
    err = capsys.readouterr().err
    assert rc == 0 and len(launched) == 1, err


def test_mutant_the_join_keys_on_the_socket_path_alone_RED(graph, calls, scratch, tmp_path):
    m = _mut(tmp_path, "heal_mut_path", BIN / "heal.py",
             "    if live is not None and live != (srv[\"tmux_server_start\"], srv[\"tmux_server_pid\"]):\n",
             "    if False:\n")
    sock = scratch / "seat"
    (w,) = _server(sock)
    ident = _identity(sock)
    _REAL_RUN(["tmux", "-S", str(sock), "kill-server"], capture_output=True, timeout=10)
    _server(sock)
    _record(graph, window_id=w, **ident)
    win, how, _s = m._seat_windows(graph, "seat-a", {"window": w}, rotate)
    assert any(x == w for x, _n in win)                               # server 2's @N read as the seat's: refused


def test_a_live_server_whose_read_fails_refuses_by_name(graph, calls, scratch, monkeypatch, capsys):
    sock = scratch / "seat"
    (w,) = _server(sock)
    _row(graph, window=w)
    _record(graph, window_id=w, **_identity(sock))
    real = subprocess.run

    def run(cmd, *a, **k):
        if isinstance(cmd, list) and "list-windows" in cmd:
            return subprocess.CompletedProcess(cmd, 1, "", "lost server\n")
        return real(cmd, *a, **k)
    monkeypatch.setattr(subprocess, "run", run)
    rc, launched = _stand_up(graph)
    err = capsys.readouterr().err
    assert rc == 1 and launched == [] and "could not be read (read-failed: socket live: " in err, err


def test_mutant_the_reason_ignored_launches_on_read_failed_RED(graph, calls, scratch, monkeypatch, tmp_path):
    m = _mut(tmp_path, "rotate_mut_ignore", BIN / "rotate.py",
             "    if (isinstance(windows, _heal.WindowsUnread)\n", "    if (False and isinstance(windows, _heal.WindowsUnread)\n")
    sock = scratch / "seat"
    (w,) = _server(sock)
    _row(graph, window=w)
    _record(graph, window_id=w, **_identity(sock))
    real = subprocess.run
    monkeypatch.setattr(subprocess, "run", lambda cmd, *a, **k: subprocess.CompletedProcess(cmd, 1, "", "lost\n")
                        if isinstance(cmd, list) and "list-windows" in cmd else real(cmd, *a, **k))
    rc, launched = _stand_up(graph, rot=m)
    assert rc == 0 and len(launched) == 1


# --- a MISS: the pre-build rule and its way out --------------------------------------------------------------------

def test_an_empty_pid_miss_is_refused_naming_the_way_out(graph, calls, scratch, capsys):
    _row(graph, window="@7")
    rc, launched = _stand_up(graph)
    err = capsys.readouterr().err
    assert rc == 1 and launched == [] and "rotate.py stand-up --post seat-a --window-closed" in err, err


def test_the_way_out_stands_it_up_named(graph, calls, scratch, capsys):
    _row(graph, window="@7")
    rc, launched = _stand_up(graph, window_closed=True)
    assert rc == 0 and len(launched) == 1 and "window closed by hand" in capsys.readouterr().err


def test_mutant_the_flag_ignored_still_refuses_RED(graph, calls, scratch, tmp_path):
    m = _mut(tmp_path, "rotate_mut_flag", BIN / "rotate.py",
             '    window_closed = bool(getattr(args, "window_closed", False))\n', "    window_closed = False\n")
    _row(graph, window="@7")
    rc, launched = _stand_up(graph, rot=m, window_closed=True)
    assert rc == 1 and launched == []


def test_a_pid_miss_reads_the_callers_default_named(graph, calls, scratch, capsys):
    _row(graph, window="@7", pid=99_999_999)
    rc, launched = _stand_up(graph)
    err = capsys.readouterr().err
    assert rc == 0 and len(launched) == 1 and "reading the caller's default tmux server" in err, err


# --- the pid read: start time is the proof ------------------------------------------------------------------------

def _live_pid_record(graph, pid, start):
    _record(graph, window_id="@7", respawn_outcome={"pid": pid}, pid_starttime=start)


def test_a_live_pid_of_another_uid_is_alive_and_the_flag_cannot_pass_it(graph, calls, scratch, capsys):
    """aio + sp (a): pid 1 (root's systemd: os.kill EPERM from here) with its real start time -> alive, refused."""
    if os.getuid() == 0:
        pytest.skip("pid 1 is ours as root")
    assert heal._pid_alive(1) is True                                 # EPERM = alive
    _row(graph, window="@7", pid=1)
    _live_pid_record(graph, 1, heal._proc_starttime(1))
    rc, launched = _stand_up(graph, window_closed=True)
    assert rc == 1 and launched == [] and "row pid 1 is alive" in capsys.readouterr().err


def test_mutant_eperm_read_as_dead_RED(tmp_path):
    if os.getuid() == 0:
        pytest.skip("pid 1 is ours as root")
    m = _mut(tmp_path, "heal_mut_eperm", BIN / "heal.py",
             "    except ProcessLookupError:\n        return False\n    except OSError:\n        return True\n",
             "    except OSError:\n        return False\n")
    assert m._pid_alive(1) is False


def test_mutant_the_flags_gate_on_the_old_read_passes_a_live_seat_RED(graph, calls, scratch, tmp_path):
    if os.getuid() == 0:
        pytest.skip("pid 1 is ours as root")
    m = _mut(tmp_path, "rotate_mut_oldread", BIN / "rotate.py",
             "    pstate, pwhy = _heal._seat_pid_read(pid, harness, _rstart)\n",
             "    pstate, pwhy = (\"dead\", \"the old EPERM-as-dead read\")\n")
    _row(graph, window="@7", pid=1)
    _live_pid_record(graph, 1, heal._proc_starttime(1))
    rc, launched = _stand_up(graph, rot=m, window_closed=True)
    assert rc == 0 and len(launched) == 1


def test_a_pid_reused_by_the_same_program_is_dead_named(graph, calls, scratch, monkeypatch, capsys):
    """aio 12:22:23Z: the same comm, another start time -> reused = dead, named with comm + uid."""
    p = subprocess.Popen(["sleep", "300"])
    try:
        monkeypatch.setattr(heal, "_seat_pid_read", heal._seat_pid_read)
        import harness_template
        monkeypatch.setattr(harness_template, "bin_name", lambda h: "sleep")
        state, why = heal._seat_pid_read(p.pid, "claude-code", "1")
        assert state == "reused" and why.startswith(f"pid {p.pid} reused by sleep (uid "), why
        assert heal._seat_pid_read(p.pid, "claude-code", heal._proc_starttime(p.pid))[0] == "alive"
    finally:
        p.kill()
        p.wait()


def test_mutant_comm_only_reads_the_reused_pid_alive_RED(tmp_path, monkeypatch):
    m = _mut(tmp_path, "heal_mut_comm", BIN / "heal.py", "    if recorded_start:\n", "    if False:\n")
    p = subprocess.Popen(["sleep", "300"])
    try:
        import harness_template
        monkeypatch.setattr(harness_template, "bin_name", lambda h: "sleep")
        assert m._seat_pid_read(p.pid, "claude-code", "1")[0] == "alive"
    finally:
        p.kill()
        p.wait()


def test_without_a_recorded_start_the_weaker_comm_read_is_named(monkeypatch):
    p = subprocess.Popen(["sleep", "300"])
    try:
        import harness_template
        monkeypatch.setattr(harness_template, "bin_name", lambda h: "claude")
        state, why = heal._seat_pid_read(p.pid, "claude-code")
        assert state == "reused" and "the weaker read: no recorded start time" in why
    finally:
        p.kill()
        p.wait()



# --- all-is-one 12:55:08Z: an UNREAD /proc value cannot prove a reuse (hidepid) --------------------------------------

def test_an_unread_start_time_on_a_live_pid_reads_alive(monkeypatch):
    """hidepid=1: the dir stats, its files don't -> the start time reads '' -> kill(0) decides: alive, named."""
    monkeypatch.setattr(heal, "_proc_starttime", lambda pid: "")
    state, why = heal._seat_pid_read(os.getpid(), "claude-code", "12345")
    assert state == "alive" and "start time unread, kill(0) read" in why, why


def test_mutant_an_unread_start_time_reads_reused_RED(tmp_path, monkeypatch):
    m = _mut(tmp_path, "heal_mut_unread", BIN / "heal.py", "    if recorded_start and not start:\n",
             "    if False:\n")
    monkeypatch.setattr(m, "_proc_starttime", lambda pid: "")
    assert m._seat_pid_read(os.getpid(), "claude-code", "12345")[0] == "reused"


def test_a_pid_hidden_by_proc_but_alive_to_kill_reads_alive(monkeypatch):
    """hidepid=2: /proc/<pid> not found while kill(0) gives EPERM -> alive, named 'hidden by /proc'."""
    real_stat = Path.stat
    monkeypatch.setattr(Path, "stat", lambda self, *a, **k: (_ for _ in ()).throw(FileNotFoundError(str(self)))
                        if str(self) == "/proc/4242" else real_stat(self, *a, **k))

    def kill(pid, sig):
        raise PermissionError(1, "Operation not permitted")
    monkeypatch.setattr(heal.os, "kill", kill)
    state, why = heal._seat_pid_read(4242, "grok-bot", "1")
    assert state == "alive" and "hidden by /proc" in why, why


def test_mutant_proc_not_found_alone_reads_dead_RED(tmp_path, monkeypatch):
    m = _mut(tmp_path, "heal_mut_hidden", BIN / "heal.py",
             "        if _pid_alive(pid):\n            return \"alive\", f\"pid {pid} hidden by /proc",
             "        if False:\n            return \"alive\", f\"pid {pid} hidden by /proc")
    real_stat = Path.stat
    monkeypatch.setattr(Path, "stat", lambda self, *a, **k: (_ for _ in ()).throw(FileNotFoundError(str(self)))
                        if str(self) == "/proc/4242" else real_stat(self, *a, **k))
    monkeypatch.setattr(m.os, "kill", lambda pid, sig: (_ for _ in ()).throw(PermissionError(1, "x")))
    assert m._seat_pid_read(4242, "grok-bot", "1")[0] == "dead"



# --- sp 12:56:53Z: --window-closed counts ONLY on a MISS; on a HIT the seat's own read decides ----------------------

def test_the_flag_on_a_hit_is_refused_and_launches_nothing(graph, calls, scratch, capsys):
    sock = scratch / "seat"
    (w,) = _server(sock)
    _row(graph, window=w)
    _record(graph, window_id=w, **_identity(sock))
    rc, launched = _stand_up(graph, window_closed=True)
    err = capsys.readouterr().err
    assert rc == 1 and launched == [] and "its server is known" in err, err


def test_mutant_the_flag_skips_the_check_on_a_hit_RED(graph, calls, scratch, tmp_path):
    m = _mut(tmp_path, "rotate_mut_hitflag", BIN / "rotate.py",
             "    else:\n        if window_closed:\n", "    else:\n        if False:\n")
    sock = scratch / "seat"
    (w,) = _server(sock)
    _row(graph, window=w)
    _record(graph, window_id=w, **_identity(sock))
    rc, launched = _stand_up(graph, rot=m, window_closed=True)
    assert rc == 0 and len(launched) == 1                             # the open window overridden: a second harness
