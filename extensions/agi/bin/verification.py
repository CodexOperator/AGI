#!/usr/bin/env python3
"""verification.py — ONE command replaces the four-tool rotation ritual.

This is NOT `verify_unified.py`. `verify_unified.py` is the `goal:g11`
migration checker — it proves the old staged-checkout repo collapsed into one
tree, and it has nothing to do with rotation. `verification.py` is the
rotation/health-check round; the two names are one keystroke apart and must
never be merged or shared. `hypothesis:l4-unified-verification`, for
`goal:g1.10`: a successor runs ONE command at rotation and spends tokens on one
summary block, not four scrollbacks, and every check it runs is resolved
THROUGH `commands.py` from `command:commands`
(`.agi/nodes/.geometry/commands.md`) — never argv written literally here.

Levels (`--level quick|rotation|full`, default `rotation`):
  quick    = links + goals-check + write-guard        (pre-commit set, <15s)
  rotation = quick + smoke + viewport-verify + dispatch-help + budget
  full     = rotation + schema + credentials + secrets + crons
NO level runs pytest. `--suite` is OPT-IN and ORTHOGONAL to level: it adds the
pytest run and nothing else, and its absence is never a failure. The suite
window is the Prime's to grant, one runner at a time, and until `goal:g17.1`'s
L4.10 lands, `test_send.py` nudges real tmux panes — so `verification.py` must
never take that window unasked. When L4.10 lands, `full` folds the suite in
and this file holds the lock that guarantees one runner; until then the lock
(plain pid file, stale-broken) is present but `--suite` stays opt-in.

The node-count check is a COMPARISON, not a print. Smoke prints counts; "the
active count must not drop" is meaningless without a baseline. The active /
deprecated / total triple is recorded between runs in `.agi/sessions/`, and
this file FAILS when active is below the recorded value — the one failure this
tool exists to catch (H0/H0b: 29k nodes lost).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402
import commands  # noqa: E402

#: Per-check wall-clock ceiling. A check that hangs past this is a failure the
#: successor must see, not a run that never returns.
PER_CHECK_TIMEOUT = 600

#: The SUITE's own ceiling. One number for every check made the one check that
#: legitimately takes minutes the one check that false-FAILs: the engine suite
#: is ~2300 tests, and reporting a green suite as "timed out after 600s" is a
#: failure the tool invented. A hang is still caught, three times further out.
SUITE_TIMEOUT = 1800

#: How each level is composed. Names are COMMAND NAMES resolved through
#: `commands.py` against the node — never argv written here.
LEVELS: dict[str, list[str]] = {
    "quick": ["links", "goals-check", "write-guard"],
    "rotation": ["links", "goals-check", "write-guard",
                 "smoke", "viewport-verify", "dispatch-help", "budget"],
    "full": ["links", "goals-check", "write-guard",
             "smoke", "viewport-verify", "dispatch-help", "budget",
             "schema", "credentials", "secrets", "crons"],
}

#: The declared command `--suite` adds to a level. Opt-in only.
SUITE_CMD = "tests"

STATE_FILE = "verify-count.json"        # under <groot>/sessions/
SUITE_LOCK = "verify-suite.lock"        # under <groot>/sessions/


@dataclass
class CheckResult:
    """One check's verdict, its elapsed time, and the number it produces."""

    name: str
    status: str                 # PASS | FAIL | SKIP
    elapsed: float
    number: dict | None = None
    note: str = ""
    message: str = ""


def _parse_number(name: str, exitcode: int, output: str) -> dict | None:
    """The one number each check exists to produce.

    Only the three checks with a real number extract one (goal:g1.10 prose
    names them): smoke's active/deprecated/total triple, links' broken count,
    goals-check's byte-identity yes/no. Everywhere else the exit code is the
    fact and the number column is empty.
    """
    if name == "smoke":
        vals = dict(re.findall(r"METRIC\s+(\w+)=(-?\d+)", output))
        return {
            "active": int(vals["active_node_count"]) if "active_node_count" in vals else -1,
            "deprecated": int(vals["deprecated_node_count"]) if "deprecated_node_count" in vals else -1,
            "total": int(vals["node_count"]) if "node_count" in vals else -1,
        }
    if name == "links":
        m = re.search(r"(\d+)\s+broken", output)
        return {"broken": int(m.group(1)) if m else -1}
    if name == "goals-check":
        return {"byte-identical": 1 if exitcode == 0 else 0}
    return None


