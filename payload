#!/usr/bin/env python3
"""mem_cap.py -- ONE memory cap for every launched child (SM.112,
hypothesis:l4-every-launched-kid-parent-and-workflow-stage-runs-under-a-memory-
cap-so-a-runaway-dies-alone-and-by-name-never-a-global-oom)."""
from __future__ import annotations

import itertools
import os
import pathlib
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time

_PROBE: "bool | None" = None
_UMR: "bool | None" = None
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
#: The two names are the DEFAULTS of the config cells `values.memcap.
#: probe_cache_dir_name` / `probe_cache_file` (config-max, owner 2026-09-23) --
#: a caller that HAS a config passes it, and a config that omits or mangles the
#: cell lands here. They are names, not paths: the base dir is box-resolved
#: (`$XDG_RUNTIME_DIR`, else the platform temp dir), so no box root is spelled
#: in this file. A cell carrying a separator is REFUSED, never joined.
_CACHE_DIR_NAME = "agi-memcap"
_CACHE_FILE_NAME = "probe"

#: `spawn.tasks_max` -- the PER-TREE process bound carried as
#: `TasksMax` on the SAME scope that carries `MemoryMax`. Shipped default
#: 96: one round's own tree is a round process plus its tools (a `pytest -n8`
#: run is ~15 procs), so 96 is ~6x headroom on a normal round, while the
#: DH.419 fan-out that pushed user@ over memory.high was 127 forks -- a
#: default below that number, and far below the box's user@ `pids.max`
#: (16384), so the SCOPE refuses the fork instead of the whole user slice
#: growing. RLIMIT_NPROC cannot express this (it is per-USER, not per-tree),
#: so the prlimit fallback carries NO process bound -- see `wrap_argv`.
_DEFAULT_TASKS_MAX = 96

#: `spawn.memory_max` absent -> this. Named so a caller (and a test row)
#: reads the shipped default instead of typing `4G` -- one source per value,
#: the same reason `_DEFAULT_TASKS_MAX` exists.
_DEFAULT_MEMORY_CAP = "4G"


def _normalise_cap(val) -> "str | None":
    """None / 'none' / 'null' / '' -> None; else the value verbatim."""
    if val is None or str(val).strip().lower() in ("", "none", "null"):
        return None
    return str(val)


def _spawn_block(cfg: "dict | None") -> dict:
    """The `spawn` container AS A DICT, or {} -- one shared guard.

    A cell is data, not a promise: `spawn` that is a number, a list or a
    string must not raise out of a reader (it did: `resolve_memory_cap`
    raised TypeError on `{"spawn": 42}`), it must read as absent and fall
    back to the shipped default.

    Two consumers, ONE guard: both resolvers
    (`resolve_memory_cap`, `resolve_tasks_max`) and the boxkit probe's
    `spawn.*` rows (extensions/agi/boxkit/probe.py, which CALLS this rather
    than re-deciding `isinstance(spawn, dict)`).  A second copy would be a
    second rule: a shape this guard learns to accept would still kill the
    probe table."""
    spawn = (cfg or {}).get("spawn")
    return spawn if isinstance(spawn, dict) else {}


def resolve_tasks_max(cfg: "dict | None" = None) -> int:
    """`spawn.tasks_max` -> an int >= 1, else the shipped default.

    The cell sits beside `spawn.memory_max`, the one `resolve_memory_cap`
    reads, so the whole per-spawn scope is one `spawn` block (TMM.263 (2),
    owner 19:5xZ). A cell that is absent, non-numeric, or below 1 falls back
    to `_DEFAULT_TASKS_MAX` rather than to "no bound": an unreadable cell
    must not silently un-cap the tree.

    `AGI_TASKS_MAX` is an ENV HOOK, not a test-only affordance. It is read
    by WHICHEVER PROCESS CALLS THIS -- the parent that builds the argv
    (wrap_argv -> TasksMax) and the boxkit probe (probe.py, in the probe's
    OWN process) -- AND it is inherited by every spawn: dispatch.scrubbed_env
    drops only ENV_VARS_TO_SCRUB (dispatch.py:295), so a set value passes
    into each spawned scope and reaches that scope's own callers too. An
    operator, a wrapper script or an inherited environment reaches it in
    PRODUCTION. The
    hook has no config cell of its own, so the probe's DRIFT row
    (test_boxkit_probe.py `test_spawn_rows_...`) drives through it -- if the
    hook is ever retired as test-only that row loses its driver, silently,
    with no failing test."""
    env = os.environ.get("AGI_TASKS_MAX")
    raw = env if env not in (None, "") else _spawn_block(cfg).get("tasks_max")
    try:
        n = int(str(raw).strip())
    except (TypeError, ValueError):
        return _DEFAULT_TASKS_MAX
    return n if n >= 1 else _DEFAULT_TASKS_MAX


