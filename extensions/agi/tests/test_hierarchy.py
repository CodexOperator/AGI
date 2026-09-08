"""Red-first tests for hierarchy.py (hypothesis:l3w4-hierarchy-one-source).

Every --check class gets a fixture reproducing the real measured shape from
2026-09-08, asserted NONZERO before the checker is considered done, and a
clean seed asserted ZERO. The fixtures are written under a tmp graph root and
pointed at with --root, so the tests never touch the live tree.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin" / "hierarchy.py"

SEATS_FM = "".join(f'  - {json.dumps(r, sort_keys=True)}\n' for r in [
    {"name": "belam", "role": "prime_director", "tier": 3, "harness": "claude-code",
     "model": "claude-fable-5-1", "effort": "max", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/belam.meter", "rotated_by": "quorum", "owning_goal": ""},
    {"name": "self-perpetuating", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-sonnet-5", "effort": "max", "session_kind": "tty",
     "pin_ref": ".agi/sessions/self-perpetuating.meter", "rotated_by": "sanctuary-master",
     "owning_goal": ""},
    {"name": "sanctuary-director", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-sonnet-5", "effort": "max", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/sanctuary-director.meter", "rotated_by": "sanctuary-master",
     "owning_goal": "goal:g17"},
    {"name": "sensei-director", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-sonnet-5", "effort": "max", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/sensei-director.meter", "rotated_by": "master-sensei",
     "owning_goal": "goal:g16"},
    {"name": "sanctuary-master", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-opus-5", "effort": "high", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/sanctuary-master.meter", "rotated_by": "quorum",
     "owning_goal": ""},
    {"name": "master-sensei", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-sonnet-5", "effort": "max", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/master-sensei.meter", "rotated_by": "sanctuary-master",
     "owning_goal": ""},
])

LADDER_ROLES = [
    {"tier": 3, "role": "prime_director", "harness": "claude-code", "model": "claude-fable-5-1", "effort": "max", "settings": "ultracode"},
    {"tier": 3, "role": "parent", "harness": "claude-code", "model": "claude-opus-5", "effort": "max", "settings": "ultracode"},
    {"tier": 1, "role": "director", "harness": "claude-code", "model": "claude-fable-5-1", "effort": "max", "settings": ""},
    {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""},
]

LADDER_FM = (
    "caps:\n"
    "  director_kids: 2\n"
    "roles:\n"
    + "".join(f'  - {json.dumps(r, sort_keys=True)}\n' for r in LADDER_ROLES)
)


def _write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _clean_seed(root: Path):
    _write(root, "nodes/.geometry/seats.md", "---\nid: config:seats\nseats:\n"
            + SEATS_FM + "---\n")
    _write(root, "nodes/.geometry/ladder.md", "---\nid: ladder:ladder\n"
            + LADDER_FM + "---\n")


def _maybe_mkdir_config(root: Path):
    """hierarchy falls back to --root directly, no config.json needed."""
    (root / "sessions").mkdir(parents=True, exist_ok=True)


def _check(root: Path) -> tuple[int, str]:
    out = subprocess.run(
        [sys.executable, str(BIN), "--check", "--root", str(root)],
        capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr


def _pin(root: Path, name: str, transcript: str):
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    (root / "sessions" / f"{name}.meter").write_text(transcript, encoding="utf-8")
    return (root / "sessions" / f"{name}.meter")


# --------------------------------------------------------------------------- #
# Class 1 — orphan pin with no seat row
# --------------------------------------------------------------------------- #
def test_orphan_pin_nonzero(tmp_path):
    _clean_seed(tmp_path)
    _maybe_mkdir_config(tmp_path)
    _pin(tmp_path, "dir-g1", "0\t/nowhere/q.jsonl")
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "dir-g1.meter has no seat row" in out


def test_orphan_pin_ignores_agent_ids(tmp_path):
    _clean_seed(tmp_path)
    _maybe_mkdir_config(tmp_path)
    _pin(tmp_path, "a00-12345678", "0\t/nowhere/q.jsonl")
    rc, _ = _check(tmp_path)
    assert rc == 0


# --------------------------------------------------------------------------- #
# Class 2 — two rows pin to the same transcript
# --------------------------------------------------------------------------- #
def test_duplicate_transcript_nonzero(tmp_path):
    _clean_seed(tmp_path)
    tx = tmp_path / "shared.jsonl"
    tx.write_text("", encoding="utf-8")
    _pin(tmp_path, "self-perpetuating", f"0\t{tx}")
    _pin(tmp_path, "sensei-director", f"0\t{tx}")
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "duplicate_transcript" in out


# --------------------------------------------------------------------------- #
# Class 3 — rotated_by naming a seat that has no row
# --------------------------------------------------------------------------- #
def test_rotated_by_nonzero(tmp_path):
    _clean_seed(tmp_path)
    seed = (tmp_path / "nodes" / ".geometry" / "seats.md").read_text()
    seed = seed.replace('"rotated_by": "quorum"',
                        '"rotated_by": "advisor"')
    _write(tmp_path, "nodes/.geometry/seats.md", seed)
    _maybe_mkdir_config(tmp_path)
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "rotated_by" in out and "advisor" in out


def test_rotated_by_roleclass_allowed(tmp_path):
    _clean_seed(tmp_path)
    _maybe_mkdir_config(tmp_path)
    rc, _ = _check(tmp_path)
    assert rc == 0  # quorum / prime are valid roleclass rotators


# --------------------------------------------------------------------------- #
# Class 4 — director-kids above caps.director_kids
# --------------------------------------------------------------------------- #
def test_director_kids_over_cap_nonzero(tmp_path):
    _clean_seed(tmp_path)  # 2 director-kids == cap 2 -> clean
    _maybe_mkdir_config(tmp_path)
    rc, _ = _check(tmp_path)
    assert rc == 0
    # add a third tier-1 director owning a goal
    seed = (tmp_path / "nodes" / ".geometry" / "seats.md").read_text()
    extra = json.dumps({"name": "dir-x", "role": "director", "tier": 1,
                        "model": "claude-sonnet-5", "effort": "max",
                        "session_kind": "tty", "rotated_by": "sanctuary-master",
                        "owning_goal": "goal:g99"})
    close = seed.rfind("---\n")
    seed = seed[:close] + f"  - {extra}\n" + "---\n"
    _write(tmp_path, "nodes/.geometry/seats.md", seed)
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "director_kids" in out


# --------------------------------------------------------------------------- #
# Class 5 — (tier, role) with no ladder row and no seat model
# --------------------------------------------------------------------------- #
def test_unresolved_nonzero(tmp_path):
    _clean_seed(tmp_path)
    extra = json.dumps({"name": "mystery", "role": "wizard", "tier": 2,
                        "harness": "claude-code", "model": "", "effort": "",
                        "session_kind": "tty", "rotated_by": "quorum",
                        "owning_goal": ""})
    seed = (tmp_path / "nodes" / ".geometry" / "seats.md").read_text()
    close = seed.rfind("---\n")
    seed = seed[:close] + f"  - {extra}\n" + "---\n"
    _write(tmp_path, "nodes/.geometry/seats.md", seed)
    _maybe_mkdir_config(tmp_path)
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "unresolved" in out and "wizard" in out


# --------------------------------------------------------------------------- #
# Class 6 — body table disagrees with its own frontmatter
# --------------------------------------------------------------------------- #
def test_body_table_nonzero(tmp_path):
    _clean_seed(tmp_path)
    bad = (
        "---\nid: ladder:ladder\n" + LADDER_FM + "---\n"
        "# body\n"
        "| tier | role | harness | model | effort | settings |\n"
        "|---|---|---|---|---|---|\n"
        "| 1 | director | claude-code | claude-sonnet-5 | max |  |\n"
    )  # frontmatter says tier-1 director is fable-5-1; body says sonnet-5
    _write(tmp_path, "nodes/.geometry/ladder.md", bad)
    _maybe_mkdir_config(tmp_path)
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "body_table" in out


def test_clean_seed_zero(tmp_path):
    _clean_seed(tmp_path)
    _maybe_mkdir_config(tmp_path)
    rc, out = _check(tmp_path)
    assert rc == 0, out