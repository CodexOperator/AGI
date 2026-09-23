"""Absence gate for goal:g7.31.4.3 — no message daemon on the heal/cron surface.

Standing L4 ruling: repo + nudge is the transport model, not a router process.
This test enumerates the WHOLE heal/cron surface at the branch tip and refuses
any entry that is a message daemon:

  * the declared systemd `services:` and cron `cadences:` in the LIVE node
    `.agi/nodes/.geometry/crons.md` (read through `crons.load_crons_node`, the
    same reader `crons.py apply` uses — never a copied list),
  * the cron lines `crons.render_managed_lines` actually derives from them,
  * the live process table (`ps`), restricted to python scripts under
    `extensions/agi/bin`.

Definition used here, from the goal brief: a message daemon = PERSISTENT (a
systemd service, or a `watch`/`serve` loop) AND MESSAGE-ROUTING (its script
reads an inbox and forwards/relays). A cron job that merely polls
(`mail_poll` -> `send.py read`) or nudges (`nudge_sweep` -> `send.py wake`) is
NOT a daemon: it runs once and exits. The last two tests make that distinction
an assertion rather than a comment, and feed a synthetic router service into
the SAME gate to prove the gate is not a no-op.
"""
from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402
import locations  # noqa: E402

ROOT = locations.find_project_root(Path(__file__).resolve())

#: A script basename carrying any of these is a message router by NAME.
ROUTER_STEM_TOKENS = ("router", "relay", "daemon", "dispatchd")
#: Message ENGINES: scripts whose whole job is to move messages between
#: inboxes, even though the name carries no router word. Name-based on
#: purpose — a source-text heuristic false-positives on docstrings (heal.py
#: mentions "deliver" in prose), which would make the gate refuse itself.
ROUTING_SCRIPTS = frozenset({"send.py", "rotate.py", "mail_alert.py",
                             "message_router.py", "mail_router.py"})
#: Exec-string markers of a long-lived loop. A one-shot cron command has none.
PERSISTENT_EXEC_TOKENS = (" watch", " serve", " --loop", " daemon", "while true",
                          " tail -f")


def _exec_of(entry: dict) -> str:
    return str(entry.get("exec_start") or entry.get("cmd") or "")


def _script_token(exec_start: str) -> str:
    """The last `.py`/`.sh` token of an exec string, or ''."""
    try:
        tokens = shlex.split(exec_start)
    except ValueError:
        tokens = exec_start.split()
    for tok in reversed(tokens):
        if tok.endswith((".py", ".sh")):
            return tok
    return ""


def _is_routing(token: str) -> bool:
    name = Path(token).name.lower()
    if name in ROUTING_SCRIPTS:
        return True
    return any(t in Path(token).stem.lower() for t in ROUTER_STEM_TOKENS)


def is_message_daemon(entry: dict) -> bool:
    """PERSISTENT and MESSAGE-ROUTING, exactly the brief's definition.

    persistent := a `watch`/`serve`/loop exec, or `restart: always`.
    routing    := the exec's script is a message engine by name.
    """
    ex = _exec_of(entry)
    token = _script_token(ex)
    if not token:
        return False
    persistent = (str(entry.get("restart") or "").lower() == "always"
                  or any(t in ex for t in PERSISTENT_EXEC_TOKENS))
    return persistent and _is_routing(token)


def surface_violations(services: dict, jobs: dict = None) -> list[str]:
    """The ONE gate: name every declared service/cadence that is a daemon."""
    out: list[str] = []
    for name, svc in (services or {}).items():
        if is_message_daemon(svc):
            out.append(f"service {name}: {_exec_of(svc)}")
    for name, job in (jobs or {}).items():
        if is_message_daemon(job):
            out.append(f"cadence {name}: {_exec_of(job)}")
    return out


def _agi_bin_processes() -> list[tuple[int, int, str]]:
    """(pid, etimes, script_path) for python processes whose OWN argv[1] is a
    script under extensions/agi/bin — argv-based, so an agent prompt that
    mentions such a path in its text is not mistaken for a process."""
    res = subprocess.run(["ps", "-eo", "pid,etimes,args"], capture_output=True,
                         text=True)
    rows: list[tuple[int, int, str]] = []
    for line in res.stdout.splitlines()[1:]:
        parts = line.split(None, 2)
        if len(parts) < 3:
            continue
        pid, etimes, args = parts
        try:
            argv = shlex.split(args)
        except ValueError:
            continue
        if len(argv) < 2:
            continue
        if not Path(argv[0]).name.startswith("python"):
            continue
        script = argv[1]
        if "extensions/agi/bin/" in script and script.endswith(".py"):
            try:
                rows.append((int(pid), int(etimes), script))
            except ValueError:
                continue
    return rows


# --- the live surface: declared services + cadences + rendered lines --------


def test_declared_surface_is_non_empty():
    """An absence claim over an empty enumeration proves nothing."""
    node = crons.load_crons_node(ROOT)
    assert node["services"], "no declared services enumerated — vacuous gate"
    assert node["jobs"], "no declared cadences enumerated — vacuous gate"


def test_no_message_daemon_declared_in_crons_node():
    node = crons.load_crons_node(ROOT)
    violations = surface_violations(node["services"], node["jobs"])
    assert not violations, "message daemon declared in crons.md: " + "; ".join(violations)


def test_no_message_daemon_in_rendered_cron_lines():
    root, _cfg, repo_root, engine_root, node = crons._resolve(ROOT)
    lines = crons.render_managed_lines(root, repo_root, engine_root, node)
    assert lines, "crons_live but render_managed_lines emitted nothing — vacuous gate"
    jobs = {f"rendered[{i}]": {"cmd": line} for i, line in enumerate(lines)}
    violations = surface_violations({}, jobs)
    assert not violations, "message daemon in rendered cron line: " + "; ".join(violations)


def test_no_long_lived_message_router_in_process_table():
    offenders = [
        f"pid={pid} etimes={etimes} {script}"
        for pid, etimes, script in _agi_bin_processes()
        if etimes >= 60 and any(t in Path(script).stem.lower() for t in ROUTER_STEM_TOKENS)
    ]
    assert not offenders, "long-lived message router live: " + "; ".join(offenders)


# --- the negative probe and its positive control ----------------------------


def test_gate_rejects_a_synthetic_message_daemon_by_name():
    """NEGATIVE PROBE: a service whose exec is a long-lived router MUST be
    refused, and named. A gate that cannot reject this proves nothing."""
    synthetic = {
        "agi-message-router": {
            "enabled": True,
            "exec_start": "{repo_root}/extensions/agi/bin/message_router.py --serve --watch",
            "restart": "always",
        }
    }
    violations = surface_violations(synthetic)
    assert violations, "gate ACCEPTED a synthetic message daemon"
    assert "agi-message-router" in violations[0]
    assert "message_router.py" in violations[0]


def test_poll_and_nudge_cron_jobs_are_not_daemons_but_a_service_would_be():
    """The distinction the brief demands, asserted: the SAME message-routing
    script is a daemon as a service and is NOT one as a one-shot cron command."""
    poll = {"cmd": "python3 {repo_root}/extensions/agi/bin/send.py read --box-local"}
    sweep = {"cmd": "python3 {repo_root}/extensions/agi/bin/send.py wake --all-local"}
    assert not is_message_daemon(poll)
    assert not is_message_daemon(sweep)
    # the SAME poll command as a systemd service (restart: always) IS a daemon,
    # so the gate is the persistence axis, not a no-op.
    as_service = {"exec_start": poll["cmd"], "restart": "always"}
    assert is_message_daemon(as_service)
