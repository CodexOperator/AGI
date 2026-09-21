"""goal:g7.31.4.3 — the heal/cron surface must gain no message daemon.

A message daemon is a LONG-LIVED process whose PURPOSE is routing or
delivering messages between seats.  The standing model is repo + nudge
(L4), so the nudge sweep and the mail poll are BOUNDED one-shot fetches and
the reaper/alarms units are not message routing at all.

This guard DERIVES the surface it audits from the graph and code, so a new
job or service is inspected without editing the test:

  * every cadence declared in `.agi/nodes/.geometry/crons.md`,
    rendered through crons.py's own per-job renderers (so a known job
    whose renderer is edited into a daemon is caught too);
  * every `services:` ExecStart, rendered through `render_unit_file`.

The surface is rendered with `enabled` forced true and `crons_live` forced
true: a declared-but-currently-off daemon is still a daemon waiting to be
switched on, and the audit must not be vacuous just because a flag is off.

The failure message NAMES the member and the command that tripped it.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402
import locations  # noqa: E402

#: A process that keeps running: a server, a daemon, or an endless loop.
_DAEMON_RE = re.compile(
    r"(?<![\w-])"
    r"(?:serve|daemon|watch|--watch|--follow|--listen|--forever|--loop|--tail)"
    r"(?![\w-])"
)
#: A process whose purpose is moving messages between seats.
_MESSAGE_RE = re.compile(
    r"(?<![\w-])"
    r"(?:send\.py|nudge|wake|mail|message|msg|inbox|router|relay|"
    r"broker|dispatcher|send|read)"
    r"(?![\w-])"
)
#: A NAME that announces its own purpose even before the command is read.
_DAEMON_NAME_RE = re.compile(
    r"(?:router|relay|broker|dispatcher|daemon|mailman|postmaster|message[-_]?server)"
)


def message_daemons(surface: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """Return `(label, command, reason)` for every message daemon in the
    surface.  A member is a daemon when a long-lived marker meets a
    message-routing marker, or when its own name says so."""
    offenders: list[tuple[str, str, str]] = []
    for label, cmd in surface:
        name = label.split(":", 1)[-1]
        if _DAEMON_NAME_RE.search(name.lower()):
            offenders.append((label, cmd, f"name {name!r} is a message-router name"))
            continue
        daemon = _DAEMON_RE.search(cmd or "")
        message = _MESSAGE_RE.search(cmd or "")
        if daemon and message:
            offenders.append((
                label, cmd,
                f"long-lived marker {daemon.group(0)!r} on a messaging command",
            ))
    return offenders


def _audit_node(node: dict) -> dict:
    """The declared surface, with every job enabled and crons live: a daemon
    parked behind `enabled: false` is still a daemon, and one parked behind a
    `box:` gate that is false on this box is still declared in the graph."""
    jobs = {}
    for name, job in node["jobs"].items():
        enabled = dict(job)
        enabled["enabled"] = True
        enabled.pop("box", None)
        jobs[name] = enabled
    return {"crons_live": True, "jobs": jobs, "services": node["services"]}


def _cron_surface(root: Path, repo_root: Path, engine_root: Path,
                  node: dict) -> list[tuple[str, str]]:
    """One `(label, command)` pair per rendered cron line, derived from the
    node's declared `cadences:` — each job rendered through crons.py's own
    renderer so today's six names are not baked in here."""
    surface: list[tuple[str, str]] = []
    for name in node["jobs"]:
        sub = {"crons_live": True, "jobs": {name: node["jobs"][name]},
               "services": {}}
        for line in crons.render_managed_lines(root, repo_root, engine_root, sub):
            surface.append((f"cadence:{name}", line))
    return surface


def _service_surface(repo_root: Path, node: dict) -> list[tuple[str, str]]:
    surface: list[tuple[str, str]] = []
    for name, svc in node["services"].items():
        if not svc.get("exec_start"):
            continue
        for line in crons.render_unit_file(name, svc, repo_root):
            if line.startswith("ExecStart="):
                surface.append((f"service:{name}", line))
    return surface


@pytest.fixture(scope="module")
def surface() -> list[tuple[str, str]]:
    root = locations.find_project_root(Path(__file__).resolve())
    assert root is not None, "no project root resolved from the test file"
    _, _cfg, repo_root, engine_root, raw = crons._resolve(root)
    node = _audit_node(raw)
    pairs = _cron_surface(root, repo_root, engine_root, node)
    pairs += _service_surface(repo_root, node)
    assert pairs, "heal/cron surface came back empty — the guard is vacuous"
    return pairs


def test_no_message_daemon_on_the_heal_cron_surface(surface):
    offenders = message_daemons(surface)
    assert not offenders, "message daemon(s) on the heal/cron surface:\n" + "\n".join(
        f"  {label}: {reason}\n    cmd: {cmd}" for label, cmd, reason in offenders
    )


def test_surface_names_its_real_members(surface):
    """The guard must be reading the real surface, not a stale copy."""
    labels = {label for label, _ in surface}
    assert "cadence:nudge_sweep" in labels
    assert "cadence:mail_poll" in labels
    assert "service:agi-reaper" in labels


def test_nudge_is_a_bounded_sweep(surface):
    """Positively assert the nudge is one bounded pass over local rows, so a
    future daemon wearing the nudge name is still caught."""
    cmds = [c for label, c in surface if label == "cadence:nudge_sweep"]
    assert cmds, "nudge_sweep not rendered"
    for cmd in cmds:
        assert "wake --all-local" in cmd, f"nudge is not the bounded sweep: {cmd}"
        assert not _DAEMON_RE.search(cmd), f"nudge grew a long-lived marker: {cmd}"


def test_guard_rejects_a_synthetic_daemon_by_name():
    """Falsification probe, in memory: a job named `message_router` running
    `send.py serve` must be rejected, by name."""
    offenders = message_daemons([
        ("cadence:message_router", "cd /x && python3 /x/send.py serve --forever"),
    ])
    assert offenders, "guard accepted a message daemon — vacuous"
    label, cmd, reason = offenders[0]
    assert label == "cadence:message_router"
    assert "message_router" in label and "send.py serve" in cmd
    assert "message-router" in reason or "serve" in reason


def test_synthetic_node_daemon_is_caught_through_the_derivation(surface):
    """The SAME builder that audits the real surface must surface a daemon
    added to the node — proof the surface is derived, not hardcoded."""
    root = locations.find_project_root(Path(__file__).resolve())
    _, _cfg, repo_root, engine_root, raw = crons._resolve(root)
    node = _audit_node(raw)
    node["jobs"]["message_router"] = {
        "enabled": True, "every_mins": 5, "schedule": None,
        "cmd": "python3 /opt/x/send.py serve", "log": None,
    }
    pairs = _cron_surface(root, repo_root, engine_root, node)
    assert any(label == "cadence:message_router" for label, _ in pairs), \
        "the synthetic job never reached the surface — derivation is blind"
    offenders = message_daemons(pairs)
    assert any("message_router" in label for label, _, _ in offenders), \
        "a daemon added to the node slipped through the derived surface"


def test_nudge_wearing_a_daemon_command_is_caught():
    """Same name, daemon body: `nudge_sweep` must not be a hiding place."""
    offenders = message_daemons([
        ("cadence:nudge_sweep", "python3 /x/send.py wake --all-local --forever"),
    ])
    assert offenders and "nudge_sweep" in offenders[0][0]