"""Regression guard: the heal/cron surface gains NO message-routing daemon.

Standing L4 ruling — messages ride repo + nudge (`send.py`), never a resident
router. The surface is the declarative pair in `.agi/nodes/.geometry/crons.md`:
`cadences:` (periodic crontab ticks) and `services:` (long-lived systemd
units). This test reads the REAL node through `crons.load_crons_node` — never
a hard-coded list — so a service/cadence added to the real node flows through
the same predicate that the positive control proves can fail.

THREE CHANNELS, because two were not enough. v1 was keyword-only; the parent
measured that a router named `agi-outbound-hub` with `exec_start: "python3
hubd.py serve"` sailed past it. v2 added novelty keyed on `kind:name`, which
caught a NEW name — but the parent then measured the residue this version
closes (probe B): a name ALREADY on the allowlist whose exec is swapped for a
neutral resident router

    {"services": {"agi-reaper": {"enabled": True,
                                 "exec_start": "python3 hubd.py serve"}}}
    v2 novelty  -> []   (the name is reviewed, so novelty is silent)
    v2 keyword  -> []   (no seeded keyword in name or exec)

is invisible. A reviewed NAME whose exec changed is exactly the new daemon
process the goal's falsifier forbids. So v3 reviews the whole
`(kind, name, exec/cmd)` tuple, not the name alone:

  (a) NOVELTY — ANY *enabled* entry (job or service) whose `kind:name` is not
      in `ALLOWED_SURFACE` is flagged. A newly added daemon of ANY name is
      caught, because novelty itself forces review.
  (b) SPEC DRIFT — ANY *enabled* entry whose `kind:name` IS reviewed but whose
      normalized `exec_start`/`cmd` differs from the reviewed string is
      flagged. This is probe B: swapping a reviewed entry's exec for a
      neutral-named resident router is a new daemon on the same name.
  (c) KEYWORDS — ANY entry (allowlisted or not, enabled or not) whose name or
      exec/cmd matches the message-routing predicate is flagged. The
      belt-and-braces third channel; it survives even a reviewed
      `(name, exec)` pair.

`ALLOWED_SURFACE` maps EVERY entry the real node currently declares, in both
tables, to the exact `exec_start`/`cmd` the live node carries (MEASURED, not
guessed) plus a one-line reason it is not a message daemon. Known periodic
jobs declare no exec string at all, so their reviewed exec is `None`.
`test_allowed_surface_matches_real_node` asserts set equality of the keys AND
equality of each reviewed exec against the live node, so an ADDITION (a new
daemon), a REMOVAL (a surface quietly losing a job), and a DRIFT (a live
entry's exec changing under a reviewed name) are all visible.

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

#: EVERY entry the real `.agi` crons node declares today, both tables, with
#: the reviewed exec string it carries and the reason it is not a
#: message-routing daemon. Measured, not guessed: raw frontmatter parse +
#: `crons.load_crons_node` agree (7 jobs, 2 services). `exec: None` means the
#: entry declares no exec/cmd at all — known jobs are rendered from
#: `cadences:` by `render_managed_lines`, so their reviewed spec has no exec
#: string. `test_allowed_surface_matches_real_node` asserts both that these
#: keys equal the live declared set AND that each reviewed exec equals the
#: live node's, so an entry added, removed, or changed under a reviewed name
#: fails loudly.
ALLOWED_SURFACE = {
    "job:grid_sync": {
        "exec": None,
        "why": "periodic 5-min grid commit/render tick; no exec string"},
    "job:branch_push": {
        "exec": None,
        "why": "hourly git push of the checked-out branch; no exec string"},
    "job:mail_poll": {
        "exec": None,
        "why": "periodic tick; one bounded inbox pass, exits"},
    "job:nudge_sweep": {
        "exec": None,
        "why": "periodic tick; one bounded nudge sweep, exits"},
    "job:publish_engine": {
        "exec": None,
        "why": "declared disabled; engine publish is vestigial (g11)"},
    "job:engine_push": {
        "exec": None,
        "why": "declared disabled; duplicates branch_push against one remote"},
    "job:prime_merge": {
        "exec": ("test -f {repo_root}/extensions/agi/bin/prime_merge.py && "
                 "PI_BIN=$HOME/.npm-global/bin/pi python3 "
                 "{repo_root}/extensions/agi/bin/prime_merge.py tick "
                 "--root {root}"),
        "why": "periodic 6-hourly town->season merge tick"},
    "service:agi-alarms-sanctuary-master": {
        "exec": ("/usr/bin/python3 {repo_root}/extensions/agi/bin/rotate.py "
                 "alarms --holder sanctuary-master --root {root}"),
        "why": "alarm rotator; rotates, routes nothing"},
    "service:agi-reaper": {
        "exec": ("/usr/bin/python3 {repo_root}/extensions/agi/bin/heal.py "
                 "watch --root {repo_root} --poll-s 30"),
        "why": "reap-only healer (`heal.py watch`); no message path"},
}

#: Jobs allowed to match the keyword predicate WITHOUT being flagged, each
#: because it is a bounded periodic tick rather than a resident process.
#: Deliberately narrow: exactly the two names whose names trip the predicate.
KEYWORD_EXEMPT_TICKS = {
    "job:mail_poll": "periodic cron tick; one bounded inbox pass, exits",
    "job:nudge_sweep": "periodic cron tick; one bounded nudge sweep, exits",
}


def _norm_exec(raw: object) -> str | None:
    """Normalize an exec/cmd string for comparison: whitespace-collapsed.

    `None`, a non-string, or a blank string all mean "no exec string
    declared" and compare as `None`. Collapsing internal whitespace keeps the
    comparison from firing on a cosmetic reflow while still catching any
    change to the command itself.
    """
    if not isinstance(raw, str) or not raw.strip():
        return None
    return " ".join(raw.split())


def _entry_exec(spec: dict) -> str | None:
    """The live entry's exec/cmd: a service's `exec_start` or a job's `cmd`."""
    return _norm_exec(spec.get("exec_start") if "exec_start" in spec
                      else spec.get("cmd"))


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

    Three channels, unioned, applied to BOTH `services:` (long-lived by
    construction) and `jobs:` (cadences) — a router parked in either table is
    a router. Returns a sorted, de-duplicated list; empty for a clean surface.
    """
    flagged: dict[str, str] = {}
    tables = (("service", node.get("services", {})),
              ("job", node.get("jobs", {})))
    for kind, table in tables:
        for name, spec in table.items():
            key = f"{kind}:{name}"
            reviewed = ALLOWED_SURFACE.get(key)
            if spec.get("enabled", True):
                # (a) NOVELTY: an enabled entry nobody has reviewed is a
                # daemon until a human says otherwise, whatever it is called.
                if reviewed is None:
                    flagged[key] = "unvetted enabled entry, not in ALLOWED_SURFACE"
                # (b) SPEC DRIFT: the name is reviewed but the exec/cmd is not
                # the reviewed one — a reviewed entry turned into a router.
                elif _entry_exec(spec) != reviewed["exec"]:
                    flagged[key] = (
                        "exec/cmd differs from reviewed spec "
                        f"({_entry_exec(spec)!r} != {reviewed['exec']!r})")
            # (c) KEYWORDS: belt-and-braces, allowlisted or not, enabled or not.
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
    """THE NOVELTY CONTROL: no seeded keyword, only a new name.

    `agi-outbound-hub` with a comment-less `python3 hubd.py serve` matches
    NO message keyword — the v1 keyword-only predicate returned `[]` for
    exactly this shape. The novelty channel must flag it because it is
    enabled and unvetted.
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


