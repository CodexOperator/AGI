from __future__ import annotations

import pytest

import magic_pane


@pytest.mark.parametrize("bogus", ["bridge", None, 0, ""])
def test_deliver_refuses_unrecognised_route(monkeypatch, bogus):
    """A gate that delivers on a decision it does not understand is a default."""
    sent = []
    monkeypatch.setattr(magic_pane, "route", lambda *_: bogus)
    monkeypatch.setattr(magic_pane, "cross_send", lambda *a, **k: sent.append("cross") or 0)
    monkeypatch.setattr(magic_pane, "native_send", lambda *a, **k: sent.append("native") or True)
    with pytest.raises(magic_pane.UnknownRoute) as exc:
        magic_pane.deliver("a", "b", "hello", target="seat")
    assert exc.value.decision is bogus
    assert sent == [], "refusal must precede any transport"


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
