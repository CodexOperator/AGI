"""Tests for hypothesis:l4-every-pi-kid-keeps-its-full-tool-call-trajectory-
at-spawn-never-pruned-never-rebuilt.

The trajectory WRAPPER (pi_trajectory.py) is what `pi_adapter.build_command`
now spawns in place of a bare pi run, so these drive the REAL wrap path: a
stub pi process emitting the parent-verified `--mode json` event stream, fed
through the wrapper exactly as dispatch feeds it (stdout = output.log).

Falsifiers locked: (a) three tool calls land three ordered args+result jsonl
entries, never a 400-char summary; (b) a trajectory file that cannot open
yields ONE named `trajectory: not captured:` line, never silence and never a
fake; (c) session-complete carries trajectory.jsonl home with the session dir.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
PY = sys.executable

EVENTS = [
    {"type": "tool_execution_start", "toolName": "bash",
     "args": {"command": "echo a"}, "timestamp": 1},
    {"type": "tool_execution_end", "toolName": "bash",
     "args": {"command": "echo a"}, "timestamp": 2, "isError": False,
     "result": {"content": [{"type": "text", "text": "a\n"}]}},
    {"type": "tool_execution_start", "toolName": "read",
     "args": {"path": "p"}, "timestamp": 3},
    {"type": "tool_execution_end", "toolName": "read",
     "args": {"path": "p"}, "timestamp": 4, "isError": True,
     "result": {"content": [{"type": "text", "text": "err"}]}},
    {"type": "tool_execution_end", "toolName": "bash",
     "args": {"command": "echo c"}, "timestamp": 5, "isError": False,
     "result": {"content": [{"type": "text", "text": "c\n"}]}},
]


def _stub_pi(tmp_path: Path, lines: list[str]) -> Path:
    """A stub `pi`: prints one `--mode json` event object per line, then exits.
    It is the SUBPROCESS the wrapper runs, so the wiring is real."""
    script = tmp_path / "stubpi.py"
    script.write_text(
        "#!/usr/bin/env python3\nimport sys\n"
        + "\n".join(f"print({json.dumps(l)!r}, flush=True)" for l in lines)
        + "\n", encoding="utf-8")
    script.chmod(0o755)
    return script


def _run_wrapper(tmp_path: Path, stub: Path, traj: Path) -> Path:
    out = tmp_path / "output.log"
    with out.open("wb") as logf:
        subprocess.run(
            [PY, str(BIN / "pi_trajectory.py"), "--wrapper", str(stub),
             str(traj), "--", "--mode", "json", "hello"],
            stdout=logf, stderr=subprocess.STDOUT, check=True)
    return out


def test_three_tool_calls_land_three_ordered_jsonl_entries(tmp_path):
    stub = _stub_pi(tmp_path, EVENTS)
    traj = tmp_path / "trajectory.jsonl"
    out = _run_wrapper(tmp_path, stub, traj)

    rows = [json.loads(l) for l in traj.read_text().splitlines()]
    assert len(rows) == 3, f"one entry per tool_execution_end, got {rows}"
    assert [r["tool"] for r in rows] == ["bash", "read", "bash"]
    assert rows[0]["args"] == {"command": "echo a"}
    assert rows[0]["result"]["content"][0]["text"] == "a\n"
    assert rows[1]["args"] == {"path": "p"} and rows[1]["isError"] is True
    assert rows[2]["ts"] == 5
    # full args+result, never a 400-char summary
    assert len(traj.read_bytes()) > 100
    # output.log keeps the raw teed stream, in order
    text = out.read_text()
    assert text.index("tool_execution_end") < text.rindex("tool_execution_end")


def test_unwritable_trajectory_yields_one_named_line_never_silence(tmp_path):
    stub = _stub_pi(tmp_path, EVENTS)
    blk = tmp_path / "blk"
    blk.write_text("a file, not a dir\n")  # trajectory path under a FILE
    traj = blk / "trajectory.jsonl"
    out = _run_wrapper(tmp_path, stub, traj)

    assert not traj.exists()
    assert "trajectory: not captured:" in out.read_text(), \
        "a failsafe named line must ride output.log"


def _load_cli():
    spec = importlib.util.spec_from_file_location("agi_cli", BIN / "cli.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["agi_cli"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_session_complete_carries_trajectory_home(tmp_path):
    cli = _load_cli()
    n = 342
    dname = cli.locations.iteration_dirname(n)
    main = tmp_path / "main" / ".agi"
    (main / "config.json").parent.mkdir(parents=True)
    (main / "config.json").write_text("{}")
    wt = main / "worktrees" / "w1"
    wt.mkdir(parents=True)
    (wt / ".agi" / "config.json").parent.mkdir(parents=True)
    (wt / ".agi" / "config.json").write_text("{}", encoding="utf-8")
    src = wt / ".agi" / "sessions" / dname
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps(
        {"agents": [{"id": "a", "status": "done", "pid": 1}]}))
    (src / "output.log").write_text("x")
    (src / "trajectory.jsonl").write_text('{"tool": "bash"}\n')

    rc = cli._session_complete(main, n, live_iters=set())
    assert rc == 0, rc
    landed = main / "sessions" / dname / "trajectory.jsonl"
    assert landed.is_file(), "trajectory.jsonl must ride home with the session"
    assert landed.read_text() == '{"tool": "bash"}\n'