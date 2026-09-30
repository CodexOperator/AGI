"""The one shell entry of hypothesis:g7556-guard-ram-writes-charge-ramdisk-
slice-through-one-shell-entry: the RAM tree is an rbind overmount AT MAIN, so
the rule is asked of the FILESYSTEM (`mem_cap.py ram-exec --to`) and a tmpfs is
declared through a mount TABLE, never mounted. The fake `systemd-run` records
its argv, so every assertion is on the scope argv carries; manager REACHABILITY
is pinned per row, being decided BEFORE the wrap."""
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
BUS = "unix:path=/run/user/1000/bus"          # the user manager IS there
_WRITERS = ("mv", "cp", "mkdir", "rm", "ln", "touch", "rsync", "ionice")
#: a manager that is NOT there: systemd-run exits 1 and the argv behind `--`
#: NEVER runs -- the silent vanishing C2 pins shut
_DOWN = '#!/bin/sh\necho "Failed to connect to bus: No such file or directory" >&2; exit 1\n'
_SCOPE_RUN = """#!/bin/sh
printf '%s\\n' "$*" >> "$AGI_FAKE_LOG"
while [ "$1" != "--" ]; do shift; done; shift
# the tail runs INSIDE the scope: its records go to a NESTED log, so an
# unscoped record in the MAIN log is a real unscoped write, never the tail
AGI_FAKE_LOG="$AGI_FAKE_LOG.nested"; export AGI_FAKE_LOG
exec "$@"
"""
_RECORD = '#!/bin/sh\nprintf \'%s %s\\n\' "$(basename "$0")" "$*" >> "$AGI_FAKE_LOG"\n{body}\n'

@pytest.fixture
def fake(tmp_path):
    """PATH-fronted dir: recording `systemd-run`, recording copies of the write
    commands, no-op sudo/mount/mountpoint, and the shared log."""
    d = tmp_path / "fakebin"
    d.mkdir()
    log = tmp_path / "fake.log"; log.write_text("")
    for name, body in (("systemd-run", _SCOPE_RUN), ("sudo", "exit 0"),
                       ("mount", "exit 0"), ("mountpoint", "exit 0")):
        _install(d, name, body if name == "systemd-run" else _RECORD.format(body="exit 0"))
    for name in _WRITERS:
        real = shutil.which(name)
        if real is not None:
            _install(d, name, _RECORD.format(body=f'exec {real} "$@"'))
    return {"dir": d, "log": log, "path": f"{d}{os.pathsep}{os.environ['PATH']}"}

def _install(d, name, body):
    p = d / name; p.write_text(body); p.chmod(0o755)

def _mounts(tmp_path, ram: pathlib.Path, malformed: bool = False) -> str:
    """`ram` a tmpfs; `malformed` prefixes a row at the SAME mount point with no
    ` - ` separator: SKIP it (D2), never raise out of it."""
    junk = ("31 25 0:99 / {ram} rw,relatime shared:9 ext4 /dev/broken rw\n" if malformed else "")
    return (junk + "21 25 0:19 / {root} rw,relatime shared:1 - ext4 /dev/root rw\n"
            "8 35 0:29 / {ram} rw,nosuid,nodev shared:4 - tmpfs tmpfs rw\n").format(
        root=os.path.realpath(tmp_path), ram=os.path.realpath(ram))

def _entries(fake):
    return [l for l in fake["log"].read_text().splitlines() if l.strip()]
def _rc(argv):
    return subprocess.run([sys.executable, str(MEM_CAP), *argv], capture_output=True, text=True)

def _writes_under(line: str, root: pathlib.Path) -> bool:
    """A WRITE whose target lands under `root`: the LAST path in the argv, normpath'd and never resolved."""
    t = line.split(); t = t[t.index("--") + 1:] if "--" in t else t
    q = [x for x in t[1:] if x.startswith("/")]
    return bool(t) and pathlib.Path(t[0]).name in _WRITERS and bool(q) and \
        pathlib.Path(os.path.normpath(q[-1])).is_relative_to(root.resolve())

def _run(env, script: str):
    e = dict(os.environ, DBUS_SESSION_BUS_ADDRESS=BUS,
             XDG_RUNTIME_DIR="/nonexistent-runtime", AGI_MEMCAP_SYSTEMD_RUN="1")
    return subprocess.run(["bash", "-c", script], env=dict(e, **env), capture_output=True, text=True)

def _shell_env(fake, tmp_path, ram, malformed: bool = False) -> "dict":
    mi = tmp_path / "mountinfo"; mi.write_text(_mounts(tmp_path, ram, malformed))
    return {"PATH": fake["path"], "AGI_FAKE_LOG": str(fake["log"]), "AGI_MEMCAP_MOUNTINFO": str(mi)}

