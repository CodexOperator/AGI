"""L4.114 s8-live + s9-s12 — the TAIL (kid 2 of the round).

Owns the tail of the ONE rotate-self call, on a FIXTURE root + stand-in
processes — never the live seats row, never a live spawn, never a real claude
pid, never a write under ~/.claude:
  (s8 live) grid-commit legality: a fixture reporting season/s2 but checked
            out on a non-season branch RECORDS `SKIPPED: grid commit illegal
            on <branch>` and never invokes grid.py.
  (s9)      re-point the `view-<seat>` livestream to the successor's @id —
            absent session / missing seam recorded SKIPPED naming it.
  (s10)     the bootstrap record carries the template telemetry + the
            verification result, `SKIPPED: 0b owns` for underivable values.
  (s11)     verification runs at the cheapest cited level; a fixture records
            SKIPPED, a seam returns its parsed --json result.
  (s12)     reap the predecessor chain DEEPEST-FIRST (stand-in sleeps) and
            kill the predecessor window BY @id, never a dotted name.
s9/s11/s12 may only be fixture-provable — the live view re-point, real
verification and the live self-reap are the parent's (named residue).
"""
import json
import os
import re
import signal
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

import rotate  # noqa: E402


@pytest.fixture
def _fix(tmp_path, monkeypatch):
    """Fixture root for rotate-self tail mechanics (mirrors
    test_rotate_handover._fix)."""
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")

    def fake_root():
        return root

    monkeypatch.setattr(rotate, "find_project_root", fake_root)
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent:\n    brief_file: extensions/agi/briefs/parent-successor.md\n"
        "    steps: [handoff, spawn, handover, readback, record, kill]\n"
        "    telemetry: [seed, model, ack]\n---\n\nbody\n",
        encoding="utf-8")
    return root


def _write_seats_sheet(root, rows):
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def _rs_args(tmp_path, **over):
    base = dict(name="adv-alive", force=False, timeout=5, debug_file=None,
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=False, successor_argv=None, role="parent",
                session_ref=None, successor_transcript=None, own_pid=None,
                belam_prefix=None)
    base.update(over)
    return SimpleNamespace(**base)


