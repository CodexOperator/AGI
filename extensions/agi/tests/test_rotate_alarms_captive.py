"""Trigger (b) of hypothesis:l5-the-meter-captures-the-final-card-and-forces-
the-rotation-itself (owner ruling 05:1xZ): the alarms pass ROTATES a held seat
directly by the master path -- `rotate.py rotate --post <seat>` with
`AGI_POST=<holder>` (the holder's key is the caller) -- instead of dmming it.
The idle lane's ratio comes from the ladder cell `captive_rotate_ratio`;
absent = the idle lane is OFF by name (the over-line lane is unchanged).

Red-first: written before the code.
"""
import json
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
def ladder(tmp_path, monkeypatch):
    """A fake ladder of exactly the cells a test sets; unknown fields fall
    back to the default (so an ABSENT captive cell is absent, not defaulted)."""
    cells = {}
    monkeypatch.setattr(rotate, "find_project_root", lambda: tmp_path)

    def fake_load(root_param, field, default):
        return cells.get(field, default)

    monkeypatch.setattr(rotate, "load_ladder_field", fake_load)
    (tmp_path / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    return cells


@pytest.fixture
def spawns(monkeypatch):
    """Record the ONE detached-child seam; nothing real is ever spawned."""
    recorded = []
    monkeypatch.setattr(rotate, "_spawn_master_rotate",
                        lambda argv, env, cwd: recorded.append((argv, env, cwd)))
    return recorded


def _keyed(monkeypatch):
    monkeypatch.setattr(rotate, "_caller_hold_key",
                        lambda root, seat, row, how: (seat, row or {}, how))


def _alarms(root, holder):
    return SimpleNamespace(holder=holder, once=True, interval=300,
                           comms_root=str(root / "comms"), root=None)


def _director(root, holder="advisor"):
    _write_seats_sheet(root, [{"name": "kid-1", "role": "director",
                               "rotated_by": holder}])


def _captive(cells):
    cells.update({"director_rotate_at": 0.40, "alarms_idle_minutes": 20,
                  "captive_rotate_ratio": 0.85,
                  "director_context_tokens": 100_000})


def test_alarms_idle_at_ratio_master_rotates_no_dm(ladder, spawns, monkeypatch,
                                                   tmp_path):
    """Idle 60m at f=0.42 (line 0.40, ratio 0.85 -> lane at 0.34): rotate the
    seat directly with the holder as caller, and send NO dm."""
    _captive(ladder)
    _keyed(monkeypatch)
    _director(tmp_path)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=42_000)   # f=0.42
    _stamp(tmp_path, "kid-1", age_s=60 * 60)
    # discriminating: the child env must SET AGI_POST itself, not inherit it.
    monkeypatch.delenv("AGI_POST", raising=False)
    assert rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path) == 0
    assert len(spawns) == 1, spawns
    argv, env, cwd = spawns[0]
    assert argv[1].endswith("rotate.py") and argv[2:] == ["rotate", "--post",
                                                          "kid-1"], argv
    assert env["AGI_POST"] == "advisor", env
    assert Path(cwd) == tmp_path
    assert not list((tmp_path / "comms").glob("dm/*.md")), "no dm in this lane"


def test_alarms_idle_below_ratio_holds(ladder, spawns, monkeypatch, tmp_path,
                                       capsys):
    """Idle 60m at f=0.10 (< 0.85 x 0.40 = 0.34): hold, no child, no dm."""
    _captive(ladder)
    _keyed(monkeypatch)
    _director(tmp_path)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=10_000)   # f=0.10
    _stamp(tmp_path, "kid-1", age_s=60 * 60)
    assert rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path) == 0
    assert spawns == []
    assert not list((tmp_path / "comms").glob("dm/*.md"))
    assert "hold kid-1" in capsys.readouterr().out


