"""A suite run never spawns a second detached pytest
(hypothesis:l4-a-suite-run-never-spawns-a-second-detached-pytest-the-
spawning-test-is-named-and-stubbed-and-the-runner-refuses-under-pytest).

MEASURED (Prime, doc:l4-owner-decisions 00:5xZ): during sanctuary-master's
`verification.py --level rotation --suite` run (launcher 324617) a SECOND
detached pytest (pid 446598, ppid 1) appeared ~10 min in — the whole suite
re-running under /tmp, doubling wall time and holding the lock while the real
runner exits. Two edges here:

1. Claim (2): `verification.py --suite` REFUSES to start when
   PYTEST_CURRENT_TEST is set — a runner launched from inside a test is never
   a legitimate rotation check. One refusal line, exit 3, before any work.
2. Claim (3): the guard. A --suite run in a throwaway tree never produces a
   second pytest with ppid 1. The named test STUBS the runner (a fake pytest
   that prints a fixed footer) instead of spawning a real one, and the ppid-1
   watcher asserts the tree stayed clean.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import verification  # noqa: E402


def _detached_pytest_ppid1() -> list[int]:
    """Pids of any pytest whose parent is init (ppid 1) — the detached second
    suite, read-only /proc scan. Empty on non-Linux."""
    pids: list[int] = []
    if os.name != "posix":
        return pids
    proc = Path("/proc")
    for p in proc.iterdir():
        if not p.name.isdigit():
            continue
        try:
            cmd = (p / "cmdline").read_bytes().decode("utf-8", "replace")
            status = (p / "status").read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "pytest" not in cmd:
            continue
        ppid: int | None = None
        for line in status.splitlines():
            if line.startswith("PPid:"):
                ppid = int(line.split()[1])
                break
        if ppid == 1:
            pids.append(int(p.name))
    return pids


def test_suite_refuses_when_launched_from_inside_a_test(tmp_path, monkeypatch,
                                                       capsys):
    """Claim (2): --suite with PYTEST_CURRENT_TEST set refuses by name, exit 3,
    before any work — the level never runs, so no second pytest can spawn."""
    monkeypatch.setenv("PYTEST_CURRENT_TEST",
                       "test_suite_no_detached_spawn.py::t ()")
    planned: list = []
    monkeypatch.setattr(verification, "run_level",
                        lambda *a, **k: planned.append(a) or [])
    rc = verification.main(["--suite", "--root", str(tmp_path)])
    assert rc == 3, rc
    assert planned == []  # the level never ran -> no second pytest
    out = capsys.readouterr().out
    assert "refusing" in out
    assert out.count("refusing") == 1  # exactly one refusal line


def test_suite_run_never_leaves_a_detached_pytest(tmp_path, monkeypatch):
    """Guard (claim 3): the --suite runner spawns pytest as a WAITED child,
    never detached. Drive the real runner against a STUBBED fake pytest (a
    fixed footer) in a throwaway tree and assert the ppid-1 watcher is empty.
    A real detached spawn would linger with ppid 1 and be caught."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    stub = tmp_path / "fake_tests.sh"
    stub.write_text("#!/bin/sh\necho '1 passed, 0 failed'\n", encoding="utf-8")
    stub.chmod(0o755)
    fake = {"tests": verification.commands.Command(
        name="tests", argv=[str(stub)], raw_argv=[str(stub)], cwd=str(groot))}
    monkeypatch.setattr(verification.commands, "load", lambda g: fake)
    r = verification.run_check(groot, verification.SUITE_CMD, verbose=False)
    assert r.status == "PASS", r.note
    assert r.number == {"passed": 1, "failed": 0}, r.number
    assert _detached_pytest_ppid1() == []
