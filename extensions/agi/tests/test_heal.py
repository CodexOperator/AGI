"""Tests for bin/heal.py's healer spawn.

Healing only runs when something has already gone wrong, which is exactly why
its defects survive: nobody watches the path that only fires on a bad day.
Both assertions below cover a bug that was live and silent until 2026-08-31 —
an unknown pi flag that killed every healer at birth (and exited 0 doing it),
and a Popen with no `env=` that billed the Claude Code subscription.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, BIN / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


heal = _load("agi_heal", "heal.py")
dispatch = _load("agi_dispatch_for_heal", "dispatch.py")


def make_project(repo: Path, **agent_dispatch) -> Path:
    graph = repo / ".agi"
    (graph / "nodes").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage", "agent_dispatch": agent_dispatch}))
    return graph


# --- the flag that killed every healer -------------------------------------

def test_healer_passes_no_unknown_max_turns_flag():
    """pi has no `--max-turns`. It printed `Unknown option: --max-turns` and
    exited 0, so the loop recorded a healer as launched that had never read its
    own context."""
    source = (BIN / "heal.py").read_text()
    spawn = source.split("pi_args = [", 1)[1].split("]", 1)[0]
    assert "--max-turns" not in spawn


def test_healer_spawn_scrubs_the_environment():
    """dispatch.py's scrub exists so pi children cannot bill the interactive
    Claude Code subscription. The healer sat outside it."""
    source = (BIN / "heal.py").read_text()
    assert "env=_scrubbed_env()" in source
    assert "ANTHROPIC_API_KEY" not in heal._scrubbed_env()


def test_scrub_agrees_with_the_one_dispatch_uses():
    """Same rule, not a second copy of it — heal.py imports the function."""
    assert heal._scrubbed_env() == dispatch.scrubbed_env()


# --- model resolution ------------------------------------------------------

def test_healer_uses_the_projects_configured_model(tmp_path):
    graph = make_project(tmp_path, provider="openrouter",
                         model="z-ai/glm-5.3-flash", thinking="medium")
    args = heal._pi_model_args(graph)
    assert args == ["--provider", "openrouter",
                    "--model", "z-ai/glm-5.3-flash",
                    "--thinking", "medium"]


def test_healer_falls_back_to_pi_defaults_when_unconfigured(tmp_path):
    graph = make_project(tmp_path)
    assert heal._pi_model_args(graph) == []


@pytest.mark.parametrize("broken", ["not json at all", '{"agent_dispatch": 3}'])
def test_broken_config_costs_the_preference_not_the_healer(broken, tmp_path):
    """Healing runs when things are already broken. A malformed config must
    lose the healer its model preference, never its existence."""
    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text(broken)
    assert heal._pi_model_args(graph) == []


def test_missing_project_returns_no_args(tmp_path):
    assert heal._pi_model_args(tmp_path / "nowhere") == []


# --- hypothesis:l3-branch-isolation-partial-break --------------------------
# A healer's cwd decides which tree its source edits touch. For a `--branch`
# spawn the record carries the agent's own worktree; the healer must re-enter
# it, not the main checkout.

def test_healer_cwd_reenters_the_branch_worktree(tmp_path):
    main_graph = tmp_path / "main" / ".agi"
    main_graph.mkdir(parents=True)
    wt = main_graph / "worktrees" / "a00-x"
    wt.mkdir(parents=True)
    rec = {"worktree": str(wt)}
    assert heal._heal_cwd(main_graph, rec).resolve() == wt.resolve()


def test_healer_cwd_falls_back_to_root_without_a_worktree(tmp_path):
    graph = tmp_path / ".agi"
    graph.mkdir(parents=True)
    assert heal._heal_cwd(graph, {}) == graph


def test_healer_cwd_ignores_a_gone_worktree(tmp_path):
    graph = tmp_path / ".agi"
    graph.mkdir(parents=True)
    rec = {"worktree": str(graph / "worktrees" / "a00-gone")}
    # Not on disk (dropped) → healers fall back to the resolved root rather
    # than spawning into a directory that does not exist.
    assert heal._heal_cwd(graph, rec) == graph

def test_healer_spawn_sets_cwd_from_worktree_record(tmp_path):
    """The Popen on the healer path must route cwd through `_heal_cwd`, not
    a re-entry of the caller's root."""
    source = (BIN / "heal.py").read_text()
    assert "cwd=str(heal_root)" in source, (
        "healer Popen must use the worktree-aware heal_root")
    assert "_heal_cwd(root, rec)" in source


