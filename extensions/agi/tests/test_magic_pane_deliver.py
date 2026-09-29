"""The committed suite a `deliver()` without `route()` CANNOT pass.

`goal:g7.32.2.1.1`. The parent MUR's near-miss: committed tests vary harness
strings rather than asserting the transport is chosen SOLELY from `route()`,
so an inlined-equality `deliver()` stays green.

The near-miss shape is deliberately present here AS a test
(`test_near_miss_varying_harness_strings_stays_green`) so the falsifier run
has something to measure: that test is green against the mutant, the rest
are red. A suite where nothing survives the mutant would prove nothing about
the near-miss.
"""
from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
if str(BIN) not in sys.path:
    sys.path.insert(0, str(BIN))

# Loaded by path: this is a messaging leaf, not a spawn adapter, so
# `adapters.load()` is the wrong door (it checks build_command/child_env).
_PANE = BIN / "adapters" / "magic_pane.py"
_spec = importlib.util.spec_from_file_location("magic_pane", _PANE)
magic_pane = importlib.util.module_from_spec(_spec)
sys.modules["magic_pane"] = magic_pane
_spec.loader.exec_module(magic_pane)


# ------------------------------------------- the near-miss (green on mutant)


def test_near_miss_varying_harness_strings_stays_green():
    """Weak BY CONSTRUCTION -- this is the near-miss the parent found."""
    assert magic_pane.deliver("grok", "grok", "hi") == magic_pane.NATIVE
    assert magic_pane.deliver("grok", "claude", "hi") == magic_pane.NUDGE
    assert magic_pane.deliver("grok", "pi", "hi") == magic_pane.NUDGE
    assert magic_pane.deliver("claude", "grok", "hi") == magic_pane.UNSUPPORTED


# --------------------------------------- the load-bearing tests (red on mutant)


def test_contradicted_route_decides_transport(monkeypatch):
    """route() says what string equality would NOT have said; deliver obeys.

    grok -> grok is `native` by equality. Patching `route` to answer `nudge`
    for that very pair makes the two possible implementations disagree, and
    an inlined-equality `deliver()` returns `native` and fails here.
    """
    monkeypatch.setattr(magic_pane, "route", lambda *a, **k: magic_pane.NUDGE)
    assert magic_pane.deliver("grok", "grok", "hi") == magic_pane.NUDGE

    monkeypatch.setattr(magic_pane, "route", lambda *a, **k: magic_pane.UNSUPPORTED)
    assert magic_pane.deliver("grok", "claude", "hi") == magic_pane.UNSUPPORTED

    monkeypatch.setattr(magic_pane, "route", lambda *a, **k: magic_pane.NATIVE)
    assert magic_pane.deliver("claude", "grok", "hi") == magic_pane.NATIVE


def test_route_is_called_exactly_once_with_the_three_args(monkeypatch):
    """Count and value: one call, same three args, answer becomes transport."""
    seen = []
    real = magic_pane.route

    def spy(*a, **k):
        seen.append((a, k))
        return magic_pane.NATIVE

    monkeypatch.setattr(magic_pane, "route", spy)
    assert magic_pane.deliver("grok", "claude", "hi") == magic_pane.NATIVE
    assert len(seen) == 1
    assert seen[0][0] == ("grok", "claude", "hi")
    assert seen[0][1] == {}
    assert real("grok", "claude", "hi") == magic_pane.NUDGE  # real answer differed


def test_deliver_body_mentions_no_harness_name():
    """Static half of the same claim: no harness literal survives in the body."""
    src = inspect.getsource(magic_pane.deliver)
    for harness in ("grok", "claude", "pi"):
        assert harness not in src


def test_module_is_a_leaf_no_rotate_or_dispatch_imports():
    """The invariant from the goal: a messaging module imports no spawn internals."""
    src = inspect.getsource(magic_pane)
    for banned in ("rotate", "dispatch", "import adapters", "from adapters"):
        assert banned not in src
