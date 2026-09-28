#!/usr/bin/env python3
"""Tool-call trajectory capture driver (hypothesis:l4-every-pi-kid-keeps-its-
full-tool-call-trajectory-at-spawn-never-pruned-never-rebuilt).

pi's session store prunes tool RESULTS, and dispatch.py exits right after
spawn (inline reaper off by default), so no parent may tee the child: the pi
adapter spawns THIS wrapper instead of bare pi. It runs the real pi under
`--mode json`, tees pi's stdout to output.log (dispatch redirects the
wrapper's stdout there) while parsing each `tool_execution_end` into one
ordered jsonl entry on trajectory.jsonl, forwards SIGTERM/SIGINT to pi and
exits with pi's code. A trajectory path that cannot open/write yields exactly
ONE named line -- never silence, never a fabricated record.

An empty provider response (stopReason=error, errorMessage naming an empty
response) is retried a BOUNDED number of times with backoff -- cells
`values.pi_retry.*`, never literals (hypothesis:an-empty-provider-response-is-
retried-not-fatal). Every other error, and an exhausted bound, end the round
exactly as before.

usage: pi_trajectory.py --wrapper <pi-bin> <trajectory.jsonl> -- [pi args...]
"""
from __future__ import annotations

import json
import signal
import subprocess
import sys
import time
from pathlib import Path

_NAMED = "trajectory: not captured: {}\n"
_RETRY = "retry: empty provider response {}/{} in {:.1f}s\n"
#: config-max: the bound and the backoff live in the config cells
#: values.pi_retry.*, never in this file. The two names below are their
#: DOCUMENTED DEFAULTS, used only when no config is reachable.
_DEFAULT_MAX_RETRIES = 2
_DEFAULT_BACKOFF_S = 5.0


def _retry_cells() -> tuple[int, float]:
    """(max retries, backoff seconds) from values.pi_retry.*, read through the
    ONE config loader; the documented defaults when none is reachable."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import locations  # noqa: PLC0415 -- the bin-script import pattern
        root = locations.find_project_root() or locations.project_root_from_env()
        cells = ((locations.load_config(root) if root else {})
                 .get("values") or {}).get("pi_retry") or {}
        max_retries = int(cells.get("empty_response_max_retries",
                                    _DEFAULT_MAX_RETRIES))
        backoff = float(cells.get("empty_response_backoff_s",
                                  _DEFAULT_BACKOFF_S))
    except Exception:
        return _DEFAULT_MAX_RETRIES, _DEFAULT_BACKOFF_S
    return max(0, max_retries), max(0.0, backoff)


def _is_empty_response(raw: str) -> bool:
    """True for the provider's empty-response stop: stopReason=error whose
    errorMessage names an empty response (5 rounds died on exactly this in
    EG.18-EG.20). Every OTHER error is False -- it ends the round as today.

    `raw` is whatever pi's PIPE yielded, so a BYTE line (pi's own plain-text
    warning, e.g. an unknown-model notice) must decode, never raise: a
    detector that crashes on a non-JSON line kills the very round it exists
    to save (measured EG.30: TypeError -> the round died on line 1).
    """
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8", "replace")
    try:
        ev = json.loads(raw)
    except Exception:
        ev = None
    if isinstance(ev, dict):
        msg = str(ev.get("errorMessage") or raw)
        return ev.get("stopReason") == "error" and "empty" in msg.lower()
    return '"stopReason":"error"' in raw and "empty response" in raw.lower()


def _attempt(pi_bin, traj_path, pi_args) -> tuple[int, bool]:
    """One pi run, teed and parsed exactly as before.

    Returns (exit code, saw an empty provider response)."""
    empty = False
    pi = subprocess.Popen([pi_bin, *pi_args], stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    # The forwarder lives exactly as long as the CHILD: past this scope it aims
    # at a reaped pid, so a cancel landing in main's backoff sleep is swallowed
    # and the round RESPAWNS the provider after dispatch gave up (measured
    # EG.30). Restored below: between runs the wrapper's own SIGTERM is the
    # default disposition -- die.
    prev_handlers = {sig: signal.signal(sig, lambda s, f, p=pi: p.send_signal(s))
                     for sig in (signal.SIGTERM, signal.SIGINT)}
    trajf, failed = None, False
    try:
        trajf = open(traj_path, "a", encoding="utf-8")
    except OSError as exc:
        failed = True
        sys.stdout.write(_NAMED.format(exc))
        sys.stdout.flush()
    args_by_id = {}
    for raw in pi.stdout:
        sys.stdout.buffer.write(raw)
        sys.stdout.flush()
        if _is_empty_response(raw):
            empty = True
        if trajf is None:
            continue
        try:
            ev = json.loads(raw)
        except Exception:
            continue  # not a json event (e.g. pi's plain-text stream error)
        # pi's real tool_execution_end carries {type, toolCallId, toolName,
        # result, isError}: NO args, NO timestamp. Doc rpc.md: "Use
        # toolCallId to correlate events", so the ARGS ride on start/update
        # and the wall-clock ts is the honest time a sidecar writer owns.
        if ev.get("type") == "tool_execution_start":
            args_by_id[ev.get("toolCallId")] = ev.get("args")
            continue
        if ev.get("type") == "tool_execution_update":
            if ev.get("args") is not None:
                args_by_id[ev.get("toolCallId")] = ev.get("args")
            continue
        if ev.get("type") != "tool_execution_end":
            continue
        try:
            trajf.write(json.dumps({
                "ts": time.time(), "tool": ev.get("toolName"),
                "args": args_by_id.get(ev.get("toolCallId")),
                "result": ev.get("result"),
                "isError": bool(ev.get("isError"))}) + "\n")
            trajf.flush()
        except Exception as exc:
            if not failed:
                sys.stdout.write(_NAMED.format(exc))
                sys.stdout.flush()
                failed = True
            trajf.close()
            trajf = None
    if trajf is not None:
        trajf.close()
    for sig, prev in prev_handlers.items():
        signal.signal(sig, prev)
    return pi.wait(), empty


def main(argv):
    a = argv[1:]
    if a and a[0] in ("-h", "--help"):
        sys.stdout.write(__doc__)
        return 0
    if len(a) < 5 or a[0] != "--wrapper" or a[3] != "--":
        return 2
    pi_bin, traj_path, pi_args = a[1], a[2], a[4:]
    max_retries, backoff = _retry_cells()
    for attempt in range(max_retries + 1):
        code, empty = _attempt(pi_bin, traj_path, pi_args)
        if not empty or attempt == max_retries:
            return code
        # The ONLY thing that earns a retry is an empty provider response, and
        # the bound is finite, so an always-empty provider cannot loop forever.
        sys.stdout.write(_RETRY.format(attempt + 1, max_retries, backoff))
        sys.stdout.flush()
        time.sleep(backoff)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
