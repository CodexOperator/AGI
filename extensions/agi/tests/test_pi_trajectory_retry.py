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
import signal
import subprocess
import sys
import time
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
PY = sys.executable
WRAPPER = os.environ.get("AGI_TRAJ_WRAPPER") or str(BIN / "pi_trajectory.py")

EMPTY = {"type": "turn_end", "stopReason": "error",
         "errorMessage": "Provider returned an empty response"}
OTHER = {"type": "turn_end", "stopReason": "error",
         "errorMessage": "Provider returned a 500 from upstream"}
# The REAL wire shape, measured on EG.104 a00-b9e8e8d9's own live log
# (.agi/sessions/iter-EG.104/a00-b9e8e8d9/output.log): every turn_end carries
# {"type","message","toolResults"} and the stop fields live INSIDE "message".
# message_end carries {"type","message"} the same way.
NESTED_EMPTY = {"type": "message_end",
                "message": {"role": "assistant", "api": "openrouter-completions",
                            "model": "stealth/space-bunny-alpha",
                            "stopReason": "error",
                            "errorMessage": "Provider returned an empty response",
                            "content": [], "provider": "openrouter",
                            "responseId": "gen-0", "timestamp": 1}}
NESTED_TURN_EMPTY = {"type": "turn_end", "toolResults": [],
                     "message": {"role": "assistant", "stopReason": "error",
                                 "errorMessage": "Provider returned an empty response"}}
NESTED_OTHER = {"type": "message_end",
                "message": {"role": "assistant", "stopReason": "error",
                            "errorMessage": "Provider returned a 500 from upstream"}}
# A toolResult's message_end. It ends a MESSAGE, never a turn, so it must not
# decide the round: on the pre-fix bytes _ended_on_empty answered False for it
# and OVERWROTE the empty=True set by the turn_end before it.
TOOLRESULT_END = {"type": "message_end",
                  "message": {"role": "toolResult", "toolCallId": "1",
                              "toolName": "bash", "isError": False,
                              "content": [{"type": "text", "text": "a\n"}],
                              "timestamp": 2}}
OK = {"type": "tool_execution_start", "toolName": "bash", "toolCallId": "1",
      "args": {"command": "echo a"}}
OK_END = {"type": "tool_execution_end", "toolName": "bash",
          "toolCallId": "1", "isError": False,
          "result": {"content": [{"type": "text", "text": "a\n"}]}}
# A COMPLETED, non-empty turn: what PROGRESS looks like on the wire (pi ends
# every turn with a turn_end), and so what zeroes the consecutive count.
GOOD = {"type": "turn_end", "toolResults": [],
        "message": {"role": "assistant", "stopReason": "stop"}}


