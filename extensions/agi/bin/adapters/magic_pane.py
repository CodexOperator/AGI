"""Magic pane — one message, ONE routing decision, in exactly one place.

`goal:g7.32.2.1.2`. `route()` is the only function that looks at a harness
name and `deliver()` takes its transport from `route()` alone, so a
`deliver()` comparing harness strings inline contradicts a patched `route()`
— the mutant `test_magic_pane_cli_path.py` kills, through the CLI. A LEAF
(`sys` is the whole import list), so it cannot reach the spawn machinery.
`reach` is the ONE side-effect seam it does not own; `send.py pane` wires it
to the target seat's inbox. Skeleton ported from the DH.375 worktree
`a00-a1d31c1a`; the seam, side effects and return-the-label contract are this
round's. Full reasoning: this node's body.
"""
from __future__ import annotations

import sys

NAME = "magic_pane"

# Transport tokens -- the ONLY keys of _TRANSPORTS. A deliver() that skipped
# route() would have to name a harness to index the table at all.
NATIVE = "native"
NUDGE = "nudge"
UNSUPPORTED = "unsupported"

_TRANSPORTS = {NATIVE: "_send_native", NUDGE: "_send_nudge",
               UNSUPPORTED: "_send_unsupported"}


def route(source: str, target: str, message: str = "") -> str:
    """Pure and total: which transport carries `message` from source to
    target. Table lookup on the two harness strings, nothing else."""
    if source == "grok" and target == "grok":
        return NATIVE
    if source == "grok" and target in ("claude", "pi"):
        return NUDGE
    return UNSUPPORTED


def _reach_unwired(target: str, message: str) -> None:
    """No sink wired — complain LOUDLY; silence is the defect this kills."""
    print(f"magic_pane: no reach sink wired for a nudge to {target!r}",
          file=sys.stderr)


#: The ONE side-effect seam; `send.py pane` sets it to the target inbox send.
reach = _reach_unwired


def _send_native(message: str) -> str:
    """Same seat: the pane IS the message. Nothing to deliver anywhere."""
    print(message)
    return NATIVE


def _send_nudge(message: str, target: str = "") -> str:
    """Reach the target seat, then report the transport that carried it."""
    globals()["reach"](target, message)
    return NUDGE


def _send_unsupported(message: str) -> str:
    """Refuse LOUDLY — a no-op returning success would be the silent lie."""
    print(f"magic_pane: unsupported transport, refusing {message!r}",
          file=sys.stderr)
    return UNSUPPORTED


def deliver(source: str, target: str, message: str = "") -> str:
    """Send `message`, transport SOLELY from `route()` — no harness-string
    comparison here; `route` is looked up in the module globals when this
    line RUNS, not at import time."""
    transport = globals()["route"](source, target, message)  # the ONE decision
    if transport == NUDGE:  # nudge alone needs the target seat
        return globals()[_TRANSPORTS[transport]](message, target)
    return globals()[_TRANSPORTS[transport]](message)
