"""Regression guard: the heal/cron surface gains NO message-routing daemon.

Standing L4 ruling — messages ride repo + nudge (`send.py`), never a resident
router. The surface is the declarative pair in `.agi/nodes/.geometry/crons.md`:
`cadences:` (periodic crontab ticks) and `services:` (long-lived systemd
units). This test reads the REAL node through `crons.load_crons_node` — never
a hard-coded list — so a service/cadence added to the real node flows through
the same predicate that the positive control proves can fail.

TWO INDEPENDENT CHANNELS, because one was not enough. The parent measured the
residue in v1 of this guard: a router whose name and cmd carry NO seeded
keyword (`services: {agi-outbound-hub: {exec_start: "python3 hubd.py serve"}}`)
sailed past the keyword predicate, because that predicate can only prove it
matches the literal it was seeded with. So v2 adds an ALLOWLIST + NOVELTY
guard as the load-bearing channel:

  (a) NOVELTY — ANY *enabled* entry (job or service) whose name is not in
      `ALLOWED_SURFACE` is flagged. A newly added daemon of ANY name is caught,
      because novelty itself forces review. Its name need not hint at routing.
  (b) KEYWORDS — ANY entry (allowlisted or not, enabled or not) whose name or
      exec/cmd matches the message-routing predicate is flagged. This is the
      belt-and-braces second channel; it survives even a name that was
      reviewed onto the allowlist.

`ALLOWED_SURFACE` names EVERY entry the real node currently declares, in both
tables, each with a one-line reason it is not a message daemon.
`test_allowed_surface_matches_real_node` asserts set equality, so an ADDITION
(a new daemon) and a REMOVAL (a surface quietly losing a job) are both visible.

Why `mail_poll` and `nudge_sweep` are NOT daemons (explicit classification):
both are PERIODIC CRON TICKS. They wake on a schedule, do one bounded pass —
read hub-fetched inboxes / sweep nudges via `send.py` — and exit. Neither
holds a socket, a queue, or a pid between runs. A daemon, by contrast, is a
process that stays resident to route/deliver/queue messages between seats.
The predicate would match their names on keywords alone, which is exactly why
they are named in `KEYWORD_EXEMPT_TICKS` below with this reason rather than
silently exempted. The two real services are the reap-only reaper
(`heal.py watch`) and the alarm rotator (`rotate.py alarms`): neither matches
the keyword predicate.
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

#: EVERY entry the real `.agi` crons node declares today, both tables, each
#: with the reason it is not a message-routing daemon. Measured, not guessed:
#: raw frontmatter parse + `crons.load_crons_node` agree (7 jobs, 2 services).
#: Set equality is asserted against the live node below, so an entry added or
#: removed here without the node changing (or vice versa) fails loudly.
ALLOWED_SURFACE = {
    "job:grid_sync": "periodic 5-min grid commit/render tick",
    "job:branch_push": "hourly git push of the checked-out branch",
    "job:mail_poll": "periodic tick; one bounded inbox pass, exits",
    "job:nudge_sweep": "periodic tick; one bounded nudge sweep, exits",
    "job:publish_engine": "declared disabled; engine publish is vestigial (g11)",
    "job:engine_push": "declared disabled; duplicates branch_push against one remote",
    "job:prime_merge": "periodic 6-hourly town->season merge tick",
    "service:agi-alarms-sanctuary-master": "alarm rotator; rotates, routes nothing",
    "service:agi-reaper": "reap-only healer (`heal.py watch`); no message path",
}

#: Jobs allowed to match the keyword predicate WITHOUT being flagged, each
#: because it is a bounded periodic tick rather than a resident process.
#: Deliberately narrow: exactly the two names whose names trip the predicate.
KEYWORD_EXEMPT_TICKS = {
    "job:mail_poll": "periodic cron tick; one bounded inbox pass, exits",
    "job:nudge_sweep": "periodic cron tick; one bounded nudge sweep, exits",
}


def _haystack(name: str, spec: dict) -> str:
    cmd = spec.get("exec_start") or spec.get("cmd") or ""
    return f"{name} {cmd}"


def _matches_message_keywords(name: str, spec: dict) -> bool:
    hay = _haystack(name, spec)
    return any(re.search(p, hay, re.I) for p in MESSAGE_DAEMON_PATTERNS)


def declared_surface(node: dict) -> set[str]:
    """`{kind:name}` for every entry the node declares, both tables."""
    return {f"job:{n}" for n in node.get("jobs", {})} | {
        f"service:{n}" for n in node.get("services", {})}


def find_message_daemons(node: dict) -> list[str]:
    """Names on the heal/cron surface that are message-routing daemons.

    Two channels, unioned, applied to BOTH `services:` (long-lived by
    construction) and `jobs:` (cadences) — a router parked in either table is
    a router. Returns a sorted, de-duplicated list; empty for a clean surface.
    """
    flagged: dict[str, str] = {}
    tables = (("service", node.get("services", {})),
              ("job", node.get("jobs", {})))
    for kind, table in tables:
        for name, spec in table.items():
            key = f"{kind}:{name}"
            # (a) NOVELTY: an enabled entry nobody has reviewed is a daemon
            # until a human says otherwise, whatever it is called.
            if spec.get("enabled", True) and key not in ALLOWED_SURFACE:
                flagged[key] = "unvetted enabled entry, not in ALLOWED_SURFACE"
            # (b) KEYWORDS: belt-and-braces, allowlisted or not, enabled or not.
            if key not in KEYWORD_EXEMPT_TICKS and _matches_message_keywords(name, spec):
                flagged[key] = "name/exec matches message-daemon keywords"
    return sorted(flagged)


def _write_node(root: Path, services: dict | None, cadences: dict) -> None:
    p = root / crons.CRONS_NODE_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = {"id": "cron:crons", "type": "cron", "crons_live": True,
          "cadences": cadences}
    if services is not None:
        fm["services"] = services
    p.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")


def _graph_root() -> Path:
    return Path(crons.__file__).resolve().parents[3] / ".agi"


# --- positive controls: the guard MUST be able to fail --------------------


def test_planted_message_router_service_is_flagged(tmp_path):
    """A `services:` entry that routes messages between seats is flagged."""
    root = tmp_path / "proj"
    root.mkdir()
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
    root.mkdir()
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


def test_unvetted_neutral_name_service_is_flagged(tmp_path):
    """THE LOAD-BEARING CONTROL: no seeded keyword, only novelty.

    `agi-outbound-hub` with a comment-less `python3 hubd.py serve` matches
    NO message keyword — the v1 keyword-only predicate returned `[]` for
    exactly this shape (the parent's measured residue). The novelty channel
    must flag it because it is enabled and unvetted.
    """
    root = tmp_path / "proj"
    root.mkdir()
    _write_node(
        root,
        services={"agi-outbound-hub": {
            "enabled": True, "exec_start": "python3 hubd.py serve"}},
        cadences={"grid_sync": {"every_mins": 5, "enabled": True}},
    )
    node = crons.load_crons_node(root)
    flagged = find_message_daemons(node)
    assert "service:agi-outbound-hub" in flagged, (
        "a neutral-named, enabled, unvetted service slipped through — "
        f"the novelty guard is not load-bearing: {flagged!r}")


def test_unvetted_neutral_name_job_is_flagged(tmp_path):
    """The same novelty guard applies to a new cadence, not just a service."""
    root = tmp_path / "proj"
    root.mkdir()
    _write_node(
        root,
        services=None,
        cadences={
            "grid_sync": {"every_mins": 5, "enabled": True},
            "agi-outbound-hub": {"every_mins": 1,
                                 "cmd": "python3 hubd.py serve"},
        },
    )
    node = crons.load_crons_node(root)
    assert "job:agi-outbound-hub" in find_message_daemons(node)


def test_disabled_unvetted_entry_is_keyword_checked_not_novelty_flagged(tmp_path):
    """Novelty is for ENABLED entries; keywords still catch a disabled router.

    A disabled entry is inert, so novelty alone need not fire — but the
    keyword channel deliberately ignores `enabled`, so a disabled router is
    still visible rather than hidden by its own off switch.
    """
    root = tmp_path / "proj"
    root.mkdir()
    _write_node(
        root,
        services=None,
        cadences={"agi-message-router": {
            "every_mins": 1, "enabled": False,
            "cmd": "python3 router.py serve"}},
    )
    node = crons.load_crons_node(root)
    assert "job:agi-message-router" in find_message_daemons(node)


def test_periodic_ticks_are_not_flagged(tmp_path):
    """The explicit non-daemon classification holds on their own keywords."""
    root = tmp_path / "proj"
    root.mkdir()
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


# --- negative controls: the REAL surface passes --------------------------


def test_allowed_surface_matches_real_node():
    """ALLOWED_SURFACE names EXACTLY the live surface — no more, no less.

    An addition (a new daemon, or an over-eager allowlist entry) and a removal
    (a live job/service disappearing from the node) both fail here.
    """
    node = crons.load_crons_node(_graph_root())
    assert node["jobs"], "real crons node declared no jobs — wrong root?"
    assert node["services"], "real crons node declared no services — wrong root?"
    assert declared_surface(node) == set(ALLOWED_SURFACE)


def test_real_heal_cron_surface_has_no_message_daemon():
    """The live `.agi` crons node carries no message-routing daemon."""
    node = crons.load_crons_node(_graph_root())
    # The predicate read a real, non-empty surface (guards against a wrong
    # path yielding an empty dict and passing by accident).
    assert node["jobs"], "real crons node declared no jobs — wrong root?"
    assert node["services"], "real crons node declared no services — wrong root?"
    assert find_message_daemons(node) == []
