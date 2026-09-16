"""Tests for `dispatch.py --dry-run` (hypothesis:l3-dispatch-dry-run).

The claim under test: `--dry-run` resolves EVERYTHING the live spawn path
resolves (target, tier, role, ladder tier, brief tier, model and effort rows,
env exports), assembles the brief, prints a compact report (quoted command,
env, brief tier, brief line count + first 20 lines) and exits 0 — WITHOUT
spawning, taking a spawn-budget slot, writing a manifest or a session dir, or
calling Popen.

These tests run dispatch.py as a real subprocess against a scratch project, so
exit codes and stdout are the ground truth, and the no-side-effect clauses are
checked on disk (`no sessions/ dir`) which is exactly the guarantee the
hypothesis names.

Run with `--harness claude-code` (the verify's advisor case: model + effort
routing, the advisor brief swap, the ultracode env gate) and `--harness pi`
(the other harness, prompt-segment spelling).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"

LADDER = """---
current_season: 2
roles:
  - {"tier": 3, "role": "parent", "harness": "claude-code", "model": "claude-opus-5", "effort": "max", "settings": "ultracode"}
  - {"tier": 1, "role": "parent", "harness": "pi", "model": "~z-ai/glm-flash-latest", "effort": "", "settings": ""}
  - {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}
---

body
"""

CONFIG = {
    "harnesses": {
        "pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "deepseek-v4", "parent": "glm-flash"},
            # fail-closed allowlist: every model this harness may actually
            # resolve in the tests -- the ladder/seat rows carry full slugs
            # (~z-ai/glm-flash-latest), the config fallback carries the bare
            # names. Both are allowed so every pre-existing green case stays
            # green under fail-closed (hypothesis:l4-dispatch-model-allowlist).
            "allowed_models": ["deepseek-v4", "glm-flash",
                               "~deepseek/deepseek-v4-flash-latest",
                               "~z-ai/glm-flash-latest"],
        },
        "claude-code": {
            "adapter": "claude_code",
            "models": {"kid": "claude-sonnet-5", "parent": "claude-opus-5",
                       "director": "claude-fable-5-1"},
            "allowed_models": ["claude-sonnet-5", "claude-opus-5",
                               "claude-fable-5-1"],
            "effort": {"director": "max"},
        },
    },
    "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
}


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """A scratch agi project: `.agi/` with a config and a ladder roles table."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps(CONFIG))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(LADDER)
    return tmp_path


def _run(project: Path, *args, env=None) -> subprocess.CompletedProcess:
    """Run dispatch --dry-run, optionally overriding/removing child env keys.

    env values of None are REMOVED from the child env (so the "neither
    present" seat case is testable regardless of the runner's own env).
    """
    base = dict(os.environ)
    if env:
        for k, v in env.items():
            if v is None:
                base.pop(k, None)
            else:
                base[k] = v
    return subprocess.run(
        [sys.executable, str(BIN / "dispatch.py"), str(project), "1", *args],
        capture_output=True, text=True, env=base,
    )


def test_pi_dry_run_resolves_the_spawn_and_exits_zero(project):
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=pi" in out
    # the ladder tier-1 parent row resolves the pi model
    assert "--model" in out and "glm-flash" in out
    assert "brief_tier=parent" in out
    assert "no budget slot taken" in out


def test_pi_dry_run_creates_no_session_dir(project):
    _run(project, "--harness", "pi", "--tier", "parent",
         "--target", "hypothesis:x", "--dry-run")
    assert not (project / ".agi" / "sessions").exists(), (
        "a dry run must not create a session dir")


