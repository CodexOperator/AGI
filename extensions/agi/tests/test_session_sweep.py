"""goal:g7.16.1.5.3.2.1 -- session-sweep.sh judges idleness by FILE mtimes.

heal's sweep homes a finished round's session dir: old files inside freshly
created directories. The sweep's `recent` test counted directory mtimes, so
such a dir read "recent" for the whole idle window and stayed on the RAM disk.
Runs the REAL script on a tmp tree through a fixture config:guard node; the
live box's cells are never read.
"""
import os
import subprocess
import time
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "guard" / "session-sweep.sh"


def _box(tmp_path: Path) -> tuple[Path, Path, dict]:
    main = tmp_path / "main"
    cold = tmp_path / "cold"
    (main / ".agi" / "sessions").mkdir(parents=True)
    cold.mkdir()
    node = tmp_path / "guard.md"
    node.write_text(
        "# guard\n```sh guard.env\n"
        f"GUARD_RAM_MAIN_fixturebox={main}\n"
        f"GUARD_RAM_DIR_fixturebox={tmp_path}\n"
        f"GUARD_AGI_SESSIONS_ARCHIVE_fixturebox={cold}\n"
        "GUARD_SWEEP_IDLE_MIN_fixturebox=120\n```\n")
    env = dict(os.environ, GUARD_ENV_NODE=str(node), GUARD_BOX="fixturebox")
    return main, cold, env


def _old(p: Path, hours: float = 3) -> None:
    t = time.time() - hours * 3600
    os.utime(p, (t, t))


def test_a_homed_dir_with_old_files_and_fresh_dirs_moves_cold(tmp_path):
    main, cold, env = _box(tmp_path)
    homed = main / ".agi" / "sessions" / "iter-701"
    (homed / "a00-x").mkdir(parents=True)      # fresh DIRECTORY mtimes
    for f in (homed / "manifest.json", homed / "a00-x" / "agent.json"):
        f.write_text("{}\n")
        _old(f)                                 # every FILE is 3 h old
    live = main / ".agi" / "sessions" / "iter-702"
    live.mkdir()
    (live / "output.log").write_text("still writing\n")   # one fresh FILE
    r = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-400:]
    assert homed.is_symlink(), "old files in fresh dirs = idle -> moved cold"
    assert (cold / "iter-701" / "a00-x" / "agent.json").read_text() == "{}\n"
    assert live.is_dir() and not live.is_symlink(), "a fresh file keeps its dir"
    assert "agi: 1 moved" in r.stdout


def test_recent_never_reads_a_directory_mtime():
    """Falsifier 2: every idle test in the script is a FILE test."""
    lines = [l for l in SCRIPT.read_text().splitlines() if "-newermt" in l]
    assert lines and all("-type f" in l for l in lines), lines
