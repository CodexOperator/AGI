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


class _TmuxShim:
    """Handle to the recording PATH `tmux` installed by `tmux_shim`.

    `expect_clean` is the teardown guard's switch: it stays True for every
    test (the autouse `_no_real_tmux` fixture fails the test if the log
    exists), and the ONE non-vacuity test sets it False because driving a
    genuine tmux call is that test's whole point.
    """

    def __init__(self, log: Path):
        self.log = log
        self.expect_clean = True

    def exists(self) -> bool:
        return self.log.exists()

    def text(self) -> str:
        return self.log.read_text() if self.log.exists() else ""


@pytest.fixture
def tmux_shim(tmp_path, monkeypatch) -> _TmuxShim:
    """A PATH `tmux` that RECORDS every real invocation and returns nonzero.

    Residue closure: `_list_windows` (send.py:2112) shells out to
    `tmux list-windows`; the test must assert that seam is NEVER reached,
    not merely hope the fixture rows keep it unreachable. The shim is
    scoped by `monkeypatch` (PATH + tmp dir), so it cannot leak. The
    autouse `_no_real_tmux` fixture requests this one, so EVERY test in the
    module runs under the shim -- not only the tests that name it.
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
    return _TmuxShim(log)


@pytest.fixture(autouse=True)
def _no_real_tmux(tmux_shim):
    """GLOBAL closure (MUR residue #2): the no-real-tmux property is a
    property of the MODULE, not of the three tests that happened to request
    the shim. This fixture forces the shim onto PATH for every test and, at
    teardown, fails the test if any code path shelled out to real tmux.
    A stub-only test (`_list_windows` never reachable) still passes -- the
    log stays absent -- but a future seam that forgets to stub fails HERE.
    """
    yield
    if tmux_shim.expect_clean:
        assert not tmux_shim.log.exists(), (
            "a code path shelled out to real tmux: " + tmux_shim.text())


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
    # Module carries no un-stubbed tmux seam: the by-name fallback
    # (`_window_listed` -> real `list-windows`) is stubbed here too, so this
    # test cannot reach real tmux even if a row loses its `@id`.
    monkeypatch.setattr(send, "_window_listed", lambda *a, **k: True)

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


def test_router_has_no_rotation_or_dispatch_import():
    """The lifecycle adapter owns those imports; the public router does not."""
    tree = ast.parse((BIN / "send.py").read_text(encoding="utf-8"))
    forbidden = {"rotate", "dispatch"}
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert imported.isdisjoint(forbidden)


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


# NON-VACUITY GUARD (MUR residue #2, #2a): the autouse teardown above is
# only meaningful if the shim CAN record a genuine tmux call. Drive the REAL
# `send._list_windows` with the shim on PATH and require the log to exist
# and name `list-windows`; without this, `assert not log.exists()` could be
# true because the shim never works at all. This is the one test that opts
# out of the teardown guard (`expect_clean = False`), because the real call
# is the point -- and it asserts the recorded call itself.
def test_tmux_shim_records_a_real_list_windows_call(tmux_shim):
    tmux_shim.expect_clean = False
    assert send._list_windows("some-session") == []   # shim exits 1
    assert tmux_shim.log.exists()
    assert "list-windows" in tmux_shim.text()


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