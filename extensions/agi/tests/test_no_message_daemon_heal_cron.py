#!/usr/bin/env python3
"""Absence-check for `goal:g7.31.4.3` falsifier 1 — no message daemon appears
on the heal/cron surface.

**The claim is an absence, so the check must be falsifiable by construction.**
Every inventory function here is *data in, findings out*: it takes a crons node
(the `jobs` / `services` mapping `crons.load_crons_node` returns) or a process
table as a PARAMETER and returns a list of finding strings. A caller can feed
a declaration that DOES contain a message daemon and watch it flagged BY NAME
— see the `test_falsifier_*` tests, which are the negative probe. A checker
that could only read one hardcoded file and always return "clean" would be
vacuous; this one is not.

Three surfaces are checked, matching the brief:

1. `message_job_findings`   — the closed message-job set AND each job's
   command. `mail_poll` and `nudge_sweep` must be PERIODIC TICKS (cron
   `every_mins`/`schedule`); no job may name itself a message daemon/router;
   and no job's `cmd`/`exec`/`exec_start` may LAUNCH one, whatever the job is
   called (a message daemon behind a generic job name is the direct way a
   daemon reaches the cron surface).
2. `message_service_findings` / `service_allowlist_findings` — the `services:`
   map. A systemd unit is long-running by construction, so any message token in
   a unit's name or exec argv is a message daemon; and any service outside the
   reviewed non-message allowlist is surfaced for review.
3. `find_message_daemon_processes` — the live process table. It takes
   `(pid, comm, args)` triples (injectable — `read_process_table` is the only
   place `ps` appears) and returns any process whose *program identity* looks
   like a message router/daemon and is not a known periodic tick.

**Program identity, not the whole argv blob.** A process is matched on the
basename of its first few argv tokens, not on a substring of the entire
command line: an agent's system-prompt text lives in argv and contains both
"message" and "daemon" many times over, so a naive substring scan of `ps args`
reports every running agent as a message daemon. That was measured on this box
before the token filter was added.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402
import locations  # noqa: E402

#: The closed set of jobs on the message path (goal:g7.31.4.3). Any other
#: message-flavoured job is a finding.
MESSAGE_JOBS = ("mail_poll", "nudge_sweep")

#: Substrings that mark a name/argv token as belonging to the message path.
MESSAGE_TOKENS = ("message", "msg", "mail", "nudge", "inbox")

#: Substrings that mark a name/argv token as a long-running/daemon shape.
DAEMON_TOKENS = ("daemon", "router", "serve", "listen", "watch", "loop")

#: The two systemd units the live crons node declares today, neither of which
#: is on the message path. Any service outside this set is surfaced for review
#: rather than silently accepted — the whole point is that a new message
#: service cannot land unnoticed.
KNOWN_NON_MESSAGE_SERVICES = frozenset(
    {"agi-alarms-sanctuary-master", "agi-reaper"}
)

#: Marker of this test's own harness invocation, excluded from the LIVE scan
#: only — the scanner must not count its own pytest command line as a daemon.
SELF_MARK = "test_no_message_daemon"

#: Program-identity filter: scan only the first few argv tokens, and only
#: tokens short enough to be a program name / subcommand rather than a whole
#: prompt or shell script blob.
_TOKENS_SCANNED = 8
_MAX_NAME_LEN = 40

#: A job `cmd` is a whole shell line (daemon may sit behind `cd`/`&&`/env
#: prefixes), so it gets a wider token window than a process argv — but it is
#: still only token basenames that are examined, never the command text as a
#: substring.
_CMD_TOKENS_SCANNED = 40


def _name_tokens(comm: str, args: str, limit: int = _TOKENS_SCANNED) -> list[str]:
    """The lowercased basenames of the first `limit` argv tokens — the tokens
    that name a program or a subcommand, not prompt text or a script body."""
    tokens = [comm] + (args or "").split()
    out = []
    for tok in tokens[:limit]:
        base = tok.rsplit("/", 1)[-1]
        if base and len(base) <= _MAX_NAME_LEN:
            out.append(base.lower())
    return out


def _message_daemon_tokens(tokens) -> bool:
    """One implementation of the verdict both scanners share: a program
    identity is a message daemon when its token list carries a message token
    AND a daemon/router token — never a substring of the whole text."""
    return any(_message_flavored(t) for t in tokens) and any(
        _daemon_flavored(t) for t in tokens
    )


def _message_flavored(text: str) -> bool:
    return any(tok in text for tok in MESSAGE_TOKENS)


def _daemon_flavored(text: str) -> bool:
    return any(tok in text for tok in DAEMON_TOKENS)


# --- surface 1: jobs ---------------------------------------------------


def message_job_findings(jobs: dict, known_jobs=crons.KNOWN_JOBS) -> list[str]:
    """Findings for a crons node's `jobs` mapping (data in, findings out).

    * every job on the message path must be a PERIODIC TICK — a cron line has
      `every_mins` or `schedule`, so its command returns and the next tick
      starts a fresh one; no `every_mins`/`schedule` would mean a job whose
      shape is a blocking daemon.
    * no job outside the closed `MESSAGE_JOBS` set may touch the message path.
    * no `KNOWN_JOBS` name may itself be a message daemon/router.
    """
    findings: list[str] = []

    for name in known_jobs:
        low = name.lower()
        if _message_flavored(low) and _daemon_flavored(low):
            findings.append(
                f"KNOWN_JOBS entry {name!r} names itself a message daemon/router"
            )

    for name, job in jobs.items():
        low = name.lower()
        periodic = (
            job.get("every_mins") is not None or job.get("schedule") is not None
        )
        if name in MESSAGE_JOBS:
            if not periodic:
                findings.append(
                    f"message job {name!r} declares no periodic tick "
                    f"(every_mins/schedule) — a blocking daemon shape"
                )
        elif _message_flavored(low):
            findings.append(
                f"job {name!r} touches the message path but is outside the "
                f"closed set {sorted(MESSAGE_JOBS)}"
            )
        # The job's COMMAND, not just its name: a generic job with an
        # innocuous name can still launch a message daemon, which is the most
        # direct way one appears in the cron surface.
        for field in ("cmd", "exec", "exec_start"):
            raw = job.get(field)
            if not (isinstance(raw, str) and raw.strip()):
                continue
            if _message_daemon_tokens(
                _name_tokens("", raw, limit=_CMD_TOKENS_SCANNED)
            ):
                findings.append(
                    f"job {name!r} launches a message daemon via {field}: "
                    f"{raw!r}"
                )
    return findings


# --- surface 2: services -----------------------------------------------


def message_service_findings(services: dict) -> list[str]:
    """Findings for a crons node's `services` mapping.

    A systemd service is long-running by construction, so a message token in
    the unit's name or its exec argv is a message daemon — no schedule can
    excuse it.
    """
    findings: list[str] = []
    for name, svc in services.items():
        tokens = _name_tokens(name, svc.get("exec_start") or "")
        blob = " ".join(tokens)
        if _message_flavored(blob):
            findings.append(
                f"service {name!r} looks like a message daemon — "
                f"exec_start={svc.get('exec_start')!r}"
            )
    return findings


def service_allowlist_findings(
    services: dict, known=KNOWN_NON_MESSAGE_SERVICES
) -> list[str]:
    """Any service not in the reviewed non-message allowlist is surfaced."""
    return [
        f"service {name!r} is not in the reviewed non-message allowlist "
        f"{sorted(known)}"
        for name in services
        if name not in known
    ]


# --- surface 3: live processes -----------------------------------------


def find_message_daemon_processes(
    procs, periodic_jobs=MESSAGE_JOBS
) -> list[str]:
    """Findings for an injectable process table of `(pid, comm, args)`.

    A process is flagged when its program-identity tokens carry both a message
    token and a daemon/router token, unless its argv names a known periodic
    tick (a `mail_poll`/`nudge_sweep` cron invocation is transient, not a
    daemon).
    """
    findings: list[str] = []
    for pid, comm, args in procs:
        tokens = _name_tokens(comm, args)
        if any(job in tokens for job in periodic_jobs):
            continue
        if _message_daemon_tokens(tokens):
            findings.append(f"pid {pid} comm={comm!r} args={args!r}")
    return findings


def read_process_table() -> list[tuple[str, str, str]]:
    """The one place `ps` appears. The scanner itself never hardcodes it."""
    out = subprocess.run(
        ["ps", "-eo", "pid=,comm=,args="],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    procs: list[tuple[str, str, str]] = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 2)
        if len(parts) < 2:
            continue
        procs.append(
            (parts[0], parts[1], parts[2] if len(parts) > 2 else parts[1])
        )
    return procs


def live_process_findings() -> list[str]:
    self_pid = str(os.getpid())
    procs = [
        p
        for p in read_process_table()
        if p[0] != self_pid and SELF_MARK not in p[2]
    ]
    return find_message_daemon_processes(procs)


# --- live node ---------------------------------------------------------


def live_crons_node() -> dict:
    root = locations.find_project_root(Path(__file__).resolve())
    assert root is not None, "no project root resolved above this test file"
    return crons.load_crons_node(root)


# --- tests: the live claim ---------------------------------------------


def test_live_message_jobs_are_periodic_ticks():
    node = live_crons_node()
    findings = message_job_findings(node["jobs"])
    assert findings == [], findings
    assert "mail_poll" in node["jobs"], "mail_poll must be declared"
    assert "nudge_sweep" in node["jobs"], "nudge_sweep must be declared"
    for name in MESSAGE_JOBS:
        job = node["jobs"][name]
        assert job["every_mins"] is not None or job["schedule"] is not None


def test_live_services_carry_no_message_daemon():
    node = live_crons_node()
    findings = message_service_findings(node["services"])
    assert findings == [], findings


def test_live_service_inventory_is_the_reviewed_set():
    node = live_crons_node()
    findings = service_allowlist_findings(node["services"])
    assert findings == [], findings


def test_live_process_table_has_no_message_daemon():
    findings = live_process_findings()
    print(f"[live-scan] processes scanned, findings={findings}")
    assert findings == [], findings


# --- tests: the negative probe (falsifiable by construction) -----------


def test_falsifier_a_message_daemon_service_is_flagged_by_name():
    services = {
        "agi-reaper": {"enabled": True, "exec_start": "python3 heal.py watch"},
        "message-router": {
            "enabled": True,
            "exec_start": "python3 /srv/msg_router.py serve",
        },
    }
    findings = message_service_findings(services)
    assert findings, "a message_router service MUST be flagged"
    assert any("message-router" in f for f in findings), findings


def test_falsifier_a_blocking_message_job_is_flagged():
    jobs = {
        "mail_poll": {"enabled": True, "every_mins": None, "schedule": None},
    }
    findings = message_job_findings(jobs)
    assert findings and any("mail_poll" in f for f in findings), findings


def test_falsifier_an_unexpected_message_job_is_flagged():
    jobs = {
        "mail_poll": {"enabled": True, "every_mins": 5},
        "message_daemon": {"enabled": True, "every_mins": 1},
    }
    findings = message_job_findings(jobs)
    assert findings and any("message_daemon" in f for f in findings), findings


def test_falsifier_a_message_daemon_process_is_flagged():
    procs = [
        ("1", "systemd", "/sbin/init"),
        ("77", "message-router", "/usr/bin/message-router --serve"),
        ("99", "python3", "python3 /srv/msg_router.py serve --forever"),
    ]
    findings = find_message_daemon_processes(procs)
    assert len(findings) == 2, findings


def test_falsifier_a_message_daemon_cmd_in_a_generic_job_is_flagged():
    """The parent's A/B probe, locked: the job NAME is innocuous, the COMMAND
    launches a message daemon, and the checker must still flag it by name."""
    for cmd in (
        "python3 /srv/mail_daemon.py --serve --forever",
        "python3 /srv/msg_router.py serve",
    ):
        findings = message_job_findings(
            {"relay_bridge": {"every_mins": 5, "enabled": True, "cmd": cmd}}
        )
        assert findings, f"a daemon cmd in a generic job MUST be flagged: {cmd!r}"
        assert any("relay_bridge" in f for f in findings), findings


def test_falsifier_a_daemon_in_exec_start_is_flagged():
    findings = message_job_findings(
        {"relay_bridge": {"every_mins": 5, "exec_start": "/usr/bin/inbox-router watch"}}
    )
    assert findings and any("relay_bridge" in f for f in findings), findings


def test_falsifier_a_benign_generic_job_cmd_is_not_flagged():
    clean = {
        "prime_merge": {
            "every_mins": 5,
            "cmd": "python3 {repo_root}/extensions/agi/bin/prime_merge.py tick",
        },
        "relay_bridge": {
            "every_mins": 5,
            "cmd": "cd /srv && python3 heal.py watch --poll-s 30",
        },
    }
    assert message_job_findings(clean) == []


def test_falsifier_known_ticks_and_clean_tables_are_not_flagged():
    clean_procs = [
        ("1", "systemd", "/sbin/init"),
        ("42", "python3", "python3 /srv/heal.py watch --poll-s 30"),
        ("43", "python3", "python3 send.py wake --all-local"),
    ]
    assert find_message_daemon_processes(clean_procs) == []
    clean_jobs = {
        "mail_poll": {"enabled": True, "every_mins": 5},
        "nudge_sweep": {"enabled": True, "every_mins": 2},
        "grid_sync": {"enabled": True, "every_mins": 5},
    }
    assert message_job_findings(clean_jobs) == []
