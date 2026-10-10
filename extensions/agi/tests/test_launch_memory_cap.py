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
import shutil
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

#: The two real binaries no test in this file may exec.
_SHIMMED = ("systemd-run", "systemctl")


@pytest.fixture(autouse=True)
def _no_real_systemd(tmp_path, monkeypatch):
    """hypothesis:launch-memory-cap-tests-never-touch-real-systemd -- this
    file NEVER reaches real systemd. Two lines, both needed:

    (1) the FAKE seam: `AGI_MEMCAP_SYSTEMD_RUN=0` forces the prlimit branch,
        so nothing here runs `systemd_run_usable`'s probe -- a real
        `systemd-run --unit=agi-memcap-probe --property=MemoryMax=64M` child
        that deliberately allocates 256 MB, followed by a real
        `systemctl --user reset-failed`. MEASURED on this box before the
        fixture: 4 real `systemd-run` execs (the 256M wraps of the runaway,
        of the fake pi, and of the green sibling) in one file run.
    (2) the GUARD: a PATH dir ahead of the real one whose `systemd-run` /
        `systemctl` log their argv and exit 137. A regression that re-reaches
        the real binary is then a loud failure naming the exec, not a silent
        real systemd call. The guard checks itself, so it cannot rot into a
        vacuous pass.

    The suite's session-scoped `_agi_env_stripped` (extensions/agi/
    conftest.py) drops every `AGI_*` var BEFORE any function-scoped body
    runs, so this setenv is the one that counts -- the same ordering
    `conftest.py`'s `_no_openrouter` documents."""
    monkeypatch.setenv("AGI_MEMCAP_SYSTEMD_RUN", "0")
    log = tmp_path / "systemd-exec.log"
    shim = tmp_path / "shim"
    shim.mkdir()
    for name in _SHIMMED:
        p = shim / name
        p.write_text(f'#!/bin/sh\necho "{name} $*" >> "{log}"\nexit 137\n')
        p.chmod(0o755)
    monkeypatch.setenv("PATH", f"{shim}{os.pathsep}{os.environ['PATH']}")
    yield
    seen = log.read_text() if log.exists() else ""
    assert not seen, f"a test in this file execed real systemd:\n{seen}"


def test_the_systemd_guard_itself_records(tmp_path, monkeypatch):
    """The guard is not vacuous: a forced probe really is caught. Without
    this, a shim that silently never fires would pass every test here."""
    monkeypatch.setenv("AGI_MEMCAP_SYSTEMD_RUN", "")
    monkeypatch.setenv("AGI_MEMCAP_CACHE", str(tmp_path / "nocache"))
    monkeypatch.setattr(mem_cap, "_PROBE", None, raising=False)
    # the box's own boot cache is a PROPERTY OF THE BOX -- never read it here,
    # or this self-test is a coin flip on whether the probe runs at all.
    monkeypatch.setattr(mem_cap, "_read_cached_probe", lambda cfg=None: None)
    shim = tmp_path / "g"
    shim.mkdir()
    log = tmp_path / "g.log"
    for name in _SHIMMED:
        p = shim / name
        p.write_text(f'#!/bin/sh\necho "{name} $*" >> "{log}"\nexit 137\n')
        p.chmod(0o755)
    monkeypatch.setenv("PATH", f"{shim}{os.pathsep}{os.environ['PATH']}")
    mem_cap.systemd_run_usable()
    assert "systemd-run" in log.read_text(), "guard did not fire"


