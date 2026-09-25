from __future__ import annotations

import magic_pane


def test_route_is_harness_equality():
    assert magic_pane.route("a", "a") == magic_pane.NATIVE
    assert magic_pane.route("a", "b") == magic_pane.CROSS


def test_deliver_uses_route_result(monkeypatch):
    calls = []
    monkeypatch.setattr(magic_pane, "cross_send", lambda *a, **k: calls.append("cross") or 0)
    monkeypatch.setattr(magic_pane, "native_send", lambda *a, **k: calls.append("native") or True)
    monkeypatch.setattr(magic_pane, "route", lambda *_: magic_pane.CROSS)
    assert magic_pane.deliver("a", "b", "hello", target="seat")[0] == magic_pane.CROSS
    assert calls == ["cross"]
    calls.clear()
    monkeypatch.setattr(magic_pane, "route", lambda *_: magic_pane.NATIVE)
    assert magic_pane.deliver("a", "b", "hello", target="seat")[0] == magic_pane.NATIVE
    assert calls == ["native"]


def test_deliver_calls_route_once(monkeypatch):
    seen = []
    monkeypatch.setattr(magic_pane, "route", lambda a, b: seen.append((a, b)) or magic_pane.NATIVE)
    monkeypatch.setattr(magic_pane, "native_send", lambda *a, **k: True)
    magic_pane.deliver("a", "a", "hello", target="seat")
    assert seen == [("a", "a")]
