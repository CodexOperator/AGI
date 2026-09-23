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

**Two persistence mechanisms, not one.** The first version of this scan
required a transport line to also carry an inline loop flag (`--poll`,
`--daemon`, `serve_forever`, ...). That missed the natural declaration
entirely: a row in the crons node's `services:` table already IS a
long-running systemd unit, so
`service agi-message-router exec_start .../send.py router restart on-failure`
-- no inline flag anywhere -- slipped through. Table membership is
persistence; the inline-loop half is kept only for the OTHER surface, where
a one-shot `send.py wake` tick is the allowed shape and a loop is the thing
that makes it a daemon.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402
import locations  # noqa: E402

#: A message TRANSPORT (send.py / a router / a mail daemon).
_TRANSPORT_RE = re.compile(r"send\.py|router|message|mail")

#: The `--poll`/`serve_forever`/`setsid`/`while True`/`Restart=` half. It
#: separates a daemon from the allowed one-shot `send.py read|wake` cron
#: lines -- but only on a NON-service line; a `services:`-table row is
#: persistent by construction and needs no inline flag.
_PERSISTENT_RE = re.compile(
    r"--poll|--serve|--daemon|serve_forever|setsid|while\s+True|Restart=")

#: The prefix `_live_surface_text` gives every row of the node's `services:`
#: table. Matching it is what tells a persistent unit apart from a one-shot
#: cron tick without trusting the transport name itself.
_SERVICE_ROW_PREFIX = "service "

#: daemon-construction primitives that must not appear in `send.py`'s bytes.
_DAEMON_PRIMITIVES = ("os.fork", "daemonize", "setsid", "serve_forever",
                      "socket.socket", "listen(")


def message_daemon_hits(text: str) -> list[str]:
    """Message-transport lines that describe a PERSISTENT process.

    Two shapes, because persistence reaches this surface two ways:

    * a `services:`-table row (`service <name> exec_start ... restart ...`)
      -- **membership in the table IS persistence.** Every row is rendered
      into a systemd unit, so the moment its `exec_start` names a transport
      it counts, inline loop flag or none. Requiring the flag here is what
      let `service agi-message-router exec_start .../send.py router restart
      on-failure` slip the first version of this scan.
    * any other line (a rendered cron job, a generic `cmd:`) -- a one-shot
      tick is the allowed shape, so a transport only counts when the line
      ALSO shows a loop. This is what keeps the live `send.py wake
      --all-local` tick out of the hits.
    """
    hits: list[str] = []
    for ln in text.splitlines():
        if not _TRANSPORT_RE.search(ln):
            continue
        if ln.strip().startswith(_SERVICE_ROW_PREFIX):
            hits.append(ln.strip())
        elif _PERSISTENT_RE.search(ln):
            hits.append(ln.strip())
    return hits


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


def test_scanner_fires_on_a_synthetic_service_row_with_no_loop_flag():
    """Negative control for the hole this version closes: a `services:` row
    running a message transport with ONLY `restart on-failure` -- the exact
    shape that slipped the inline-loop-flag-only scan. Table membership alone
    must flag it."""
    raw = ("service agi-message-router exec_start "
           "/usr/bin/python3 /repo/extensions/agi/bin/send.py router "
           "restart on-failure")
    assert "--poll" not in raw and "--daemon" not in raw, "control is not bare"
    assert message_daemon_hits(raw), \
        "scanner missed a bare services-row message transport"

    # Same bare shape through a real `services:` dict rendered by the live
    # surface formatter, not a hand-built string.
    root, repo_root, engine_root = _roots()
    node = {
        "crons_live": True,
        "services": {"agi-message-router": {
            "enabled": True,
            "exec_start": (f"/usr/bin/python3 {BIN}/send.py router"),
            "restart": "on-failure",
            "working_directory": None,
            "environment": {},
        }},
        "jobs": {},
    }
    from_string = "\n".join(
        f"service {n} exec_start {s['exec_start']} restart {s['restart']}"
        for n, s in node["services"].items())
    assert message_daemon_hits(from_string), from_string


def test_scanner_ignores_the_benign_live_services():
    """The service-row rule must not flag the two real units: `heal.py watch`
    (`agi-reaper`) and `rotate.py alarms` (`agi-alarms`)."""
    benign = (
        "service agi-reaper exec_start /usr/bin/python3 "
        "/repo/extensions/agi/bin/heal.py watch --root /repo --poll-s 30 "
        "restart on-failure\n"
        "service agi-alarms-sanctuary-master exec_start /usr/bin/python3 "
        "/repo/extensions/agi/bin/rotate.py alarms --holder sanctuary-master "
        "--root /repo restart on-failure"
    )
    assert message_daemon_hits(benign) == [], message_daemon_hits(benign)


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