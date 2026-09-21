#!/usr/bin/env python3
"""mem_cap.py -- ONE memory cap for every launched child (SM.112,
hypothesis:l4-every-launched-kid-parent-and-workflow-stage-runs-under-a-memory-
cap-so-a-runaway-dies-alone-and-by-name-never-a-global-oom)."""
from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys

_PROBE: "bool | None" = None
_SUFFIX = {"K": 1024, "M": 1024 ** 2, "G": 1024 ** 3, "T": 1024 ** 4}


def resolve_memory_cap(cfg: dict) -> "str | None":
    """`spawn.memory_max`: absent -> '4G'; null/'none'/'' -> None; else as-is."""
    spawn = (cfg or {}).get("spawn") or {}
    if "memory_max" not in spawn:
        return "4G"
    val = spawn.get("memory_max")
    if val is None or str(val).strip().lower() in ("", "none", "null"):
        return None
    return str(val)


def _as_bytes(spec: str) -> int:
    """`4G` -> bytes, for `prlimit --as`."""
    s = str(spec).strip().upper()
    return int(float(s[:-1]) * _SUFFIX[s[-1]]) if s[-1] in _SUFFIX else int(s)


def systemd_run_usable() -> bool:
    """Probe ONCE per process: launchability is not enforcement. Launch a REAL
    allocation past a REAL tiny cap and require the observed SIGKILL -- on
    boxes whose swap absorbs the overage, or that swallow the property, the
    probe must say False so `wrap_argv` falls through to prlimit."""
    global _PROBE
    if _PROBE is None:
        _PROBE = False
        if shutil.which("systemd-run"):
            try:
                _PROBE = subprocess.run(
                    ["systemd-run", "--user", "--scope", "-q",
                     "--property=MemoryMax=64M",
                     "--property=MemorySwapMax=0", "--", sys.executable,
                     "-c", "x=bytearray(256*1024*1024)"],
                    capture_output=True, timeout=30).returncode == -signal.SIGKILL
            except (OSError, subprocess.SubprocessError):
                _PROBE = False
    return _PROBE


def wrap_argv(argv: list, cap: "str | None") -> list:
    """`cap is None` -> the SAME argv object, unwrapped; else systemd-run when
    usable, else the prlimit fallback."""
    if cap is None:
        return argv
    if systemd_run_usable():
        return ["systemd-run", "--user", "--scope", "-q",
                f"--property=MemoryMax={cap}",
                "--property=MemorySwapMax=0", "--", *argv]
    return ["prlimit", f"--as={_as_bytes(cap)}", "--", *argv]


def is_cap_death(returncode, cap, output: str = "") -> bool:
    """The cap's kill: cgroup SIGKILL (negative rc) or RLIMIT_AS exhaustion
    (MemoryError / out of memory). A wall timeout raises before this."""
    if cap is None or returncode is None:
        return False
    if returncode < 0:
        return True
    low = (output or "").lower()
    return "memoryerror" in low or "out of memory" in low


def reaped_cap_death(pid: int, cap: "str | None") -> bool:
    """SIGKILL on a dead child, observable only while it is still this
    process's child. Not our child -> False, never a guess."""
    if cap is None or pid <= 0:
        return False
    try:
        _p, status = os.waitpid(pid, os.WNOHANG)
    except (ChildProcessError, OSError):
        return False
    return os.WIFSIGNALED(status) and os.WTERMSIG(status) == signal.SIGKILL

if __name__ == "__main__":
    import argparse
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
