"""glitch_master.py format-record — (hypothesis:l3w4-bug-master-seat, TESTS)

The Glitch Master seat's review formatter. Given agi-round-review.js's
returned JSON ({iter, global, targets}) on stdin, `format-record` writes it
verbatim to .agi/sessions/iter-<id>/review/results.json and prints exactly
one REVIEW line per target plus one GLOBAL line, each shaped for
send.py send --room tier3-quorum.
"""
from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parents[1] / "bin"
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import glitch_master  # noqa: E402


def _fixture(iter_id="L3.99"):
    return {
        "iter": iter_id,
        "global": {
            "git_status": " M extensions/agi/bin/glitch_master.py",
            "links_broken": 0,
            "goals_check_ok": True,
            "guard_output": "",
            "suite_passed": 42,
            "suite_failed": 0,
            "suite_skipped": 2,
            "suite_failures": [],
            "unexpected_files": [],
            "summary": "suite green; links intact",
        },
        "targets": [
            {
                "hypothesis": "hypothesis:l3w4-bug-master-seat",
                "parent_agent": "a00-abc",
                "experiment_ids": ["experiment:a00-3bb64c37-5f4296"],
                "verdict": "inconclusive_lean_proved:60",
                "parent_accepted": True,
                "parent_demoted": False,
                "files_changed": ["extensions/agi/bin/glitch_master.py",
                                  "extensions/agi/tests/test_glitch_master.py"],
                "verify_reran": True,
                "overclaims": [],
                "open_gaps": ["seat row install (sanctuary-master)"],
                "summary": "format-record built and green",
            },
        ],
    }


@contextlib.contextmanager
def _stdin(data):
    """Swap stdin for `data` for the duration of a direct format_record call."""
    prev = sys.stdin
    sys.stdin = io.StringIO(json.dumps(data))
    try:
        yield
    finally:
        sys.stdin = prev


def test_format_record_writes_results_json_verbatim(tmp_path):
    data = _fixture()
    with _stdin(data):
        out = glitch_master.format_record(
            _ns(iter_data="L3.99", root=str(tmp_path), out=None)
        )
    assert out == 0
    results = tmp_path / ".agi" / "sessions" / "iter-L3.99" / "review" / "results.json"
    assert results.read_text() == json.dumps(data)
    assert json.loads(results.read_text()) == data


def test_format_record_prints_one_review_line_per_target(tmp_path, capsys):
    with _stdin(_fixture()):
        glitch_master.format_record(
            _ns(iter_data="L3.99", root=str(tmp_path), out=None)
        )
    lines = [l for l in capsys.readouterr().out.splitlines()
             if l.startswith("REVIEW ")]
    assert len(lines) == 1
    assert lines[0].startswith(
        "REVIEW iter=L3.99 target=hypothesis:l3w4-bug-master-seat "
        "verdict=inconclusive_lean_proved:60 overclaims=0 open_gaps=1 "
        "files_changed=2 summary=\"format-record built and green\""
    )


def test_format_record_prints_one_global_line(tmp_path, capsys):
    with _stdin(_fixture()):
        glitch_master.format_record(
            _ns(iter_data="L3.99", root=str(tmp_path), out=None)
        )
    lines = [l for l in capsys.readouterr().out.splitlines() if l.startswith("GLOBAL ")]
    assert len(lines) == 1
    # guard_output empty -> clean; suite p/f/s from schema
    assert "links_broken=0 suite=42/0/2 guard=clean" in lines[0]
    assert lines[0].endswith('summary="suite green; links intact"')


def test_format_record_guard_warn_when_guard_output_nonempty(tmp_path):
    data = _fixture()
    data["global"]["guard_output"] = "warn: node X\nwarn: node Y"
    with _stdin(data):
        glitch_master.format_record(
            _ns(iter_data="L3.99", root=str(tmp_path), out=None)
        )
    results = tmp_path / ".agi" / "sessions" / "iter-L3.99" / "review" / "results.json"
    assert json.loads(results.read_text())["global"]["guard_output"]


def test_format_record_guard_warn_says_warn_n(tmp_path, capsys):
    data = _fixture()
    data["global"]["guard_output"] = "warn: node X\nwarn: node Y"
    with _stdin(data):
        glitch_master.format_record(
            _ns(iter_data="L3.99", root=str(tmp_path), out=None)
        )
    lines = [l for l in capsys.readouterr().out.splitlines() if l.startswith("GLOBAL ")]
    assert "guard=WARN:2" in lines[0]


def test_format_record_reads_stdin_and_cli_writes_file(tmp_path):
    data = _fixture(iter_id="L3.99")
    proc = subprocess.run(
        [sys.executable, str(BIN_DIR / "glitch_master.py"),
         "format-record", "--iter", "L3.99", "--root", str(tmp_path)],
        input=json.dumps(data), text=True, capture_output=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.count("REVIEW ") == 1
    assert proc.stdout.count("GLOBAL ") == 1
    results = tmp_path / ".agi" / "sessions" / "iter-L3.99" / "review" / "results.json"
    assert json.loads(results.read_text()) == data


def _ns(**kw):
    import argparse

    ns = argparse.Namespace()
    for k, v in kw.items():
        setattr(ns, k, v)
    return ns
