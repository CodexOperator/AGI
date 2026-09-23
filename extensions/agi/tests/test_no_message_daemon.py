"""goal:g7.31.4.3 (Falsifier-3) -- no NEW message daemon/router on the
heal/cron surface.

Standing L4 ruling: messaging is **repo + nudge**, not a router process. The
transport is a one-shot `send.py` tick (file inbox write + tmux nudge) plus
the `mail_poll`/`nudge_sweep` cron lines; nothing long-running routes
messages.

The scan reads the LIVE surface -- the crons node, its declared services and
the lines `render_managed_lines` actually emits -- not a copied list, plus
`send.py`'s own bytes. The negative control proves the scan is not vacuous:
a synthetic message transport rendered as a PERSISTENT process IS flagged.
A grep that returns nothing because it keys the wrong word is the near miss
this control rules out.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402
import locations  # noqa: E402

#: A message TRANSPORT (send.py / a router / a mail daemon) rendered as a
#: PERSISTENT process rather than a one-shot tick. The `--poll`/`serve_forever`
#: /`setsid`/`while True`/`Restart=` half is what separates a daemon from the
#: allowed one-shot `send.py read|wake` cron lines.
_TRANSPORT_RE = re.compile(r"send\.py|router|message|mail")
_PERSISTENT_RE = re.compile(
    r"--poll|--serve|--daemon|serve_forever|setsid|while\s+True|Restart=")

#: daemon-construction primitives that must not appear in `send.py`'s bytes.
_DAEMON_PRIMITIVES = ("os.fork", "daemonize", "setsid", "serve_forever",
                      "socket.socket", "listen(")


def message_daemon_hits(text: str) -> list[str]:
    """Lines that are BOTH a message transport AND a persistent process."""
    return [ln.strip() for ln in text.splitlines()
            if _TRANSPORT_RE.search(ln) and _PERSISTENT_RE.search(ln)]


def daemon_primitive_hits(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines()
            if any(p in ln for p in _DAEMON_PRIMITIVES)]


def _roots() -> tuple[Path, Path, Path]:
    root = locations.find_project_root(Path(__file__))
    assert root is not None, "no .agi project root from the test file"
    engine = Path(__file__).resolve().parents[2]
    return root, root.parent, engine


def _live_surface_text() -> str:
    root, repo_root, engine_root = _roots()
    node = crons.load_crons_node(root)
    parts: list[str] = []
    for name, svc in node["services"].items():
        parts.append(f"service {name} exec_start {svc['exec_start']} "
                     f"restart {svc['restart']}")
    parts += crons.render_managed_lines(root, repo_root, engine_root, node)
    for name, job in node["jobs"].items():
        if job.get("cmd"):
            parts.append(f"job {name} cmd {job['cmd']}")
    return "\n".join(parts)


def test_no_message_daemon_on_the_live_heal_cron_surface():
    hits = message_daemon_hits(_live_surface_text())
    assert hits == [], f"message daemon on heal/cron surface: {hits}"


def test_send_py_carries_no_daemon_construction_primitives():
    src = (BIN / "send.py").read_text()
    hits = daemon_primitive_hits(src)
    assert hits == [], f"daemon primitives in send.py: {hits}"


def test_scanner_fires_on_a_synthetic_message_daemon():
    """Negative control: non-vacuity, on both the raw surface and the real
    renderer. A scan that cannot see a daemon certifies nothing."""
    raw = ("service agi-message-router exec_start "
           "/usr/bin/python3 /repo/extensions/agi/bin/send.py router "
           "--poll-s 30 --daemon restart always")
    assert message_daemon_hits(raw), "scanner missed a synthetic service daemon"

    root, repo_root, engine_root = _roots()
    node = {
        "crons_live": True,
        "services": {},
        "jobs": {"fake_router": {
            "enabled": True, "every_mins": 1,
            "cmd": (f"while True; do python3 {BIN}/send.py wake --all-local;"
                    f" sleep 5; done"),
        }},
    }
    rendered = "\n".join(
        crons.render_managed_lines(root, repo_root, engine_root, node))
    assert message_daemon_hits(rendered), rendered

    assert daemon_primitive_hits("import os\nos.fork()\n"), \
        "scanner missed os.fork()"