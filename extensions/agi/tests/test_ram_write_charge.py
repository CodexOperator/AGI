"""F1-F4 of hypothesis:g7556-guard-ram-writes-charge-ramdisk-slice-through-one-
shell-entry -- every write INTO the RAM dir is charged to `ramdisk.slice`
through `mem_cap.py ram-exec`, and no disk-bound write is.

Nothing here touches the live RAM dir, a real unit or sudo: `systemd-run` and
the six write commands are faked on PATH, and the fake systemd-run RECORDS its
argv before running the tail, so the assertion is on the scope the argv
actually carries.
"""
from __future__ import annotations

import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[3]
BIN = ROOT / "extensions" / "agi" / "bin"
GUARD = ROOT / "extensions" / "agi" / "guard"
MEM_CAP = BIN / "mem_cap.py"
SCOPE_FLAG = "--slice=ramdisk.slice"

_FAKE_SYSTEMD_RUN = """#!/bin/sh
printf '%s\\n' "$*" >> "$AGI_FAKE_LOG"
while [ "$1" != "--" ]; do shift; done
shift
# the tail runs INSIDE the scope: its own records go to a nested log, so an
# unscoped record in the main log is a real unscoped write, never the tail
AGI_FAKE_LOG="$AGI_FAKE_LOG.nested"
export AGI_FAKE_LOG
exec "$@"
"""

_FAKE_CMD = """#!/bin/sh
printf '%s %s\\n' "$(basename "$0")" "$*" >> "$AGI_FAKE_LOG"
exec {real} "$@"
"""

_WRITERS = ("mv", "cp", "mkdir", "rm", "ln", "rsync", "ionice", "cpio", "dd")


@pytest.fixture
def fake(tmp_path):
    """A PATH-fronted dir holding a recording `systemd-run` and a recording
    copy of every write command, plus the log both append to."""
    d = tmp_path / "fakebin"
    d.mkdir()
    log = tmp_path / "fake.log"
    log.write_text("")
    for name, body in (("systemd-run", _FAKE_SYSTEMD_RUN),):
        p = d / name
        p.write_text(body)
        p.chmod(0o755)
    for name in _WRITERS:
        real = shutil.which(name)
        if real is None:
            continue
        p = d / name
        p.write_text(_FAKE_CMD.format(real=real))
        p.chmod(0o755)
    return {"dir": d, "log": log, "path": f"{d}{os.pathsep}{os.environ['PATH']}"}


def _entries(fake) -> "list[str]":
    return [l for l in fake["log"].read_text().splitlines() if l.strip()]


def _scoped(fake) -> "list[str]":
    return [l for l in _entries(fake) if SCOPE_FLAG in l]


def _run(env, script: str, **kw):
    e = dict(os.environ, **env)
    e.setdefault("AGI_MEMCAP_SYSTEMD_RUN", "1")   # the fake stands in for the probe
    return subprocess.run(["bash", "-c", script], env=e, capture_output=True,
                          text=True, **kw)


def test_F1_ram_exec_charges_a_write_into_the_ram_dir(fake, tmp_path):
    """F1a -- the ONE shell entry: a write into a RAM-dir fixture runs under
    the ramdisk.slice scope argv, and the write still happens."""
    ram = tmp_path / "ram"
    ram.mkdir()
    src = tmp_path / "src.txt"
    src.write_text("page")
    r = _run({"PATH": fake["path"], "AGI_FAKE_LOG": str(fake["log"])},
             f"{sys.executable} {MEM_CAP} ram-exec -- cp {src} {ram}/page")
    assert r.returncode == 0, r.stderr
    assert (ram / "page").read_text() == "page"
    assert _scoped(fake), _entries(fake)


def test_F1_sweep_move_into_the_ram_dir_is_fully_scoped(fake, tmp_path):
    """F1b -- session-sweep.sh's move, driven as a function, into a RAM-dir
    fixture: every write that lands under the RAM dir is a scoped one."""
    ram = tmp_path / "ram"
    (ram / "keep").mkdir(parents=True)
    src = ram / "keep" / "iter-x"
    src.mkdir()
    (src / "a.txt").write_text("a")
    env = {"PATH": fake["path"], "AGI_FAKE_LOG": str(fake["log"])}
    r = _run(env, _snippet(ram, src, ram / "arch" / "iter-x", _funcs_file(tmp_path)))
    assert r.returncode == 0, r.stderr
    assert (ram / "arch" / "iter-x" / "a.txt").read_text() == "a"
    # every write that landed under the RAM dir ran INSIDE the scope argv
    assert _scoped(fake), _entries(fake)
    nested = pathlib.Path(str(fake["log"]) + ".nested")
    assert nested.exists() and nested.read_text().strip(), "no write ran in the scope"
    for line in _entries(fake):
        if SCOPE_FLAG not in line:
            assert not any(_under(p, ram) for p in line.split()[1:]), line