def _project(tmp_path: Path, max_retries: int, backoff: float,
             **cells) -> Path:
    """A .agi/ project the wrapper's OWN config loader walks up to, carrying
    only the cells under test. Extra kwargs are the two backoff cells;
    omitting them IS the missing-cell case."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"values": {"pi_retry": dict(
            {"empty_response_max_retries": max_retries,
             "empty_response_backoff_s": backoff}, **cells)}}),
        encoding="utf-8")
    return root


def _stub_pi(tmp_path: Path, runs: list[list[dict]],
             code: int | None = None,
             raw: bytes = b"") -> tuple[Path, Path]:
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
        f"if {raw!r}:\n"
        "    sys.stdout.buffer.write(" + repr(raw) + ")\n"
        "    sys.stdout.buffer.flush()\n"
        "evs = runs[min(n, len(runs) - 1)]\n"
        "for ev in evs:\n    print(json.dumps(ev), flush=True)\n"
        f"ec = {code!r}\n"
        "sys.exit(ec if ec is not None else\n"
        "           (1 if any(e.get('stopReason') == 'error' for e in evs) else 0))\n",
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
    recs = [json.loads(l) for l in traj.read_text().splitlines()]
    assert [r["tool"] for r in recs if r.get("tool")] == ["bash"], \
        "the retried round's real work still lands on the trajectory"
    assert [r["attempt"] for r in recs if r.get("type") == "attempt_boundary"] \
        == [1, 2], \
        "each attempt opens with ONE boundary record, so the discarded " \
        f"attempt's records are attributable, not fused: {recs}"


def test_the_real_pi_shape_exit_0_on_an_empty_response_is_retried(tmp_path):
    """Real pi exits 0 on an empty response in `--mode json`: its print-mode
    raises exitCode=1 inside the `mode === "text"` branch only, and dispatch
    spawns `-p --mode json` (pi dist/modes/print-mode.ts). So an exit-code
    guard suppresses EVERY retry in production while a stub suite stays green
    -- this test is the stub that carries pi's REAL exit code, not the code the
    test itself would like (EG.34's guard test passed code=0 by parameter)."""
    root = _project(tmp_path, 2, 0.05)
    stub, counter = _stub_pi(tmp_path, [[EMPTY], [OK, OK_END]], code=0)
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert runs == ["run", "run"], \
        f"an exit-0 empty response is what production sends; got {runs}"
    assert "retry: empty provider response 1/2" in text, text


def test_an_attempt_that_emptied_then_landed_is_not_respawned(tmp_path):
    """The bound is not the exit code either: an attempt that emptied mid-stream
    and then ended on a NORMAL stop has finished its round, so respawning it
    would redo the work. The LAST turn decides, not the first empty line."""
    root = _project(tmp_path, 2, 0.05)
    stub, counter = _stub_pi(tmp_path, [[OK, OK_END, EMPTY,
                                         {"type": "turn_end",
                                          "stopReason": "stop"}]])
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert runs == ["run"], f"a landed attempt is not respawned, got {runs}"
    assert "retry: empty provider response" not in text, text


def test_a_plain_byte_line_decodes_and_never_kills_the_round(tmp_path):
    """Regression on the bytes-decode repair: pi's own plain-text notice
    arrives on the PIPE as bytes, so the detector decodes instead of raising
    (a TypeError here killed the round the wrapper exists to save)."""
    root = _project(tmp_path, 1, 0.05)
    stub, _ = _stub_pi(tmp_path, [[OK, OK_END]],
                       raw=b"warning: unknown model\n")
    text, _ = _run(root, stub, tmp_path / "absent.txt", root / "t.jsonl")
    assert "Traceback" not in text, f"a byte line must not crash: {text!r}"
    assert (root / "t.jsonl").read_text().strip(), "records still land"


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




def test_the_nested_real_wire_shape_is_retried(tmp_path):
    """RED on EG.103's bytes: pi nests stopReason/errorMessage under
    `message`, and both detectors read the TOP level, so on a real production
    line the retry NEVER fired. Fixture = the shape measured on this round's own
    output.log, not a shape the engine invented for itself."""
    root = _project(tmp_path, 2, 0.05)
    stub, counter = _stub_pi(tmp_path, [[NESTED_EMPTY], [OK, OK_END]])
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert runs == ["run", "run"], \
        f"the REAL nested empty response is retried, not fatal: {runs} / {text!r}"
    assert "retry: empty provider response 1/2" in text, text


def test_a_nested_turn_end_empty_is_retried_too(tmp_path):
    """turn_end nests the same way as message_end; a provider can empty on
    either, and both end the turn."""
    root = _project(tmp_path, 2, 0.05)
    stub, counter = _stub_pi(tmp_path, [[NESTED_TURN_EMPTY], [OK, OK_END]])
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert runs == ["run", "run"], f"a nested turn_end empty retries: {runs}"
    assert "retry: empty provider response 1/2" in text, text


def test_a_toolresult_message_end_after_an_empty_turn_end_still_retries(tmp_path):
    """RED on the pre-fix bytes: the last-turn decision was keyed on
    ("turn_end","message_end"), so a toolResult's message_end arriving AFTER an
    empty turn_end answered False and MASKED the empty stop -- the empty last
    turn would have gone unretried. LATENT, not live: no production log shows
    a toolResult message_end AFTER a turn_end (every one precedes it; measured
    CORRECTIVE EG.151), so this is a strict narrowing of the trigger, not a
    round that died. Only a turn ends a turn."""
    root = _project(tmp_path, 2, 0.05)
    stub, counter = _stub_pi(tmp_path, [[NESTED_TURN_EMPTY, TOOLRESULT_END],
                                        [OK, OK_END]])
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert runs == ["run", "run"], \
        f"a toolResult message_end never masks an empty turn_end: {runs} / {text!r}"
    assert "retry: empty provider response 1/2" in text, text


def test_a_nested_NON_empty_error_is_still_not_retried(tmp_path):
    """The nesting fix must not widen the trigger: a 500 nested under
    `message` still ends the round exactly as before."""
    root = _project(tmp_path, 2, 0.05)
    stub, counter = _stub_pi(tmp_path, [[NESTED_OTHER]])
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert runs == ["run"], f"no retry on another error: {runs} / {text!r}"
    assert "retry: empty provider response" not in text, text


def _cancel(root: Path, stub: Path, marker: str):
    """Run the wrapper on `stub`, SIGTERM it once `marker` is in its log, and
    return (rc|None, seconds): rc None = still ALIVE, the cancel was
    swallowed. The counter file of the stub (its respawn evidence) is left on
    disk for the caller to read."""
    proc = subprocess.Popen(
        [PY, WRAPPER, "--wrapper", str(stub), str(root / "trajectory.jsonl"),
         "--", "--mode", "json", "hello"], cwd=str(root),
        stdout=(root / "output.log").open("wb"), stderr=subprocess.STDOUT)
    for _ in range(80):                     # a backoff wide enough to land in
        if marker in (root / "output.log").read_text(errors="replace"):
            break
        time.sleep(0.05)
    t0 = time.time()
    proc.send_signal(signal.SIGTERM)
    try:
        return proc.wait(timeout=2.0), time.time() - t0
    except subprocess.TimeoutExpired:
        return None, time.time() - t0
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()


def _waits(text: str) -> list[float]:
    """The sleeps the wrapper RECORDED in its own log, in order."""
    return [float(l.rsplit(" in ", 1)[1].rstrip("s")) for l in text.splitlines()
            if l.startswith("retry: empty provider response")]


def test_more_total_empties_than_the_bound_still_finishes(tmp_path):
    """RED on the base: the bound was PER RUN, so a third empty -- never more
    than one IN A ROW, each after a completed turn -- killed a progressing
    round. A completed turn zeroes the count: the run FINISHES.

    The TOTAL ceiling is set explicitly to 12, well above this run's 4
    attempts, because the finishing guarantee FALSIFIER 1 claims is now
    BOUNDED by it (EG.187): left at the derived 4 x (max_retries + 1) = 8 the
    fixture would sit under the ceiling by luck, not by construction."""
    root = _project(tmp_path, 1, 0.0, empty_response_max_attempts_total=12)
    stub, counter = _stub_pi(tmp_path, [[OK, OK_END, GOOD, EMPTY]] * 3 +
                                        [[OK, OK_END, GOOD]])
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert len(runs) == 4, f"3 empties > max_retries=1, never 2 in a row: {runs}"
    assert text.count("retry: empty provider response 1/1") == 3, \
        f"every empty of the run was retried and counted: {text!r}"
    for ordinal in (2, 3, 4):
        assert f"(attempt {ordinal}/12)" in text, \
            f"the retry line names the TOTAL attempt ordinal: {text!r}"
    assert "total empty-response attempts" not in text, \
        f"the total ceiling never cut this run: {text!r}"


def test_the_consecutive_bound_is_real(tmp_path):
    """Not 'unlimited while progressing': an always-empty provider still costs
    1 + max_retries attempts, then the round ends."""
    root = _project(tmp_path, 2, 0.0)
    stub, counter = _stub_pi(tmp_path, [[EMPTY]])
    text, runs = _run(root, stub, counter, root / "trajectory.jsonl")
    assert runs == ["run"] * 3, f"2 CONSECUTIVE retries, then the end: {runs}"
    assert text.count("retry: empty provider response") == 2, text


def test_the_growing_backoff_is_min_base_x_factor_pow_k_minus_1_capped(tmp_path):
    """RED on the base: every retry waited the flat base cell. The wait before
    retry k is min(base x factor^(k-1), cap) -- cells, one loader."""
    root = _project(tmp_path, 3, 0.01, empty_response_backoff_factor=2.0,
                    empty_response_backoff_cap_s=0.03)
    stub, counter = _stub_pi(tmp_path, [[EMPTY]])
    text, _ = _run(root, stub, counter, root / "trajectory.jsonl")
    assert _waits(text) == [0.01, 0.02, 0.03], f"growing, then capped: {_waits(text)}"


def test_a_missing_backoff_cell_falls_back_to_todays_flat_wait(tmp_path):
    """A config written before the two cells exist waits exactly what it
    waited before: factor 1.0, cap = base, so the default costs no waiting."""
    root = _project(tmp_path, 2, 0.01)
    stub, counter = _stub_pi(tmp_path, [[EMPTY]])
    text, _ = _run(root, stub, counter, root / "trajectory.jsonl")
    assert _waits(text) == [0.01, 0.01], f"no cells, no change: {_waits(text)}"


def test_cancel_inside_the_backoff_dies_and_does_not_respawn(tmp_path):
    """RED on the base: the SIGTERM forwarder outlived the child, so a cancel
    landing in main's backoff was swallowed and the provider was RESPAWNED."""
    root = _project(tmp_path, 2, 6.0)
    stub, counter = _stub_pi(tmp_path, [[EMPTY]])
    rc, secs = _cancel(root, stub, "retry: empty provider response")
    runs = counter.read_text().splitlines() if counter.exists() else []
    assert rc is not None and secs < 2.0, \
        f"a cancelled round dies promptly, not parked in backoff: rc={rc}"
    assert runs == ["run"], \
        f"a cancelled round never respawns the provider, got {runs}"


def test_cancel_while_pi_runs_is_still_forwarded(tmp_path):
    """The forwarder keeps its job WHILE the child lives: the cancel reaches
    pi and the wrapper dies promptly instead of waiting the run out."""
    root = _project(tmp_path, 0, 0.05)
    sleeper = tmp_path / "sleeper.py"
    sleeper.write_text("#!/usr/bin/env python3\nimport time\nprint('{}',"
                       " flush=True)\ntime.sleep(30)\n", encoding="utf-8")
    sleeper.chmod(0o755)
    rc, secs = _cancel(root, sleeper, "{}")
    assert rc is not None and secs < 2.0, \
        f"a live child's cancel is forwarded, not ignored: rc={rc} {secs:.1f}s"


def _run_bounded(root: Path, stub: Path, timeout: float):
    """(rc|None, runs, log) with a HARD timeout: rc None means the wrapper never
    ended on its own, which is the defect F4 is about. Never an unbounded run."""
    log = root / "output.log"
    with log.open("wb") as logf:
        try:
            rc = subprocess.run(
                [PY, WRAPPER, "--wrapper", str(stub),
                 str(root / "trajectory.jsonl"), "--", "--mode", "json", "hello"],
                cwd=str(root), stdout=logf, stderr=subprocess.STDOUT,
                check=False, timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            rc = None
    counter = root.parent / "runs.txt"
    runs = counter.read_text().splitlines() if counter.exists() else []
    return rc, runs, log.read_text()


def test_a_total_attempt_ceiling_ends_a_provider_that_always_progresses(
        tmp_path):
    """F4 (EG.187). RED on the cut f498ef5e7, where the run HANGS: main() zeroes
    `empties` on ANY attempt that made progress, so a stub that completes a
    turn and THEN ends empty, on every attempt, never spends the consecutive
    bound -- the parent's GATE probe measured 606 attempts in 15 s and was
    killed. The total-attempt ceiling is what ends such a run."""
    root = _project(tmp_path, 1, 0.0, empty_response_max_attempts_total=5)
    stub, _ = _stub_pi(tmp_path, [[OK, OK_END, GOOD, EMPTY]])
    rc, runs, text = _run_bounded(root, stub, 20)
    assert rc is not None, \
        f"the run NEVER ends on its own: {len(runs)} attempts in 20 s"
    assert len(runs) == 5, \
        f"values.pi_retry.empty_response_max_attempts_total=5, got {len(runs)}"
    assert "total empty-response attempts 5/5" in text, \
        f"the ceiling names itself in the round log: {text!r}"
    assert rc == 1, f"the round's own code is returned, got {rc}"


def test_the_total_ceiling_default_is_derived_from_the_consecutive_bound(
        tmp_path):
    """Absent, the total ceiling is DERIVED (4 x (max_retries + 1)), never a
    new magic number, and it is a cell: max_retries=2 -> 12 attempts."""
    root = _project(tmp_path, 2, 0.0)
    stub, _ = _stub_pi(tmp_path, [[OK, OK_END, GOOD, EMPTY]])
    rc, runs, _ = _run_bounded(root, stub, 60)
    assert rc is not None, f"never ends without the ceiling: {len(runs)}"
    assert len(runs) == 12, f"4 x (2 + 1) attempts, got {len(runs)}"
