"""Red-first tests for hierarchy.py (hypothesis:l3w4-hierarchy-one-source).

Every --check class gets a fixture reproducing the real measured shape from
2026-09-08, asserted NONZERO before the checker is considered done, and a
clean seed asserted ZERO. The fixtures are written under a tmp graph root and
pointed at with --root, so the tests never touch the live tree.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin" / "hierarchy.py"

SEATS_FM = "".join(f'  - {json.dumps(r, sort_keys=True)}\n' for r in [
    {"name": "belam", "role": "prime_director", "tier": 3, "harness": "claude-code",
     "model": "claude-fable-5-1", "effort": "max", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/belam.meter", "rotated_by": "quorum", "owning_goal": ""},
    {"name": "self-perpetuating", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-sonnet-5", "effort": "max", "session_kind": "tty",
     "pin_ref": ".agi/sessions/self-perpetuating.meter", "rotated_by": "sanctuary-master",
     "owning_goal": ""},
    {"name": "sanctuary-director", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-sonnet-5", "effort": "max", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/sanctuary-director.meter", "rotated_by": "sanctuary-master",
     "owning_goal": "goal:g17"},
    {"name": "sensei-director", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-sonnet-5", "effort": "max", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/sensei-director.meter", "rotated_by": "master-sensei",
     "owning_goal": "goal:g16"},
    {"name": "sanctuary-master", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-opus-5", "effort": "high", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/sanctuary-master.meter", "rotated_by": "quorum",
     "owning_goal": ""},
    {"name": "master-sensei", "role": "director", "tier": 1, "harness": "claude-code",
     "model": "claude-sonnet-5", "effort": "max", "session_kind": "remote-control",
     "pin_ref": ".agi/sessions/master-sensei.meter", "rotated_by": "sanctuary-master",
     "owning_goal": ""},
])

LADDER_ROLES = [
    {"tier": 3, "role": "prime_director", "harness": "claude-code", "model": "claude-fable-5-1", "effort": "max", "settings": "ultracode"},
    {"tier": 3, "role": "parent", "harness": "claude-code", "model": "claude-opus-5", "effort": "max", "settings": "ultracode"},
    {"tier": 1, "role": "director", "harness": "claude-code", "model": "claude-fable-5-1", "effort": "max", "settings": ""},
    {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""},
]

LADDER_FM = (
    "caps:\n"
    "  director_kids: 2\n"
    "roles:\n"
    + "".join(f'  - {json.dumps(r, sort_keys=True)}\n' for r in LADDER_ROLES)
)


def _write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _clean_seed(root: Path):
    _write(root, "nodes/.geometry/seats.md", "---\nid: config:seats\nseats:\n"
            + SEATS_FM + "---\n")
    _write(root, "nodes/.geometry/ladder.md", "---\nid: ladder:ladder\n"
            + LADDER_FM + "---\n")


def _maybe_mkdir_config(root: Path):
    """hierarchy falls back to --root directly, no config.json needed."""
    (root / "sessions").mkdir(parents=True, exist_ok=True)


def _check(root: Path) -> tuple[int, str]:
    out = subprocess.run(
        [sys.executable, str(BIN), "--check", "--root", str(root)],
        capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr


def _pin(root: Path, name: str, transcript: str):
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    (root / "sessions" / f"{name}.meter").write_text(transcript, encoding="utf-8")
    return (root / "sessions" / f"{name}.meter")


# --------------------------------------------------------------------------- #
# Class 1 — orphan pin with no seat row
# --------------------------------------------------------------------------- #
def test_orphan_pin_nonzero(tmp_path):
    _clean_seed(tmp_path)
    _maybe_mkdir_config(tmp_path)
    _pin(tmp_path, "dir-g1", "0\t/nowhere/q.jsonl")
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "dir-g1.meter has no seat row" in out


def test_orphan_pin_ignores_agent_ids(tmp_path):
    _clean_seed(tmp_path)
    _maybe_mkdir_config(tmp_path)
    _pin(tmp_path, "a00-12345678", "0\t/nowhere/q.jsonl")
    rc, _ = _check(tmp_path)
    assert rc == 0


# --------------------------------------------------------------------------- #
# Class 2 — two rows pin to the same transcript
# --------------------------------------------------------------------------- #
def test_duplicate_transcript_nonzero(tmp_path):
    _clean_seed(tmp_path)
    tx = tmp_path / "shared.jsonl"
    tx.write_text("", encoding="utf-8")
    _pin(tmp_path, "self-perpetuating", f"0\t{tx}")
    _pin(tmp_path, "sensei-director", f"0\t{tx}")
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "duplicate_transcript" in out


# --------------------------------------------------------------------------- #
# Class 3 — rotated_by naming a seat that has no row
# --------------------------------------------------------------------------- #
def test_rotated_by_nonzero(tmp_path):
    _clean_seed(tmp_path)
    seed = (tmp_path / "nodes" / ".geometry" / "seats.md").read_text()
    seed = seed.replace('"rotated_by": "quorum"',
                        '"rotated_by": "advisor"')
    _write(tmp_path, "nodes/.geometry/seats.md", seed)
    _maybe_mkdir_config(tmp_path)
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "rotated_by" in out and "advisor" in out


def test_rotated_by_roleclass_allowed(tmp_path):
    _clean_seed(tmp_path)
    _maybe_mkdir_config(tmp_path)
    rc, _ = _check(tmp_path)
    assert rc == 0  # quorum / prime are valid roleclass rotators


# --------------------------------------------------------------------------- #
# Class 4 — director-kids above caps.director_kids
# --------------------------------------------------------------------------- #
def test_director_kids_over_cap_nonzero(tmp_path):
    _clean_seed(tmp_path)  # 2 director-kids == cap 2 -> clean
    _maybe_mkdir_config(tmp_path)
    rc, _ = _check(tmp_path)
    assert rc == 0
    # add a third tier-1 director owning a goal
    seed = (tmp_path / "nodes" / ".geometry" / "seats.md").read_text()
    extra = json.dumps({"name": "dir-x", "role": "director", "tier": 1,
                        "model": "claude-sonnet-5", "effort": "max",
                        "session_kind": "tty", "rotated_by": "sanctuary-master",
                        "owning_goal": "goal:g99"})
    close = seed.rfind("---\n")
    seed = seed[:close] + f"  - {extra}\n" + "---\n"
    _write(tmp_path, "nodes/.geometry/seats.md", seed)
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "director_kids" in out


# --------------------------------------------------------------------------- #
# Class 5 — (tier, role) with no ladder row and no seat model
# --------------------------------------------------------------------------- #
def test_unresolved_nonzero(tmp_path):
    _clean_seed(tmp_path)
    extra = json.dumps({"name": "mystery", "role": "wizard", "tier": 2,
                        "harness": "claude-code", "model": "", "effort": "",
                        "session_kind": "tty", "rotated_by": "quorum",
                        "owning_goal": ""})
    seed = (tmp_path / "nodes" / ".geometry" / "seats.md").read_text()
    close = seed.rfind("---\n")
    seed = seed[:close] + f"  - {extra}\n" + "---\n"
    _write(tmp_path, "nodes/.geometry/seats.md", seed)
    _maybe_mkdir_config(tmp_path)
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "unresolved" in out and "wizard" in out


# --------------------------------------------------------------------------- #
# Class 6 — body table disagrees with its own frontmatter
# --------------------------------------------------------------------------- #
def test_body_table_nonzero(tmp_path):
    _clean_seed(tmp_path)
    bad = (
        "---\nid: ladder:ladder\n" + LADDER_FM + "---\n"
        "# body\n"
        "| tier | role | harness | model | effort | settings |\n"
        "|---|---|---|---|---|---|\n"
        "| 1 | director | claude-code | claude-sonnet-5 | max |  |\n"
    )  # frontmatter says tier-1 director is fable-5-1; body says sonnet-5
    _write(tmp_path, "nodes/.geometry/ladder.md", bad)
    _maybe_mkdir_config(tmp_path)
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "body_table" in out


def test_clean_seed_zero(tmp_path):
    _clean_seed(tmp_path)
    _maybe_mkdir_config(tmp_path)
    rc, out = _check(tmp_path)
    assert rc == 0, out


# --------------------------------------------------------------------------- #
# Class 7 — the role card grammar (hypothesis:l4-card-grammar-and-the-
# written-by-join). Cards are `seat` nodes under nodes/seat/; the ladder is the
# declared matrix (at most 2 tracks, at most 2 tells, exactly 1 decides). A card
# that declares MORE than the matrix REFUSES (exit nonzero); FEWER WARNS and
# exits 0. Every violation NAMES the field and the row.
# --------------------------------------------------------------------------- #
def _card(root, name, **fm):
    fm.setdefault("type", "seat")
    fm.setdefault("role", "keeper")
    fm.setdefault("what", "watch that the system does not drift")
    rows = "".join(
        f'{k}: {v!r}\n' if not isinstance(v, (list, tuple, dict))
        else f'{k}: ' + json.dumps(v) + "\n"
        for k, v in fm.items())
    _write(root, f"nodes/seat/{name}.md", f"---\nid: 'seat:{name}'\n{rows}---\n")
    return name


def _schema(root, ntype, **fm):
    rows = "".join(
        f'{k}: {v!r}\n' if not isinstance(v, list)
        else f'{k}: ' + json.dumps(v) + "\n"
        for k, v in fm.items())
    _write(root, f"context/schemas/[{ntype}].md", f"---\n{rows}---\n")


def _clean_full(root):
    """clean seed + a good card + a resolvable .where target."""
    _clean_seed(root)
    _maybe_mkdir_config(root)
    (root / "nodes" / "goal").mkdir(parents=True, exist_ok=True)
    (root / "nodes" / "goal" / "g17.md").write_text("# goal:g17\n", encoding="utf-8")


def test_card_what_too_long_refuses(tmp_path):
    _clean_full(tmp_path)
    _card(tmp_path, "c1", **{**{"role": "director", "where": "nodes/goal/g17.md",
                            "cost": "read", "to": "sanctuary-master",
                            "trigger": "on an event", "channel": "dm"},
                             "what": "x" * 81})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "what" in out and "c1" in out


def test_card_where_unresolved_refuses(tmp_path):
    _clean_full(tmp_path)
    _card(tmp_path, "c1", **{**{"role": "director", "what": "ok", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm"},
                             "where": "nodes/goal/does-not-exist.md"})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "where" in out and "c1" in out


# (b) wake in .cost and brief in .channel each refuse, reason stated

def test_card_wake_cost_refuses(tmp_path):
    _clean_full(tmp_path)
    _card(tmp_path, "c1", **{**{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "to": "sanctuary-master",
                            "trigger": "on an event", "channel": "dm"},
                             "cost": "wake"})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "cost" in out and "wake" in out and "c1" in out


def test_card_brief_channel_refuses(tmp_path):
    _clean_full(tmp_path)
    _card(tmp_path, "c1", **{**{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event"},
                             "channel": "brief"})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "channel" in out and "brief" in out and "c1" in out


def test_card_to_unknown_target_fail_closed(tmp_path):
    _clean_full(tmp_path)
    _card(tmp_path, "c1", **{**{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "trigger": "on an event", "channel": "dm"},
                             "to": "no-such-role"})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "to" in out and "no-such-role" in out and "c1" in out


# (c) cadence lint

def test_card_trigger_cadence_refuses_event_passes(tmp_path):
    _clean_full(tmp_path)
    # an event-shaped trigger passes (no bad card in the tree yet)
    _card(tmp_path, "c2", **{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "channel": "dm",
                            "trigger": "on a season's brief"})
    rc2, _ = _check(tmp_path)
    assert rc2 == 0
    # a cadence-looking trigger refuses on the lint
    _card(tmp_path, "c1", **{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "channel": "dm",
                            "trigger": "every hour"})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "trigger" in out and "c1" in out


def test_card_options_lowercase_and_count(tmp_path):
    _clean_full(tmp_path)
    _card(tmp_path, "c1", **{**{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm"},
                             "options": ["Accept", "propose"]})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "options" in out and "c1" in out


def test_card_decides_must_be_exactly_one(tmp_path):
    _clean_full(tmp_path)
    # MORE than one decision (a list) refuses — decides is EXACTLY ONE
    _card(tmp_path, "c1", **{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm", "decides": ["keep", "rearrange"]})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "decides" in out and "c1" in out


# (d) the ASYMMETRY — MORE refuses, FEWER warns and exits 0

def test_card_more_than_matrix_refuses(tmp_path):
    _clean_full(tmp_path)
    _card(tmp_path, "c1", **{**{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm", "tells": ["a", "b", "c"]},
                             "tracks": ["1", "2", "3"]})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "tracks" in out and "tells" in out and "c1" in out


def test_card_fewer_than_matrix_warns_exits_zero(tmp_path):
    _clean_full(tmp_path)
    _card(tmp_path, "c1", **{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm", "tracks": ["only one"],
                            "tells": ["one"]})
    rc, out = _check(tmp_path)
    assert rc == 0, out
    assert "warning" in out and "c1" in out


# --------------------------------------------------------------------------- #
# Class 8 — the decides.writes join (written_by via the shared parser)
# --------------------------------------------------------------------------- #
def test_written_by_join_role_not_admitted_refuses(tmp_path):
    _clean_full(tmp_path)
    _schema(tmp_path, "doc", written_by="prime_director")  # admits only prime
    _card(tmp_path, "c1", **{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm", "writes": "doc"})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "written_by_join" in out and "c1" in out and "doc" in out


def test_written_by_join_role_admitted_passes(tmp_path):
    _clean_full(tmp_path)
    _schema(tmp_path, "doc", written_by="director")
    _card(tmp_path, "c1", **{"role": "director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm", "writes": "doc"})
    rc, out = _check(tmp_path)
    assert rc == 0, out


def test_written_by_join_list_valued_read_correctly(tmp_path):
    _clean_full(tmp_path)
    # a LIST-valued written_by — [owner, prime_director] — the shared parser
    # must admit both members, not read it as one token.
    _schema(tmp_path, "config", written_by=["owner", "prime_director"])
    _card(tmp_path, "c2", **{"role": "prime_director", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm", "writes": "config"})
    rc0, _ = _check(tmp_path)
    assert rc0 == 0  # prime_director is admitted, so the join passes
    _card(tmp_path, "c1", **{"role": "keeper", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm", "writes": "config"})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "written_by_join" in out and "keeper" in out


def test_written_by_join_seat_predicate_fails(tmp_path):
    _clean_full(tmp_path)
    _schema(tmp_path, "vision", written_by="director",
            seat_predicate="role == 'director' and tier == 2")
    _card(tmp_path, "c1", **{"role": "director", "tier": 1, "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm", "writes": "vision"})
    rc, out = _check(tmp_path)
    assert rc != 0
    assert "written_by_join" in out and "seat_predicate" in out and "c1" in out


def test_writes_none_gates_nothing(tmp_path):
    _clean_full(tmp_path)
    _schema(tmp_path, "config", written_by="owner")
    _card(tmp_path, "c1", **{"role": "keeper", "what": "ok",
                            "where": "nodes/goal/g17.md", "cost": "read",
                            "to": "sanctuary-master", "trigger": "on an event",
                            "channel": "dm", "writes": "none"})
    rc, out = _check(tmp_path)
    assert rc == 0, out

def _render(root: Path) -> str:
    out = subprocess.run(
        [sys.executable, str(BIN), "render", "--root", str(root)],
        capture_output=True, text=True)
    return out.stdout


def test_render_town_council_chain(tmp_path):
    """hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council — render
    draws the reporting chain from the ladder's `towns:` list and the
    council-role rows in config:seats. With no Core Council seat the Prime
    plays it; a seated non-core council reports to Core Council; a declared
    but unseated town renders as `? (unseated)`, never an invented row."""
    seats = SEATS_FM + ('  - {"name": "council-a", "role": "council", "tier": 2, '
                        '"town": "townA", "harness": "claude-code", '
                        '"model": "claude-sonnet-5", "effort": "max", '
                        '"session_kind": "tty", "pin_ref": "", "rotated_by": '
                        '"prime", "owning_goal": ""}\n')
    _write(tmp_path, "nodes/.geometry/seats.md",
           "---\nid: config:seats\nseats:\n" + seats + "---\n")
    _write(tmp_path, "nodes/.geometry/ladder.md",
           "---\nid: ladder:ladder\n" + LADDER_FM
           + "towns:\n  - core\n  - townA\n  - townB\n---\n")
    out = _render(tmp_path)
    assert "| core | Prime (as Core Council) | Prime |" in out
    assert "| townA | council-a | Core Council |" in out
    assert "| townB | ? (unseated) | Core Council |" in out
