"""messaging.py — the one transport-choice seam for magic-pane messaging.

goal:g7.32.2. Same harness (grok↔grok) = native pane-to-pane; different
harness (grok→claude/pi) = nudge artifact then send.py as transport. Transport
choice only: no formation/rotate/dispatch lives here.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def route(src_harness: str, dst_harness: str) -> str:
    """`native` when both ends share a harness, else `nudge`."""
    return "native" if src_harness == dst_harness else "nudge"


def _tmux_pane_seam(seat: str, text: str) -> dict:
    """Default pane seam: type `text` into the seat's pane, then Enter."""
    target = f"agi-rc:{seat}"
    subprocess.run(["tmux", "send-keys", "-l", "-t", target, text],
                   check=True, capture_output=True, text=True)
    subprocess.run(["tmux", "send-keys", "-t", target, "Enter"],
                   check=True, capture_output=True, text=True)
    return {"seam": "tmux", "target": target}


def send_native(pane_seam=None, *, seat: str, text: str) -> dict:
    """Same-harness path: call the pane seam, never send.py transport."""
    seam = pane_seam or _tmux_pane_seam
    return {"path": "native", "seat": seat,
            "seam": seam(seat, text), "send_py": None}


def send(src_harness: str, dst_harness: str, *, seat: str, text: str,
         pane_seam=None, nudge_dir=None, send_py=None) -> dict:
    """route() decides; same-harness -> native, cross -> nudge->send.py.

    Cross-harness MUST name nudge_dir and send_py: it refuses by name rather
    than silently falling back to the native pane.
    """
    if route(src_harness, dst_harness) == "native":
        return send_native(pane_seam, seat=seat, text=text)
    missing = [name for name, val in (("nudge_dir", nudge_dir),
                                      ("send_py", send_py)) if val is None]
    if missing:
        raise ValueError(
            f"cross-harness send {src_harness}->{dst_harness} requires "
            f"{', '.join(missing)}; refusing to fall back to the native pane")
    return send_cross(src=src_harness, dst=dst_harness, seat=seat, text=text,
                      nudge_dir=nudge_dir, send_py=send_py)


def send_cross(*, src: str, dst: str, seat: str, text: str,
               nudge_dir, send_py) -> dict:
    """Cross-harness path: write the nudge artifact FIRST, then shell send.py.

    Returns ONE trace dict naming both the artifact and the transport argv/rc.
    """
    nudge_dir = Path(nudge_dir)
    nudge_dir.mkdir(parents=True, exist_ok=True)
    artifact = nudge_dir / f"nudge-{src}-to-{seat}.md"
    artifact.write_text(json.dumps({"src": src, "dst": dst, "seat": seat,
                                    "text": text}, indent=1) + "\n")
    argv = [sys.executable, str(send_py), "send", seat, text, "--from", src]
    run = subprocess.run(argv, capture_output=True, text=True)
    return {"path": "nudge", "seat": seat, "nudge_artifact": str(artifact),
            "send_py": {"argv": argv, "returncode": run.returncode,
                        "stdout": run.stdout.strip()}}