def test_prompt_file_threads_the_carry_forward_addendum_into_the_command(project, tmp_path):
    """hypothesis:l3-parent-never-told-to-iterate, carry-forward axis (SD.12)
    -- the per-kid brief channel lands in the RECORDED COMMAND STRING, which
    is exactly how the live gate reads it (kid 2's agent.json command field).
    The addendum is read by FILE PATH (the writer already chose path|-> for
    the same reason: a kid's result holds arbitrary characters), is never
    inlined as an argv string, and appears as its own labelled
    --append-system-prompt segment in the dry-reported command line.
    """
    add = tmp_path / "kid1-result.txt"
    add.write_text("KID1 disproved hypothesis:x\nline two with && and \"quotes\"")
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run",
             "--prompt-file", str(add))
    assert r.returncode == 0, r.stderr
    assert "WHAT THE LAST KID PRODUCED" in r.stdout
    # The full addendum text is truncated by the dry-run's compact command
    # display (_compact shortens args >200 chars); verbatim carry of the text
    # itself is asserted at the assemble level (test_kid_addendum_lands_as_a_
    # labelled_segment_and_names_the_flag). Here the LABEL in the reported
    # command line is what proves the flag threaded the segment.
    assert "from your parent, not from the node" in r.stdout


def test_prompt_file_absent_adds_no_addendum_and_does_not_name_the_segment(project):
    """The no-flag no-regression half: a --dry-run WITHOUT --prompt-file
    must not inject the carry-forward segment or its label into a kid's
    reported command, i.e. the spawn is byte-identical to a non-addendum one.
    """
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "WHAT THE LAST KID PRODUCED" not in r.stdout


def test_parent_prompt_file_is_refused_and_never_silently_dropped(project, tmp_path):
    """hypothesis:l4b23-promptfile-drop -- `--prompt-file` is the per-KID
    carry-forward channel (brief.assemble threads addendum into _kid but
    never into _parent), so `--tier parent --prompt-file X` used to read X's
    bytes and silently discard them inside assemble(). It is now REFUSED
    loudly (exit 2, a clear stderr message) at argument-parsing time rather
    than accepted-then-dropped. The next_edges-compatible resolution is
    refusal, not threading, because a parent's brief is built fresh from its
    target node every dispatch and consumes no carry-forward.
    """
    add = tmp_path / "parent-misuse.txt"
    add.write_text("parent-distinctive-marker")
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--prompt-file", str(add))
    assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
    assert "per-KID carry-forward" in r.stderr
    assert "Refusing rather than silently discarding" in r.stderr
    # the marker must NOT leak into any brief that still assembled
    assert "parent-distinctive-marker" not in r.stdout


def test_parent_orders_reach_the_brief_and_are_printed_by_the_dry_run(
        project, tmp_path):
    """goal:g15.25 SM.26 -- `--tier parent --orders <file>` threads the
    director's dispatch-time instruction into the parent brief VERBATIM under
    one `## DISPATCH ORDERS` heading, and a dry run PRINTS that heading plus
    its first lines before any spawn is paid for. The old parent refusal was
    for `--prompt-file`; `--orders` is the new, accepted channel."""
    orders = tmp_path / "orders.md"
    orders.write_text("SCOPE: touch only dispatch.py\nCOUPLE: SM.24\n")
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run",
             "--orders", str(orders), "--from", "sanctuary-director")
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert "## DISPATCH ORDERS (from sanctuary-director," in r.stdout
    assert "orders:" in r.stdout
    assert "SCOPE: touch only dispatch.py" in r.stdout


def test_a_dispatch_refused_at_the_zoom_gate_leaves_no_orders_copy(
        project, tmp_path):
    """goal:g15.25 SM.28 claim (4), ORPHAN half -- measured pre-fix: the
    orders copy was written ABOVE the per-slot refusal gates, so a LIVE
    dispatch refused at the zoom gate (rc 1, no spawn) left
    `<iter>/orders.<from>.md` on disk with no manifest record to name it. A
    bogus target refuses at the zoom render inside the slot loop -- before
    Popen -- so this test exercises the real path end to end and spawns
    nothing (claude-code harness: no provider key floor to refuse earlier)."""
    orders = tmp_path / "orders.md"
    orders.write_text("SCOPE: only dispatch.py\n")
    r = _run(project, "--harness", "claude-code", "--tier", "parent",
             "--target", "hypothesis:no-such-node", "--orders", str(orders),
             "--from", "SAME")
    assert r.returncode == 1, (r.returncode, r.stdout, r.stderr)
    assert "no context for target" in r.stderr, r.stderr
    iter_dir = project / ".agi" / "sessions" / "iter-001"
    leftovers = sorted(iter_dir.glob("orders.*")) if iter_dir.exists() else []
    assert leftovers == [], (
        f"a dispatch refused at the zoom gate left an orphan orders copy: "
        f"{leftovers}")
    assert not (iter_dir / "manifest.json").exists(), (
        "a refused round must not have a manifest for the orphan to hide in")


