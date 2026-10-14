"""goal:g7.16.1.5.5.6.1 -- `mem_cap.recharge` / `ram-recharge`: the one-shot that
re-allocates a RAM tree's pages without ever crossing a mount, losing a held
write, or leaving a tempfile. Every row runs on a tmp tree: nothing here spawns
a scope (the verb's scope re-exec is asserted on its exit code only)."""
from __future__ import annotations

import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bin"))
import mem_cap  # noqa: E402

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "mem_cap.py")


def _tree(tmp_path):
    root = tmp_path / "ram"
    (root / "mnt").mkdir(parents=True)
    (root / "a.txt").write_text("alpha")
    (root / "mnt" / "disk.txt").write_text("on another device")
    (root / "ro.txt").write_text("readable")
    os.utime(root / "a.txt", ns=(1_000_000_000, 2_000_000_000))
    return root


def _leftovers(root):
    return [p for p in root.rglob(".recharge.*")]


def test_f1_clean_tree_rewrites_keeps_bytes_mode_mtime_and_hardlinks(tmp_path):
    root = _tree(tmp_path)
    os.link(root / "a.txt", root / "a2.txt")
    os.chmod(root / "ro.txt", 0o444)
    ino_before = os.stat(root / "ro.txt").st_ino
    n = mem_cap.recharge(str(root))
    assert n == {"rewritten": 4, "skipped": 0, "failed": 0}
    assert (root / "a.txt").read_text() == "alpha"
    assert os.stat(root / "a.txt").st_mtime_ns == 2_000_000_000
    assert os.stat(root / "ro.txt").st_mode & 0o777 == 0o444
    assert os.stat(root / "ro.txt").st_ino != ino_before          # really rewritten
    assert os.stat(root / "a.txt").st_ino == os.stat(root / "a2.txt").st_ino
    assert os.stat(root / "a.txt").st_nlink == 2
    assert _leftovers(root) == []


def test_f1_never_enters_a_mount(tmp_path, monkeypatch):
    root = _tree(tmp_path)
    real = mem_cap._dev_of
    monkeypatch.setattr(mem_cap, "_dev_of",
                        lambda p: real(p) + 1 if p.endswith("/mnt") else real(p))
    ino = os.stat(root / "mnt" / "disk.txt").st_ino
    n = mem_cap.recharge(str(root))
    assert n["rewritten"] == 2 and n["failed"] == 0
    assert os.stat(root / "mnt" / "disk.txt").st_ino == ino


def test_f1_open_for_write_file_is_skipped_and_keeps_its_writer(tmp_path):
    root = _tree(tmp_path)
    with open(root / "a.txt", "a") as held:
        ino = os.stat(root / "a.txt").st_ino
        n = mem_cap.recharge(str(root))
        held.write("-more")
        held.flush()
    assert n["skipped"] == 1 and n["rewritten"] == 2
    assert os.stat(root / "a.txt").st_ino == ino
    assert (root / "a.txt").read_text() == "alpha-more"


def test_f1_hardlink_with_a_name_outside_the_tree_is_skipped_whole(tmp_path):
    root = _tree(tmp_path)
    os.link(root / "a.txt", tmp_path / "outside.txt")
    n = mem_cap.recharge(str(root))
    assert n["skipped"] == 1
    assert os.stat(root / "a.txt").st_ino == os.stat(tmp_path / "outside.txt").st_ino


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads a mode-000 file")
def test_f1_unreadable_file_leaves_no_tempfile_and_counts_failed(tmp_path):
    root = _tree(tmp_path)
    os.chmod(root / "ro.txt", 0)
    n = mem_cap.recharge(str(root))
    assert n["failed"] == 1 and n["rewritten"] == 2
    assert _leftovers(root) == []
    os.chmod(root / "ro.txt", 0o644)


def test_dry_run_writes_nothing_and_prints_counts_only(tmp_path):
    root = _tree(tmp_path)
    ino = os.stat(root / "a.txt").st_ino
    r = subprocess.run([sys.executable, BIN, "ram-recharge", "--dry-run", str(root)],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert r.stdout.strip() == "would-rewrite=3 skipped=0 failed=0"
    assert str(root) not in r.stdout + r.stderr
    assert os.stat(root / "a.txt").st_ino == ino


def test_missing_dir_exits_nonzero(tmp_path):
    r = subprocess.run([sys.executable, BIN, "ram-recharge", str(tmp_path / "nope")],
                       capture_output=True, text=True)
    assert r.returncode == 1


def test_skipped_file_makes_the_verb_exit_nonzero(tmp_path):
    root = _tree(tmp_path)
    env = dict(os.environ, **{mem_cap._RECHARGE_ENV: "1"})
    with open(root / "a.txt", "a"):
        # the child is a different process: hold the file open in THIS one and
        # ask the child to run the dry pass, which counts the same skip
        r = subprocess.run([sys.executable, BIN, "ram-recharge", "--dry-run", str(root)],
                           capture_output=True, text=True, env=env)
    assert r.returncode == 1 and "skipped=1" in r.stdout


def test_f2_negative_no_walk_without_a_device_check():
    src = open(BIN).read()
    body = src[src.index("def recharge("):src.index("def _verb_ram_recharge")]
    assert "rglob" not in body and "_dev_of" in body