def _block(script: str, name: str) -> str:
    """The SHIPPED text of one function, brace-balanced (never falls through)."""
    lines = pathlib.Path(script).read_text().splitlines()
    start = next(i for i, l in enumerate(lines) if re.match(rf"^{name}\(\) \{{", l))
    depth, end = 0, start
    for j in range(start, len(lines)):
        depth, end = depth + lines[j].count("{") - lines[j].count("}"), j
        if depth == 0:
            break
    return "\n".join(lines[start:end + 1]) + "\n"

def _funcs(tmp_path, script, *names) -> pathlib.Path:
    p = tmp_path / f"funcs-{pathlib.Path(script).name}.sh"
    p.write_text("\n".join(_block(script, n) for n in names) + "\n"); return p

def _snippet(src, dest, funcs: pathlib.Path) -> str:
    return (f"\nset -euo pipefail\nHERE=$(dirname {GUARD / 'session-sweep.sh'})\n. {funcs}\n"
            f"DRY=0\nlog() {{ echo \"$*\"; }}\nmove {src} {dest}\n")

def _ram_disk(tmp_path):
    ram, disk = tmp_path / "ram", tmp_path / "disk"
    (ram / "keep").mkdir(parents=True); disk.mkdir()
    return ram, disk

@pytest.mark.parametrize("malformed", [False, True], ids=["W1-table", "D2-junk-row"])
def test_W1_charge_is_a_real_filesystem_decision(fake, tmp_path, malformed):
    """W1 tmpfs DESTINATION charged, disk-bound plain, argv's own rc. D2: a row with no ` - ` separator is SKIPPED, so the tmpfs row behind it still charges."""
    ram, disk = _ram_disk(tmp_path)
    src = tmp_path / "src.txt"; src.write_text("page")
    py = f"{sys.executable} {MEM_CAP} ram-exec --to"
    r = _run(_shell_env(fake, tmp_path, ram / "keep", malformed),
             f"{py} {ram}/keep -- cp {src} {ram}/keep/page; {py} {disk} -- sh -c 'exit 7'")
    assert r.returncode == 7, (r.returncode, r.stderr)   # argv's own exit code
    assert (ram / "keep" / "page").read_text() == "page"
    assert [l for l in _entries(fake) if SCOPE_FLAG in l], _entries(fake)
    assert pathlib.Path(str(fake["log"]) + ".nested").read_text().strip()

@pytest.mark.parametrize("src_on_ram", [False, True], ids=["G1-into-tmpfs", "G2-out-of-tmpfs"])
def test_G_move_charges_exactly_the_tmpfs_side(fake, tmp_path, src_on_ram):
    """G1 (the near miss) src on DISK dest on tmpfs, G2 the reverse: every write landing ON the tmpfs ran in the scope."""
    ram, disk = _ram_disk(tmp_path)
    src = (ram / "keep" / "iter-x") if src_on_ram else (disk / "iter-x")
    src.mkdir(parents=True); (src / "a.txt").write_text("a")
    dest = (disk / "arch" / "iter-x") if src_on_ram else (ram / "arch" / "iter-x")
    body = _snippet(src, dest, _funcs(tmp_path, GUARD / "session-sweep.sh", "ramw", "move"))
    r = _run(_shell_env(fake, tmp_path, ram), body)
    assert r.returncode == 0, r.stderr
    assert (dest / "a.txt").read_text() == "a"
    assert (src).is_symlink() and os.readlink(src) == str(dest)
    assert [l for l in _entries(fake) if SCOPE_FLAG not in l and _writes_under(l, ram)] == []
    scoped = [l for l in _entries(fake) if SCOPE_FLAG in l]
    assert scoped and all(_writes_under(l, ram) for l in scoped), scoped

def test_U1_every_ram_bound_write_in_up_goes_through_the_entry(fake, tmp_path):
    """U1 -- every $RAM-destination write in up/bind_in is a ramw line; no DISK/STATE one is."""
    text = (GUARD / "ram-main.sh").read_text()
    up = text.split("\nup)\n", 1)[1].split("\nsync)", 1)[0]
    lines = up.splitlines() + _block(GUARD / "ram-main.sh", "bind_in").splitlines()
    stmts = [s.split("#")[0].strip() for l in lines for s in l.split(";")]
    w = r"\b(mkdir|touch|rsync|cp|mv|rm)\b"
    raml = [s for s in stmts if re.search(w, s) and re.search(r'"\$RAM|"\$\(dirname "\$RAM', s)]
    diskl = [s for s in stmts if re.search(w, s) and re.search(r'"\$(DISK|STATE)[^"]*"\s*$', s)]
    assert len(raml) >= 5, raml      # the subject is still there
    assert all(re.sub(r"^(if|then|else)\s+", "", s).startswith("ramw ") for s in raml), raml
    assert diskl and not any(l.startswith("ramw ") for l in diskl), diskl