def test_F2_a_disk_bound_move_is_not_charged(fake, tmp_path):
    """F2 -- a move whose every path is on disk stays UNSCOPED: the RAM slice
    is not charged for disk writes."""
    plain = tmp_path / "plain"
    src = plain / "iter-y"
    src.mkdir(parents=True)
    (src / "b.txt").write_text("b")
    r = _run({"PATH": fake["path"], "AGI_FAKE_LOG": str(fake["log"])},
             _snippet(tmp_path / "unused-ram", src, plain / "arch" / "iter-y",
                      _funcs_file(tmp_path)))
    assert r.returncode == 0, r.stderr
    assert (plain / "arch" / "iter-y" / "b.txt").read_text() == "b"
    assert _scoped(fake) == [], _entries(fake)


def test_F3_ram_recharge_keeps_bytes_and_mode_and_stays_scoped(fake, tmp_path):
    """F3 -- the on-demand recharge rewrites the tree in the scope and leaves
    every file's bytes and mode exactly as they were."""
    ram = tmp_path / "ram"
    deep = ram / "sub"
    deep.mkdir(parents=True)
    (ram / "a.txt").write_bytes(b"\x00\x01page")
    (deep / "b.sh").write_bytes(b"#!/bin/sh\n")
    (deep / "b.sh").chmod(0o750)
    before = {p: (p.read_bytes(), stat.S_IMODE(p.stat().st_mode))
              for p in sorted(ram.rglob("*")) if p.is_file()}
    r = _run({"PATH": fake["path"], "AGI_FAKE_LOG": str(fake["log"])},
             f"{sys.executable} {MEM_CAP} ram-recharge {ram}")
    assert r.returncode == 0, r.stderr
    assert _scoped(fake), _entries(fake)
    after = {p: (p.read_bytes(), stat.S_IMODE(p.stat().st_mode))
             for p in sorted(ram.rglob("*")) if p.is_file()}
    assert after == before
    assert {p.relative_to(ram) for p in after} == {p.relative_to(ram) for p in before}


def test_F4_no_scope_argv_is_built_in_shell():
    """F4 (negative) -- a `systemd-run` argv spelled in either guard script
    would be a second copy of the rule; the helper is the only way in."""
    for script in (GUARD / "ram-main.sh", GUARD / "session-sweep.sh"):
        hits = [l for l in script.read_text().splitlines()
                if re.search(r"systemd-run", l)]
        assert hits == [], (script, hits)


def test_ram_main_ram_bound_rsync_goes_through_the_helper():
    """(2) -- the DISK -> RAM rsync passes in ram-main.sh are the helper's."""
    text = (GUARD / "ram-main.sh").read_text()
    ram_passes = [l for l in text.splitlines()
                  if re.search(r"rsync .*\bRAM\b", l) or "RSYNC_PLACEHOLDER" in l]
    assert ram_passes, "no DISK -> RAM rsync pass found -- the test lost its subject"
    assert all("ramw " in l for l in ram_passes), ram_passes
    assert text.count("ramw() {") == 1


def _under(path: str, root: pathlib.Path) -> bool:
    try:
        return pathlib.Path(path).resolve().is_relative_to(root.resolve())
    except OSError:
        return False


def _functions() -> str:
    """The SHIPPED text of `ramw()` and `move()` -- read from the script, never
    copied here, so the assertion runs what production runs. Brace-balanced by
    hand because a regex cannot tell the function's closing brace from the one
    inside a `{ ...; }` group on a line of its own."""
    lines = (GUARD / "session-sweep.sh").read_text().splitlines()
    out = []
    for name in ("ramw", "move"):
        start = next(i for i, l in enumerate(lines)
                     if re.match(rf"^{name}\(\) \{{", l))
        depth, end = 0, start
        for j in range(start, len(lines)):
            depth += lines[j].count("{") - lines[j].count("}")
            end = j
            if depth == 0:
                break
        out.append("\n".join(lines[start:end + 1]))
    return "\n".join(out) + "\n"


def _snippet(ram, src, dest, funcs: pathlib.Path) -> str:
    return (_SWEEP_MOVE_SNIPPET.replace("@sweep@", str(GUARD / "session-sweep.sh"))
            .replace("@ram@", str(ram)).replace("@src@", str(src))
            .replace("@dest@", str(dest)).replace("@funcs@", str(funcs)))


def _funcs_file(tmp_path) -> pathlib.Path:
    p = tmp_path / "funcs.sh"
    p.write_text(_functions())
    return p


#: `move()` and `ramw()` of session-sweep.sh, run as written, in a shell whose
#: RAM_DIR points at a tmp fixture -- no live RAM dir, no real unit, no sudo.
_SWEEP_MOVE_SNIPPET = r"""
set -euo pipefail
HERE=$(dirname @sweep@)
RAM_DIR=@ram@
. @funcs@
DRY=0
log() { echo "$*"; }
move "@src@" "@dest@"
"""
