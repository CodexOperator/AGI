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
    # (c) L4.281 — throwaway derive seam BY DEFAULT: `_derive_own_chain` is a
    # DEAD-END ([]) unless a test deliberately overrides it for its own chain.
    # A probe that would climb from $TMUX_PANE up into its own host shell gets
    # nothing to TERM, so no fixture can reach a live pane (the original
    # defect reaped the host prime, belam.log 58240-58290).
    monkeypatch.setattr(rotate, "_derive_own_chain", lambda pane_pid: [])
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
    a value rotate-self cannot derive is a NAMED `SKIPPED: <reason>`, never
    the old blanket `0b owns deriving <name>` (0b ADDENDUM kid 2 replaced it
    with per-fact derivation). On a fixture with no seats row and no repo,
    every fact resolves to a NAMED skip or stays unstamped."""
    path = rotate._write_bootstrap(
        tmp_path, seat="adv-alive", generation=1,
        telemetry=["seed", "model", "worktree"],
        verification={"ok": True, "level": "quick", "count": 7})
    p = tmp_path / "sessions" / "seats" / "adv-alive.bootstrap.json"
    assert str(p) == path
    doc = json.loads(p.read_text(encoding="utf-8"))
    assert doc["shape"] == "v1"
    assert doc["generation"] == 1
    assert doc["verification"]["count"] == 7
    # no blanket skip anywhere: every SKIPPED names its reason.
    for key, val in doc["telemetry"].items():
        if val.startswith("SKIPPED:"):
            assert "0b owns" not in val, val
            assert len(val) > len("SKIPPED:")
    # no repo => nothing was measured_at-stamped.
    assert doc["measured_at"] == {}
    assert doc["commit"] is None


def test_bootstrap_derives_real_facts_stamped_at_head(_fix, tmp_path,
                                                      monkeypatch):
    """0b kid 2: with a config:seats row and a git HEAD, _write_bootstrap
    derives the seat-row facts for real and stamps each in measured_at with
    the commit — never a skip for a fact the handover CAN see."""
    _write_seats_sheet(tmp_path, [
        {"name": "adv-alive", "seed": "s-7", "model": "claude-sonnet-5",
         "effort": "max", "window": "@5", "worktree": "/wt/adv",
         "ack": "continue", "prev_gen": 0},
    ])
    monkeypatch.setattr(rotate, "_git_head", lambda *a, **k: "7cff1aa")
    path = rotate._write_bootstrap(
        tmp_path, seat="adv-alive", generation=1,
        telemetry=["seed", "model", "effort", "window", "worktree",
                   "ack", "prev_gen"],
        verification={"ok": True, "level": "quick", "count": 7})
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    assert doc["shape"] == "v1"
    assert doc["commit"] == "7cff1aa"
    assert doc["telemetry"]["seed"] == "s-7"
    assert doc["telemetry"]["model"] == "claude-sonnet-5"
    assert doc["telemetry"]["prev_gen"] == "0"
    assert doc["telemetry"]["seat_row"].startswith("HEAD@7cff1aa:")
    # join-only / sibling facts are named SKIPPED, present by default.
    assert doc["telemetry"]["successor_live_model"].startswith("SKIPPED:")
    assert "join" in doc["telemetry"]["successor_live_model"]
    assert doc["telemetry"]["mail"].startswith("SKIPPED:")
    # every derived fact is stamped at HEAD.
    for fact in ("seed", "model", "effort", "window", "worktree", "ack",
                 "prev_gen", "seat_row", "verification"):
        assert doc["measured_at"][fact] == "7cff1aa", fact
    # SKIPPED facts are NOT stamped.
    assert "successor_live_model" not in doc["measured_at"]


def test_bootstrap_staleness_refuses_stale_accepts_fresh(_fix):
    """0b kid 2: _bootstrap_stale refuses a record whose measured fact is at
    an older commit than HEAD (the staleness bound the hook enforces), and
    accepts a fresh one; it also accepts a permanent fact at an older commit
    and a record with nothing measured."""
    fresh = {"shape": "v1", "commit": "abc1234",
             "measured_at": {"seed": "abc1234", "model": "abc1234",
                              "verification": "abc1234"}}
    assert rotate._bootstrap_stale(fresh, "abc1234") is False
    stale = {"shape": "v1", "commit": "abc1234",
             "measured_at": {"seed": "abc1234", "model": "deadbeef"}}
    assert rotate._bootstrap_stale(stale, "abc1234") is True
    # default bound is 'head': a fresh model at deadbeef is refused.
    assert rotate._bootstrap_stale(stale, "abc1234") is True
    # a permanent-bound fact (seed) never goes stale; model is still 'head'.
    assert rotate._bootstrap_stale(
        stale, "abc1234", {"seed": "permanent"}) is True
    # when the ONLY stale fact is permanent-bound, the record stays fresh.
    stale_perm = {"shape": "v1", "commit": "abc1234",
                  "measured_at": {"seed": "deadbeef", "model": "abc1234"}}
    assert rotate._bootstrap_stale(
        stale_perm, "abc1234", {"seed": "permanent"}) is False
    # a fully-skipped doc (nothing measured) is never stale.
    assert rotate._bootstrap_stale({"shape": "v1", "measured_at": {}},
                                   "abc1234") is False


def _write_rotations_with_fact_bounds(root, fact_bounds):
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:rotations\ntype: config\nfact_bounds:\n"
    for k, v in fact_bounds.items():
        body += f"  {k}: {v}\n"
    body += "---\n\nbody\n"
    (g / "rotations.md").write_text(body, encoding="utf-8")


def _write_record(root, measured_at, telemetry):
    seats = root / "sessions" / "seats"
    seats.mkdir(parents=True, exist_ok=True)
    doc = {"shape": "v1", "generation": 7,
           "measured_at": measured_at, "telemetry": telemetry}
    (seats / "adv-alive.bootstrap.json").write_text(
        json.dumps(doc) + "\n", encoding="utf-8")


# (L4.290) per-fact staleness: `fact_bounds` has a reader — the block marks
# only head-bound facts, never refuses the whole block, reads the map from the
# node when no `bounds` kwarg is passed.
def test_bootstrap_permanent_fact_at_old_commit_emits_plain(_fix, tmp_path):
    """A permanent-bound fact measured at an old commit is emitted with NO
    stale mark (and does not refuse the block)."""
    _write_rotations_with_fact_bounds(tmp_path, {"model": "permanent"})
    _write_record(tmp_path, {"model": "deadbeef"},
                  {"model": "claude-sonnet-5"})
    block, reason = rotate._bootstrap_block(
        tmp_path, "adv-alive", commit="abc1234")
    assert reason is None
    assert "[stale:" not in block
    assert "model: claude-sonnet-5" in block


def test_bootstrap_head_fact_at_old_commit_emits_stale_mark(_fix, tmp_path):
    """A head-bound fact measured at an old commit is emitted with the
    `[stale: measured@<sha>, HEAD@<sha>]` mark."""
    _write_rotations_with_fact_bounds(tmp_path, {"model": "head"})
    _write_record(tmp_path, {"model": "deadbeef"}, {"model": "x"})
    block, reason = rotate._bootstrap_block(
        tmp_path, "adv-alive", commit="abc1234")
    assert reason is None
    assert "[stale: measured@deadbeef, HEAD@abc1234]" in block


def test_bootstrap_unbounded_fact_is_treated_as_head(_fix, tmp_path):
    """An unbounded fact (not in the map) takes the declared default 'head'
    and is marked stale at an old commit."""
    _write_rotations_with_fact_bounds(tmp_path, {"model": "permanent"})
    _write_record(tmp_path, {"seed": "deadbeef"}, {"seed": "s-7"})
    block, reason = rotate._bootstrap_block(
        tmp_path, "adv-alive", commit="abc1234")
    assert reason is None
    assert "seed: s-7  [stale: measured@deadbeef, HEAD@abc1234]" in block


def test_bootstrap_every_fact_stale_still_emits(_fix, tmp_path):
    """A record with EVERY measured fact stale still emits — staleness is a
    per-fact mark, never a whole-block refusal."""
    _write_rotations_with_fact_bounds(tmp_path, {})
    _write_record(tmp_path, {"seed": "deadbeef", "model": "cafebabe"},
                  {"seed": "s-7", "model": "x"})
    block, reason = rotate._bootstrap_block(
        tmp_path, "adv-alive", commit="abc1234")
    assert reason is None
    assert "## ⚓ bootstrap: adv-alive successor handover" in block
    assert "[stale:" in block


def test_bootstrap_bounds_kwarg_overrides_node(_fix, tmp_path):
    """The `bounds=` kwarg overrides the node's `fact_bounds` — the seam a
    test/other reader can pin an explicit map against."""
    _write_rotations_with_fact_bounds(tmp_path, {"model": "head"})
    _write_record(tmp_path, {"model": "deadbeef"}, {"model": "x"})
    block, _ = rotate._bootstrap_block(
        tmp_path, "adv-alive", commit="abc1234",
        bounds={"model": "permanent"})
    assert "[stale:" not in block


def test_fact_bounds_absent_key_returns_empty(_fix, tmp_path):
    """`_fact_bounds` on a node without the key (or without the node) returns
    {}"""
    assert rotate._fact_bounds(tmp_path) == {}
    _write_rotations_with_fact_bounds(tmp_path, {"model": "permanent"})
    assert rotate._fact_bounds(tmp_path) == {"model": "permanent"}
    # malformed (non-dict) -> {}
    g = tmp_path / "nodes" / ".geometry"
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\nfact_bounds: nope\n---\n\n",
        encoding="utf-8")
    assert rotate._fact_bounds(tmp_path) == {}


def test_live_rotations_declares_permanent_model():
    """The LIVE config:rotations declares `fact_bounds` with model:
    permanent — a test of live config reads the live node, never a copy."""
    # reuse rotate's own resolver to locate the graph, so the test reads the
    # same bytes the engine reads (no `_fix` fixture: it mocks
    # find_project_root to a tmp dir).
    root = rotate.find_project_root()
    fb = rotate._fact_bounds(root)
    assert fb.get("model") == "permanent"


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


# ── L4.281: rotate-self under pytest never reaps the host prime ────────────


def test_rotate_self_refuses_derived_reap_when_pytest_without_seam(
        _fix, tmp_path, monkeypatch):
    """(a) — under PYTEST_CURRENT_TEST with NO --own-chain seam the own-chain
    reap is REFUSED by name and a derived chain is NEVER TERM'd: a probe
    running inside the pytest runtime must not reach a live pane (the
    original defect reaped the host prime, belam.log 58240-58290)."""
    probe = subprocess.Popen(["sleep", "1000"])
    try:
        _write_seats_sheet(tmp_path,
                           [{"name": "adv-alive", "role": "parent",
                             "model": "x", "effort": "max", "settings": "",
                             "pid": probe.pid}])
        ft = _FakeTmux(tmp_path, initial=["adv-alive"])
        monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
        monkeypatch.setattr(rotate, "_read_ack",
                            lambda *a, **k: {"seat": "adv-alive",
                                             "gen_after": 1,
                                             "answer": "continue"})
        # even a PERFECT derive (the probe IS the would-be host) must not TERM
        # under pytest without a seam.
        monkeypatch.setattr(rotate, "_derive_own_chain",
                            lambda pane_pid: [probe.pid])
        args = _rs_args(tmp_path, window_path=str(ft.win), timeout=5,
                        session_ref="abc")
        rc = rotate.cmd_rotate_self(args, tmp_path)
        assert rc == 0
        rec = _latest_record(tmp_path, "adv-alive")
        s12 = rec["s12_self_reap"]
        src = s12["reap_source"]
        assert "REFUSED" in src
        assert "PYTEST_CURRENT_TEST" in src
        assert "no --own-chain seam" in src
        assert rotate._pid_alive(probe.pid)   # the probe was never TERM'd
    finally:
        if rotate._pid_alive(probe.pid):
            os.kill(probe.pid, signal.SIGKILL)


def test_rotate_self_derived_reap_skips_row_without_pid(
        _fix, tmp_path, monkeypatch):
    """(b) — a DERIVED chain is SKIPPED when the seat ROW carries no pid: a
    row that cannot name its own process never authorizes a reap. NAMED in
    the record and on stdout."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent", "model": "x",
                         "effort": "max", "settings": ""}])  # no pid
    ft = _FakeTmux(tmp_path, initial=["adv-alive"])
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                                         "answer": "continue"})
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)  # prod path
    monkeypatch.setenv("TMUX_PANE", "%test")
    monkeypatch.setattr(rotate, "_pane_pid", lambda pane: 9999)
    chain = [1234, 5678]
    monkeypatch.setattr(rotate, "_derive_own_chain", lambda pane_pid: chain)
    args = _rs_args(tmp_path, window_path=str(ft.win), timeout=5,
                    session_ref="abc")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    rec = _latest_record(tmp_path, "adv-alive")
    s12 = rec["s12_self_reap"]
    src = s12["reap_source"]
    assert "SKIPPED" in src and "no pid" in src
    assert s12.get("skipped")


