"""Optional pane surface on the ONE grok adapter. `goal:g7.32.3`.

The pane methods are OPTIONAL: discovered by `hasattr`, never in
`adapters.REQUIRED`, and absent from harnesses without panes. They WRAP the
durable hold of `goal:g7.31.1` (a held pane is a tmux name) and fail CLOSED
with a NAMED `PaneNotHeldError` — they never hang and never open a fresh pane.
One module for grok: no `grok_pane_adapter.py`.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402
from adapters import grok_bot_adapter as grok  # noqa: E402


@pytest.fixture(autouse=True)
def _fresh_hold():
    """Module hold state is process-global; each test starts unheld."""
    grok._ATTACHED_PANES.clear()
    yield
    grok._ATTACHED_PANES.clear()


class FakeRunner:
    def __init__(self):
        self.calls = []

    def __call__(self, argv):
        self.calls.append(list(argv))

        class _CP:
            stdout = "pane text\n"

        return _CP()


# ------------------------------------------------- feature-detect / one module


def test_pane_methods_are_optional_and_feature_detected():
    assert hasattr(grok, "pane_attach")
    assert hasattr(grok, "pane_send")
    assert hasattr(grok, "pane_read")
    # Harnesses WITHOUT panes simply omit them.
    assert not hasattr(adapters.load("pi"), "pane_attach")
    assert not hasattr(adapters.load("claude_code"), "pane_attach")


def test_pane_methods_are_not_part_of_the_required_surface():
    assert not set(adapters.REQUIRED) & {"pane_attach", "pane_send", "pane_read"}
    assert adapters.load("grok_bot") is grok


def test_exactly_one_grok_adapter_module_exists():
    d = BIN / "adapters"
    assert not (d / "grok_pane_adapter.py").exists()
    assert sorted(p.name for p in d.glob("grok*_adapter.py")) == \
        ["grok_bot_adapter.py"]


# ------------------------------------------------------- fail closed, no hang


def test_no_held_pane_raises_the_named_error_for_every_pane_method():
    for call in (lambda: grok.pane_attach(None, harness={}, seat="seat-a"),
                 lambda: grok.pane_send("hi", None, harness={}, seat="seat-a"),
                 lambda: grok.pane_read(None, harness={}, seat="seat-a")):
        with pytest.raises(grok.PaneNotHeldError) as exc:
            call()
        assert isinstance(exc.value, RuntimeError)
        assert "seat-a" in str(exc.value)


def test_send_read_fail_closed_when_named_but_not_attached():
    """A pane NAME alone is not a hold; attach must have happened."""
    for call in (lambda: grok.pane_send("hi", "s"),
                 lambda: grok.pane_read("s")):
        with pytest.raises(grok.PaneNotHeldError):
            call()


def test_no_held_pane_never_shells_tmux_and_never_opens_a_pane():
    runner = FakeRunner()
    with pytest.raises(grok.PaneNotHeldError):
        grok.pane_attach(None, harness={}, seat="seat-a", runner=runner)
    assert runner.calls == [], "a fresh pane was shelled for an unheld seat"


def test_failure_does_not_hang_under_a_short_timeout():
    """The call must raise, not block — run it in a subprocess with a bound."""
    code = (
        "import sys; sys.path.insert(0, %r)\n"
        "import adapters.grok_bot_adapter as g\n"
        "try:\n"
        "    g.pane_read(None, harness={}, seat='s')\n"
        "except g.PaneNotHeldError:\n"
        "    print('raised')\n" % str(BIN)
    )
    env = {**os.environ, "PYTHONPATH": str(BIN)}
    cp = subprocess.run([sys.executable, "-c", code], capture_output=True,
                        text=True, timeout=15, env=env)
    assert cp.returncode == 0, cp.stderr
    assert "raised" in cp.stdout


# ----------------------------------------------------- real tmux wiring


def test_attach_is_idempotent_and_targets_the_config_pane_cell():
    runner = FakeRunner()
    h = {"pane": {"seat-a": "grok-seat-a"}, "tmux_session": "agi-rc"}
    first = grok.pane_attach(harness=h, seat="seat-a", runner=runner)
    second = grok.pane_attach(harness=h, seat="seat-a", runner=runner)
    assert first == second == "grok-seat-a"
    # ONE select-window call: a repeat never opens a second pane.
    assert runner.calls == [["select-window", "-t", "agi-rc:grok-seat-a"]]


def test_session_falls_back_to_a_bare_name_never_a_home_literal():
    runner = FakeRunner()
    grok.pane_attach("s", runner=runner)
    assert runner.calls == [[
        "select-window", "-t", f"{grok.DEFAULT_TMUX_SESSION}:s"]]
    assert "/home/" not in grok.DEFAULT_TMUX_SESSION


def test_send_and_read_reach_the_held_pane():
    runner = FakeRunner()
    h = {"pane": "seat-a", "tmux_session": "agi-rc"}
    grok.pane_attach(harness=h, runner=runner)
    assert grok.pane_send("ping", harness=h, runner=runner) is True
    assert grok.pane_read(harness=h, runner=runner) == "pane text\n"
    assert runner.calls[-2] == [
        "send-keys", "-t", "agi-rc:seat-a", "ping", "Enter"]
    assert runner.calls[-1] == [
        "capture-pane", "-p", "-J", "-t", "agi-rc:seat-a"]


def test_string_pane_cell_is_the_single_held_pane():
    runner = FakeRunner()
    assert grok.pane_attach(harness={"pane": " the-pane "},
                            runner=runner) == "the-pane"
    assert runner.calls[0][-1] == "agi-rc:the-pane"