def test_systemd_run_branch_is_covered_without_exec():
    """The systemd-run argv is still asserted -- as a STRING, never a run --
    so forcing the prlimit seam costs no coverage of the real branch."""
    saved = os.environ.get("AGI_MEMCAP_SYSTEMD_RUN")
    os.environ["AGI_MEMCAP_SYSTEMD_RUN"] = "1"
    try:
        wrapped = mem_cap.wrap_argv(["echo", "x"], "256M")
    finally:
        if saved is None:
            os.environ.pop("AGI_MEMCAP_SYSTEMD_RUN", None)
        else:
            os.environ["AGI_MEMCAP_SYSTEMD_RUN"] = saved
    assert wrapped[0] == "systemd-run", wrapped
    assert "--property=MemoryMax=256M" in wrapped, wrapped


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
    # BOTH call sites now pass the cfg they already hold (config-max of the
    # probe cache) -- hypothesis:a00-50b210d5-b85ee2 closed the stage seam's
    # last cfg-less `wrap_argv`. Both route through the ONE helper.
    assert "mem_cap.wrap_argv(spawn_args, _mem_cap, cfg)" in src
    src = (BIN / "workflow.py").read_text()
    # the stage seam ALSO names its scope now
    # (hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit):
    assert "mem_cap.wrap_argv(cmd, cap, cfg, unit=unit)" in src


def test_workflow_stage_site_really_launches_under_a_cap(tmp_path):
    r = _wf._run_stage_proc(
        [sys.executable, "-c", _ALLOC], budget=60,
        stage={"label": "only"},
        spawn_env=os.environ.copy(), view=None, cap="256M")
    # Under the faked seam the cap is prlimit's, so the death is
    # RLIMIT_DATA exhaustion (MemoryError, rc 1), not a cgroup SIGKILL --
    # `is_cap_death` is the seam-independent name for both.
    assert mem_cap.is_cap_death(r.returncode, "256M", r.stderr), r


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
    assert wrapped[1] == f"--data={256 * 1024 ** 2}", wrapped
    p = subprocess.run(wrapped[:2] + [sys.executable, "-c", _ALLOC],
                       capture_output=True, text=True)
    assert p.returncode != 0
    assert mem_cap.is_cap_death(p.returncode, "256M", p.stderr), p.stderr


# ---- (5b) the fallback bounds COMMITTED memory, so a node harness lives ---
# goal:g7.16.1.11.35: `prlimit --as` also counts PROT_NONE reservations, and
# V8's wasm reservation (node's undici, every pi stage) dies under it on a box
# with no user systemd manager. `--data` (RLIMIT_DATA) counts only what a
# process has committed, so the runaway still dies and the harness does not.

_NODE = shutil.which("node")
_need_node = pytest.mark.skipif(
    _NODE is None, reason="node absent on this box: the pi-harness rows need it")
_FETCH = ('fetch("http://127.0.0.1:9")'
          '.catch(e=>console.log("settled:",e.message))')
# Each child below exceeds ITS cap by a bounded amount (<= 200 MB) and exits 0
# when the limit is dropped, so the unbounded witness stays small on a 2 GB box.
# The wordings are the runtimes' own ENOMEM texts (is_cap_death's needles).
_KILL_ROWS = {
    # kind: (child argv tail, cap, the text the death must carry)
    "python": (["-c", "x=bytearray(200*1024*1024)"], "128M", "memoryerror"),
    # the falsifier as written (goal:g7.16.1.11.35 falsifier 3): a node
    # Buffer.alloc past the cap, rc 1, no abort
    "node-buffer": (["-e", 'Buffer.alloc(2e8).fill(1);console.log("ok")'],
                    "128M", "array buffer allocation failed"),
    "node-wasm-memory": (["-e", 'new WebAssembly.Memory({initial:3200});'
                                'console.log("ok")'],
                         "128M", "could not allocate memory"),
    # 40 x 8 MB thread stacks: private mappings, so RLIMIT_DATA bounds them;
    # daemon threads released in finally so a failed start cannot hang exit
    "python-thread": (["-c", "import threading as t\n"
                             "t.stack_size(8*1024*1024);e=t.Event();l=[]\n"
                             "try:\n"
                             " for _ in range(40):\n"
                             "  x=t.Thread(target=e.wait,daemon=True)\n"
                             "  x.start();l.append(x)\n"
                             "finally:\n"
                             " e.set()\n"],
                      "64M", "can't start new thread"),
}


