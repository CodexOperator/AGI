"""Tests for the STEP 1 driven handoff writer — `rotate.py handoff --driven`
(goal:g15.14, hypothesis:l4-rotate-self-drives-the-handoff-and-prepares-the-
spawn).

RED FIRST: every claim below was written before the code, and each drives the
fixture root (never the live tree) end-to-end:

1. **Driven §0 carries the fixture record's gen/window/pid and the fixture
   verify counts** — the MEASURED-only §0 block, never hand-written.
2. **An empty §3 answer is refused** — the one next command is never guessed.
3. **A card over the guard (HANDOFF_CARD_LIMIT_LINES) is refused naming the
   section to cut** — the existing "under 100 lines" rule, found not invented.
4. **Non-§0/§3/§6 sections and the preamble are carried verbatim.**
5. **A field that is not s3/s6 is refused.**
6. **A card absent §3 never writes** (refusal is atomic — no partial card).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "extensions"))   # the `agi` package
_BIN = _REPO / "extensions" / "agi" / "bin"
sys.path.insert(0, str(_BIN))  # so the lazy `import verification` resolves

from agi.bin import rotate  # noqa: E402


@pytest.fixture
def card_root(tmp_path):
    """A fixture GRAPH root (`nodes/` marks it a graph dir → sessions under
    it), with the verify-count baseline and a rotation record the driven §0
    must carry. No seats.md → role/model/fraction degrade to n/a, which keeps
    the fixture free of the ladder."""
    (tmp_path / "nodes").mkdir(parents=True)
    sess = tmp_path / "sessions"
    (sess / "rotations").mkdir(parents=True)
    # verification.py's baseline under <groot>/sessions/verify-count.json.
    (sess / "verify-count.json").write_text(json.dumps({
        "active": 100, "deprecated": 5, "total": 108,
        "sha": "abc123", "stamped_at": 0.0, "reason": "test",
    }), encoding="utf-8")
    # One durable rotation record for the seat.
    (sess / "rotations" / "adv-alive.20260911T120000Z.json").write_text(
        json.dumps({
            "rotation": "rotate-self", "seat": "adv-alive",
            "recorded_at": "2026-09-11T12:00:00Z", "result": "success",
            "observations": {"b_generation": {"before": 4, "after": 5}},
            "handover": {
                "join": {"found": True, "window_id": "@285", "pid": 3959818,
                         "name": "seed-adv-alive"},
                "model_confirm": {"expected": {"model": "x"},
                                  "live": {"model": "x"}, "verdict": "ok"},
            },
        }), encoding="utf-8")
    return tmp_path


def _args(**over):
    base = dict(driven=True, seat="adv-alive", field=None)
    base.update(over)
    return SimpleNamespace(**base)


def _written_card(root):
    return (root / "sessions" / "quorum" / "adv-alive.md").read_text(
        encoding="utf-8")


class _Stdin:
    """One-answer stdin stand-in: `-` reads a single line."""
    def __init__(self, lines):
        self._lines = list(lines)

    def readline(self):
        return (self._lines.pop(0) + "\n") if self._lines else "\n"


def _stdin(monkeypatch, lines):
    monkeypatch.setattr("sys.stdin", _Stdin(lines))


def test_driven_s0_carries_fixture_record_and_verify_counts(
        card_root, capsys, monkeypatch):
    """§0 is generated from the recorded gen/window/pid and the fixture
    verify-count baseline — never hand-written values."""
    _stdin(monkeypatch, ["bash next.sh", "banked option"])
    rc = rotate.cmd_handoff(_args(field=[["s3", "-"], ["s6", "-"]]),
                            card_root)
    assert rc == 0, capsys.readouterr().err
    card = _written_card(card_root)
    assert "gen 4->5" in card
    assert "@285" in card
    assert "3959818" in card
    assert "model_confirm ok" in card
    assert "active 100" in card
    assert "deprecated 5" in card


def test_driven_writes_card_when_s3_supplied_s6_omitted(card_root, capsys,
                                                        monkeypatch):
    """§6 is optional to fill; §3 is the critical field and suffices."""
    monkeypatch.setattr("sys.stdin", _Stdin(["bash next.sh"]))
    rc = rotate.cmd_handoff(_args(field=[["s3", "-"]]), card_root)
    assert rc == 0, capsys.readouterr().err
    card = _written_card(card_root)
    assert "## §3" in card
    assert "bash next.sh" in card


class _Stdin:
    """One-answer stdin stand-in: `-` reads a single line."""
    def __init__(self, lines):
        self._lines = list(lines)

    def readline(self):
        return (self._lines.pop(0) + "\n") if self._lines else "\n"


def test_empty_s3_is_refused_and_writes_nothing(card_root, capsys,
                                                monkeypatch):
    """The one next command is never guessed: an empty §3 refuses (exit 2)
    BEFORE any write — no partial card."""
    _stdin(monkeypatch, [""])
    rc = rotate.cmd_handoff(_args(field=[["s3", "-"]]), card_root)
    assert rc == 2
    err = capsys.readouterr().err
    assert "EMPTY §3" in err
    assert not (card_root / "sessions" / "quorum" / "adv-alive.md").exists()


def test_card_over_the_guard_is_refused_naming_the_section(
        card_root, capsys, monkeypatch):
    """A composed card past HANDOFF_CARD_LIMIT_LINES refuses, naming the
    biggest section to cut (the existing "under 100 lines" rule)."""
    _stdin(monkeypatch, ["bash next", "banked"])
    fat = "\n".join(f"l{i}" for i in range(200))  # one long carried section
    existing = (
        "# SESSION HANDOFF — fixture\n\n"
        "## §0 STATE (old)\nold s0\n\n"
        f"## §1 CARRIED\n{fat}\n\n"
        "## §3 🔴 NEXT COMMAND\nold next\n\n"
        "## §6 BANKED\nold banked\n"
    )
    q = card_root / "sessions" / "quorum"
    q.mkdir(parents=True, exist_ok=True)
    (q / "adv-alive.md").write_text(existing, encoding="utf-8")
    rc = rotate.cmd_handoff(
        _args(field=[["s3", "-"], ["s6", "-"]]), card_root)
    assert rc == 2
    err = capsys.readouterr().err
    assert "over the" in err
    assert "## §1 CARRIED" in err  # the biggest section is named
    # not written
    assert "old next" in _written_card(card_root)


def test_nonasked_sections_and_preamble_carried_verbatim(
        card_root, capsys, monkeypatch):
    """Every section but §0/§3/§6 — and the pre-`##` preamble — survives
    byte-for-byte; only §0 is replaced and §3/§6 filled."""
    _stdin(monkeypatch, ["bash next", "banked"])
    existing = (
        "# SESSION HANDOFF — fixture\n\n"
        "owner rule line\n\n"
        "## §0 STATE (old)\nold s0 stuff\n\n"
        "## §1 WHAT LANDED\nline-A\nline-B\n\n"
        "## §3 🔴 NEXT COMMAND\nold next\n\n"
        "## §4 TRAPS\nkeep me exactly\n\n"
        "## §6 BANKED\nold banked\n"
    )
    q = card_root / "sessions" / "quorum"
    q.mkdir(parents=True, exist_ok=True)
    (q / "adv-alive.md").write_text(existing, encoding="utf-8")
    rc = rotate.cmd_handoff(
        _args(field=[["s3", "-"], ["s6", "-"]]), card_root)
    assert rc == 0, capsys.readouterr().err
    card = _written_card(card_root)
    assert card.startswith("# SESSION HANDOFF — fixture\n\nowner rule line")
    assert "## §1 WHAT LANDED\nline-A\nline-B" in card
    assert "## §4 TRAPS\nkeep me exactly" in card
    assert "old s0 stuff" not in card       # §0 replaced
    assert "old next" not in card           # §3 replaced
    assert "old banked" not in card         # §6 replaced


def test_unknown_field_is_refused(card_root, capsys):
    """Only §3/§6 are bounded; a field outside them is a named refusal."""
    rc = rotate.cmd_handoff(_args(field=[["s1", "-"]]), card_root)
    assert rc == 2
    assert "not one of them" in capsys.readouterr().err