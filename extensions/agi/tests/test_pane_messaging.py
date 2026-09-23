#!/usr/bin/env python3
"""One test per falsifier conjunct of goal:g7.32.2, on the production module
`extensions/agi/bin/pane_messaging.py` (built this round).

  (1) same-harness pair -> native via an injected transport, and send.py is
      never touched (a spy raises if it is).
  (2) cross-harness pair -> nudge artifact written BEFORE send.py fires;
      and native with no transport refuses by name (fail closed, no hang).
  (3) AST import scan: the module imports neither rotate nor dispatch.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import pane_messaging as pm  # noqa: E402


def test_conjunct1_same_harness_native_calls_transport_never_send_py(monkeypatch, tmp_path):
    """Conjunct 1: same harness routes native; send.py is never touched."""
    assert pm.classify("grok-bot", "grok-bot") == "native"

    def send_spy(*a, **k):  # would fire if the native path shelled out
        raise AssertionError("native path touched send.py subprocess")

    monkeypatch.setattr(pm.subprocess, "run", send_spy)
    calls = []

    def transport(recipient, body):
        calls.append((recipient, body))
        return "native-delivered"

    assert pm.native_send("grok-b", "hi", transport=transport) == "native-delivered"
    assert calls == [("grok-b", "hi")]
    assert not (tmp_path / "nudge-grok-b.json").exists()


def test_conjunct2_cross_nudge_before_send_and_native_refuses_without_transport(
    monkeypatch, tmp_path
):
    """Conjunct 2: nudge artifact exists when send.py fires; no-transport refuses."""
    seen = {}

    def fake_run(cmd, **kw):
        seen["cmd"] = cmd
        seen["nudge_existed"] = (tmp_path / "nudge-claude-x.json").exists()
        return SimpleNamespace(returncode=0, stdout="ok\n", stderr="")

    monkeypatch.setattr(pm.subprocess, "run", fake_run)
    assert pm.classify("grok-bot", "claude-code") == "cross"
    res = pm.cross_send("claude-x", "hello", comms_root=tmp_path, sender="grok-a")

    assert seen["nudge_existed"] is True, "nudge artifact must precede send.py"
    assert seen["cmd"][1].endswith("send.py") and seen["cmd"][2] == "send"
    assert res["nudge"] == str(tmp_path / "nudge-claude-x.json")
    assert res["returncode"] == 0

    # Negative: no transport -> refuse by name, never fall back to send.py.
    with pytest.raises(pm.NoTransport):
        pm.native_send("grok-b", "hi")


def test_conjunct3_module_imports_neither_rotate_nor_dispatch():
    """Conjunct 3: grep/AST — the messaging module imports no rotate/dispatch."""
    tree = ast.parse(Path(pm.__file__).read_text())
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module.split(".")[0])
    assert not ({"rotate", "dispatch"} & mods), mods
    assert "send" not in mods  # never imports the transport either