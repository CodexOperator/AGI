"""goal:g7.31.4.2 -- the caller-facing send/nudge surface is the SAME for a
local peer and a foreign-box (mesh) peer: same names/args, same result shape,
transport chosen engine-internally, zero `is_ssh` in the caller bodies.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import send  # noqa: E402


def _graph(tmp: Path, rows: list[dict]) -> Path:
    """A minimal graph root (the `.agi` dir) exactly as test_box_guard builds."""
    root = tmp / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / "config.json").write_text("{}\n")
    body = "---\nid: config:posts\ntype: config\ndefault_box: core-town\nposts:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    (root / "nodes" / ".geometry" / "posts.md").write_text(body + "---\n")
    return root


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    monkeypatch.delenv("AGI_BOX", raising=False)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.setenv("AGI_SEAT", "sender")


LOCAL = {"name": "local-seat", "pid": 111, "window": "@111"}
FOREIGN = {"name": "far-seat", "pid": 222, "window": "@222",
           "box": "local-town"}


# conjunct 1+2: SAME call, SAME result shape, BOTH land -- transport invisible.
def test_same_send_dm_call_and_result_shape_both_transports(
        tmp_path, monkeypatch):
    root = _graph(tmp_path, [LOCAL, FOREIGN])
    monkeypatch.setattr(send, "_locally_loaded_rows", lambda r: [LOCAL, FOREIGN])
    nudged: list[str] = []
    monkeypatch.setattr(send, "_nudge_window",
                        lambda *a, **k: nudged.append(a[1]) or False)

    p_local = send.send_dm(root, "sender", "local-seat", "hi local", "sender")
    p_far = send.send_dm(root, "sender", "far-seat", "hi far", "sender")

    assert isinstance(p_local, Path) and isinstance(p_far, Path)
    assert p_local.parent == p_far.parent                 # one dm surface
    for p, text in ((p_local, "hi local"), (p_far, "hi far")):
        assert p.exists()
        blocks = send._conv_blocks(p)
        assert len(blocks) == 1
        assert blocks[0]["text"] == text
        assert {"ts", "from", "to"} <= set(blocks[0])      # same block shape
    # One nudge seam, reached by both; the caller named no transport.
    assert nudged == ["local-seat", "far-seat"]


# conjunct 3: the transport decision is engine-internal, not caller-chosen.
def test_transport_decision_is_engine_internal(tmp_path, monkeypatch):
    root = _graph(tmp_path, [LOCAL, FOREIGN])
    monkeypatch.setattr(send, "_locally_loaded_rows", lambda r: [LOCAL, FOREIGN])
    monkeypatch.setattr(send, "_window_id_listed", lambda *a, **k: True)

    assert send._nudge_target(root, "local-seat", None) is not None
    assert send._nudge_target(root, "far-seat", None) is None


# conjunct 4: no `is_ssh` in the caller-facing send/nudge bodies (source bytes).
def test_no_is_ssh_in_caller_facing_send_bodies():
    src = (BIN / "send.py").read_text(encoding="utf-8")
    want = {"send_dm", "send_room", "_nudge_target", "_nudge_window",
            "_announce_nudge"}
    found = [n for n in ast.walk(ast.parse(src))
             if isinstance(n, ast.FunctionDef) and n.name in want]
    assert {f.name for f in found} == want
    for fn in found:
        assert "is_ssh" not in (ast.get_source_segment(src, fn) or ""), fn.name