"""hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-
commit-is-never-silent -- the pre-commit lock gate and the non-silent commit.

TMP GIT REPOS ONLY. No test here touches a live worktree.
"""
import argparse
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


def _hold_lock_open(lock, as_git=False):
    """A live process holding `lock` open on fd 9 -- PATH QUOTED (item 5) and
    NO bare sleep for liveness: poll for the fd so a lost race FAILS. `as_git`
    execs git AFTER the open, so the holder's `comm` really IS git (fd 9
    survives the exec) -- the uninspectable-git shape DH.564 must refuse on."""
    cmd = f"exec 9<{shlex.quote(str(lock))}; "
    cmd += "exec git hash-object --stdin" if as_git else "exec sleep 30"
    holder = subprocess.Popen(["sh", "-c", cmd], stdin=subprocess.PIPE,
                              stdout=subprocess.DEVNULL)
    try:
        fddir = Path(f"/proc/{holder.pid}/fd")
        deadline = time.time() + 10
        while time.time() < deadline and not (fddir / "9").exists():
            time.sleep(0.05)
        assert (fddir / "9").exists(), "the holder never opened the lock on fd 9"
        if as_git:
            assert Path(f"/proc/{holder.pid}/comm").read_text().strip() == "git", \
                "the holder's comm must be git for this shape"
    except BaseException:   # the assert path must NOT orphan `sh`/`sleep 30`
        holder.kill(); holder.wait()
        raise
    return holder, lock


def _linked_wt(tmp_path):
    """A tmp linked worktree whose pre-commit hook ALWAYS fails, plus the
    graph root inside it -- the shape a `--branch` parent's `done` commits."""
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
    (root / "config.json").write_text(json.dumps(
        {"values": {"core": {"stale_index_lock_s": 900}}}))
    (root / "nodes" / "verdict" / "a00-t.md").write_text(
        "---\nid: verdict:a00-t\ntype: verdict\n---\nbody\n")
    hooks = wt / "hooks"
    hooks.mkdir()
    (hooks / "pre-commit").write_text("#!/bin/sh\nexit 1\n")
    (hooks / "pre-commit").chmod(0o755)
    subprocess.run(["git", "-C", str(wt), "config", "core.hooksPath",
                    str(hooks)], check=True, env=env)
    return wt, root


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
    wt, root = _linked_wt(tmp_path)
    out = cli._auto_commit_worktree(root, "a00-t", "verdict:a00-t", None, "proved")
    assert isinstance(out, str) and "commit failed" in out, out
    assert "commit FAILED" in cli._parent_harvest_body(
        root, {"agents": []}, "DH.1", "a00-t", {}, commit_failed=out)


def test_a_failed_round_commit_exits_3_and_names_itself_in_the_dm(tmp_path, monkeypatch):
    # DH.564 item 2: cli.py's `return 3` was executed by NO test -- the old
    # test re-derived the harvest body. This drives cmd_done ITSELF, so the
    # lines that return 3 (commit_fail -> ERR + return) run live. Only the dm
    # TRANSPORT is stubbed: the reason it carries is asserted, not delivered.
    cli = _cli()
    wt, root = _linked_wt(tmp_path)
    (root / "nodes" / "experiment").mkdir(parents=True)
    (root / "nodes" / "experiment" / "a00-t.md").write_text(
        "---\nid: experiment:a00-t\ntype: experiment\n---\nbody\n")
    rec = root / "sessions" / cli.locations.iteration_dirname("DH.9") / "a00-t"
    rec.mkdir(parents=True)
    (rec / "agent.json").write_text(json.dumps(
        {"agent_id": "a00-t", "tier": "kid", "status": "running",
         "asked": ["verdict:a00-t"], "node_id": "verdict:a00-t"}))
    seen = {}
    monkeypatch.setattr(cli, "_alarm_dispatcher_on_done",
                        lambda *a, **k: seen.update(k) or 0)
    monkeypatch.chdir(wt)
    rc = cli.cmd_done(argparse.Namespace(
        iter_n="DH.9", agent_id="a00-t", verdict="proved", confidence=0.9,
        node_id="verdict:a00-t", parent=None, notes="", next_edge=None,
        push_further=None, owns=None, evidence_runs=["experiment:a00-t"],
        probes=None, dry_run=False, no_evidence_gate=False,
        no_spawn_gate=False))
    assert rc == 3, f"a FAILED round commit must exit 3, not {rc}"
    assert seen.get("commit_failed"), "the dm must carry the failure reason"
    assert "commit FAILED:" in cli._parent_harvest_body(
        root, {"agents": []}, "DH.9", "a00-t", {},
        commit_failed=seen["commit_failed"])


