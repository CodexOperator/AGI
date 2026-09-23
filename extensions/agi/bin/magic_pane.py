#!/usr/bin/env python3
"""magic_pane.py — thin magic-pane messaging router (goal:g7.32.2).

Two paths, chosen by the EQUALITY of the two harness strings only:

    grok A ──native──▶ grok B                 (same harness; pane-to-pane)
    grok A ──nudge──▶ send.py ──▶ claude/pi   (cross; nudge artifact FIRST)

No formation, no rotate/dispatch import, no harness-name special case.
"""
from __future__ import annotations
import hashlib, json, subprocess, time
from pathlib import Path

SEND_PY = Path(__file__).resolve().parent / "send.py"

def route(from_harness: str, to_harness: str) -> str:
    """Same harness (case-insensitive) -> 'native'; else 'nudge_send'."""
    same = from_harness.strip().lower() == to_harness.strip().lower()
    return "native" if same else "nudge_send"

def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def native_send(pane_target: str, text: str) -> dict:
    """Deliver pane-to-pane (tmux send-keys + Enter); never send.py."""
    subprocess.run(["tmux", "send-keys", "-t", pane_target, text, "Enter"], check=True)
    return {"path": "native", "pane": pane_target, "sha256": _sha256(text)}

def deliver(from_harness: str, to_harness: str, text: str, *, pane_target=None,
            nudge_dir=None, send_py=None) -> dict:
    """The ENFORCING entrypoint: route() decides, then exactly one path runs.

    A native route without a pane_target fails CLOSED (ValueError), so a
    cross-harness pair can never reach the pane-to-pane transport.
    """
    if route(from_harness, to_harness) == "native":
        if not pane_target:
            raise ValueError(
                f"deliver: route({from_harness!r}, {to_harness!r}) == 'native' "
                "requires a non-empty pane_target")
        return native_send(pane_target, text)
    return cross_send(from_harness, to_harness, text, nudge_dir, send_py=send_py)


def cross_send(from_harness: str, to_harness: str, text: str, nudge_dir,
               send_py=None) -> dict:
    """Write ONE nudge artifact FIRST, then invoke the send.py transport."""
    nudge = {"from": from_harness, "to": to_harness,
             "sha256": _sha256(text), "ts": time.time()}
    d = Path(nudge_dir)
    d.mkdir(parents=True, exist_ok=True)
    artifact = d / f"nudge-{nudge['sha256'][:12]}-{int(nudge['ts'] * 1000)}.json"
    artifact.write_text(json.dumps(nudge, sort_keys=True) + "\n", encoding="utf-8")
    proc = subprocess.run([str(send_py or SEND_PY), "send", to_harness, text], check=False)
    return {"path": "nudge_send", "nudge": str(artifact), "exit_code": proc.returncode}