# --- ladder is the ONE source (hypothesis:l4-a-model-change-is-one-write) ---

def _make_ladder_project(repo: Path, parent_model: str) -> Path:
    graph = repo / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "~deepseek/deepseek-v4-flash-latest",
                       "parent": "~z-ai/glm-flash-latest"},
            "allowed_extra": ["~z-ai/glm-flash-latest"]}},
        "agent_dispatch": {"model": "~z-ai/glm-flash-latest"}}))
    ladder = (graph / "nodes" / ".geometry" / "ladder.md")
    ladder.write_text(f"""---
current_season: 2
roles:
  - {{"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}}
  - {{"tier": 1, "role": "parent", "harness": "pi", "model": "{parent_model}", "effort": "", "settings": ""}}
---

fixture
""")
    return graph


def test_heal_resolves_the_ladder_row_model_for_the_healed_role(tmp_path):
    """A healed parent re-spawns with the LADDER row's model (the one source),
    not the config's allowed/legacy values — so the same one write on the
    ladder that changed the live spawn changes what a re-spawn uses."""
    graph = _make_ladder_project(tmp_path, "deepseek/deepseek-v4.1-flash")
    args = heal._pi_model_args(graph, "parent", "parent")
    assert "--model" in args
    assert args[args.index("--model") + 1] == "deepseek/deepseek-v4.1-flash"


def test_heal_without_a_ladder_still_uses_config(tmp_path):
    """No ladder file -> the historical config path still answers (missing
    ladder never blocks)."""
    graph = make_project(tmp_path, provider="openrouter",
                         model="z-ai/glm-5.3-flash")
    args = heal._pi_model_args(graph, "parent", "parent")
    assert "--model" in args
    assert args[args.index("--model") + 1] == "z-ai/glm-5.3-flash"


# --- hyp:l4-a-suspend-killed-round-comes-home-stalled-with-a-dead-pid- ----
# resolves-like-a-dead-running-record (claim b): the SECOND live admission
# point -- `_main_heal`'s per-agent block, the loop driver.sh runs as
# `heal.py <root> <iter_n>`. Even with the dispatch fix live, a `stalled`
# record found by THIS loop used to die at the `status != "running"` guard
# (L183 pre-fix) and never resolve. These tests drive the REAL `_main_heal`
# path, not a copy of its block.


def _stalled_round(tmp_path: Path, pid: int) -> tuple[Path, Path]:
    """A tmp graph with one round carrying a single `stalled` agent whose
    pid is `pid`. Returns `(root, agent_json_path)`."""
    root = tmp_path
    graph = root / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    iter_dir = graph / "sessions" / "iter-001"
    (iter_dir / "a00-s").mkdir(parents=True, exist_ok=True)
    (iter_dir / "manifest.json").write_text(json.dumps({
        "iter": 1,
        "timeout_seconds": 600,
        "agents": [{"id": "a00-s", "status": "running"}],
    }, indent=2))
    aj = iter_dir / "a00-s" / "agent.json"
    aj.write_text(json.dumps({
        "id": "a00-s",
        "status": "stalled",
        "pid": pid,
        "started_at": int(time.time()) - 100,
        "node_id": "hypothesis:h1",
    }, indent=2))
    return root, aj, iter_dir / "manifest.json"


# the real dispatch module heal's `_reap_one` closes over, so patching on it
# is the ONLY patch that reaches the resolution rule heal actually calls.
import dispatch as real_dispatch  # noqa: E402 -- cached module heal imported


