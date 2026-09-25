"""Harness-to-harness pane transport.

Routing is intentionally a pure equality decision; this module owns no
harness registry and imports no rotation internals.
"""
from __future__ import annotations
import subprocess

NATIVE = "native"
CROSS = "cross"


def route(from_harness: str, to_harness: str) -> str:
    """Return the sole transport decision for two harness strings."""
    return NATIVE if from_harness == to_harness else CROSS


def native_send(text: str, *, target: str | None = None) -> bool:
    """Type text into a same-harness tmux pane."""
    argv = ["tmux", "send-keys", "-t", target, "-l", text]
    try:
        return subprocess.run(argv, check=False, capture_output=True).returncode == 0
    except OSError:
        return False


def cross_send(text: str, *, target: str, sender: str | None = None) -> int:
    """Write a cross-harness message through send.py (its inbox/dm path)."""
    import send
    argv = ["--from", sender] if sender else []
    return send.main(argv + ["send", "--to", target, text])


def deliver(from_harness: str, to_harness: str, text: str, *, target: str | None = None,
            sender: str | None = None) -> tuple[str, int | bool]:
    """Deliver one message, choosing transport only from ``route``'s result."""
    decision = route(from_harness, to_harness)
    if decision == NATIVE:
        return decision, native_send(text, target=target)
    return decision, cross_send(text, target=target or to_harness, sender=sender)