def test_a_lock_held_under_an_unlistable_fd_dir_is_refused_by_name(tmp_path, monkeypatch):
    # DH.564: `except OSError: fds = []` on the fd DIRECTORY dropped the whole
    # pid -- the per-fd bug one level up -- and unlinked a HELD lock. The fix
    # is refuse-to-unlink: an unreadable table is NOT an empty table.
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=60)
    holder, lock = _hold_lock_open(_mklock(repo, 3600), as_git=True)
    real = os.listdir

    def fake_listdir(p, *a, **k):
        if str(p) == f"/proc/{holder.pid}/fd":
            raise PermissionError(13, "Permission denied", str(p))
        return real(p, *a, **k)

    try:
        monkeypatch.setattr(os, "listdir", fake_listdir)
        reason = cli._clear_stale_index_lock(root, repo)
    finally:
        holder.kill(); holder.wait()
    assert reason and "NOT removed" in reason, reason
    assert lock.exists(), "an unlistable fd dir must REFUSE, never unlink"


def _unlistable(monkeypatch, pid, exc, err):
    """Make /proc/<pid>/fd unreadable, for the shape the walk cannot see."""
    real = os.listdir

    def fake(p, *a, **k):
        if str(p) == f"/proc/{pid}/fd":
            raise exc(err, "unreadable", str(p))
        return real(p, *a, **k)

    monkeypatch.setattr(os, "listdir", fake)


def test_a_lock_held_by_an_uninspectable_NON_GIT_holder_is_refused(tmp_path, monkeypatch):
    # Item 5: the shipped test built its holder `as_git=True` -- the ONE comm
    # the allowlist still refused -- so it could only be green, and an editor /
    # backup / scanner holding the lock open was ALLOWLISTED OUT and unlinked.
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=60)
    holder, lock = _hold_lock_open(_mklock(repo, 3600), as_git=False)
    _unlistable(monkeypatch, holder.pid, PermissionError, 13)
    try:
        reason = cli._clear_stale_index_lock(root, repo)
    finally:
        holder.kill(); holder.wait()
    assert reason and "NOT removed" in reason, reason
    assert lock.exists(), "an uninspectable NON-git holder must REFUSE, never unlink"


def test_a_kids_failed_commit_is_named_in_the_dm_its_parent_receives(tmp_path, monkeypatch):
    # Item 6: the exit-3 test stubbed `_alarm_dispatcher_on_done` ITSELF, so the
    # real dm builder (the only code that turns `commit_failed` into a body
    # anyone RECEIVES) never ran. Here only the TRANSPORT is stubbed: what
    # `send.send` was called with is the assertion, on the real builder.
    cli = _cli()
    wt, root = _linked_wt(tmp_path)
    rec = root / "sessions" / cli.locations.iteration_dirname("DH.9") / "a00-t"
    rec.mkdir(parents=True)
    row = {"id": "a00-t", "tier": "kid", "status": "running",
           "spawned_by_agent": "a00-par", "node_id": "verdict:a00-t"}
    (rec / "agent.json").write_text(json.dumps({**row, "agent_id": "a00-t",
                                                "asked": ["verdict:a00-t"]}))
    (rec.parent / "manifest.json").write_text(json.dumps({"agents": [row]}))
    sent = {}
    import send as _send
    monkeypatch.setattr(_send, "send", lambda *a, **k: sent.update(a=a) or 0)
    monkeypatch.setenv("AGI_TIER", "kid")
    monkeypatch.chdir(wt)
    rc = cli.cmd_done(argparse.Namespace(
        iter_n="DH.9", agent_id="a00-t", verdict="proved", confidence=0.9,
        node_id="verdict:a00-t", parent=None, notes="", next_edge=None,
        push_further=None, owns=None, evidence_runs=["verdict:a00-t"],
        probes=None, dry_run=False, no_evidence_gate=False,
        no_spawn_gate=False))
    assert rc == 3, f"a FAILED round commit must exit 3, not {rc}"
    assert sent.get("a"), "the parent must be dm'd, not the seat"
    assert "a00-par" in sent["a"], sent["a"]
    assert "commit FAILED:" in sent["a"][2], sent["a"]
    # item 4: the record must not read `done` after a failed commit
    rec_after = json.loads((rec / "agent.json").read_text())
    assert rec_after["status"] == "failed"
    # MISS 1: the restamp is of the AGENT RECORD. The manifest entry
    # DELIBERATELY stays `done`: `_mirror_terminal_into_manifest` ranks
    # failed(3) BELOW done(5) and the `rec_rank >= _merge_status_rank(entry)`
    # guard leaves its target None, so a manifest reading `failed` would send
    # workflow.py's round-wait into its FIRST branch and DROP the whole
    # harvest. The rank guard is load-bearing; the reason lives in the record.
    mrow = next(e for e in json.loads((rec.parent / "manifest.json").read_text())["agents"]
                if e["id"] == "a00-t")
    assert mrow["status"] == "done", mrow
    assert "commit FAILED:" in rec_after["fail_reason"]


