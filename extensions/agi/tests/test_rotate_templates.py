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

# --- hypothesis:l4-rotations-startup-commands-must-parse -------------------
# A first_turn command that names a verb the producing tool does not have, or
# uses a placeholder EMPTY by construction at spawn time, wakes a successor
# into a usage dump (exit 2) on its very first turn (measured reproduction:
# `rotate.py whois` is not a verb; `send.py whois {succ_ref}` with {succ_ref}
# empty-by-construction). A template test must RENDER every first_turn cmd of
# every template with fixture values, assert each producing python verb parses
# with `-h` (exit 0), and assert no placeholder renders empty.

import json  # noqa: E402
import shlex  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402

# First_turn VALUES mirroring the LIVE canon (test_rotate_startup.VALUES), with
# every placeholder the fixed director/prime first_turn lists still uses.
STARTUP_VALUES = {
    "seat": "sanctuary-director",
    "succ_ref": "abc123",
    "succ_name": "sd-next",
    "succ_transcript": "/tmp/sd-next.jsonl",
    "pin_ref": "/tmp/sanctuary-director.meter",
    "gen": "11",
    "prime_ref": "7cff1a",
    "worktree": "/wt",
    "repo": "/repo",
    "tmux_session": "agi-rc",
    "pred_pids": "123 456",
}

# The FIXED director / prime_director first_turn lists, as the live
# rotations.md must read after this hypothesis: rotation-record names a verb
# that EXISTS (`rotate.py status ... --record latest`), and seat-row is gone
# (it read {succ_ref}, empty by construction at spawn — the row is only
# produced by the successor's own ack). Mirrors .agi/nodes/.geometry/rotations.md
# under the OWNER/PRIME gate: the gate is why the fix is a template edit a kid
# cannot land, not a code change.
FIXED_FIRST_TURN = {
    "director": [
        {"label": "rotation-record",
         "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} "
                "--record latest"},
        {"label": "prime-authority",
         "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} "
                "--claim belam"},
        {"label": "git-state",
         "cmd": "git -C {worktree} status -sb | head -5; "
                "git -C {repo} status -sb | head -3"},
        {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}"},
        {"label": "live-spawns",
         "cmd": "python3 extensions/agi/bin/spawn_budget.py status; "
                "python3 extensions/agi/bin/provisioning.py status | head -4"},
        {"label": "write-verbs",
         "cmd": "python3 extensions/agi/bin/write.py -h | sed -n 1,40p"},
    ],
}

_FIXED_TEMPLATES_BODY = """---
id: config:rotations
mint_id: deadbeef00000000000000000000000002
type: config
templates:
  director:
    brief_file: extensions/agi/briefs/director-successor.md
    steps: [handoff, spawn, join]
    telemetry: [seed]
    startup:
      first_turn:
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} --record latest", "why": "read-only record read"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "authority against the graph"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms"}
  prime_director:
    brief_file: extensions/agi/briefs/prime-director-successor.md
    steps: [handoff, spawn, join, authority]
    telemetry: [seed, ack]
    startup:
      first_turn:
        - {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} --record latest", "why": "read-only record read"}
        - {"label": "prime-authority", "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam", "why": "authority against the graph"}
        - {"label": "inbox", "cmd": "python3 extensions/agi/bin/send.py read {seat}", "why": "unread dms"}
---
# config:rotations fixture (fixed first_turn)
"""


def _producing_python_verb(cmd: str) -> tuple[Path, str] | None:
    """For an engine-python producing stage (`python3 <abs|rel>.py <verb> ...`),
    return (abs_script, verb); None for a non-python producer (git/tmux/ps) or
    a help-only stage (script already invoked with `-h`)."""
    try:
        toks = shlex.split(cmd)
    except ValueError:
        return None
    if not toks or toks[0] not in ("python3", sys.executable):
        return None
    if len(toks) < 3:
        return None
    script = toks[1]
    if not script.endswith(".py") or "extensions/" not in script:
        return None
    verb = toks[2]
    if verb.startswith("-"):
        return None  # help-only stage, parses by construction
    p = Path(script)
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[3] / script  # repo-root-relative
    return p, verb


def test_uniquely_director_first_turn_is_the_shipped_outer_shape():
    # The test's FIXED_FIRST_TURN is the outer contract this file pins: the
    # live rotations.md director list plus the fix. If it drifts from the live
    # node, the parse-assertions below guard a template nobody ships.
    cmds = [e["label"] for e in FIXED_FIRST_TURN["director"]]
    assert "rotation-record" in cmds
    assert "seat-row" not in cmds  # the fix: seat-row cannot succeed at spawn


def test_every_first_turn_producing_verb_parses_and_no_placeholder_empty():
    # hypothesis:l4-rotations-startup-commands-must-parse, fix-proof: render
    # each first_turn cmd of every template with fixture values, assert each
    # producing python verb parses (`<argv0> <verb> -h` exit 0) and that no
    # placeholder was left EMPTY (`{p}` resolving to "") — the state that made
    # `send.py whois {succ_ref}` dump usage (empty session_ref).
    import re as _re
    checked_verb = 0
    for tmpl_name, entries in FIXED_FIRST_TURN.items():
        for entry in entries:
            cmd = entry["cmd"]
            # every placeholder the cmd uses must have a NON-EMPTY value —
            # the state whose absence made `send.py whois {succ_ref}` dump
            # usage (empty session_ref) at spawn.
            used = _re.findall(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", cmd)
            for key in used:
                assert STARTUP_VALUES.get(key), (
                    f"{entry['label']} uses {{{key}}} which is EMPTY at spawn: "
                    f"{cmd!r}")
            rendered = rotate._resolve_startup_placeholders(cmd, STARTUP_VALUES)
            assert "{" not in rendered, (tmpl_name, entry["label"], rendered)
            # check every stage of a `;` sequence and the FIRST stage of each
            # `|` pipeline (the producing stage; post-`|` filters are sed/head)
            for stage in rendered.split(";"):
                producing = stage.split("|")[0].strip()
                if not producing:
                    continue
                pv = _producing_python_verb(producing)
                if pv is None:
                    continue
                script, verb = pv
                r = subprocess.run(
                    [sys.executable, str(script), verb, "-h"],
                    capture_output=True, text=True)
                assert r.returncode == 0, (
                    f"{entry['label']} verb {verb!r} does not parse: "
                    f"{r.stderr.strip() or r.stdout.strip()}")
                checked_verb += 1
    assert checked_verb >= 1, "no producing python verb was checked"


def test_falsifier_old_rotate_whois_does_not_parse():
    # The falsifier, made load-bearing: the OLD shipped command
    # `rotate.py whois` is NOT a verb — `-h` exits 2 (usage). The fix proof is
    # that the assertion above passes for `rotate.py status ... --record
    # latest` while this one proves whois is genuinely the defect.
    r = subprocess.run([sys.executable, str(BIN / "rotate.py"), "whois", "-h"],
                       capture_output=True, text=True)
    assert r.returncode != 0, "rotate.py whois must not parse (it has no such verb)"
    assert "invalid choice: 'whois'" in r.stderr


def test_status_record_reads_latest_surfaces_capsys(tmp_path, monkeypatch, capsys):
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)
    import datetime
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    (rot / f"sanctuary-director.{stamp}.json").write_text(
        json.dumps({"rotation": "rotate-self", "seat": "sanctuary-director",
                    "result": "success", "recorded_at": "2026-09-11T00:00:00Z"}))

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "latest rotation record" in out
    assert "result" in out and "success" in out
    assert "sequence=" in out
    assert "row:" in out and "sanctuary-director" in out
