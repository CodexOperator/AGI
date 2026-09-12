"""L4.311 — `_button_down_legal_hint` consults `branches.is_legal_branch`.

The dry-run one-liner previously trusted any non-empty `git rev-parse`
output and printed `legal on '<branch>'` even for a post / loop / town
branch the real `grid.py commit --all` refuses. The hint must defer to the
ONE legality rule (branches.is_legal_branch, L4.311) and say NOT legal for
anything except master / season main, WITHOUT duplicating the rule here.

Each test fakes `git rev-parse --abbrev-ref HEAD` via
`monkeypatch.setattr(rotate.subprocess, "run", ...)` and asserts the exact
returned line.
"""
import subprocess
from pathlib import Path

import pytest

import rotate  # noqa: E402

_NOT_LEGAL = ("NOT legal on {branch!r} (grid commit would be SKIPPED \u2014 "
              "season main or master only)")
_LEGAL = "legal on {branch!r}"


def _fake(monkeypatch, branch, returncode=0):
    """Fake git rev-parse to report `branch` and return its CompletedProcess.

    Only the `rev-parse` call is ever made by _button_down_legal_hint, so a
    bare success value in `stdout` is the whole drive surface.
    """
    monkeypatch.setattr(
        rotate.subprocess, "run",
        lambda argv, *a, **k: subprocess.CompletedProcess(
            argv, returncode, f"{branch}\n", ""))


@pytest.fixture
def root(tmp_path):
    return tmp_path


@pytest.mark.parametrize("branch", [
    "season2/posts/x",
    "season2/loops/x",
    "season2/town/season/acme/main",
])
def test_post_loop_town_branches_read_not_legal(root, monkeypatch, branch):
    _fake(monkeypatch, branch)
    assert rotate._button_down_legal_hint(root) == (
        _NOT_LEGAL.format(branch=branch))


@pytest.mark.parametrize("branch", [
    "season2/main",
    "season/s2",
    "master",
])
def test_season_main_and_master_read_legal(root, monkeypatch, branch):
    _fake(monkeypatch, branch)
    assert rotate._button_down_legal_hint(root) == _LEGAL.format(branch=branch)


def test_empty_branch_keeps_existing_line(root, monkeypatch):
    """Empty rev-parse output still reads the SKIPPED no-repo line."""
    _fake(monkeypatch, "", returncode=0)
    assert rotate._button_down_legal_hint(root) == (
        "no repo / unknown branch (grid commit would be SKIPPED)")


def test_nonzero_return_keeps_existing_line(root, monkeypatch):
    """A failing rev-parse (no git repo) keeps the SKIPPED no-repo line."""
    _fake(monkeypatch, "whatever\n", returncode=128)
    assert rotate._button_down_legal_hint(root) == (
        "no repo / unknown branch (grid commit would be SKIPPED)")