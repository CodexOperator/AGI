"""Conjunct (3) of hypothesis:pin-reap-never-names-a-live-session-and-a-
reap-leaves-no-stale-app-session — the s12 TERM GRACE IS A CONFIG CELL.

`_reap_chain` hard-coded `wait_secs: float = 5.0` in its signature, so every
caller that passed nothing got 5 s between SIGTERM and SIGKILL and no
operator could widen it. Now the absent-argument case resolves
`reaper.term_grace_s` at RUNTIME (default 15.0, the resolver for a missing
cell, not a second value) and an explicit `wait_secs=` still wins.

Fixtures only: a fixture graph root with a fixture config, and FAKE pids.
No real pane, pid, unit or crontab -- enforced, not promised: this module
sets `NO_REAL_PROCESSES = True`, which puts it under conftest's autouse
`_no_real_process_or_live_config` guard (no spawn, no /proc, no signal to a
foreign pid, no live `.agi/config.json` outside tmp_path). The live cell
assertion moved to tests/test_live_config_cells.py, the file that owns live
config declarations.
"""
from __future__ import annotations

import importlib.util
import json
import signal
import sys
import time
from pathlib import Path

import pytest

#: Opt in to the conftest process/config guard for this whole module.
NO_REAL_PROCESSES = True

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


def _fake_reaper(monkeypatch, *, pid=424242, pids=None, ignore_term=True):
    """Inject the three seams `_reap_chain` reaches for: the liveness probe
    (`_pid_alive`), the `ps -o pid=,cmd= -p` reader (`_short_ps`) and the
    signalling seam (`os.kill` in rotate's own module globals, plus
    `os.waitpid` which only ever succeeds for a real child). Nothing is
    spawned, nothing outside this dict is touched, and every signal the
    chain sends is recorded so the test can assert on it.

    `ignore_term=True` models the original subject of this test: a process
    that IGNORES SIGTERM, so the wait runs to the cell's deadline and the
    survivor is SIGKILL'd."""
    state = {"alive": set(pids) if pids else {pid}, "signals": []}

    def _alive(p):
        return int(p) in state["alive"]

    def _kill(p, sig, *a, **k):
        state["signals"].append((int(p), sig))
        if sig != signal.SIGTERM or not ignore_term:
            state["alive"].discard(int(p))

    monkeypatch.setattr(rot, "_pid_alive", _alive)
    monkeypatch.setattr(rot, "_short_ps", lambda p: f"{int(p)} fake-cmd")
    monkeypatch.setattr(rot.os, "kill", _kill)
    monkeypatch.setattr(rot.os, "waitpid",
                        lambda *a, **k: (_ for _ in ()).throw(
                            ChildProcessError()))
    return state


def test_reap_chain_without_wait_secs_uses_the_cell(fake_root, monkeypatch):
    """A FAKE pid that IGNORES SIGTERM: the cell's 0.4 s bounds the wait, then
    the survivor is SIGKILL'd -- so the cell reaches the real wait loop, and
    the default argument is no longer a hard-coded 5.0. No fork, no /proc
    scan, no real `ps`/`git`, no signal to a pid this test did not fake."""
    fake_root({"term_grace_s": 0.4})
    state = _fake_reaper(monkeypatch)

    t0 = time.monotonic()
    out = rot._reap_chain([424242])
    elapsed = time.monotonic() - t0

    rec = out["chain"][0]
    assert rec["pid"] == 424242
    assert rec["was_alive"] is True
    assert rec["termd"] is True
    assert rec["gone_after"] is True
    # the `ps` read is the INJECTED one, so the real `ps` never ran
    assert rec["ps_before"] == "424242 fake-cmd"
    assert rec["ps_after"] == "424242 fake-cmd"
    # TERM first, KILL only after the grace expired: the whole point
    assert [s for _p, s in state["signals"]] == [signal.SIGTERM,
                                                 signal.SIGKILL]
    # the CELL bounded the wait: at least its 0.4 s was actually spent, and
    # well under the 5.0 the hard-coded default would have cost
    assert elapsed >= 0.4, elapsed
    assert elapsed < 3.0, elapsed


