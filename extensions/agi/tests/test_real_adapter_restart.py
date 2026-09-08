"""Integration test: real pi_adapter restart with actual subprocess.

goal:g4.7's falsifier — the inline reaper (proved at 0.88 against fake
adapters) has never restarted a real process. This test exercises
`pi_adapter.restart()` with actual `subprocess.Popen`, real pid lifecycle,
and the reaper's `_reap_one` detection + restart path using a real adapter.

Each test creates a minimal mock pi binary (a shell script that touches a node
file and exits) so no API key is needed — the gap is the subprocess machinery,
not pi's LLM calling.
"""
from __future__ import annotations

import importlib.util
import json
import os
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

# Import pi_adapter directly (the real one, not a mock)
import adapters  # noqa: E402
import spawn_budget  # noqa: E402


def _load_dispatch():
    spec = importlib.util.spec_from_file_location("agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

MOCK_PI = """#!/bin/bash
# Mock pi binary: writes a "completed" marker and exits
echo "MOCK PI AGENT STARTED: $0"
mkdir -p "$(dirname "$1")" 2>/dev/null || true
touch "$1/agent_completed"
echo "mock agent done for session $1"
"""


@pytest.fixture
def mock_pi_bin(tmp_path: Path) -> str:
    """Create a mock pi binary that just exits cleanly."""
    pi_bin = tmp_path / "mock_pi.sh"
    pi_bin.write_text(MOCK_PI)
    pi_bin.chmod(0o755)
    return str(pi_bin)


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """Minimal project structure for dispatch/reaper tests."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "sessions").mkdir(parents=True)
    # Minimal config
    (graph / "config.json").write_text(json.dumps({
        "agent_dispatch": {"provider": "openrouter",
                           "model": "test-model"},
    }))
    return tmp_path


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestPiAdapterRestartWithRealProcess:
    """Validate that `pi_adapter.restart()` spawns a real process with a real
    pid that can be killed, detected dead, and restarted."""

    def test_restart_reenters_the_branch_worktree_not_main(self, project_root, monkeypatch):
        """hypothesis:l3-branch-isolation-partial-break — a reaper restart
        of a `--branch` spawn must be born with its cwd INSIDE its own
        worktree, or its relative source edits land in the MAIN checkout. The
        old `cwd=sess_dir.parent.parent.parent` resolved iter_dir against the
        dispatch's own root (main for a top-level dispatch) and re-spawned the
        restarted parent in main. Red-first: with mocked pi recording `pwd`,
        restart must report the worktree, never main."""
        import adapters
        pi = adapters.load("pi")

        # A branch agent's record carries `worktree`; the session dir lives in
        # MAIN (top-level dispatch resolves iter_dir against the main root).
        wt = project_root / ".agi" / "worktrees" / "a00-branchy"
        wt.mkdir(parents=True)
        sess_dir = project_root / "sessions" / "iter-996" / "a00-branchy"
        sess_dir.mkdir(parents=True)
        (sess_dir / "context.md").write_text("ctx")

        pwd_marker = project_root / "restart_cwd.txt"
        pwd_pi = project_root / "pwd_pi.sh"
        pwd_pi.write_text(
            f"#!/bin/bash\npwd > {pwd_marker}\nexit 0\n")
        pwd_pi.chmod(0o755)
        monkeypatch.setenv("PI_BIN", str(pwd_pi))

        harness = {"adapter": "pi", "bin": str(pwd_pi),
                   "provider": "openrouter", "models": {"kid": "test-model"}}
        agent_record = {
            "id": "a00-branchy", "tier": "kid", "iter": 996,
            "status": "failed", "pid": 0, "worktree": str(wt),
        }

        new_pid = pi.restart(
            harness=harness, tier="kid",
            context_file=str(sess_dir / "context.md"),
            agent_id="a00-branchy", iter_n=996, sess_dir=sess_dir,
            agent_record=agent_record,
        )
        assert new_pid, "restart must spawn"
        try:
            import time
            for _ in range(50):
                if pwd_marker.exists():
                    break
                time.sleep(0.05)
            assert pwd_marker.exists(), "mock pi never ran"
            cwd = pwd_marker.read_text().strip()
        finally:
            try:
                os.kill(new_pid, signal.SIGKILL)
            except OSError:
                pass
        wt_res = str(wt.resolve())
        assert os.path.realpath(cwd) == wt_res, (
            f"restarted --branch agent must have cwd inside its worktree "
            f"{wt_res}, got {cwd!r}")
        assert cwd != str(project_root.resolve()), (
            "restarted agent must NOT be born in the main checkout")

    def test_restart_cwd_helper_falls_back_without_a_worktree(self, project_root):
        """Non-branch records (no `worktree`) keep the historical cwd
        derivation, so restarts of ordinary kids are unchanged."""
        import adapters
        pi = adapters.load("pi")
        sess_dir = project_root / "sessions" / "iter-1" / "a00-plain"
        sess_dir.mkdir(parents=True)
        # No worktree in the record → historical sess_dir.parent.parent.parent.
        cwd = pi._restart_cwd(sess_dir, {"id": "a00-plain"})
        assert cwd == sess_dir.parent.parent.parent

    def test_restart_returns_real_pid(self, mock_pi_bin, project_root, monkeypatch):
        """The core claim: pi_adapter.restart() through subprocess.Popen produces
        a real, valid OS pid — not a synthetic one returned by a mock."""
        monkeypatch.setenv("PI_BIN", mock_pi_bin)
        pi = adapters.load("pi")

        sess_dir = project_root / "sessions" / "iter-999" / "agent-test"
        sess_dir.mkdir(parents=True)
        ctx_file = sess_dir / "context.md"
        ctx_file.write_text("Test context")
        agent_record = {
            "id": "agent-test",
            "tier": "kid",
            "iter": 999,
            "status": "failed",
            "pid": 0,
        }

        harness = {"adapter": "pi",
                   "bin": mock_pi_bin,
                   "provider": "openrouter",
                   "models": {"kid": "test-model"}}

        new_pid = pi.restart(
            harness=harness,
            tier="kid",
            context_file=str(ctx_file),
            agent_id="agent-test",
            iter_n=999,
            sess_dir=sess_dir,
            agent_record=agent_record,
        )

        assert new_pid is not None, "restart() must return a pid"
        assert isinstance(new_pid, int), "pid must be an int"
        assert new_pid > 0, "pid must be a valid OS pid (>0)"
        assert agent_record["pid"] == new_pid, "agent_record.pid must be updated"
        assert agent_record["status"] == "restarted", "status must be restarted"
        assert agent_record.get("restart_count") is None, "restart_count not set by restart()"
        assert agent_record.get("restarted_at") is not None, "restarted_at must be set"

        # Clean up: kill the process
        try:
            os.kill(new_pid, signal.SIGKILL)
        except OSError:
            pass

    def test_is_alive_detects_dead_and_live_real_processes(self, mock_pi_bin, monkeypatch):
        """is_alive() works with OS pids, not just values >0."""
        monkeypatch.setenv("PI_BIN", mock_pi_bin)
        pi = adapters.load("pi")

        # Spawn a real long-lived process
        proc = subprocess.Popen(
            ["bash", "-c", "sleep 60"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        assert pi.is_alive(proc.pid), "a running process must report alive"
        proc.kill()
        proc.wait(timeout=5)
        time.sleep(0.2)
        assert not pi.is_alive(proc.pid), "a dead process must report not alive"

    def test_is_alive_reports_an_unreaped_zombie_as_dead(self, mock_pi_bin, monkeypatch):
        """hypothesis:l3-reaper-restarts-through-stop. A killed child is a
        ZOMBIE (state Z) until its parent reaps it -- `os.kill(pid, 0)`
        answers true for a zombie, so signal-existence alone (the old
        `pi_adapter.is_alive`) reports it alive for a window that can span
        several reaper polls. `claude_code_adapter.is_alive` and
        `spawn_budget._pid_alive` were already fixed for exactly this
        (hypothesis:l3-cc-adapter-zombie-lease); pi_adapter had drifted.
        Deliberately does NOT waitpid before asserting, so this only passes
        if is_alive() itself reads process STATE rather than mere
        existence."""
        monkeypatch.setenv("PI_BIN", mock_pi_bin)
        pi = adapters.load("pi")

        proc = subprocess.Popen(
            ["bash", "-c", "sleep 60"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        proc.send_signal(signal.SIGKILL)
        # Give the kernel a moment to transition the process to Z, but do
        # NOT wait()/waitpid() it — that would reap it and defeat the test.
        for _ in range(50):
            try:
                with open(f"/proc/{proc.pid}/stat") as fh:
                    state = fh.read().rsplit(") ", 1)[1].split()[0]
            except (OSError, IndexError):
                state = "?"
            if state == "Z":
                break
            time.sleep(0.02)
        assert state == "Z", (
            f"test setup: expected pid {proc.pid} to be a zombie, got "
            f"state {state!r} -- the test proves nothing if it was "
            f"already reaped before is_alive() ran")
        assert not pi.is_alive(proc.pid), (
            "an unreaped zombie must report dead, not alive")
        proc.wait(timeout=5)  # clean up: reap it for real

    def test_restart_produces_a_killable_process(self, mock_pi_bin, project_root, monkeypatch):
        """A process spawned via restart() can be terminated and detected dead,
        proving it is a real subprocess (not a fake/synthetic pid)."""
        monkeypatch.setenv("PI_BIN", mock_pi_bin)
        pi = adapters.load("pi")

        # Use a variant that sleeps so we can kill it
        sleep_pi = project_root / "sleep_pi.sh"
        sleep_pi.write_text("#!/bin/bash\nsleep 30\necho done\n")
        sleep_pi.chmod(0o755)
        monkeypatch.setenv("PI_BIN", str(sleep_pi))

        sess_dir = project_root / "sessions" / "iter-998" / "agent-killtest"
        sess_dir.mkdir(parents=True)
        (sess_dir / "context.md").write_text("ctx")
        agent_record = {"id": "agent-killtest", "tier": "kid", "iter": 998,
                        "pid": 0, "status": "failed"}

        harness = {"adapter": "pi", "bin": str(sleep_pi),
                   "provider": "openrouter", "models": {"kid": "test-model"}}

        new_pid = pi.restart(
            harness=harness, tier="kid", context_file=str(sess_dir / "context.md"),
            agent_id="agent-killtest", iter_n=998, sess_dir=sess_dir,
            agent_record=agent_record,
        )

        assert new_pid and new_pid > 0, "must get a real pid"
        assert pi.is_alive(new_pid), "process must be alive after restart"

        # Kill it
        os.kill(new_pid, signal.SIGKILL)
        # Reap the zombie so os.kill(pid, 0) returns ESRCH
        try:
            os.waitpid(new_pid, 0)
        except OSError:
            pass
        assert not pi.is_alive(new_pid), "process must be dead after kill"

    def test_real_restart_path_through_reaper_detects_and_restarts(self, mock_pi_bin, project_root, monkeypatch):
        """The full _reap_one path with a real adapter: a real process dies,
        the reaper detects it, restarts it, and the record says running."""
        monkeypatch.setenv("PI_BIN", mock_pi_bin)
        pi = adapters.load("pi")

        iter_dir = project_root / "sessions" / "iter-997"
        iter_dir.mkdir(parents=True)
        agent_id = "a00-realtest"
        sess_dir = iter_dir / agent_id
        sess_dir.mkdir(parents=True)
        ctx_file = sess_dir / "context.md"
        ctx_file.write_text("Test context for real-agent restart")
        log_file = sess_dir / "output.log"
        log_file.write_text("")

        # Spawn a process that will be detected as an agent
        harness = {"adapter": "pi", "bin": mock_pi_bin,
                   "provider": "openrouter", "models": {"kid": "test-model"}}

        # Spawn a mock agent process that sleeps so we can kill it
        sleep_bin = project_root / "agent_sleep.sh"
        sleep_bin.write_text("#!/bin/bash\nsleep 30\necho done\n")
        sleep_bin.chmod(0o755)

        proc = subprocess.Popen(
            [str(sleep_bin)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

        agent_record = {
            "id": agent_id,
            "pid": proc.pid,
            "status": "running",
            "tier": "kid",
            "node_id": "",
            "started_at": int(time.time()),
            "context_file": str(ctx_file),
            "iter": 997,
            "harness_spec": harness,
        }
        (sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))

        # Kill the process
        os.kill(proc.pid, signal.SIGKILL)
        try:
            os.waitpid(proc.pid, 0)
        except OSError:
            pass
        assert not pi.is_alive(proc.pid), "process must be dead before reaper"

        # Now let the reaper's _reap_one handle it with a real adapter
        import completion
        monkeypatch.setattr(completion, "is_complete", lambda root, nid: False)

        # Use a harness that has the mock_pi_bin for restart
        restart_harness = dict(harness)

        out = dispatch._reap_one(
            project_root, iter_dir, pi,
            {
                "node_id": "",
                "tier": "kid",
                "pid": proc.pid,
                "status": "running",
                "restart_count": 0,
                "context_file": str(ctx_file),
                "iter": 997,
                "harness_spec": restart_harness,
            },
            agent_id, proc.pid, cap=5,
            cfg={"reaper": {"max_restarts": 1}},
        )

        assert out["record"]["status"] == "running", (
            f"reaper must restart the agent, got {out['record']['status']}: "
            f"{out['message']}"
        )
        new_pid = out["record"].get("pid", 0)
        assert new_pid > 0 and new_pid != proc.pid, (
            f"new pid {new_pid} must be different from killed pid {proc.pid}"
        )
        assert out["record"].get("restart_count") == 1, "restart count must be 1"

        # The new process must be alive
        assert pi.is_alive(new_pid), "the restarted process must be alive"
        os.kill(new_pid, signal.SIGKILL)
        try:
            os.waitpid(new_pid, 0)
        except OSError:
            pass

    def test_reaper_does_not_restart_a_killed_agent_while_paused(self, mock_pi_bin, project_root, monkeypatch):
        """hypothesis:l3-reaper-restarts-through-stop — the actual bug this
        node exists to fix. Reproduced live at least six times today
        (L3.42, L3.44, this seat's own SD.01 first attempt): an agent
        killed as part of a declared owner stop is respawned by the
        reaper seconds to hours later and resumes spending. Red before the
        fix (the reaper restarted unconditionally on any dead pid);
        green after (a paused tree must never produce a new pid here)."""
        monkeypatch.setenv("PI_BIN", mock_pi_bin)
        pi = adapters.load("pi")

        iter_dir = project_root / "sessions" / "iter-993"
        iter_dir.mkdir(parents=True)
        agent_id = "a00-pausetest"
        sess_dir = iter_dir / agent_id
        sess_dir.mkdir(parents=True)
        ctx_file = sess_dir / "context.md"
        ctx_file.write_text("Test context")

        sleep_bin = project_root / "pause_sleep.sh"
        sleep_bin.write_text("#!/bin/bash\nsleep 30\necho done\n")
        sleep_bin.chmod(0o755)

        proc = subprocess.Popen(
            [str(sleep_bin)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        os.kill(proc.pid, signal.SIGKILL)
        try:
            os.waitpid(proc.pid, 0)
        except OSError:
            pass
        assert not pi.is_alive(proc.pid), "process must be dead before reaper"

        import completion
        monkeypatch.setattr(completion, "is_complete", lambda root, nid: False)

        # THE pause, at the exact anchor a worktree-based seat also reaches
        # (budget_dir's main-checkout resolution) — project_root here IS
        # the main checkout for this fixture, so this is the direct case.
        spawn_budget.pause(project_root, reason="owner: low on tokens", actor="belam")
        try:
            out = dispatch._reap_one(
                project_root, iter_dir, pi,
                {
                    "node_id": "", "tier": "kid", "pid": proc.pid,
                    "status": "running", "restart_count": 0,
                    "context_file": str(ctx_file), "iter": 993,
                    "harness_spec": {"adapter": "pi", "bin": mock_pi_bin},
                },
                agent_id, proc.pid, cap=5,
                cfg={"reaper": {"max_restarts": 1}},
            )
        finally:
            spawn_budget.resume(project_root)

        assert out["record"]["status"] == "failed", (
            f"a paused tree must never restart, got "
            f"{out['record']['status']}: {out['message']}")
        assert "paused" in out["message"].lower(), out["message"]
        assert "paused" in out["record"]["fail_reason"].lower(), out["record"]
        assert out["record"].get("pid") is None or out["record"].get("pid") == proc.pid, (
            "no new pid may appear in the record — nothing was spawned")

    def test_done_unreported_path_with_real_dead_process(self, mock_pi_bin, project_root, monkeypatch):
        """A kid that died after its node landed must NOT be restarted — even
        with a real adapter."""
        monkeypatch.setenv("PI_BIN", mock_pi_bin)
        pi = adapters.load("pi")

        # Create a completed node
        node_dir = project_root / ".agi" / "nodes" / "experiment"
        node_dir.mkdir(parents=True, exist_ok=True)
        node_file = node_dir / "exp-complete-test.md"
        node_file.write_text("""---
id: experiment:exp-complete-test
type: experiment
---

Already done.
""")

        iter_dir = project_root / "sessions" / "iter-996"
        iter_dir.mkdir(parents=True)
        agent_id = "a00-done-unreported"
        sess_dir = iter_dir / agent_id
        sess_dir.mkdir(parents=True)

        # Spawn a mock process
        sleep_bin = project_root / "agent2_sleep.sh"
        sleep_bin.write_text("#!/bin/bash\nsleep 60\necho done\n")
        sleep_bin.chmod(0o755)

        proc = subprocess.Popen(
            [str(sleep_bin)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

        # Kill it immediately
        os.kill(proc.pid, signal.SIGKILL)
        try:
            os.waitpid(proc.pid, 0)
        except OSError:
            pass

        import completion
        monkeypatch.setattr(completion, "is_complete", lambda root, nid: True)

        out = dispatch._reap_one(
            project_root, iter_dir, pi,
            {
                "node_id": "experiment:exp-complete-test",
                "tier": "kid",
                "pid": proc.pid,
                "status": "running",
                "restart_count": 0,
                "context_file": str(sess_dir / "context.md"),
                "iter": 996,
                "harness_spec": {"adapter": "pi", "bin": mock_pi_bin},
            },
            agent_id, proc.pid, cap=5,
            cfg={"reaper": {"max_restarts": 1}},
        )

        assert out["record"]["status"] == "done-unreported", (
            f"completed agent must NOT be restarted, got {out['record']['status']}"
        )
        assert "NOT restarted" in out["message"]

    def test_restart_budget_bound_with_real_processes(self, mock_pi_bin, project_root, monkeypatch):
        """Max restarts bound works with real processes."""
        monkeypatch.setenv("PI_BIN", mock_pi_bin)
        pi = adapters.load("pi")

        iter_dir = project_root / "sessions" / "iter-995"
        iter_dir.mkdir(parents=True)
        agent_id = "a00-budget-test"
        sess_dir = iter_dir / agent_id
        sess_dir.mkdir(parents=True)

        sleep_bin = project_root / "agent3_sleep.sh"
        sleep_bin.write_text("#!/bin/bash\nsleep 60\necho done\n")
        sleep_bin.chmod(0o755)

        proc = subprocess.Popen(
            [str(sleep_bin)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        time.sleep(0.2)

        # Kill and reap
        os.kill(proc.pid, signal.SIGKILL)
        try:
            os.waitpid(proc.pid, 0)
        except OSError:
            pass

        import completion
        monkeypatch.setattr(completion, "is_complete", lambda root, nid: False)

        out = dispatch._reap_one(
            project_root, iter_dir, pi,
            {
                "node_id": "",
                "tier": "kid",
                "pid": proc.pid,
                "status": "running",
                "restart_count": 1,
                "context_file": str(sess_dir / "context.md"),
                "iter": 995,
                "harness_spec": {"adapter": "pi", "bin": mock_pi_bin},
            },
            agent_id, proc.pid, cap=5,
            cfg={"reaper": {"max_restarts": 1}},
        )

        assert out["record"]["status"] == "failed", (
            f"must fail when restart budget exhausted, got {out['record']['status']}"
        )
        assert "restarts used" in out["message"]

        try:
            os.waitpid(proc.pid, os.WNOHANG)
        except OSError:
            pass

    def test_restart_reuses_existing_scaffolded_node_twin_fix(self, mock_pi_bin, project_root, monkeypatch):
        """Fix A: restart reuses the original scaffolded node id from
        agent_record instead of minting a second node. The restarted agent
        receives scaffold info matching the existing node."""
        monkeypatch.setenv("PI_BIN", mock_pi_bin)

        exp_dir = project_root / ".agi" / "nodes" / "experiment"
        exp_dir.mkdir(parents=True, exist_ok=True)
        node_id = "experiment:existing-twin-test"
        node_file = exp_dir / "existing-twin-test.md"
        node_file.write_text(f"""---
id: {node_id}
type: experiment
parents:
  - hypothesis:test-root
scaffold_hash: abcdef1234567890
---

# {node_id}

## Experiment

## Evidence

""")

        iter_dir = project_root / "sessions" / "iter-994"
        iter_dir.mkdir(parents=True)
        agent_id = "a00-twin-fix"
        sess_dir = iter_dir / agent_id
        sess_dir.mkdir(parents=True)
        ctx_file = sess_dir / "context.md"
        ctx_file.write_text("Test context")

        pi = adapters.load("pi")
        original_restart = pi.restart
        captured_scaffold = {"value": None}

        def mock_restart(**kwargs):
            captured_scaffold["value"] = kwargs.get("scaffold")
            return original_restart(**kwargs)
        monkeypatch.setattr(pi, "restart", mock_restart)

        sleep_bin = project_root / "twin_sleep.sh"
        sleep_bin.write_text("#!/bin/bash\nsleep 30\necho done\n")
        sleep_bin.chmod(0o755)

        proc = subprocess.Popen(
            [str(sleep_bin)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

        harness = {"adapter": "pi", "bin": mock_pi_bin,
                   "provider": "openrouter", "models": {"kid": "test-model"}}
        agent_record = {
            "id": agent_id, "pid": proc.pid, "status": "running",
            "tier": "kid", "node_id": node_id,
            "parent": "hypothesis:test-root",
            "started_at": int(time.time()),
            "context_file": str(ctx_file),
            "iter": 994, "harness_spec": harness,
        }
        (sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))

        os.kill(proc.pid, signal.SIGKILL)
        try:
            os.waitpid(proc.pid, 0)
        except OSError:
            pass
        assert not pi.is_alive(proc.pid), "process must be dead"

        import completion
        monkeypatch.setattr(completion, "is_complete", lambda root, nid: False)

        out = dispatch._reap_one(
            project_root, iter_dir, pi,
            {
                "node_id": node_id, "parent": "hypothesis:test-root",
                "tier": "kid", "pid": proc.pid, "status": "running",
                "restart_count": 0, "context_file": str(ctx_file),
                "iter": 994, "harness_spec": harness,
            },
            agent_id, proc.pid, cap=5,
            cfg={"reaper": {"max_restarts": 1}},
        )

        assert out["record"]["status"] == "running", (
            f"reaper must restart, got {out['record']['status']}: {out['message']}"
        )

        sc = captured_scaffold["value"]
        assert sc is not None, "scaffold must be passed to restart"
        assert sc["node_id"] == node_id, (
            f"scaffold must reuse existing node_id {node_id}, got {sc['node_id']}"
        )
        assert sc["parent"] == "hypothesis:test-root", (
            "scaffold parent mismatch"
        )
        assert sc["node_type"] == "experiment", (
            f"scaffold node_type must be experiment, got {sc['node_type']}"
        )
        assert sc["path"] and "existing-twin-test.md" in sc["path"], (
            f"scaffold path must point to existing node file, got {sc['path']}"
        )

        twin_files = list(exp_dir.glob("*twin*"))
        assert len(twin_files) == 1, (
            f"only one experiment node file should exist, got {len(twin_files)}: {twin_files}"
        )

        try:
            os.kill(out["record"]["pid"], signal.SIGKILL)
        except OSError:
            pass
        try:
            os.waitpid(out["record"]["pid"], 0)
        except OSError:
            pass

    def test_evidence_runs_persisted_in_node_frontmatter(self, tmp_path, monkeypatch):
        """Fix B: cli.py done --evidence-runs <self> persists evidence_runs
        into the node's own frontmatter at signal time, so a node citing
        itself as evidence survives a later grid-commit re-check."""
        import importlib.util
        import argparse
        import yaml

        bin_dir = Path(__file__).resolve().parents[1] / "bin"
        spec = importlib.util.spec_from_file_location("agi_cli", bin_dir / "cli.py")
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)

        root = tmp_path / "proj-fixb"
        graph_root = root / ".agi"
        (graph_root / "nodes" / "experiment").mkdir(parents=True)
        (graph_root / "nodes" / "hypothesis").mkdir(parents=True)
        (graph_root / "nodes" / "hypothesis" / "test-root.md").write_text(
            """---
id: hypothesis:test-root
type: hypothesis
---

Root.""")
        (graph_root / "sessions" / "iter-L2.13" / "a00-fixb-test").mkdir(parents=True)
        (graph_root / "config.json").write_text(json.dumps({}))

        node_id = "experiment:self-cite-test"
        node_file = graph_root / "nodes" / "experiment" / "self-cite-test.md"
        node_file.write_text(f"""---
id: {node_id}
type: experiment
parents:
  - hypothesis:test-root
---

# {node_id}

## Experiment

Ran a test.
""")

        agent_json = graph_root / "sessions" / "iter-L2.13" / "a00-fixb-test" / "agent.json"
        agent_json.write_text(json.dumps({
            "id": "a00-fixb-test", "status": "running",
            "pid": 12345, "started_at": 1234567890,
        }))
        (graph_root / "sessions" / "iter-L2.13" / "manifest.json").write_text(
            json.dumps({"iter": "L2.13", "agents": [{"id": "a00-fixb-test"}]}))

        import locations as loc
        monkeypatch.setattr(loc, "find_project_root", lambda *args: graph_root)

        args = argparse.Namespace()
        args.func = lambda: 0
        args.iter_n = "L2.13"
        args.agent_id = "a00-fixb-test"
        args.verdict = "proved"
        args.confidence = 0.8
        args.node_id = node_id
        args.parent = "hypothesis:test-root"
        args.notes = ""
        args.next_edge = None
        args.evidence_runs = [node_id]
        args.no_evidence_gate = False
        args.owns = None

        exit_code = cli.cmd_done(args)
        assert exit_code == 0, f"cmd_done should succeed, got exit {exit_code}"

        text = node_file.read_text()
        assert text.startswith("---"), "node must still have frontmatter"
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1]) or {}

        raw = fm.get("evidence_runs")
        assert raw is not None, (
            f"evidence_runs must be present in node frontmatter, got {raw!r}"
        )
        assert node_id in raw, (
            f"evidence_runs must contain cited node id {node_id}, got {raw!r}"
        )

    def test_evidence_runs_frontmatter_survives_enforce_on_disk(self, tmp_path, monkeypatch):
        """A node with evidence_runs in frontmatter survives the
        grid-commit gate re-check (enforce_on_disk), proving Fix B's
        persistence works at the commit boundary."""
        import yaml

        root = tmp_path / "proj-enforce"
        (root / ".agi" / "nodes" / "experiment").mkdir(parents=True)
        (root / ".agi" / "nodes" / "hypothesis").mkdir(parents=True)
        (root / ".agi" / "sessions").mkdir(parents=True)
        (root / ".agi" / "config.json").write_text(json.dumps({}))

        hyp_file = root / ".agi" / "nodes" / "hypothesis" / "parent-test.md"
        hyp_file.write_text("""---
id: hypothesis:parent-test
type: hypothesis
---

Parent.""")

        node_id = "experiment:grid-check-test"
        node_file = root / ".agi" / "nodes" / "experiment" / "grid-check-test.md"
        node_file.write_text(f"""---
id: {node_id}
type: experiment
parents:
  - hypothesis:parent-test
---

# {node_id}

## Experiment

Ran it.""")

        import evidence_gate
        corpus = evidence_gate.build_corpus(root / ".agi" / "nodes")
        assert node_id in corpus, (
            f"node {node_id} must be in corpus for evidence_runs to resolve"
        )

        import node_writer
        res = node_writer.update_node(
            root / ".agi", node_id,
            set_fm={
                "verdict": "proved",
                "confidence": 0.8,
                "evidence_runs": [node_id],
            },
        )
        assert res.status == node_writer.UPDATED, (
            f"update_node should succeed: {res.reason}"
        )

        demotions = evidence_gate.enforce_on_disk(
            root / ".agi", dry_run=True)
        matching = [d for d in demotions if node_id in d.node_id]
        assert len(matching) == 0, (
            f"node with self-cited evidence_runs should NOT be demoted, "
            f"got {len(matching)} matching demotions: {matching}"
        )

        text = node_file.read_text()
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1]) or {}
        er = fm.get("evidence_runs")
        assert er is not None and node_id in er, (
            f"evidence_runs must survive in frontmatter after verdict write, "
            f"got {er!r}"
        )

