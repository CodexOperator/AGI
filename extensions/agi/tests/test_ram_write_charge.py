"""The one shell entry of hypothesis:g7556-guard-ram-writes-charge-ramdisk-
slice-through-one-shell-entry, on the shape the box HAS.

The RAM tree is an rbind overmount AT MAIN, so no "$RAM_DIR"/* prefix names it.
The rule is therefore asked of the FILESYSTEM (`mem_cap.py ram-exec --to`),
and these rows declare a tmpfs through a mount table instead of mounting one:
no real mount, no real unit, no sudo, no live RAM dir. The fake `systemd-run`
records its argv before running the tail, so the assertion is on the scope the
argv actually carries.
"""
from __future__ import annotations

import os
import pathlib
import re
import shutil
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

_FAKE_NOOP = """#!/bin/sh
printf '%s %s\\n' "$(basename "$0")" "$*" >> "$AGI_FAKE_LOG"
exit 0
"""

_WRITERS = ("mv", "cp", "mkdir", "rm", "ln", "touch", "rsync", "ionice")


@pytest.fixture
def fake(tmp_path):
    """A PATH-fronted dir holding a recording `systemd-run`, a recording copy of
    every write command, a no-op sudo/mount/mountpoint, and the shared log."""
    d = tmp_path / "fakebin"
    d.mkdir()
    log = tmp_path / "fake.log"
    log.write_text("")
    for name, body in (("systemd-run", _FAKE_SYSTEMD_RUN), ("sudo", _FAKE_NOOP),
                       ("mount", _FAKE_NOOP), ("mountpoint", _FAKE_NOOP)):
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


def _mounts(tmp_path, ram: pathlib.Path) -> str:
    """A mount table that declares `ram` a tmpfs and everything under
    tmp_path a disk fs -- the box shape, RAM tree overmounting a disk dir."""
    return ("21 25 0:19 / {root} rw,relatime shared:1 - ext4 /dev/root rw\n"
            "8 35 0:29 / {ram} rw,nosuid,nodev shared:4 - tmpfs tmpfs rw\n"
            ).format(root=os.path.realpath(tmp_path), ram=os.path.realpath(ram))


def _entries(fake) -> "list[str]":
    return [l for l in fake["log"].read_text().splitlines() if l.strip()]


def _under(line: str, root: pathlib.Path) -> bool:
    """Does this recorded command WRITE under `root`? The write lands on the
    LAST path in the argv (`ln -s A B` makes the inode at B, `cp -a a b` at b),
    so only that one decides where the page was charged."""
    paths = [p for p in line.split()[1:] if p.startswith("/")]
    if not paths:
        return False
    try:
        r = pathlib.Path(os.path.normpath(paths[-1]))   # NOT resolve(): the
        # write target may already BE a symlink into the other tree
        return r == root.resolve() or r.is_relative_to(root.resolve())
    except OSError:
        return False


def _cmd(line: str) -> str:
    """The command a recorded line runs, past any scope argv."""
    t = line.split()
    if "--" in t:
        t = t[t.index("--") + 1:]
    return pathlib.Path(t[0]).name if t else ""


def _writes_under(line: str, root: pathlib.Path) -> bool:
    """A WRITE command whose target lands under `root`."""
    return _cmd(line) in _WRITERS and _under(line, root)


def _run(env, script: str):
    e = dict(os.environ, **env)
    e.setdefault("AGI_MEMCAP_SYSTEMD_RUN", "1")
    return subprocess.run(["bash", "-c", script], env=e, capture_output=True, text=True)


def _shell_env(fake, tmp_path, ram) -> "dict":
    """PATH fakes + a mount table file that makes `ram` the tmpfs."""
    mi = tmp_path / "mountinfo"
    mi.write_text(_mounts(tmp_path, ram))
    return {"PATH": fake["path"], "AGI_FAKE_LOG": str(fake["log"]),
            "AGI_MEMCAP_MOUNTINFO": str(mi)}


def _block(script: str, name: str) -> str:
    """The SHIPPED text of one function -- by the explicit guard-ram-write
    markers when it has them, else brace-balanced, so the loader can never
    fall through into the rest of the script."""
    lines = pathlib.Path(script).read_text().splitlines()
    begin = [i for i, l in enumerate(lines) if "guard-ram-write: begin" in l]
    if begin:
        end = next(i for i in range(begin[0], len(lines))
                   if "guard-ram-write: end" in lines[i])
        block = "\n".join(lines[begin[0] + 1:end]) + "\n"
        if re.match(rf"^{name}\(\) \{{", block):
            return block
    start = next(i for i, l in enumerate(lines) if re.match(rf"^{name}\(\) \{{", l))
    depth, end = 0, start
    for j in range(start, len(lines)):
        depth += lines[j].count("{") - lines[j].count("}")
        end = j
        if depth == 0:
            break
    return "\n".join(lines[start:end + 1]) + "\n"


def _funcs(tmp_path, script, *names) -> pathlib.Path:
    p = tmp_path / f"funcs-{pathlib.Path(script).name}.sh"
    p.write_text("\n".join(_block(script, n) for n in names) + "\n")
    return p


