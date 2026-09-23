"""Tests for the magic-pane messaging router (goal:g7.32.2).

Conjunct 1: same-harness native delivery types into the recipient's @id
window and NEVER invokes the send.py transport.
Conjunct 2: routing classifies by harness.
Conjunct 3: messaging.py imports neither rotate nor dispatch.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

_BIN = Path(__file__).resolve().parents[1] / "bin"
if str(_BIN) not in sys.path:
    sys.path.insert(0, str(_BIN))

import messaging  # noqa: E402
import send  # noqa: E402


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps({}))
    (root / "nodes" / ".geometry").mkdir(parents=True)
    return root


def _posts_md(rows, default_box: str = "") -> str:
    lines = ["---", "id: config:posts", "type: config"]
    if default_box:
        lines.append(f"default_box: {default_box}")
    lines.append("posts:")
    for r in rows:
        lines.append("  - " + json.dumps(r))
    lines.append("---")
    return "\n".join(lines) + "\n"


def _write_posts(root: Path, rows, default_box: str = "") -> None:
    (root / "nodes" / ".geometry" / "posts.md").write_text(
        _posts_md(rows, default_box))


def _fake_tmux(monkeypatch):
    """Record every tmux argv; no live session, no real sleep."""
    calls: list[list[str]] = []

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(list(cmd))
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(messaging.subprocess, "run", fake_run)
    monkeypatch.setattr(messaging.time, "sleep", lambda _s: None)
    return calls


def _instrument_transport(monkeypatch):
    """Record ANY call to send.py's transport; we assert the record is empty."""
    records: list[str] = []
    for name in ("send_dm", "_nudge_window", "_nudge_target"):
        monkeypatch.setattr(
            send, name,
            (lambda n: lambda *a, **k: records.append(n))(name))
    return records


def _typed(calls):
    return [c for c in calls if c[:3] == ["tmux", "send-keys", "-l"]]


def _enters(calls):
    return [c for c in calls
            if c[:2] == ["tmux", "send-keys"] and c[-1] == "Enter"]


def test_native_types_to_at_id_and_never_calls_send_transport(
        project: Path, monkeypatch):
    """Conjunct 1, wire: the changed bytes reach <session>:@id; zero send.py."""
    _write_posts(project, [{"name": "grok-a", "harness": "grok",
                            "window": "@246", "pid": 4242}])
    calls = _fake_tmux(monkeypatch)
    transport = _instrument_transport(monkeypatch)

    result = messaging.native_send(project, "grok-a", "hello-b")

    assert result["path"] == "native"
    assert result["target"] == "agi-rc:@246"
    assert result["typed"] == len("hello-b")
    assert [c[5] for c in _typed(calls)] == ["hello-b"]
    assert _typed(calls)[0][4] == "agi-rc:@246"
    assert len(_enters(calls)) == 1
    assert transport == []            # never shells out to send.py transport


def test_route_classifies_by_harness():
    """Conjunct 2, gate."""
    assert messaging.route("grok-bot", "grok-bot") == "native"
    assert messaging.route("grok-bot", "claude-code") == "nudge-send"
    assert messaging.route("  Grok-Bot  ", "grok-bot") == "native"  # ws+case
    assert messaging.route("", "") == "nudge-send"                  # never native
    assert messaging.route("   ", "\t") == "nudge-send"


def test_fail_closed_without_addressable_window(project: Path, monkeypatch):
    """Conjunct 1, auth: no row / no window / a NAME window -> refuse, type 0."""
    for rows, seat in (
        ([{"name": "grok-a", "harness": "grok"}], "grok-a"),        # no window
        ([{"name": "grok-a", "window": "grok-a"}], "grok-a"),       # a NAME
        ([{"name": "other", "window": "@1"}], "grok-a"),            # no row
    ):
        _write_posts(project, rows)
        calls = _fake_tmux(monkeypatch)
        with pytest.raises(messaging.NoAddressableWindow):
            messaging.native_send(project, seat, "should-not-type")
        assert calls == []