def resolve_memory_cap(cfg: dict, override: "str | None" = None) -> "str | None":
    """`spawn.memory_max`: absent -> '4G'; null/'none'/'' -> None; else as-is.

    `override` (hypothesis:lm-dispatch-memory-override-feeds-agi-batch-
    scheduling) is a per-invocation cap: when it is not None it wins over the
    config value, normalised the same way, and `cfg` is never mutated -- the
    override is request-scoped, not written back to disk.
    """
    if override is not None:
        return _normalise_cap(override)
    spawn = _spawn_block(cfg)
    if "memory_max" not in spawn:
        return _DEFAULT_MEMORY_CAP
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


def _cache_names(cfg: "dict | None") -> "tuple[str, str] | None":
    """(dir name, file name) from `values.memcap`, or None if a cell is
    unusable. A name with a path separator, `.`/`..` or a NUL could move the
    cache somewhere `_private_dir` would happily trust, so it is refused."""
    v = ((cfg or {}).get("values") or {}).get("memcap") or {}
    d = str(v.get("probe_cache_dir_name") or _CACHE_DIR_NAME)
    f = str(v.get("probe_cache_file") or _CACHE_FILE_NAME)
    for name in (d, f):
        if not name or name in (".", "..") or "/" in name or "\0" in name:
            return None
    return d, f


def _cache_path_pure(cfg: "dict | None" = None) -> "pathlib.Path | None":
    """WHERE the cross-process probe verdict lives, and nothing else -- no
    mkdir, no chmod, no lstat, so a read-only caller resolves the same path
    this module writes without touching the box.  `_probe_cache_path` is this
    plus the private-dir creation, so ONE place does the arithmetic.
    `AGI_MEMCAP_CACHE` (an explicit file path, for tests) wins; else the
    per-user runtime dir (tmpfs, cleared on boot); else `tempfile.gettempdir()`
    ($TMPDIR, else the box's `/tmp`), NOT a `/tmp` literal: the same base every
    other engine temp path resolves through, so the box's own answer wins and
    this file spells no root."""
    env = os.environ.get("AGI_MEMCAP_CACHE")
    if env:
        return pathlib.Path(env)
    names = _cache_names(cfg)
    if names is None:
        return None
    run = os.environ.get("XDG_RUNTIME_DIR")
    base = pathlib.Path(run) if run else pathlib.Path(tempfile.gettempdir())
    return base / names[0] / names[1]


def _probe_cache_path(cfg: "dict | None" = None) -> "pathlib.Path | None":
    """The WRITER's path: the pure resolution above, then the dir WE own made
    private.  None means "no cache is writable" -- the probe then runs per
    process, the old behaviour, rather than failing."""
    if os.environ.get("AGI_MEMCAP_CACHE"):
        return _cache_path_pure(cfg)     # the caller named the file; its dir is its own
    path = _cache_path_pure(cfg)
    if path is None:
        return None
    d = _private_dir(path.parent)
    return None if d is None else path


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


def _read_cached_probe(cfg: "dict | None" = None) -> "bool | None":
    """The verdict cached for THIS boot, or None (absent, stale, foreign,
    partial or corrupt). A body that is not exactly `0` or `1` is a torn or
    planted write and is re-probed, never read as a `False`."""
    path = _probe_cache_path(cfg)
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


