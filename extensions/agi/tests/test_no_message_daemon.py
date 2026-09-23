"""goal:g7.31.4.3 -- the durable tripwire that no message daemon appears on
the heal/cron surface.

Standing L4 ruling for goal:g7.31.4: messages are *repo + nudge*, NOT a
router process. This test pins that shape so a future edit that adds a
message daemon has to break a named test rather than land silently:

  * ``send.py`` is ONE-SHOT by construction -- its argparse verb set contains
    none of ``serve`` / ``daemon`` / ``watch`` / ``listen`` / ``loop`` /
    ``run`` / ``start`` / ``start-server``. The source is parsed with ``ast``,
    never imported, so the probe cannot be fooled by an import side effect and
    cannot itself start anything.
  * the declared ``services:`` table in ``.agi/nodes/.geometry/crons.md``
    never runs a message router: a service may run ``send.py`` only with a
    one-shot verb, and no message program sits behind ``while True`` /
    ``serve`` / ``daemon`` / ``listen`` / ``loop``.
  * ``nudge_sweep`` is a CRON cadence running the one-shot
    ``send.py wake --all-local`` sweep, never a service -- the nudge is
    retried by the timer, not by a resident process.

The file READS source and the live graph; it mutates nothing. Two tests are
deliberately non-vacuous: the AST probe asserts it found the real verb set,
and a factory test plants a message daemon and asserts the detector names it.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402

SEND_PY = BIN / "send.py"

#: Verbs that mean "run forever". None of these may ever appear as a
#: `send.py` subcommand; the message seam has no resident mode.
LONG_RUNNING_VERBS = frozenset({
    "serve", "daemon", "watch", "listen", "loop", "run", "start",
    "start-server",
})

#: The only verbs a service or cadence may invoke `send.py` with. Each returns;
#: none stays resident.
ONESHOT_VERBS = frozenset({
    "send", "read", "peek", "wake", "rooms", "audience", "vote", "ask",
    "report", "whois", "status", "escalate", "veto", "keygen",
    "prime-excluded",
})

#: Substrings that mark a command line as touching the message seam at all.
MESSAGE_MARKERS = ("send.py", "message", "router", "comms")


def _send_py_verbs(source: str) -> set[str]:
    """Every `add_parser("verb", ...)` name in send.py's argparse setup, via
    `ast` -- no import, so nothing the module does at import time can run."""
    verbs: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_parser"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            verbs.add(node.args[0].value)
    return verbs


def _send_py_verb_in(exec_start: str) -> str | None:
    """The verb token that follows a `send.py` path in an exec_start, or None
    when there is no `send.py` / no verb after it."""
    tokens = exec_start.split()
    for i, tok in enumerate(tokens):
        if tok.endswith("send.py"):
            for nxt in tokens[i + 1:]:
                if nxt.startswith("-"):
                    continue
                return nxt.strip(";&|()")
            return None
    return None


def _mentions_message(exec_start: str) -> bool:
    low = exec_start.lower()
    return any(marker in low for marker in MESSAGE_MARKERS)


def _service_offenders(services: dict) -> list[str]:
    """Name every enabled service whose `exec_start` is a message daemon.

    A service is an offender when it (a) runs `send.py` with a verb outside
    ONESHOT_VERBS, (b) runs `send.py` with no verb at all, or (c) wraps a
    message program in a resident marker (`while True`, or a long-running
    verb token). Returns one string per offending service, naming the service
    and the exact exec_start so a failure is actionable.
    """
    offenders: list[str] = []
    for name, svc in services.items():
        if not svc.get("enabled", True):
            continue
        exec_start = svc.get("exec_start") or ""
        low = exec_start.lower()
        message = _mentions_message(exec_start)

        if "send.py" in exec_start:
            verb = _send_py_verb_in(exec_start)
            if verb is None:
                offenders.append(
                    f"{name}: exec_start runs send.py with no verb "
                    f"(a required-verb CLI): {exec_start}"
                )
            elif verb not in ONESHOT_VERBS:
                offenders.append(
                    f"{name}: exec_start runs send.py with non-one-shot verb "
                    f"{verb!r}: {exec_start}"
                )

        if message and "while true" in low:
            offenders.append(
                f"{name}: resident `while True` wraps a message program: "
                f"{exec_start}"
            )
        if message:
            verbs = {t.strip(";&|()").lower() for t in exec_start.split()}
            resident = sorted(verbs & LONG_RUNNING_VERBS)
            if resident:
                offenders.append(
                    f"{name}: exec_start runs a message program with "
                    f"long-running verb(s) {resident}: {exec_start}"
                )
    return offenders


def _graph_root() -> Path | None:
    """The live graph root (the `.agi` dir) when discoverable, else None."""
    try:
        import locations

        return locations.find_project_root(Path(__file__).resolve())
    except Exception:  # noqa: BLE001 -- a layout we cannot resolve: skip, not crash
        return None


def _live_crons_node() -> tuple[Path, dict] | None:
    """`(root, parsed crons node)` for the live graph, or None when the graph
    root or its crons node is not discoverable (the caller skips cleanly)."""
    root = _graph_root()
    if root is None:
        return None
    if not (Path(root) / crons.CRONS_NODE_REL).is_file():
        return None
    return Path(root), crons.load_crons_node(Path(root))


# --- the send.py verb tripwire ------------------------------------------


def test_send_py_declares_no_long_running_verb():
    """The message seam's verb set contains none of the resident verbs."""
    verbs = _send_py_verbs(SEND_PY.read_text(encoding="utf-8"))
    assert verbs, "no add_parser() verbs found -- the AST probe itself is broken"
    assert "wake" in verbs and "send" in verbs, (
        f"the AST probe did not find the real send.py verbs; found {sorted(verbs)}"
    )
    offending = sorted(verbs & LONG_RUNNING_VERBS)
    assert not offending, (
        f"send.py declares long-running verb(s) {offending}: the message seam "
        f"must stay one-shot (verb set is {sorted(verbs)})"
    )