def _passed(name: str, exitcode: int, number: dict | None) -> bool:
    """Decide pass/fail for one check, beyond the bare exit code.

    `links` exits 0 even with broken links (it only fails with `--broken`), so
    the broken count is the fact, not the code. Everything else passes on
    exit 0.
    """
    if name == "links":
        return number is not None and number.get("broken") == 0 and exitcode == 0
    if name == "smoke":
        return exitcode == 0 and number is not None and number["active"] >= 0
    return exitcode == 0


# --- the count baseline (a comparison, not a print) -------------------------


def _state_path(groot: Path) -> Path:
    return Path(groot) / "sessions" / STATE_FILE


def _read_state(groot: Path) -> dict | None:
    try:
        return json.loads(_state_path(groot).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def compare_count(groot: Path, current: dict | None) -> CheckResult:
    """The node-count check: FAIL when active is below the recorded baseline.

    First run has no baseline — record the triple, pass, and SAY SO. Later
    runs FAIL when current active < recorded active, else update and pass.
    """
    start = time.monotonic()
    if current is None or current.get("active", -1) < 0:
        return CheckResult("node-count", "SKIP", time.monotonic() - start,
                           note="smoke did not report an active count")
    state = _read_state(groot)
    if state is None:
        _write_state(groot, current)
        return CheckResult("node-count", "PASS", time.monotonic() - start,
                           current,
                           note="baseline recorded (no prior baseline)",
                           message=f"active={current['active']} recorded")
    if current["active"] < state["active"]:
        return CheckResult(
            "node-count", "FAIL", time.monotonic() - start, current,
            note=("ACTIVE COUNT DROPPED: "
                  f"active={current['active']} below baseline={state['active']} "
                  "(H0/H0b: 29k nodes lost to a silent drop)"),
            message=("active below recorded baseline: "
                     f"{current['active']} < {state['active']}"))
    _write_state(groot, current)
    return CheckResult("node-count", "PASS", time.monotonic() - start, current,
                       message=("active steady: "
                                f"{current['active']} >= baseline {state['active']}"))


def _write_state(groot: Path, current: dict) -> None:
    path = _state_path(groot)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(current), encoding="utf-8")


