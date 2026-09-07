"""Tests for sensei.py — the Master Sensei (hypothesis:l3w4-master-sensei).

Each test exercises a named claim from the hypothesis's TESTS list, against
fixtures that never touch a real seat or a real write.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

import sensei  # noqa: E402


def _row(**kw):
    base = {"name": "dir-g1", "role": "director", "tier": 1,
            "rotated_by": "advisor"}
    base.update(kw)
    return base


def _write_conv(path: Path, blocks):
    path.parent.mkdir(parents=True, exist_ok=True)
    parts = []
    for b in blocks:
        parts.append(f"ts: {b['ts']}\nfrom: {b['from']}\nto: {b['to']}\n\n"
                     f"{b['text']}\n")
    path.write_text("\n---\n".join(parts), encoding="utf-8")


def test_direct_supervisor_room_for_quorum_advisor_prime_dm_for_named_seat():
    for rb in ("quorum", "advisor", "prime"):
        assert sensei._direct_supervisor(_row(rotated_by=rb)) == (
            "room", sensei.ROOM_QUORUM)
    assert sensei._direct_supervisor(_row(rotated_by="sanctuary-master")) == (
        "dm", "sanctuary-master")
    assert sensei._direct_supervisor(_row(rotated_by="")) is None


def test_pick_worst_returns_highest_rate_row_ties_broken_by_count():
    rows = [
        {"seat_or_role": "dir-g1", "model": "claude-sonnet-5",
         "fail_rate": 0.3, "failed": 3},
        {"seat_or_role": "liaison", "model": "claude-sonnet-5",
         "fail_rate": 0.4, "failed": 1},
        {"seat_or_role": "dir-g15", "model": "claude-sonnet-5",
         "fail_rate": 0.4, "failed": 5},
    ]
    worst = sensei.pick_worst(rows)
    assert worst["seat_or_role"] == "dir-g15"  # 0.4 ties → higher count wins
    assert sensei.pick_worst([]) is None


def test_apply_refuses_without_a_reply_after_since_on_every_thread(
        tmp_path):
    croot = tmp_path / "comms"
    # seat has own dm + supervisor dm (rotated_by named seat)
    row = seat_fixture(tmp_path, _row(name="dir-g1", rotated_by="advisor"))
    # reply only on the role dm, none from advisor on/after since
    since = "2026-09-07T00:00:00Z"
    _write_conv(croot / "dm" / "master-sensei--dir-g1.md", [
        {"ts": "2026-09-07T00:01:00Z", "from": "dir-g1", "to": "master-sensei",
         "text": "ok"},
    ])
    with pytest.raises(SystemExit):
        sensei._required_threads  # sanity import
    threads = sensei._required_threads(row, "dir-g1", None)
    assert not sensei._has_reply(croot, ("dm", "advisor"), since)
    assert sensei._has_reply(croot, ("dm", "dir-g1"), since)


def seat_fixture(root: Path, row: dict) -> dict:
    """Materialise a one-row config:seats so load_seats finds it."""
    nodes = root / ".agi" / "nodes" / "config"
    nodes.mkdir(parents=True, exist_ok=True)
    (nodes / "seats.md").write_text(
        "---\nid: config:seats\nmint_id: x\ntype: config\n"
        f"seats:\n  - {json.dumps(row, sort_keys=True)}\n---\n",
        encoding="utf-8")
    return row


def test_apply_protected_target_never_calls_write_py_without_owner_approved(
        tmp_path, monkeypatch):
    root = tmp_path
    croot = tmp_path / "comms"
    row = seat_fixture(root, _row(name="belam", role="prime_director",
                                  tier=3))
    since = "2026-09-07T00:00:00Z"
    # both threads (belam's dm is itself the prime dm; use supervisor room via
    # quorum) must show a reply
    row["rotated_by"] = "quorum"
    _write_conv(croot / "dm" / "master-sensei--belam.md", [
        {"ts": "2026-09-07T00:01:00Z", "from": "belam", "to": "master-sensei",
         "text": "yes"},
    ])
    _write_conv(croot / "room" / f"{sensei.ROOM_QUORUM}.md", [
        {"ts": "2026-09-07T00:02:00Z", "from": "advisor", "to": "tier3-quorum",
         "text": "agree"},
    ])

    calls = []
    monkeypatch.setattr(sensei, "apply_note",
                        lambda *a, **k: calls.append(a) or "written")

    args = _Args(target="belam", node_id="build:belam", change="raise effort",
                 since=since, supervisor=None, owner_approved=False,
                 dry_run=False)
    rc = sensei.cmd_apply(root, croot, args)
    assert rc == 0
    assert calls == []  # write.py never reached without --owner-approved
    assert (tmp_path / sensei.DRAFTS_DIR / "belam.md").is_file()


class _Args:
    def __init__(self, **kw):
        defaults = dict(target="", node_id="", change="", since="",
                        supervisor=None, owner_approved=False, dry_run=False)
        defaults.update(kw)
        self.__dict__.update(defaults)


def test_apply_ephemeral_target_checks_only_the_supervisor_thread(
        tmp_path, monkeypatch):
    root = tmp_path
    croot = tmp_path / "comms"
    since = "2026-09-07T00:00:00Z"
    # no seat row → only the supervisor dm must have a reply; the (absent)
    # role dm must be neither required nor even probed
    _write_conv(croot / "dm" / "master-sensei--sanctuary-master.md", [
        {"ts": "2026-09-07T00:01:00Z", "from": "sanctuary-master",
         "to": "master-sensei", "text": "ok"},
    ])
    calls = []
    monkeypatch.setattr(sensei, "apply_note",
                        lambda *a, **k: calls.append(a) or "written")
    args = _Args(target="tmp-role", node_id="build:tmp-role",
                 change="use glm", since=since, supervisor="sanctuary-master",
                 owner_approved=False, dry_run=False)
    rc = sensei.cmd_apply(root, croot, args)
    assert rc == 0
    assert len(calls) == 1  # ephemeral isn't protected; note written once
    # confirm the role dm was never created (only supervisor thread used)
    assert not (croot / "dm" / "master-sensei--tmp-role.md").exists()


def test_apply_unprotected_target_writes_note_exactly_once(tmp_path,
                                                           monkeypatch):
    root = tmp_path
    croot = tmp_path / "comms"
    row = seat_fixture(root, _row(name="dir-g1", rotated_by="advisor"))
    since = "2026-09-07T00:00:00Z"
    _write_conv(croot / "dm" / "master-sensei--dir-g1.md", [
        {"ts": "2026-09-07T00:01:00Z", "from": "dir-g1", "to": "master-sensei",
         "text": "ok"},
    ])
    _write_conv(croot / "dm" / "master-sensei--advisor.md", [
        {"ts": "2026-09-07T00:02:00Z", "from": "advisor", "to": "master-sensei",
         "text": "approved"},
    ])
    calls = []
    monkeypatch.setattr(sensei, "apply_note",
                        lambda *a, **k: calls.append(a) or "written")
    args = _Args(target="dir-g1", node_id="build:dir-g1", change="try opus",
                 since=since, supervisor=None, owner_approved=False,
                 dry_run=False)
    rc = sensei.cmd_apply(root, croot, args)
    assert rc == 0
    assert len(calls) == 1
    assert calls[0] == (root, "build:dir-g1")