def _fallback(monkeypatch, argv, cap):
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: False)
    return mem_cap.wrap_argv(argv, cap)


def _run(argv):
    return subprocess.run(argv, capture_output=True, text=True, timeout=120)


@_need_node
def test_fallback_argv_lets_a_node_child_instantiate_webassembly(monkeypatch):
    argv = _fallback(monkeypatch, [_NODE, "-e", _FETCH], "2G")
    assert argv[:2] == ["prlimit", f"--data={2 * 1024 ** 3}"], argv

    def settles(a):
        p = _run(a)
        return (p.returncode == 0 and "settled: fetch failed" in p.stdout
                and "WebAssembly" not in p.stderr)

    assert settles(argv)
    # the row can fail: the same child under --as (the old fallback) dies
    # in WebAssembly.instantiate
    assert not settles([x.replace("--data=", "--as=") for x in argv])


@pytest.mark.parametrize("kind", sorted(_KILL_ROWS))
def test_fallback_still_kills_a_child_that_allocates_past_the_cap(
        monkeypatch, kind):
    tail, cap, wording = _KILL_ROWS[kind]
    if kind.startswith("node") and _NODE is None:
        pytest.skip("node absent on this box: the pi-harness rows need it")
    interp = _NODE if kind.startswith("node") else sys.executable
    argv = _fallback(monkeypatch, [interp, *tail], cap)
    assert argv[1] == f"--data={mem_cap._as_bytes(cap)}", argv
    p = _run(argv)
    assert p.returncode != 0, (kind, p.stdout, p.stderr)
    assert wording in p.stderr.lower(), (kind, p.stderr)
    assert mem_cap.is_cap_death(p.returncode, cap, p.stderr), (
        kind, p.returncode, p.stderr)
    # the row can fail: with the limit dropped the same child finishes
    free = _run(argv[argv.index("--") + 1:])
    assert free.returncode == 0, (kind, free.stderr)
    assert not mem_cap.is_cap_death(free.returncode, cap, free.stderr)


@pytest.mark.parametrize("text", [
    "MemoryError",
    "FATAL ERROR: Allocation failed - JavaScript heap out of memory",
    "RangeError: Array buffer allocation failed",
    "RangeError: WebAssembly.Memory(): could not allocate memory",
    "RuntimeError: can't start new thread",
    "fork: Cannot allocate memory"])
def test_is_cap_death_names_each_runtimes_enomem_wording(text):
    assert mem_cap.is_cap_death(1, "256M", text), text
    # the needle is the only reason: an ordinary rc 1 is not a cap death
    assert not mem_cap.is_cap_death(1, "256M", "ValueError: bad input")
    assert not mem_cap.is_cap_death(1, None, text)


def test_cap_none_is_the_same_argv_object_and_systemd_has_no_prlimit(
        monkeypatch):
    argv = ["echo", "x"]
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: False)
    assert mem_cap.wrap_argv(argv, None) is argv
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    assert mem_cap.wrap_argv(argv, None) is argv
    out = mem_cap.wrap_argv(argv, "256M")
    assert out[0] == "systemd-run" and "prlimit" not in out, out
    assert not [x for x in out if x.startswith(("--as", "--data"))], out


# ---- (2) the sibling beside a capped runaway finishes green ---------------

def test_sibling_beside_the_capped_runaway_comes_home_green():
    runaway = mem_cap.wrap_argv([sys.executable, "-c", _ALLOC], "256M")
    sibling = mem_cap.wrap_argv([sys.executable, "-c", "print('ok')"], "256M")
    dead = subprocess.run(runaway, capture_output=True, text=True)
    green = subprocess.run(sibling, capture_output=True, text=True)
    assert dead.returncode != 0
    assert green.returncode == 0 and green.stdout.strip() == "ok"
    assert not mem_cap.is_cap_death(green.returncode, "256M")
