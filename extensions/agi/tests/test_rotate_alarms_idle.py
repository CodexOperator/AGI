"""Conjuncts 3+4 of hypothesis:l5-the-meter-captures-the-final-card-and-forces-
the-rotation-itself: `alarms --once` also dms a held seat that is IDLE below the
line, and `alarms` is runnable as a detached systemd user unit.

Red-first: written before the code.
"""
import json
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate


def _write_seats_sheet(root, rows):
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def _pin_seat_transcript(root, name, tokens):
    transcript = root / f"t-{name}.jsonl"
    transcript.write_text(json.dumps({
        "message": {"role": "assistant",
                    "usage": {"input_tokens": tokens,
                              "cache_read_input_tokens": 0,
                              "cache_creation_input_tokens": 0}},
    }) + "\n", encoding="utf-8")
    (root / "sessions" / f"{name}.meter").write_text(
        str(transcript) + "\n", encoding="utf-8")


def _stamp(root, seat, age_s):
    p = root / "sessions" / "seats" / f"{seat}.last-act"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"{int(time.time()) - age_s}\n", encoding="utf-8")


@pytest.fixture
def fake_ladder(tmp_path, monkeypatch):
    monkeypatch.setattr(rotate, "find_project_root", lambda: tmp_path)

    def fake_load(root_param, field, default):
        return {"director_context_tokens": 100_000,
                "director_rotate_at": 0.25}.get(field, default)

    monkeypatch.setattr(rotate, "load_ladder_field", fake_load)
    (tmp_path / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    return tmp_path


def _alarms(root, holder):
    return SimpleNamespace(holder=holder, once=True, interval=300,
                           comms_root=str(root / "comms"), root=None)


def test_alarms_idle_below_line_dms_held_seat(fake_ladder, tmp_path, capsys):
    """A held seat at 0.85 x line, idle >= M minutes, gets exactly one dm."""
    _write_seats_sheet(tmp_path, [{"name": "kid-1", "role": "director",
                                   "rotated_by": "advisor"}])
    _pin_seat_transcript(tmp_path, "kid-1", tokens=21_250)  # 0.2125 = 0.85*0.25
    _stamp(tmp_path, "kid-1", age_s=21 * 60)                # idle > 20 min
    rc = rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path)
    assert rc == 0
    dms = list((tmp_path / "comms").glob("dm/*.md"))
    assert len(dms) == 1, capsys.readouterr().out
    assert "rotate now" in dms[0].read_text(encoding="utf-8")


def test_alarms_working_seat_same_fraction_stays_silent(fake_ladder, tmp_path,
                                                        capsys):
    """Same fraction but a fresh last act: NOT idle, NO dm (never a false alarm)."""
    _write_seats_sheet(tmp_path, [{"name": "kid-1", "role": "director",
                                   "rotated_by": "advisor"}])
    _pin_seat_transcript(tmp_path, "kid-1", tokens=21_250)
    _stamp(tmp_path, "kid-1", age_s=60)                     # worked a minute ago
    rc = rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path)
    assert rc == 0
    assert not list((tmp_path / "comms").glob("dm/*.md"))


def test_alarms_unmeasurable_last_act_is_not_idle(fake_ladder, tmp_path):
    """No stamp and no card commit -> unmeasurable -> not idle -> no dm."""
    _write_seats_sheet(tmp_path, [{"name": "kid-1", "role": "director",
                                   "rotated_by": "advisor"}])
    _pin_seat_transcript(tmp_path, "kid-1", tokens=21_250)
    rc = rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path)
    assert rc == 0
    assert not list((tmp_path / "comms").glob("dm/*.md"))


def test_alarms_unit_argv_carries_user_working_directory_and_root(tmp_path,
                                                                  monkeypatch):
    seen = {}

    def rec(argv, **kw):
        seen["argv"] = argv
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", rec)
    rc = rotate._run_alarms_unit(tmp_path, "advisor")
    argv = seen["argv"]
    assert argv[0] == "systemd-run"
    assert "--user" in argv
    assert "--working-directory" in argv
    assert argv[argv.index("--working-directory") + 1] == str(tmp_path)
    assert "--root" in argv
    assert argv[argv.index("--root") + 1] == str(tmp_path)
    assert rc == 0


def _alarms_detached(root, holder):
    return SimpleNamespace(holder=holder, once=False, interval=300, detach=True,
                           comms_root=str(root / "comms"), root=None)


def test_alarms_detach_launches_unit_once_and_never_meters(tmp_path,
                                                           monkeypatch):
    """P7 fix: `alarms --detach` calls `_run_alarms_unit` once, does not
    enter the meter loop, and sends no dm."""
    calls = []

    def rec(argv, **kw):
        calls.append(argv)
        return SimpleNamespace(returncode=7)

    monkeypatch.setattr(subprocess, "run", rec)
    rc = rotate.cmd_alarms(_alarms_detached(tmp_path, "advisor"), tmp_path)
    assert rc == 7, "the runner's returncode is returned"
    assert len(calls) == 1, calls
    argv = calls[0]
    assert argv[0] == "systemd-run"
    assert "--user" in argv
    assert "--working-directory" in argv
    assert argv[argv.index("--working-directory") + 1] == str(tmp_path)
    assert argv[argv.index("--root") + 1] == str(tmp_path)
    assert "alarms" in argv
    inner = argv[argv.index("alarms") + 1:]
    assert "--holder" in inner and inner[inner.index("--holder") + 1] == "advisor"
    assert "--root" in inner and inner[inner.index("--root") + 1] == str(tmp_path)
    assert "--detach" not in argv, "the detached unit must not recurse"
    assert not (tmp_path / "comms").exists(), "no dm, no meter"
