"""hypothesis:a00-50b210d5-b85ee2 -- the stage seam hands `mem_cap.wrap_argv`
NO config, so every `values.memcap.*` cell the operator declares is silently
ignored on every workflow stage launch while `dispatch.py` honours the same
cells from the same graph.

The seam is measured, not argued: `wrap_argv`'s only reader of `cfg` is
`systemd_run_usable(cfg)`, so a recording stand-in for that function observes
EXACTLY which cfg object reached the cap helper -- `None` (the defect) or the
caller's own dict (the fix). W2 pins that threading the cfg in did not un-wrap
the stage: a runaway launched through the real seam still dies of the cap.
W3 pins the legacy path: a caller with no cfg still gets the shipped defaults.
W4 pins the byte.

Scope note: the cell this seam drops TODAY is the `values.memcap` probe-cache
pair, NOT `tasks_max` -- `tasks_max` does not exist on this tree (it is on
kid 1's branch). Named in the hypothesis node so nobody hunts for a seam that
was never here.
"""
from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import mem_cap  # noqa: E402
import workflow as _wf  # noqa: E402

_ALLOC = "x=bytearray(600*1024*1024)"


@pytest.fixture(autouse=True)
def _no_real_systemd(tmp_path, monkeypatch):
    """Forced verdict: the prlimit branch, so no test here execs the real
    `systemd-run` (the same rule `test_launch_memory_cap.py` states)."""
    monkeypatch.setenv("AGI_MEMCAP_SYSTEMD_RUN", "0")
    shim = tmp_path / "shim"
    shim.mkdir()
    for name in ("systemd-run", "systemctl"):
        p = shim / name
        p.write_text(f"#!/bin/sh\necho {name} \"$@\" >> "
                     f"{tmp_path / 'exec.log'}\nexit 137\n")
        p.chmod(p.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", f"{shim}:{os.environ.get('PATH', '')}")
    monkeypatch.delenv("AGI_MEMCAP_CACHE", raising=False)


def _recording_probe(monkeypatch) -> list:
    """Replace `systemd_run_usable` with a recorder that returns the prlimit
    verdict (False) and remembers the cfg it was handed, BY IDENTITY -- a copy
    of the dict would not prove the caller's object travelled."""
    seen: list = []
    monkeypatch.setattr(mem_cap, "systemd_run_usable",
                        lambda cfg=None: (seen.append(cfg), False)[1])
    return seen


# ---- W1: the seam passes the caller's OWN cfg down ------------------------

def test_stage_seam_hands_the_callers_cfg_to_the_cap_helper(monkeypatch):
    seen = _recording_probe(monkeypatch)
    cfg = {"spawn": {"memory_max": "256M"},
           "values": {"memcap": {"probe_cache_dir_name": "seat-cache"}}}
    r = _wf._run_stage_proc(
        [sys.executable, "-c", "print('ok')"], budget=30,
        stage={"label": "only"}, spawn_env=os.environ.copy(), view=None,
        cap="256M", cfg=cfg)
    assert r.returncode == 0, r.stderr
    assert len(seen) == 1, seen
    assert seen[0] is cfg, "the stage seam dropped the cfg it already holds"


# ---- W2: threading the cfg in did NOT un-wrap the stage -------------------

def test_stage_seam_still_caps_the_child_under_prlimit(monkeypatch):
    _recording_probe(monkeypatch)
    cfg = {"spawn": {"memory_max": "256M"}}
    r = _wf._run_stage_proc(
        [sys.executable, "-c", _ALLOC], budget=60,
        stage={"label": "only"}, spawn_env=os.environ.copy(), view=None,
        cap="256M", cfg=cfg)
    assert mem_cap.is_cap_death(r.returncode, "256M", r.stderr), r


# ---- W3: a caller with no cfg still gets the shipped defaults -------------

def test_no_cfg_in_hand_still_uses_the_shipped_defaults(monkeypatch):
    seen = _recording_probe(monkeypatch)
    r = _wf._run_stage_proc(
        [sys.executable, "-c", "print('ok')"], budget=30,
        stage={"label": "only"}, spawn_env=os.environ.copy(), view=None,
        cap="256M")
    assert r.returncode == 0, r.stderr
    assert seen == [None], seen


# ---- W4: the byte --------------------------------------------------------

def test_the_seam_reads_the_cfg_aware_call():
    src = (BIN / "workflow.py").read_text()
    # cfg stays third; the named unit rides along (hypothesis:g73360-a-workflow-
    # stage-stops-its-own-scope-on-exit).
    assert "mem_cap.wrap_argv(cmd, cap, cfg, unit=unit)" in src
    assert "mem_cap.wrap_argv(cmd, cap)" not in src
