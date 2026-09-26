"""hypothesis:mem-cap-probe-cache-is-private-and-atomic -- the RESIDUE round.

Kid a00-d8e5d627 built the private, atomic probe cache and left two literals
behind: the base dir `/tmp` and the cache dir NAME. Owner rule (2026-09-23,
"template max and config max everything"): a path a script relies on is a
named variable read at runtime, never a literal in code.

What these tests pin:

  1. the NAMES come from the config cell `values.memcap`, and a caller with no
     config still gets the shipped defaults (the launch hot path must not have
     to resolve the graph);
  2. a cell carrying a path separator is REFUSED, not joined -- otherwise
     config-max would become a new way to move the cache somewhere the
     ownership checks would trust;
  3. the BASE is `tempfile.gettempdir()` ($TMPDIR, else the box temp dir) --
     the same resolver every other engine temp path uses -- so this file (and
     mem_cap.py) spell no box root;
  4. the hot path is not deadlocked by the lookup: `wrap_argv` takes the config
     the CALLER already has (dispatch.py resolves cfg long before it launches)
     and never resolves a graph itself.

NEVER a real `systemd-run`
(hypothesis:launch-memory-cap-tests-never-touch-real-systemd).
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
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


def _cfg(dir_name=None, file_name=None):
    mem = {}
    if dir_name is not None:
        mem["probe_cache_dir_name"] = dir_name
    if file_name is not None:
        mem["probe_cache_file"] = file_name
    return {"values": {"memcap": mem}}


def test_the_names_come_from_the_config_cell(cache_home):
    assert mem_cap._probe_cache_path(_cfg("cfg-dir", "cfg-probe")) == (
        cache_home / "cfg-dir" / "cfg-probe")
    assert mem_cap._probe_cache_path() == (
        cache_home / mem_cap._CACHE_DIR_NAME / mem_cap._CACHE_FILE_NAME)
    # a cell that omits a key keeps the shipped default for THAT key only
    assert mem_cap._probe_cache_path(_cfg("cfg-dir")).name == "probe"
    assert mem_cap._probe_cache_path(_cfg(None, "p")).parent.name == (
        mem_cap._CACHE_DIR_NAME)


def test_the_shipped_config_agrees_with_the_defaults(cache_home):
    """`.agi/config.json` carries the cells, and they resolve to the defaults
    the code falls back to -- the round is a move, not a rename."""
    cfg = json.loads(
        (Path(__file__).resolve().parents[3] / ".agi" / "config.json")
        .read_text(encoding="utf-8"))
    mem = cfg["values"]["memcap"]
    assert mem["probe_cache_dir_name"] == mem_cap._CACHE_DIR_NAME
    assert mem["probe_cache_file"] == mem_cap._CACHE_FILE_NAME


@pytest.mark.parametrize("bad", ["../escape", "a/b", "..", ".", "x\0y"])
def test_a_name_that_could_move_the_cache_is_refused(cache_home, bad):
    """Fail closed: an unusable cell costs a re-probe, never a cache that
    `_private_dir` would have trusted somewhere it does not belong. An EMPTY
    or absent cell is not "unusable" -- it means the shipped default."""
    assert mem_cap._probe_cache_path(_cfg(bad)) is None
    assert mem_cap._probe_cache_path(_cfg("")) == (
        cache_home / mem_cap._CACHE_DIR_NAME / "probe")
    assert not (cache_home.parent / "escape").exists()


def test_the_base_is_the_platform_temp_dir(cache_home, monkeypatch):
    """No `/tmp` literal: `$TMPDIR` wins, exactly as the stdlib resolves it."""
    monkeypatch.delenv("XDG_RUNTIME_DIR", raising=False)
    monkeypatch.setenv("TMPDIR", str(cache_home))
    monkeypatch.setattr(mem_cap.tempfile, "tempdir", None)  # drop the cache
    assert mem_cap.tempfile.gettempdir() == str(cache_home)
    assert mem_cap._probe_cache_path(_cfg("d")) == cache_home / "d" / "probe"
    src = (BIN / "mem_cap.py").read_text(encoding="utf-8")
    assert '"/tmp"' not in src and "'/tmp'" not in src


def test_wrap_argv_forwards_the_config_the_caller_already_has(monkeypatch):
    """The hot path never resolves the graph: `wrap_argv` takes the cfg its
    caller already holds (dispatch.py has had `cfg` for a thousand lines by
    the time it launches) or nothing."""
    seen = []
    monkeypatch.setattr(
        mem_cap, "systemd_run_usable",
        lambda cfg=None: seen.append(cfg) or True)
    out = mem_cap.wrap_argv(["true"], "4G", _cfg("hot-dir"))
    assert out[0] == "systemd-run" and out[-1] == "true"
    assert seen == [_cfg("hot-dir")]
    seen.clear()
    mem_cap.wrap_argv(["true"], "4G")
    assert seen == [None], "a caller with no config must still get the defaults"


def test_a_round_trip_under_a_configured_name(cache_home):
    """The verdict written under a configured name reads back under it."""
    cfg = _cfg("rt-dir")
    mem_cap._write_cached_probe(True, cfg)
    assert mem_cap._read_cached_probe(cfg) is True
    assert mem_cap._read_cached_probe() is None  # a different cache, not this one
    assert os.lstat(cache_home / "rt-dir" / "probe").st_uid == os.geteuid()
