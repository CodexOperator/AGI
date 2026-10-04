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
import shlex
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[3]
BIN = ROOT / "extensions" / "agi" / "bin"
GUARD = ROOT / "extensions" / "agi" / "guard"
SHARED = GUARD / "ram-write.sh"
MEM_CAP = BIN / "mem_cap.py"
SCOPE_FLAG = "--slice=ramdisk.slice"
BUS = "unix:path=/run/user/1000/bus"          # the user manager IS there
_WRITERS = ("mv", "cp", "mkdir", "rm", "ln", "touch", "rsync", "ionice")
#: a manager that is NOT there: systemd-run exits 1 and the argv behind `--`
#: NEVER runs -- the silent vanishing C2 pins shut
_DOWN = '#!/bin/sh\necho "Failed to connect to bus: No such file or directory" >&2; exit 1\n'
#: a LIVE user manager: the call mem_cap asks, answered (the liveness probe)
_LIVE = "#!/bin/sh\necho 256\n"
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
    _install(d, "systemctl", _LIVE)          # the user manager ANSWERS
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
    junk = {False: "", True: "31 25 0:99 / {ram} rw,relatime shared:9 ext4 /dev/broken rw\n",
            "tail": "31 25 0:99 / {ram} rw,relatime shared:9 shared:10 shared:11 shared:12 -\n"}[malformed]
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

def _funcs(tmp_path, *pairs) -> pathlib.Path:
    """One extraction file from (function, script) pairs -- `ramw` comes from the ONE
    shared file, `move`/`bind_in` from the script that carries them."""
    p = tmp_path / "funcs.sh"
    p.write_text("\n".join(_block(s, n) for n, s in pairs) + "\n"); return p

def _snippet(src, dest, funcs: pathlib.Path) -> str:
    return (f"\nset -euo pipefail\nHERE=$(dirname {GUARD / 'session-sweep.sh'})\n. {funcs}\n"
            f"DRY=0\nlog() {{ echo \"$*\"; }}\nmove {src} {dest}\n")

def _ram_disk(tmp_path):
    ram, disk = tmp_path / "ram", tmp_path / "disk"
    (ram / "keep").mkdir(parents=True); disk.mkdir()
    return ram, disk