def test_fail_closed_on_foreign_box_row(project: Path, monkeypatch):
    """A row whose box is not this box is not addressable here."""
    monkeypatch.setenv("AGI_BOX", "here")
    _write_posts(project, [{"name": "grok-a", "window": "@246",
                            "box": "elsewhere"}], default_box="here")
    calls = _fake_tmux(monkeypatch)
    with pytest.raises(messaging.NoAddressableWindow):
        messaging.native_send(project, "grok-a", "nope")
    assert calls == []


def test_module_imports_neither_rotate_nor_dispatch():
    """Conjunct 3, grep on this module's OWN import list, not transitivity."""
    path = _BIN / "messaging.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    mods: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module.split(".")[0])
    assert "rotate" not in mods
    assert "dispatch" not in mods


def test_cross_send_emits_ordered_nudge_then_send_dm_trace(
        project: Path, monkeypatch):
    """Conjunct 2, gate/wire: the cross-harness path is ONE ordered trace,
    pane-intent nudge FIRST, send.py transport SECOND, carrying the body."""
    _write_posts(project, [{"name": "claude-a", "harness": "claude-code",
                            "window": "@77", "pid": 77}])
    tmux = _fake_tmux(monkeypatch)
    trace: list[str] = []

    real_intent = messaging._pane_intent

    def traced_intent(*a, **k):
        trace.append("nudge")
        return real_intent(*a, **k)

    def fake_send_dm(croot, me, other, text, sender, quote_harness=False):
        trace.append("send_dm")
        trace.append(text)
        return croot / f"{me}--{other}.md"

    monkeypatch.setattr(messaging, "_pane_intent", traced_intent)
    monkeypatch.setattr(send, "send_dm", fake_send_dm)

    result = messaging.cross_send(project, "claude-a", "hello-pi",
                                  sender="grok-a")

    assert result["path"] == "nudge-send"
    assert trace[:2] == ["nudge", "send_dm"]        # measured order
    assert trace[2] == "hello-pi"                    # body to the transport
    assert result["events"] == ["nudge", "send_dm"]  # returned trace agrees
    assert result["nudge"]["pane"] == "agi-rc:@77"
    assert tmux == []            # intent is RECORDED, never typed: no body, no keys


def test_cross_send_never_claims_native_and_types_no_body(
        project: Path, monkeypatch):
    """Conjunct 2, auth: cross-harness records ZERO native_send calls and
    never types the body with `tmux send-keys -l`."""
    _write_posts(project, [{"name": "claude-a", "harness": "claude-code",
                            "window": "@77", "pid": 77}])
    calls = _fake_tmux(monkeypatch)
    native: list[str] = []
    monkeypatch.setattr(messaging, "native_send",
                        lambda *a, **k: native.append("native_send"))
    monkeypatch.setattr(send, "send_dm",
                        lambda *a, **k: project / "x.md")

    messaging.cross_send(project, "claude-a", "secret-body", sender="grok-a")

    assert native == []
    assert _typed(calls) == []                   # no `send-keys -l` at all
    assert all("secret-body" not in c for c in calls)


def test_cross_send_records_intent_when_seat_has_no_window(
        project: Path, monkeypatch):
    """A windowless recipient is still deliverable via the dm file; the pane
    intent records pane=None rather than refusing (best-effort nudge)."""
    _write_posts(project, [{"name": "claude-a", "harness": "claude-code"}])
    _fake_tmux(monkeypatch)
    monkeypatch.setattr(send, "send_dm", lambda *a, **k: project / "x.md")

    result = messaging.cross_send(project, "claude-a", "hi", sender="grok-a")

    assert result["nudge"]["pane"] is None
    assert result["nudge"]["event"] == "nudge"
    assert result["events"] == ["nudge", "send_dm"]