# --- the declared services table tripwire -------------------------------


def test_live_services_table_has_no_message_daemon():
    """Read the LIVE crons node and refuse any service that is a message
    router. Skips cleanly when the graph root is not discoverable."""
    live = _live_crons_node()
    if live is None:
        pytest.skip("graph root / crons node not discoverable -- nothing live to read")
    _root, node = live
    offenders = _service_offenders(node["services"])
    assert not offenders, (
        "message daemon on the heal/cron surface (goal:g7.31.4.3 falsifier): "
        + "; ".join(offenders)
    )


def test_detector_catches_a_planted_message_daemon():
    """Non-vacuity: the detector above actually fails on a planted daemon, so
    a green result means the surface is clean, not that the check is dead."""
    planted_verb = {
        "agi-message-router": {
            "enabled": True,
            "exec_start": "/usr/bin/python3 {repo_root}/extensions/agi/bin/send.py "
                          "serve --root {root}",
            "restart": "on-failure",
        }
    }
    offenders = _service_offenders(planted_verb)
    assert offenders and "agi-message-router" in offenders[0], offenders

    planted_loop = {
        "agi-message-loop": {
            "enabled": True,
            "exec_start": "/bin/bash -c 'while True; do python3 "
                          "{repo_root}/extensions/agi/bin/send.py wake --all-local; "
                          "done'",
            "restart": "always",
        }
    }
    offenders = _service_offenders(planted_loop)
    assert offenders and "agi-message-loop" in offenders[0], offenders

    # ...and an ordinary non-message service is NOT flagged.
    assert _service_offenders({
        "agi-reaper": {
            "enabled": True,
            "exec_start": "/usr/bin/python3 {repo_root}/extensions/agi/bin/heal.py "
                          "watch --root {repo_root} --poll-s 30",
            "restart": "on-failure",
        }
    }) == []


# --- the nudge sweep is a timer, not a service --------------------------


def test_nudge_sweep_renders_as_a_cron_one_shot_not_a_service(tmp_path):
    """`nudge_sweep` renders as a one-shot cron line (`send.py wake
    --all-local`) and is never a service. Uses a fixture crons node with only
    nudge_sweep enabled, so no git context is required."""
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text("{}\n")
    frontmatter = {
        "id": "cron:crons",
        "type": "cron",
        "crons_live": True,
        "cadences": {"nudge_sweep": {"every_mins": 2, "enabled": True}},
    }
    (root / crons.CRONS_NODE_REL).write_text(
        "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n\nBody.\n"
    )
    node = crons.load_crons_node(root)
    assert "nudge_sweep" in node["jobs"]
    assert "nudge_sweep" not in node["services"]

    lines = crons.render_managed_lines(root, root, root, node, box_name="core-town")
    assert len(lines) == 1, lines
    assert "send.py" in lines[0] and "wake --all-local" in lines[0], lines[0]
    assert not any(verb in lines[0] for verb in LONG_RUNNING_VERBS), lines[0]