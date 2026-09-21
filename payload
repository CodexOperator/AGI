"""Tests for the grid coverage checker (hypothesis:l3-engine-files-outside-the-grid).

Three properties, each on a throwaway git repo so the checker's enumeration
(git ls-files) is real:

1. exits 0 when every tracked engine code file has a payload_ref
2. exits nonzero when a tracked code file has no payload_ref (a real gap)
3. an excluded path is reported with its reason, not silently skipped

The engine-root and exclusion-file arguments exist so the tests point the
checker at their own fixture tree instead of the live checkout.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
CHECKER = BIN / "grid_coverage_check.py"


@pytest.fixture
def engine_repo(tmp_path):
    """A bare git repo shaped like an agi engine with .agi/nodes inside it."""
    repo = tmp_path / "engine"
    (repo / "extensions" / "agi" / "bin").mkdir(parents=True)
    (repo / ".agi" / "nodes" / "build").mkdir(parents=True)
    (repo / ".agi" / "context").mkdir(parents=True)
    subprocess.run(["git", "init"], cwd=repo, capture_output=True, check=True)
    # a tracked engine code file
    (repo / "extensions" / "agi" / "bin" / "rotate.py").write_text(
        "def rotate(): pass\n")
    return repo


def _git_add_all(repo: Path) -> None:
    subprocess.run(["git", "add", "-A"], cwd=repo, capture_output=True, check=True)


def _check(repo: Path, exclusions: Path | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(CHECKER), "--engine", str(repo)]
    if exclusions is not None:
        cmd += ["--exclusions", str(exclusions)]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_clean_when_every_file_covered(engine_repo):
    """Exits 0 when every tracked code file has a build node payload_ref."""
    node = engine_repo / ".agi" / "nodes" / "build" / "rotate.md"
    node.write_text(
        "---\n"
        "id: build:rotate\n"
        "payload_ref: extensions/agi/bin/rotate.py\n"
        "---\n"
        "body\n")
    _git_add_all(engine_repo)

    proc = _check(engine_repo)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "clean" in proc.stdout


def test_nonzero_when_file_has_no_payload_ref(engine_repo):
    """Exits 1 when a tracked code file has no build node (a real gap)."""
    _git_add_all(engine_repo)

    proc = _check(engine_repo)
    assert proc.returncode == 1, "tracked file with no payload_ref must fail"
    assert "OUTSIDE the grid" in proc.stdout
    verbose = subprocess.run(
        [sys.executable, str(CHECKER), "--engine", str(engine_repo), "--verbose"],
        capture_output=True, text=True)
    assert "extensions/agi/bin/rotate.py" in verbose.stdout


def test_excluded_path_reported_with_reason(engine_repo):
    """An excluded path is named and skipped, but only when declared.

    Declaration lives in the exclusion DATA file; without it the same file is
    a gap. Assert both directions so a reader sees the exclusion is what
    turns red green — not a silent editing of the checker.
    """
    node = engine_repo / ".agi" / "nodes" / "build" / "rotate.md"
    node.write_text(
        "---\n"
        "id: build:rotate\n"
        "payload_ref: extensions/agi/bin/rotate.py\n"
        "---\n"
        "body\n")
    # a second code file with no node
    (engine_repo / "extensions" / "agi" / "bin" / "spare.sh").write_text(
        "#!/bin/sh\necho spare\n")
    _git_add_all(engine_repo)

    # without an exclusion, spare.sh is a gap -> exit 1
    bare = _check(engine_repo)
    assert bare.returncode == 1

    # declare the exclusion with a reason -> still exits 0 because nothing
    # is uncovered, and the excluded path is reported with its reason when
    # verbose (not silently skipped).
    exclusions = engine_repo / ".agi" / "context" / "grid-coverage-exclusions.md"
    exclusions.write_text(
        "# declared exclusions\n"
        "extensions/agi/bin/spare.sh | scratch script, deliberately ungridded\n")
    guarded = _check(engine_repo)
    assert guarded.returncode == 0, guarded.stdout + guarded.stderr

    # prove the reason surfaces when verbose, so an exclusion is a declared
    # decision a reader can see rather than a silent skip.
    verbose = subprocess.run(
        [sys.executable, str(CHECKER), "--engine", str(engine_repo),
         "--exclusions", str(exclusions), "--verbose"],
        capture_output=True, text=True)
    assert verbose.returncode == 0, verbose.stdout + verbose.stderr
    assert "EXCLUDED: extensions/agi/bin/spare.sh" in verbose.stdout
    assert "scratch script, deliberately ungridded" in verbose.stdout