@pytest.mark.parametrize("malformed", [False, True, "tail"], ids=["W1-table", "D2-junk-row", "D3-trailing-dash"])
def test_W1_charge_is_a_real_filesystem_decision(fake, tmp_path, malformed):
    """W1 tmpfs DESTINATION charged, disk-bound plain, argv's own rc. D2/D3: a row with no ` - ` separator, or ending ON it, is SKIPPED, so the tmpfs row behind it still charges."""
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
    body = _snippet(src, dest, _funcs(tmp_path, ("ramw", SHARED), ("move", GUARD / "session-sweep.sh")))
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
    body = (f". {_funcs(tmp_path, ('ramw', SHARED), ('bind_in', GUARD / 'ram-main.sh'))}\n"
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

def test_C1_no_usable_scope_runs_the_real_argv(fake, tmp_path):
    """C1 -- no usable scope: argv UNWRAPPED, its own rc, said ONCE, nothing claimed the scope."""
    ram, _ = _ram_disk(tmp_path); env = _shell_env(fake, tmp_path, ram)
    r = _run(dict(env, AGI_MEMCAP_SYSTEMD_RUN="0"),
             f"{sys.executable} {MEM_CAP} ram-exec --to {ram} -- sh -c 'exit 3'")
    assert r.returncode == 3 and r.stderr.count("UNWRAPPED") == 1, (r.returncode, r.stderr)
    assert [l for l in _entries(fake) if SCOPE_FLAG in l] == [], _entries(fake)

@pytest.mark.parametrize("live", [True, False], ids=["P1-live-manager", "P1-dead-manager"])
def test_P1_reachability_is_liveness_not_presence(fake, tmp_path, live):
    """P1 (the banked DG3.50 hole) -- the manager is ASKED, not read off the env: the bus address stays SET and a `systemd/private` socket is present in BOTH rows."""
    ram, _ = _ram_disk(tmp_path)
    rt = tmp_path / "rt"; (rt / "systemd").mkdir(parents=True); (rt / "systemd" / "private").write_text("")
    _install(fake["dir"], "systemctl", _LIVE if live else _DOWN)
    r = _run(dict(_shell_env(fake, tmp_path, ram), XDG_RUNTIME_DIR=str(rt)),
             f"{sys.executable} {MEM_CAP} ram-exec --to {ram} -- "
             "sh -c 'echo CHILD-RAN >> \"$AGI_FAKE_LOG\"; exit 7'")
    nested = pathlib.Path(str(fake["log"]) + ".nested")
    seen = fake["log"].read_text() + (nested.read_text() if nested.exists() else "")
    assert r.returncode == 7, (r.returncode, r.stderr)     # argv's rc, never 1
    assert "CHILD-RAN" in seen, seen        # it RAN either way: the C2 guarantee
    assert ([l for l in _entries(fake) if SCOPE_FLAG in l] != []) is live, _entries(fake)
    assert r.stderr.count("UNREACHABLE") == (0 if live else 1), r.stderr

def test_F1_and_F2_the_rest_of_the_path_fails_open(fake, tmp_path):
    """F1 an unreadable mount TABLE and F2 a scope that cannot be exec'd: each runs argv UNWRAPPED, ONE stderr line, NO traceback, rc still argv's."""
    ram, _ = _ram_disk(tmp_path); env = _shell_env(fake, tmp_path, ram)
    py = f"{sys.executable} {MEM_CAP} ram-exec --to"
    r = _run(dict(env, AGI_MEMCAP_MOUNTINFO=str(tmp_path / "gone")), f"{py} {ram} -- /bin/sh -c 'exit 5'")
    assert r.returncode == 5, (r.returncode, r.stderr)
    assert "Traceback" not in r.stderr and r.stderr.count("UNCHARGED") == 1, r.stderr
    bare = tmp_path / "bare"; bare.mkdir()          # systemd-run nowhere on PATH
    os.symlink(shutil.which("bash"), bare / "bash"); _install(bare, "systemctl", _LIVE)
    r = _run(dict(env, PATH=str(bare)), f"{py} {ram} -- /bin/sh -c 'exit 6'")
    assert r.returncode == 6, (r.returncode, r.stderr)
    assert "Traceback" not in r.stderr and r.stderr.count("UNWRAPPED") == 1, r.stderr

def test_M1_a_mount_point_with_a_space_is_found(fake, tmp_path):
    """M1 -- the table's octal escapes are DECODED, so a tmpfs mounted at a path holding a space is found and its writes still charge."""
    ram = tmp_path / "ram tree"; (ram / "keep").mkdir(parents=True)
    mi = tmp_path / "spaceinfo"
    mi.write_text("8 35 0:29 / %s rw,nosuid - tmpfs tmpfs rw\n" % str(ram / "keep").replace(" ", "\\040"))
    src = tmp_path / "src.txt"; src.write_text("page")
    r = _run(dict(_shell_env(fake, tmp_path, ram), AGI_MEMCAP_MOUNTINFO=str(mi)),
             f"q={shlex.quote(str(ram / 'keep'))}; "
             f"{sys.executable} {MEM_CAP} ram-exec --to \"$q\" -- cp {src} \"$q/page\"")
    assert (r.returncode, (ram / "keep" / "page").read_text()) == (0, "page"), r.stderr
    assert [l for l in _entries(fake) if SCOPE_FLAG in l], _entries(fake)

def test_N1_one_rule_sourced_by_both_and_no_scope_argv_in_shell(fake, tmp_path):
    """N1 -- no scope argv in shell, and the rule that used to be spelled twice lives in ONE file, SOURCED by both."""
    text = SHARED.read_text()
    assert "hypothesis:g7556" in text and "ramw() {" in text, text
    for s in (GUARD / "ram-main.sh", GUARD / "session-sweep.sh"):
        body = s.read_text()
        assert "systemd-run" not in body and 'case "$p" in' not in body, s
        assert '. "$HERE/ram-write.sh"' in body and "ramw() {" not in body, s
        assert "guard-ram-write" not in body, s
    rc = _rc(["ram-recharge", str(tmp_path / "gone")])
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

def test_R1_a_path_on_the_root_mount_is_answered(fake, tmp_path, monkeypatch):
    """R1 (F1) -- "/" is a mount like any other: a path whose longest mount is "/" gets ITS type, so no false UNCHARGED line, and the write runs plain."""
    mi = tmp_path / "rootinfo"; ram = tmp_path / "ram"; ram.mkdir()
    mi.write_text(f"21 1 0:19 / / rw - ext4 /dev/root rw\n8 35 0:29 / {os.path.realpath(ram)} rw - tmpfs tmpfs rw\n")
    monkeypatch.setenv("AGI_MEMCAP_MOUNTINFO", str(mi)); sys.path.insert(0, str(BIN))
    try:
        import mem_cap
    finally:
        sys.path.pop(0)
    assert (mem_cap.fstype_at(str(tmp_path)), mem_cap.fstype_at(str(ram / "x"))) == ("ext4", "tmpfs")
    r = _run(_shell_env(fake, tmp_path, ram) | {"AGI_MEMCAP_MOUNTINFO": str(mi)}, f"{sys.executable} {MEM_CAP} ram-exec --to {tmp_path} -- true")
    assert (r.returncode, r.stderr) == (0, ""), r.stderr
    assert [l for l in _entries(fake) if SCOPE_FLAG in l] == [], _entries(fake)

def test_T1_ram_tier_sources_the_entry_and_builds_no_scope_argv():
    """T1 (F3, static) -- ram-tier.sh sources ram-write.sh and never builds a scope argv in shell."""
    text = (GUARD / "ram-tier.sh").read_text()
    assert "systemd-run" not in text and '. "$HERE/ram-write.sh"' in text

def test_T2_ram_tier_writes_into_hot_through_the_entry(fake, tmp_path):
    """T2 (F2, behavioural) -- shipped ram-tier.sh ensure, fakes only: tier a real dir, restore a missing one, then an emptied HOT; every write INTO hot is scoped (exactly 10), the cold-bound ones never are."""
    hot, cold, home = tmp_path / "hot", tmp_path / "cold", tmp_path / "home"
    hot.mkdir(); (home / ".claude").mkdir(parents=True); (home / ".claude" / "a").write_text("a")
    (cold / "pi").mkdir(parents=True); (cold / "pi" / "b").write_text("b")
    _install(fake["dir"], "findmnt", "#!/bin/sh\necho tmpfs\n")
    env = dict(_shell_env(fake, tmp_path, hot), GUARD_BOX="tbox", GUARD_ENV_NODE=str(tmp_path / "none"),
               GUARD_TIER_HOT_tbox=str(hot), GUARD_TIER_COLD_tbox=str(cold), GUARD_TIER_DIRS_tbox=f"{home}/.claude {home}/.pi")
    for i in range(2):
        r = _run(env, f"bash {GUARD / 'ram-tier.sh'} ensure")
        assert r.returncode == 0, r.stderr
        _ = i or (shutil.rmtree(hot / "claude"), (hot / "claude").mkdir())   # the reboot: HOT empties
    assert (hot / "claude" / "a").read_text() == "a" == (cold / "claude" / "a").read_text()
    assert (home / ".pi").is_symlink() and (hot / "pi" / "b").read_text() == "b"
    assert [l for l in _entries(fake) if SCOPE_FLAG not in l and _writes_under(l, hot)] == []
    scoped = [l for l in _entries(fake) if SCOPE_FLAG in l]
    assert len(scoped) == 10 and all(_writes_under(l, hot) for l in scoped), scoped
