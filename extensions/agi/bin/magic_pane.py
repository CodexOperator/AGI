"""magic_pane — the magic-pane messaging seam: exactly two transport routes.

Route is chosen from the DESTINATION harness family, `NATIVE_HARNESSES` as
data (never an `if harness == "grok"` soup):
  * same-harness (grok->grok): type the message DIRECTLY into the destination
    seat's tmux pane; this route never invokes send.py nor its transport.
  * cross-harness (grok->claude|pi): FIRST write a nudge artifact under the
    sessions comms root, THEN invoke send.py's `send` verb as the transport.

No formation/policy here (that lives in seats/rotate); imports neither rotate
nor dispatch, even transitively.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import locations

#: Harness families with a native pane route. DATA -- choose_route looks it up.
NATIVE_HARNESSES = frozenset({"grok"})
#: Artifact dir under the sessions comms root, apart from send.py's own
#: `<inbox>/<seat>.nudge` marker on purpose.
NUDGE_DIRNAME = "pane-nudge"
ENTER_DELAY_S = 0.3
SEND_PY = Path(__file__).with_name("send.py")


def choose_route(dest_harness: str) -> str:
    """`native` iff the destination family has a pane route, else `cross`."""
    return "native" if str(dest_harness).lower() in NATIVE_HARNESSES else "cross"


def nudge_artifact_path(root: Path, to: str) -> Path:
    return (locations.shared_sessions_dir(root) / "comms" / NUDGE_DIRNAME
            / f"{to}.nudge")


def write_nudge_artifact(root: Path, to: str, dest_harness: str,
                         sender: str | None) -> Path:
    """The cross-route wake artifact, written BEFORE send.py is invoked."""
    p = nudge_artifact_path(root, to)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"to": to, "harness": dest_harness,
                             "from": sender, "route": "cross"}))
    return p


def _type_into_pane(target: str, text: str, run, delay: float) -> list:
    """send.py's measured shape: literal text, pause, then Enter separately."""
    argv1 = ["tmux", "send-keys", "-l", "-t", target, text]
    argv2 = ["tmux", "send-keys", "-t", target, "Enter"]
    run(argv1, capture_output=True, text=True, timeout=5)
    time.sleep(delay)
    run(argv2, capture_output=True, text=True, timeout=5)
    return [argv1, argv2]


def send_message(root: Path, to: str, text: str, dest_harness: str, *,
                 sender: str | None = None, tmux_session: str = "agi-rc",
                 run=subprocess.run, send_py: Path = SEND_PY,
                 enter_delay_s: float = ENTER_DELAY_S) -> dict:
    """Route one message by destination-harness family; return its trace."""
    route = choose_route(dest_harness)
    if route == "native":
        target = f"{tmux_session}:{to}"
        return {"route": route, "target": target,
                "argv": _type_into_pane(target, text, run, enter_delay_s)}
    art = write_nudge_artifact(root, to, dest_harness, sender)
    cmd = [sys.executable, str(send_py), "send", to, text]
    if sender:
        cmd += ["--from", sender]
    cp = run(cmd, capture_output=True, text=True)
    return {"route": route, "artifact": str(art), "argv": cmd,
            "returncode": cp.returncode}
