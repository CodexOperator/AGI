"""An all-green --suite run writes the stamp `cli.py --delete-old` reads
(hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run).

Before this round the only writers of `sessions/verified.stamp` were test
fixtures (`write_text("green")`), and `cli.py --delete-old`'s freshness gate
(`cli.py:5336`) reads `_find_root()/sessions/verified.stamp`. These tests
drive the REAL production entry point -- `verification.main --suite`, not a
hand-written stamp -- and prove the write path and the read path agree:

  1. green  -> the stamp exists at exactly `cli._find_root()/sessions/verified.stamp`
  2. SKIP-only is green too (the claim says PASS or SKIP, no FAIL)
  3. red    -> no stamp is created at all
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import cli  # noqa: E402  (same-dir module, like the other tests)
import locations  # noqa: E402
import verification  # noqa: E402


def _arm(tmp_path: Path, monkeypatch, results: list) -> Path:
    """Point verification.main at a scratch graph and hand it fake results.

    `verification.locations` IS `cli.locations` (one module object), so
    monkeypatching the resolver here makes `cli._find_root()` resolve the
    same scratch graph the suite wrote into -- which is what lets the test
    compare the real write path against the real read path.
    """
    groot = tmp_path / ".agi"
    groot.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(verification.locations, "find_project_root",
                        lambda p=None: groot)
    monkeypatch.setattr(verification.commands, "engine_for",
                        lambda g: str(groot))
    monkeypatch.setattr(verification, "_suite_lock_guard", lambda g: None)
    monkeypatch.setattr(verification, "_git", lambda g, a: "deadbeef")
    monkeypatch.setattr(verification, "run_level", lambda *a, **k: list(results))
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    return groot


def _result(status: str):
    return verification.CheckResult(verification.SUITE_CMD, status, 1.0, None)


def test_green_suite_writes_the_stamp_the_delete_old_gate_reads(
        tmp_path, monkeypatch):
    groot = _arm(tmp_path, monkeypatch, [_result("PASS")])
    assert verification.main(["--suite", "--root", str(tmp_path)]) == 0

    # The gate's own read expression, evaluated through its own resolver.
    gate_reads = cli._find_root() / "sessions/verified.stamp"
    assert gate_reads.exists(), f"no stamp at the path the gate reads: {gate_reads}"
    assert gate_reads == verification._verified_stamp_path(groot)

    body = gate_reads.read_text(encoding="utf-8")
    assert "green suite" in body and "deadbeef" in body, body


def test_skip_only_is_green_too(tmp_path, monkeypatch):
    """SKIP is not FAIL: a suite that skipped everything is still all-green."""
    groot = _arm(tmp_path, monkeypatch, [_result("SKIP")])
    assert verification.main(["--suite", "--root", str(tmp_path)]) == 0
    assert (groot / "sessions/verified.stamp").exists()


def test_red_suite_writes_no_stamp(tmp_path, monkeypatch):
    """A FAIL must never certify itself: the stamp stays absent."""
    groot = _arm(tmp_path, monkeypatch, [_result("FAIL")])
    assert verification.main(["--suite", "--root", str(tmp_path)]) == 1
    assert not (groot / "sessions/verified.stamp").exists()


def test_red_retracts_a_prior_green_stamp(tmp_path, monkeypatch):
    """GREEN then RED: the certification must not outlive the green run.

    cli.py:5336's gate tests EXISTS only, so a stale stamp would pass
    --delete-old on red evidence. The predicate that writes must be the one
    that retracts.
    """
    groot = _arm(tmp_path, monkeypatch, [_result("PASS")])
    assert verification.main(["--suite", "--root", str(tmp_path)]) == 0
    gate = cli._find_root() / "sessions/verified.stamp"
    assert gate.exists()

    _arm(tmp_path, monkeypatch, [_result("FAIL")])
    assert verification.main(["--suite", "--root", str(tmp_path)]) == 1
    assert not gate.exists(), "red run left a green certification standing"


# --- the worktree arm: real resolvers, NO find_project_root monkeypatch -----
# Kid 1's _arm() monkeypatches verification.locations.find_project_root, which
# collapses the writer's resolver and the gate's resolver onto ONE scratch
# graph -- agreement asserted where disagreement is impossible. These tests
# cut a REAL linked git worktree and leave every resolver alone, which is the
# only environment where the writer/reader split this hypothesis exists to
# kill can actually show itself.


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cwd), *args], check=True,
                   capture_output=True, text=True)


def _make_project_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "README").write_text("x")
    graph = repo / ".agi"
    graph.mkdir(parents=True)
    (graph / "config.json").write_text('{"metric_primary": "outcome_coverage"}')
    (graph / "nodes").mkdir(exist_ok=True)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init with graph dir")
    return repo


def _make_worktree(repo: Path, tmp_path: Path, name: str = "wt") -> Path:
    wt = tmp_path / name
    _git(repo, "worktree", "add", "-b", f"loop/slug-{name}@s2", str(wt), "master")
    return wt


def _arm_real(wt: Path, monkeypatch, results: list) -> None:
    """Fake ONLY the suite spawn / lock; leave every resolver real."""
    monkeypatch.setattr(verification, "run_level",
                        lambda *a, **k: [_result(results)])
    monkeypatch.setattr(verification, "_suite_lock_guard", lambda g: None)
    monkeypatch.setattr(verification, "_suite_basetemp_refusal", lambda e: None)
    monkeypatch.setattr(verification, "_git", lambda g, a: "deadbeef")
    monkeypatch.setattr(verification.commands, "engine_for", lambda g: str(wt))
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)


def test_worktree_green_run_satisfies_the_gate_run_from_that_worktree(
        tmp_path, monkeypatch):
    repo = _make_project_repo(tmp_path)
    wt = _make_worktree(repo, tmp_path)
    monkeypatch.chdir(wt)

    wt_graph = locations.find_project_root(wt)
    main_graph = locations.find_project_root(repo)
    shared = locations.shared_sessions_dir(wt_graph) / verification.VERIFIED_STAMP_FILE
    local = verification._verified_stamp_path(wt_graph)
    # The fork is real: the shared-dir write and the gate's local read differ.
    assert local != shared
    assert local == wt_graph / "sessions" / verification.VERIFIED_STAMP_FILE

    _arm_real(wt, monkeypatch, "PASS")
    assert verification.main(["--suite", "--root", str(wt)]) == 0
    gate = cli._find_root() / "sessions/verified.stamp"   # gate's own expression
    assert gate == local
    assert gate.exists(), f"green worktree run certified nothing at {gate}"
    assert shared.exists(), "shared copy must also land for a main-checkout gate"
    assert "deadbeef" in gate.read_text(encoding="utf-8")

    # FAIL writes NOTHING at either path -- in the real worktree, not a patch.
    for p in verification._verified_stamp_paths(wt_graph):
        p.unlink()
    _arm_real(wt, monkeypatch, "FAIL")
    assert verification.main(["--suite", "--root", str(wt)]) == 1
    assert not any(p.exists() for p in verification._verified_stamp_paths(wt_graph))


def test_worktree_red_retracts_a_prior_green_stamp(tmp_path, monkeypatch):
    """GREEN then RED in a REAL worktree: no path the gate can read survives."""
    repo = _make_project_repo(tmp_path)
    wt = _make_worktree(repo, tmp_path)
    monkeypatch.chdir(wt)
    wt_graph = locations.find_project_root(wt)
    paths = verification._verified_stamp_paths(wt_graph)

    _arm_real(wt, monkeypatch, "PASS")
    assert verification.main(["--suite", "--root", str(wt)]) == 0
    assert all(p.exists() for p in paths), paths

    _arm_real(wt, monkeypatch, "FAIL")
    assert verification.main(["--suite", "--root", str(wt)]) == 1
    assert not any(p.exists() for p in paths), [p for p in paths if p.exists()]
    assert cli._find_root() / "sessions/verified.stamp" == paths[0]