def _write_cached_probe(val: bool, cfg: "dict | None" = None) -> None:
    """Best-effort and ATOMIC: a temp file in the same dir (0600 by
    construction) then `os.replace`, so a concurrent reader sees the old
    verdict or the new one, never a half-written one. An unwritable cache
    costs a re-probe, never a failure."""
    path = _probe_cache_path(cfg)
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
        subprocess.run(["systemctl", "--user", "reset-failed", scope_unit(_PROBE_UNIT)],
                       capture_output=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        pass


def systemd_run_usable(cfg: "dict | None" = None) -> bool:
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
        _PROBE = _read_cached_probe(cfg)
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
        _write_cached_probe(_PROBE, cfg)
    return _PROBE


#: goal:g6.41.1 P1/P6 -- the slice the tmux server's scope and every post's own
#: scope land in. NAMED RISK (verdict:dg2-r1-per-post-scope): on local-town this
#: slice carries MemoryHigh/MemoryMax shared with agi-work + agi-engine.
POST_SCOPE_SLICE = "agi.slice"


def resolve_post_scope(cfg: "dict | None") -> "str | None":
    """`spawn.post_scope` = {live: true, slice: <name>} -> that slice (default
    POST_SCOPE_SLICE); absent, or `live` not true -> None: post launches stay
    unscoped. The live cutover is this ONE cell (owner's word, goal:g6.41.1)."""
    cell = _spawn_block(cfg).get("post_scope")
    if not isinstance(cell, dict) or cell.get("live") is not True:
        return None
    return str(cell.get("slice") or POST_SCOPE_SLICE)


_UNIT_SEQ = itertools.count()


def unit_name(prefix: str, name: str) -> str:
    """THE one spelling of a transient unit name (goal:g7.16.1.7.1.1, SM rotate
    candidate): `<prefix>-<name>-<ns>-<seq>`. The old `int(time.time())` suffix let
    two launches of one name in the same second collide on the unit; a
    per-process sequence covers a clock too coarse to tick between calls."""
    return f"{prefix}-{re.sub(r'[^\w.-]', '_', name)}-{time.time_ns()}-{next(_UNIT_SEQ)}"


def scope_unit(unit: str) -> str:
    """THE one `.scope` spelling: `systemd-run --scope --unit=X` creates `X.scope`."""
    return f"{unit}.scope"


def scope_argv(argv: list, slice_: "str | None", unit: "str | None" = None,
               cfg: "dict | None" = None, *, own_scope: bool = False) -> list:
    """THE one scope-argv builder (goal:g7.16.1.7.1.1, C3). A POST's launch
    argv in its OWN scope under `slice_`, cap-free (the slice holds the cap),
    so an oomd kill takes one post, never tmux and every post (goal:g6.41.1
    P6). `own_scope=True` (the tmux server) scopes it even with no slice.
    Nothing to scope, or no usable systemd-run -> the SAME argv object, so the
    caller runs it plain. wrap_argv's shared `cap None -> argv` contract is
    untouched."""
    if not (slice_ or own_scope) or not systemd_run_usable(cfg):
        return argv
    return ["systemd-run", "--user", "--scope", "-q",
            *([f"--slice={slice_}"] if slice_ else []),
            *([f"--unit={unit}"] if unit else []), "--", *argv]


def wrap_argv(argv: list, cap: "str | None",
              cfg: "dict | None" = None, unit: "str | None" = None) -> list:
    """`cap is None` -> the SAME argv object, unwrapped; else systemd-run when
    usable, else the prlimit fallback. `cfg` is OPTIONAL and read only for the
    cache's `values.memcap` cells and for `spawn.tasks_max` (via
    `resolve_tasks_max`, which defaults when `cfg` is None) -- a caller with
    no config on hand gets the shipped defaults, so the hot path never has to
    resolve the graph itself. `unit` (mem_cap.unit_name) NAMES the scope so
    its owner can stop it by name on exit; no unit -> the SAME argv, so every
    existing caller is byte-unchanged."""
    if cap is None:
        return argv
    if systemd_run_usable(cfg):
        return ["systemd-run", "--user", "--scope", "-q",
                *([f"--unit={unit}"] if unit else []),
                f"--property=MemoryMax={cap}",
                f"--property=TasksMax={resolve_tasks_max(cfg)}",
                "--property=MemorySwapMax=0", "--", *argv]
    # NAMED RESIDUAL (DH.421): the prlimit fallback bounds ADDRESS SPACE per
    # process and NOTHING about the tree's width -- RLIMIT_NPROC is per-USER,
    # so a per-tree process cap has no prlimit spelling. A box without a
    # usable systemd-run still fans out unbounded; the fix is the systemd
    # path, not a second limit here.
    return ["prlimit", f"--as={_as_bytes(cap)}", "--", *argv]


def is_wrapped(argv) -> bool:
    """True when `wrap_argv` put `argv` in a systemd scope (so a NAMED unit
    exists to stop); the prlimit fallback and an unwrapped argv are False."""
    return bool(argv) and argv[0] == "systemd-run"


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

def fstype_at(path: str) -> str:
    """The FILESYSTEM holding `path`, asked of the mount table -- never of a path
    prefix (the RAM tree is an rbind overmount AT MAIN). A path that does not
    exist yet is answered by its nearest existing parent; the table is
    overridable (AGI_MEMCAP_MOUNTINFO) so a row can name a tmpfs without one. Octal escapes are DECODED before comparing (a space would never match); an unreadable table returns '' (fails OPEN), never a traceback."""
    p = os.path.realpath(os.path.abspath(path))
    while not os.path.isdir(p):
        n = os.path.dirname(p)
        if n == p:
            break
        p = n
    table = os.environ.get("AGI_MEMCAP_MOUNTINFO", "/proc/self/mountinfo")
    best, kind = "", ""
    try:
        with open(table) as fh:
            for line in fh:
                f = line.split()
                mp = re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), f[4].rstrip("/") or "/") if len(f) > 9 and "-" in f[:-1] else None
                if mp and len(mp) > len(best) and (p == mp or p.startswith(mp.rstrip("/") + "/")):
                    best, kind = mp, f[f.index("-") + 1]
    except OSError:     # fails OPEN; ram-exec says so, once
        return ""
    return kind


