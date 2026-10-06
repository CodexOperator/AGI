#!/usr/bin/env python3
"""box_mail.py — AA1 mail facade for old-engine callers (rotate/heal).

Never import deprecated send.py. Mail is git-ref box; wake is in-pane box n.
Keygen is agi-out (out-line), not send.py keygen.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

PRIME = "belam"
WHOIS_NOT_AUTHORIZED = "WHOIS_NOT_AUTHORIZED"

# Operator recovery: new-engine out-line, never send.py keygen.
KEYGEN_LINE = (
    "touch ~/.fresh && systemctl restart agi-post@{seat}.service  "
    "# agi-out does out-line keygen; never send.py"
)


class BoxMailError(RuntimeError):
    pass


def comms_root(root: Path, override=None) -> Path:
    if override:
        return Path(override)
    return Path(root) / "comms"


def wake(root, seat: str) -> None:
    """No-op: AA1 wake is in-pane (`box n` / mail: box read), not a central nudge."""
    return None


def _box_env(sender: str) -> dict:
    env = os.environ.copy()
    env["AGI_POST"] = sender
    env.setdefault("AGI_TRUNK", os.environ.get("AGI_TRUNK", "core/season2/et-grok-pilot"))
    return env


def _box_bin() -> str:
    home = os.environ.get("HOME", "")
    cand = Path(home) / "bin" / "box"
    if cand.is_file():
        return str(cand)
    # fall back to post home layout
    post = os.environ.get("AGI_POST", "")
    if post:
        p = Path(f"/var/lib/agi/{post}/bin/box")
        if p.is_file():
            return str(p)
    return "box"


def send(root, to: str, text: str, sender: str | None = None, **_kw) -> None:
    sender = sender or os.environ.get("AGI_POST") or PRIME
    proc = subprocess.run(
        [_box_bin(), "send", to],
        input=text if text.endswith("\n") else text + "\n",
        text=True,
        capture_output=True,
        env=_box_env(sender),
        cwd=str(Path(root).parent if Path(root).name == ".agi" else root),
    )
    if proc.returncode != 0:
        raise BoxMailError(proc.stderr.strip() or f"box send failed rc={proc.returncode}")


def send_dm(croot, sender: str, to: str, text: str, **_kw) -> None:
    send(Path(croot).parent if Path(croot).name == "comms" else croot, to, text, sender=sender)


def send_room(croot, room: str, text: str, sender: str | None = None, **_kw) -> None:
    # AA1 has no rooms; best-effort no-op (rotation alerts were send.py rooms).
    return None


def _locally_loaded_rows(root) -> list:
    return []


def _resolve_rows(rows, ref, claim=None):
    # No send.py whois: treat as authorized if claim matches ref loosely.
    if claim and ref and claim in str(ref):
        return ("OK", ref)
    return (WHOIS_NOT_AUTHORIZED, ref)


def whois(root, token: str, claim: str | None = None):
    code, text = _resolve_rows([], token, claim=claim)
    return code, text


def rewind_read_cursors(*_a, **_k):
    return []


def _mint_seat_key(root, seat: str, scheme=None, stage: bool = False):
    raise BoxMailError(
        f"keygen retired: {KEYGEN_LINE.format(seat=seat)}"
    )


def _row_write_submit(*_a, **_k):
    return None