def test_send_magic_same_harness_routes_native_only(
        project: Path, monkeypatch):
    """send_magic, wire: two grok-bot rows -> native typing, ZERO send_dm."""
    _write_posts(project, [
        {"name": "grok-a", "harness": "grok-bot", "window": "@11", "pid": 11},
        {"name": "grok-b", "harness": "grok-bot", "window": "@22", "pid": 22},
    ])
    calls = _fake_tmux(monkeypatch)
    transport = _instrument_transport(monkeypatch)

    result = messaging.send_magic(project, "grok-a", "grok-b", "body-native",
                                  sender="grok-a")

    assert result["via_route"] == "native"
    assert result["path"] == "native"
    assert result["from_harness"] == "grok-bot"
    assert result["to_harness"] == "grok-bot"
    assert [c[5] for c in _typed(calls)] == ["body-native"]
    assert _typed(calls)[0][4] == "agi-rc:@22"
    assert transport == []                       # ONLY the native path ran


def test_send_magic_different_harness_routes_cross_only(
        project: Path, monkeypatch):
    """send_magic, gate: grok-bot -> claude-code -> send_dm, ZERO native."""
    _write_posts(project, [
        {"name": "grok-a", "harness": "grok-bot", "window": "@11", "pid": 11},
        {"name": "claude-b", "harness": "claude-code", "window": "@33", "pid": 33},
    ])
    calls = _fake_tmux(monkeypatch)
    native: list[str] = []
    monkeypatch.setattr(messaging, "native_send",
                        lambda *a, **k: native.append("native_send"))
    sent: list[tuple] = []

    def fake_send_dm(croot, me, other, text, sender, quote_harness=False):
        sent.append((me, other, text, sender))
        return croot / f"{me}--{other}.md"

    monkeypatch.setattr(send, "send_dm", fake_send_dm)

    result = messaging.send_magic(project, "grok-a", "claude-b", "body-cross",
                                  sender="grok-a")

    assert result["via_route"] == "nudge-send"
    assert result["path"] == "nudge-send"
    assert result["from_harness"] == "grok-bot"
    assert result["to_harness"] == "claude-code"
    assert native == []                          # ONLY the cross path ran
    assert sent == [("grok-a", "claude-b", "body-cross", "grok-a")]
    assert _typed(calls) == []                   # no native body keystrokes


def test_send_magic_missing_harness_is_never_native(
        project: Path, monkeypatch):
    """send_magic, auth: a recipient row with no `harness` cell routes cross."""
    _write_posts(project, [
        {"name": "grok-a", "harness": "grok-bot", "window": "@11", "pid": 11},
        {"name": "ghost-b", "window": "@44", "pid": 44},        # no harness
    ])
    _fake_tmux(monkeypatch)
    native: list[str] = []
    monkeypatch.setattr(messaging, "native_send",
                        lambda *a, **k: native.append("native_send"))
    monkeypatch.setattr(send, "send_dm", lambda *a, **k: project / "x.md")

    result = messaging.send_magic(project, "grok-a", "ghost-b", "hi")

    assert result["via_route"] == "nudge-send"
    assert result["to_harness"] == ""
    assert native == []


def test_send_magic_missing_sender_harness_is_never_native(
        project: Path, monkeypatch):
    """Both sides need a harness: sender without one routes cross too."""
    _write_posts(project, [
        {"name": "ghost-a", "window": "@11", "pid": 11},        # no harness
        {"name": "ghost-b", "window": "@22", "pid": 22},        # no harness
    ])
    _fake_tmux(monkeypatch)
    native: list[str] = []
    monkeypatch.setattr(messaging, "native_send",
                        lambda *a, **k: native.append("native_send"))
    monkeypatch.setattr(send, "send_dm", lambda *a, **k: project / "x.md")

    result = messaging.send_magic(project, "ghost-a", "ghost-b", "hi")

    assert result["via_route"] == "nudge-send"
    assert native == []