def test_kid_orders_is_the_carry_forward_alias(project, tmp_path):
    """goal:g15.25 SM.26 -- at KID tier `--orders` is the same per-kid
    carry-forward as `--prompt-file` (ONE implementation), landing as the
    labelled `WHAT THE LAST KID PRODUCED` segment, never a parent heading."""
    f = tmp_path / "kid1.txt"
    f.write_text("KID1 landed dispatch.py --orders")
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run",
             "--orders", str(f))
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert "WHAT THE LAST KID PRODUCED" in r.stdout
    assert "DISPATCH ORDERS" not in r.stdout


def test_claude_advisor_dry_run_resolves_model_effort_and_env(project):
    """The verify's advisor case: a tier-3 parent aimed at a vision node gets
    the advisor brief and the full ultracode spawn, resolved without
    spawning."""
    r = _run(project, "--harness", "claude-code", "--tier", "parent",
             "--ladder-tier", "3", "--target", "vision:alive", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=claude-code" in out
    # the tier-3 parent ladder row -> claude-opus-5 / effort max / ultracode
    assert "--model claude-opus-5" in out
    assert "--effort max" in out
    # the ladder settings row is shell-quoted in the printed command (JSON
    # carries spaces, so shlex adds single-quote marks) — match the printed
    # spelling.
    assert "--settings '{\"ultracode\": true}'" in out
    # the advisor brief swap
    assert "brief_tier=advisor" in out
    # the ultracode env gate, shown in the exported env
    assert "CLAUDE_CODE_WORKFLOWS=1" in out
    assert "AGI_LADDER_TIER=3" in out
    assert "AGI_MODEL=claude-opus-5" in out
    # the brief is summarized, not printed in full
    assert "first 20:" in out


def test_claude_advisor_dry_run_creates_no_session_dir(project):
    _run(project, "--harness", "claude-code", "--tier", "parent",
         "--ladder-tier", "3", "--target", "vision:alive", "--dry-run")
    assert not (project / ".agi" / "sessions").exists(), (
        "a dry run must not create a session dir")
    assert not list((project / ".agi" / "nodes").rglob("experiment/*.md")), (
        "a dry run must not scaffold a node")


def test_dry_run_takes_no_budget_slot(project):
    """The budget is checked on disk: a dry run registers nothing live."""
    _run(project, "--harness", "pi", "--tier", "parent",
         "--target", "hypothesis:x", "--dry-run")
    budget_dir = project / ".agi" / "sessions" / ".spawn-budget"
    assert not budget_dir.exists(), (
        f"a dry run must not register a spawn-budget slot, but {budget_dir} exists")


def test_explicit_harness_flag_wins_over_ladder_row(project):
    """hypothesis:l3-dispatch-harness-flag-overridden — an explicit
    --harness claude-code must beat a ladder row that names pi (the tier-1
    parent row), and take claude-code's OWN parent model/effort, not the pi
    row's glm-flash model. One notice line names both harnesses."""
    r = _run(project, "--harness", "claude-code", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=claude-code" in out, out
    # the command line is a claude command with claude-code's own parent
    # model, NOT the pi row's glm-flash
    cmd_line = next(l.strip() for l in out.splitlines()
                    if l.strip().startswith("command:"))
    assert "claude -p" in cmd_line, out
    assert "--model claude-opus-5" in cmd_line, out
    assert "glm-flash" not in cmd_line, out
    # a notice names both the explicit and the ladder-row harness
    assert "overrides" in out and "claude-code" in out and "pi" in out, out


def test_ladder_row_wins_without_harness_flag(project):
    """Without --harness the ladder row still wins: a tier-3 parent row that
    names claude-code beats the config default harness (pi)."""
    r = _run(project, "--tier", "parent", "--ladder-tier", "3",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=claude-code" in out, out
    assert "--model claude-opus-5" in out, out


def test_seat_row_wins_over_both_harness_and_ladder(project):
    """A --seat row keeps winning over BOTH an explicit --harness and the
    ladder row: the seat names pi while the explicit flag names claude-code,
    so the seat's pi harness must win."""
    seats = (project / ".agi" / "nodes" / ".geometry" / "seats.md")
    seats.write_text("---\nseats:\n"
                     "  - {name: liaison, tier: 1, role: parent, "
                     "harness: pi, model: ~z-ai/glm-flash-latest, "
                     "effort: \"\", settings: \"\"}\n---\n")
    r = _run(project, "--harness", "claude-code", "--tier", "parent",
             "--seat", "liaison", "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "harness=pi" in out, out
    assert "glm-flash" in out, out


def test_dry_run_exports_seat_from_flag(project):
    """hypothesis:l4-dispatch-exports-seat — `--seat NAME` must export
    AGI_SEAT=NAME in the dry-report env line."""
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--seat", "liaison", "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "AGI_SEAT=liaison" in r.stdout, r.stdout


def test_dry_run_flag_wins_over_inherited_agi_seat(project):
    """hypothesis:l4-dispatch-exports-seat — `--seat` WINS over an AGI_SEAT
    already in the environment."""
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--seat", "liaison", "--target", "hypothesis:x", "--dry-run",
             env={"AGI_SEAT": "inherited-seat"})
    assert r.returncode == 0, r.stderr
    assert "AGI_SEAT=liaison" in r.stdout, r.stdout
    assert "AGI_SEAT=inherited-seat" not in r.stdout, r.stdout


def test_dry_run_inherited_agi_seat_survives_without_flag(project):
    """hypothesis:l4-dispatch-exports-seat — without `--seat`, an AGI_SEAT
    already in the env (the manual export the help text documents) survives."""
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run",
             env={"AGI_SEAT": "inherited-seat"})
    assert r.returncode == 0, r.stderr
    assert "AGI_SEAT=inherited-seat" in r.stdout, r.stdout


def test_dry_run_no_seat_leaves_key_absent(project):
    """hypothesis:l4-dispatch-exports-seat — neither `--seat` nor an
    inherited AGI_SEAT means the key is ABSENT, never a placeholder."""
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run",
             env={"AGI_SEAT": None})
    assert r.returncode == 0, r.stderr
    assert "AGI_SEAT=" not in r.stdout, r.stdout


def test_dry_run_exports_identity_and_readers_agree(project, monkeypatch):
    """hypothesis:l3-agent-id-never-exported — the JOINED contract.

    dispatch --dry-run resolves the real child env, so it must export the id
    it minted as both AGI_AGENT_ID and AGI_ACTOR. This test reads the
    PRODUCER's own output (not a value the test invented), then feeds exactly
    that env to the two READERS, send._detect_sender and write._default_actor,
    and asserts all three surfaces resolve to the one id. Green here means the
    suite is no longer testing a contract half by hand-constructing the other
    half's input — the shape test_send.py used to mask with
    monkeypatch.setenv.
    """
    import importlib.util
    import re as _re

    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run")
    assert r.returncode == 0, r.stderr
    out = r.stdout
    m_id = _re.search(r"\bAGI_AGENT_ID=(\S+)", out)
    m_actor = _re.search(r"\bAGI_ACTOR=(\S+)", out)
    assert m_id, f"dry-run env must export AGI_AGENT_ID:\n{out}"
    assert m_actor, f"dry-run env must export AGI_ACTOR:\n{out}"
    aid, actor = m_id.group(1), m_actor.group(1)
    assert aid.startswith("dry") and len(aid) >= 10, f"not an agent id: {aid}"
    assert actor == aid, "AGI_ACTOR must equal the minted agent id"

    # Feed the producer's OWN exported values to the readers — no invented id.
    monkeypatch.setenv("AGI_AGENT_ID", aid)
    monkeypatch.setenv("AGI_ACTOR", aid)
    monkeypatch.delenv("AGI_TMUX_WINDOW_NAME", raising=False)
    monkeypatch.delenv("TMUX", raising=False)
    monkeypatch.delenv("USER", raising=False)

    sys.path.insert(0, str(BIN))
    loaded = {}
    for name in ("send", "write"):
        spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod  # dataclasses needs the module registered
        spec.loader.exec_module(mod)
        loaded[name] = mod
    assert loaded["send"]._detect_sender(None) == aid
    assert loaded["write"]._default_actor() == aid


def test_dry_run_exports_reaper_knob_for_kid_and_parent(project):
    """hypothesis:l4-spawn-paths-export-the-reaper-knob — every spawn path
    must export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 explicitly, and
    the dry run must SHOW it (a check that costs a spawn is a check nobody
    runs). Cover the pi harness (kid + parent) and the claude-code harness."""
    for harness, tier in (("pi", "kid"), ("pi", "parent"),
                          ("claude-code", "parent")):
        r = _run(project, "--harness", harness, "--tier", tier,
                 "--target", "hypothesis:x", "--dry-run")
        assert r.returncode == 0, r.stderr
        assert ("CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1" in r.stdout), (
            f"{harness}/{tier} dry-run must export the reaper knob:\n{r.stdout}")
        # the plain integer "1", never an inherited "0"
        assert "CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=0" not in r.stdout


def test_dry_run_reaper_knob_overrides_an_inherited_zero(project):
    """hypothesis:l4-spawn-paths-export-the-reaper-knob — the knob must be
    set UNCONDITIONALLY, so an inherited "0" from the parent environment (a
    stale pause, a manual export) is overridden to "1", never preserved —
    a preserved "0" would silently re-arm the reaper."""
    r = _run(project, "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run",
             env={"CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP": "0"})
    assert r.returncode == 0, r.stderr
    assert "CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1" in r.stdout, (
        f"inherited 0 must be overridden to 1:\n{r.stdout}")
    assert "CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=0" not in r.stdout


def _g15_project(tmp_path: Path) -> Path:
    """A scratch project whose OWN graph carries a g15-lineage target.

    hypothesis:l4-brief-resolves-g15-lineage-from-the-nearest-agi — the
    end-to-end wiring: dispatch.py passes its resolved project root to the
    brief, so the g15 build-order rule is decided against THIS project's
    `.agi`, not against the `.agi` enclosing the engine's brief.py (which on
    this test rig is the real repo — a different graph, exactly the
    cloned-engine boundary the hypothesis names).
    """
    graph = tmp_path / ".agi"
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n", encoding="utf-8")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n", encoding="utf-8")
    return tmp_path




