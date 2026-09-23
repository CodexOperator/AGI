"""Tests for bin/messaging.py — the magic-pane transport-choice seam.

goal:g7.32.2 falsifier, three conjuncts on the returned values / wire bytes:
(1) same-harness native calls the pane seam and NEVER send.py transport;
(2) cross-harness writes the nudge artifact then invokes send.py, in ONE
    trace dict; (3) the module imports no rotate/dispatch internals.
"""
from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

spec = importlib.util.spec_from_file_location("messaging", BIN / "messaging.py")
messaging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(messaging)


def test_route_native_same_harness():
    assert messaging.route("grok-bot", "grok-bot") == "native"


def test_route_nudge_different_harness():
    assert messaging.route("grok-bot", "claude-code") == "nudge"
    assert messaging.route("grok-bot", "pi") == "nudge"


def test_native_calls_pane_seam_and_never_transport(monkeypatch):
    """Conjunct 1: the pane seam is called; subprocess (send.py transport)
    is NEVER invoked on the same-harness path."""
    calls = []
    spy = []

    def seam(seat, text):
        calls.append((seat, text))
        return {"seam": "stub"}

    def spy_run(*a, **k):
        spy.append(a)
        raise AssertionError("native path must not shell out")

    monkeypatch.setattr(messaging.subprocess, "run", spy_run)
    trace = messaging.send_native(seam, seat="grok-b", text="hello")
    assert calls == [("grok-b", "hello")]
    assert spy == []
    assert trace["path"] == "native"
    assert trace["send_py"] is None
    assert trace["seam"] == {"seam": "stub"}


def test_cross_writes_nudge_artifact_and_invokes_send_py(tmp_path):
    """Conjunct 2: the nudge artifact exists AND the same trace dict carries
    the exact send.py argv / return code."""
    marker = tmp_path / "sent.txt"
    send_py = tmp_path / "fake_send.py"
    send_py.write_text(
        "import sys, pathlib\n"
        f"pathlib.Path({str(marker)!r}).write_text(' '.join(sys.argv[1:]))\n"
    )
    nudge_dir = tmp_path / "nudges"
    trace = messaging.send_cross(
        src="grok-bot", dst="claude-code", seat="director", text="ping",
        nudge_dir=nudge_dir, send_py=send_py)

    artifact = Path(trace["nudge_artifact"])
    assert artifact.is_file(), "the nudge artifact must exist on disk"
    assert artifact.parent == nudge_dir
    assert "director" in artifact.read_text()
    # and the ONE trace dict carries the transport invocation
    assert trace["path"] == "nudge"
    assert trace["send_py"]["returncode"] == 0
    argv = trace["send_py"]["argv"]
    assert argv[1] == str(send_py)
    assert argv[2:] == ["send", "director", "ping", "--from", "grok-bot"]
    # the subprocess really ran, with exactly that argv
    assert marker.read_text() == "send director ping --from grok-bot"


def test_cross_records_nonzero_return_code(tmp_path):
    send_py = tmp_path / "fail_send.py"
    send_py.write_text("import sys\nsys.exit(3)\n")
    trace = messaging.send_cross(
        src="grok-bot", dst="pi", seat="kid", text="x",
        nudge_dir=tmp_path / "n", send_py=send_py)
    assert trace["send_py"]["returncode"] == 3


def test_send_native_same_harness_never_shells_send_py(monkeypatch):
    """Unified entrypoint, same harness: path native, ZERO send.py runs."""
    calls = []
    seen = []

    def seam(seat, text):
        calls.append((seat, text))
        return {"seam": "stub"}

    def spy_run(argv, *a, **k):
        seen.append(argv)
        raise AssertionError("same-harness send must not shell out")

    monkeypatch.setattr(messaging.subprocess, "run", spy_run)
    trace = messaging.send("grok-bot", "grok-bot", seat="kid", text="hi",
                           pane_seam=seam)
    assert trace["path"] == "native"
    assert trace["send_py"] is None
    assert calls == [("kid", "hi")]
    assert [a for a in seen if any("send.py" in str(x) for x in a)] == []


def test_send_cross_one_trace_with_artifact_and_send_py(tmp_path):
    """Unified entrypoint, cross harness: ONE trace carries BOTH."""
    marker = tmp_path / "sent.txt"
    send_py = tmp_path / "fake_send.py"
    send_py.write_text(
        "import sys, pathlib\n"
        f"pathlib.Path({str(marker)!r}).write_text(' '.join(sys.argv[1:]))\n")
    nudge_dir = tmp_path / "nudges"
    trace = messaging.send("grok-bot", "claude-code", seat="director",
                           text="ping", nudge_dir=nudge_dir, send_py=send_py)
    assert trace["path"] == "nudge"
    assert Path(trace["nudge_artifact"]).is_file()
    assert trace["send_py"]["returncode"] == 0
    assert marker.read_text() == "send director ping --from grok-bot"


def test_send_cross_without_transport_refuses_by_name(monkeypatch):
    """Cross without nudge_dir/send_py refuses BY NAME, never native."""
    touched = []

    def seam(seat, text):
        touched.append(seat)
        return {"seam": "stub"}

    def spy_run(argv, *a, **k):
        raise AssertionError("refusal must not shell out")

    monkeypatch.setattr(messaging.subprocess, "run", spy_run)
    try:
        messaging.send("grok-bot", "pi", seat="kid", text="x", pane_seam=seam)
    except ValueError as exc:
        msg = str(exc)
    else:
        raise AssertionError("cross without nudge_dir/send_py must refuse")
    assert "nudge_dir" in msg and "send_py" in msg
    assert touched == []


def test_module_imports_no_rotate_or_dispatch_internals():
    """Conjunct 3: the module source imports no rotate/dispatch internals."""
    tree = ast.parse((BIN / "messaging.py").read_text())
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert not any(m == "rotate" or m.startswith("rotate.")
                   for m in imported), imported
    assert not any(m == "dispatch" or m.startswith("dispatch.")
                   for m in imported), imported
    # and no dynamic import of them either (source-level grep as backstop)
    src = (BIN / "messaging.py").read_text()
    for verb in ("import rotate", "import dispatch",
                 "from rotate", "from dispatch"):
        assert verb not in src, verb
