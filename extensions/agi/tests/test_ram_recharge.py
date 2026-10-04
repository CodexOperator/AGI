"""goal:g7.16.1.5.5.6.1 -- mem_cap.py ram-recharge.

A tmp tree: nested other-dev stand-in, write-open file, hardlink pair,
mode-000 file. Counts only, no paths. Never rglob."""
from __future__ import annotations

import os
import stat
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import mem_cap  # noqa: E402


def test_missing_dir_names_the_verb(tmp_path):
    r = mem_cap.recharge_tree(str(tmp_path / "gone"))
    assert r[0] == 2 and r[1:] == (0, 0, 0)
    p = __import__("subprocess").run(
        [sys.executable, str(BIN / "mem_cap.py"), "ram-recharge", str(tmp_path / "gone")],
        capture_output=True, text=True)
    assert p.returncode == 2 and "ram-recharge" in p.stderr and str(tmp_path) not in p.stderr


def test_keeps_bytes_mode_mtime_and_hardlinks(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_bytes(b"hello-recharge")
    os.chmod(a, 0o640)
    past = time.time() - 86_400
    os.utime(a, (past, past))
    os.link(a, b)
    ino = a.stat().st_ino
    mode = stat.S_IMODE(a.stat().st_mode)
    mtime = a.stat().st_mtime_ns
    rc, rw, sk, fl = mem_cap.recharge_tree(str(tmp_path))
    assert (rc, rw, sk, fl) == (0, 1, 0, 0)
    assert a.read_bytes() == b"hello-recharge"
    assert b.read_bytes() == b"hello-recharge"
    assert a.stat().st_ino == b.stat().st_ino
    assert a.stat().st_ino != ino  # rewritten onto a new inode
    assert stat.S_IMODE(a.stat().st_mode) == mode
    assert abs(a.stat().st_mtime_ns - mtime) < 1_000_000_000


def test_skips_write_open_mode_000_and_other_dev(tmp_path, monkeypatch):
    keep = tmp_path / "keep.txt"
    keep.write_text("keep")
    nested = tmp_path / "mnt"
    nested.mkdir()
    other = nested / "other.txt"
    other.write_text("other-dev")
    locked = tmp_path / "locked.txt"
    locked.write_text("secret")
    os.chmod(locked, 0o000)
    live = tmp_path / "live.txt"
    live.write_text("old")
    root_dev = os.lstat(tmp_path).st_dev
    nested_st = os.lstat(nested)
    other_st = os.lstat(other)

    def fake_lstat(path):
        p = os.path.realpath(path)
        if p == os.path.realpath(nested) or p.startswith(os.path.realpath(nested) + os.sep):
            st = nested_st if os.path.isdir(path) or p == os.path.realpath(nested) else other_st
            return os.stat_result((st.st_mode, st.st_ino, root_dev + 1, st.st_nlink,
                                   st.st_uid, st.st_gid, st.st_size,
                                   st.st_atime, st.st_mtime, st.st_ctime))
        return os.lstat(path)

    monkeypatch.setattr(mem_cap, "_lstat", fake_lstat)
    try:
        with live.open("w") as fh:
            fh.write("LIVE")
            fh.flush()
            rc, rw, sk, fl = mem_cap.recharge_tree(str(tmp_path))
    finally:
        os.chmod(locked, 0o644)
    assert rc == 1 and fl == 0
    assert rw >= 1  # keep.txt
    assert sk >= 2  # live write-open + locked + other-dev
    assert live.read_text() == "LIVE"
    assert other.read_text() == "other-dev"
    assert keep.read_text() == "keep"
    leftovers = list(tmp_path.rglob(".agi-recharge-*"))
    assert leftovers == []


def test_dry_run_counts_only(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text("x")
    before = p.stat().st_ino
    rc, rw, sk, fl = mem_cap.recharge_tree(str(tmp_path), dry_run=True)
    assert (rc, rw, sk, fl) == (0, 1, 0, 0)
    assert p.stat().st_ino == before
    r = __import__("subprocess").run(
        [sys.executable, str(BIN / "mem_cap.py"), "ram-recharge", "--dry-run", str(tmp_path)],
        capture_output=True, text=True)
    assert r.returncode == 0 and "dry-run" in r.stderr and "rewritten=1" in r.stderr
    assert str(tmp_path) not in r.stderr
    assert p.stat().st_ino == before


def test_no_rglob_in_recharge():
    src = (BIN / "mem_cap.py").read_text()
    assert "rglob(" not in src and ".rglob" not in src
    # same-device check is the walk, not a glob
    assert "_walk_same_dev" in src and "st_dev" in src


def test_no_scope_fail_closed(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("x")
    monkeypatch.setattr(mem_cap, "user_manager_reachable", lambda: False)
    monkeypatch.setattr(mem_cap, "_in_ram_slice", lambda: False)
    monkeypatch.delenv("AGI_RAM_RECHARGE_SCOPED", raising=False)
    rc = mem_cap._verb_ram_recharge(str(tmp_path), dry_run=False)
    err = capsys.readouterr().err
    assert rc == 2 and "UNREACHABLE" in err
    assert (tmp_path / "a.txt").read_text() == "x"


def test_unreadable_leaves_no_tempfile(tmp_path, monkeypatch):
    p = tmp_path / "gone-under.txt"
    p.write_text("x")

    def boom(*_a, **_k):
        raise OSError("nope")

    monkeypatch.setattr(mem_cap, "_relink_group", boom)
    rc, rw, sk, fl = mem_cap.recharge_tree(str(tmp_path))
    assert rc == 1 and fl == 1 and rw == 0
    assert list(tmp_path.rglob(".agi-recharge-*")) == []
