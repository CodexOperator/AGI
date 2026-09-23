"""magic_pane — two messaging routes, chosen by destination harness FAMILY.

same-family (grok->grok): type into the destination tmux pane; the native route
never invokes nor imports send.py, even when tmux returns non-zero.
cross-family (grok->claude|pi): FIRST write a pane-intent nudge under send.py's
own comms root (resolved through `send.comms_root`, its ONE owner), THEN invoke
send.py send. No formation/policy here; imports neither rotate nor dispatch.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

#: Registry/adapter name -> family. DATA, consulted by choose_route; there is
#: no `if harness == "grok-bot"` branch in this module.
HARNESS_FAMILIES = {
    "grok": "grok", "grok-bot": "grok",
    "claude": "claude", "claude-code": "claude",
    "pi": "pi", "pi-local": "pi",
    "copilot": "copilot", "copilot-cli": "copilot",
}
#: Families whose peers share a pane route (the native set, as data).
NATIVE_FAMILIES = frozenset({"grok"})
NUDGE_DIRNAME = "pane-nudge"
ENTER_DELAY_S = 0.3
SEND_PY = Path(__file__).with_name("send.py")


def family_of(harness: str) -> str:
    name = str(harness).lower()
    return HARNESS_FAMILIES.get(name, name)


def choose_route(dest_harness: str) -> str:
    """`native` iff the destination FAMILY has a pane route, else `cross`."""
    return "native" if family_of(dest_harness) in NATIVE_FAMILIES else "cross"


def nudge_artifact_path(root: Path, to: str) -> Path:
    """The cross-route wake artifact, in the SAME room send.py reads."""
    import send  # lazy: only the cross path needs the comms root
    return send.comms_root(root) / NUDGE_DIRNAME / f"{to}.nudge"


def _type_into_pane(target: str, text: str, run, delay: float) -> list:
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
    art = nudge_artifact_path(root, to)
    art.parent.mkdir(parents=True, exist_ok=True)
    art.write_text(json.dumps({"to": to, "harness": dest_harness,
                               "from": sender, "route": "cross"}))
    cmd = [sys.executable, str(send_py), "send", to, text]
    if sender:
        cmd += ["--from", sender]
    cp = run(cmd, capture_output=True, text=True)
    return {"route": route, "artifact": str(art), "argv": cmd,
            "returncode": cp.returncode}
