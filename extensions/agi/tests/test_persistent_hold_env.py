"""goal:g7.31.1.2.1 -- the HELD restart reaches the filtered child env.

The goal was written against a `HOLD_PANE` / `tmux_hold` seam that does not
exist in this tree. The real durable named hold is the PERSISTENT seat
(`goal:g7.28.1`): `--persistent` makes `dispatch._supervise_persistent` hold the
seat and re-open it through the same `_open_round` closure after a death. So
the seam under test is `_open_round` -> `subprocess.Popen(env=spawn_env)`, and
the claim is that the env a HELD seat re-spawns with is the SAME filtered
`child_env` the first spawn used -- no second env path, no bare environ
inherited by the re-opened child.

Two directions, both through the wire boundary (`kwargs["env"]` on the Popen
call), never through an internal:

  1. `credential: "none"` row  -> OPENROUTER_API_KEY absent on BOTH the first
     spawn and the held restart (the falsifier in goal:g7.31.1.2.1);
  2. unmarked row              -> the inherited key is present on both.

Plus the identity conjunct: the restart hands the SAME env object content, so a
future second-env path in the supervisor turns this red.

No live model, no network, no real sleep: `subprocess.Popen` is stubbed for the
spawn call and `dispatch._PERSIST_SLEEP` is a no-op.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import provisioning  # noqa: E402

KEY = provisioning.RUNTIME_KEY_VAR


def _load_dispatch():
    spec = importlib.util.spec_from_file_location(
        "agi_dispatch_hold_env", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()

PI_LOCAL_ROW = {"adapter": "pi", "provider": "local-town",
                "credential": "none", "models": {"kid": "Qwen3.5-9B-Q4_K_M"}}
PI_ROW = {"adapter": "pi", "provider": "fake",
          "models": {"kid": "deepseek-v4"}}


def _project(tmp_path: Path, row: dict) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": dict(row)},
        "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 0, role: kid, "
        "harness: pi, model: M}\n---\nbody")
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR", dispatch._PERSIST_STOP_ENV):
        os.environ.pop(k, None)
    return tmp_path


class _StubProc:
    def __init__(self, pid, rc, left):
        self.pid = pid
        self._rc = rc
        self._left = left
        self.returncode = None

    def poll(self):
        if self._left <= 0:
            if self._rc is not None:
                self.returncode = self._rc
            return self.returncode
        self._left -= 1
        return None


def _hold_and_capture(monkeypatch, project: Path) -> list[dict]:
    """Run one `--persistent` dispatch that dies once and is re-opened; return
    the `env=` mapping of each Popen on the spawn path, in order."""
    envs: list[dict] = []
    real_popen = subprocess.Popen

    def _patched(argv, **kwargs):
        if not kwargs.get("start_new_session"):
            return real_popen(argv, **kwargs)
        envs.append(dict(kwargs.get("env") or {}))
        n = len(envs)
        if n >= 2:
            os.environ[dispatch._PERSIST_STOP_ENV] = "1"
        return _StubProc(5000 + n, 1 if n == 1 else None, 0 if n == 1 else 99)

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.setattr(dispatch, "_PERSIST_SLEEP", lambda s: None)
    monkeypatch.delenv(dispatch._PERSIST_STOP_ENV, raising=False)
    monkeypatch.setenv(KEY, "sk-or-v1-inherited")
    monkeypatch.setattr(sys, "argv", [
        str(BIN / "dispatch.py"), str(project), "1", "--level", "small",
        "--harness", "pi", "--tier", "kid", "--target", "hypothesis:x",
        "--persistent"])
    assert dispatch.main() == 0
    return envs


@pytest.mark.parametrize("row,expect_key", [
    (PI_LOCAL_ROW, False),
    (PI_ROW, True),
])
def test_held_restart_env_follows_the_credential_row(row, expect_key,
                                                    tmp_path, monkeypatch):
    """The HELD re-spawn gets the SAME filtered env the first spawn got: no
    key for a `credential: "none"` row, the inherited key for an unmarked one,
    on BOTH Popen calls."""
    envs = _hold_and_capture(monkeypatch, _project(tmp_path, row))
    assert len(envs) == 2, f"expected one held restart, got {len(envs)} envs"
    first, restarted = envs
    for label, env in (("first spawn", first), ("held restart", restarted)):
        if expect_key:
            assert env.get(KEY) == "sk-or-v1-inherited", (
                f"{label}: the unmarked row must keep {KEY}; "
                f"got {env.get(KEY)!r}")
        else:
            assert KEY not in env, (
                f"{label}: a held credential-none seat must not inherit "
                f"{KEY}")


def test_held_restart_reuses_the_one_filtered_env(tmp_path, monkeypatch):
    """The identity conjunct: the restart is the SAME env content, so a second
    env built inside the supervisor (an unfiltered one) turns this red."""
    envs = _hold_and_capture(monkeypatch, _project(tmp_path, PI_LOCAL_ROW))
    first, restarted = envs
    assert first == restarted, (
        "the held restart built a different env than the first spawn; keys "
        f"differ: "
        f"{ {k for k in set(first) | set(restarted) if first.get(k) != restarted.get(k)} }")
    assert first.get("AGI_TIER") == "kid", first
