#!/usr/bin/env python3
"""Race repro v5b — test whether atomic write (write-then-rename) eliminates
concurrent-read-during-write race.  Fixed stale detection: sequential reader
trials with writer's launch-time version captured to avoid false positives
from concurrent subprocess ordering.

Method:
  - Writer thread: rewrites sensor.py continuously, NO handshake.
    Tracks shared `latest_version` atomic counter.
  - Reader: runs N sequential subprocess trials.  Before each, captures
    the writer's latest_version at that instant.  After subprocess returns,
    compares: stale if reader got version < latest_version_at_launch.
  - Both regimes use PYTHONDONTWRITEBYTECODE=1 to isolate write mechanism.
  - Regime 1: Slow non-atomic chunked writes (baseline — provokes race).
  - Regime 2: Atomic writes (write .tmp, fsync, rename — proposed fix).
"""

import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

SENSOR_CODE_TPL = """\
# sensor module — v5b race repro
VERSION = {version}
"""


def non_atomic_chunked_write(path: Path, content: str, chunk_size: int = 128,
                             chunk_delay: float = 0.002, padding_kb: int = 1):
    """Slow chunked write — creates wide read-during-write window."""
    padding = "# " + "x" * (padding_kb * 1024 - len(content) - 4) + "\n"
    full_content = content + padding
    data = full_content.encode("utf-8")
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    try:
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            os.write(fd, chunk)
            os.fsync(fd)
            time.sleep(chunk_delay)
    finally:
        os.close(fd)


def atomic_write(path: Path, content: str):
    """Write .tmp, fsync dir, rename — atomic on same filesystem."""
    tmp = path.with_suffix(".py.tmp")
    tmp.write_text(content)
    fd = os.open(str(tmp.parent), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    tmp.rename(path)
    fd = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(fd)
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
                sv: SharedVersion, use_atomic: bool):
    """Keep rewriting sensor.py, updating shared version atomically."""
    path = sensor_dir / "sensor.py"
    while not stop_event.is_set():
        v = sv.increment()
        content = SENSOR_CODE_TPL.format(version=v)
        if use_atomic:
            atomic_write(path, content)
        else:
            non_atomic_chunked_write(path, content)
        time.sleep(0.001)  # avoid CPU saturation