def test_U2_bind_in_and_the_up_rsync_write_in_the_scope(fake, tmp_path):
    """U2 -- shipped bind_in and the up mkdir: tmpfs-bound writes charged, none else; with a disk `ram`, none of them is."""
    ram, disk = _ram_disk(tmp_path)
    (disk / ".git").mkdir(parents=True); (disk / ".env").write_text("k=1")
    env = dict(_shell_env(fake, tmp_path, ram), HERE=str(GUARD), DISK=str(disk), RAM=str(ram))
    body = (f". {_funcs(tmp_path, GUARD / 'ram-main.sh', 'ramw', 'bind_in')}\n"
            'ramw "$RAM" mkdir -p "$RAM"\nbind_in .git\nbind_in .env\n')
    r = _run(env, "set -euo pipefail\n" + body)
    assert r.returncode == 0, r.stderr
    assert (ram / ".git").is_dir() and (ram / ".env").is_file()
    assert _entries(fake), "no writes ran at all"
    assert [l for l in _entries(fake) if SCOPE_FLAG not in l and _writes_under(l, ram)] == []
    assert any(SCOPE_FLAG in l for l in _entries(fake)), _entries(fake)
    off = tmp_path / "mountinfo.disk"   # `ram` is a disk fs from here on
    off.write_text(_mounts(tmp_path, tmp_path / "unmounted"))
    (ram / ".env").unlink()
    fake["log"].write_text("")            # phase two starts from an empty log
    r = _run(dict(env, AGI_MEMCAP_MOUNTINFO=str(off)), "set -euo pipefail\n" + body)
    assert r.returncode == 0, r.stderr
    assert [l for l in _entries(fake) if SCOPE_FLAG in l] == [], _entries(fake)
    assert any(_writes_under(l, ram) for l in _entries(fake)), "the writes did not run"

def test_C1_and_C2_an_unusable_or_unreachable_scope_runs_the_real_argv(fake, tmp_path):
    """C1 no usable scope: argv UNWRAPPED, rc kept, said ONCE. C2 (DG3.50) manager DOWN: reachability decided BEFORE wrapping, so argv runs plain (own marker, rc 7) instead of vanishing."""
    ram, _ = _ram_disk(tmp_path); env = _shell_env(fake, tmp_path, ram)
    r = _run(dict(env, AGI_MEMCAP_SYSTEMD_RUN="0"),
             f"{sys.executable} {MEM_CAP} ram-exec --to {ram} -- sh -c 'exit 3'")
    assert r.returncode == 3, (r.returncode, r.stderr)
    assert r.stderr.count("UNWRAPPED") == 1, r.stderr
    assert _entries(fake) == [], _entries(fake)      # nothing claimed the scope
    # the manager is DOWN now: systemd-run itself exits 1, and tmp_path (as the
    # runtime dir) carries no systemd/private, so bus AND socket are unreachable
    _install(fake["dir"], "systemd-run", _DOWN)
    r = _run(dict(env, DBUS_SESSION_BUS_ADDRESS="", XDG_RUNTIME_DIR=str(tmp_path)),
             f"{sys.executable} {MEM_CAP} ram-exec --to {ram} -- "
             "sh -c 'echo CHILD-RAN >> \"$AGI_FAKE_LOG\"; exit 7'")
    assert r.returncode == 7, (r.returncode, r.stderr)      # argv's rc, not 1
    assert r.stderr.count("UNREACHABLE") == 1, r.stderr
    assert "CHILD-RAN" in fake["log"].read_text(), _entries(fake)
    assert not pathlib.Path(str(fake["log"]) + ".nested").exists(), "it was scoped"

def test_N1_no_scope_argv_in_shell_and_no_second_rule(fake, tmp_path):
    """N1 -- no scope argv in shell, one spelling of the caller, recharge gone."""
    bodies = []
    for s in (GUARD / "ram-main.sh", GUARD / "session-sweep.sh"):
        text = s.read_text()
        assert "systemd-run" not in text, s
        assert 'case "$p" in' not in text, s      # the prefix rule is gone
        bodies.append(_block(s, "ramw"))
    assert bodies[0] == bodies[1], bodies         # one spelling of the caller
    rc = _rc(["ram-recharge", str(tmp_path)])
    assert rc.returncode != 0 and "ram-recharge" in rc.stderr

def test_W0_live_table_and_N2_argv_strict(fake, tmp_path):
    """W0 -- the REAL table answers when nothing overrides it. N2 -- no `--` and
    an empty argv both exit 2, by name."""
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
    for argv in (["ram-exec", "true"], ["ram-exec", "--to", "/tmp", "--"]):
        rc = _rc(argv)
        assert rc.returncode == 2 and "ram-exec" in rc.stderr, (argv, rc.returncode)
