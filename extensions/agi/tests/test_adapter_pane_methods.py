"""Optional pane methods on ONE adapter (goal:g7.32.3).

The optional surface lives on `grok_bot_adapter` behind feature detection:
`hasattr(mod, "pane_send")` is True for grok and False for every harness with
no panes. Required surface (`adapters.REQUIRED`) is untouched, so this file
asserts absence as well as presence. No live tmux is needed: the fail-closed
test proves the named error fires BEFORE any subprocess, and the send/read
tests capture the argv with a fake `subprocess.run`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402

grok = adapters.load("grok_bot")

PANE_NAMES = ("pane_send", "pane_read", "has_pane", "held_pane_id",
              "NoHeldPaneError")


# --------------------------------------------------------- feature detection

def test_grok_adapter_exposes_the_optional_pane_surface():
    for name in PANE_NAMES:
        assert hasattr(grok, name), name
    assert callable(grok.pane_send) and callable(grok.pane_read)
    assert callable(grok.has_pane) and callable(grok.held_pane_id)
    assert issubclass(grok.NoHeldPaneError, RuntimeError)


@pytest.mark.parametrize("name", ["pi", "claude_code", "copilot_cli"])
def test_pane_free_harnesses_omit_the_optional_surface(name):
    """Absence is the feature: a harness without panes must not pretend."""
    mod = adapters.load(name)
    for pane_name in PANE_NAMES:
        assert not hasattr(mod, pane_name), f"{name} gained {pane_name}"


def test_pane_names_are_not_in_the_required_surface():
    """Optional stays optional -- adding them to REQUIRED would make every
    pane-free adapter unloadable."""
    for pane_name in PANE_NAMES:
        assert pane_name not in adapters.REQUIRED


# ------------------------------------------------------ fail closed, no hang

def test_pane_send_with_no_held_pane_raises_the_named_error(monkeypatch):
    """Fail closed promptly and BY NAME, and never reach tmux (a tmux call
    without a target is exactly the hang this guards)."""
    def boom(*a, **kw):
        raise AssertionError("tmux was reached with no held pane")

    monkeypatch.setattr(grok.subprocess, "run", boom)
    for handle in (None, "", "   ", {}, {"pane": ""}, {"pane": None}, 7):
        with pytest.raises(grok.NoHeldPaneError):
            grok.pane_send(handle, "hello")


def test_pane_read_with_no_held_pane_raises_the_named_error(monkeypatch):
    monkeypatch.setattr(grok.subprocess, "run",
                        lambda *a, **kw: pytest.fail("tmux reached"))
    with pytest.raises(grok.NoHeldPaneError):
        grok.pane_read(None)


def test_has_pane_is_the_feature_predicate_and_never_raises():
    assert grok.has_pane({"pane": "%3"}) is True
    assert grok.has_pane("%3") is True
    assert grok.has_pane(None) is False
    assert grok.has_pane({"pane": ""}) is False


# -------------------------------------------- wrap a held pane (argv proof)

def test_pane_send_wraps_the_held_pane_with_real_bytes(monkeypatch):
    captured = {}

    def fake_run(args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs

        class P:
            stdout = ""
        return P()

    monkeypatch.setattr(grok.subprocess, "run", fake_run)
    grok.pane_send({"pane": "%3"}, "ping")
    assert captured["args"] == ["tmux", "send-keys", "-t", "%3", "--", "ping",
                                "Enter"]
    assert captured["kwargs"]["check"] is True


def test_pane_read_returns_captured_output(monkeypatch):
    def fake_run(args, **kwargs):
        class P:
            stdout = "hello from the pane\n"
        return P()

    monkeypatch.setattr(grok.subprocess, "run", fake_run)
    assert grok.pane_read("%7", lines=42) == "hello from the pane\n"


# ---------------------------------------------------- still ONE adapter file

def test_still_exactly_one_adapter_module_for_grok_bot():
    """No second `grok_pane_adapter.py`: the optional methods live in the one
    file that already exists."""
    matches = sorted(p.name for p in (BIN / "adapters").glob("*grok*_adapter.py"))
    assert matches == ["grok_bot_adapter.py"], matches


def test_required_surface_is_unchanged():
    assert adapters.REQUIRED == ("build_command", "child_env", "is_alive",
                                 "restart", "needs_credential")
