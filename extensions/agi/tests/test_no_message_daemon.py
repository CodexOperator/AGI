"""Falsifier for goal:g7.31.4.3 -- no new message daemon on the heal/cron
surface. Reads the LIVE `.geometry/crons.md`, never a copied list.

Falsifier, verbatim: "1. No new message daemon process appears in the
heal/cron surface for this goal."
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[3]
CRONS_MD = REPO / ".agi" / "nodes" / ".geometry" / "crons.md"

#: The only durable surfaces this project declares (both are the L4 ruling,
#: not message transport): a rotate.py alarms holder and the heal.py reaper.
KNOWN_SERVICES = {
    "agi-alarms-sanctuary-master": "rotate.py alarms",
    "agi-reaper": "heal.py watch",
}
ALLOWED_EXEC = tuple(KNOWN_SERVICES.values())
#: Jobs that legitimately touch send.py/mail_alert.py -- cadenced, never a
#: `services:` long-runner.
MESSAGE_JOBS = {"nudge_sweep", "mail_poll"}
DAEMON_SIGS = ("message-daemon", "message_daemon", "router", "relay",
               "SendToAgent", "send.py", "mail_alert.py", "nudge")


def parse_frontmatter(text: str) -> dict:
    return yaml.safe_load(text.split("---", 2)[1])


def audit(fm: dict) -> None:
    services = fm.get("services") or {}
    extra = set(services) - set(KNOWN_SERVICES)
    assert not extra, (
        f"third long-running service on the heal/cron surface: {sorted(extra)}"
        f" (only {sorted(KNOWN_SERVICES)} are declared durable surfaces)")
    for name, svc in services.items():
        ex = (svc or {}).get("exec_start") or ""
        assert any(a in ex for a in ALLOWED_EXEC), (
            f"service {name!r} exec_start is not rotate.py alarms / "
            f"heal.py watch: {ex!r}")
        assert not any(s.lower() in ex.lower() for s in DAEMON_SIGS), (
            f"service {name!r} launches a message daemon/long-runner: {ex!r}")
    for job, cfg in (fm.get("cadences") or {}).items():
        cmd = (cfg or {}).get("cmd") if isinstance(cfg, dict) else None
        if not cmd or job in MESSAGE_JOBS:
            continue
        assert not any(s.lower() in cmd.lower() for s in DAEMON_SIGS), \
            f"cadence {job!r} launches a message daemon: {cmd!r}"


def test_live_crons_node_has_no_message_daemon() -> None:
    fm = parse_frontmatter(CRONS_MD.read_text())
    audit(fm)
    assert set(fm.get("services") or {}) <= set(KNOWN_SERVICES)


def test_audit_is_not_vacuous() -> None:
    """Negative probe: both the new-service and the smuggled-exec_start
    checks must fail on synthetic falsifying input."""
    base = {"crons_live": True, "cadences": {}}
    third = dict(base, services={"agi-message-router": {
        "enabled": True, "restart": "always",
        "exec_start": "python3 /repo/extensions/agi/bin/send.py watch"}})
    with pytest.raises(AssertionError, match="agi-message-router"):
        audit(third)
    smuggled = dict(base, services={"agi-reaper": {
        "enabled": True, "restart": "always",
        "exec_start": "python3 /repo/extensions/agi/bin/send.py serve"}})
    with pytest.raises(AssertionError, match="agi-reaper"):
        audit(smuggled)