def run_reader_trial(sensor_dir: Path, trial_num: int,
                     launch_version: int) -> dict:
    """One reader subprocess: import sensor.py fresh, report version."""
    runner_code = """\
import sys, importlib, importlib.util
from pathlib import Path
sd = {sensor_dir!r}
sp = {sensor_py!r}
for key in list(sys.modules.keys()):
    if 'sensor' in key:
        del sys.modules[key]
spec = importlib.util.spec_from_file_location('sensor', sp)
m = importlib.util.module_from_spec(spec)
sys.modules['sensor'] = m
spec.loader.exec_module(m)
print('VERSION=' + str(m.VERSION), flush=True)
""".format(sensor_dir=str(sensor_dir), sensor_py=str(sensor_dir / "sensor.py"))

    runner_path = sensor_dir / f"_runner_{trial_num}.py"
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
        return {"trial": trial_num, "got": None, "error": "timeout",
                "launch_version": launch_version}

    runner_path.unlink(missing_ok=True)

    got = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("VERSION="):
            try:
                got = int(line.split("=", 1)[1])
            except ValueError:
                pass

    has_syntax_error = "SyntaxError" in result.stderr
    return {
        "trial": trial_num,
        "got": got,
        "rc": result.returncode,
        "stderr": result.stderr.strip(),
        "syntax_error": has_syntax_error,
        "launch_version": launch_version,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=500,
                        help="Sequential reader trials per regime")
    parser.add_argument("--inter-trial-delay", type=float, default=0.005,
                        help="Delay between reader trials (default: 0.005)")
    args = parser.parse_args()

    import tempfile
    sensor_dir = Path(tempfile.mkdtemp(prefix="race_repro_v5b_"))
    print(f"Sensor dir: {sensor_dir}")

    # Prime
    atomic_write(sensor_dir / "sensor.py", SENSOR_CODE_TPL.format(version=0))

    def run_regime(label: str, use_atomic: bool) -> dict:
        print(f"\n{label}")
        print(f"{'─' * len(label)}")

        stop = threading.Event()
        sv = SharedVersion()

        # Start writer (fully concurrent — no handshake)
        writer = threading.Thread(
            target=writer_loop,
            args=(sensor_dir, stop, sv, use_atomic),
            daemon=True
        )
        writer.start()

        time.sleep(0.05)  # let writer get ahead

        # Sequential reader trials
        results = []
        for i in range(args.trials):
            launch_v = sv.value
            r = run_reader_trial(sensor_dir, i, launch_v)
            results.append(r)
            time.sleep(args.inter_trial_delay)

        stop.set()
        writer.join(timeout=5)

        # Detect stale: reader got version < launch_version
        stale = []
        parse_fails = []
        for r in results:
            v = r.get("got")
            lv = r.get("launch_version", 0)
            if v is None:
                if r.get("syntax_error"):
                    parse_fails.append(r)
                continue
            if v < lv:
                stale.append(r)

        # Summary
        max_v = max((r["got"] for r in results if r["got"] is not None), default=None)
        print(f"  Total trials: {len(results)}")
        print(f"  Failures (parse errors / timeouts): {len(parse_fails)}")
        print(f"  Max version seen: {max_v}")
        print(f"  Stale imports (got < launch_version): {len(stale)}")
        if stale:
            for s in stale[:10]:
                print(f"    Trial {s['trial']}: launch={s['launch_version']}, got={s['got']} STALE (lag={s['launch_version']-s['got']})")
            if len(stale) > 10:
                print(f"    ... and {len(stale)-10} more")

        return {"stale": len(stale), "parse": len(parse_fails),
                "trials": len(results), "results": results}

    # Regime 1: Non-atomic writes
    r1 = run_regime(
        "REGIME 1: Non-atomic writes (chunked, 2ms delay, fsync per chunk)",
        use_atomic=False
    )

    # Clean
    for p in sensor_dir.glob("*.py"):
        if p.name != "sensor.py":
            p.unlink(missing_ok=True)
    for p in sensor_dir.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    atomic_write(sensor_dir / "sensor.py", SENSOR_CODE_TPL.format(version=0))

    # Regime 2: Atomic writes
    r2 = run_regime(
        "REGIME 2: Atomic writes (write .tmp, fsync dir, rename)",
        use_atomic=True
    )

    # Summary
    s1, p1, n1 = r1["stale"], r1["parse"], r1["trials"]
    s2, p2, n2 = r2["stale"], r2["parse"], r2["trials"]

    print(f"\n{'=' * 50}")
    print("SUMMARY")
    print(f"{'=' * 50}")
    print(f"  Non-atomic: {s1} stale / {p1} parse errors in {n1} trials")
    print(f"  Atomic:     {s2} stale / {p2} parse errors in {n2} trials")
    print(f"  All regimes use PYTHONDONTWRITEBYTECODE=1")

    if s1 > 0 and s2 == 0:
        print("\n  ✓ HYPOTHESIS PROVED: non-atomic writes cause race; atomic writes eliminate it.")
    elif s1 > 0 and s2 > 0:
        reduction = (s1 - s2) / s1 * 100
        print(f"\n  ✗ HYPOTHESIS DISPROVED: race still reproduces with atomic writes ({s2} stale).")
        print(f"    Reduction from non-atomic baseline: {reduction:.0f}%")
    elif s1 == 0:
        print("\n  ∘ INCONCLUSIVE: could not reproduce race with non-atomic writes.")
    else:
        print(f"\n  ∘ INCONCLUSIVE: unhandled case (s1={s1}, s2={s2})")

    return 0


if __name__ == "__main__":
    main()