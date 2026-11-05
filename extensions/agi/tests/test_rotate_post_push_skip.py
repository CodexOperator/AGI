"""goal:g7.16.1.11.46.28 -- rotate's out push skips a posts/<post> branch that
is NOT the pushing seat's (alive [decision] 23:50:53Z 10-28, 3/3).

`_stops_push` is the rotate-out push. branches.parse does not know
`posts/<post>`, so such a branch has no mirror ref and used to fall through
to a head push to origin: on a post uid with no github helper that push
fails and the rotation stops (SM's [red] 23:4xZ). The skip is keyed on the
SEAT (the one config:posts row whose role is prime_director names the branch
that pushes), never on a missing helper: the pushing seat's own push still
runs and still refuses by name when it cannot authenticate.

Every row runs under a PATH git shim that logs each `push` and fails it
(the "no helper" case); the log is READ, never inferred.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[3]
_BIN = _REPO / "extensions" / "agi" / "bin"
sys.path.insert(0, str(_REPO / "extensions"))
sys.path.insert(0, str(_BIN))

from agi.bin import branches, rotate  # noqa: E402

SKIP = ("stops push: SKIPPED -- posts/sanctuary-master is not the pushing "
        "seat's branch (posts/belam, config:posts role prime_director); "
        "it stays local")


@pytest.fixture(autouse=True)
def _hermetic_git(monkeypatch):
    """A post uid's global core.hooksPath (~/bin) carries the ref-guard that
    refuses a peer's refs/heads/posts/*: these rows build such branches in a
    scratch repo, so git runs without the global or system config."""
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def _git(top, *a):
    return subprocess.run(["git", "-C", str(top), *a], check=True,
                          capture_output=True, text=True).stdout.strip()


def _seed(tmp_path, branch, rows):
    """A repo at tmp_path with a config:posts registry, an `origin` bare
    remote, and `branch` checked out with one commit. Returns (root, bare)."""
    nodes = tmp_path / "nodes" / ".geometry"
    nodes.mkdir(parents=True)
    body = "---\nid: config:posts\ntype: config\nposts:\n"
    body += "".join("  - " + json.dumps(r) + "\n" for r in rows)
    (nodes / "posts.md").write_text(body + "---\n", encoding="utf-8")
    bare = tmp_path.parent / f"{tmp_path.name}-remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "commit.gpgsign", "false")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "seed")
    _git(tmp_path, "checkout", "-q", "-b", branch)
    _git(tmp_path, "commit", "-q", "--allow-empty", "-m", "rotate-out")
    _git(tmp_path, "remote", "add", "origin", str(bare))
    return tmp_path, bare


@pytest.fixture
def shim(tmp_path_factory, monkeypatch):
    """A `git` first on PATH that appends each push's argv to a log and
    fails it like a uid with no github helper; every other call is git's."""
    d = tmp_path_factory.mktemp("gitshim")
    log = d / "push.log"
    real = subprocess.run(["sh", "-c", "command -v git"], capture_output=True,
                          text=True, check=True).stdout.strip()
    (d / "git").write_text(
        "#!/bin/sh\n"
        'for a; do [ "$a" = push ] && { echo "push $*" >>"' + str(log) + '"; '
        "echo \"fatal: could not read Username for 'https://github.com': "
        'No such device or address" >&2; exit 128; }; done\n'
        f'exec "{real}" "$@"\n', encoding="utf-8")
    (d / "git").chmod(0o755)
    monkeypatch.setenv("PATH", f"{d}{os.pathsep}{os.environ['PATH']}")
    return log


def _pushes(log):
    return log.read_text().splitlines() if log.exists() else []


ROWS = [{"name": "belam", "role": "prime_director"},
        {"name": "sanctuary-master"}]


def test_a_non_pushing_post_branch_skips_with_zero_push_calls(
        tmp_path, shim, capsys):
    root, _ = _seed(tmp_path, "posts/sanctuary-master", ROWS)
    assert rotate._stops_push(root, "stops") is None
    err = capsys.readouterr().err
    assert SKIP in err.splitlines(), err
    assert _pushes(shim) == [], _pushes(shim)


def test_b_the_pushing_seat_without_a_helper_attempts_and_refuses_by_name(
        tmp_path, shim, capsys):
    root, _ = _seed(tmp_path, "posts/belam", ROWS)
    out = rotate._stops_push(root, "stops")
    assert out and out.startswith("push refused out: ") and "Username" in out, out
    assert len(_pushes(shim)) == 1, _pushes(shim)
    assert "SKIPPED" not in capsys.readouterr().err


def test_c_the_pushing_seat_with_a_working_remote_is_pushed(tmp_path, capsys):
    root, bare = _seed(tmp_path, "posts/belam", ROWS)
    assert rotate._stops_push(root, "stops") is None
    assert "stops push: OK -- posts/belam" in capsys.readouterr().err
    head = _git(root, "rev-parse", "HEAD")
    assert _git(bare, "rev-parse", "refs/heads/posts/belam") == head


@pytest.mark.parametrize("rows,why", [
    ([{"name": "sanctuary-master"}],
     "0 config:posts rows with role prime_director, want 1"),
    ([{"name": "belam", "role": "prime_director"},
      {"name": "sanctuary-master", "role": "prime_director"}],
     "2 config:posts rows with role prime_director, want 1"),
])
def test_d_an_unread_pushing_seat_says_so_and_attempts_the_push(
        tmp_path, shim, capsys, rows, why):
    root, _ = _seed(tmp_path, "posts/sanctuary-master", rows)
    out = rotate._stops_push(root, "stops")
    assert out and out.startswith("push refused out: "), out
    assert len(_pushes(shim)) == 1, _pushes(shim)
    err = capsys.readouterr().err
    assert (f"stops push: pushing seat unread ({why}); the head push is "
            f"attempted") in err.splitlines(), err


def test_pinned_branches_still_does_not_know_posts_post():
    """F2: the fix stays rotate-side; if branches.parse learns posts/<post>
    (a mirror ref), this row and the skip are re-read together."""
    for b in ("posts/belam", "posts/sanctuary-master"):
        with pytest.raises(ValueError):
            branches.parse(b)
        assert branches.mirror_ref_for_branch(b) is None
        assert not branches.is_remote_visible(b)
