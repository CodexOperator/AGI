#!/usr/bin/env python3
"""Race repro v5 — test whether atomic write (write-then-rename) eliminates
the concurrent-read-during-write race that v4 revealed as the true cause.

hypothesis:a01-390e52ad-e286a2 claimed stale-.pyc was the mechanism.  v4
disproved that: -B made MORE stale reads (4 vs 2) and MORE parse errors
(9 vs 4), because without bytecode caching every import re-reads the .py
source and is MORE vulnerable to catching a partial write.

The v4 conclusion: the true fix is file-level atomicity in the writer.
This experiment tests that claim directly.

Method:
  - Same slow chunked non-atomic writer as v4 (128B chunks, 2ms delay,
    1KB padding, fsync per chunk) to create wide race window.
  - Concurrent reader subprocesses (no handshake — true concurrency).
  - ALL regimes use PYTHONDONTWRITEBYTECODE=1 to isolate write mechanism
    from any bytecode cache effect.
  - Regime 1: Non-atomic writes (direct truncate+write in chunks).
  - Regime 2: Atomic writes (write to .tmp, fsync, rename).

Expected: non-atomic shows stale reads + parse errors; atomic shows zero.
"""

import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

SENSOR_CODE_TPL = """\
# sensor module — v5 race repro
VERSION = {version}
"""


def non_atomic_chunked_write(path: Path, content: str, chunk_size: int = 128,
                             chunk_delay: float = 0.002, padding_kb: int = 1):
    """Simulate a slow non-atomic write by truncating, then writing in
    small chunks with delays.  This creates a wide read-during-write window
    of the kind that happens when one agent is mid-edit while another runs
    tests (the goal:g4.1 scenario)."""
    # Add padding to make the race window easier to hit
    padding = "# " + "x" * (padding_kb * 1024 - len(content) - 4) + "\n"
    full_content = content + padding
    data = full_content.encode("utf-8")

    # Non-atomic: truncate then write chunks
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    try:
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            os.write(fd, chunk)
            os.fsync(fd)  # make it durable (slow)
            time.sleep(chunk_delay)
    finally:
        os.close(fd)


