"""hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-
commit-is-never-silent -- the pre-commit lock gate and the non-silent commit.

TMP GIT REPOS ONLY. No test here touches a live worktree.
"""
import importlib.util
import json
import os
import shlex
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


def _hold_lock_open(lock):
    """A live process holding `lock` open on fd 9 -- PATH QUOTED (item 5) and
    NO bare sleep for liveness: poll for the fd so a lost race FAILS."""
    holder = subprocess.Popen(
        ["sh", "-c", f"exec 9<{shlex.quote(str(lock))}; exec sleep 30"])
    fddir = Path(f"/proc/{holder.pid}/fd")
    deadline = time.time() + 10
    while time.time() < deadline and not (fddir / "9").exists():
        time.sleep(0.05)
    assert (fddir / "9").exists(), "the holder never opened the lock on fd 9"
    return holder, lock


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
    assert cli._clear_stale_index_lock(root, repo) is None, "clear = a no-op"


def test_a_fresh_lock_is_refused_by_name_and_left_untouched(tmp_path):
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=3600)
    lock = _mklock(repo, 5)              # fresh: inside the cell
    reason = cli._clear_stale_index_lock(root, repo)
    assert reason and "index.lock" in reason and "NOT removed" in reason
    assert lock.exists(), "a FRESH lock is never removed"


def test_a_lock_open_in_some_process_fds_is_never_removed(tmp_path):
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=60)
    holder, lock = _hold_lock_open(_mklock(repo, 3600))
    try:
        reason = cli._clear_stale_index_lock(root, repo)
    finally:
        holder.kill(); holder.wait()
    assert reason and "held=yes" in reason, reason
    assert lock.exists(), "a lock open in an fd is never removed"


def test_a_lock_held_above_an_unreadable_fd_is_never_removed(tmp_path, monkeypatch):
    # The DH.547 falsifier: ONE OSError on ONE fd must skip that fd only, never
    # the rest of the pid's table. Pre-fix, any() propagates the raise and the
    # whole pid is SKIPPED -- a HELD lock is unlinked.
    cli = _cli()
    spaced = tmp_path / "a dir with spaces"   # quoted-path case in the SAME
    spaced.mkdir()                           # test: an unquoted holder dies here
    root, repo = _repo(spaced, stale_s=60)
    holder, lock = _hold_lock_open(_mklock(repo, 3600))

    real = os.readlink

    def fake_readlink(p, *a, **k):
        tail = str(p).rsplit("/", 1)[-1]
        if "/fd/" in str(p) and tail.isdigit() and int(tail) < 9:
            raise PermissionError(f"fd {tail} is not readable by this user")
        return real(p, *a, **k)

    try:
        monkeypatch.setattr(os, "readlink", fake_readlink)
        reason = cli._clear_stale_index_lock(root, repo)
    finally:
        holder.kill(); holder.wait()
    assert reason and "held=yes" in reason, reason
    assert lock.exists(), "a lock HELD above an unreadable fd is never removed"


def test_a_lock_held_by_a_git_with_cwd_in_the_checkout_is_never_removed(tmp_path):
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=60)
    lock = _mklock(repo, 100000)         # 100000s old vs a 60s cell
    holder = subprocess.Popen(["git", "update-index", "--index-info"],
                              cwd=str(repo), stdin=subprocess.PIPE,
                              stdout=subprocess.DEVNULL)
    try:
        assert holder.poll() is None, "the holder must be ALIVE"
        argv = Path(f"/proc/{holder.pid}/cmdline").read_bytes().decode()
        assert str(repo) not in argv, f"the path must not be in argv: {argv}"
        assert not any(str(lock) in str(p) for p in
                       Path(f"/proc/{holder.pid}/fd").iterdir()), \
            "this test must exercise the cwd+comm branch, not the fd branch"
        reason = cli._clear_stale_index_lock(root, repo)
    finally:
        holder.stdin.close()
        holder.wait()
    assert reason and "held=yes" in reason, reason
    assert lock.exists(), "a HELD lock is never removed"


def test_a_missing_threshold_cell_refuses_by_name(tmp_path):
    cli = _cli()
    root, repo = _repo(tmp_path)
    (root / "config.json").write_text(json.dumps({"values": {"core": {}}}))
    lock = _mklock(repo, 100000)
    reason = cli._clear_stale_index_lock(root, repo)
    assert reason and "stale_index_lock_s not set" in reason, reason
    assert lock.exists(), "no threshold cell = never unlink"


def test_a_failed_round_commit_in_a_real_linked_worktree_is_named(tmp_path):
    # Conjunct 2 end to end: a REAL linked worktree whose commit FAILS.
    cli = _cli()
    main = tmp_path / "main"
    env = dict(os.environ, GIT_AUTHOR_NAME="a", GIT_AUTHOR_EMAIL="a@b",
               GIT_COMMITTER_NAME="a", GIT_COMMITTER_EMAIL="a@b")
    subprocess.run(["git", "init", "-q", "-b", "main", str(main)], check=True, env=env)
    (main / "f.txt").write_text("x")
    subprocess.run(["git", "-C", str(main), "add", "f.txt"], check=True, env=env)
    subprocess.run(["git", "-C", str(main), "commit", "-qm", "seed"], check=True, env=env)
    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(main), "worktree", "add", "-qb", "kid", str(wt)],
                   check=True, env=env)
    root = wt / ".agi"
    (root / "nodes" / "verdict").mkdir(parents=True)
    (root / "config.json").write_text(json.dumps({"values": {"core": {"stale_index_lock_s": 900}}}))
    (root / "nodes" / "verdict" / "a00-x.md").write_text("---\nid: verdict:a00-x\ntype: verdict\n---\nbody\n")
    hooks = wt / "hooks"
    hooks.mkdir()
    (hooks / "pre-commit").write_text("#!/bin/sh\nexit 1\n")
    (hooks / "pre-commit").chmod(0o755)
    subprocess.run(["git", "-C", str(wt), "config", "core.hooksPath",
                    str(hooks)], check=True, env=env)
    out = cli._auto_commit_worktree(root, "a00-x", "verdict:a00-x", None, "proved")
    assert isinstance(out, str) and "commit failed" in out, out
    assert "commit FAILED" in cli._parent_harvest_body(
        root, {"agents": []}, "DH.1", "a00-x", {}, commit_failed=out)


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