def test_alarms_over_line_rotates_directly_no_dm(ladder, spawns, monkeypatch,
                                                 tmp_path):
    """f=0.50 >= the line: rotate directly (the dm is what the ruling
    replaced), regardless of idleness."""
    _captive(ladder)
    _keyed(monkeypatch)
    _director(tmp_path)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=50_000)   # f=0.50
    _stamp(tmp_path, "kid-1", age_s=60)                      # working
    assert rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path) == 0
    assert [s[0][2:] for s in spawns] == [["rotate", "--post", "kid-1"]], spawns
    assert not list((tmp_path / "comms").glob("dm/*.md"))


def test_alarms_ratio_read_from_ladder_half(ladder, spawns, monkeypatch,
                                            tmp_path):
    """The cell is the threshold: ratio 0.5 fires the idle lane at 0.5 x 0.40
    = 0.20, so f=0.21 idle 60m rotates."""
    _captive(ladder)
    ladder["captive_rotate_ratio"] = 0.5
    _keyed(monkeypatch)
    _director(tmp_path)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=21_000)   # f=0.21
    _stamp(tmp_path, "kid-1", age_s=60 * 60)
    assert rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path) == 0
    assert len(spawns) == 1, spawns


def test_alarms_absent_ratio_idle_lane_off_by_name(ladder, spawns, monkeypatch,
                                                   tmp_path, capsys):
    """No captive cell: a seat at 0.9 x the line, idle 60m, is HELD -- the idle
    lane is off by name. (The over-line lane is proven unchanged above.)"""
    ladder.update({"director_rotate_at": 0.40, "alarms_idle_minutes": 20,
                   "director_context_tokens": 100_000})
    _keyed(monkeypatch)
    _director(tmp_path)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=36_000)   # f=0.36 = 0.9*0.4
    _stamp(tmp_path, "kid-1", age_s=60 * 60)
    assert rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path) == 0
    assert spawns == []
    assert "hold kid-1" in capsys.readouterr().out


def test_alarms_unkeyable_holder_refuses_by_name_and_spawns_nothing(
        ladder, spawns, tmp_path, capsys):
    """The holder's key does not load: refuse BY NAME, never spawn (the child
    would refuse after a success print), and never fall back to a dm."""
    _captive(ladder)
    _director(tmp_path)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=42_000)
    _stamp(tmp_path, "kid-1", age_s=60 * 60)
    assert rotate.cmd_alarms(_alarms(tmp_path, "advisor"), tmp_path) == 0
    assert spawns == []
    err = capsys.readouterr().err
    assert "refused" in err and "advisor" in err, err
    assert not list((tmp_path / "comms").glob("dm/*.md"))


def test_alarms_master_row_needs_the_ladder_cell(ladder, spawns, monkeypatch,
                                                 tmp_path):
    """A *master* seat rotates only when captive_rotate_masters is on."""
    _captive(ladder)
    _keyed(monkeypatch)
    _write_seats_sheet(tmp_path, [{"name": "sanctuary-master",
                                   "role": "director",
                                   "rotated_by": "prime"}])
    _pin_seat_transcript(tmp_path, "sanctuary-master", tokens=42_000)
    _stamp(tmp_path, "sanctuary-master", age_s=60 * 60)
    assert rotate.cmd_alarms(_alarms(tmp_path, "prime"), tmp_path) == 0
    assert spawns == [], "master row rotated with the cell default off"
    ladder["captive_rotate_masters"] = True
    monkeypatch.delenv("AGI_POST", raising=False)
    assert rotate.cmd_alarms(_alarms(tmp_path, "prime"), tmp_path) == 0
    assert len(spawns) == 1, spawns
    assert spawns[0][1]["AGI_POST"] == "prime"


def test_alarms_prime_row_is_never_rotated(ladder, spawns, monkeypatch,
                                           tmp_path):
    """The Prime is never a captive target, even at f=0.99."""
    _captive(ladder)
    _keyed(monkeypatch)
    _write_seats_sheet(tmp_path, [{"name": "belam", "role": "prime_director",
                                   "rotated_by": "quorum"}])
    _pin_seat_transcript(tmp_path, "belam", tokens=99_000)
    _stamp(tmp_path, "belam", age_s=60 * 60)
    assert rotate.cmd_alarms(_alarms(tmp_path, "quorum"), tmp_path) == 0
    assert spawns == []