class _FakeTmux(object):
    """window-name file stands in for `tmux list-windows` (like
    test_rotate_handover)."""

    def __init__(self, tmp_path, initial=()):
        self.win = tmp_path / "windows.txt"
        self.win.write_text("\n".join(initial) + "\n", encoding="utf-8")

    def fake_spawn(self, **kw):
        with open(self.win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"


def _latest_record(root, seat):
    rot = root / "sessions" / "rotations"
    recs = sorted(rot.glob(f"{seat}.*.json"))
    assert recs, f"no rotation record under {rot}"
    return json.loads(recs[-1].read_text(encoding="utf-8"))


# ── (s8 live) grid-commit legality: season reports s2, branch differs ──────


def test_button_down_skips_illegal_branch_real_state(_fix, tmp_path,
                                                     monkeypatch):
    """A fixture reporting season/s2 (legal_branch=season/s2) checked out on a
    NON-season branch records `SKIPPED: grid commit illegal on <branch>` with
    the real branch named, and never invokes grid.py (no commit, no push)."""
    calls = []

    def fake_run(argv, *a, **k):
        calls.append(argv)
        if "rev-parse" in argv:                    # the only git read
            return subprocess.CompletedProcess(argv, 0, "iter24-foo\n", "")
        return subprocess.CompletedProcess(argv, 1, "", "")  # grid illegal

    monkeypatch.setattr(rotate.subprocess, "run", fake_run)
    out = rotate._button_down(
        root=tmp_path, branch_allow=True, legal_branch="season/s2")
    assert "SKIPPED: grid commit illegal on iter24-foo" in out
    assert "branch != season/s2" in out
    assert not any("grid.py" in " ".join(str(c) for c in call)
                   for call in calls)


def test_button_down_legal_branch_runs_grid(_fix, tmp_path, monkeypatch):
    """When the checked-out branch IS the season branch and the gate is on,
    grid.py is invoked once (the mechanism, not the destination — a fixture
    git is faked so no real commit happens)."""
    calls = []

    def fake_run(argv, *a, **k):
        calls.append(argv)
        if "rev-parse" in argv:
            return subprocess.CompletedProcess(argv, 0, "season/s2\n", "")
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(rotate.subprocess, "run", fake_run)
    out = rotate._button_down(
        root=tmp_path, branch_allow=True, legal_branch="season/s2")
    assert out.startswith("grid committed")
    assert any("grid.py" in " ".join(str(c) for c in call)
               for call in calls)


# ── (s9) re-point the livestream views ────────────────────────────────────


def test_repoint_livestream_views_absent_session_skipped(_fix, tmp_path):
    """No successor @id => SKIPPED naming the view session; with the
    window-path seam set but no view-path seam => SKIPPED, never real tmux."""
    out = rotate._repoint_livestream_views(
        tmux_session="t", seat="adv-alive", succ_id=None, window_path="x")
    assert out["skipped"]
    assert "view-adv-alive" in out["skipped"]
    out2 = rotate._repoint_livestream_views(
        tmux_session="t", seat="adv-alive", succ_id="@9", window_path="x")
    assert "no view-path seam" in out2["skipped"]


def test_repoint_livestream_views_uses_view_path_seam(_fix, tmp_path):
    """With a view-path seam (the view session's `@id <active>` lines) the
    re-point records the successor @id as its target and the verify read."""
    view = tmp_path / "views.txt"
    view.write_text("@5 1\n@9 0\n", encoding="utf-8")  # @5 active, @9 successor
    out = rotate._repoint_livestream_views(
        tmux_session="t", seat="adv-alive", succ_id="@9", window_path="x",
        view_path=str(view))
    assert out["target"] == "@9"
    assert out["session"] == "view-adv-alive"
    assert any(w.startswith("@9") for w in out["active_windows"])


# ── (s10) the bootstrap record ────────────────────────────────────────────


def test_bootstrap_records_telemetry_and_skips_0b(_fix, tmp_path):
    """<sessions>/seats/<seat>.bootstrap.json carries the template telemetry;
    values rotate-self cannot derive are `SKIPPED: 0b owns deriving <name>`."""
    path = rotate._write_bootstrap(
        tmp_path, seat="adv-alive", generation=1,
        telemetry=["seed", "model", "worktree"],
        verification={"ok": True, "level": "quick", "count": 7})
    p = tmp_path / "sessions" / "seats" / "adv-alive.bootstrap.json"
    assert str(p) == path
    doc = json.loads(p.read_text(encoding="utf-8"))
    assert doc["shape"] == "v1"
    assert doc["generation"] == 1
    assert doc["telemetry"]["seed"].startswith("SKIPPED: 0b owns")
    assert doc["verification"]["count"] == 7


# ── (s11) verification at the cheapest level ──────────────────────────────


def test_run_verification_fixture_skipped(_fix, tmp_path):
    """Running the cheap level against a fixture root (no graph) is a
    non-zero exit => recorded {ok: False, skipped: ...} — never a raise."""
    out = rotate._run_verification(tmp_path)
    assert out["ok"] is False
    assert "skipped" in out


def test_run_verification_seam_parses_json(_fix, tmp_path):
    """A verification_argv seam (a fake `--json` producer) returns its parsed
    dict with ok=True — the mechanism, not the destination."""
    out = rotate._run_verification(
        tmp_path,
        argv=["python3", "-c",
              "import json,sys; json.dump({'level':'quick','links':0}, "
              "sys.stdout)"])
    assert out["ok"] is True
    assert out["links"] == 0


# ── (s12) the predecessor chain reap + kill by @id ────────────────────────


def test_reap_chain_deepest_first(_fix, tmp_path):
    """A two-deep `sleep` chain is TERM'd DEEPEST-FIRST and each pid is gone
    afterward (verified with the `ps` reads the observation records)."""
    proc_pane = subprocess.Popen(["sleep", "1000"])
    proc_claude = subprocess.Popen(["sleep", "1000"])
    try:
        out = rotate._reap_chain([proc_pane.pid, proc_claude.pid])
        assert out["order"] == "deepest-first"
        # deepest (the outer element) reaped FIRST: chain[0] is the deep pid.
        assert out["chain"][0]["pid"] == proc_claude.pid
        assert out["chain"][0]["gone_after"] is True
        assert out["chain"][1]["gone_after"] is True
        assert not rotate._pid_alive(proc_pane.pid)
        assert not rotate._pid_alive(proc_claude.pid)
    finally:
        for pid in (proc_pane.pid, proc_claude.pid):
            if rotate._pid_alive(pid):
                try:
                    os.kill(pid, signal.SIGKILL)
                except OSError:
                    pass


def test_reap_chain_refuses_own_pid(_fix, tmp_path):
    """A chain containing the caller's own pid leaves that entry untouched
    (the live predecessor chain is reaped externally by PID — named residue)
    while a stand-in sleep sibling in the same chain is reaped."""
    proc = subprocess.Popen(["sleep", "1000"])
    try:
        out = rotate._reap_chain([os.getpid(), proc.pid])
        # deepest-first: the stand-in sleep (deep) is reaped first, the
        # caller's own pid (shallow) is refused and never touched.
        assert out["chain"][0]["pid"] == proc.pid
        assert out["chain"][0]["gone_after"] is True
        own = out["chain"][1]
        assert own["pid"] == os.getpid()
        assert own["termd"] is False
        assert "refused" in own["note"]
    finally:
        if rotate._pid_alive(proc.pid):
            os.kill(proc.pid, signal.SIGKILL)


def test_rotate_self_kills_window_by_id_full_flow(_fix, tmp_path,
                                                  monkeypatch):
    """The full rotate-self call kills the predecessor window BY its @id: the
    window-path line `@5 adv-alive.gen1` (the renamed own window) is dropped,
    the successor's plain-name line survives."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    # the renamed own window carries its @id (s2 capture); the successor is
    # the plain name below it.
    win.write_text("@5 adv-alive.gen1\nadv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):            # successor appears under the plain name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                                         "answer": "continue"})
    proc = subprocess.Popen(["sleep", "1000"])
    try:
        args = _rs_args(tmp_path, window_path=str(win), timeout=5,
                        session_ref="abc", own_chain=[str(proc.pid)])
        rc = rotate.cmd_rotate_self(args, tmp_path)
        assert rc == 0
        after = win.read_text(encoding="utf-8")
        assert "adv-alive.gen1" not in after      # own window reaped by @id
        assert "adv-alive" in after               # successor survives
        assert not rotate._pid_alive(proc.pid)    # chain reap happened
        rec = _latest_record(tmp_path, "adv-alive")
        assert "livestream_repoint" in rec["handover"]
        assert "bootstrap" in rec["handover"]
    finally:
        if rotate._pid_alive(proc.pid):
            os.kill(proc.pid, signal.SIGKILL)


# ── (s13) no shipped template/brief step is algorithmic ───────────────────

_BRIEFS = Path(__file__).resolve().parents[3] / "extensions" / "agi" / "briefs"

# The manual imperative phrasings rotate-self now EXECUTES; a shipped
# successor brief must contain NONE of them (the ack continue/diff line is the
# one decision-boundary instruction left).
MANUAL_ALGO_MARKERS = [
    "Invoke the `agi` skill",      # skill
    "Read HANDOFF.md",             # read handoff
    "commands.py run verify-suite",  # verify-suite
    "verify-suite",
    "session_ref on every rotation",  # row write (rotate-self's now)
    "--own-pid",
    "--session-ref",
]

# rotate-self's algorithm step names (the shipped template `steps`). None of
# these may be a manual instruction a successor is told to run.
ALGO_STEP_NAMES = {
    "handoff", "spawn", "join", "authority", "release", "button-down",
    "bootstrap", "reap", "belam-cap", "rename", "readback", "record",
    "kill",
}


def test_prime_brief_has_zero_algorithmic_steps():
    """(g/s13) the prime brief's algorithmic steps are gone — skill, read
    handoff, verify-suite, the row-write imperative, and the removed CLI flags
    — while the ack line (a decision boundary) is the one instruction left."""
    txt = (_BRIEFS / "prime-director-successor.md").read_text(encoding="utf-8")
    for marker in MANUAL_ALGO_MARKERS:
        assert marker not in txt, \
            f"algorithmic step still in the prime brief: {marker!r}"
    assert "rotate.py ack" in txt   # the ack (decision boundary) is kept


def test_shipped_template_steps_are_algorithm_not_manual():
    """(g/s13) the shipped rotations.geometry.md template `steps` are exactly
    rotate-self's algorithm names, and none of them collides with a manual
    step token (skill/ack/verify/pin/row/dm/model) a successor would be told
    to run itself."""
    txt = (_BRIEFS / "rotations.geometry.md").read_text(encoding="utf-8")
    manual = {"skill", "ack", "verify", "pin", "row", "dm", "model",
              "meter", "read-handoff"}
    for name, stepstr in re.findall(r"(\w+):\s*\{?[^}]*?steps: \[([^\]]*)\]",
                                    txt, re.S):
        steps = {s.strip().strip("'") for s in stepstr.split(",") if s.strip()}
        assert steps, f"template {name!r} has no steps"
        assert steps <= ALGO_STEP_NAMES, \
            f"template {name!r} has a non-algorithm step: {steps - ALGO_STEP_NAMES}"
        assert not (steps & manual), \
            f"template {name!r} steps collide with manual steps: {steps & manual}"


# ── (s9/s10/s11) the record carries the tail observables ──────────────────


def test_rotate_self_tail_writes_bootstrap_and_repoint(_fix, tmp_path,
                                                       monkeypatch):
    """s9/s10/s11 land in the rotation record's handover and the bootstrap file
    exists, on a fixture: live repoint SKIPPED (no live view), bootstrap
    carries telemetry + a fixture-skipped verification (never real
    verification.py against a fake root)."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    transcript = tmp_path / "succ.jsonl"
    transcript.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                                         "answer": "continue"})
    args = _rs_args(tmp_path, window_path=str(ft.win), timeout=5,
                    session_ref="abc", successor_transcript=str(transcript))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    h = rec["handover"]
    # s9: live repoint is SKIPPED on a fixture (no view seam) — named, not a
    #     silent absence.
    assert h["livestream_repoint"]["skipped"]
    assert "view-adv-alive" in h["livestream_repoint"]["session"]
    # s10: the bootstrap file exists with the template telemetry.
    bp = tmp_path / "sessions" / "seats" / "adv-alive.bootstrap.json"
    assert bp.exists()
    doc = json.loads(bp.read_text(encoding="utf-8"))
    assert set(doc["telemetry"]) >= {"seed", "model", "ack"}
    # the record names the written bootstrap path.
    assert "bootstrap.json" in str(h["bootstrap"])
    # s11: on a fixture the verification is SKIPPED (no graph), never run.
    assert "SKIPPED" in doc["verification"]["skipped"]
    assert doc["verification"]["ok"] is False