def test_heal_resolves_stalled_dead_pid_to_failed(monkeypatch, tmp_path):
    """A `stalled` record with a PROVABLY dead pid reaches the dead-pid path
    in `_main_heal` and resolves through dispatch._reap_one to `failed` with
    the stall named (no completion, no branch advance -> never restarted),
    and the manifest mirrors it."""
    root, aj, mp = _stalled_round(tmp_path, 999999)
    monkeypatch.setattr(heal, "_pid_alive", lambda pid: False)
    monkeypatch.setattr(sys, "argv", ["heal.py", str(root), "1"])
    assert heal.main() == 0  # resolved THIS pass -> all terminal
    rec = json.loads(aj.read_text(encoding="utf-8"))
    assert rec["status"] == "failed"
    assert "stalled" in rec["fail_reason"]
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    assert manifest["agents"][0]["status"] == "failed"


def test_heal_resolves_stalled_dead_to_done_unreported_on_branch_advance(
        monkeypatch, tmp_path):
    """Same admission, but the work landed: when the round branch advanced,
    dispatch._reap_one still resolves the stalled-dead record to
    `done-unreported` (never restarted)."""
    root, aj, mp = _stalled_round(tmp_path, 999999)
    monkeypatch.setattr(heal, "_pid_alive", lambda pid: False)
    monkeypatch.setattr(real_dispatch, "_branch_has_done_commit",
                        lambda root, rec, agent_id: True)
    monkeypatch.setattr(sys, "argv", ["heal.py", str(root), "1"])
    assert heal.main() == 0
    rec = json.loads(aj.read_text(encoding="utf-8"))
    assert rec["status"] == "done-unreported"
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    assert manifest["agents"][0]["status"] == "done-unreported"


def test_heal_leaves_a_live_pid_stalled_record_untouched(monkeypatch, tmp_path):
    """A `stalled` record whose pid is LIVE is NOT terminal: one pass leaves
    it untouched (status stalled, no fail_reason, no finished_at), all_terminal
    is False, and `_main_heal` returns the NAMED non-zero `NOT_TERMINAL_YET`
    code instead of sleeping toward the 30-min deadline. Clock and sleep are
    seam-injected, so the pass is bounded and no real sleep happens."""
    root, aj, mp = _stalled_round(tmp_path, 987654)
    monkeypatch.setattr(heal, "_pid_alive", lambda pid: True)
    slept: list = []
    monkeypatch.setattr(heal, "_sleep", lambda s: slept.append(s))
    monkeypatch.setattr(heal, "_now", lambda: 0.0)
    monkeypatch.setattr(sys, "argv", ["heal.py", str(root), "1"])
    t0 = time.monotonic()
    rc = heal.main()
    assert time.monotonic() - t0 < 1.0
    assert rc == heal.NOT_TERMINAL_YET
    assert rc != 0
    assert slept == []  # returned after one pass; never polled
    rec = json.loads(aj.read_text(encoding="utf-8"))
    assert rec["status"] == "stalled"
    assert "fail_reason" not in rec
    assert "finished_at" not in rec
    assert json.loads(mp.read_text(encoding="utf-8"))["agents"][0]["status"] \
        == "stalled"


def test_healer_pi_bin_resolves_through_the_shared_resolver(tmp_path, monkeypatch):
    """The healer's pi binary goes through `adapters.resolve_bin` (the ONE
    resolver every spawn site uses), never a stored `/home/<user>` literal
    (goal:g15.29.2)."""
    graph = make_project(tmp_path)
    seen = {}

    def fake(h, env_var, default):
        seen.update(env=env_var, raw=default)
        return "/resolved/pi"

    monkeypatch.setattr(heal.adapters, "resolve_bin", fake)
    assert heal._pi_bin(graph) == "/resolved/pi"
    assert seen["env"] == "PI_BIN"
    assert seen["raw"] == "pi"


# --- the log-tail guard + the stale-lock skip (TMM.262 residues 8+10) ------
#
# Both guards fire on a BAD day only (a dead seat, a gone worktree), so both
# survived untested. `heal-worktree-refusal-tests-never-reach-live-tmux-and-
# dead-branches-go` gives each its own row.

