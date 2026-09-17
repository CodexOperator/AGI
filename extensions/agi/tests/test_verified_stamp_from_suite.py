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

import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import cli  # noqa: E402  (same-dir module, like the other tests)
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
