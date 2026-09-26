"""hypothesis:mem-cap-probe-cache-is-private-and-atomic.

The probe verdict cache is a cross-process trust surface: it lives at a
PREDICTABLE name, so another local user can pre-create the dir, the file, or a
symlink where it will land. These tests pin the three defences -- a private
dir we own at 0700, an atomic replace, and a refusal to read anything that is
not our own regular file holding a whole verdict.

NEVER a real `systemd-run`: the probe is never invoked here, only the cache
read/write around it (hypothesis:launch-memory-cap-tests-never-touch-real-
systemd).
"""
from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import mem_cap  # noqa: E402


@pytest.fixture
def cache_home(tmp_path, monkeypatch):
    """A private per-user runtime dir standing in for `$XDG_RUNTIME_DIR`."""
    monkeypatch.delenv("AGI_MEMCAP_SYSTEMD_RUN", raising=False)
    monkeypatch.delenv("AGI_MEMCAP_CACHE", raising=False)
    run = tmp_path / "run"
    run.mkdir(mode=0o700)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(run))
    return run


def test_cache_lives_in_a_private_dir_we_own(cache_home):
    path = mem_cap._probe_cache_path()
    assert path is not None
    parent = path.parent
    assert parent == cache_home / mem_cap._CACHE_DIR_NAME
    assert stat.S_IMODE(os.lstat(parent).st_mode) == 0o700
    assert os.lstat(parent).st_uid == os.geteuid()


def test_a_foreign_owned_cache_dir_is_refused(cache_home, monkeypatch):
    """A dir another user pre-created is not ours to write a verdict into.

    Ownership cannot be faked without root, so the check under test -- "is
    this dir MINE" -- is exercised by moving the observer, not the inode.
    """
    foreign = cache_home / mem_cap._CACHE_DIR_NAME
    foreign.mkdir(mode=0o777)
    os.chmod(foreign, 0o777)
    real = mem_cap._private_dir(foreign)
    assert real is not None and stat.S_IMODE(os.lstat(foreign).st_mode) == 0o700

    monkeypatch.setattr(mem_cap.os, "geteuid", lambda: os.lstat(foreign).st_uid + 1)
    assert mem_cap._private_dir(foreign) is None
    assert mem_cap._probe_cache_path() is None
    assert mem_cap._read_cached_probe() is None
    assert mem_cap._write_cached_probe(True) is None  # never raises
    assert not (foreign / "probe").exists()


def test_write_is_atomic_and_leaves_no_partial_file(cache_home):
    mem_cap._write_cached_probe(True)
    path = mem_cap._probe_cache_path()
    assert path.read_text() == f"{mem_cap._boot_id()} 1\n"
    assert mem_cap._read_cached_probe() is True
    # the temp file is gone -- os.replace consumed it
    assert [p.name for p in path.parent.iterdir()] == ["probe"]


def test_a_symlink_at_the_cache_path_is_not_followed_or_trusted(cache_home, tmp_path):
    target = tmp_path / "planted"
    target.write_text(f"{mem_cap._boot_id()} 1\n")
    path = cache_home / mem_cap._CACHE_DIR_NAME / "probe"
    path.parent.mkdir(mode=0o700, exist_ok=True)
    path.symlink_to(target)
    assert mem_cap._read_cached_probe() is None
    mem_cap._write_cached_probe(False)
    assert target.read_text() == f"{mem_cap._boot_id()} 1\n"  # untouched
    assert not path.is_symlink() and path.read_text() == f"{mem_cap._boot_id()} 0\n"


def test_a_foreign_owned_cache_file_is_not_trusted(cache_home, monkeypatch):
    path = cache_home / mem_cap._CACHE_DIR_NAME / "probe"
    path.parent.mkdir(mode=0o700, exist_ok=True)
    path.write_text(f"{mem_cap._boot_id()} 1\n")
    monkeypatch.setattr(mem_cap.os, "geteuid", lambda: os.lstat(path).st_uid + 1)
    assert mem_cap._read_cached_probe() is None


@pytest.mark.parametrize("body", ["", "x", "1 1", "maybe", "01", "true"])
def test_a_partial_or_corrupt_body_is_re_probed_not_read_as_false(cache_home, body):
    path = cache_home / mem_cap._CACHE_DIR_NAME / "probe"
    path.parent.mkdir(mode=0o700, exist_ok=True)
    path.write_text(f"{mem_cap._boot_id()} {body}\n")
    assert mem_cap._read_cached_probe() is None


def test_a_stale_boot_id_is_re_probed(cache_home):
    path = cache_home / mem_cap._CACHE_DIR_NAME / "probe"
    path.parent.mkdir(mode=0o700, exist_ok=True)
    path.write_text("not-a-boot-id 1\n")
    assert mem_cap._read_cached_probe() is None


def test_the_env_override_is_honoured_verbatim(tmp_path, monkeypatch):
    f = tmp_path / "cache-file"
    monkeypatch.setenv("AGI_MEMCAP_CACHE", str(f))
    mem_cap._write_cached_probe(False)
    assert mem_cap._probe_cache_path() == f
    assert mem_cap._read_cached_probe() is False
