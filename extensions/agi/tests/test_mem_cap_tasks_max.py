"""TasksMax on the same scope that carries MemoryMax (DH.421,
hypothesis:a00-1ff9316d-177aae -- "a round's kid cannot fan out processes
past the box's bound"). The cell is `values.memcap.tasks_max`; the shipped
default lives in `mem_cap._DEFAULT_TASKS_MAX` so a config with no cell keeps
working (a round may never commit `.agi/config.json`).

The fan-out probe uses `bash` + `sleep` only -- no python, no pytest, nothing
that recurses into the suite -- and every subprocess carries a `timeout`.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import mem_cap  # noqa: E402

WANTED = 18  # < 20 processes even on the uncapped path (the kid-tier rule)


def _cfg(**memcap):
    return {"values": {"memcap": memcap}}


# ---- (1) the cell and the shipped default ----------------------------------

def test_default_is_shipped_when_no_cell_is_present():
    assert mem_cap.resolve_tasks_max() == mem_cap._DEFAULT_TASKS_MAX
    assert mem_cap.resolve_tasks_max({}) == mem_cap._DEFAULT_TASKS_MAX
    assert mem_cap.resolve_tasks_max({"values": {}}) == mem_cap._DEFAULT_TASKS_MAX


def test_the_cell_wins_when_it_is_readable():
    assert mem_cap.resolve_tasks_max(_cfg(tasks_max=8)) == 8
    assert mem_cap.resolve_tasks_max(_cfg(tasks_max="12")) == 12


def test_an_unreadable_cell_falls_back_and_never_uncaps(monkeypatch):
    for bad in (None, "", "abc", 0, -3, {}, []):
        assert mem_cap.resolve_tasks_max(_cfg(tasks_max=bad)) is not None
        assert mem_cap.resolve_tasks_max(_cfg(tasks_max=bad)) == \
            mem_cap._DEFAULT_TASKS_MAX, bad
    monkeypatch.setenv("AGI_TASKS_MAX", "5")
    assert mem_cap.resolve_tasks_max(_cfg(tasks_max=8)) == 5


# ---- (2) the argv ----------------------------------------------------------

def test_systemd_run_argv_carries_both_bounds(monkeypatch):
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    out = mem_cap.wrap_argv(["echo", "x"], "256M", _cfg(tasks_max=8))
    assert out[0] == "systemd-run", out
    assert "--property=MemoryMax=256M" in out, out
    assert "--property=TasksMax=8" in out, out
    assert out[-1] == "x", out


def test_no_cell_means_the_shipped_default_on_the_argv(monkeypatch):
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    out = mem_cap.wrap_argv(["echo", "x"], "256M")
    assert f"--property=TasksMax={mem_cap._DEFAULT_TASKS_MAX}" in out, out


def test_cap_none_is_still_the_same_argv_object():
    argv = ["echo", "hi"]
    assert mem_cap.wrap_argv(argv, None, _cfg(tasks_max=8)) is argv


def test_the_prlimit_fallback_names_no_process_bound_it_cannot_enforce(
        monkeypatch):
    """RLIMIT_NPROC is per-USER, so the fallback has NO per-tree cap. That is
    a NAMED residual in `wrap_argv`'s comment, not a silent hole -- and this
    test fails the day someone pretends otherwise."""
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: False)
    out = mem_cap.wrap_argv(["echo", "x"], "256M", _cfg(tasks_max=8))
    assert out[:2] == ["prlimit", f"--as={256 * 1024 ** 2}"], out
    assert not [a for a in out if "TasksMax" in a or "nproc" in a], out


# ---- (3) the real fan-out: RED on the bound, GREEN on the unwrapped path ----

_FANOUT = """#!/usr/bin/env python3
# Fork W children with NO retry (bash's `&` retries a refused fork with backoff,
# so counting markers measured patience, not the bound -- director-engine, DH.421
# harvest). Every child sleeps while the parent is still forking, so the count is
# CONCURRENT; a refused fork is recorded, never retried.
import os, sys, time
d, w = sys.argv[1], int(sys.argv[2])
os.makedirs(d, exist_ok=True)
ok = refused = 0
for i in range(w):
    try:
        pid = os.fork()
    except OSError:
        refused += 1
        continue
    if pid == 0:
        open(os.path.join(d, "m%d" % i), "w").close()
        time.sleep(3)
        os._exit(0)
    ok += 1
print("ok=%d refused=%d" % (ok, refused))
while True:
    try:
        os.wait()
    except ChildProcessError:
        break
sys.exit(1 if refused else 0)
"""


def _skip_without_systemd_run():
    if not shutil.which("systemd-run"):
        pytest.skip("no systemd-run on this box: nothing can carry TasksMax")


def test_a_fanout_past_the_bound_is_refused_by_the_scope(tmp_path, monkeypatch):
    _skip_without_systemd_run()
    monkeypatch.setenv("AGI_TASKS_MAX", "8")
    script = tmp_path / "fanout.sh"
    script.write_text(_FANOUT)
    script.chmod(0o755)
    marks = tmp_path / "marks"
    argv = mem_cap.wrap_argv([str(script), str(marks), str(WANTED)], "512M")
    p = subprocess.run(argv, capture_output=True, text=True, timeout=90)
    started = len(list(marks.glob("m*"))) if marks.exists() else 0
    assert started <= 8, f"{started} processes started under TasksMax=8"
    assert p.returncode != 0, p.stdout + p.stderr


def test_the_unwrapped_path_is_unchanged(tmp_path):
    """`cap is None` -> the SAME argv, so the whole fan-out runs: the bound
    is a property of the wrapped scope, never a behaviour change for a caller
    that asked for no cap."""
    _skip_without_systemd_run()
    script = tmp_path / "fanout2.sh"
    script.write_text(_FANOUT)
    script.chmod(0o755)
    marks = tmp_path / "marks2"
    argv = mem_cap.wrap_argv([str(script), str(marks), str(WANTED)], None)
    assert argv[:3] == [str(script), str(marks), str(WANTED)], argv
    p = subprocess.run(argv, capture_output=True, text=True, timeout=90)
    assert p.returncode == 0, p.stdout + p.stderr
    assert len(list(marks.glob("m*"))) == WANTED, p.stdout