WT_ROW = {"name": "wt", "role": "director", "pid": 424242, "window": "@50",
          "worktree": ".agi/worktrees/seat-wt"}


def _wt_graph(tmp_path: Path, *, worktree: bool) -> tuple[Path, Path]:
    """A worktree-shaped graph root; `worktree=False` is it after the
    worktree dir is pruned (what a dead seat leaves behind)."""
    gdir = make_project(tmp_path)
    wt = gdir / "worktrees" / "seat-wt" / ".agi"
    if worktree:
        (wt / "sessions").mkdir(parents=True, exist_ok=True)
    return gdir, wt


def test_log_tail_falls_back_to_main_when_the_worktree_log_is_gone(
        tmp_path, monkeypatch):
    """THE LOG-TAIL GUARD: a row claiming a worktree whose `.agi` is GONE
    resolves no own log, so the tail must come from MAIN's copy — not be
    ''. An empty tail classifies the death wrong (every dead seat reads as
    'no evidence'), which is the day this path exists for."""
    import rotate
    gdir, _ = _wt_graph(tmp_path, worktree=False)
    (gdir / "sessions").mkdir(parents=True, exist_ok=True)
    (gdir / "sessions" / "wt.log").write_text("MAIN-COPY", encoding="utf-8")
    assert heal._read_seat_log_tail(gdir, WT_ROW, rotate) == "MAIN-COPY"


class _SessionsDirSpy:
    """The candidate ORDER `_read_seat_log_tail` asks for, in-process: every
    `_sessions_dir(gdir)` call is recorded, so the row can name WHICH geometry
    was asked first; `watch_reads` records every log file the tail actually
    READS, in order — the candidate list as the code consumes it.

    It answers each geometry root with that root's OWN `<gdir>/sessions`,
    which is the contract the tail code is written against. The real
    `rotate._sessions_dir` deliberately collapses every worktree seat onto
    MAIN's shared room (hypothesis:l4-a-check-that-answers-a-question-it-is-
    not-asking), so with the real module `own` and `main` are one path here and
    the worktree-vs-MAIN preference is unobservable."""

    def __init__(self):
        self.seen: list[Path] = []
        self.reads: list[Path] = []

    def _sessions_dir(self, gdir):
        self.seen.append(Path(gdir))
        return Path(gdir) / "sessions"

    def watch_reads(self, monkeypatch) -> "_SessionsDirSpy":
        real_read = Path.read_bytes
        reads = self.reads

        def spy_read(self, *a, **kw):
            reads.append(Path(self))
            return real_read(self, *a, **kw)

        monkeypatch.setattr(Path, "read_bytes", spy_read)
        return self


def test_log_tail_prefers_own_copy_then_falls_back_to_main_exactly_once(
        tmp_path, monkeypatch):
    """THE LOG-TAIL CANDIDATE ORDER, red-first for its OWN reason: a worktree
    seat's OWN copy is read first, and MAIN's copy is the fallback of LAST
    resort once the own copy is gone. Asserting the fallback TEXT alone is not
    a gate — deleting the whole MAIN branch made DH.427's row red through an
    unrelated locations.py RuntimeError instead
    (experiment:a00-416266d2-e77f31). The `if main != own` DEDUP is NOT pinned
    here: the read loop returns at the first readable candidate, so a
    duplicated MAIN candidate is never stat-ed or read and the guard has no
    observable effect — EXCEPT on the MISS path, which
    `test_log_tail_dedups_main_against_own_when_the_seat_room_is_shared`
    pins by counting the `Path.exists` stats."""
    gdir, wt = _wt_graph(tmp_path, worktree=True)
    (gdir / "sessions").mkdir(parents=True, exist_ok=True)
    own_log = wt / "sessions" / "wt.log"
    main_log = gdir / "sessions" / "wt.log"
    main_log.write_text("MAIN-COPY", encoding="utf-8")
    own_log.write_text("OWN-COPY", encoding="utf-8")

    spy = _SessionsDirSpy().watch_reads(monkeypatch)
    assert heal._read_seat_log_tail(gdir, WT_ROW, spy) == "OWN-COPY"
    assert spy.seen[0] == wt, f"own geometry not asked first: {spy.seen}"
    assert spy.reads == [own_log], f"own copy not preferred: {spy.reads}"

    # worktree pruned: the own copy is gone, MAIN's copy answers.
    own_log.unlink()
    spy.seen.clear()
    spy.reads.clear()
    tail = heal._read_seat_log_tail(gdir, WT_ROW, spy)
    assert tail == "MAIN-COPY", (
        f"MAIN fallback copy not preferred after the worktree went: {tail!r}")
    assert spy.reads == [main_log], (
        f"MAIN copy is not the fallback of last resort: {spy.reads}")


