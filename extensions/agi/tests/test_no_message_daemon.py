"""Regression guard: the heal/cron surface gains NO message-routing daemon.

Standing L4 ruling — messages ride repo + nudge (`send.py`), never a resident
router. The surface is the declarative pair in `.agi/nodes/.geometry/crons.md`:
`cadences:` (periodic crontab ticks) and `services:` (long-lived systemd
units). This test reads the REAL node through `crons.load_crons_node` — never
a hard-coded list — so a service/cadence added to the real node flows through
the same predicate that the positive control proves can fail.

Why `mail_poll` and `nudge_sweep` are NOT daemons (explicit classification):
both are PERIODIC CRON TICKS. They wake on a schedule, do one bounded pass —
read hub-fetched inboxes / sweep nudges via `send.py` — and exit. Neither
holds a socket, a queue, or a pid between runs. A daemon, by contrast, is a
process that stays resident to route/deliver/queue messages between seats.
The predicate would match their names on keywords alone, which is exactly why
they are allowlisted below with this reason rather than silently exempted.
The two real services are the reap-only reaper (`heal.py watch`) and the
alarm rotator (`rotate.py alarms`): neither matches the keyword predicate.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402

#: Keywords marking a process whose PURPOSE is routing/delivering/queueing
#: messages between seats. Matched case-insensitively against the name AND
#: the exec command, so a daemon cannot hide behind an opaque unit name.
MESSAGE_DAEMON_PATTERNS = (
    r"message", r"\brouter\b", r"\brelay\b", r"\bbroker\b", r"\bqueue\b",
    r"\bdispatcher\b", r"\binbox\b", r"\bmail\b", r"\bnudge\b",
)

#: Job names deliberately exempt: periodic ticks, not daemons — see module
#: docstring. Keys are job names; values say why.
ALLOWED_PERIODIC_TICKS = {
    "mail_poll": "periodic cron tick; one bounded inbox pass, exits",
    "nudge_sweep": "periodic cron tick; one bounded nudge sweep, exits",
}


def _haystack(name: str, spec: dict) -> str:
    cmd = spec.get("exec_start") or spec.get("cmd") or ""
    return f"{name} {cmd}"


def find_message_daemons(node: dict) -> list[str]:
    """Names on the heal/cron surface that are message-routing daemons.

    Applies the same predicate to BOTH `services:` (long-lived by
    construction) and `cadences:` (jobs) — a router parked in either table is
    a router. Returns a sorted list, empty for a clean surface.
    """
    flagged = []
    for name, spec in node.get("services", {}).items():
        if any(re.search(p, _haystack(name, spec), re.I) for p in MESSAGE_DAEMON_PATTERNS):
            flagged.append(f"service:{name}")
    for name, spec in node.get("jobs", {}).items():
        if name in ALLOWED_PERIODIC_TICKS:
            continue  # classified tick, not daemon
        if any(re.search(p, _haystack(name, spec), re.I) for p in MESSAGE_DAEMON_PATTERNS):
            flagged.append(f"job:{name}")
    return sorted(flagged)


def _write_node(root: Path, services: dict | None, cadences: dict) -> None:
    p = root / crons.CRONS_NODE_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = {"id": "cron:crons", "type": "cron", "crons_live": True,
          "cadences": cadences}
    if services is not None:
        fm["services"] = services
    p.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")


# --- positive control: the guard MUST be able to fail --------------------


def test_planted_message_router_service_is_flagged(tmp_path):
    """A `services:` entry that routes messages between seats is flagged."""
    root = tmp_path / "proj"
    root.mkdir(parents=True)
    _write_node(
        root,
        services={"agi-message-router": {
            "enabled": True, "exec_start": "python3 router.py serve"}},
        cadences={"grid_sync": {"every_mins": 5, "enabled": True}},
    )
    node = crons.load_crons_node(root)
    assert "service:agi-message-router" in find_message_daemons(node)


def test_planted_message_router_job_is_flagged(tmp_path):
    """A cadence whose name/cmd routes messages is flagged too."""
    root = tmp_path / "proj"
    root.mkdir(parents=True)
    _write_node(
        root,
        services=None,
        cadences={
            "grid_sync": {"every_mins": 5, "enabled": True},
            "agi-message-router": {"every_mins": 1,
                                   "cmd": "python3 router.py serve"},
        },
    )
    node = crons.load_crons_node(root)
    assert "job:agi-message-router" in find_message_daemons(node)


def test_periodic_ticks_are_not_flagged(tmp_path):
    """The explicit non-daemon classification holds on their own keywords."""
    root = tmp_path / "proj"
    root.mkdir(parents=True)
    _write_node(
        root,
        services=None,
        cadences={
            "grid_sync": {"every_mins": 5, "enabled": True},
            "mail_poll": {"every_mins": 5, "enabled": True},
            "nudge_sweep": {"every_mins": 2, "enabled": True},
        },
    )
    node = crons.load_crons_node(root)
    assert find_message_daemons(node) == []


# --- negative control: the REAL surface passes --------------------------


def test_real_heal_cron_surface_has_no_message_daemon():
    """The live `.agi` crons node carries no message-routing daemon."""
    graph_root = Path(crons.__file__).resolve().parents[3] / ".agi"
    node = crons.load_crons_node(graph_root)
    # The predicate read a real, non-empty surface (guards against a wrong
    # path yielding an empty dict and passing by accident).
    assert node["jobs"], "real crons node declared no jobs — wrong root?"
    assert node["services"], "real crons node declared no services — wrong root?"
    assert find_message_daemons(node) == []
