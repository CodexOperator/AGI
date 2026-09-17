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
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
PY = sys.executable

EVENTS = [
    # real pi wire (parent-verified in installed pi-agent-core):
    # tool_execution_start {type, toolCallId, toolName, args}
    # tool_execution_end   {type, toolCallId, toolName, result, isError}
    # -- NO args and NO timestamp on the END event (rpc.md: "Use toolCallId
    # to correlate events"). The third end pair below has NO matching start:
    # it is the sequential-overrun case the stash still resolves.
    {"type": "tool_execution_start", "toolName": "bash",
     "toolCallId": "1", "args": {"command": "echo a"}},
    {"type": "tool_execution_end", "toolName": "bash",
     "toolCallId": "1", "isError": False,
     "result": {"content": [{"type": "text", "text": "a\n"}]}},
    {"type": "tool_execution_start", "toolName": "read",
     "toolCallId": "2", "args": {"path": "p"}},
    {"type": "tool_execution_end", "toolName": "read",
     "toolCallId": "2", "isError": True,
     "result": {"content": [{"type": "text", "text": "err"}]}},
    {"type": "tool_execution_end", "toolName": "bash",
     "toolCallId": "3", "isError": False,
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
    # real-wire shape: end event carries NO args, so the row must carry the
    # ARGS from the start stash -- THIS is the regression that proved the wire
    # fix. rows[2]'s end has no matching start (sequential overrun), so its
    # args resolve to None, which the named-line semantics still tolerate.
    assert rows[0]["args"] == {"command": "echo a"}, \
        "end event args:null must be backfilled from the start stash"
    assert rows[1]["args"] == {"path": "p"} and rows[1]["isError"] is True
    assert all(r["ts"] is not None for r in rows), \
        f"each row needs a non-null ts (from local clock), got {rows}"
    assert abs(rows[0]["ts"] - time.time()) < 5, "ts is local wall-clock receipt"
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


def test_end_without_args_carries_the_start_stash_args(tmp_path):
    """The exact wire regression (SM.87): pi's real tool_execution_end carries
    {type, toolCallId, toolName, result, isError} -- NO args. The row must
    backfill args from the tool_execution_start stash keyed by toolCallId."""
    stub = _stub_pi(tmp_path, [
        {"type": "tool_execution_start", "toolName": "bash",
         "toolCallId": "9", "args": {"command": "echo wire"}},
        {"type": "tool_execution_end", "toolName": "bash",
         "toolCallId": "9", "isError": False,
         "result": {"content": [{"type": "text", "text": "wire\n"}]}},
        {"type": "tool_execution_start", "toolName": "edit",
         "toolCallId": "10", "args": {"path": "p", "edits": []}},
        {"type": "tool_execution_update", "toolName": "edit",
         "toolCallId": "10", "args": {"path": "p", "edits": [1]},
         "partialResult": None},
        {"type": "tool_execution_end", "toolName": "edit",
         "toolCallId": "10", "isError": False,
         "result": {"content": [{"type": "text", "text": "ok"}]}},
    ])
    traj = tmp_path / "trajectory.jsonl"
    _run_wrapper(tmp_path, stub, traj)
    rows = [json.loads(l) for l in traj.read_text().splitlines()]
    assert [r["tool"] for r in rows] == ["bash", "edit"]
    assert rows[0]["args"] == {"command": "echo wire"}, \
        "end event carries no args; start stash must backfill it"
    assert rows[1]["args"] == {"path": "p", "edits": [1]}, \
        "update overwrites the start args; the LAST non-null wins"
    assert all(r["ts"] is not None for r in rows)


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

def _load_dispatch():
    sys.path.insert(0, str(BIN))
    spec = importlib.util.spec_from_file_location("agi_dispatch_traj", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_produced_command_wrapper_path_is_real_and_runs_end_to_end(tmp_path):
    """SM.87 regression (re-cut from the reverted SM.85): pi_adapter's wire
    is a REAL argv, so the produced command's wrapper path must be a file that
    EXISTS and the command must run the wrapper end-to-end to 3 ordered rows.
    The SM.85 revert happened because with_name() resolved the wrapper into
    adapters/ (a missing file), and no test executed the produced command."""
    dispatch = _load_dispatch()
    cmd = dispatch._build_pi_args(
        {"agent_dispatch": {"model": "qwen/qwen3.8-27b"}},
        str(tmp_path / "ctx.md"), "agent-0", 1, tmp_path)

    # the wrapper path the producer actually returned is a real file
    wrapper = Path(cmd[1])
    assert wrapper.is_file(), f"wrapper path must exist: {wrapper}"

    # run the produced command's own wrapper+python, retargeting only the
    # pi binary and trajectory path to the stub -- end to end -> 3 ordered rows
    stub = _stub_pi(tmp_path, EVENTS)
    traj = tmp_path / "traj_out.jsonl"
    run_cmd = [cmd[0], str(wrapper), "--wrapper", str(stub),
               str(traj), "--", *cmd[5:]]
    with (tmp_path / "run_out.log").open("wb") as logf:
        subprocess.run(run_cmd, stdout=logf, stderr=subprocess.STDOUT, check=True)

    rows = [json.loads(l) for l in traj.read_text().splitlines()]
    assert len(rows) == 3, f"one ordered entry per tool_execution_end, got {rows}"
    assert [r["tool"] for r in rows] == ["bash", "read", "bash"]
    assert rows[0]["args"] == {"command": "echo a"}
    assert rows[2]["result"]["content"][0]["text"] == "c\n"
    assert len(traj.read_bytes()) > 100, "full args+result, never a 400-char summary"