class _SharedRoomSpy:
    """A `_rotate` stand-in that COLLAPSES every geometry root onto ONE
    shared sessions room — the contract the real `rotate._sessions_dir` has
    (all seats log into MAIN's room, hypothesis:l4-a-check-that-answers-a-
    question-it-is-not-asking). So `own` and `main` are literally the same
    Path and `if main != own:` is the only thing standing between a doubled
    candidate and a doubled stat. Every `Path.exists` call is recorded."""

    def __init__(self, room: Path):
        self.room = room
        self.stats: list[Path] = []

    def _sessions_dir(self, gdir):
        return self.room

    def watch_stats(self, monkeypatch) -> "_SharedRoomSpy":
        real_exists = Path.exists
        stats = self.stats

        def spy_exists(self, *a, **kw):
            stats.append(Path(self))
            return real_exists(self, *a, **kw)

        monkeypatch.setattr(Path, "exists", spy_exists)
        return self


def test_log_tail_dedups_main_against_own_when_the_seat_room_is_shared(
        tmp_path, monkeypatch):
    """THE `if main != own:` DEDUP, and the gate the order row could not
    build. With the real `_rotate` the worktree seat's own room and MAIN's
    room are ONE path, so `cands` is a single entry by construction; drop the
    dedup and the SAME path sits in the list twice.

    The order row cannot see this: the read loop RETURNS at the first readable
    candidate, so a duplicate is never read. The MISS path is where the
    duplicate is observable — the loop's `if p.exists()` is then reached once
    per candidate — so a missing seat log is counted, not read. Probe MUT-B in
    experiment:a00-f3548040-e4e0c8: `if main != own:` -> `if True:` makes this
    row red with 2 stats against the pinned 1. Without the dedup the tail is
    still '' (the second stat is a harmless no-op), which is exactly why
    asserting the tail alone would be a dead assertion.
    """
    gdir, _ = _wt_graph(tmp_path, worktree=True)
    room = gdir / "sessions"
    room.mkdir(parents=True, exist_ok=True)
    log = room / "wt.log"
    assert not log.exists(), "the miss path needs the log to be ABSENT"

    spy = _SharedRoomSpy(room).watch_stats(monkeypatch)
    assert heal._read_seat_log_tail(gdir, WT_ROW, spy) == ""
    monkeypatch.undo()
    assert spy.stats == [log], (
        f"the shared seat room was stat-ed more than once: {spy.stats} "
        "(a duplicate MAIN candidate; `if main != own:` did not dedup)")


def test_stale_lock_skip_leaves_a_clean_sessions_dir_alone(tmp_path,
                                                          monkeypatch,
                                                          capsys):
    """THE STALE-LOCK SKIP, as a real gate: a dead seat with NO
    verify-suite.lock under its own sessions/ must leave Path.unlink
    UNCALLED on that path and never reach the `warn: could not remove stale
    lock` branch. The no-log-line claim alone is not a gate — the unlink's
    `except OSError` swallows FileNotFoundError, so a mutating version
    produces the same log and stays green
    (experiment:a00-f76b1fde-5e44ad)."""
    gdir, wt = _wt_graph(tmp_path, worktree=True)
    lock = wt / "sessions" / "verify-suite.lock"
    log = tmp_path / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))

    real_unlink = Path.unlink
    touched: list[Path] = []

    def spy_unlink(self, *a, **kw):
        touched.append(Path(self))
        return real_unlink(self, *a, **kw)

    monkeypatch.setattr(Path, "unlink", spy_unlink)
    heal._clean_stale_layout_locks(gdir, WT_ROW)
    monkeypatch.undo()

    assert lock not in touched, f"unlink called on a lock that is not there: {touched}"
    assert not lock.exists()
    err = capsys.readouterr().err
    assert "could not remove stale lock" not in err, err
    text = log.read_text(encoding="utf-8") if log.exists() else ""
    assert "removed stale verify-suite.lock" not in text, text


