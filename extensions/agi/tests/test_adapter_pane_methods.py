"""goal:g7.32.3 — optional pane methods on ONE adapter, absent elsewhere.

The falsifier, stated as tests: a single declared optional-pane interface on
the adapter layer, grok-bot DEFINING it and pi OMITTING it, no held pane
failing closed with a named error, and still exactly one grok adapter file.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402

grok = adapters.load("grok_bot")
pi = adapters.load("pi")


class FakeRunner:
    """Injectable tmux seam — records argv, never touches a live server."""

    def __init__(self, returncode: int = 0, stdout: str = ""):
        self.calls: list[list[str]] = []
        self._rc, self._stdout = returncode, stdout

    def __call__(self, args):
        self.calls.append(args)
        return type("Result", (), {"returncode": self._rc, "stdout": self._stdout})


def test_interface_is_declared_once_on_the_adapter_layer():
    assert adapters.OPTIONAL_PANE == ("pane_attach", "pane_send", "pane_read")
    assert adapters.pane_interface(grok) == adapters.OPTIONAL_PANE


def test_pi_omits_every_optional_pane_method():
    assert adapters.pane_interface(pi) == ()
    for fn in adapters.OPTIONAL_PANE:
        assert hasattr(pi, fn) is False, fn


def test_grok_defines_every_optional_pane_method():
    for fn in adapters.OPTIONAL_PANE:
        assert callable(getattr(grok, fn)), fn


@pytest.mark.parametrize("fn", adapters.OPTIONAL_PANE)
def test_no_held_pane_fails_closed_with_a_named_error(fn):
    with pytest.raises(adapters.PaneNotHeld) as exc:
        getattr(grok, fn)(pane=None, runner=FakeRunner())
    assert "pane" in str(exc.value).lower()


def test_pane_send_routes_through_the_injected_runner():
    r = FakeRunner()
    grok.pane_send(pane="%3", text="hello", runner=r)
    assert r.calls == [["send-keys", "-t", "%3", "hello", "Enter"]]


def test_pane_read_returns_the_runner_stdout():
    assert grok.pane_read(pane="%3", runner=FakeRunner(stdout="lines")) == "lines"


def test_pane_attach_reports_liveness_from_the_runner():
    assert grok.pane_attach(pane="%3", runner=FakeRunner(returncode=0))["live"] is True


def test_exactly_one_grok_adapter_module():
    hits = sorted(p.name for p in (BIN / "adapters").glob("*grok*"))
    assert hits == ["grok_bot_adapter.py"]
