"""goal:g7.31.1.3 -- heal names every silent seat read.

F1 run 1 of goal:g7.31.1.2 read 'seat-dead scan ... 0 dead' while the row's pid was gone, and heal's log could not
say why. Rows here, each RED on the trunk's heal.py before this leaf (the mutant: the old bare skip / the old label):

  guard (_crash_recovery_recorded), an unread record or field HOLDS the respawn and is named:
    unreadable (mode 000) · torn JSON · bytes that are not UTF-8 · not a JSON object · a respawned record with an unparsable recorded_at
  CONTROL: a readable respawned record older than SEAT_DEAD_WINDOW_S does NOT hold, and writes no hold line
  in-window: the guard hands the caller '<file> <age> s old'; _watch_one_seat names it only when the pid is gone
  _watch_one_seat's window-present return names the @id and the pane pid (unknown when the pass map lacks it), never 'vouches'
  _watch_seats' summary reads '<n> pid(s) gone + <e> empty-pid closed-window row(s); <m> acted', never 'dead'
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
import rotate  # noqa: E402

NOW = 2_000_000_000.0


@pytest.fixture(autouse=True)
def _env(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_REAPER_LOG", str(tmp_path / "reaper.log"))
    rot = tmp_path / "rotations"
    rot.mkdir()
    monkeypatch.setattr(rotate, "_rotations_dir", lambda root: rot)
    return rot


def _log(tmp_path) -> str:
    p = tmp_path / "reaper.log"
    return p.read_text() if p.exists() else ""


def _stamp(t: float) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _rec(rot: Path, name: str, body) -> Path:
    p = rot / f"s.{name}.json"
    p.write_text(body if isinstance(body, str) else json.dumps(body))
    return p


def _respawned(age: float) -> dict:
    return {"rotation": "crash-recovery", "result": "respawned", "recorded_at": _stamp(NOW - age)}


def _guard(tmp_path, why=None):
    return heal._crash_recovery_recorded(tmp_path, "s", rotate, now=NOW, why=why)


# --- the guard: an unread record or field HOLDS and is named ------------------------------------------------

def test_unreadable_record_holds_and_is_named(tmp_path, _env):
    p = _rec(_env, "A", _respawned(30))
    p.chmod(0o000)
    try:
        # sp NIT 10:57:48Z: the row proves the file IS unreadable first (root reads a 000 file): a loud fail, never a skip
        try:
            p.read_text()
        except PermissionError:
            pass
        else:
            pytest.fail("the mode-000 record is readable to this uid (root?): the row would read nothing")
        assert _guard(tmp_path) is True
    finally:
        p.chmod(0o600)
    assert "crash-recovery record s.A.json unreadable (PermissionError" in _log(tmp_path)
    assert "respawn held" in _log(tmp_path)


def test_torn_record_holds_and_is_named(tmp_path, _env):
    _rec(_env, "A", '{"rotation": "crash-recovery", "res')
    assert _guard(tmp_path) is True
    assert "crash-recovery record s.A.json unreadable (JSONDecodeError" in _log(tmp_path)


def test_invalid_utf8_record_holds_and_is_named(tmp_path, _env):
    """aio 12:59:54Z: bytes that are not UTF-8 raise UnicodeDecodeError (a ValueError, not a JSONDecodeError); the
    guard must HOLD + name it, never raise out of the scan for every seat."""
    (_env / "s.A.json").write_bytes(b'{"rotation": "crash-recovery", "result": "respawned", "x": "\xff"}')
    assert _guard(tmp_path) is True
    assert "crash-recovery record s.A.json unreadable (UnicodeDecodeError" in _log(tmp_path)


def test_utf16_record_holds_and_is_named(tmp_path, _env):
    """sp 13:03:33Z: a UTF-16 file (with its mark) is a second bad-bytes shape: held + named, never raised."""
    (_env / "s.A.json").write_bytes(json.dumps(_respawned(30)).encode("utf-16"))
    assert _guard(tmp_path) is True
    assert "crash-recovery record s.A.json unreadable (UnicodeDecodeError" in _log(tmp_path)


def test_non_object_record_holds_and_is_named(tmp_path, _env):
    _rec(_env, "A", "[1, 2]")
    assert _guard(tmp_path) is True
    assert "s.A.json is not a JSON object: respawn held" in _log(tmp_path)


def test_unparsable_recorded_at_holds_and_is_named(tmp_path, _env):
    _rec(_env, "A", {"rotation": "crash-recovery", "result": "respawned", "recorded_at": "yesterday"})
    assert _guard(tmp_path) is True
    assert "s.A.json recorded_at 'yesterday' unparsable: respawn held" in _log(tmp_path)


def test_a_bad_record_sorted_first_still_holds(tmp_path, _env):
    """The torn record sorts before a readable OLD one: the hold comes from the torn one, never 'no record'."""
    _rec(_env, "A", "{torn")
    _rec(_env, "B", _respawned(5_000))
    assert _guard(tmp_path) is True


def test_control_old_readable_record_does_not_hold(tmp_path, _env):
    _rec(_env, "A", _respawned(heal.SEAT_DEAD_WINDOW_S + 60))
    assert _guard(tmp_path) is False
    assert "respawn held" not in _log(tmp_path)


def test_in_window_hold_hands_the_caller_its_file_and_age(tmp_path, _env):
    _rec(_env, "A", _respawned(40))
    why: list = []
    assert _guard(tmp_path, why=why) is True
    assert why == ["s.A.json 40 s old"]


def test_other_rotation_kinds_still_do_not_hold(tmp_path, _env):
    _rec(_env, "A", {"rotation": "rotate-self", "result": "success", "recorded_at": _stamp(NOW - 5)})
    assert _guard(tmp_path) is False


# --- _watch_one_seat: the two silent returns now name themselves ------------------------------------------

def _one(tmp_path, monkeypatch, *, held: bool, alive: bool, window: bool, pane_pids=None):
    def guard(root, seat, _rotate, now=None, why=None):
        if held and why is not None:
            why.append("s.A.json 40 s old")
        return held
    monkeypatch.setattr(heal, "_crash_recovery_recorded", guard)
    monkeypatch.setattr(heal, "_seat_geometry_dir", lambda root, row: None)
    monkeypatch.setattr(heal, "_window_present", lambda *a, **k: (window, None))
    row = {"name": "s", "pid": 4242, "window": "@7"}
    return heal._watch_one_seat(tmp_path, row, [], rotate, now=NOW, pid_alive=lambda p: alive, pane_pids=pane_pids)


def test_held_seat_with_a_gone_pid_is_named(tmp_path, monkeypatch):
    assert _one(tmp_path, monkeypatch, held=True, alive=False, window=False) == {}
    assert ("watch: seat s pid 4242 gone; held by a respawned record s.A.json 40 s old"
            in _log(tmp_path))


def test_held_seat_with_a_live_pid_stays_quiet(tmp_path, monkeypatch):
    assert _one(tmp_path, monkeypatch, held=True, alive=True, window=False) == {}
    assert "held by a respawned record" not in _log(tmp_path)


def test_window_present_return_names_the_window(tmp_path, monkeypatch):
    """sp 13:03:33Z: the line says what was READ: the @id, the pane pid from the pass map, and no more than 'not
    another seat's window' (the row pid is gone, so the chain can never vouch for it)."""
    assert _one(tmp_path, monkeypatch, held=False, alive=False, window=True, pane_pids={"@7": 9001}) == {}
    assert ("watch: seat s pid 4242 gone; window @7 present (pane pid 9001); not another seat's window: "
            "not respawned") in _log(tmp_path)
    assert "vouches" not in _log(tmp_path)


def test_window_present_with_the_pane_unknown_says_unknown(tmp_path, monkeypatch):
    assert _one(tmp_path, monkeypatch, held=False, alive=False, window=True, pane_pids={}) == {}
    assert "window @7 present (pane pid unknown); not another seat's window: not respawned" in _log(tmp_path)
    assert "vouches" not in _log(tmp_path)


# --- _watch_seats: the summary says what it counts ------------------------------------------------------

def test_summary_counts_gone_pids_and_acted(tmp_path, monkeypatch):
    rows = [{"name": "a", "pid": 11}, {"name": "b", "pid": 22}]
    monkeypatch.setattr(rotate, "_load_seats", lambda root: rows)
    monkeypatch.setattr(heal, "_all_windows", lambda wp=None: [])
    monkeypatch.setattr(heal, "_load_launcher", lambda l: None)
    monkeypatch.setattr(heal, "_pin_table", lambda root, rows: ({}, []))
    monkeypatch.setattr(heal, "_seat_sessions", lambda *a, **k: {})
    monkeypatch.setattr(heal.boxes, "row_is_local", lambda root, r: True)
    monkeypatch.setattr(heal, "_watch_one_seat", lambda *a, **k: {})
    monkeypatch.setattr(heal, "_alert_deferred", lambda *a, **k: None)
    heal._watch_seats(tmp_path, now=NOW, pid_alive=lambda p: p == 11)
    log = _log(tmp_path)
    assert "seat-dead scan over 2 configured pid row(s); 1 pid(s) gone + 0 empty-pid closed-window row(s); 0 acted" in log
    assert " dead\n" not in log
