"""goal:g4.18.5.2.1 -- a write's commit survives a busy index.

DG2's measurement (verdict:dg2mvp-w1b): 3 concurrent writers x 20 writes left
29 of 60 uncommitted (index.lock, no retry) while each write exited 0, and the
printed recovery failed for a create (the node is untracked). TMP GIT REPOS
ONLY; the writers are real `write.py` processes.
"""
import json
import subprocess
import sys
import threading
import time
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
WRITE = BIN / "write.py"


def _repo(tmp_path: Path, wait_s: float = 30) -> Path:
    repo = tmp_path / "repo"
    (repo / ".agi" / "nodes" / "doc").mkdir(parents=True)
    for a in (["init", "-q", "-b", "master"], ["config", "user.email", "t@t"],
              ["config", "user.name", "t"]):
        subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True)
    (repo / ".agi" / "config.json").write_text(json.dumps(
        {"values": {"core": {"write_commit_wait_s": wait_s}}}))
    (repo / ".gitignore").write_text(".agi/sessions/\n")
    for i in range(3):
        (repo / ".agi" / "nodes" / "doc" / f"w{i}.md").write_text(
            f'---\nid: doc:w{i}\ntype: doc\ntitle: "w{i}"\nconfidence: 0.5\n'
            f"tags: []\n---\n# doc:w{i}\n\nbody\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "init"], check=True,
                   capture_output=True)
    return repo


def _write(repo: Path, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(WRITE), *argv], cwd=repo,
                          capture_output=True, text=True)


def _commits(repo: Path) -> int:
    return int(subprocess.run(["git", "-C", str(repo), "rev-list", "--count", "HEAD"],
                              capture_output=True, text=True).stdout) - 1


def _dirty(repo: Path) -> list:
    return subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--", ".agi/nodes"],
                          capture_output=True, text=True).stdout.splitlines()


def test_three_concurrent_writers_never_exit_0_over_an_uncommitted_node(tmp_path):
    """Falsifier 1 + 2: 3 writers x 20 writes -> every write is committed, or
    refused NON-ZERO by name; no write exits 0 with its node uncommitted."""
    repo = _repo(tmp_path)
    rcs: list = []

    def writer(i: int) -> None:
        for n in range(20):
            r = _write(repo, f"doc:w{i}", f'set title "w{i} v{n}"')
            rcs.append((i, n, r.returncode, r.stderr))

    threads = [threading.Thread(target=writer, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(rcs) == 60
    bad = [(i, n, rc, e[-200:]) for i, n, rc, e in rcs if rc not in (0, 3)]
    assert not bad, bad
    refused = [(i, n, e) for i, n, rc, e in rcs if rc == 3]
    assert all("commit failed" in e and "UNCOMMITTED" in e for _, _, e in refused)
    # every exit 0 is a commit of its own node; nothing is left behind unnamed
    assert _commits(repo) == sum(1 for *_, rc, _ in rcs if rc == 0)
    if not refused:
        assert _dirty(repo) == [], "60 of 60 committed"
    assert "index.lock" not in " ".join(e for *_, rc, e in rcs if rc == 0 and "commit" in e)


def test_a_busy_index_past_the_budget_refuses_non_zero_and_the_create_recovery_commits(tmp_path):
    """A create meeting a held index.lock past the budget exits 3 by name;
    the printed recovery line ADDS the untracked node, so running it commits."""
    repo = _repo(tmp_path, wait_s=0.6)
    lock = repo / ".git" / "index.lock"
    lock.write_text("held by a fixture writer")
    t0 = time.monotonic()
    body = tmp_path / "b.md"
    body.write_text("fresh body\n")
    r = _write(repo, "create", "doc", "fresh", "--body-file", str(body),
               "--set", "title=fresh")
    assert time.monotonic() - t0 >= 0.5, "it waited out the budget first"
    assert r.returncode == 3, (r.returncode, r.stderr[-300:])
    assert "commit failed after" in r.stderr and "UNCOMMITTED" in r.stderr
    node = repo / ".agi" / "nodes" / "doc" / "fresh.md"
    assert node.is_file(), "the write stays on disk"
    recover = r.stderr.split("recover: ", 1)[1].split("): ", 1)[0]
    assert f"add -- {node}" in recover
    lock.unlink()
    subprocess.run(recover, shell=True, check=True, capture_output=True)
    assert _dirty(repo) == [] and _commits(repo) == 1


def test_a_lock_freed_within_the_budget_lands_the_write(tmp_path):
    """The retry: a lock another writer releases inside the budget is waited
    out and the write lands committed, exit 0."""
    repo = _repo(tmp_path, wait_s=10)
    lock = repo / ".git" / "index.lock"
    lock.write_text("held briefly")
    threading.Timer(1.0, lock.unlink).start()
    r = _write(repo, "doc:w1", 'set title "after the lock"')
    assert r.returncode == 0, r.stderr[-300:]
    assert _dirty(repo) == [] and _commits(repo) == 1


def test_a_peer_commit_inside_the_budget_exits_0_with_the_tree_clean(tmp_path):
    """Falsifier 1: the loser of a same-node race must NOT refuse UNCOMMITTED.
    A Timer frees index.lock and commits the SAME node bytes while this write is
    still in its backoff -- the index's truth is then 'already at HEAD'."""
    repo = _repo(tmp_path, wait_s=10)
    node = repo / ".agi" / "nodes" / "doc" / "w1.md"
    lock = repo / ".git" / "index.lock"
    lock.write_text("held until the peer commits")

    def peer() -> None:
        time.sleep(1.0)
        lock.unlink(missing_ok=True)
        subprocess.run(["git", "-C", str(repo), "add", "--", str(node)],
                       capture_output=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", "peer"],
                       capture_output=True)

    threading.Thread(target=peer, daemon=True).start()
    r = _write(repo, "doc:w1", 'set title "peers tie"')
    assert r.returncode == 0, (r.returncode, r.stderr[-300:])
    assert "UNCOMMITTED" not in r.stderr, r.stderr[-300:]
    assert _dirty(repo) == [], "the index says it is committed, so the tree is clean"
    assert _commits(repo) in (1, 2), "one commit: ours or the peer's, never both lost"


def test_a_lock_held_past_the_budget_never_says_STILL_STAGED_for_an_unstaged_path(tmp_path):
    """Falsifier 3: with index.lock held the reset fails, but `git diff --cached`
    is quiet for the path -- the note must not claim STILL STAGED."""
    repo = _repo(tmp_path, wait_s=0.6)
    lock = repo / ".git" / "index.lock"
    lock.write_text("held by a fixture writer")
    node = repo / ".agi" / "nodes" / "doc" / "w0.md"
    r = _write(repo, "doc:w0", 'set title "never staged"')
    assert r.returncode == 3, (r.returncode, r.stderr[-300:])
    assert "UNCOMMITTED" in r.stderr and "STILL STAGED" not in r.stderr, r.stderr[-300:]
    cached = subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--quiet", "--",
                             str(node)])
    assert cached.returncode == 0, "the path really is unstaged -- the note said so"


