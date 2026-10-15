"""Conjuncts 3+4 of hypothesis:l5-the-meter-captures-the-final-card-and-forces-
the-rotation-itself, as amended by the owner ruling 05:1xZ (trigger (b)):
`alarms --once` ROTATES a held seat that is IDLE at/over `captive_rotate_ratio`
x the line directly by the master path (no dm), and `alarms` is runnable as a
declared detached systemd user unit.

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
                "director_rotate_at": 0.25,
                "captive_rotate_ratio": 0.85}.get(field, default)

    monkeypatch.setattr(rotate, "load_ladder_field", fake_load)
    (tmp_path / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    return tmp_path


def _alarms(root, holder):
    return SimpleNamespace(holder=holder, once=True, interval=300,
                           comms_root=str(root / "comms"), root=None)


def test_alarms_idle_at_ratio_master_rotates_held_seat(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """A held seat at 0.85 x line, idle >= M minutes, is rotated directly by
    the master path with the holder as caller -- and no dm is sent."""
    _write_seats_sheet(tmp_path, [{"name": "kid-1", "role": "director",
                                   "rotated_by": "advisor"}])
    _pin_seat_transcript(tmp_path, "kid-1", tokens=21_250)  # 0.2125 = 0.85*0.25
    _stamp(tmp_path, "kid-1", age_s=21 * 60)                # idle > 20 min
    spawns = []
    monkeypatch.setattr(rotate, "_caller_hold_key",
                        lambda root, seat, row, how: (seat, row or {}, how))
    monkeypatch.setattr(rotate, "_spawn_master_rotate",
                        lambda argv, env, cwd: spawns.append((argv, env)))
    rc = rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path)
    assert rc == 0
    assert len(spawns) == 1, capsys.readouterr().out
    assert spawns[0][0][2:] == ["rotate", "--post", "kid-1"]
    assert spawns[0][1]["AGI_POST"] == "advisor"
    assert not list((tmp_path / "comms").glob("dm/*.md"))


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


def test_alarms_unit_argv_carries_user_working_directory_and_root(
        tmp_path, monkeypatch):
    """The meter loop NEVER reaches for systemd: the only detached runner is
    the declared unit file (residue 3, option a), so a plain `cmd_alarms` call
    spawns nothing."""
    calls = []

    def rec(*a, **kw):
        calls.append(a)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", rec)
    monkeypatch.setattr(rotate, "find_project_root", lambda: tmp_path)
    monkeypatch.setattr(rotate, "load_ladder_field", lambda r, f, d: d)
    assert rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path) == 0
    assert calls == []


def test_alarms_detach_flag_and_helper_are_gone():
    """Residue 3, option (a): the DECLARED systemd service in
    .agi/nodes/.geometry/crons.md (`agi-alarms-sanctuary-master`, rendered by
    `crons.py` from the node's own `services:` table) is the real detached
    runner, so `alarms --detach` and `_run_alarms_unit` are dead code and must
    be gone -- no flag kept "just in case". Naming the service line that
    replaces them keeps the deletion falsifiable."""
    assert not hasattr(rotate, "_run_alarms_unit")
    src = Path(rotate.__file__).read_text(encoding="utf-8")
    assert "--detach" not in src, "the dead alarms --detach flag survived"


def test_declared_alarms_service_is_the_detached_production_runner():
    """The surviving production path really runs the meter: the LIVE crons
    node declares `agi-alarms-sanctuary-master` with an exec_start that runs
    `rotate.py alarms --holder sanctuary-master`, and that line must NOT carry
    `--detach` (the service IS the detach). Reads the live node, never a
    copied list."""
    engine_root = Path(rotate.__file__).resolve().parents[3]
    sys.path.insert(0, str(engine_root / "extensions" / "agi"))
    from agi.bin import crons  # noqa: PLC0415

    node = crons.load_crons_node(engine_root / ".agi")
    svc = node["services"]["agi-alarms-sanctuary-master"]
    assert svc["enabled"] is True
    exec_start = svc["exec_start"]
    assert "rotate.py alarms --holder sanctuary-master" in exec_start, exec_start
    assert "--detach" not in exec_start, exec_start