def atomic_write(path: Path, content: str):
    """Write THEN rename — atomic on the same filesystem.  The reader
    always sees a complete file or the previous complete file."""
    tmp = path.with_suffix(".py.tmp")
    tmp.write_text(content)
    # fsync the tmp file's directory entry too
    fd = os.open(str(tmp.parent), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    tmp.rename(path)
    # fsync the target directory
    fd = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def writer_loop(sensor_dir: Path, stop_event: threading.Event,
                use_atomic: bool = False):
    """Keep rewriting sensor.py as fast as realistic, no handshake."""
    path = sensor_dir / "sensor.py"
    v = 0
    while not stop_event.is_set():
        v += 1
        content = SENSOR_CODE_TPL.format(version=v)
        if use_atomic:
            atomic_write(path, content)
        else:
            non_atomic_chunked_write(path, content)
        time.sleep(0.001)  # small gap so CPU isn't saturated


def run_reader_trial(sensor_dir: Path, trial_num: int) -> dict:
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

    result = subprocess.run(
        [sys.executable, str(runner_path)],
        capture_output=True, text=True, timeout=10, env=env,
    )
    runner_path.unlink(missing_ok=True)

    got = None
    parse_error = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("VERSION="):
            try:
                got = int(line.split("=", 1)[1])
            except ValueError:
                pass

    # Check stderr for parse errors (SyntaxError, etc. = caught partial write)
    has_syntax_error = "SyntaxError" in result.stderr or "ParseError" in result.stderr
    is_crash = result.returncode != 0 and not has_syntax_error

    return {
        "trial": trial_num,
        "got": got,
        "rc": result.returncode,
        "stderr": result.stderr.strip(),
        "syntax_error": has_syntax_error,
    }


def detect_stale_imports(results: list) -> tuple:
    """Return (stale_events, parse_errors).  A stale import is when the
    version DECLINES from the max seen so far — the source moved forward
    but the import served the past.  A parse error is a SyntaxError from
    reading a partial write."""
    stale_events = []
    parse_errors = []
    max_seen = 0
    for r in results:
        v = r.get("got")
        if v is None:
            if r.get("syntax_error"):
                parse_errors.append(r)
            continue
        if v < max_seen:
            stale_events.append(r)
        max_seen = max(max_seen, v)
    return stale_events, parse_errors


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=500,
                        help="Reader trials per regime (default: 500)")
    parser.add_argument("--duration", type=float, default=5.0,
                        help="Duration per regime in seconds (default: 5.0)")
    parser.add_argument("--reader-count", type=int, default=2,
                        help="Concurrent reader threads (default: 2)")
    args = parser.parse_args()

    sensor_dir = Path(tempfile.mkdtemp(prefix="race_repro_v5_"))
    print(f"Sensor dir: {sensor_dir}")

    # Prime
    atomic_write(sensor_dir / "sensor.py", SENSOR_CODE_TPL.format(version=0))

    def run_regime(label: str, use_atomic: bool) -> tuple:
        print(f"\n{label}")
        print(f"{'─' * len(label)}")

        stop = threading.Event()

        # Start writer
        writer = threading.Thread(
            target=writer_loop,
            args=(sensor_dir, stop, use_atomic),
            daemon=True
        )
        writer.start()

        # Run concurrent readers for `duration` seconds
        results = []
        lock = threading.Lock()
        trial_counter = [0]

        def reader_worker():
            while not stop.is_set():
                with lock:
                    tn = trial_counter[0]
                    trial_counter[0] += 1
                r = run_reader_trial(sensor_dir, tn)
                with lock:
                    results.append(r)

        readers = []
        for _ in range(args.reader_count):
            t = threading.Thread(target=reader_worker, daemon=True)
            t.start()
            readers.append(t)

        time.sleep(args.duration)
        stop.set()

        writer.join(timeout=5)
        for t in readers:
            t.join(timeout=5)

        stale, parse_fails = detect_stale_imports(results)

        print(f"  Total imports: {len(results)}")
        print(f"  Failures (parse errors): {len(parse_fails)}")
        versions = [r["got"] for r in results if r["got"] is not None]
        print(f"  Max version seen: {max(versions) if versions else 'N/A'}")
        print(f"  Stale imports (version regressions): {len(stale)}")

        if stale:
            for s in stale[:5]:  # show first 5
                print(f"    Trial {s['trial']}: got={s['got']} STALE")
            if len(stale) > 5:
                print(f"    ... and {len(stale)-5} more")

        return len(stale), len(parse_fails), len(results)

    # Regime 1: Non-atomic writes (baseline — should show race)
    s1, p1, n1 = run_regime(
        "REGIME 1: Non-atomic writes (chunked, 2ms delay, fsync per chunk)",
        use_atomic=False
    )

    # Clean and re-prime
    for p in sensor_dir.glob("*.py"):
        if p.name != "sensor.py":
            p.unlink(missing_ok=True)
    for p in sensor_dir.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    atomic_write(sensor_dir / "sensor.py", SENSOR_CODE_TPL.format(version=0))

    # Regime 2: Atomic writes (write-then-rename — proposed fix)
    s2, p2, n2 = run_regime(
        "REGIME 2: Atomic writes (write-then-rename, fsync+rename)",
        use_atomic=True
    )

    # Summary
    print(f"\n{'=' * 50}")
    print("SUMMARY")
    print(f"{'=' * 50}")
    print(f"  Non-atomic: {s1} stale / {p1} parse errors in {n1} imports")
    print(f"  Atomic:     {s2} stale / {p2} parse errors in {n2} imports")

    if s1 > 0 and (s2 == 0 and p2 == 0):
        print("\n  ✓ HYPOTHESIS PROVED: non-atomic writes cause the race; atomic writes eliminate it.")
    elif s1 > 0 and s2 > 0:
        print("\n  ✗ HYPOTHESIS DISPROVED: race still reproduces with atomic writes — not purely a write-atomicity problem.")
    elif s1 == 0:
        print("\n  ∘ INCONCLUSIVE: could not reproduce race with non-atomic writes (may need tighter timing).")
    else:
        print(f"\n  ∘ INCONCLUSIVE: unhandled case (s1={s1}, s2={s2})")

    return 0


if __name__ == "__main__":
    import tempfile
    main()