def test_an_IGNORED_node_never_exits_0_over_uncommitted_bytes(tmp_path):
    """Falsifier 2, the blind spot `status --porcelain` hides: an IGNORED path
    never shows up as dirty, so a 'clean at HEAD' read over it is a lie. The
    write must refuse UNCOMMITTED, not exit 0 over bytes no commit holds."""
    repo = _repo(tmp_path)
    node = repo / ".agi" / "nodes" / "doc" / "w0.md"
    (repo / ".gitignore").write_text(".agi/sessions/\n.agi/nodes/\n")
    subprocess.run(["git", "-C", str(repo), "rm", "-q", "--cached", "-r", ".agi/nodes"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "ignore the nodes"],
                   check=True, capture_output=True)
    assert subprocess.run(["git", "-C", str(repo), "ls-files", "--error-unmatch", "--",
                           str(node)], capture_output=True).returncode != 0, "untracked"
    hook = repo / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    subprocess.run(["git", "-C", str(repo), "config", "core.hooksPath",
                    str(repo / ".git" / "hooks")], check=True, capture_output=True)
    r = _write(repo, "doc:w0", 'set title "ignored"')
    assert r.returncode == 3, (r.returncode, r.stderr[-300:])
    assert "UNCOMMITTED" in r.stderr, r.stderr[-300:]
    assert "clean at HEAD" not in r.stderr, "an ignored path is NOT clean at HEAD"


def test_a_third_writer_locking_the_peer_commit_instant_still_exits_0_at_the_deadline(tmp_path):
    """Falsifier 4: the peer's commit lands, then a THIRD writer takes
    index.lock in that instant and holds it past the budget. `busy` is a read of
    git's error STRING, so the old path broke at the deadline and refused
    UNCOMMITTED over bytes HEAD already holds. The index's truth must be asked
    on the deadline path too."""
    repo = _repo(tmp_path, wait_s=4.0)
    node = repo / ".agi" / "nodes" / "doc" / "w0.md"
    lock = repo / ".git" / "index.lock"
    lock.write_text("writer A")

    def peer_then_third() -> None:
        time.sleep(1.0)
        lock.unlink(missing_ok=True)
        subprocess.run(["git", "-C", str(repo), "add", "--", str(node)],
                       capture_output=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", "peer carries my bytes"],
                       capture_output=True)
        lock.write_text("writer C")  # the third writer, straight onto the peer
        time.sleep(6.0)
        lock.unlink(missing_ok=True)

    threading.Thread(target=peer_then_third, daemon=True).start()
    r = _write(repo, "doc:w0", 'set title "mine"')
    assert r.returncode == 0, (r.returncode, r.stderr[-400:])
    assert "UNCOMMITTED" not in r.stderr, r.stderr[-400:]
    assert "clean at HEAD" in r.stdout + r.stderr, (r.stdout + r.stderr)[-400:]
    assert _dirty(repo) == [], "HEAD holds the write and the tree is clean"
    assert "mine" in subprocess.run(["git", "-C", str(repo), "show", "HEAD:.agi/nodes/doc/w0.md"],
                                    capture_output=True, text=True).stdout
