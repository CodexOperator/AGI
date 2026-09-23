"""Magic-pane messaging router (goal:g7.32.2): same-harness native tmux typing; cross-harness seam for goal:g7.32.4."""
from __future__ import annotations
import subprocess, time
from pathlib import Path

DEFAULT_TMUX_SESSION = "agi-rc"
NATIVE_ENTER_DELAY_S = 0.3

class NoAddressableWindow(RuntimeError):
    """No addressable @id window for this seat."""


def route(sender_harness: str, target_harness: str) -> str:
    a = (sender_harness or "").strip().casefold()
    b = (target_harness or "").strip().casefold()
    return "native" if a and a == b else "nudge-send"


def _native_target(root: Path, to_seat: str, tmux_session: str | None) -> str:
    import boxes, send  # reader only; never send_dm/_nudge_*
    row = send._seat_row_by_name(send._locally_loaded_rows(root), to_seat)
    window = str((row or {}).get("window") or "").strip()
    if row is None or not window.startswith("@") or not boxes.row_is_local(root, row):
        raise NoAddressableWindow(f"native_send: {to_seat}: no addressable @id window")
    return f"{tmux_session or DEFAULT_TMUX_SESSION}:{window}"


def native_send(root: Path, to_seat: str, text: str, *,
                sender: str | None = None, tmux_session: str | None = None) -> dict:
    target = _native_target(root, to_seat, tmux_session)
    typed = subprocess.run(["tmux", "send-keys", "-l", "-t", target, text],
                           capture_output=True, text=True, timeout=5).returncode == 0
    time.sleep(NATIVE_ENTER_DELAY_S)
    typed = typed and subprocess.run(["tmux", "send-keys", "-t", target, "Enter"],
                                     capture_output=True, text=True, timeout=5).returncode == 0
    return {"path": "native", "target": target, "typed": len(text) if typed else 0}


def cross_send(root: Path, to_seat: str, text: str, *, sender: str | None = None) -> dict:
    raise NotImplementedError("g7.32.2 cross-harness nudge->send: kid 2 fills this")
