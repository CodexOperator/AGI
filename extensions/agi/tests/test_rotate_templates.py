"""L4.110 prime ruling A — rotation template resolution from a FIXTURE root.

rotate-self resolves its rotation template (brief file + step list + telemetry
set) from `.agi/nodes/.geometry/rotations.md` — a type-config node the PRIME
owns. RESOLUTION ORDER, testable: `--template <name>` > role default > refuse
loudly NAMING THE NODE. No hardcoded brief path lives in rotate.py; the brief
file always comes from the node.

The resolution/refusal tests build a throwaway .agi with its OWN rotations.md
(written by the test) and drive `rotate.main(['rotate-self', '--dry-run', ...])`
against it — they never touch the live node or seats.md. The startup-parse tests
(hypothesis:l4-rotations-startup-commands-must-parse) are the one exception:
they READ templates.*.startup.first_turn from the checked-in live
.agi/nodes/.geometry/rotations.md (both roles) so a dead command in the shipped
node fails the suite; they never write it.
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

# The startup-parse tests read templates.*.startup.first_turn straight from
# the checked-in .agi/nodes/.geometry/rotations.md (BOTH roles: director and
# prime_director), instead of a mirrored fixture that could mask a dead command
# in the live node. Reading the live node is all the tests do — rotations.md is
# never written here. The dead _FIXED_TEMPLATES_BODY / FIXED_FIRST_TURN fixture
# this replaced only MIRRORED the node, so a live node that regressed to
# `rotate.py whois` would keep them green; reading the bytes the suite ships is
# the only claim that holds the templates to what rotates the seats.
def _live_first_turn() -> dict:
    """Templates.<role>.startup.first_turn for EVERY role, read from the
    checked-in .agi/nodes/.geometry/rotations.md (not a fixture copy). The
    rotations node is `type: config`, owned by the owner/prime — a kid reads it
    (and the fixed templates it already carries under
    hypothesis:l4-rotations-startup-commands-must-parse) and never writes it.
    """
    from graph_core.persistence import frontmatter as _fm  # noqa: E402
    rot = (Path(__file__).resolve().parents[3]
           / ".agi" / "nodes" / ".geometry" / "rotations.md")
    assert rot.exists(), f"live rotations.md missing: {rot}"
    nf = _fm.load_node_file(rot)
    templates = nf.frontmatter.get("templates") or {}
    out = {}
    for name, ent in templates.items():
        if not isinstance(ent, dict):
            continue
        startup = ent.get("startup") or {}
        ft = startup.get("first_turn") or []
        entries = [e for e in ft if isinstance(e, dict)]
        if entries:
            out[str(name)] = entries
    return out


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
    # Outer-shape guard on the LIVE node, not a mirror: the checked-in
    # rotations.md director first_turn must carry the shipped `rotation-record`
    # fix and must NOT carry the dead `seat-row` (it read {succ_ref}, empty by
    # construction at spawn — the row is only produced by the successor's own
    # ack). If the live node drifts, the guard trips here AND the parse/
    # empty-assertions below guard the templates that actually ship.
    first_turn = _live_first_turn()
    assert "director" in first_turn, "live rotations.md has no director template"
    assert "prime_director" in first_turn, (
        "live rotations.md has no prime_director template")
    cmds = [e["label"] for e in first_turn["director"]]
    assert "rotation-record" in cmds
    assert "seat-row" not in cmds  # the fix: seat-row cannot succeed at spawn


def test_every_first_turn_producing_verb_parses_and_no_placeholder_empty():
    # hypothesis:l4-rotations-startup-commands-must-parse, fix-proof on the
    # LIVE node: render every first_turn cmd of EVERY template read from the
    # checked-in .agi/nodes/.geometry/rotations.md (director + prime_director),
    # assert each producing python verb parses (`<argv0> <verb> -h` exit 0) and
    # that no placeholder was left EMPTY (`{p}` resolving to "") — the state
    # that made `send.py whois {succ_ref}` dump usage (empty session_ref).
    # A live node that regresses to `rotate.py whois` fails here (whois is not
    # a rotate.py verb — the falsifier below proves it), which is exactly the
    # drift the FIXED_FIRST_TURN fixture used to mask.
    import re as _re
    first_turn = _live_first_turn()
    assert set(first_turn) >= {"director", "prime_director"}, (
        "expected BOTH templates' first_turn in the live rotations.md")
    checked_verb = 0
    for tmpl_name, entries in first_turn.items():
        for entry in entries:
            cmd = entry["cmd"]
            # every placeholder the cmd uses must have a NON-EMPTY value —
            # the state whose absence made `send.py whois {succ_ref}` dump
            # usage (empty session_ref) at spawn.
            used = _re.findall(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", cmd)
            for key in used:
                assert STARTUP_VALUES.get(key), (
                    f"{tmpl_name}/{entry['label']} uses {{{key}}} which is "
                    f"EMPTY at spawn: {cmd!r}")
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
                    f"{tmpl_name}/{entry['label']} verb {verb!r} does not "
                    f"parse: {r.stderr.strip() or r.stdout.strip()}")
                checked_verb += 1
    assert checked_verb >= 2, "each of the two live templates must check a verb"


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


def test_wait_returns_zero_when_record_already_terminal(
        tmp_path, monkeypatch, capsys):
    """hypothesis:rotate-status-record-latest-gains-wait FALSIFIER (a): a
    `--wait` call must return 0 immediately (never sleep) when the record is
    already terminal — s12_self_reap present — on its first read."""
    import datetime
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    (rot / f"sanctuary-director.{stamp}.json").write_text(json.dumps({
        "rotation": "rotate-self", "seat": "sanctuary-director",
        "result": "success", "s12_self_reap": {"pane_pid": 123}}))

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)

    def boom(*a, **k):
        raise AssertionError("--wait slept past an already-terminal record")
    monkeypatch.setattr(rotate.time, "sleep", boom)

    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest", "--wait", "30"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "s12_self_reap" in out and "123" in out
    assert "sequence=" in out


def test_wait_times_out_when_record_never_terminal(
        tmp_path, monkeypatch, capsys):
    """hypothesis:rotate-status-record-latest-gains-wait FALSIFIER (b): a
    `--wait N` whose record never becomes terminal must time out, print the
    last-seen record plus ERR, and exit 2 — never return 0."""
    import datetime
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    (rot / f"sanctuary-director.{stamp}.json").write_text(json.dumps({
        "rotation": "rotate-self", "seat": "sanctuary-director",
        "result": "success"}))

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    monkeypatch.setattr(rotate.time, "sleep", lambda *a, **k: None)

    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest", "--wait", "3"])
    cap = capsys.readouterr()
    assert rc == 2
    assert "ERR: still not terminal after 3s" in cap.err
    assert "latest rotation record" in cap.out
    assert "success" in cap.out


def test_wait_returns_zero_when_record_becomes_terminal_mid_wait(
        tmp_path, monkeypatch, capsys):
    """hypothesis:rotate-status-record-latest-gains-wait happy path: a
    `--wait N` call must hold until s12_self_reap lands mid-wait, then return
    0 with the now-terminal record printed."""
    import datetime
    import threading
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "seats.md").write_text(SEATS_BODY)
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    rec = rot / f"sanctuary-director.{stamp}.json"
    rec.write_text(json.dumps({"rotation": "rotate-self",
                               "seat": "sanctuary-director",
                               "result": "success"}))

    real_sleep = rotate.time.sleep

    def become_terminal():
        real_sleep(0.2)
        doc = json.loads(rec.read_text())
        doc["s12_self_reap"] = {"pane_pid": 999}
        rec.write_text(json.dumps(doc))
    threading.Thread(target=become_terminal, daemon=True).start()

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    monkeypatch.setattr(rotate.time, "sleep",
                        lambda *a, **k: real_sleep(0.05))

    rc = rotate.main(["status", "--seat", "sanctuary-director",
                      "--record", "latest", "--wait", "10"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "s12_self_reap" in out and "999" in out

# --- hypothesis:l4-a-rotation-costs-... mechanism 3: geometry freshness ------
# A rotating WORKTREE's OWN copy of `.agi/nodes/.geometry/` (config:rotations +
# config:seats) can be BEHIND the shared geometry branch (`origin/season/s2`).
# Spawning a successor there would bake a STALE rotation config into it
# SILENTLY. So rotate-self resolves WHICH tree the geometry comes from, once,
# up front: the integration tree (`locations.git_common_root`) when the
# worktree's own is behind and that tree's is current, else REFUSE BY NAME with
# the behind-count and the sync command. Falsifier: a rotate-self that spawns
# on a stale .geometry/ silently.
import subprocess as _sp  # noqa: E402


def _mgit(root, *args):
    out = _sp.run(["git", "-C", str(root), *args],
                  capture_output=True, text=True)
    assert out.returncode == 0, f"git {' '.join(args)}: {out.stderr.strip()}"
    return out.stdout.strip()


def _geometry_commit(root, rotations_body, message) -> str:
    """Write .agi/nodes/.geometry/ + config.json into `root`, commit, return the
    full commit sha. The commit only touches the geometry subtree, so a later
    `rev-list --count HEAD..ref -- .agi/nodes/.geometry/` sees exactly 1."""
    agi = root / ".agi"
    agi.mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}")
    g = agi / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(rotations_body)
    (g / "seats.md").write_text(SEATS_BODY)
    _mgit(root, "add", "-A")
    _mgit(root, "commit", "-q", "-m", message)
    return _mgit(root, "rev-parse", "HEAD")


def _mgit_repo(root):
    root.mkdir(parents=True, exist_ok=True)
    _mgit(root, "init", "-q")
    _mgit(root, "config", "user.email", "test@example.com")
    _mgit(root, "config", "user.name", "test")


def test_m3_stale_worktree_refuses_by_name_and_sync_cmd(
        tmp_path, monkeypatch, capsys):
    """Mechanism 3 (REFUSE): a worktree whose own .geometry/ is behind
    origin/season/s2 must refuse rotate-self BY NAME with the behind-count and
    the sync command — never spawn on the stale config silently."""
    repo = tmp_path / "repo"
    _mgit_repo(repo)
    base = _geometry_commit(repo, ROTATIONS_BODY, "geometry v1")
    tip = _geometry_commit(repo, ROTATIONS_BODY + "# v2\n", "geometry v2")
    # Simulate the shared geometry branch having moved: origin/season/s2 points
    # at the newer geometry while this worktree stays at v1 (behind by 1).
    _mgit(repo, "update-ref", "refs/remotes/origin/season/s2", tip)
    _mgit(repo, "checkout", "-q", "-b", "loop/stale", base)
    root = repo / ".agi"

    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    monkeypatch.chdir(repo)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "refused" in err
    assert "behind" in err
    assert "1 commit" in err
    assert "origin/season/s2" in err
    assert "git merge --no-edit origin/season/s2" in err   # merge, never rebase


def test_m3_stale_worktree_serves_integration_tree_geometry(
        tmp_path, monkeypatch, capsys):
    """Mechanism 3 (serve from {repo}): a WORKTREE behind on .geometry/ whose
    integration tree (locations.git_common_root) carries CURRENT geometry
    resolves config:rotations + config:seats FROM that tree — the resolver
    names it. The live rotate-self still never spawns on it: `_prepare_checks`
    (goal:g15.14 STEP 2, landed after this mechanism was cut) refuses ANY
    behind count first — rc 3, the merge line — so a behind seat SYNCS its
    tree rather than being served around it (director fix-up at the SL1.06
    harvest; the serve path stays as the guard on the fixture seam, where the
    checklist does not run)."""
    main = tmp_path / "main"
    _mgit_repo(main)
    base = _geometry_commit(main, ROTATIONS_BODY, "geometry v1")
    _mgit(main, "checkout", "-q", "-b", "season/s2")
    # A linked worktree forked at v1: its own geometry is behind.
    wt = tmp_path / "wt"
    _mgit(main, "worktree", "add", "-q", "-b", "loop/stale", str(wt), base)
    # Advance the INTEGRATION tree (season/s2) with newer geometry; the worktree
    # (still at v1) is now behind origin/season/s2 by exactly 1 geometry commit.
    tip = _geometry_commit(main, ROTATIONS_BODY + "# v3\n", "geometry v3")
    _mgit(main, "update-ref", "refs/remotes/origin/season/s2", tip)
    root = wt / ".agi"

    # the resolver alone: the integration tree's geometry is served, by name
    cfg_root, note = rotate._geometry_resolution_root(root)
    assert cfg_root == main / ".agi"
    assert "integration tree" in note
    assert str(main) in note
    assert "by 1 commit" in note

    # the live command: the captive checklist wins — refused by name, rc 3,
    # with the ONE clear command (merge, never rebase)
    def fake_root():
        return root
    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    monkeypatch.chdir(wt)
    rc = rotate.main(["rotate-self", "--name", "sanctuary-director",
                      "--dry-run", "--role", "director"])
    cap = capsys.readouterr()
    assert rc == 3, cap.out + cap.err
    assert "behind origin/season/s2 (1)" in cap.err
    assert "git merge --no-edit origin/season/s2" in cap.err
    assert "rebase" not in cap.err


def test_m3_template_source_recorded(tmp_path):
    """Mechanism 3: the rotate-self rotation record NAMES which tree the
    template came from (`template_source`)."""
    import json as _json  # noqa: E402
    rec = tmp_path / "seat.20260101T000000Z.json"
    rotate._write_rotate_self_started(
        rec, seat="sanctuary-director", steps=["handoff"],
        gen_before=10, gen_after=11,
        template_source="integration tree /repo (worktree geometry behind "
                        "origin/season/s2 by 2 commit(s))")
    doc = _json.loads(rec.read_text(encoding="utf-8"))
    assert doc["template_source"].startswith("integration tree /repo")
    assert "by 2 commit(s)" in doc["template_source"]
    assert doc["result"] == "started"
    assert doc["steps_reached"] == ["handoff"]
