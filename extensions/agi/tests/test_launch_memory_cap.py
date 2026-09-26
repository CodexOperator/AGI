"""Tests for bin/mem_cap.py -- the ONE memory cap both launch paths use.

hypothesis:l4-every-launched-kid-parent-and-workflow-stage-runs-under-a-memory-
cap-so-a-runaway-dies-alone-and-by-name-never-a-global-oom:
(1) a child that allocates past a 256M cap dies and the status reads
`memory-cap`; (2) a sibling beside it finishes green; (3) BOTH call sites route
through the helper -- an import-level assert plus one real launch through the
workflow stage site; (4) `memory_max: none` leaves argv unchanged (identity);
(5) with systemd-run forced unusable the prlimit fallback dies under the SAME
`memory-cap` name.
"""
from __future__ import annotations

import os
import stat
import subprocess
import sys
import io
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import mem_cap  # noqa: E402
import workflow as _wf  # noqa: E402
import dispatch as _dispatch  # noqa: E402

_ALLOC = "x=bytearray(600*1024*1024)"


@pytest.fixture(autouse=True)
def _no_ambient_pi_bin(monkeypatch):
    """`$PI_BIN` WINS over the `harnesses.pi.bin` config cell (the ONE
    shared resolver, env-first by design), so a suite run from a pi seat
    would dispatch these fake-bin tests at the REAL pi. Same EF.14 pattern
    as test_workflow.py's autouse fixture. A test that exercises the
    override sets PI_BIN itself, after this fixture.
    (hypothesis:harness-bin-paths-resolve-per-box round 4)"""
    monkeypatch.delenv("PI_BIN", raising=False)


def _fake_pi(tmp_path: Path) -> Path:
    """A `pi`-shaped binary that ignores its argv and allocates past any cap."""
    p = tmp_path / "fakepi"
    p.write_text(f"#!/bin/sh\nexec {sys.executable} -c '{_ALLOC}'\n")
    p.chmod(p.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return p


# ---- (4) identity: disabled cap never touches argv ------------------------

def test_memory_max_none_returns_the_same_argv_object():
    argv = ["echo", "hi"]
    assert mem_cap.wrap_argv(argv, None) is argv


def test_resolve_memory_cap_default_none_and_verbatim():
    assert mem_cap.resolve_memory_cap({}) == "4G"
    assert mem_cap.resolve_memory_cap({"spawn": {}}) == "4G"
    assert mem_cap.resolve_memory_cap({"spawn": {"memory_max": None}}) is None
    assert mem_cap.resolve_memory_cap(
        {"spawn": {"memory_max": "none"}}) is None
    assert mem_cap.resolve_memory_cap(
        {"spawn": {"memory_max": "2G"}}) == "2G"


# ---- (3) both call sites route through the SAME helper --------------------

def test_both_call_sites_share_the_one_helper():
    assert _dispatch.mem_cap is mem_cap
    assert _wf.mem_cap is mem_cap
    src = (BIN / "dispatch.py").read_text()
    # dispatch passes the cfg it already holds (config-max of the probe
    # cache); workflow's helper takes only the cap, so it reads the
    # shipped defaults. Both route through the ONE helper.
    assert "mem_cap.wrap_argv(spawn_args, _mem_cap, cfg)" in src
    src = (BIN / "workflow.py").read_text()
    assert "mem_cap.wrap_argv(cmd, cap)" in src


def test_workflow_stage_site_really_launches_under_a_cap(tmp_path):
    r = _wf._run_stage_proc(
        [sys.executable, "-c", _ALLOC], budget=60,
        stage={"label": "only"},
        spawn_env=os.environ.copy(), view=None, cap="256M")
    assert r.returncode < 0, r.returncode  # SIGKILL from the scope cap
    assert mem_cap.is_cap_death(r.returncode, "256M")


# ---- (1) real pi-stage death names `memory-cap`, rc recorded --------------

def test_stage_cap_death_is_named_memory_cap(tmp_path):
    cfg = {"harnesses": {"pi": {"bin": str(_fake_pi(tmp_path)),
                                "provider": "openrouter"}},
           "spawn": {"memory_max": "256M"}}
    stage = {"label": "draft:a", "prompt": "p"}
    view = _wf.RunView("review", [{"label": "draft:a"}], "pi",
                       out=io.StringIO())
    rc, value = _wf._run_stage_pi(cfg, stage, {"draft:a": {"model": "m"}},
                                  {"thinking": "medium"}, view=view)
    assert rc == 3 and value is None
    state = view.state["draft:a"]
    assert state["status"] == "failed"
    assert "memory-cap" in state["detail"], state


# ---- (5) systemd-run unusable -> prlimit fallback, same name --------------

def test_prlimit_fallback_keeps_the_memory_cap_name(monkeypatch):
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: False)
    wrapped = mem_cap.wrap_argv(["echo", "x"], "256M")
    assert wrapped[:1] == ["prlimit"], wrapped
    assert wrapped[1] == f"--as={256 * 1024 ** 2}", wrapped
    p = subprocess.run(wrapped[:2] + [sys.executable, "-c", _ALLOC],
                       capture_output=True, text=True)
    assert p.returncode != 0
    assert mem_cap.is_cap_death(p.returncode, "256M", p.stderr), p.stderr


# ---- (2) the sibling beside a capped runaway finishes green ---------------

def test_sibling_beside_the_capped_runaway_comes_home_green():
    runaway = mem_cap.wrap_argv([sys.executable, "-c", _ALLOC], "256M")
    sibling = mem_cap.wrap_argv([sys.executable, "-c", "print('ok')"], "256M")
    dead = subprocess.run(runaway, capture_output=True, text=True)
    green = subprocess.run(sibling, capture_output=True, text=True)
    assert dead.returncode != 0
    assert green.returncode == 0 and green.stdout.strip() == "ok"
    assert not mem_cap.is_cap_death(green.returncode, "256M")
