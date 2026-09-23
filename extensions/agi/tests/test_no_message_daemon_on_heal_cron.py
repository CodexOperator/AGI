"""Regression guard for goal:g7.31.4.3 — the heal/cron surface gains no
message daemon.

The standing L4 ruling is **repo + nudge, not a router process**: messages
land in an inbox file and the recipient is woken with a token; nothing in the
system is allowed to grow a persistent message-routing process. This test is
the mechanism for that ruling on the heal/cron surface — the `services:`
table (persistent systemd units) plus the `cadences:` jobs of the live crons
node. A claim in a node cannot refuse anything; this can.

It reads the REAL node through `crons.load_crons_node` (the real path
resolver `crons._node_path` underneath), never a fixture list, so a stub
cannot satisfy it. The negative control is in-file:
`test_guard_detects_a_planted_message_router` plants an `agi-message-router`
service into a COPY of the node (temp dir, never the live node) and asserts
the same guard reports it — a guard that cannot fail on the refusing state is
not a guard.

See hypothesis:a00-ffd04a24-02b8b5 / experiment:a00-ffd04a24-daemon-guard.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402
import locations  # noqa: E402

#: A name shaped like a message daemon/router: a message transport noun glued
#: to a daemon/route noun. Deliberately token-shaped, not a bare "mail" or
#: "nudge" — `mail_poll` and `nudge_sweep` are periodic cron ticks (one-shot
#: processes), not daemons, and must never false-positive.
MESSAGE_ROUTER_NAME_RE = re.compile(
    r"(?:message|msg|mail|inbox)[-_]?(?:router|daemon|bus|broker|relay|hub|svc|service|d)\b"
    r"|\b(?:router|broker|relay|mux)[-_]?(?:daemon|service|svc|d)\b",
    re.IGNORECASE,
)

#: An exec_start / cmd that launches a message router, whatever the service is
#: called: a router module by filename, a maild, or the messaging seam
#: (`send.py`) running in a serve/daemon/listen mode instead of one-shot.
MESSAGE_ROUTER_EXEC_RE = re.compile(
    r"(?:message|msg)[-_]?(?:router|daemon|bus|broker)\.py"
    r"|\bmaild\b"
    r"|send\.py\s+(?:serve|daemon|listen|watch|router)\b",
    re.IGNORECASE,
)

#: The persistent services reviewed as message-free: the reaper
#: (`heal.py watch`, death/heal only) and the alarms service. Any NEW entry
#: here is a change to the heal/cron surface that a human must review.
REVIEWED_PERSISTENT_SERVICES = frozenset({
    "agi-reaper",
    "agi-alarms-sanctuary-master",
})


def _graph_root() -> Path:
    """The real graph root, resolved exactly as production resolves it."""
    root = locations.find_project_root(Path(__file__).resolve().parent)
    assert root is not None, "could not resolve the real project graph root"
    return root


def message_daemons(node: dict) -> list:
    """Every entry of the parsed crons node shaped like a message daemon.

    Returns a list of `(kind, name, detail)` so a failure names the exact
    entry, not just "something matched".
    """
    hits = []
    for name, svc in node["services"].items():
        if MESSAGE_ROUTER_NAME_RE.search(name) or \
                MESSAGE_ROUTER_EXEC_RE.search(svc.get("exec_start") or ""):
            hits.append(("service", name, svc.get("exec_start")))
    for name, job in node["jobs"].items():
        if MESSAGE_ROUTER_NAME_RE.search(name) or \
                MESSAGE_ROUTER_EXEC_RE.search(job.get("cmd") or ""):
            hits.append(("job", name, job.get("cmd")))
    return hits


def test_no_message_daemon_on_the_heal_cron_surface():
    """The live heal/cron surface carries no message daemon/router."""
    node = crons.load_crons_node(_graph_root())
    hits = message_daemons(node)
    assert hits == [], (
        "goal:g7.31.4.3 forbids a message daemon on the heal/cron surface "
        f"(repo + nudge, not a router process); found: {hits}"
    )


def test_persistent_services_are_the_reviewed_message_free_pair():
    """The services table is exactly the reviewed pair — proves absence today
    and forces a human to see any new persistent process added to the
    surface."""
    node = crons.load_crons_node(_graph_root())
    assert set(node["services"]) == set(REVIEWED_PERSISTENT_SERVICES), (
        "a persistent service was added to or removed from the heal/cron "
        "surface; review it against goal:g7.31.4.3 (no message daemon) and "
        "update REVIEWED_PERSISTENT_SERVICES if it is message-free. Current: "
        f"{sorted(node['services'])}"
    )


def test_guard_detects_a_planted_message_router(tmp_path):
    """NEGATIVE CONTROL, in-file: plant a message-router service into a COPY
    of the node and assert the guard above reports it. Temp dir only — the
    live node is never touched."""
    fm = crons._parse_frontmatter(_graph_root() / crons.CRONS_NODE_REL)
    fm.setdefault("services", {})["agi-message-router"] = {
        "enabled": True,
        "exec_start": "python3 /engine/extensions/agi/bin/message_router.py serve",
        "restart": "always",
    }
    root = tmp_path / "graph"
    node_path = root / crons.CRONS_NODE_REL
    node_path.parent.mkdir(parents=True)
    node_path.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\nBody.\n")

    planted = crons.load_crons_node(root)
    hits = message_daemons(planted)
    assert any(name == "agi-message-router" for _, name, _ in hits), (
        "the guard did NOT flag a planted message-router service — it cannot "
        f"guard anything. hits={hits}"
    )
