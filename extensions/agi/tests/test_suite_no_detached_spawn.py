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


def _is_pytest_argv(argv: list[str]) -> bool:
    """True only when the cmdline IS a pytest launch, never a mere mention:
    argv[0] basename starts with pytest, or argv[1:3] == ['-m', 'pytest']
    (python -m pytest). A live pi trajectory wrapper (ppid 1) carries pi's
    argv with the word pytest inside, so it must NOT match."""
    if not argv or not argv[0]:
        return False
    if os.path.basename(argv[0]).startswith("pytest"):
        return True
    return argv[1:3] == ["-m", "pytest"]


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
        if not _is_pytest_argv(cmd.split("\0")):
            continue
        ppid: int | None = None
        for line in status.splitlines():
            if line.startswith("PPid:"):
                ppid = int(line.split()[1])
                break
        # The scanning suite ITSELF is never "the detached second suite": a
        # suite launched with `setsid nohup ... & disown` (the DURABLE rule --
        # long work runs detached) has ppid 1 and flagged its own pid, red x2
        # on 267a6ef04 (director-engine gen 24; TMM.225 had no red on a
        # launch whose parent stayed alive).
        if ppid == 1 and int(p.name) != os.getpid():
            pids.append(int(p.name))
    return pids


def test_suite_refuses_when_launched_from_inside_a_test(tmp_path, monkeypatch):
    """Claim (2): at the REAL launch site the suite REFUSES when it would
    launch pytest while already inside a test (PYTEST_CURRENT_TEST set) — one
    refusal line in the note, nothing spawned. A stubbed fake-suite (non-
    pytest argv) is NOT refused (the guard test below proves that leg)."""
    monkeypatch.setenv("PYTEST_CURRENT_TEST",
                       "test_suite_no_detached_spawn.py::t ()")
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    real = {"tests": verification.commands.Command(
        name="tests", argv=["python3", "-m", "pytest", str(tmp_path)],
        raw_argv=["python3", "-m", "pytest", str(tmp_path)],
        cwd=str(groot))}
    monkeypatch.setattr(verification.commands, "load", lambda g: real)
    r = verification.run_check(groot, verification.SUITE_CMD, verbose=False)
    assert r.status == "FAIL", r.note
    assert r.note.count("refusing") == 1  # exactly one refusal line
    assert _detached_pytest_ppid1() == []  # nothing launched


def test_ring_fields_under_pytest_exits_zero(tmp_path, monkeypatch):
    """Claim (2) carve-out: an in-process `--suite --ring-fields` reads/prints
    the grant bytes and exits 0 even while running under pytest, because it
    never reaches the launch site the refusal guards. This is the RED the
    main()-level refusal caused (test_ring_cli_seam broke); the refusal must
    NOT sit on the print-only path."""
    monkeypatch.setenv("PYTEST_CURRENT_TEST",
                       "test_suite_no_detached_spawn.py::t ()")
    root = tmp_path / ".agi"
    root.mkdir(parents=True)
    (root / "config.json").write_text("{}", encoding="utf-8")
    (root / "context" / "schemas").mkdir(parents=True)
    (root / "context" / "schemas" / "[config].md").write_text(
        "---\ntype: config\n", encoding="utf-8")
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "rings.md").write_text(
        "---\ntype: cell\nrings:\n  - name: approval\n    m: 2\n"
        "    members: [alice, bob, carol]\n---\n", encoding="utf-8")
    (root / "nodes" / ".geometry" / "posts.md").write_text(
        "---\ntype: config\nposts:\n  - name: alice\n    pubkey: "
        + ("6b" * 32) + "\n---\n", encoding="utf-8")
    (root / "nodes").mkdir(parents=True, exist_ok=True)
    (root / "nodes" / "posts.md").write_text(
        "---\nid: config:posts\ntype: config\nmint_id: cfgtst002\n"
        "title: posts\n---\n\nbody\n", encoding="utf-8")
    monkeypatch.setattr(verification, "run_level",
                        lambda *a, **k: [])
    fresh = "1970-01-01T00:00:00Z|t"
    # --ring-fields returns before run_level AND before the launch site.
    rc = verification.main(["--root", str(tmp_path), "--suite",
                            "--suite-ring", "approval",
                            "--ring-fresh", fresh, "--ring-fields"])
    assert rc == 0, rc


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


def test_matcher_is_pytest_launch_not_a_mention():
    """The ppid-1 watcher matches only a real pytest launch: python -m pytest
    and a pytest binary, never a pi trajectory wrapper whose argv merely
    MENTIONS pytest inside the pi command line."""
    assert _is_pytest_argv(["python3", "-m", "pytest", "tests/"]) is True
    assert _is_pytest_argv(["/usr/bin/pytest", "-q"]) is True
    assert _is_pytest_argv(["pytest-x", "-q"]) is True  # binary starts w/ pytest
    wrapper = ["/home/pi/bin/pi", "-p", "--mode", "json",
               "run a test with pytest please"]
    assert _is_pytest_argv(wrapper) is False
    assert _is_pytest_argv(["/home/pi/bin/pi_trajectory.py", "--wrapper",
                            "/usr/bin/python3", "traj.json", "--",
                            "-p", "--mode", "json", "pytest"]) is False
    assert _is_pytest_argv([]) is False
