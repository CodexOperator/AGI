"""goal:g7.31.4.2 -- the caller-facing send/nudge surface is the SAME for a
local peer and a foreign-box (mesh) peer: same names/args, same result shape,
transport chosen engine-internally, zero `is_ssh` in the caller bodies.
"""
from __future__ import annotations

import ast
import json
import os
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import send  # noqa: E402


def _graph(tmp: Path, rows: list[dict]) -> Path:
    """A minimal graph root (the `.agi` dir) exactly as test_box_guard builds."""
    root = tmp / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / "config.json").write_text("{}\n")
    body = "---\nid: config:posts\ntype: config\ndefault_box: core-town\nposts:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    (root / "nodes" / ".geometry" / "posts.md").write_text(body + "---\n")
    return root


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    monkeypatch.delenv("AGI_BOX", raising=False)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.setenv("AGI_SEAT", "sender")


@pytest.fixture
def tmux_shim(tmp_path, monkeypatch):
    """A PATH `tmux` that RECORDS every real invocation and returns nonzero.

    Residue closure: `_list_windows` (send.py:2112) shells out to
    `tmux list-windows`; the test must assert that seam is NEVER reached,
    not merely hope the fixture rows keep it unreachable. The shim is
    scoped by `monkeypatch` (PATH + tmp dir), so it cannot leak.
    """
    shim_dir = tmp_path / "shim"
    shim_dir.mkdir()
    log = tmp_path / "tmux-invocations.log"
    tmux = shim_dir / "tmux"
    tmux.write_text(
        "#!/bin/sh\n"
        f'echo "$@" >> "{log}"\n'
        "exit 1\n")
    tmux.chmod(0o755)
    monkeypatch.setenv(
        "PATH", f"{shim_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return log


LOCAL = {"name": "local-seat", "pid": 111, "window": "@111"}
FOREIGN = {"name": "far-seat", "pid": 222, "window": "@222",
           "box": "local-town"}


# conjunct 1+2: SAME call, SAME result shape, BOTH land -- transport invisible.
def test_same_send_dm_call_and_result_shape_both_transports(
        tmp_path, monkeypatch):
    root = _graph(tmp_path, [LOCAL, FOREIGN])
    monkeypatch.setattr(send, "_locally_loaded_rows", lambda r: [LOCAL, FOREIGN])
    nudged: list[str] = []
    monkeypatch.setattr(send, "_nudge_window",
                        lambda *a, **k: nudged.append(a[1]) or False)

    p_local = send.send_dm(root, "sender", "local-seat", "hi local", "sender")
    p_far = send.send_dm(root, "sender", "far-seat", "hi far", "sender")

    assert isinstance(p_local, Path) and isinstance(p_far, Path)
    assert p_local.parent == p_far.parent                 # one dm surface
    for p, text in ((p_local, "hi local"), (p_far, "hi far")):
        assert p.exists()
        blocks = send._conv_blocks(p)
        assert len(blocks) == 1
        assert blocks[0]["text"] == text
        assert {"ts", "from", "to"} <= set(blocks[0])      # same block shape
    # One nudge seam, reached by both; the caller named no transport.
    assert nudged == ["local-seat", "far-seat"]


# conjunct 3: the transport decision is engine-internal, not caller-chosen.
def test_transport_decision_is_engine_internal(tmp_path, monkeypatch):
    root = _graph(tmp_path, [LOCAL, FOREIGN])
    monkeypatch.setattr(send, "_locally_loaded_rows", lambda r: [LOCAL, FOREIGN])
    monkeypatch.setattr(send, "_window_id_listed", lambda *a, **k: True)

    assert send._nudge_target(root, "local-seat", None) is not None
    assert send._nudge_target(root, "far-seat", None) is None


# conjunct 4: no `is_ssh` in the caller-facing send/nudge bodies (source bytes).
def test_no_is_ssh_in_caller_facing_send_bodies():
    src = (BIN / "send.py").read_text(encoding="utf-8")
    want = {"send_dm", "send_room", "_nudge_target", "_nudge_window",
            "_announce_nudge"}
    found = [n for n in ast.walk(ast.parse(src))
             if isinstance(n, ast.FunctionDef) and n.name in want]
    assert {f.name for f in found} == want
    for fn in found:
        assert "is_ssh" not in (ast.get_source_segment(src, fn) or ""), fn.name


# conjunct 2, REAL path: send_dm -> REAL _nudge_window -> REAL _nudge_target.
# Only the tmux/capture layer is faked; neither _nudge_window nor
# _nudge_target is stubbed, so the foreign-box refusal is exercised as built.
def test_real_path_refuses_foreign_box_and_reaches_local(
        tmp_path, monkeypatch, capsys, tmux_shim):
    root = _graph(tmp_path, [LOCAL, FOREIGN])
    monkeypatch.setattr(send, "_window_id_listed", lambda *a, **k: True)
    # Residue closure: the by-name fallback (`_window_listed` -> real tmux
    # `list-windows`) is stubbed too, so no branch shells out. `tmux_shim`
    # then ASSERTS the property below instead of assuming it.
    monkeypatch.setattr(send, "_window_listed", lambda *a, **k: True)
    monkeypatch.setattr(send, "_leave_copy_mode", lambda *a, **k: True)
    monkeypatch.setattr(send, "_capture_pane", lambda *a, **k: "")
    monkeypatch.setattr(send, "_registry_status", lambda *a, **k: None)
    typed: list[tuple] = []

    def _fake_send_keys(target, *keys, **kw):
        typed.append((target, keys))
        return True
    monkeypatch.setattr(send, "_send_keys", _fake_send_keys)

    # foreign-box peer: REFUSED by name, and no keystroke reaches any pane.
    p_far = send.send_dm(root, "sender", "far-seat", "hi far", "sender")
    err = capsys.readouterr().err
    assert "FOREIGN box row" in err and "far-seat" in err
    assert typed == []

    # local peer: SAME call, reached, typed into its own pane.
    p_local = send.send_dm(root, "sender", "local-seat", "hi local", "sender")
    assert [t for t, _ in typed] and typed[0][0].endswith(":@111")

    # SAME result shape both peers (the dm record, transport aside).
    assert isinstance(p_far, Path) and isinstance(p_local, Path)
    assert p_far.parent == p_local.parent
    for p, text in ((p_far, "hi far"), (p_local, "hi local")):
        blocks = send._conv_blocks(p)
        assert len(blocks) == 1 and blocks[0]["text"] == text
        assert {"ts", "from", "to"} <= set(blocks[0])

    # The no-real-tmux property is ASSERTED, not assumed: `_list_windows`
    # never ran, so the PATH `tmux` log file does not exist.
    assert not tmux_shim.exists()


# Residue closure: the WINDOWLESS branch is exercised by bytes, not left
# latent. A row with no `window` cell takes the by-name fallback in
# `_nudge_target` (`send.py:2217`), the one path that reaches
# `_window_listed` -> `_list_windows` -> real tmux.
WINDOWLESS = {"name": "ephemeral-seat", "pid": 333}


def test_windowless_row_by_name_fallback_reaches_pane(
        tmp_path, monkeypatch, tmux_shim):
    root = _graph(tmp_path, [LOCAL, FOREIGN, WINDOWLESS])
    monkeypatch.setattr(send, "_locally_loaded_rows",
                        lambda r: [LOCAL, FOREIGN, WINDOWLESS])
    looked_up: list[tuple] = []

    def _fake_window_listed(session, name):
        looked_up.append((session, name))
        return True
    monkeypatch.setattr(send, "_window_listed", _fake_window_listed)
    monkeypatch.setattr(send, "_leave_copy_mode", lambda *a, **k: True)
    monkeypatch.setattr(send, "_capture_pane", lambda *a, **k: "")
    monkeypatch.setattr(send, "_registry_status", lambda *a, **k: None)
    typed: list[tuple] = []
    monkeypatch.setattr(
        send, "_send_keys",
        lambda target, *keys, **kw: typed.append((target, keys)) or True)

    p = send.send_dm(root, "sender", "ephemeral-seat", "hi windowless",
                     "sender")
    # the by-name listing WAS consulted (the latent branch is live here), and
    # a real listed window named after the seat is addressed BY NAME.
    assert looked_up and looked_up[0][1] == "ephemeral-seat"
    assert typed and typed[0][0].endswith(":ephemeral-seat")
    assert isinstance(p, Path) and p.exists()
    assert send._conv_blocks(p)[0]["text"] == "hi windowless"
    # ...and still zero real tmux: the listing was stubbed.
    assert not tmux_shim.exists()


def test_windowless_row_unlisted_is_a_named_no_op(
        tmp_path, monkeypatch, tmux_shim, capsys):
    root = _graph(tmp_path, [LOCAL, FOREIGN, WINDOWLESS])
    monkeypatch.setattr(send, "_locally_loaded_rows",
                        lambda r: [LOCAL, FOREIGN, WINDOWLESS])
    monkeypatch.setattr(send, "_window_listed", lambda *a, **k: False)
    monkeypatch.setattr(send, "_leave_copy_mode", lambda *a, **k: True)
    monkeypatch.setattr(send, "_capture_pane", lambda *a, **k: "")
    monkeypatch.setattr(send, "_registry_status", lambda *a, **k: None)
    typed: list[tuple] = []
    monkeypatch.setattr(
        send, "_send_keys",
        lambda target, *keys, **kw: typed.append((target, keys)) or True)

    p = send.send_dm(root, "sender", "ephemeral-seat", "hi nowhere",
                     "sender")
    assert typed == []                       # windowless+unlisted: no wake
    assert isinstance(p, Path) and p.exists()  # the dm still landed
    assert send._conv_blocks(p)[0]["text"] == "hi nowhere"
    assert not tmux_shim.exists()            # no real tmux, ever