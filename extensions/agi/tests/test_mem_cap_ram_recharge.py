"""goal:g7.16.1.5.5.6.1 -- `mem_cap.recharge` / `ram-recharge`: the one-shot that
re-allocates a RAM tree's pages without crossing a mount, losing a held write,
resetting an mtime, splitting a hardlink pair, leaving a tempfile or exiting 0
on a failure. Rows R1-R9 are DG5's list for mur g7556's UNSAFE first build
(rglob + mkstemp + copyfile + chmod + replace, no guards): each row is a function
of a module, run on the real `mem_cap` (must PASS) and on a MUTANT with exactly
one guard removed (must FAIL that row). Nothing here spawns a scope."""
from __future__ import annotations

import os
import subprocess
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bin"))
import mem_cap  # noqa: E402

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "mem_cap.py")
SRC = open(BIN).read()
NOT_ROOT = pytest.mark.skipif(os.geteuid() == 0, reason="root reads a mode-000 file")


def mutant(old: str, new: str) -> types.ModuleType:
    """mem_cap with ONE guard edited out; the edit must find its text."""
    assert SRC.count(old) == 1, f"mutation anchor not found once: {old!r}"
    mod = types.ModuleType("mem_cap_mutant")
    mod.__file__ = BIN
    exec(compile(SRC.replace(old, new), BIN, "exec"), mod.__dict__)
    return mod


def _tree(tmp_path):
    root = tmp_path / "ram"
    (root / "mnt").mkdir(parents=True)
    (root / "a.txt").write_text("alpha")
    (root / "mnt" / "disk.txt").write_text("on another device")
    (root / "ro.txt").write_text("readable")
    return root


def _leftovers(root):
    return list(root.rglob(".recharge.*"))


def _ino(p):
    return os.stat(p).st_ino


