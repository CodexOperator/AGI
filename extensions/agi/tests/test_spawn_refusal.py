"""Falsifiers for goal:g7.31.3.3.4 (refusal stamps named row + one reply).

1. Induced refusal: row updated by name + exactly one reply delivered.
2. Negative: zero multi-reply storms for a single failed request.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import spawn_refusal  # noqa: E402


@pytest.fixture
def root(tmp_path):
    r = tmp_path / "proj"
    (r / ".agi" / "sessions").mkdir(parents=True)
    return r


def test_refuse_stamps_named_row_and_sends_one_reply(root):
    delivered = []

    def reply_fn(to, body):
        delivered.append((to, body))

    stamp = spawn_refusal.refuse(
        root,
        row_name="parent-0",
        request_id="req-abc",
        reason="slot full",
        to_post="director-helper",
        body="refused: slot full",
        reply_fn=reply_fn,
    )
    assert stamp["row"] == "parent-0"
    assert stamp["request_id"] == "req-abc"
    assert stamp["status"] == "refused"
    assert stamp["reply_sent"] is True
    assert delivered == [("director-helper", "refused: slot full")]
    # stamp persisted under the row name
    data = spawn_refusal._read_json(spawn_refusal.stamps_path(root), {"rows": {}})
    assert "parent-0" in data["rows"]
    assert data["rows"]["parent-0"]["reason"] == "slot full"


def test_second_reply_same_request_id_is_capped(root):
    delivered = []

    def reply_fn(to, body):
        delivered.append((to, body))

    spawn_refusal.refuse(
        root, "parent-0", "req-1", "full", "director-helper", "once", reply_fn
    )
    stamp2 = spawn_refusal.refuse(
        root, "parent-0", "req-1", "full-again", "director-helper", "twice", reply_fn
    )
    assert stamp2["reply_sent"] is False
    assert delivered == [("director-helper", "once")]
    assert spawn_refusal.reply_already_sent(root, "req-1") is True


def test_distinct_request_ids_each_get_one_reply(root):
    delivered = []

    def reply_fn(to, body):
        delivered.append(body)

    spawn_refusal.refuse(root, "parent-0", "r1", "a", "dh", "body-1", reply_fn)
    spawn_refusal.refuse(root, "parent-0", "r2", "b", "dh", "body-2", reply_fn)
    assert delivered == ["body-1", "body-2"]


def test_send_one_reply_alone_caps(root):
    n = []

    def reply_fn(to, body):
        n.append(1)

    assert spawn_refusal.send_one_reply(root, "x", "dh", "hi", reply_fn) is True
    assert spawn_refusal.send_one_reply(root, "x", "dh", "hi", reply_fn) is False
    assert spawn_refusal.send_one_reply(root, "x", "dh", "hi", reply_fn) is False
    assert len(n) == 1
