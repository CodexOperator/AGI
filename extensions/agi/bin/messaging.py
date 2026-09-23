"""messaging.py — magic-pane messaging product layer (goal:g7.32.2).

DECIDES native vs cross and carries the message. Owns NO pane-hold (g7.31.1),
NO adapter pane methods (g7.32.3), NO send.py internals (g7.32.4).
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SEND_PY = Path(__file__).resolve().with_name("send.py")
NUDGE_WAKE = "[agi-nudge] {sender} -> {seat}: {body}"


class PaneMethodMissing(RuntimeError):
    """Fail-closed: the pane object exposes no callable `pane_send`."""


@dataclass(frozen=True)
class NudgeArtifact:
    seat: str
    sender: str
    body: str
    wake_intent: str


def route(sender_harness: str, target_harness: str) -> str:
    """native IFF the harness strings are identical, cross otherwise."""
    return "native" if sender_harness == target_harness else "cross"


def send_native(*, pane, sender: str, text: str) -> list:
    """Drive the pane's own channel. Never touches send.py."""
    fn = getattr(pane, "pane_send", None)
    if not callable(fn):
        raise PaneMethodMissing(f"pane_send missing on pane {sender!r}")
    fn(text)
    return [("pane_send", {"sender": sender, "text": text})]


def send_cross(*, seat: str, sender: str, text: str, runner=subprocess.run,
               send_py=SEND_PY) -> list:
    """Nudge artifact FIRST, then the send.py CLI as the only transport."""
    art = NudgeArtifact(seat, sender, text,
                        NUDGE_WAKE.format(seat=seat, sender=sender, body=text))
    argv = [sys.executable, str(send_py), "send", "--to", seat, text]
    runner(argv, check=False)
    return [("nudge_artifact", art), ("send_py", argv)]


def send(*, sender_harness: str, target_harness: str, sender: str, text: str,
         pane=None, seat=None, runner=subprocess.run) -> list:
    """Route on harness identity and dispatch to the matching carrier."""
    if route(sender_harness, target_harness) == "native":
        return send_native(pane=pane, sender=sender, text=text)
    return send_cross(seat=seat or target_harness, sender=sender, text=text,
                      runner=runner)