# ---- the rows: each takes (mod, tmp_path) and asserts ------------------------
def r1_mount(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    real = mod._dev_of
    monkeypatch.setattr(mod, "_dev_of", lambda p: real(p) + 1 if p.endswith("/mnt") else real(p))
    ino = _ino(root / "mnt" / "disk.txt")
    n = mod.recharge(str(root))
    assert _ino(root / "mnt" / "disk.txt") == ino
    assert (root / "mnt" / "disk.txt").read_text() == "on another device"
    assert n["crossed"] == 1 and n["rewritten"] == 2 and n["skipped"] == 0


def r2_open_for_write(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    ino = _ino(root / "a.txt")
    with open(root / "a.txt", "r+") as held:          # this very process holds it
        n = mod.recharge(str(root))
        held.seek(0, 2)
        held.write("-late")                           # a write AFTER the recharge
    assert n["skipped"] == 1 and n["rewritten"] == 2
    assert _ino(root / "a.txt") == ino
    assert (root / "a.txt").read_text() == "alpha-late"


def r2_read_only_fd_does_not_count(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    with open(root / "a.txt", "r"):
        n = mod.recharge(str(root))
    assert n["skipped"] == 0 and n["rewritten"] == 3


def r2_toctou(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    ino = _ino(root / "a.txt")

    def late(path):
        if path.endswith("a.txt"):
            with open(path, "a") as f:
                f.write("-late")
    monkeypatch.setattr(mod, "_before_replace", late)
    n = mod.recharge(str(root))
    assert n["skipped"] == 1
    assert _ino(root / "a.txt") == ino and (root / "a.txt").read_text() == "alpha-late"
    assert _leftovers(root) == []


def r3_mtime(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    os.utime(root / "a.txt", ns=(1_000_000_000, 2_000_000_000))
    ino = _ino(root / "a.txt")
    mod.recharge(str(root))
    assert _ino(root / "a.txt") != ino                # really rewritten
    assert os.stat(root / "a.txt").st_mtime_ns == 2_000_000_000


def r3_mode(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    os.chmod(root / "ro.txt", 0o444)
    mod.recharge(str(root))
    assert os.stat(root / "ro.txt").st_mode & 0o777 == 0o444


def r4_hardlinks(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    os.link(root / "a.txt", root / "b.txt")
    n = mod.recharge(str(root))
    assert n["rewritten"] == 4 and n["failed"] == 0
    assert _ino(root / "a.txt") == _ino(root / "b.txt") and os.stat(root / "a.txt").st_nlink == 2


def r4_outside_name_skips_whole_set(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    os.link(root / "a.txt", tmp_path / "outside.txt")
    n = mod.recharge(str(root))
    assert n["skipped"] == 1
    assert _ino(root / "a.txt") == _ino(tmp_path / "outside.txt")


def r5_copy_raises_midway(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)

    def boom(*a, **k):
        raise OSError("disk full")
    monkeypatch.setattr(mod.shutil, "copyfileobj", boom)
    before = sorted(os.listdir(root))
    n = mod.recharge(str(root))
    assert n["failed"] == 3 and n["rewritten"] == 0
    assert sorted(os.listdir(root)) == before and _leftovers(root) == []


def r5_unreadable(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    os.chmod(root / "ro.txt", 0)
    before = sorted(os.listdir(root))
    try:
        n = mod.recharge(str(root))
    finally:
        os.chmod(root / "ro.txt", 0o644)
    assert n["failed"] == 1 and sorted(os.listdir(root)) == before


def r9_symlinks(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "x.txt").write_text("not yours")
    os.symlink(root / "a.txt", root / "link-in")
    os.symlink(outside / "x.txt", root / "link-out")
    os.symlink(outside, root / "dirlink")
    oino = _ino(outside / "x.txt")
    mod.recharge(str(root))
    assert all(os.path.islink(root / n) for n in ("link-in", "link-out", "dirlink"))
    assert os.readlink(root / "link-out") == str(outside / "x.txt")
    assert _ino(outside / "x.txt") == oino and (outside / "x.txt").read_text() == "not yours"


def _verb(mod, root, monkeypatch):
    """(rc, stdout+stderr) of the verb already inside its scope."""
    import contextlib
    import io
    monkeypatch.setenv(mod._RECHARGE_ENV, "1")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = mod._verb_ram_recharge([str(root)])
    return rc, buf.getvalue()


def rA_unreadable_directory(mod, tmp_path, monkeypatch):
    if os.geteuid() == 0:
        pytest.skip("root reads a mode-000 dir")
    root = _tree(tmp_path)
    sub = root / "sub"
    sub.mkdir()
    (sub / "hidden.txt").write_text("x")
    os.chmod(sub, 0)
    try:
        n = mod.recharge(str(root))
        rc, out = _verb(mod, root, monkeypatch)
    finally:
        os.chmod(sub, 0o755)
    assert n["failed"] >= 1 and rc == 1
    assert str(tmp_path) not in out


def rB_vanished_entry(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    real = os.lstat

    def gone(path, *a, **k):
        if str(path).endswith("ro.txt"):
            raise FileNotFoundError(path)
        return real(path, *a, **k)
    monkeypatch.setattr(mod.os, "lstat", gone)
    rc, out = _verb(mod, root, monkeypatch)             # no exception out of the verb
    assert rc == 1 and "failed=1" in out and str(tmp_path) not in out


def rC_setid_bits_survive(mod, tmp_path, monkeypatch):
    if os.geteuid() == 0:
        pytest.skip("root's chown keeps setuid/setgid, so the order cannot show")
    root = _tree(tmp_path)
    os.chmod(root / "a.txt", 0o2755)
    os.chmod(root / "ro.txt", 0o4755)
    mod.recharge(str(root))
    assert os.stat(root / "a.txt").st_mode & 0o7777 == 0o2755
    assert os.stat(root / "ro.txt").st_mode & 0o7777 == 0o4755


def rD_late_opener(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    monkeypatch.setattr(mod, "_RESCAN_AFTER", 0)
    keep = []

    def open_late(path):
        if path.endswith("a.txt"):
            keep.append(open(path, "r+"))               # opens r+, has not written yet
    monkeypatch.setattr(mod, "_before_replace", open_late)
    ino = _ino(root / "a.txt")
    try:
        n = mod.recharge(str(root))
        keep[0].seek(0, 2)
        keep[0].write("-NEW")
        keep[0].flush()
    finally:
        keep[0].close()
    assert n["skipped"] == 1 and _ino(root / "a.txt") == ino
    assert (root / "a.txt").read_text() == "alpha-NEW" and _leftovers(root) == []


def rE_bind_mounted_file(mod, tmp_path, monkeypatch):
    root = _tree(tmp_path)
    real = os.lstat

    def bound(path, *a, **k):
        st = real(path, *a, **k)
        if str(path).endswith("ro.txt"):
            f = {k2: getattr(st, k2) for k2 in dir(st) if k2.startswith("st_")}
            f["st_dev"] += 1
            return types.SimpleNamespace(**f)
        return st
    monkeypatch.setattr(mod.os, "lstat", bound)
    ino = _ino(root / "ro.txt")
    n = mod.recharge(str(root))
    assert n["crossed"] == 1 and n["rewritten"] == 2 and _ino(root / "ro.txt") == ino


# (row, guard removed, replacement) -- ONE edit each; the row must go RED on it.
ROWS = [
    (r1_mount, "and _dev_of(os.path.join(d, x)) == top]", "]"),
    (r2_open_for_write, "if key in held or st.st_nlink", "if st.st_nlink"),
    (r2_toctou, "if (now.st_ino, now.st_size, now.st_mtime_ns) != (st.st_ino, st.st_size, st.st_mtime_ns):", "if False:"),
    (r3_mtime, "shutil.copystat(names[0], tmp)", "pass"),
    (r3_mode, "shutil.copystat(names[0], tmp)", "pass"),
    (r4_hardlinks, "for other in names[1:]:", "for other in []:"),
    (r4_outside_name_skips_whole_set, "st.st_nlink != len(names)", "False"),
    (rA_unreadable_directory, "followlinks=False, onerror=unreadable)", "followlinks=False)"),
    (rB_vanished_entry, "            try:\n                st = os.lstat(path)\n            except OSError:\n                n[\"failed\"] += 1\n                continue\n",
     "            st = os.lstat(path)\n"),
    (rC_setid_bits_survive, "os.chown(tmp, st.st_uid, st.st_gid)     # BEFORE copystat: a non-root chown clears setuid/setgid\n            shutil.copystat(names[0], tmp)",
     "shutil.copystat(names[0], tmp)\n            os.chown(tmp, st.st_uid, st.st_gid)"),
    (rD_late_opener, "if time.monotonic() - scan_t > _RESCAN_AFTER:", "if False:"),
    (rE_bind_mounted_file, "if st.st_dev != top:        # a bind-mounted FILE", "if False:"),
    (r5_copy_raises_midway, "            if tmp is not None:\n                try:\n                    os.unlink(tmp)",
     "            if False:\n                try:\n                    os.unlink(tmp)"),
]
PLAIN = [r2_read_only_fd_does_not_count, r9_symlinks]


@pytest.mark.parametrize("row", [r[0] for r in ROWS] + PLAIN + [r5_unreadable], ids=lambda f: f.__name__)
def test_real_module_passes_the_row(row, tmp_path, monkeypatch):
    if row is r5_unreadable and os.geteuid() == 0:
        pytest.skip("root reads a mode-000 file")
    row(mem_cap, tmp_path, monkeypatch)


@pytest.mark.parametrize("row,old,new", ROWS, ids=lambda x: getattr(x, "__name__", None) or None)
def test_mutant_turns_the_row_red(row, old, new, tmp_path, monkeypatch):
    with pytest.raises(Exception):      # an AssertionError, or the traceback the guard exists to prevent
        row(mutant(old, new), tmp_path, monkeypatch)


@NOT_ROOT
def test_r5_unreadable_mutant_leaves_the_tempfile(tmp_path, monkeypatch):
    """The unsafe shape (no cleanup) on a mode-000 file: the tempfile stays."""
    m = mutant("            if tmp is not None:\n                try:\n                    os.unlink(tmp)",
               "            if False:\n                try:\n                    os.unlink(tmp)")
    with pytest.raises(AssertionError):
        r5_unreadable(m, tmp_path, monkeypatch)


def test_r2_read_only_mutant_counts_a_reader(tmp_path, monkeypatch):
    """If the scan counted a read-only fd, the row would go RED."""
    m = mutant("if flags & os.O_ACCMODE != os.O_RDONLY:", "if True:")
    with pytest.raises(AssertionError):
        r2_read_only_fd_does_not_count(m, tmp_path, monkeypatch)


def test_r2_scan_includes_its_own_pid(tmp_path):
    p = tmp_path / "f"
    p.write_text("x")
    with open(p, "r+"):
        assert (os.stat(p).st_dev, os.stat(p).st_ino) in mem_cap._open_for_write()


# ---- R6 / R7: the verb's exit codes, counts and dry-run ---------------------
def _run(*args, env=None):
    return subprocess.run([sys.executable, BIN, "ram-recharge", *args],
                          capture_output=True, text=True, env=env)


def test_r6_clean_tree_in_scope_rc0_counts_only(tmp_path):
    root = _tree(tmp_path)
    r = _run(str(root), env=dict(os.environ, **{mem_cap._RECHARGE_ENV: "1"}))
    assert r.returncode == 0
    assert r.stdout.strip() == "recharged=3 skipped=0 failed=0 crossed=0"
    assert str(tmp_path) not in r.stdout + r.stderr and ".recharge" not in r.stdout + r.stderr


def test_r6_missing_dir_is_nonzero(tmp_path):
    assert _run(str(tmp_path / "nope")).returncode != 0


def test_r6_a_skipped_file_is_nonzero_and_names_no_path(tmp_path):
    root = _tree(tmp_path)
    with open(root / "a.txt", "r+"):                  # the child sees THIS process's fd
        r = _run(str(root), env=dict(os.environ, **{mem_cap._RECHARGE_ENV: "1"}))
    assert r.returncode == 1 and "skipped=1" in r.stdout
    assert str(tmp_path) not in r.stdout + r.stderr


def test_r6_mutant_exit_zero_on_skip_is_red(tmp_path, monkeypatch):
    """The unsafe shape exits 0 whatever happened: with the rc rule removed a held file still gives 0."""
    root = _tree(tmp_path)
    monkeypatch.setenv(mem_cap._RECHARGE_ENV, "1")
    m = mutant('return 0 if not (n["skipped"] or n["failed"]) else 1', "return 0")
    with open(root / "a.txt", "r+"):
        assert m._verb_ram_recharge([str(root)]) == 0          # the mutant is the unsafe shape
        assert mem_cap._verb_ram_recharge([str(root)]) == 1    # the real one is not


def test_r7_dry_run_changes_nothing_and_follows_the_rc_rule(tmp_path):
    root = _tree(tmp_path)
    os.utime(root / "a.txt", ns=(1_000_000_000, 2_000_000_000))
    before = {p.name: (_ino(p), os.stat(p).st_mtime_ns) for p in root.iterdir() if p.is_file()}
    r = _run("--dry-run", str(root))
    assert r.returncode == 0 and r.stdout.strip() == "recharged=3 skipped=0 failed=0 crossed=0 dry-run"
    assert before == {p.name: (_ino(p), os.stat(p).st_mtime_ns) for p in root.iterdir() if p.is_file()}
    assert _leftovers(root) == []
    with open(root / "a.txt", "r+"):
        assert _run("--dry-run", str(root)).returncode == 1


# ---- R8: scope -------------------------------------------------------------
def test_r8_one_scope_argv_on_the_ram_slice_built_by_scope_argv(tmp_path, monkeypatch):
    root = _tree(tmp_path)
    seen = []
    monkeypatch.delenv(mem_cap._RECHARGE_ENV, raising=False)
    monkeypatch.setattr(mem_cap, "user_manager_reachable", lambda: True)
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    monkeypatch.setattr(mem_cap.os, "execvp", lambda f, argv: seen.append(list(argv)))
    ino = _ino(root / "a.txt")
    mem_cap._verb_ram_recharge([str(root)])
    (argv,) = seen
    assert argv.count("systemd-run") == 1 and "--scope" in argv and "--slice=ramdisk.slice" in argv
    assert argv[argv.index("--") + 1:][1:] == [os.path.abspath(BIN), "ram-recharge", str(root)]
    assert os.environ[mem_cap._RECHARGE_ENV] == "1"
    assert _ino(root / "a.txt") == ino                 # the walk runs INSIDE the scope, not here


def test_r8_no_usable_scope_touches_nothing_and_exits_3(tmp_path, monkeypatch):
    root = _tree(tmp_path)
    monkeypatch.delenv(mem_cap._RECHARGE_ENV, raising=False)
    monkeypatch.setattr(mem_cap, "user_manager_reachable", lambda: False)
    ino = _ino(root / "a.txt")
    assert mem_cap._verb_ram_recharge([str(root)]) == 3
    assert _ino(root / "a.txt") == ino


def test_r8_no_second_scope_argv_and_never_a_timer():
    body = SRC[SRC.index("def recharge("):]
    body = body[:body.index('if __name__ == "__main__"')]
    assert "systemd-run" not in body and "--scope" not in body
    tracked = subprocess.run(["git", "ls-files", "*.timer", "*.service"], capture_output=True, text=True,
                             cwd=os.path.dirname(BIN)).stdout.split()
    assert not [f for f in tracked if "recharge" in open(os.path.join(os.path.dirname(BIN), "..", "..", "..", f)).read()]


def test_f2_negative_no_walk_without_a_device_check():
    body = SRC[SRC.index("def recharge("):SRC.index("def _verb_ram_recharge")]
    assert "rglob" not in body and "_dev_of" in body