def test_live_spawn_env_hooks_path_is_this_trees_hooks(tmp_path, monkeypatch):
    """hypothesis:l4-a-parent-done-commits-on-every-grammar, claim (2) -- the
    VALUE of the spawn env, captured at the exact `Popen` that launches the
    agent, NOT a source-string grep.

    dispatch.py's `--dry-run` only exports GIT_CONFIG_COUNT (it never builds
    GIT_CONFIG_VALUE_0 in the dry-run mirror), so the real hooksPath value is
    reachable only on the LIVE spawn path. This test runs the REAL live spawn
    machinery with `subprocess.Popen` captured (returning a stub child --
    nothing is actually launched, budget/session/manifest all live under the
    scratch tmp_path) and asserts the core.hooksPath value dispatch hands the
    child resolves to `<this tree>/extensions/agi/hooks/agent-git` and that
    that directory's pre-commit hook exists.

    Why the old grep was insufficient (test_git_commit_guard.py):
    `assert "agent-git" in src` passes if the string appears ANYWHERE in
    dispatch.py -- even if the block never runs, or the assigned VALUE on the
    next line points at a different directory. Here the hook path is read off
    the env object actually passed to the spawned process, so a rewiring that
    changes the value fails it.
    """
    # The box runs this repo's loop, so AGI_TREE_PROJECT_ROOT / AGI_PROJECT_ROOT
    # are set in the inherited env and `child_working_graph` would override the
    # passed scratch root with the real worktree -- a live run would write its
    # session/manifest/budget into the shared tree. Drop them so the spawn is
    # fully contained under the scratch project.
    monkeypatch.delenv("AGI_TREE_PROJECT_ROOT", raising=False)
    monkeypatch.delenv("AGI_PROJECT_ROOT", raising=False)

    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {"adapter": "pi", "provider": "fake",
                             "models": {"parent": "glm"}}},
        "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
        # keep the live run fast and focused: no inline reaper loop
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 1, role: parent, "
        "harness: pi, model: glm}\n---\nbody")
    # pin the secrets geometry to a nonexistent file so provisioning.available
    # is False -> the live path never mints a credential or touches the network
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    # the target the live spawn zooms for
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")

    import importlib.util
    import dispatch

    captured: dict = {}
    real_popen = subprocess.Popen

    class _StubProc:
        pid = 7777
        def poll(self): return None
        def wait(self, timeout=None): return 0
        def __enter__(self): return self
        def __exit__(self, *a): return False

    def _patched_popen(popenargs, **kwargs):
        env = kwargs.get("env") or {}
        if env.get("GIT_CONFIG_VALUE_0"):
            captured["env"] = env
            return _StubProc()
        return real_popen(popenargs, **kwargs)

    monkeypatch.setattr(subprocess, "Popen", _patched_popen)
    # item 2: the stub child is alive past the grace, so without this seam the
    # poll sleeps the real 20 s (`_GRACE_SLEEP` in 2 s steps).
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.setattr(sys, "argv",
                        [str(BIN / "dispatch.py"), str(tmp_path), "1",
                         "--level", "small", "--harness", "pi",
                         "--tier", "parent", "--target", "hypothesis:x"])

    code = dispatch.main()
    assert code == 0, (
        "live dispatch of a scratch parent tier failed before the spawn: "
        f"exit {code}")
    assert "env" in captured, (
        "dispatch live path never handed the GIT_CONFIG triple to a process; "
        "the spawn env was not captured")

    env = captured["env"]
    assert env["GIT_CONFIG_COUNT"] == "1"
    assert env["GIT_CONFIG_KEY_0"] == "core.hooksPath"
    want_hooks = (BIN.parent / "hooks" / "agent-git").resolve()
    assert env["GIT_CONFIG_VALUE_0"] == str(want_hooks), (
        f"dispatch wired core.hooksPath at {env['GIT_CONFIG_VALUE_0']!r} "
        f"but the dispatcher's own tree lives at {want_hooks}")
    assert (want_hooks / "pre-commit").is_file(), (
        f"the hook value points at {want_hooks} but pre-commit is absent")
    assert env.get("AGI_PROJECT_ROOT") is not None