def test_a_pid_that_exited_mid_walk_is_not_a_holder(tmp_path, monkeypatch):
    # Item 7: the ENOENT arm keeps the gate usable and had NO test.
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=60)
    lock = _mklock(repo, 3600)
    gone = str(max(int(p) for p in os.listdir("/proc") if p.isdigit()) + 7)
    _unlistable(monkeypatch, int(gone), FileNotFoundError, 2)
    assert cli._uninspectable(f"/proc/{gone}", FileNotFoundError(2, "gone")) == ""
    assert cli._clear_stale_index_lock(root, repo) is None
    assert not lock.exists(), "a stale unheld lock must still clear"


def test_a_comm_that_cannot_be_read_still_names_the_refusal(tmp_path, monkeypatch):
    # Item 7: the `?` arm (our uid, our own fd dir, no comm) had NO test.
    cli = _cli()
    real_read = Path.read_text

    def fake_read(self, *a, **k):
        if str(self).endswith("/comm"):
            raise PermissionError(13, "Permission denied")
        return real_read(self, *a, **k)

    monkeypatch.setattr(Path, "read_text", fake_read)
    assert cli._uninspectable(f"/proc/{os.getpid()}",
                              PermissionError(13, "denied")) == "?"


def _a_live_same_uid_pid_not_us():
    """A REAL, live, same-uid pid that is not this process -- read out of THIS
    process's own /proc table, never invented, and never a `git`."""
    for p in sorted(os.listdir("/proc"), key=lambda x: int(x) if x.isdigit() else 0):
        if not p.isdigit() or int(p) == os.getpid():
            continue
        try:
            if os.stat(f"/proc/{p}").st_uid != os.getuid():
                continue
            if Path(f"/proc/{p}/comm").read_text().strip() == "git":
                continue
        except OSError:
            continue
        return p
    raise AssertionError("no live same-uid non-git pid in this process's /proc")


def test_a_pid_that_exits_between_the_fd_listing_and_the_stat_is_not_a_holder(tmp_path, monkeypatch):
    # MISS 2: the ENOENT arm only covered the exc raised BY the listdir. A pid
    # whose fd table came back dark and that then EXITED before the stat was
    # returned as an UNKNOWN HOLDER ("?"), refusing every commit on a host that
    # spawns and reaps agents. No test covered the stat arm; this one drives
    # both halves on a REAL same-uid pid out of this process's own /proc.
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=60)
    lock = _mklock(repo, 3600)
    pid = int(_a_live_same_uid_pid_not_us())
    _unlistable(monkeypatch, pid, PermissionError, 13)   # the fd table is dark
    real = os.stat

    def fake_stat(p, *a, **k):                            # ... and the pid is
        if str(p).startswith(f"/proc/{pid}"):            # GONE by the stat
            raise FileNotFoundError(2, "No such file or directory", str(p))
        return real(p, *a, **k)

    monkeypatch.setattr(os, "stat", fake_stat)
    assert cli._uninspectable(f"/proc/{pid}", PermissionError(13, "denied")) == ""
    assert cli._clear_stale_index_lock(root, repo) is None, \
        "a pid that exited mid-walk must not refuse the whole commit"
    assert not lock.exists(), "a stale unheld lock must still clear"


def test_a_stat_that_fails_with_anything_but_ENOENT_still_refuses(tmp_path, monkeypatch):
    # The other half of MISS 2: the fix is NARROW. EACCES on the stat is not
    # an exit and must keep returning the "?" UNKNOWN-HOLDER refusal, and the
    # gate must still refuse BY NAME on it.
    cli = _cli()
    root, repo = _repo(tmp_path, stale_s=60)
    lock = _mklock(repo, 3600)
    pid = int(_a_live_same_uid_pid_not_us())
    _unlistable(monkeypatch, pid, PermissionError, 13)
    real = os.stat

    def fake_stat(p, *a, **k):
        if str(p).startswith(f"/proc/{pid}"):
            raise PermissionError(13, "Permission denied", str(p))
        return real(p, *a, **k)

    monkeypatch.setattr(os, "stat", fake_stat)
    assert cli._uninspectable(f"/proc/{pid}", PermissionError(13, "denied")) == "?"
    reason = cli._clear_stale_index_lock(root, repo)
    assert reason and "NOT removed" in reason, reason
    assert lock.exists(), "an unreadable stat is never a licence to unlink"


def test_a_malformed_config_refuses_by_name_and_never_unlinks(tmp_path):
    # Item 8: the `except (OSError, ValueError, ...)` refusal had NO test.
    cli = _cli()
    root, repo = _repo(tmp_path)
    (root / "config.json").write_text("{not json")
    lock = _mklock(repo, 3600)
    reason = cli._clear_stale_index_lock(root, repo)
    assert reason and "index.lock check failed" in reason, reason
    assert lock.exists(), "a malformed config is never a licence to unlink"


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
