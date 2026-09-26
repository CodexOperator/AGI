"""Conjunct (3) of hypothesis:pin-reap-never-names-a-live-session-and-a-
reap-leaves-no-stale-app-session — the s12 TERM GRACE IS A CONFIG CELL.

`_reap_chain` hard-coded `wait_secs: float = 5.0` in its signature, so every
caller that passed nothing got 5 s between SIGTERM and SIGKILL and no
operator could widen it. Now the absent-argument case resolves
`reaper.term_grace_s` at RUNTIME (default 15.0, the resolver for a missing
cell, not a second value) and an explicit `wait_secs=` still wins.

Fixtures only: fixture graph root with a fixture config, and a throwaway
`python3 -c` child of THIS test. No real pane, pid, unit or crontab.
"""
from __future__ import annotations

import importlib.util
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rot = _load("rotate")


def _graph(tmp_path: Path, reaper: dict) -> Path:
    g = tmp_path / "repo" / ".agi"
    g.mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps({"reaper": reaper}))
    return g


@pytest.fixture
def fake_root(tmp_path, monkeypatch):
    """Point rotate's root resolver at a fixture graph with a given reaper
    block; returns the block setter."""
    g = _graph(tmp_path, {})
    monkeypatch.setattr(rot, "find_project_root", lambda: g)

    def _set(reaper):
        (g / "config.json").write_text(json.dumps({"reaper": reaper}))
    return _set


def test_absent_cell_resolves_to_the_code_default(fake_root):
    fake_root({})
    assert rot._term_grace_s() == 15.0


def test_cell_is_read_at_runtime(fake_root):
    fake_root({"term_grace_s": 3.5})
    assert rot._term_grace_s() == 3.5
    fake_root({"term_grace_s": 41})
    assert rot._term_grace_s() == 41.0   # not cached from the first read


@pytest.mark.parametrize("bad", ["abc", True, -1, 0, None, []])
def test_malformed_cell_falls_back_and_never_raises(fake_root, bad):
    fake_root({"term_grace_s": bad})
    assert rot._term_grace_s() == 15.0


def test_broken_config_json_falls_back(tmp_path, monkeypatch):
    g = tmp_path / "repo" / ".agi"
    g.mkdir(parents=True)
    (g / "config.json").write_text("{not json")
    monkeypatch.setattr(rot, "find_project_root", lambda: g)
    assert rot._term_grace_s() == 15.0


def test_live_config_declares_the_cell():
    """The cell is in the REAL .agi/config.json, not only in a fixture."""
    cfg = json.loads((rot.ENGINE_ROOT / ".agi" / "config.json"
                      ).read_text(encoding="utf-8"))
    assert cfg["reaper"]["term_grace_s"] == 15.0


def test_reap_chain_without_wait_secs_uses_the_cell(fake_root, tmp_path):
    """A child that IGNORES SIGTERM: the cell's 0.4 s bounds the wait, then
    the survivor is SIGKILL'd — so the cell reaches the real wait loop, and
    the default argument is no longer a hard-coded 5.0."""
    fake_root({"term_grace_s": 0.4})
    # Double-fork so the sleeper is NOT our direct child: a SIGKILLed direct
    # child stays a ZOMBIE we alone can reap, and the post-KILL poll only
    # probes `os.kill(pid, 0)` (which succeeds on a zombie), so gone_after
    # would read False for reasons that have nothing to do with the grace.
    sleeper = tmp_path / "sleeper.py"
    sleeper.write_text("import signal, time\n"
                       "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
                       "time.sleep(120)\n")
    launcher = tmp_path / "launcher.py"
    launcher.write_text(
        "import os, subprocess, sys\n"
        "if os.fork() == 0:\n"
        "    os.setsid()\n"
        f"    subprocess.Popen([sys.executable, {str(sleeper)!r}])\n"
        "    os._exit(0)\n"
        "os.wait()\n")
    child = subprocess.Popen([sys.executable, str(launcher)])
    child.wait(timeout=10)
    # find the grandchild by its unique marker
    time.sleep(0.3)
    gpid = None
    for p in Path("/proc").iterdir():
        if not p.name.isdigit():
            continue
        try:
            cl = (p / "cmdline").read_bytes().decode("utf-8", "replace")
        except OSError:
            continue
        if str(sleeper) in cl:
            gpid = int(p.name)
            break
    try:
        assert gpid is not None and gpid > 0
        t0 = time.time()
        out = rot._reap_chain([gpid])
        elapsed = time.time() - t0
        assert out["chain"][0]["gone_after"] is True
        # 0.4 s of grace + the 1.0 s post-KILL collect poll, well under 5.0:
        # if the hard-coded 5.0 were still in force this would exceed it.
        assert elapsed < 3.0, elapsed
    finally:
        try:
            os.kill(gpid, signal.SIGKILL)
        except OSError:
            pass