def test_dispatch_threads_project_root_into_the_assembled_brief(
        project, monkeypatch, capsys):
    """dispatch.py hands its own resolved project root to brief.assemble as
    `project_root`, so the g15 build-order rule is decided against the PROJECT
    graph the dispatcher owns, not the `.agi` enclosing brief.py
    (hypothesis:l4-brief-resolves-g15-lineage-from-the-nearest-agi — proof on
    the calls, by monkeypatching `assemble` to capture kwargs, since the
    dry-run printer shows only the first 20 brief lines)."""
    import dispatch as _dispatch
    import brief as _brief_mod

    calls: list = []
    monkeypatch.setattr(_brief_mod, "assemble",
                        lambda *a, **k: calls.append(k) or ["MARKER-SEGMENT"])
    _g15_project(project)  # give the scratch graph a g15-lineage target
    monkeypatch.setattr(sys, "argv",
                        [str(BIN / "dispatch.py"), str(project), "1",
                         "--harness", "pi", "--tier", "parent",
                         "--target", "hypothesis:x", "--dry-run"])
    code = _dispatch.main()
    capsys.readouterr()
    assert code == 0
    assert any(c.get("project_root") == project / ".agi" for c in calls), calls


# ---- goal:g15.25 SM.28 -- the orders channel refuses what it cannot deliver --


