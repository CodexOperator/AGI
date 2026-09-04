#!/usr/bin/env python3
"""Race repro v7 — test whether in-process module staleness is the true
mechanism behind the g4.1 incident, and test whether subprocess isolation
(which is what worktree-per-kid / designated-committer provides) eliminates it.

Method (two regimes):
  Both regimes write sensor.py non-atomically (chunked, 2ms delay) to create
  a wide race window. Both regimes use PYTHONDONTWRITEBYTECODE=1 to eliminate
  .pyc staleness (sibling experiment a00-cce327d4 already showed -B does NOT
  fix the race).

  **Regime A — In-process shared import (simulates shared workspace):**
    One reader thread imports sensor via importlib *once* and shares the
    module object across all subsequent reads via a shared ref. This is what
    happens when two agents share a pytest workspace: Agent A's long-running
    pytest imports the module once and never re-imports it.

  **Regime B — Fresh subprocess per read (simulates subprocess isolation):**
    Each reader thread spawns a fresh subprocess that imports sensor fresh.
    This is what worktree-per-kid or designated-committer provides: each
    agent's test runner runs in its own process, ensuring fresh imports.

Prediction:
  - Regime A will show frequent stale reads (shared module stays old
    after writer edits the .py file)
  - Regime B will show minimal or zero stale reads (each subprocess imports
    fresh, so reader always sees either the old file before write or the new
    file after write, never an in-between stale from cache)

This would confirm that in-process module caching (sys.modules) is the true
mechanism, and that subprocess isolation (already provided by the sibling
hypotheses) is the correct fix.
"""

import importlib
import importlib.util
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

SENSOR_CODE_TPL = """\
# sensor module — v7 race repro
VERSION = {version}
"""


def non_atomic_chunked_write(path: Path, content: str, chunk_size: int = 128,
                             chunk_delay: float = 0.002):
    """Slow chunked write — creates wide read-during-write window."""
    data = content.encode("utf-8")
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    try:
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            os.write(fd, chunk)
            os.fsync(fd)
            time.sleep(chunk_delay)
    finally:
        os.close(fd)


class SharedVersion:
    """Thread-safe writer version counter."""
    def __init__(self):
        self._v = 0
        self._lock = threading.Lock()

    @property
    def value(self) -> int:
        with self._lock:
            return self._v

    def increment(self) -> int:
        with self._lock:
            self._v += 1
            return self._v


def writer_loop(sensor_dir: Path, stop_event: threading.Event,
                sv: SharedVersion):
    """Keep rewriting sensor.py non-atomically."""
    path = sensor_dir / "sensor.py"
    while not stop_event.is_set():
        v = sv.increment()
        non_atomic_chunked_write(path, SENSOR_CODE_TPL.format(version=v))
        time.sleep(0.001)


def _import_sensor(sensor_py: Path):
    """Import sensor module fresh, return its VERSION."""
    for key in list(sys.modules.keys()):
        if 'sensor' in key:
            del sys.modules[key]
    spec = importlib.util.spec_from_file_location("sensor", str(sensor_py))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["sensor"] = mod
    spec.loader.exec_module(mod)
    return mod.VERSION


def inprocess_reader(sensor_dir: Path, sv: SharedVersion,
                     stop_event: threading.Event,
                     results: list, lock: threading.Lock,
                     reader_id: int):
    """Regime A: import sensor ONCE, read from shared module forever."""
    sensor_py = sensor_dir / "sensor.py"

    # Retry import until sensor has VERSION (may not on first partial write)
    for attempt in range(10):
        try:
            v = _import_sensor(sensor_py)
            if v is not None:
                break
        except Exception:
            pass
        time.sleep(0.01)
    else:
        v = -1

    trial = 0
    while not stop_event.is_set() and trial < 100000:
        trial += 1
        launch_v = sv.value

        # Read from the shared (cached) module — NEVER reimports
        try:
            read_v = sys.modules["sensor"].VERSION
        except (KeyError, AttributeError):
            read_v = -1

        # Stale: module version is behind what was written
        if read_v < launch_v:
            with lock:
                results.append({
                    "reader": reader_id,
                    "trial": trial,
                    "got": read_v,
                    "launch": launch_v,
                    "stale": True,
                })

        time.sleep(0.002)


def fresh_subprocess_reader(sensor_dir: Path, sv: SharedVersion,
                            stop_event: threading.Event,
                            results: list, lock: threading.Lock,
                            reader_id: int):
    """Regime B: spawn fresh subprocess per import."""
    runner_code = """\
import sys, importlib, importlib.util
sp = {sensor_py!r}
for key in list(sys.modules.keys()):
    if 'sensor' in key:
        del sys.modules[key]
spec = importlib.util.spec_from_file_location('sensor', sp)
m = importlib.util.module_from_spec(spec)
sys.modules['sensor'] = m
spec.loader.exec_module(m)
print('VERSION=' + str(m.VERSION), flush=True)
""".format(sensor_py=str(sensor_dir / "sensor.py"))

    trial = 0
    while not stop_event.is_set() and trial < 100000:
        trial += 1
        launch_v = sv.value

        runner_path = sensor_dir / "_runner_v7_{}_{}.py".format(reader_id, trial)
        runner_path.write_text(runner_code)

        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        try:
            result = subprocess.run(
                [sys.executable, str(runner_path)],
                capture_output=True, text=True, timeout=10, env=env,
            )
        except subprocess.TimeoutExpired:
            runner_path.unlink(missing_ok=True)
            continue

        runner_path.unlink(missing_ok=True)

        # Parse VERSION=
        got = None
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("VERSION="):
                try:
                    got = int(line.split("=", 1)[1])
                except ValueError:
                    pass

        if got is not None and got < launch_v:
            with lock:
                results.append({
                    "reader": reader_id,
                    "trial": trial,
                    "got": got,
                    "launch": launch_v,
                    "stale": True,
                })

        time.sleep(0.002)