def test_rotate_self_derived_reap_skips_row_pid_mismatch(
        _fix, tmp_path, monkeypatch):
    """(b) — a DERIVED chain is SKIPPED when the seat ROW's pid is not in it:
    a row that does not own the chain cannot reap it. NAMED in the record."""
    probe = subprocess.Popen(["sleep", "1000"])
    try:
        row_pid = probe.pid + 12345          # a pid NOT in the derived chain
        _write_seats_sheet(tmp_path,
                           [{"name": "adv-alive", "role": "parent",
                             "model": "x", "effort": "max", "settings": "",
                             "pid": row_pid}])
        ft = _FakeTmux(tmp_path, initial=["adv-alive"])
        monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
        monkeypatch.setattr(rotate, "_read_ack",
                            lambda *a, **k: {"seat": "adv-alive",
                                             "gen_after": 1,
                                             "answer": "continue"})
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setenv("TMUX_PANE", "%test")
        monkeypatch.setattr(rotate, "_pane_pid", lambda pane: 9999)
        monkeypatch.setattr(rotate, "_derive_own_chain",
                            lambda pane_pid: [probe.pid])  # row pid NOT here
        args = _rs_args(tmp_path, window_path=str(ft.win), timeout=5,
                        session_ref="abc")
        rc = rotate.cmd_rotate_self(args, tmp_path)
        assert rc == 0
        rec = _latest_record(tmp_path, "adv-alive")
        s12 = rec["s12_self_reap"]
        src = s12["reap_source"]
        assert "SKIPPED" in src
        assert str(row_pid) in src
        assert "not in the derived chain" in src
        assert rotate._pid_alive(probe.pid)   # the chain was never TERM'd
    finally:
        if rotate._pid_alive(probe.pid):
            os.kill(probe.pid, signal.SIGKILL)


