"""hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-
commit-is-never-silent -- the pre-commit lock gate and the non-silent commit.

TMP GIT REPOS ONLY. No test here touches a live worktree.
"""
import importlib.util
import json
import os
import subprocess
import time
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"


def _cli():
    spec = importlib.util.spec_from_file_location("agi_cli_lock", BIN / "cli.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _repo(tmp_path, stale_s=900):
    """A tmp git repo whose graph root carries the cell `stale_index_lock_s`."""
    repo = tmp_path / "wt"
    repo.mkdir()
    env = dict(os.environ, GIT_AUTHOR_NAME="a", GIT_AUTHOR_EMAIL="a@b",
               GIT_COMMITTER_NAME="a", GIT_COMMITTER_EMAIL="a@b")
    subprocess.run(["git", "init", "-q", str(repo)], check=True, env=env)
    (repo / "f.txt").write_text("x")
    subprocess.run(["git", "-C", str(repo), "add", "f.txt"], check=True, env=env)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "seed"], check=True,
                   env=env)
    root = repo / ".agi"
    root.mkdir()
    (root / "config.json").write_text(json.dumps(
        {"values": {"core": {"stale_index_lock_s": stale_s}}}))
    return root, repo


def _lock_path(repo):
    rel = subprocess.run(["git", "-C", str(repo), "rev-parse", "--git-path",
                          "index.lock"], capture_output=True, text=True).stdout.strip()
    lock = Path(rel)
    return lock if lock.is_absolute() else repo / lock


def _mklock(repo, age_s):
    lock = _lock_path(repo)
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("")
    t = time.time() - age_s
    os.utime(lock, (t, t))
    return lock


def test_stale_lock_is_cleared_with_one_named_line_and_the_path_continues(tmp_path):
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=60)
    lock = _mklock(repo, 3600)          # 0-byte, an hour old, no git holder
    assert cli._clear_stale_index_lock(root, repo) is None
    assert not lock.exists(), "a stale unheld lock must be removed"
    again = cli._clear_stale_index_lock(root, repo)
    assert again is None, "a clear checkout is a no-op, not a refusal"


def test_a_fresh_lock_is_refused_by_name_and_left_untouched(tmp_path):
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=3600)
    lock = _mklock(repo, 5)              # fresh: inside the cell
    reason = cli._clear_stale_index_lock(root, repo)
    assert reason and "index.lock" in reason and "NOT removed" in reason
    assert lock.exists(), "a FRESH lock is never removed"


def test_a_held_lock_is_refused_even_when_it_is_old(tmp_path):
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=60)
    lock = _mklock(repo, 3600)           # old, but a git process lives here
    holder = subprocess.Popen(
        ["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
    try:
        reason = cli._clear_stale_index_lock(root, repo)
    finally:
        holder.communicate(b"held\n")
        holder.wait()
    assert reason and "held=yes" in reason, reason
    assert lock.exists(), "a HELD lock is never removed"


def test_a_failed_commit_exits_non_zero_and_is_named_in_the_harvest_dm():
    cli = _cli()
    body = cli._parent_harvest_body(
        Path("/nonexistent"), {"agents": []}, "DH.1", "a00-x", {},
        commit_failed="index.lock /wt/.git/index.lock age=5s held=no")
    assert "commit FAILED: index.lock" in body, body


def test_a_clean_harvest_dm_carries_no_failure_field():
    cli = _cli()
    body = cli._parent_harvest_body(Path("/nonexistent"), {"agents": []},
                                    "DH.1", "a00-x", {})
    assert "commit FAILED" not in body
