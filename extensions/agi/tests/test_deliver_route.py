"""Focused falsifier for the one-decision messaging seam."""
from __future__ import annotations

import importlib.util
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
spec = importlib.util.spec_from_file_location("send_route", BIN / "send.py")
send = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send)


def test_deliver_selects_one_transport_and_passes_decision():
    calls = []
    native = lambda text, decision: calls.append(("native", text, decision)) or "native"
    cross = lambda text, decision: calls.append(("cross", text, decision)) or "cross"

    assert send.deliver("a", "a", "same", native=native, cross=cross) == "native"
    assert send.deliver("a", "b", "cross", native=native, cross=cross) == "cross"
    assert calls == [("native", "same", "native"),
                      ("cross", "cross", "send.py")]


def test_empty_identity_is_not_same_harness():
    calls = []
    native = lambda text, decision: calls.append("native") or "native"
    cross = lambda text, decision: calls.append("cross") or "cross"

    assert send.deliver("", "", "empty", native=native, cross=cross) == "cross"
    assert calls == ["cross"]
