#!/usr/bin/env python3
"""mem_cap.py -- ONE memory cap for every launched child (SM.112,
hypothesis:l4-every-launched-kid-parent-and-workflow-stage-runs-under-a-memory-
cap-so-a-runaway-dies-alone-and-by-name-never-a-global-oom)."""
from __future__ import annotations

import os
import pathlib
import shutil
import signal
import stat
import subprocess
import sys
import tempfile

_PROBE: "bool | None" = None
_SUFFIX = {"K": 1024, "M": 1024 ** 2, "G": 1024 ** 3, "T": 1024 ** 4}

#: The probe's scope carries a FIXED unit name so its failed unit can be
#: reset by name afterwards. An anonymous `run-<random>.scope` cannot be, and
#: systemd keeps every failed transient unit resident until `reset-failed` --
#: measured 1422 failed `run-*.scope` units against 1784 cgroup OOM kills on
#: encryption-town in 6 days, one pair per spawn.
_PROBE_UNIT = "agi-memcap-probe"

#: The cache lives in a dir of this name under the per-user runtime dir. Named
#: because the DIR, not the file, is the unit of privacy:
#: `hypothesis:mem-cap-probe-cache-is-private-and-atomic`.
_CACHE_DIR_NAME = "agi-memcap"


def _normalise_cap(val) -> "str | None":
    """None / 'none' / 'null' / '' -> None; else the value verbatim."""
    if val is None or str(val).strip().lower() in ("", "none", "null"):
        return None
    return str(val)


def resolve_memory_cap(cfg: dict, override: "str | None" = None) -> "str | None":
    """`spawn.memory_max`: absent -> '4G'; null/'none'/'' -> None; else as-is.

    `override` (hypothesis:lm-dispatch-memory-override-feeds-agi-batch-
    scheduling) is a per-invocation cap: when it is not None it wins over the
    config value, normalised the same way, and `cfg` is never mutated -- the
    override is request-scoped, not written back to disk.
    """
    if override is not None:
        return _normalise_cap(override)
    spawn = (cfg or {}).get("spawn") or {}
    if "memory_max" not in spawn:
        return "4G"
    return _normalise_cap(spawn.get("memory_max"))


def _as_bytes(spec: str) -> int:
    """`4G` -> bytes, for `prlimit --as`."""
    s = str(spec).strip().upper()
    return int(float(s[:-1]) * _SUFFIX[s[-1]]) if s[-1] in _SUFFIX else int(s)


def _boot_id() -> str:
    """The running kernel's boot id, so a cached probe verdict is never read
    across a reboot (cgroup support, swap and the user manager can all differ
    on the next boot)."""
    try:
        return pathlib.Path(
            "/proc/sys/kernel/random/boot_id").read_text().strip()
    except OSError:
        return ""


def _private_dir(path: pathlib.Path) -> "pathlib.Path | None":
    """A cache dir WE own, mode 0700, or None. A dir another user pre-created
    at a predictable `/tmp` name is refused outright -- otherwise the file
    checks below trust a verdict planted for us. An unwritable or foreign
    cache costs a re-probe, never a wrong verdict."""
    try:
        path.mkdir(parents=True, exist_ok=True, mode=0o700)
        if os.lstat(path).st_uid != os.geteuid():
            return None
        os.chmod(path, 0o700)
    except OSError:
        return None
    return path


def _probe_cache_path() -> "pathlib.Path | None":
    """Where the cross-process probe verdict lives. `AGI_MEMCAP_CACHE` (an
    explicit file path, for tests) wins; else a private dir under the
    per-user runtime dir (tmpfs, cleared on boot); else `/tmp`.
    None means "no cache is writable" -- the probe then runs per process, the
    old behaviour, rather than failing."""
    env = os.environ.get("AGI_MEMCAP_CACHE")
    if env:
        return pathlib.Path(env)
    run = os.environ.get("XDG_RUNTIME_DIR")
    base = pathlib.Path(run) if run else pathlib.Path("/tmp")
    d = _private_dir(base / _CACHE_DIR_NAME)
    return None if d is None else d / "probe"


def _trusted_cache_file(path: pathlib.Path) -> "pathlib.Path | None":
    """The cache file only if it is a REGULAR file we own. A symlink at a
    predictable path is not followed (a planted link would otherwise both
    read a foreign verdict and redirect our write), and a file another user
    owns is not trusted."""
    try:
        st = os.lstat(path)
    except OSError:
        return None
    if not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid():
        return None
    return path


def _read_cached_probe() -> "bool | None":
    """The verdict cached for THIS boot, or None (absent, stale, foreign,
    partial or corrupt). A body that is not exactly `0` or `1` is a torn or
    planted write and is re-probed, never read as a `False`."""
    path = _probe_cache_path()
    if path is None:
        return None
    path = _trusted_cache_file(path)
    if path is None:
        return None
    try:
        boot, _, val = path.read_text().strip().partition(" ")
    except OSError:
        return None
    if val not in ("0", "1") or boot != _boot_id():
        return None
    return val == "1"


def _write_cached_probe(val: bool) -> None:
    """Best-effort and ATOMIC: a temp file in the same dir (0600 by
    construction) then `os.replace`, so a concurrent reader sees the old
    verdict or the new one, never a half-written one. An unwritable cache
    costs a re-probe, never a failure."""
    path = _probe_cache_path()
    if path is None:
        return
    try:
        fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".")
    except OSError:
        return
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(f"{_boot_id()} {'1' if val else '0'}\n")
        os.replace(tmp, path)
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def _reset_probe_unit() -> None:
    """Drop the probe scope's FAILED unit so `systemd --user` does not carry
    it for the life of the session. The probe's whole contract is an observed
    SIGKILL, so the unit ALWAYS ends up failed -- leaving it resident is the
    leak, not the kill."""
    try:
        subprocess.run(
            ["systemctl", "--user", "reset-failed", f"{_PROBE_UNIT}.scope"],
            capture_output=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        pass


def systemd_run_usable() -> bool:
    """Launchability is not enforcement: launch a REAL allocation past a REAL
    tiny cap and require the observed SIGKILL -- on boxes whose swap absorbs
    the overage, or that swallow the property, the probe must say False so
    `wrap_argv` falls through to prlimit.

    Probed ONCE PER BOOT, not once per process. The verdict is a property of
    the box, not of the caller, and every `dispatch.py` / `heal.py` / cron
    invocation is a fresh process: probing per process meant one deliberate
    256 MB allocation and one cgroup OOM kill PER SPAWN, each leaving a failed
    transient scope behind. `AGI_MEMCAP_SYSTEMD_RUN=0|1` forces the verdict
    and skips the probe entirely (for tests and for boxes already known)."""
    global _PROBE
    forced = os.environ.get("AGI_MEMCAP_SYSTEMD_RUN")
    if forced is not None and forced.strip() != "":
        return forced.strip() not in ("0", "false", "False", "no")
    if _PROBE is None:
        _PROBE = _read_cached_probe()
    if _PROBE is None:
        _PROBE = False
        if shutil.which("systemd-run"):
            try:
                _PROBE = subprocess.run(
                    ["systemd-run", "--user", "--scope", "-q",
                     f"--unit={_PROBE_UNIT}",
                     "--property=MemoryMax=64M",
                     "--property=MemorySwapMax=0", "--", sys.executable,
                     "-c", "x=bytearray(256*1024*1024)"],
                    capture_output=True, timeout=30).returncode == -signal.SIGKILL
            except (OSError, subprocess.SubprocessError):
                _PROBE = False
            _reset_probe_unit()
        _write_cached_probe(_PROBE)
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
