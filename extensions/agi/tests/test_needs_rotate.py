"""Falsifiers for goal:g7.31.3.3.3 (AGI_BOX host-only needs-rotate clear).

1. Cross-box probe: non-matching AGI_BOX does not mutate the row; matching
   box clears needs-rotate after act.
2. Negative: no silent clear of needs-rotate without an action record.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import needs_rotate  # noqa: E402


def _graph(tmp_path: Path, *, env_box: str = "encryption-town") -> Path:
    root = tmp_path / "proj"
    (root / ".agi" / "sessions").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text("{}\n", encoding="utf-8")
    (tmp_path / ".env").write_text(f"AGI_BOX={env_box}\n", encoding="utf-8")
    # boxes.this_box resolves envfile from root; put .env beside .agi parent
    (root / ".env").write_text(f"AGI_BOX={env_box}\n", encoding="utf-8")
    return root


@pytest.fixture(autouse=True)
def _no_inherited_box(monkeypatch):
    monkeypatch.delenv("AGI_BOX", raising=False)


def test_may_act_true_only_when_agi_box_matches(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "encryption-town")
    root = _graph(tmp_path, env_box="encryption-town")
    local = {"name": "director-helper", "box": "encryption-town", "needs-rotate": True}
    foreign = {"name": "director-helper", "box": "local-town", "needs-rotate": True}
    assert needs_rotate.may_act(root, local) is True
    assert needs_rotate.may_act(root, foreign) is False


def test_cross_box_act_and_clear_does_not_mutate(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "encryption-town")
    root = _graph(tmp_path, env_box="encryption-town")
    row = {"name": "director-helper", "box": "local-town", "needs-rotate": True}
    before = copy.deepcopy(row)
    out = needs_rotate.act_and_clear(root, row, kind="rotate")
    assert out is row  # same object, unchanged
    assert out == before
    assert out.get("needs-rotate") is True
    # no action log written for refused cross-box
    assert not needs_rotate.actions_path(root).is_file()


def test_matching_box_clears_needs_rotate_after_act(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "encryption-town")
    root = _graph(tmp_path, env_box="encryption-town")
    row = {"name": "director-helper", "box": "encryption-town", "needs-rotate": True}
    seen = []

    def _act(r):
        seen.append(r["name"])

    out = needs_rotate.act_and_clear(root, row, kind="rotate", act_fn=_act)
    assert seen == ["director-helper"]
    assert out.get("needs-rotate") is False
    assert out.get("needs_rotate_cleared_by")
    assert needs_rotate.action_recorded(root, out["needs_rotate_cleared_by"])


def test_silent_clear_without_action_record_refuses(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "encryption-town")
    root = _graph(tmp_path, env_box="encryption-town")
    row = {"name": "director-helper", "box": "encryption-town", "needs-rotate": True}
    with pytest.raises(PermissionError, match="silent clear refused"):
        needs_rotate.clear_needs_rotate(root, row, action_id="no-such-action")
    assert row.get("needs-rotate") is True


def test_cross_box_clear_refuses_even_with_action(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "encryption-town")
    root = _graph(tmp_path, env_box="encryption-town")
    # record an action under a local post name, then try clear on foreign row
    aid = needs_rotate.record_action(root, "director-helper", "rotate")
    foreign = {"name": "director-helper", "box": "local-town", "needs-rotate": True}
    with pytest.raises(PermissionError, match="cross-box clear refused"):
        needs_rotate.clear_needs_rotate(root, foreign, aid)