# --- the suite lock (opt-in; one runner at a time) --------------------------


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def acquire_suite_lock(groot: Path) -> tuple[Path | None, int | None]:
    """A plain lock file holding the holder's pid, stale-broken by a dead pid.

    Returns `(path, None)` on success and `(None, holder_pid)` when another
    LIVE runner owns the window — the pid is returned rather than swallowed so
    the refusal can name who to wait for; "refused" without a holder is a
    message that tells a successor nothing it can act on. `(None, None)` means
    the lock could not be written at all.

    Keeping `--suite` opt-in is what rules today; the lock is the mechanism
    that rules when L4.10 folds the suite into `full`.
    """
    path = Path(groot) / "sessions" / SUITE_LOCK
    path.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(2):
        if path.exists():
            try:
                holder = int(path.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                path.unlink(missing_ok=True)
                continue
            if _pid_alive(holder) and holder != os.getpid():
                return None, holder  # another live runner owns the window
            path.unlink(missing_ok=True)  # stale: dead pid
        try:
            path.write_text(str(os.getpid()), encoding="utf-8")
            return path, None
        except OSError:
            return None, None
    return None, None


# --- the runner ------------------------------------------------------------


def run_check(groot: Path, name: str, verbose: bool) -> CheckResult:
    """Run ONE declared command and judge it. Never raises for the check.

    The argv comes from `commands.load(groot)[name].argv` — resolved from the
    node, never written here. A check that is not declared in the node is a
    FAIL with a message saying so: the graph is the single source, and a level
    that names a check the node has not declared is a graph that has drifted.
    """
    start = time.monotonic()
    table = commands.load(groot)
    if name not in table or not table[name].argv:
        return CheckResult(name, "FAIL", time.monotonic() - start,
                           note=f"check {name!r} is not a declared command in "
                                ".geometry/commands.md — add it to the node")
    cmd = table[name]
    ceiling = SUITE_TIMEOUT if name == SUITE_CMD else PER_CHECK_TIMEOUT
    try:
        proc = subprocess.run(
            cmd.argv, capture_output=True, text=True,
            timeout=ceiling, cwd=cmd.cwd or None)
    except subprocess.TimeoutExpired:
        return CheckResult(name, "FAIL", time.monotonic() - start,
                           note=f"timed out after {ceiling}s")
    except OSError as exc:
        return CheckResult(name, "FAIL", time.monotonic() - start,
                           note=f"could not execute: {exc}")
    output = (proc.stdout or "") + (proc.stderr or "")
    number = _parse_number(name, proc.returncode, output)
    ok = _passed(name, proc.returncode, number)
    note = ""
    # stdout is suppressed unless the check fails or --verbose is passed; the
    # failure's tail is the evidence the successor needs.
    if not ok or verbose:
        tail = "\n".join(output.splitlines()[-12:])
        note = tail
    return CheckResult(name, "PASS" if ok else "FAIL",
                       time.monotonic() - start, number, note=note)


def run_level(groot: Path, level: str, suite: bool, verbose: bool) -> list[CheckResult]:
    """Execute a level: its checks in order, then the count comparison."""
    names = list(LEVELS[level])
    if suite:
        names.append(SUITE_CMD)
    results = [run_check(groot, n, verbose) for n in names]
    smoke = next((r for r in results if r.name == "smoke"), None)
    if smoke is not None:
        results.append(compare_count(groot, smoke.number))
    return results


# --- reporting -------------------------------------------------------------


def _one_line(r: CheckResult) -> str:
    num = ""
    if r.number:
        num = "  [" + ", ".join(f"{k}={v}" for k, v in r.number.items()) + "]"
    note = f"  {r.note}" if r.note and not r.note.startswith("\n") else ""
    return (f"{r.status:4}  {r.name:16} {r.elapsed:6.1f}s{num}{note}").rstrip()


def render_summary(level: str, suite: bool, results: list[CheckResult]) -> str:
    lines = [f"== verification summary (level={level}, suite={'on' if suite else 'off'}) =="]
    for r in results:
        lines.append(_one_line(r))
    failed = [r for r in results if r.status == "FAIL"]
    lines.append("")
    if failed:
        lines.append(f"RESULT: FAIL ({len(failed)} of {len(results)} checks failed)")
    else:
        lines.append(f"RESULT: PASS (all {len(results)} checks green)")
    return "\n".join(lines)


def render_json(level: str, suite: bool, results: list[CheckResult]) -> dict:
    return {
        "level": level,
        "suite": suite,
        "result": "FAIL" if any(r.status == "FAIL" for r in results) else "PASS",
        "checks": [{
            "name": r.name,
            "status": r.status,
            "elapsed": round(r.elapsed, 3),
            "number": r.number,
            "note": r.note,
        } for r in results],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="levels: " + ", ".join(
            f"{k}={','.join(v)}" for k, v in LEVELS.items()))
    ap.add_argument("--level", choices=list(LEVELS), default="rotation")
    ap.add_argument("--suite", action="store_true",
                    help="opt-in: also run the pytest suite (never taken)")
    ap.add_argument("--json", action="store_true",
                    help="emit only a JSON object of the same facts")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="show per-check output even when it passes")
    ap.add_argument("--root", default=".",
                    help="any path inside the project")
    args = ap.parse_args(argv)

    groot = locations.find_project_root(Path(args.root).resolve())
    if groot is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    lock = None
    if args.suite:
        lock, holder = acquire_suite_lock(groot)
        if lock is None:
            if holder is None:
                print("ERR: --suite refused — the suite lock could not be "
                      f"written under {groot / 'sessions'}", file=sys.stderr)
            else:
                print(f"ERR: --suite refused — pid {holder} is a LIVE runner "
                      "holding the suite window (one suite at a time); wait "
                      "for it or ask whoever owns it", file=sys.stderr)
            return 1
        # Information, not a warning. The window rule is a fact the runner
        # should see stated once; it is not a refusal and never blocks.
        print(f"[suite] window acquired, lock {lock} (pid {os.getpid()}); "
              "one suite runner at a time — the window is the Prime's to "
              "grant, and --suite stays opt-in until L4.10 lands")

    try:
        results = run_level(groot, args.level, args.suite, args.verbose)
    finally:
        if lock is not None and lock.exists():
            try:
                lock.unlink()
            except OSError:
                pass

    if args.json:
        print(json.dumps(render_json(args.level, args.suite, results),
                         indent=2))
    else:
        print(render_summary(args.level, args.suite, results))

    return 1 if any(r.status == "FAIL" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
