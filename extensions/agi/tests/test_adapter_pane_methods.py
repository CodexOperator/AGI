"""Optional pane methods on ONE adapter (goal:g7.32.3).

The optional surface lives on `grok_bot_adapter` behind feature detection:
`adapters.pane_interface(grok) == adapters.OPTIONAL_PANE` and
`pane_interface(pi) == ()`. Required surface (`adapters.REQUIRED`, goal:g7.25)
is untouched. No tmux server is needed: the `runner=` seam is the only place a
tmux call goes, so the suite injects fakes. Every failure mode -- no held pane,
dead target (rc != 0), OSError, timeout -- must raise the NAMED
`adapters.PaneNotHeld`, never return a silent value.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402

grok = adapters.load("grok_bot")
pane_free = [adapters.load(n) for n in ("pi", "claude_code", "copilot_cli")]

METHODS = ("pane_attach", "pane_send", "pane_read")


class Result:
    def __init__(self, returncode=0, stdout=""):
        self.returncode = returncode
        self.stdout = stdout


def ok(returncode=0, stdout="%3"):
    return lambda argv: Result(returncode, stdout)


# --------------------------------------------------------- feature detection

def test_optional_names_declared_once_and_not_required():
    assert adapters.OPTIONAL_PANE == METHODS
    assert all(m not in adapters.REQUIRED for m in adapters.OPTIONAL_PANE)


def test_pane_interface_reports_grok_present_and_pi_absent():
    assert adapters.pane_interface(grok) == METHODS
    for mod in pane_free:
        assert adapters.pane_interface(mod) == ()
        assert hasattr(mod, "pane_send") is False


def test_required_surface_unchanged():
    assert adapters.REQUIRED == ("build_command", "child_env", "is_alive",
                                 "restart", "needs_credential")


def test_still_exactly_one_adapter_module_for_grok_bot():
    matches = sorted(p.name for p in (BIN / "adapters").glob("*grok*_adapter.py"))
    assert matches == ["grok_bot_adapter.py"], matches


# --------------------------------------------- fail closed with no held pane

@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("handle", [None, "", "   "])
def test_no_held_pane_raises_named_error_before_tmux(method, handle):
    def boom(argv):
        raise AssertionError("tmux was reached with no held pane")

    with pytest.raises(adapters.PaneNotHeld):
        getattr(grok, method)(pane=handle, runner=boom)


@pytest.mark.parametrize("method", METHODS)
def test_malformed_handle_is_not_a_held_pane(method):
    for handle in (7, True, ["%3"], {"pane": "%3"}):
        with pytest.raises(adapters.PaneNotHeld):
            getattr(grok, method)(pane=handle, runner=ok())


# ------------------------------------------------- dead / unresolved target

@pytest.mark.parametrize("method", METHODS)
def test_dead_target_returncode_raises_named_error(method):
    """A target tmux answers non-zero for is DEAD, not silently `live: False`."""
    with pytest.raises(adapters.PaneNotHeld):
        getattr(grok, method)(pane="%3", runner=ok(returncode=1))


@pytest.mark.parametrize("method", METHODS)
def test_oserror_from_runner_raises_named_error(method):
    def boom(argv):
        raise OSError("no tmux server")

    with pytest.raises(adapters.PaneNotHeld):
        getattr(grok, method)(pane="%3", runner=boom)


@pytest.mark.parametrize("method", METHODS)
def test_timeout_from_runner_raises_named_error(method):
    def slow(argv):
        raise subprocess.TimeoutExpired(argv, 5)

    with pytest.raises(adapters.PaneNotHeld):
        getattr(grok, method)(pane="%3", runner=slow)


# ------------------------------------------------- wrap a resolved pane

def test_pane_attach_returns_live_dict_on_success():
    assert grok.pane_attach(pane=" %3 ", runner=ok()) == {"pane": "%3",
                                                          "live": True}


def test_pane_send_targets_the_pane_with_real_bytes():
    seen = {}

    def fake(argv):
        seen["argv"] = argv
        return Result()

    grok.pane_send(pane="%3", text="ping", runner=fake)
    assert seen["argv"] == ["send-keys", "-t", "%3", "ping", "Enter"]


def test_pane_read_returns_captured_stdout():
    assert grok.pane_read(pane="%7", runner=ok(stdout="hi\n")) == "hi\n"
