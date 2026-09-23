"""Tests for bin/magic_pane.py — the two-route messaging seam.

Falsifier conjuncts (goal:g7.32.2):
  1. NATIVE grok->grok types into the destination pane; no send.py invocation.
  2. CROSS grok->claude|pi writes the nudge artifact AND invokes send.py, in
     one trace, in order (artifact present when the subprocess is launched).
  3. After `import magic_pane`, `rotate`/`dispatch` are not reachable (source
     grep + a fresh-interpreter sys.modules assertion).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import magic_pane  # noqa: E402


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A minimal agi project so locations.shared_sessions_dir resolves."""
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(
        json.dumps({"metric_primary": "outcome_coverage"}))
    return root


class _Trace:
    """Fake subprocess.run: records argv, returns rc 0, honours kwargs."""

    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def __call__(self, cmd, **kwargs):
        self.calls.append(list(cmd))
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")


def test_choose_route_is_destination_harness_data():
    assert magic_pane.NATIVE_HARNESSES == frozenset({"grok"})
    assert magic_pane.choose_route("grok") == "native"
    assert magic_pane.choose_route("GROK") == "native"
    assert magic_pane.choose_route("claude") == "cross"
    assert magic_pane.choose_route("pi") == "cross"


def test_native_route_types_into_pane_without_send_py(project, monkeypatch):
    """Conjunct 1: grok->grok is pane type-in, and no send.py anywhere."""
    monkeypatch.setattr(magic_pane.time, "sleep", lambda s: None)
    trace = _Trace()
    result = magic_pane.send_message(
        project, "grok-b", "hi there", "grok",
        sender="grok-a", run=trace, enter_delay_s=0)

    assert result["route"] == "native"
    assert trace.calls == [
        ["tmux", "send-keys", "-l", "-t", "agi-rc:grok-b", "hi there"],
        ["tmux", "send-keys", "-t", "agi-rc:grok-b", "Enter"],
    ]
    flat = " ".join(" ".join(c) for c in trace.calls)
    assert "send.py" not in flat
    # native route writes no nudge artifact
    assert not magic_pane.nudge_artifact_path(project, "grok-b").exists()
    # and the module source carries no send.py import (import statements only,
    # so the docstring's prose about send.py cannot false-positive)
    src = (BIN / "magic_pane.py").read_text()
    assert not re.search(r"^\s*(?:import|from)\s+send\b", src, re.M)


@pytest.mark.parametrize("harness", ["claude", "pi"])
def test_cross_route_artifact_then_send_py_in_order(project, harness):
    """Conjunct 2: one trace, both events, artifact already on disk."""
    seen: dict = {}

    class _Run:
        def __call__(self, cmd, **kwargs):
            p = magic_pane.nudge_artifact_path(project, "dest-b")
            seen["artifact_exists_at_invoke"] = p.is_file()
            seen["argv"] = list(cmd)
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    result = magic_pane.send_message(
        project, "dest-b", "hello", harness, sender="grok-a", run=_Run())

    assert result["route"] == "cross"
    artifact = Path(result["artifact"])
    assert artifact.is_file()
    assert json.loads(artifact.read_text()) == {
        "to": "dest-b", "harness": harness, "from": "grok-a", "route": "cross"}
    assert seen["artifact_exists_at_invoke"] is True
    argv = seen["argv"]
    assert argv[1].endswith("send.py") and Path(argv[1]) == magic_pane.SEND_PY
    assert argv[2] == "send"
    assert argv[3] == "dest-b" and argv[4] == "hello"
    assert argv[5:] == ["--from", "grok-a"]
    assert result["returncode"] == 0


def test_import_graph_has_no_rotate_or_dispatch():
    """Conjunct 3: source grep AND a fresh-interpreter sys.modules assert."""
    src = (BIN / "magic_pane.py").read_text()
    assert not re.search(
        r"^\s*(?:import|from)\s+(?:rotate|dispatch)\b", src, re.M)

    code = (
        "import sys; sys.path.insert(0, %r)\n"
        "import magic_pane\n"
        "bad = [m for m in ('rotate', 'dispatch') if m in sys.modules]\n"
        "print(','.join(bad))\n" % str(BIN)
    )
    env = dict(os.environ, PYTHONPATH=str(BIN))
    out = subprocess.run([sys.executable, "-c", code], capture_output=True,
                         text=True, env=env)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == ""
