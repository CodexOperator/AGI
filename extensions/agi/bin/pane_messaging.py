#!/usr/bin/env python3
"""pane_messaging.py — route one pane message by harness pair (goal:g7.32.2).

    same harness                 different harness
      │                              │
      ▼                              ├─ 1. write nudge artifact
   native_send                       └─ 2. send.py send  (subprocess)
      │                                        │
      ▼                                        ▼
   transport(recipient, body)              transport

The pair alone decides the path. Native NEVER imports or invokes send.py;
cross ALWAYS writes the nudge artifact before the send.py subprocess fires.
This module imports neither rotate nor dispatch.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

NATIVE = "native"
CROSS = "cross"
_SEND = Path(__file__).resolve().parent / "send.py"


class NoTransport(RuntimeError):
    """native_send called without a transport: fail closed, by name."""


def classify(sender_harness: str, recipient_harness: str) -> str:
    """The whole routing rule: the harness pair, and nothing else."""
    return NATIVE if sender_harness == recipient_harness else CROSS


def native_send(recipient: str, body: str, *, transport=None) -> object:
    """Same-harness send through an injected transport. Never touches send.py."""
    if transport is None:
        raise NoTransport(
            "native_send: no transport injected; refusing to fall back to send.py"
        )
    return transport(recipient, body)


def cross_send(recipient: str, body: str, *, comms_root, sender: str) -> dict:
    """Cross-harness: nudge artifact FIRST, then send.py send as subprocess."""
    nudge = Path(comms_root) / f"nudge-{recipient}.json"
    nudge.parent.mkdir(parents=True, exist_ok=True)
    nudge.write_text(json.dumps({"to": recipient, "body": body, "sender": sender,
                                 "transport": "send.py", "ts": time.time()}))
    cmd = [sys.executable, str(_SEND), "send", "--comms-root", str(comms_root),
           "--from", sender, "--to", recipient, body]
    done = subprocess.run(cmd, capture_output=True, text=True)
    return {"nudge": str(nudge), "returncode": done.returncode,
            "output": (done.stdout or done.stderr).strip()}