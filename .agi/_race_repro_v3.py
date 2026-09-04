#!/usr/bin/env python3
"""Stale-.pyc race reproducer — v3, truly concurrent.

The handshake (writer-signals-reader) makes them sequential and eliminates
the race.  In the real g4.1 scenario the writer and reader are fully
concurrent — one edits the .py file at the same clock instant the other
imports it.

Approach:
  - Writer loop: rewrite sensor.py continuously, NO handshake.
  - Reader loop: in parallel, repeatedly run a subprocess that imports
    sensor.py and prints the version it got.
  - Check: did a subsequent reader process get an OLDER version than a
    previous reader process got?  That is the definition of a stale import
    — the source file moved forward, but the import served the past.

We also check the SIMPLER case: every write renames in place (the `atomic_write`
approach).  This guarantees the reader always gets a complete file, but the
.mtime changes, so Python *should* recompile.  We will see if it does.
"""

import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

SENSOR_CODE_TPL = """\
# sensor module
VERSION = {version}
"""


def atomic_write(path: Path, content: str):
    tmp = path.with_suffix(".py.tmp")
    tmp.write_text(content)
    tmp.rename(path)  # atomic on same filesystem


def direct_write(path: Path, content: str):
    """Write DIRECTLY (non-atomic) — creates real read-during-write window."""
    path.write_text(content)


def writer_loop(sensor_dir: Path, stop_event: threading.Event, interval: float = 0.0005,
                atomic: bool = True):
    """Keep rewriting sensor.py as fast as possible (no handshake)."""
    path = sensor_dir / "sensor.py"
    write_fn = atomic_write if atomic else direct_write
    v = 0
    while not stop_event.is_set():
        v += 1
        write_fn(path, SENSOR_CODE_TPL.format(version=v))
        time.sleep(interval)  # small gap so CPU isn't saturated


def run_reader_trial(sensor_dir: Path, trial_num: int, no_bytecode: bool) -> dict:
    """One reader subprocess: import sensor.py fresh, report version."""
    runner_code = """\
import sys, importlib, importlib.util
from pathlib import Path
sd = {sensor_dir!r}
sp = {sensor_py!r}
# Clear sys.modules so we get a fresh import
for key in list(sys.modules.keys()):
    if 'sensor' in key:
        del sys.modules[key]
# Do NOT clear __pycache__ — we want to see if the old .pyc is served
spec = importlib.util.spec_from_file_location('sensor', sp)
m = importlib.util.module_from_spec(spec)
sys.modules['sensor'] = m
spec.loader.exec_module(m)
print('VERSION=' + str(m.VERSION), flush=True)
""".format(sensor_dir=str(sensor_dir), sensor_py=str(sensor_dir / "sensor.py"))

    runner_path = sensor_dir / f"_runner_{trial_num}.py"
    runner_path.write_text(runner_code)

    env = os.environ.copy()
    if no_bytecode:
        env["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [sys.executable, str(runner_path)],
        capture_output=True, text=True, timeout=10, env=env,
    )
    runner_path.unlink(missing_ok=True)

    got = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("VERSION="):
            try:
                got = int(line.split("=", 1)[1])
            except ValueError:
                pass

    return {"trial": trial_num, "got": got}


def detect_stale_imports(results: list) -> list:
    """A stale import is when trial N gets a LOWER version than trial N-M
    (M >= 1), meaning the source file was at a higher version before and
    a later import somehow regressed — classic stale .pyc.
    
    Since the writer monotonically increments, any non-monotonic version
    sequence is evidence of stale caching."""
    stale_events = []
    max_seen = 0
    for r in results:
        v = r.get("got")
        if v is None:
            continue
        if v < max_seen:
            stale_events.append(r)
        max_seen = max(max_seen, v)
    return stale_events


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=30,
                        help="Reader trials per regime")
    parser.add_argument("--writer-interval", type=float, default=0.0005,
                        help="Gap between writer writes (seconds)")
    parser.add_argument("--non-atomic", action="store_true",
                        help="Use direct (non-atomic) writes to create read-during-write window")
    args = parser.parse_args()

    sensor_dir = Path(tempfile.mkdtemp(prefix="race_repro_v3_"))
    print(f"Sensor dir: {sensor_dir}")

    # Prime
    atomic_write(sensor_dir / "sensor.py", SENSOR_CODE_TPL.format(version=0))

    def run_regime(no_bytecode: bool, label: str, atomic: bool = True) -> tuple:
        stop = threading.Event()
        writer = threading.Thread(
            target=writer_loop,
            args=(sensor_dir, stop, args.writer_interval, atomic),
            daemon=True
        )
        writer.start()
        time.sleep(0.01)  # let writer get ahead

        results = []
        for i in range(args.trials):
            r = run_reader_trial(sensor_dir, i, no_bytecode)
            results.append(r)

        stop.set()
        writer.join(timeout=5)

        stale = detect_stale_imports(results)

        print(f"\n{label}")
        print(f"{'─' * len(label)}")
        versions = [r["got"] for r in results]
        version_str = ", ".join(str(v) if v is not None else "?" for v in versions)
        print(f"  Versions: {version_str}")
        for s in stale:
            print(f"  → Trial {s['trial']}: version={s['got']} is STALE (declines from earlier max)")
        print(f"  Stale imports: {len(stale)}/{args.trials}")
        return len(stale), results

    atomic = not args.non_atomic
    # Regime 1: default bytecode caching
    s1, r1 = run_regime(no_bytecode=False,
                        label="REGIME 1: Default bytecode caching (no -B)",
                        atomic=atomic)

    # Wipe __pycache__ between regimes
    for p in Path(sensor_dir).rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)

    # Regime 2: PYTHONDONTWRITEBYTECODE=1
    s2, r2 = run_regime(no_bytecode=True,
                        label="REGIME 2: PYTHONDONTWRITEBYTECODE=1 (no cache)",
                        atomic=atomic)

    # Summary
    print(f"\n{'=' * 50}")
    print("SUMMARY")
    print(f"{'=' * 50}")
    print(f"  Default (with cache): {s1}/{args.trials} stale imports")
    print(f"  -B (no cache):        {s2}/{args.trials} stale imports")

    if s1 > 0 and s2 == 0:
        print("\n  ✓ HYPOTHESIS PROVED: stale .pyc causes the race, -B eliminates it.")
    elif s1 > 0 and s2 > 0:
        print("\n  ✗ HYPOTHESIS DISPROVED: race still reproduces with -B — not .pyc-driven.")
    elif s1 == 0:
        print("\n  ∘ INCONCLUSIVE: could not reproduce the race.")
    else:
        print(f"\n  ∘ INCONCLUSIVE: unhandled case (s1={s1}, s2={s2})")

    return 0


if __name__ == "__main__":
    import tempfile
    main()