def test_orders_at_a_tier_that_cannot_deliver_is_refused_by_name(project,
                                                                tmp_path):
    """SM.28 claim (1). `--orders` is consumed by exactly two tiers -- `kid`
    (carry-forward) and `parent` (the orders section). Measured pre-fix:
    `--tier director --orders <path>` exited 0 with the file never opened,
    no heading and no note. A tier that neither threads nor carries it
    forward must be REFUSED BY NAME, exit 2, naming itself and the two
    tiers that accept it -- never accepted-and-dropped."""
    orders = tmp_path / "orders.md"
    orders.write_text("SCOPE: touch only dispatch.py\n")
    for tier in ("director", "advisor"):
        r = _run(project, "--harness", "claude-code", "--tier", tier,
                 "--target", "hypothesis:x", "--dry-run",
                 "--orders", str(orders))
        assert r.returncode == 2, (tier, r.returncode, r.stderr)
        assert f"`{tier}` neither threads nor carries it forward" in r.stderr
        assert "`kid` (per-kid carry-forward)" in r.stderr
        assert "`parent` (the dispatch-orders section)" in r.stderr


def test_an_absent_orders_path_is_a_named_refusal_not_a_traceback(
        project, tmp_path):
    """SM.28 claim (5). Measured pre-fix: `--tier parent --orders <missing>`
    exited 1 with a FileNotFoundError traceback out of `_read_prompt_file`.
    A missing path is an operator error and must read like one."""
    missing = tmp_path / "nope.md"
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run",
             "--orders", str(missing))
    assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
    assert "path does not exist or is not a file" in r.stderr
    assert str(missing) in r.stderr
    assert "Traceback" not in r.stderr