def test_reap_chain_explicit_wait_secs_still_wins(fake_root, monkeypatch):
    """An explicit `wait_secs=` beats the cell, and the same fake pid goes
    away without a KILL when it honours SIGTERM."""
    fake_root({"term_grace_s": 41.0})
    state = _fake_reaper(monkeypatch, ignore_term=False)

    t0 = time.monotonic()
    out = rot._reap_chain([424242], wait_secs=0.1)
    elapsed = time.monotonic() - t0

    assert out["chain"][0]["gone_after"] is True
    assert state["signals"] == [(424242, signal.SIGTERM)]
    assert elapsed < 3.0, elapsed  # 41.0 was NOT consulted


def test_reap_chain_refuses_the_real_own_pid(fake_root, monkeypatch):
    """The own-pid fence still holds with the seams injected: no signal is
    sent to this process (or any other) when the chain names it."""
    fake_root({"term_grace_s": 0.4})
    state = _fake_reaper(monkeypatch)
    own = rot.os.getpid()

    out = rot._reap_chain([own, 424242])

    # the record is DEEPEST-FIRST, so the own pid is the LAST entry
    assert out["chain"][-1]["termd"] is False
    assert "refused" in out["chain"][-1]["note"]
    assert all(p == 424242 for p, _s in state["signals"])



# ── hypothesis:a-reap-chain-is-bounded-by-one-chain-deadline-not-per-pid-grace
def test_absent_chain_deadline_cell_resolves_to_the_code_default(fake_root):
    """The chain deadline is a CONFIG CELL like the term grace, and 20.0 is
    the RESOLVER for a missing cell, not a second value."""
    fake_root({})
    assert rot._chain_deadline_s() == 20.0


def test_chain_deadline_cell_is_read_at_runtime(fake_root):
    fake_root({"chain_deadline_s": 2.5})
    assert rot._chain_deadline_s() == 2.5
    fake_root({"chain_deadline_s": 7})
    assert rot._chain_deadline_s() == 7.0   # not cached from the first read


@pytest.mark.parametrize("bad", ["abc", True, -1, 0, None, []])
def test_malformed_chain_deadline_falls_back_and_never_raises(fake_root, bad):
    fake_root({"chain_deadline_s": bad})
    assert rot._chain_deadline_s() == 20.0


def test_three_term_immune_members_cost_ONE_chain_deadline(fake_root,
                                                          monkeypatch):
    """The falsifier: N TERM-ignoring members must all be SIGKILLed inside ONE
    `chain_deadline_s` budget, never N x `term_grace_s`. term_grace 1.0 x 3 =
    3.0 s is what the old per-pid deadline would have cost; the chain deadline
    of 1.2 s is what the whole chain may cost (+ settling)."""
    fake_root({"term_grace_s": 1.0, "chain_deadline_s": 1.2})
    state = _fake_reaper(monkeypatch, pids=[424242, 424243, 424244],
                         ignore_term=True)

    t0 = time.monotonic()
    out = rot._reap_chain([424242, 424243, 424244])
    elapsed = time.monotonic() - t0

    assert all(e["gone_after"] is True for e in out["chain"])
    assert [p for p, _s in state["signals"]] == \
        [424244, 424244, 424243, 424243, 424242, 424242]  # TERM+KILL each
    assert elapsed >= 1.2, elapsed          # the whole chain really waited
    assert elapsed < 2.5, elapsed           # NOT 3 x term_grace_s


def test_chain_deadline_caps_an_oversized_term_grace(fake_root, monkeypatch):
    """`term_grace_s` 41.0 with a 0.5 s chain deadline: the member still gets
    TERM then KILL, inside the chain deadline, not after 41 s of waiting."""
    fake_root({"term_grace_s": 41.0, "chain_deadline_s": 0.5})
    state = _fake_reaper(monkeypatch, ignore_term=True)

    t0 = time.monotonic()
    out = rot._reap_chain([424242])
    elapsed = time.monotonic() - t0

    assert out["chain"][0]["gone_after"] is True
    assert [s for _p, s in state["signals"]] == [signal.SIGTERM,
                                                 signal.SIGKILL]
    assert elapsed < 2.5, elapsed
