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

def deliver(from_harness: str, to_harness: str, text: str, *, pane_target=None,
            nudge_dir=None, requested_path=None, send_py=None) -> dict:
    """Sole entrypoint: pick the transport from route() and nothing else.

    A caller-supplied `requested_path` that contradicts route() is refused by
    name (both the request and the verdict are in the error text), so a
    same-harness pair can never be pushed onto the send.py path and a
    cross-harness pair can never claim native tmux.
    """
    verdict = route(from_harness, to_harness)
    if requested_path is not None and requested_path != verdict:
        raise ValueError(
            f"transport {requested_path!r} contradicts route verdict "
            f"{verdict!r} for {from_harness!r} -> {to_harness!r}")
    if verdict == "native":
        if pane_target is None:
            raise ValueError("native route requires pane_target")
        out = native_send(pane_target, text)
    else:
        if nudge_dir is None:
            raise ValueError("nudge_send route requires nudge_dir")
        out = cross_send(from_harness, to_harness, text, nudge_dir,
                         send_py=send_py)
    out["route"] = verdict
    return out

def native_send(pane_target: str, text: str) -> dict:
    """Deliver pane-to-pane (tmux send-keys + Enter); never send.py."""
    subprocess.run(["tmux", "send-keys", "-t", pane_target, text, "Enter"], check=True)
    return {"path": "native", "pane": pane_target, "sha256": _sha256(text)}

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
