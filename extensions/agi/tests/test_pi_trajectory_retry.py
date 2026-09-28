"""Tests for hypothesis:an-empty-provider-response-is-retried-not-fatal.

An empty provider response (stopReason=error + an errorMessage naming an empty
response) killed 5 parent rounds dead (DH.660/661, EG.18-EG.20 -- 3 x each in
output.log). The wrapper must retry a BOUNDED number of times with backoff and
name every retry in the log; every OTHER error, and an exhausted bound, must
end the round exactly as before.

Stub pi only, never the live provider. The bound and the backoff come from a
config the TEST writes (values.pi_retry.*), which is also the proof that they
are cells and not literals. Falsifiers locked: the retry fires on a
non-empty-response error; the bound does not hold (an always-empty provider
loops forever); the retries are invisible in the log.

AGI_TRAJ_WRAPPER lets the round point the same tests at the PRE-fix wrapper to
show RED.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
PY = sys.executable
WRAPPER = os.environ.get("AGI_TRAJ_WRAPPER") or str(BIN / "pi_trajectory.py")

EMPTY = {"type": "turn_end", "stopReason": "error",
         "errorMessage": "Provider returned an empty response"}
OTHER = {"type": "turn_end", "stopReason": "error",
         "errorMessage": "Provider returned a 500 from upstream"}
OK = {"type": "tool_execution_start", "toolName": "bash", "toolCallId": "1",
      "args": {"command": "echo a"}}
OK_END = {"type": "tool_execution_end", "toolName": "bash",
          "toolCallId": "1", "isError": False,
          "result": {"content": [{"type": "text", "text": "a\n"}]}}


def _project(tmp_path: Path, max_retries: int, backoff: float) -> Path:
    """A .agi/ project the wrapper's OWN config loader walks up to, carrying
    only the two cells under test."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"values": {"pi_retry": {"empty_response_max_retries": max_retries,
                                 "empty_response_backoff_s": backoff}}}),
        encoding="utf-8")
    return root


def _stub_pi(tmp_path: Path, runs: list[list[dict]]) -> tuple[Path, Path]:
    """A stub `pi`: the Nth invocation prints runs[n] (the last set repeats),
    and every invocation appends a line to the counter file, so the test can
    assert how many times the wrapper respawned the provider."""
    counter = tmp_path / "runs.txt"
    script = tmp_path / "stubpi.py"
    script.write_text(
        "#!/usr/bin/env python3\n"
        "import json, sys, pathlib\n"
        f"runs = {runs!r}\n"
        f"c = pathlib.Path({str(counter)!r})\n"
        "n = len(c.read_text().splitlines()) if c.exists() else 0\n"
        "c.write_text(('run\\n') * (n + 1))\n"
        "evs = runs[min(n, len(runs) - 1)]\n"
        "for ev in evs:\n    print(json.dumps(ev), flush=True)\n"
        "sys.exit(1 if any(e.get('stopReason') == 'error' for e in evs) else 0)\n",
        encoding="utf-8")
    script.chmod(0o755)
    return script, counter


def _run(root: Path, stub: Path, counter: Path, traj: Path) -> tuple[str, list[str]]:
    out = root / "output.log"
    with out.open("wb") as logf:
        rc = subprocess.run(
            [PY, WRAPPER, "--wrapper", str(stub), str(traj), "--", "--mode",
             "json", "hello"], cwd=str(root), stdout=logf,
            stderr=subprocess.STDOUT, check=False).returncode
    runs = counter.read_text().splitlines() if counter.exists() else []
    return out.read_text(), runs


def test_empty_response_is_retried_and_then_the_round_lands(tmp_path):
    """RED on the base: one empty response ends the round. GREEN here -- the
    wrapper respawns the provider, names the retry, and the next normal stop
    ends the round with its work on the trajectory."""
    root = _project(tmp_path, 2, 0.05)
    stub, counter = _stub_pi(tmp_path, [[EMPTY], [OK, OK_END]])
    traj = root / "trajectory.jsonl"
    text, runs = _run(root, stub, counter, traj)

    assert runs == ["run", "run"], \
        f"the empty response is retried once, not fatal; got {runs}"
    assert "retry: empty provider response 1/2" in text, \
        f"every retry is counted in the round log, got {text!r}"
    assert [json.loads(l)["tool"] for l in traj.read_text().splitlines()] \
        == ["bash"], "the retried round's real work still lands on the trajectory"


def test_other_errors_are_not_retried(tmp_path):
    """A non-empty-response error ends the round exactly as today."""
    root = _project(tmp_path, 2, 0.05)
    stub, counter = _stub_pi(tmp_path, [[OTHER]])
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert runs == ["run"], f"no retry on another error, got {runs}"
    assert "retry: empty provider response" not in text, text


def test_the_bound_is_the_config_cell_and_holds(tmp_path):
    """An always-empty provider costs 1 + the cell's retries, then dies."""
    root = _project(tmp_path, 1, 0.05)
    stub, counter = _stub_pi(tmp_path, [[EMPTY]])
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert runs == ["run", "run"], \
        f"the BOUND is values.pi_retry.empty_response_max_retries=1, got {runs}"
    assert text.count("retry: empty provider response 1/1") == 1, text
