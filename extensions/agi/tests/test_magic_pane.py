"""Tests for bin/magic_pane.py — the two-route messaging seam.

Falsifier conjuncts (goal:g7.32.2):
  1. NATIVE same-family (grok-bot->grok-bot) types into the destination pane;
     send.py is never invoked, even when tmux returns non-zero.
  2. CROSS (grok-bot->claude-code|pi) writes the nudge artifact AND invokes
     send.py, in one trace, in order (artifact present at subprocess launch),
     and the artifact lives under the SAME root send.py's own reader uses.
  3. After `import magic_pane`, `rotate`/`dispatch` are not reachable (source
     grep + a fresh-interpreter sys.modules assertion), and the native path
     does not even import send.py.

The live harness names are DERIVED from the sources (config `harnesses` keys
and the adapters' `NAME` constants), never an invented string -- the round-1
defect was a native set ("grok") no live caller can produce.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import magic_pane  # noqa: E402


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A minimal agi project so comms_root resolves without the live graph."""
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(
        json.dumps({"metric_primary": "outcome_coverage"}))
    return root


def _live_harness_names() -> set[str]:
    """Every harness name this tree actually constructs: config keys + NAMEs."""
    cfg = json.loads((ROOT / ".agi" / "config.json").read_text())
    names = set((cfg.get("harnesses") or {}).keys())
    for adapter in sorted((BIN / "adapters").glob("*_adapter.py")):
        m = re.search(r'^NAME\s*=\s*"([^"]+)"', adapter.read_text(), re.M)
        if m:
            names.add(m.group(1))
    return names


class _Trace:
    """Fake subprocess.run: records argv, returns rc 0, honours kwargs."""

    def __init__(self, rc: int = 0) -> None:
        self.calls: list[list[str]] = []
        self.rc = rc

    def __call__(self, cmd, **kwargs):
        self.calls.append(list(cmd))
        return subprocess.CompletedProcess(cmd, self.rc, stdout="", stderr="")


def test_choose_route_is_destination_family_data():
    assert magic_pane.NATIVE_FAMILIES == frozenset({"grok"})
    assert magic_pane.family_of("grok-bot") == "grok"
    assert magic_pane.choose_route("grok-bot") == "native"
    assert magic_pane.choose_route("GROK-BOT") == "native"
    assert magic_pane.choose_route("claude-code") == "cross"
    assert magic_pane.choose_route("pi") == "cross"


def test_live_registry_grok_is_native_and_others_cross(project, monkeypatch):
    """Conjunct 1, on the names the tree ACTUALLY constructs. Fails round 1."""
    live = _live_harness_names()
    assert "grok-bot" in live, "grok-bot must be a live registry/adapter name"
    monkeypatch.setattr(magic_pane.time, "sleep", lambda s: None)

    trace = _Trace()
    result = magic_pane.send_message(
        project, "grok-b", "hi there", "grok-bot",
        sender="grok-a", run=trace, enter_delay_s=0)

    assert result["route"] == "native"
    assert trace.calls == [
        ["tmux", "send-keys", "-l", "-t", "agi-rc:grok-b", "hi there"],
        ["tmux", "send-keys", "-t", "agi-rc:grok-b", "Enter"],
    ]
    flat = " ".join(" ".join(c) for c in trace.calls)
    assert "send.py" not in flat

    for dest in ("claude-code", "pi"):
        assert dest in live
        assert magic_pane.choose_route(dest) == "cross"


def test_native_route_survives_nonzero_tmux_without_send_py(project, monkeypatch):
    """Conjunct 1 hardened: rc!=0 must NOT fall back to send.py."""
    monkeypatch.setattr(magic_pane.time, "sleep", lambda s: None)
    trace = _Trace(rc=1)
    result = magic_pane.send_message(
        project, "grok-b", "hi", "grok-bot",
        sender="grok-a", run=trace, enter_delay_s=0)

    assert result["route"] == "native"
    flat = " ".join(" ".join(c) for c in trace.calls)
    assert "send.py" not in flat and "send-keys" in flat
    # native route writes no nudge artifact
    assert not magic_pane.nudge_artifact_path(project, "grok-b").exists()


@pytest.mark.parametrize("harness", ["claude-code", "pi"])
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


def test_cross_artifact_root_is_sends_own_comms_root(project):
    """Conjunct 2 hardened: the nudge lives where send.py reads (not a fork)."""
    import send as send_mod

    expected = (send_mod.comms_root(project) / magic_pane.NUDGE_DIRNAME
                / "dest-b.nudge")
    assert magic_pane.nudge_artifact_path(project, "dest-b") == expected


def test_import_graph_has_no_rotate_or_dispatch():
    """Conjunct 3: source grep, fresh-interpreter sys.modules, lazy send."""
    src = (BIN / "magic_pane.py").read_text()
    assert not re.search(
        r"^\s*(?:import|from)\s+(?:rotate|dispatch)\b", src, re.M)
    # send.py may be imported LAZILY by the cross path only: no module-level
    # import of it (the native route must never reach it at all).
    assert not re.search(r"^(?:import|from)\s+send\b", src, re.M)

    code = (
        "import sys; sys.path.insert(0, %r)\n"
        "import magic_pane\n"
        "bad = [m for m in ('rotate', 'dispatch', 'send') if m in sys.modules]\n"
        "print(','.join(bad))\n" % str(BIN)
    )
    env = dict(os.environ, PYTHONPATH=str(BIN))
    out = subprocess.run([sys.executable, "-c", code], capture_output=True,
                         text=True, env=env)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == ""