def test_stale_lock_clean_reads_the_name_from_the_config_block(tmp_path,
                                                              monkeypatch):
    """heal.py resolves the stale lock through `verification.suite_lock_name`:
    a block naming `other.lock` is the file unlinked, and the default name is
    left alone (no `verify-suite.lock` literal in extensions/agi/bin)."""
    gdir, wt = _wt_graph(tmp_path, worktree=True)   # the GEOMETRY dir is wt/.agi
    (wt / "config.json").write_text(json.dumps({"values": {"core": {
        "suite_lock": {"file": "other.lock"}}}}))
    lock = wt / "sessions" / "other.lock"
    lock.write_text("1", encoding="utf-8")
    default = wt / "sessions" / "verify-suite.lock"
    default.write_text("1", encoding="utf-8")      # the default name: left alone
    monkeypatch.setenv("AGI_REAPER_LOG", str(tmp_path / "reaper.log"))
    heal._clean_stale_layout_locks(gdir, WT_ROW)
    assert not lock.exists()
    assert default.exists()


def test_stale_lock_clean_never_raises_on_a_pruned_worktree_geometry(
        tmp_path, monkeypatch, capsys):
    """THE DEFENSIVE `gdir is None` ARM, as a real gate: `_seat_geometry_dir`
    REFUSES a row whose worktree `.agi` is gone (None is a refusal, never a
    fallback to MAIN), so a direct call on such a row must return without
    raising and touch nothing. `_clean_stale_layout_locks` is module-level and
    its docstring promises "best-effort, never raises"; with the arm deleted
    the body did `None / "sessions"` and raised TypeError
    (DIRECTOR RULING DH.449, restoring the DH.436 deletion)."""
    gdir, wt = _wt_graph(tmp_path, worktree=False)

    # (b) SCOPE, and NOT a restatement of the unlink spy below: a REAL
    # sibling seat's REAL planted lock under a REAL geometry dir must
    # SURVIVE this call. The `gdir is None` arm is a refusal for THIS
    # row's geometry, never a sweep over the room; the old closing
    # assertion (`not (gdir/"sessions"/"verify-suite.lock").exists()`)
    # was VACUOUS -- nothing ever created that file, so it was true of any
    # code at all. Delete the arm and this row dies red on the `None /`
    # TypeError; widen the arm into a sweep and it is red on the message.
    sib = gdir / "worktrees" / "seat-sibling" / ".agi" / "sessions"
    sib.mkdir(parents=True, exist_ok=True)
    sib_lock = sib / "verify-suite.lock"
    sib_lock.write_text("LIVE-SIBLING-SEAT", encoding="utf-8")

    log = tmp_path / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))

    real_unlink = Path.unlink
    touched: list[Path] = []

    def spy_unlink(self, *a, **kw):
        touched.append(Path(self))
        return real_unlink(self, *a, **kw)

    monkeypatch.setattr(Path, "unlink", spy_unlink)
    try:
        heal._clean_stale_layout_locks(gdir, WT_ROW)  # must not raise
    finally:
        monkeypatch.undo()

    assert not touched, f"touched something on a refusal: {touched}"
    assert sib_lock.exists(), (
        f"the refusal swept a sibling seat's REAL lock away: {sib_lock}")
    assert sib_lock.read_text(encoding="utf-8") == "LIVE-SIBLING-SEAT"
    err = capsys.readouterr().err
    assert "could not remove stale lock" not in err, err
    text = log.read_text(encoding="utf-8") if log.exists() else ""
    assert "removed stale verify-suite.lock" not in text, text