def test_reviewed_name_with_swapped_exec_is_flagged():
    """THE SPEC-DRIFT CONTROL (parent's probe B): a reviewed name, new exec.

    `agi-reaper` IS in `ALLOWED_SURFACE`, so the novelty channel is silent and
    the keyword channel matches nothing in `python3 hubd.py serve`. v2
    returned `[]` for exactly this node (measured). Reviewing the whole
    `(name, exec)` tuple is what closes it: the exec is not the reviewed one.
    """
    probe_b = {"services": {"agi-reaper": {
        "enabled": True, "exec_start": "python3 hubd.py serve"}}, "jobs": {}}
    flagged = find_message_daemons(probe_b)
    assert "service:agi-reaper" in flagged, (
        "a reviewed name whose exec was swapped for a neutral resident "
        f"router slipped through — the spec-drift guard is not load-bearing: "
        f"{flagged!r}")


def test_reviewed_name_with_unchanged_exec_is_not_flagged(tmp_path):
    """The drift channel is not trigger-happy: the reviewed exec passes."""
    root = tmp_path / "proj"
    root.mkdir()
    _write_node(
        root,
        services={"agi-reaper": {
            "enabled": True,
            "exec_start": ALLOWED_SURFACE["service:agi-reaper"]["exec"]}},
        cadences={"grid_sync": {"every_mins": 5, "enabled": True}},
    )
    node = crons.load_crons_node(root)
    assert find_message_daemons(node) == []


def test_disabled_unvetted_entry_is_keyword_checked_not_novelty_flagged(tmp_path):
    """Novelty/drift are for ENABLED entries; keywords still catch a router.

    A disabled entry is inert, so novelty and drift need not fire — but the
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
    """ALLOWED_SURFACE names EXACTLY the live surface, spec included.

    Keys: an addition (a new daemon, or an over-eager allowlist entry) and a
    removal (a live job/service disappearing from the node) both fail.
    Exec: each reviewed `exec_start`/`cmd` must be the string the live node
    carries, which is what makes the spec-drift channel load-bearing.
    """
    node = crons.load_crons_node(_graph_root())
    assert node["jobs"], "real crons node declared no jobs — wrong root?"
    assert node["services"], "real crons node declared no services — wrong root?"
    assert declared_surface(node) == set(ALLOWED_SURFACE)
    for key, reviewed in ALLOWED_SURFACE.items():
        kind, name = key.split(":", 1)
        table = node["services"] if kind == "service" else node["jobs"]
        assert _entry_exec(table[name]) == reviewed["exec"], (
            f"{key}: reviewed exec is not the live node's spec — "
            f"{reviewed['exec']!r} != {_entry_exec(table[name])!r}")


def test_real_heal_cron_surface_has_no_message_daemon():
    """The live `.agi` crons node carries no message-routing daemon."""
    node = crons.load_crons_node(_graph_root())
    # The predicate read a real, non-empty surface (guards against a wrong
    # path yielding an empty dict and passing by accident).
    assert node["jobs"], "real crons node declared no jobs — wrong root?"
    assert node["services"], "real crons node declared no services — wrong root?"
    assert find_message_daemons(node) == []
