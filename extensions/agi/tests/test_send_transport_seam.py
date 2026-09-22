"""goal:g7.32.4 falsifier 2 — the `send` verb selects a transport from a
runtime-extensible table, so adding a transport is a new module + a
register_transport(...) row, never a new channel-specific `if` in send.py.

The testable claim: a NEW transport registered at run time (no edit to
send.py's selection loop) is selected and dispatched by `_route_send`, and
the three built-in channels keep their order (room -> dm -> inbox).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

spec = importlib.util.spec_from_file_location("send", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)


@pytest.fixture
def registry():
    """Snapshot/restore the transport table so a test's registration cannot
    leak into another test (the table is module-global state)."""
    saved = list(send_mod.SEND_TRANSPORTS)
    yield
    send_mod.SEND_TRANSPORTS[:] = saved


def _args(**kw) -> SimpleNamespace:
    base = dict(room=None, dm_to=None, send_args=[], quote_harness=False)
    base.update(kw)
    return SimpleNamespace(**base)


def test_new_transport_selected_without_editing_send(registry):
    """A brand-new channel registered at run time is chosen by the generic
    loop -- the falsifier: no edit to send.py's selection logic."""
    calls = []

    def matches(a):
        return getattr(a, "fake_channel", None) == "carrier-pigeon"

    def handler(root, croot, args, sender):
        calls.append((args.fake_channel, sender))
        return 0

    send_mod.register_transport("carrier-pigeon", matches, handler, priority=1)

    rc = send_mod._route_send(Path("/nonexistent-r"), Path("/nonexistent-c"),
                              _args(fake_channel="carrier-pigeon"), "me")
    assert rc == 0
    assert calls == [("carrier-pigeon", "me")]

    # It wins even when the catch-all inbox matcher would also fire.
    rc = send_mod._route_send(Path("/nonexistent-r"), Path("/nonexistent-c"),
                              _args(fake_channel="carrier-pigeon",
                                    send_args=["someone", "hi"]), "me")
    assert rc == 0
    assert calls[-1] == ("carrier-pigeon", "me")


def test_builtin_rows_point_at_their_cli_handlers(registry):
    rows = {name: handler for name, _matches, handler in send_mod.SEND_TRANSPORTS}
    assert rows["room"] is send_mod._send_room_cli
    assert rows["dm"] is send_mod._send_dm_cli
    assert rows["inbox"] is send_mod._send_inbox_cli


def test_selection_order_is_room_then_dm_then_inbox(registry):
    seen = []
    spied = [
        (name, matches,
         (lambda n: (lambda *a, **k: seen.append(n) or 0))(name))
        for name, matches, _handler in send_mod.SEND_TRANSPORTS
    ]
    send_mod.SEND_TRANSPORTS[:] = spied

    send_mod._route_send(None, None, _args(room="r", dm_to="d",
                                           send_args=["hi"]), "me")
    assert seen == ["room"]
    seen.clear()
    send_mod._route_send(None, None, _args(dm_to="d", send_args=["hi"]), "me")
    assert seen == ["dm"]
    seen.clear()
    send_mod._route_send(None, None, _args(send_args=["someone", "hi"]), "me")
    assert seen == ["inbox"]


def test_no_matching_transport_returns_1(registry):
    """A table with no match (the catch-all removed) refuses cleanly."""
    send_mod.SEND_TRANSPORTS[:] = [
        ("never", lambda a: False, lambda *a, **k: 0)]
    assert send_mod._route_send(None, None, _args(), "me") == 1