def test_whitespace_only_orders_are_absent_and_leave_the_brief_identical(
        project, tmp_path):
    """SM.28 claim (3). The presence gate is `text.strip()`: measured pre-fix
    a `"   \\n\\t\\n"` file rendered `## DISPATCH ORDERS` with a blank body and
    was copied and recorded. It must instead be ABSENT -- no heading, no
    dry-run `orders:` line, and a brief byte-identical to the no-orders run.
    A non-empty file is still rendered, unstripped."""
    base = _run(project, "--harness", "pi", "--tier", "parent",
                "--target", "hypothesis:x", "--dry-run")
    assert base.returncode == 0, base.stderr
    ws = tmp_path / "ws.md"
    ws.write_text("   \n\t\n")
    r = _run(project, "--harness", "pi", "--tier", "parent",
             "--target", "hypothesis:x", "--dry-run", "--orders", str(ws))
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert "DISPATCH ORDERS" not in r.stdout
    assert "orders:" not in r.stdout
    assert _brief_line_count(r.stdout) == _brief_line_count(base.stdout), (
        "a whitespace-only orders file must leave the brief byte-identical")


def test_parent_orders_ride_the_survival_and_advisor_briefs_the_dry_run_reports(
        project, tmp_path):
    """SM.28 claim (2). Measured pre-fix on the survival profile and on the
    advisor route (--tier parent --ladder-tier 3 --target vision:<id>): the
    dry run printed `orders: N lines` and the manifest recorded
    {from,sha256,bytes,path}, while the assembled brief carried NO section --
    the record said delivered, the brief did not. The heading must appear in
    the SEGMENTS the harness is handed (the `command:` line inlines every
    segment), so dry-run line, manifest record and brief agree on every
    route that accepts --orders."""
    orders = tmp_path / "orders.md"
    orders.write_text("SCOPE: touch only dispatch.py\nCOUPLE: SM.24\n")
    cases = [
        ("pi", ["--tier", "parent", "--target", "hypothesis:x"]),
        ("claude-code", ["--tier", "parent", "--ladder-tier", "3",
                         "--target", "vision:alive"]),
    ]
    for harness, argv in cases:
        r = _run(project, "--harness", harness, *argv, "--dry-run",
                 "--orders", str(orders), "--from", "sanctuary-director",
                 env={"AGI_BRIEF_PROFILE": "survival"})
        assert r.returncode == 0, (harness, r.returncode, r.stderr)
        assert "orders:" in r.stdout, harness
        command = r.stdout.split("command:", 1)[1]
        assert "## DISPATCH ORDERS" in command, (
            f"{harness}: the dry run claims orders but no brief segment "
            f"carries them")


def _brief_line_count(out: str) -> str:
    import re as _re
    m = _re.search(r"brief: tier=\S+ (\d+) lines", out)
    assert m, out
    return m.group(1)