def test_W1_charge_is_a_real_filesystem_decision(fake, tmp_path):
    """W1 -- the ONE entry charges a write whose DESTINATION the mount table
    calls tmpfs, and runs a disk-bound destination plain, with argv's exit."""
    ram, disk = tmp_path / "ram", tmp_path / "disk"
    (ram / "d").mkdir(parents=True)
    disk.mkdir()
    src = tmp_path / "src.txt"
    src.write_text("page")
    env = _shell_env(fake, tmp_path, ram / "d")
    r = _run(env, f"{sys.executable} {MEM_CAP} ram-exec --to {ram}/d -- cp {src} {ram}/d/page; "
                  f"{sys.executable} {MEM_CAP} ram-exec --to {disk} -- sh -c 'exit 7'")
    assert r.returncode == 7, (r.returncode, r.stderr)   # argv's own exit code
    assert (ram / "d" / "page").read_text() == "page"
    assert [l for l in _entries(fake) if SCOPE_FLAG in l], _entries(fake)
    nested = pathlib.Path(str(fake["log"]) + ".nested")
    assert nested.exists() and nested.read_text().strip()


def test_G1_move_into_the_overmounted_tmpfs_is_scoped(fake, tmp_path):
    """G1 (the parent's near miss) -- src on DISK, dest on the tmpfs: every
    write that lands on the tmpfs ran in the scope, and none on the disk."""
    ram, disk = tmp_path / "ram", tmp_path / "disk"
    (ram / "keep").mkdir(parents=True)
    disk.mkdir()
    src = disk / "iter-x"
    src.mkdir()
    (src / "a.txt").write_text("a")
    dest = ram / "arch" / "iter-x"
    r = _run(_shell_env(fake, tmp_path, ram),
             _snippet(ram, src, dest, _funcs(tmp_path, GUARD / "session-sweep.sh",
                                             "ramw", "move")))
    assert r.returncode == 0, r.stderr
    assert (dest / "a.txt").read_text() == "a"
    assert (src).is_symlink() and os.readlink(src) == str(dest)
    bad = [l for l in _entries(fake) if SCOPE_FLAG not in l and _writes_under(l, ram)]
    assert bad == [], bad
    assert [l for l in _entries(fake) if SCOPE_FLAG in l], _entries(fake)


def test_G2_move_out_of_the_tmpfs_charges_only_the_tmpfs_side(fake, tmp_path):
    """G2 -- the reverse: the dest is on disk, so mkdir/cp/mv there stay plain
    while the symlink replacing the RAM-side source is charged."""
    ram, disk = tmp_path / "ram", tmp_path / "disk"
    (ram / "keep").mkdir(parents=True)
    disk.mkdir()
    src = ram / "keep" / "iter-y"
    src.mkdir()
    (src / "b.txt").write_text("b")
    dest = disk / "arch" / "iter-y"
    r = _run(_shell_env(fake, tmp_path, ram),
             _snippet(ram, src, dest, _funcs(tmp_path, GUARD / "session-sweep.sh",
                                             "ramw", "move")))
    assert r.returncode == 0, r.stderr
    assert (dest / "b.txt").read_text() == "b"
    bad = [l for l in _entries(fake) if SCOPE_FLAG not in l and _writes_under(l, ram)]
    assert bad == [], bad
    scoped = [l for l in _entries(fake) if SCOPE_FLAG in l]
    assert scoped and all(_under(l, ram) for l in scoped), scoped


def test_U1_every_ram_bound_write_in_up_goes_through_the_entry(fake, tmp_path):
    """U1 -- the rows that can fail on text: in ram-main.sh every write whose
    destination is $RAM (up's mkdir/rsync, bind_in's mkdir/touch) is a ramw
    line, and every DISK/STATE-bound write is not."""
    text = (GUARD / "ram-main.sh").read_text()
    up = text.split("\nup)\n", 1)[1].split("\nsync)", 1)[0]
    lines = up.splitlines() + _block(GUARD / "ram-main.sh", "bind_in").splitlines()
    stmts = [s.split("#")[0].strip() for l in lines for s in l.split(";")]
    ram_lines = [s for s in stmts
                 if re.search(r"\b(mkdir|touch|rsync|cp|mv|rm|ln)\b", s)
                 and re.search(r'"\$RAM|"\$\(dirname "\$RAM', s)]
    assert len(ram_lines) >= 5, ram_lines      # the subject is still there
    assert all(re.sub(r"^(if|then|else)\s+", "", s).startswith("ramw ")
               for s in ram_lines), ram_lines
    disk_lines = [s for s in stmts
                  if re.search(r"\b(mkdir|touch|rsync|mv|rm)\b", s)
                  and re.search(r'"\$(DISK|STATE)[^"]*"\s*$', s)]
    assert disk_lines and not any(l.startswith("ramw ") for l in disk_lines), disk_lines


