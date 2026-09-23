"""Unit tests for magic_pane.py — the thin magic-pane messaging router
(goal:g7.32.2). These are the author's claim, not proof: the parent probes
them. Everything is hermetic — no real tmux, no real send.py.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import magic_pane  # noqa: E402


class FakeRun:
    """Stand-in for subprocess.run: records argv, answer a returncode."""

    def __init__(self, nudge_dir=None, returncode=0):
        self.calls = []
        self.nudge_dir = Path(nudge_dir) if nudge_dir else None
        self.returncode = returncode
        self.artifact_present_at_call = []

    def __call__(self, argv, **kwargs):
        self.calls.append(list(argv))
        if self.nudge_dir is not None:
            self.artifact_present_at_call.append(
                sorted(p.name for p in self.nudge_dir.glob("*.json")))
        return type("P", (), {"returncode": self.returncode, "stdout": "",
                              "stderr": ""})()


def test_route_is_equality_only(monkeypatch):
    assert magic_pane.route("grok-bot", "grok-bot") == "native"
    assert magic_pane.route("Grok-Bot", "  grok-bot  ") == "native"
    assert magic_pane.route("grok-bot", "pi") == "nudge_send"
    assert magic_pane.route("pi", "grok-bot") == "nudge_send"


def test_native_send_tmux_and_never_send_py(monkeypatch):
    fake = FakeRun()
    monkeypatch.setattr(magic_pane.subprocess, "run", fake)
    out = magic_pane.native_send("agi:0.1", "hello peer")
    assert out["path"] == "native"
    assert out["pane"] == "agi:0.1"
    assert out["sha256"] == hashlib.sha256(b"hello peer").hexdigest()
    # exactly one delivery call, a tmux send-keys + Enter
    assert len(fake.calls) == 1
    argv = fake.calls[0]
    assert argv[0] == "tmux"
    assert argv[1] == "send-keys"
    assert argv[2:4] == ["-t", "agi:0.1"]
    assert argv[4] == "hello peer"
    assert argv[5] == "Enter"
    # the native path never touches the send.py transport
    flat = [" ".join(map(str, c)) for c in fake.calls]
    assert not any("send.py" in s or s.strip().startswith("send ") or
                   " send " in s for s in flat)


def test_cross_send_nudge_before_send_py(tmp_path, monkeypatch):
    fake = FakeRun(nudge_dir=tmp_path)
    monkeypatch.setattr(magic_pane.subprocess, "run", fake)
    out = magic_pane.cross_send("grok-bot", "pi", "cross body", tmp_path)
    assert out["path"] == "nudge_send"
    assert out["exit_code"] == 0
    nudge = Path(out["nudge"])
    assert nudge.exists()
    # the nudge artifact existed on disk BEFORE send.py was invoked
    assert fake.artifact_present_at_call == [[nudge.name]]
    # and send.py was invoked as the transport, with recipient + body
    assert fake.calls == [[str(magic_pane.SEND_PY), "send", "pi", "cross body"]]
    import json
    payload = json.loads(nudge.read_text())
    assert payload["from"] == "grok-bot"
    assert payload["to"] == "pi"
    assert payload["sha256"] == hashlib.sha256(b"cross body").hexdigest()


def test_deliver_same_harness_native_no_send_py(monkeypatch):
    fake = FakeRun()
    monkeypatch.setattr(magic_pane.subprocess, "run", fake)
    out = magic_pane.deliver("grok-bot", "grok-bot", "same body",
                             pane_target="agi:0.1")
    assert out["path"] == "native"
    assert [c[0] for c in fake.calls] == ["tmux"]
    assert not any("send.py" in str(tok) for c in fake.calls for tok in c)


def test_deliver_cross_harness_nudge_before_send_py(tmp_path, monkeypatch):
    fake = FakeRun(nudge_dir=tmp_path)
    monkeypatch.setattr(magic_pane.subprocess, "run", fake)
    out = magic_pane.deliver("grok-bot", "pi", "cross body", nudge_dir=tmp_path)
    assert out["path"] == "nudge_send"
    nudge = Path(out["nudge"])
    assert nudge.exists()
    assert fake.artifact_present_at_call == [[nudge.name]]
    assert fake.calls == [[str(magic_pane.SEND_PY), "send", "pi", "cross body"]]


def test_deliver_cross_harness_never_native(tmp_path, monkeypatch):
    fake = FakeRun()
    monkeypatch.setattr(magic_pane.subprocess, "run", fake)
    magic_pane.deliver("grok-bot", "pi", "cross body", nudge_dir=tmp_path)
    assert [c[0] for c in fake.calls if c[0] == "tmux"] == []


def test_deliver_native_missing_pane_raises_and_runs_nothing(monkeypatch):
    fake = FakeRun()
    monkeypatch.setattr(magic_pane.subprocess, "run", fake)
    try:
        magic_pane.deliver("grok-bot", "grok-bot", "body", pane_target=None)
        raise AssertionError("expected ValueError")
    except ValueError as e:
        assert "pane_target" in str(e)
    assert fake.calls == []


def test_import_audit_no_orchestration_and_no_grok_literal():
    src = (BIN / "magic_pane.py").read_text()
    for forbidden in ("import rotate", "import dispatch",
                      "from rotate", "from dispatch"):
        assert forbidden not in src, forbidden
    assert '"grok"' not in src and "'grok'" not in src
