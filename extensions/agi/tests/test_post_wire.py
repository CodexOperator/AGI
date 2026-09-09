"""Tests for post_wire.py — wiring agent results into the node graph.

Focused on the pieces this file adds and owns, isolated so a test does not
have to run the whole `cmd_wire` pass (which pulls graph_core, completion,
spawn_gate and a real node tree). The done_line contract (hypothesis:
l2-done-doubled-frontmatter) lives here: post_wire stamps
`done_line: present|missing` on every manifest agent entry from the kid's
output.log, so a parent can tell which kid skipped its DONE report without
reading the log.
"""
import importlib.util
import json
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"


def _load(name, filename=None):
    path = BIN / (filename or f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


import sys

pw = _load("post_wire")


def _manifest(agents):
    return {"iter": "L3.09", "agents": agents}


def test_done_line_present_when_log_has_a_done_line(tmp_path):
    log = tmp_path / "output.log"
    log.write_text(
        "some work\nDONE experiment:a00-abcd-1234\ncaveats: none\n")
    assert pw._done_line(str(log)) == "present"


def test_done_line_missing_when_log_has_no_done(tmp_path):
    log = tmp_path / "output.log"
    log.write_text("some work\nbut no DONE contract line here\n")
    assert pw._done_line(str(log)) == "missing"


def test_done_line_missing_when_log_is_absent(tmp_path):
    assert pw._done_line(str(tmp_path / "nope.log")) == "missing"


def test_stamp_done_lines_marks_every_agent_and_writes_back(tmp_path):
    a_log = tmp_path / "a" / "output.log"
    a_log.parent.mkdir(parents=True)
    a_log.write_text("DONE experiment:a00-aaaa-1111\n")
    mpath = tmp_path / "manifest.json"
    mpath.write_text(json.dumps(_manifest([
        {"id": "a00-aaaa", "log_file": str(a_log)},
        {"id": "a00-bbbb", "log_file": str(tmp_path / "missing.log")},
    ])))

    n = pw.stamp_done_lines(mpath)
    assert n == 2
    data = json.loads(mpath.read_text())
    by_id = {a["id"]: a["done_line"] for a in data["agents"]}
    assert by_id == {"a00-aaaa": "present", "a00-bbbb": "missing"}


def test_stamp_done_lines_absent_manifest_is_a_no_op(tmp_path):
    mpath = tmp_path / "manifest.json"
    assert pw.stamp_done_lines(mpath) == 0
    assert not mpath.exists()