def user_manager_reachable() -> bool:
    """LIVENESS, not presence: the manager is ASKED, once per process -- a set-but-dead bus address is not one (systemd-run behind it exits 1 and the argv never runs, C2)."""
    global _UMR
    if _UMR is None:
        try:
            _UMR = subprocess.run(
                ["systemctl", "--user", "show", "-p", "Version", "--value"],
                capture_output=True, timeout=10).returncode == 0
        except (OSError, subprocess.SubprocessError):
            _UMR = False
    return _UMR


def ram_argv(argv: list) -> list:
    """`argv` as the ONE transient unit under `locations.RAM_SLICE`, or argv
    itself when systemd-run is unusable -- the shell-reachable way in, since a
    guard script cannot import Python (hypothesis:g7556-...)."""
    import locations  # local, as locations imports this module in turn
    return list(locations.ram_write_argv(list(argv)))


def _verb_ram_exec(argv: list, to: str | None = None) -> int:
    """exec the argv after `--` in the RAM scope. No argv -> usage, 2.

    `--to PATH` is THE rule for "this write lands on the tmpfs", asked of the
    filesystem: a disk-bound destination runs argv plain, untouched, and its
    exit code is argv's. No usable scope -> fail open, argv UNWRAPPED, said once
    on stderr (ram-main.sh `up` runs before the user manager)."""
    if not argv:
        sys.stderr.write("mem_cap.py ram-exec [--to PATH] -- <argv...>\n")
        return 2
    fs = fstype_at(to) if to is not None else "tmpfs"
    if fs != "tmpfs":
        if not fs:
            sys.stderr.write("mem_cap.py ram-exec: mount table unreadable -- write ran UNCHARGED\n")
        return subprocess.run(argv).returncode
    scoped, why = (ram_argv(argv), "") if user_manager_reachable() else ([], "user manager UNREACHABLE")
    if why or list(scoped) == list(argv):
        sys.stderr.write(f"mem_cap.py ram-exec: {why or 'no usable scope'} -- argv ran UNWRAPPED\n")
        return subprocess.run(argv).returncode
    try:
        os.execvp(scoped[0], scoped)
    except OSError as exc:      # fail OPEN, never a traceback off a write
        sys.stderr.write(f"mem_cap.py ram-exec: {exc} -- argv ran UNWRAPPED\n")
        return subprocess.run(argv).returncode


if __name__ == "__main__":
    import argparse
    # ram-exec carries a FOREIGN argv after `--`: argparse never sees it.
    if sys.argv[1:2] == ["ram-exec"]:
        _h = sys.argv[2:]
        if "--" not in _h:
            sys.stderr.write("mem_cap.py ram-exec: '--' is required\n")
            sys.exit(2)
        _i = _h.index("--")
        _to = _h[1] if _h[:1] == ["--to"] and len(_h) > 1 else None
        sys.exit(_verb_ram_exec(_h[_i + 1:], to=_to))
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
