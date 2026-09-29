"""Falsifiers for goal:g7.31.3.3.5 (write gate: parents own kid rows; kids none).

1. Probe: parent write to own kid row succeeds; kid write and foreign-kid
   write refuse by name.
2. Negative: no unscoped write path that mutates arbitrary geometry rows.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import kid_write_gate as gate  # noqa: E402


def test_is_kid_row_key():
    assert gate.is_kid_row_key("kid")
    assert gate.is_kid_row_key("kid0")
    assert gate.is_kid_row_key("kid-1")
    assert gate.is_kid_row_key("kid_a")
    assert not gate.is_kid_row_key("parent-0")
    assert not gate.is_kid_row_key("needs-rotate")
    assert not gate.is_kid_row_key("")


def test_parent_write_own_kid_succeeds():
    store: dict = {}
    writer = {"role": "parent", "post": "director-helper"}
    gate.apply_write(store, writer, "kid0", {"occupant": "a00"}, parent_post="director-helper")
    assert store["kid0"]["occupant"] == "a00"
    ok, reason = gate.may_write(writer, "kid1", parent_post="director-helper")
    assert ok and reason == ""


def test_kid_write_refuses_by_name():
    writer = {"role": "kid", "post": "a00-kid"}
    ok, reason = gate.may_write(writer, "kid0", parent_post="director-helper")
    assert not ok
    assert "kids write none" in reason
    with pytest.raises(PermissionError, match="kids write none"):
        gate.apply_write({}, writer, "kid0", {"x": 1}, parent_post="director-helper")


def test_foreign_kid_write_refuses_by_name():
    writer = {"role": "parent", "post": "director-helper"}
    ok, reason = gate.may_write(writer, "kid0", parent_post="director-engine")
    assert not ok
    assert "foreign-kid" in reason
    with pytest.raises(PermissionError, match="foreign-kid"):
        gate.apply_write({}, writer, "kid0", {"x": 1}, parent_post="director-engine")


def test_parent_unscoped_non_kid_write_refuses():
    """Negative: no unscoped write path for arbitrary geometry rows."""
    writer = {"role": "parent", "post": "director-helper"}
    store = {"parent-0": {"id": "parent-0"}}
    ok, reason = gate.may_write(writer, "parent-0", parent_post="director-helper")
    assert not ok
    assert "only own kid*" in reason
    with pytest.raises(PermissionError, match="only own kid"):
        gate.apply_write(store, writer, "parent-0", {"hacked": True}, parent_post="director-helper")
    assert store["parent-0"] == {"id": "parent-0"}  # unchanged


def test_director_not_gated_by_this_leaf():
    writer = {"role": "director", "name": "director-engine"}
    ok, reason = gate.may_write(writer, "parent-0")
    assert ok and reason == ""
