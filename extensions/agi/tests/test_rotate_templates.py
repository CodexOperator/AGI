"""L4.110 prime ruling A — rotation template resolution from a FIXTURE root.

rotate-self resolves its rotation template (brief file + step list + telemetry
set) from `.agi/nodes/.geometry/rotations.md` — a type-config node the PRIME
owns. RESOLUTION ORDER, testable: `--template <name>` > role default > refuse
loudly NAMING THE NODE. No hardcoded brief path lives in rotate.py; the brief
file always comes from the node.

The tests build a throwaway .agi with its OWN rotations.md (written by the
test) and drive `rotate.main(['rotate-self', '--dry-run', ...])` against it.
They never touch the live .agi/nodes/.geometry/rotations.md (absent today —
that is the live refusal state this file pins) or seats.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import rotate  # noqa: E402

ROTATIONS_BODY = """---
id: config:rotations
mint_id: deadbeef00000000000000000000000001
type: config
templates:
  director:
    brief_file: extensions/agi/briefs/director-successor.md
    steps: [handoff, spawn, join, authority, release]
    telemetry: [seed, model, effort]
  prime_director:
    brief_file: extensions/agi/briefs/prime-director-successor.md
    steps: [handoff, spawn, join, authority, release, button-down]
    telemetry: [seed, model, effort, ack]
  helper:
    brief_file: extensions/agi/briefs/helper-successor.md
    steps: [handoff, spawn]
    telemetry: [seed]
---
# config:rotations
fixture
"""

SEATS_BODY = """---
id: config:seats
mint_id: 3e88873e3c204c5088f6ab81322a26de
type: config
seats:
  - {"name": "sanctuary-director", "role": "director"}
  - {"name": "belam", "role": "prime_director"}
---
body
"""


def _fixture_root(tmp_path, rotations: str | None,
                  seats: str | None = SEATS_BODY) -> Path:
    root = tmp_path
    agi = root / ".agi"
    agi.mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}")
    g = agi / "nodes" / ".geometry"
    g.mkdir(parents=True)
    if seats is not None:
        (g / "seats.md").write_text(seats)
    if rotations is not None:
        (g / "rotations.md").write_text(rotations)
    return agi  # the graph root (.agi), which is what find_project_root returns


def _rot_root(tmp_path, monkeypatch, rotations, seats=SEATS_BODY):
    r = _fixture_root(tmp_path, rotations, seats)

    def fake_root():
        return r
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    return r


def test_e_role_default_resolves_director(tmp_path, monkeypatch, capsys):
    """PROOF (e): on each seated role's dry run, rotate-self prints the
    template it resolved and from which level (role default)."""
    r = _rot_root(tmp_path, monkeypatch, ROTATIONS_BODY)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "(0) template" in out
    assert "director" in out
    assert "role default" in out
    assert "director-successor.md" in out
    assert "steps" in out


def test_f_explicit_template_from_another_role(tmp_path, monkeypatch, capsys):
    """PROOF (f): `--template <other-role>` resolves that role's brief/steps
    with no code change (using one role's template on another is legal)."""
    r = _rot_root(tmp_path, monkeypatch, ROTATIONS_BODY)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--template", "helper", "--dry-run", "--role", "director"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "--template flag" in out
    assert "helper-successor.md" in out


def test_g_removed_default_refuses_naming_node(tmp_path, monkeypatch, capsys):
    """PROOF (g): removing a role's default from the node makes its dry run
    refuse, NAMING THE NODE."""
    import re
    # drop the `director:` entry from the templates block
    body = re.sub(r"(?ms)^  director:.*?^  prime_director:",
                  "  prime_director:", ROTATIONS_BODY)
    _rot_root(tmp_path, monkeypatch, body)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "rotations.md" in err
    assert "director" in err


def test_absent_node_refuses_loudly(tmp_path, monkeypatch, capsys):
    """The LIVE state until the prime lands rotations.md: the node is absent,
    and rotate-self refuses loudly naming it."""
    _rot_root(tmp_path, monkeypatch, None)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "rotations.md" in err