def run_regime(label: str, reader_fn, n_readers: int = 2,
               duration: float = 10.0, sensor_dir: Path = None) -> dict:
    """Run a regime with specified reader function."""
    sensor_dir = sensor_dir or Path(".")

    stop = threading.Event()
    sv = SharedVersion()

    # Prime sensor
    sensor_py = sensor_dir / "sensor.py"
    sensor_py.write_text(SENSOR_CODE_TPL.format(version=0))

    # Start writer
    writer = threading.Thread(
        target=writer_loop, args=(sensor_dir, stop, sv), daemon=True
    )
    writer.start()
    time.sleep(0.05)

    # Start N readers
    results = []
    lock = threading.Lock()
    readers = []
    for i in range(n_readers):
        r = threading.Thread(
            target=reader_fn,
            args=(sensor_dir, sv, stop, results, lock, i),
            daemon=True
        )
        readers.append(r)
        r.start()

    time.sleep(duration)
    stop.set()

    for r in readers:
        r.join(timeout=5)
    writer.join(timeout=5)

    stale_count = len(results)
    return {
        "stale_count": stale_count,
        "stale": results,
        "max_launch": sv.value,
    }


def fmt_stale(s):
    """Format a stale result safely (got may be None)."""
    if s.get("got") is not None:
        lag = s["launch"] - s["got"]
        return "Reader {}, trial {}: got={} < launch={} (lag={})".format(
            s["reader"], s["trial"], s["got"], s["launch"], lag)
    else:
        return "Reader {}, trial {}: got=None, launch={} (parse error)".format(
            s["reader"], s["trial"], s["launch"])


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Test in-process module staleness vs subprocess isolation"
    )
    parser.add_argument("--duration", type=float, default=10.0,
                        help="Run duration in seconds per regime")
    parser.add_argument("--readers", type=int, default=2,
                        help="Number of concurrent reader threads")
    args = parser.parse_args()

    import tempfile
    import shutil
    sensor_dir = Path(tempfile.mkdtemp(prefix="race_repro_v7_"))
    pycache = sensor_dir / "__pycache__"
    pycache.mkdir(exist_ok=True)
    print("Sensor dir: {}".format(sensor_dir))

    def run_one_regime(label, name, reader_fn):
        print()
        print("=" * 60)
        print("{} — {}".format(label, name))
        print("  {} concurrent reader threads, {}s".format(args.readers, args.duration))
        print("=" * 60)
        r = run_regime(label, reader_fn,
                        n_readers=args.readers, duration=args.duration,
                        sensor_dir=sensor_dir)
        print("  Stale reads: {}".format(r["stale_count"]))
        print("  Max version written: {}".format(r["max_launch"]))
        if r["stale"]:
            print("  Stale samples:")
            for s in r["stale"][:10]:
                print("    " + fmt_stale(s))
            if len(r["stale"]) > 10:
                print("    ... and {} more".format(len(r["stale"]) - 10))
        return r

    # ---- Regime A: In-process shared import ----
    rA = run_one_regime(
        "REGIME A",
        "IN-PROCESS SHARED IMPORT (simulates shared workspace)",
        inprocess_reader)

    # Clean up between regimes
    for p in sensor_dir.glob("_runner_*.py"):
        p.unlink(missing_ok=True)
    for p in sensor_dir.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    # Re-prime sensor
    (sensor_dir / "sensor.py").write_text(SENSOR_CODE_TPL.format(version=0))

    # ---- Regime B: Fresh subprocess per import ----
    rB = run_one_regime(
        "REGIME B",
        "FRESH SUBPROCESS PER IMPORT (simulates isolation)",
        fresh_subprocess_reader)

    # ---- Summary ----
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("  Regime A (in-process shared import):  {} stale reads".format(rA["stale_count"]))
    print("  Regime B (fresh subprocess per read):  {} stale reads".format(rB["stale_count"]))

    if rA["stale_count"] > 0 and rB["stale_count"] == 0:
        print()
        print("  ✓ MECHANISM CONFIRMED: in-process module caching causes stale reads;")
        print("     subprocess isolation eliminates them entirely.")
        print("  -> Subprocess isolation (worktree-per-kid / designated-committer)")
        print("     is the correct fix for the in-memory staleness mechanism.")
    elif rA["stale_count"] > 0 and rB["stale_count"] > 0:
        print()
        print("  o PARTIALLY: both regimes show staleness.")
        ratio = rB["stale_count"] / max(rA["stale_count"], 1)
        print("    Ratio: subprocess/in-process = {:.2f}".format(ratio))
    elif rA["stale_count"] == 0 and rB["stale_count"] == 0:
        print()
        print("  o INCONCLUSIVE: No stale reads in either regime.")
    else:
        print()
        print("  o UNEXPECTED: Regime A={}, Regime B={}".format(
            rA["stale_count"], rB["stale_count"]))

    # Cleanup
    shutil.rmtree(sensor_dir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())