def test_U2_bind_in_and_the_up_rsync_write_in_the_scope(fake, tmp_path):
    """U2 -- the shipped bind_in and the up mkdir, driven with fakes for
    mount/sudo/mountpoint: the tmpfs-bound writes are charged, and nothing is."""
    ram, disk = tmp_path / "ram", tmp_path / "disk"
    ram.mkdir()
    (disk / ".git").mkdir(parents=True)
    (disk / ".env").write_text("k=1")
    env = _shell_env(fake, tmp_path, ram)
    env.update({"HERE": str(GUARD), "DISK": str(disk), "RAM": str(ram)})
    body = f". {_funcs(tmp_path, GUARD / 'ram-main.sh', 'ramw', 'bind_in')}\n" \
           'ramw "$RAM" mkdir -p "$RAM"\nbind_in .git\nbind_in .env\n'
    r = _run(env, "set -euo pipefail\n" + body)
    assert r.returncode == 0, r.stderr
    assert (ram / ".git").is_dir() and (ram / ".env").is_file()
    assert _entries(fake), "no writes ran at all"
    bad = [l for l in _entries(fake) if SCOPE_FLAG not in l and _writes_under(l, ram)]
    assert bad == [], bad          # every tmpfs-bound write was in the scope
    assert any(SCOPE_FLAG in l for l in _entries(fake)), _entries(fake)
    off = tmp_path / "mountinfo.disk"
    off.write_text(_mounts(tmp_path, tmp_path / "unmounted"))
    disk_bound = dict(env, AGI_MEMCAP_MOUNTINFO=str(off))
    (ram / ".env").unlink()
    fake["log"].write_text("")            # phase two starts from an empty log
    r = _run(disk_bound, "set -euo pipefail\n" + body)
    assert r.returncode == 0, r.stderr
    assert [l for l in _entries(fake) if SCOPE_FLAG in l] == [], _entries(fake)
    assert any(_writes_under(l, ram) for l in _entries(fake)), "the writes did not run"


def test_C1_the_entry_survives_an_unreachable_user_manager(fake, tmp_path):
    """C1 -- `up` runs before the user manager: with no usable scope the entry
    runs argv UNWRAPPED, keeps argv's exit code and says so once on stderr."""
    ram = tmp_path / "ram"
    ram.mkdir()
    env = _shell_env(fake, tmp_path, ram)
    env["AGI_MEMCAP_SYSTEMD_RUN"] = "0"
    r = _run(env, f"{sys.executable} {MEM_CAP} ram-exec --to {ram} -- sh -c 'exit 3'")
    assert r.returncode == 3, (r.returncode, r.stderr)
    assert r.stderr.count("UNWRAPPED") == 1, r.stderr
    assert _entries(fake) == [], _entries(fake)      # nothing claimed the scope


def test_N1_no_scope_argv_in_shell_and_no_second_rule(fake, tmp_path):
    """N1 -- the scripts build no scope argv, spell the one caller identically,
    and the removed recharge verb is gone (goal:g7.16.1.5.5.6.1 carries it)."""
    scripts = [GUARD / "ram-main.sh", GUARD / "session-sweep.sh"]
    bodies = []
    for s in scripts:
        text = s.read_text()
        assert "systemd-run" not in text, s
        assert 'case "$p" in' not in text, s      # the prefix rule is gone
        bodies.append(_block(s, "ramw"))
    assert bodies[0] == bodies[1], bodies         # one spelling of the caller
    r = subprocess.run([sys.executable, str(MEM_CAP), "ram-recharge", str(tmp_path)],
                       capture_output=True, text=True)
    assert r.returncode != 0 and "ram-recharge" in r.stderr


def test_N2_the_entry_is_argv_strict(fake, tmp_path):
    """N1b -- no `--` and an empty argv both exit 2, by name."""
    for argv in (["ram-exec", "true"], ["ram-exec", "--to", "/tmp", "--"]):
        r = subprocess.run([sys.executable, str(MEM_CAP), *argv],
                           capture_output=True, text=True)
        assert r.returncode == 2, (argv, r.returncode, r.stderr)
        assert "ram-exec" in r.stderr


def test_W0_live_mount_table_answers_for_a_real_tmpfs():
    """W0 -- the decision reads the REAL table when nothing overrides it: a
    tmpfs mount names itself, and a plain dir names its own filesystem."""
    sys.path.insert(0, str(BIN))
    try:
        import mem_cap
    finally:
        sys.path.pop(0)
    shm = pathlib.Path("/dev/shm")
    if shm.is_dir():
        assert mem_cap.fstype_at(str(shm)) == "tmpfs"
        assert mem_cap.fstype_at(str(shm / "nope" / "deeper")) == "tmpfs"
    assert mem_cap.fstype_at("/etc") != "tmpfs"


_SWEEP_MOVE_SNIPPET = r"""
set -euo pipefail
HERE=$(dirname @sweep@)
. @funcs@
DRY=0
log() { echo "$*"; }
move "@src@" "@dest@"
"""


def _snippet(ram, src, dest, funcs: pathlib.Path) -> str:
    return (_SWEEP_MOVE_SNIPPET.replace("@sweep@", str(GUARD / "session-sweep.sh"))
            .replace("@ram@", str(ram)).replace("@src@", str(src))
            .replace("@dest@", str(dest)).replace("@funcs@", str(funcs)))