def test_rotate_self_derived_reap_runs_when_row_pid_in_chain(
        _fix, tmp_path, monkeypatch):
    """(d) — the production path is UNCHANGED when the seat ROW's pid IS in
    the derived chain and pytest is absent: the chain is TERM'd deepest-first.
    The L4.281 guard does not pinch the real rotation."""
    probe = subprocess.Popen(["sleep", "1000"])
    try:
        _write_seats_sheet(tmp_path,
                           [{"name": "adv-alive", "role": "parent",
                             "model": "x", "effort": "max", "settings": "",
                             "pid": probe.pid}])
        ft = _FakeTmux(tmp_path, initial=["adv-alive"])
        monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
        monkeypatch.setattr(rotate, "_read_ack",
                            lambda *a, **k: {"seat": "adv-alive",
                                             "gen_after": 1,
                                             "answer": "continue"})
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setenv("TMUX_PANE", "%test")
        monkeypatch.setattr(rotate, "_pane_pid", lambda pane: 9999)
        monkeypatch.setattr(rotate, "_derive_own_chain",
                            lambda pane_pid: [probe.pid])
        args = _rs_args(tmp_path, window_path=str(ft.win), timeout=5,
                        session_ref="abc")
        rc = rotate.cmd_rotate_self(args, tmp_path)
        assert rc == 0
        rec = _latest_record(tmp_path, "adv-alive")
        s12 = rec["s12_self_reap"]
        src = s12["reap_source"]
        assert "derived from" in src
        assert str(probe.pid) in src
        assert not rotate._pid_alive(probe.pid)   # chain WAS reaped (prod path)
    finally:
        if rotate._pid_alive(probe.pid):
            os.kill(probe.pid, signal.SIGKILL)


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