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


def _harness_of(root: Path, seat: str) -> str:
    """The `harness` cell of `seat`'s config:posts row, "" when absent.

    The row reader is the transport's own (`send._locally_loaded_rows` +
    `send._seat_row_by_name`), never a second parser; a missing row or a
    missing harness cell yields "" -- never an invented harness, since "" can
    never match and so can never route native.
    """
    import send  # reader only; _seat_row_by_name is a pure lookup
    row = send._seat_row_by_name(send._locally_loaded_rows(root), seat)
    return str((row or {}).get("harness") or "").strip()


def send_magic(root: Path, from_seat: str, to_seat: str, text: str, *,
               sender: str | None = None, tmux_session: str | None = None,
               ) -> dict:
    """The ONE entrypoint that chooses a path: `route()` decides, and exactly
    one of `native_send` / `cross_send` runs.

    Same harness -> native tmux typing into the recipient's @id window (zero
    `send.send_dm`). Differing or empty harness -> the cross-harness seam
    (zero native body keystrokes). The chosen path's result is returned with
    `via_route` and the resolved harnesses stamped on it, so the caller can
    see WHICH branch ran without re-reading the posts rows.
    """
    from_harness = _harness_of(root, from_seat)
    to_harness = _harness_of(root, to_seat)
    path = route(from_harness, to_harness)
    if path == "native":
        result = native_send(root, to_seat, text, sender=sender,
                             tmux_session=tmux_session)
    else:
        result = cross_send(root, to_seat, text, sender=sender or from_seat,
                            tmux_session=tmux_session)
    return {**result, "via_route": path, "from_harness": from_harness,
            "to_harness": to_harness}


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


def _pane_intent(root: Path, to_seat: str, *,
                 tmux_session: str | None = None) -> dict:
    """Pane-intent artifact for the cross-harness path: WHERE send.py's own
    wake nudge will land. Read-only — it resolves the recipient's @id window
    and records the intent; it types nothing, so the message body is never
    duplicated natively and no keystroke races send.py's nudge. A seat with
    no addressable @id window is still deliverable through the dm file, so
    the intent records pane=None instead of refusing.
    """
    try:
        target = _native_target(root, to_seat, tmux_session)
    except NoAddressableWindow:
        target = None
    return {"event": "nudge", "to": to_seat, "pane": target,
            "via": "send.py _nudge_window"}


def cross_send(root: Path, to_seat: str, text: str, *, sender: str | None = None,
               tmux_session: str | None = None) -> dict:
    """Cross-harness delivery (goal:g7.32.2): pane-intent nudge -> send.py.

    A different harness is never claimed native. The pane-intent artifact is
    emitted FIRST (recorded, not typed), then the body is handed to the
    send.py transport, which writes the dm record and fires its own wake
    nudge at that pane. The body is never typed natively; the returned
    `events` list is the ordered trace of the one path.
    """
    import send  # the transport; never route.native_send here
    nudge = _pane_intent(root, to_seat, tmux_session=tmux_session)
    events = [nudge["event"]]
    dm_path = send.send_dm(root, sender or "unknown", to_seat, text, sender)
    events.append("send_dm")
    return {"path": "nudge-send", "nudge": nudge,
            "transport": {"event": "send_dm", "dm": str(dm_path)},
            "events": events}
