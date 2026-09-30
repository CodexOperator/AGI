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
    # a write after a refused one on the SAME node meets that prior uncommitted write: the
    # launder guard legitimately refuses it (no other dirt is admitted: the predecessor must be rc 3)
    prev = {(i, n): rc for i, n, rc, _ in rcs}
    assert all(("commit failed" in e or ("already dirty against HEAD" in e and prev.get((i, n - 1)) == 3))
               and "UNCOMMITTED" in e for i, n, e in refused)
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
    # NO hook fixture: the session exports GIT_CONFIG_COUNT/KEY_0/VALUE_0 =
    # core.hooksPath, and command line config outranks repo config, so a
    # core.hooksPath set HERE never fires -- the row used to pass for a reason
    # its docstring did not claim. What actually refuses is `git add` on an
    # ignored path (rc 1, "use -f"), so the assertion rests on that: no ls-files
    # row means the index does not hold the path, hence not clean at HEAD.
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
    # the PROPERTY, not the note string: between the peer unlinking index.lock
    # and writer C re-taking it a backoff retry can slip through and make this
    # writer's own real commit -- both outcomes are a commit of these bytes, and
    # git cannot commit at all while C's lock is held, so the window is closed
    # by asserting the index's truth rather than by ordering the fixture.
    assert _dirty(repo) == [], "HEAD holds the write and the tree is clean"
    assert "mine" in subprocess.run(["git", "-C", str(repo), "show", "HEAD:.agi/nodes/doc/w0.md"],
                                    capture_output=True, text=True).stdout


def test_a_SKIP_WORKTREE_node_is_never_called_clean_at_HEAD(tmp_path):
    """Falsifier 2, the SECOND blind spot (row 2): `skip-worktree` hides the
    worktree bytes from status AND from `git commit`, and `ls-files
    --error-unmatch` is happy for such a path -- so the 'clean at HEAD' read
    said yes over bytes NO commit holds. Measured pre-fix: rc 0 "clean at HEAD",
    HEAD still carrying the OLD title. Only a plain `H` ls-files row is the
    index's truth, so this write must refuse UNCOMMITTED."""
    repo = _repo(tmp_path, wait_s=0.6)
    node = repo / ".agi" / "nodes" / "doc" / "w0.md"
    subprocess.run(["git", "-C", str(repo), "update-index", "--skip-worktree", str(node)],
                   check=True, capture_output=True)
    tag = subprocess.run(["git", "-C", str(repo), "ls-files", "-v", "--", str(node)],
                         capture_output=True, text=True).stdout
    assert tag.startswith("S "), tag
    lock = repo / ".git" / "index.lock"
    lock.write_text("held by a fixture writer")
    r = _write(repo, "doc:w0", 'set title "skip me"')
    assert r.returncode == 3, (r.returncode, r.stderr[-300:])
    assert "UNCOMMITTED" in r.stderr, r.stderr[-300:]
    assert "clean at HEAD" not in r.stderr, "an S path is never clean at HEAD"
    head = subprocess.run(["git", "-C", str(repo), "show", "HEAD:.agi/nodes/doc/w0.md"],
                          capture_output=True, text=True).stdout
    assert 'title: "w0"' in head and 'title: "skip me"' not in head, head[:200]
    assert 'skip me' in node.read_text(), "the bytes stay on disk, named"


def test_a_payload_OUTSIDE_the_work_tree_never_says_STILL_STAGED(tmp_path):
    """Row 1: `git diff --cached` returns git's ERROR rc 128 for a path outside
    the work tree, and `!= 0` read that as STAGED. Only rc 1 is staged; an error
    says its own note instead."""
    sys.path.insert(0, str(BIN))
    import write  # noqa: PLC0415
    from types import SimpleNamespace  # noqa: PLC0415
    repo = _repo(tmp_path, wait_s=0.6)
    node = repo / ".agi" / "nodes" / "doc" / "w0.md"
    lock = repo / ".git" / "index.lock"
    lock.write_text("held by a fixture writer")
    note, uncommitted = write._commit_write(repo, "doc:w0", SimpleNamespace(
        path=node, payload_changed=True, payload_path="/etc/hosts"))
    assert uncommitted and "STILL STAGED" not in note, note[-300:]
    assert "STAGED check itself failed" in note, note[-300:]


def test_a_BUSY_retry_pays_no_index_read(tmp_path):
    """Row 5: the at_head read must run only on a path that can return on it
    (a non-busy failure, or the deadline). A retry under a held index.lock used
    to pay `ls-files -v` + `status` on EVERY try -- the cheap backoff path paid
    the very read it was widened to avoid."""
    sys.path.insert(0, str(BIN))
    import write  # noqa: PLC0415
    from types import SimpleNamespace  # noqa: PLC0415
    repo = _repo(tmp_path, wait_s=10)
    node = repo / ".agi" / "nodes" / "doc" / "w0.md"
    # the write has already rewritten the node, as main() does before _commit_write
    node.write_text(node.read_text().replace('title: "w0"', 'title: "mine"'))
    lock = repo / ".git" / "index.lock"
    lock.write_text("held across several retries")
    threading.Timer(2.0, lock.unlink).start()
    seen: list = []
    real = subprocess.run

    def spy(*a, **k):
        argv = a[0] if a else k.get("args")
        if isinstance(argv, list) and "ls-files" in argv:
            seen.append(argv)
        return real(*a, **k)

    write.subprocess.run = spy
    try:
        note, uncommitted = write._commit_write(repo, "doc:w0", SimpleNamespace(
            path=node, payload_changed=False, payload_path=None))
    finally:
        write.subprocess.run = real
    assert not uncommitted and not seen, (note[-200:], seen)
    assert _dirty(repo) == [], "the retry landed the write committed"


# --- g1315131: a held suite lock is WAITED; a live peer's in-flight write is no hand edit ---
def _holder(repo: Path, secs: float):
    """A live child holding the tmp suite lock; reaped by a thread so its pid reads dead on release."""
    p = subprocess.Popen([sys.executable, "-c", f"import time;time.sleep({secs});print(time.time())"],
                         stdout=subprocess.PIPE, text=True)
    (repo / ".agi" / "sessions").mkdir(exist_ok=True)
    (repo / ".agi" / "sessions" / "verify-suite.lock").write_text(f"{p.pid}\n")
    return p


def _cfg(repo: Path, **cell) -> None:
    (repo / ".agi" / "config.json").write_text(json.dumps({"values": {"core": {"suite_lock": cell}}}))


def test_a_held_suite_lock_released_inside_the_bound_commits_after_the_release(tmp_path):
    repo = _repo(tmp_path)
    _cfg(repo, hold_wait_s=30)
    p = _holder(repo, 2)
    threading.Thread(target=p.wait).start()
    r = _write(repo, "doc:w1", 'set title "after the release"')
    released = float(p.stdout.read())
    ct = float(subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%ct"],
                              capture_output=True, text=True).stdout)
    assert r.returncode == 0, r.stderr[-300:]
    assert int(ct) >= int(released), "committed only after the holder was gone"
    assert _dirty(repo) == [] and _commits(repo) == 1


def test_a_held_suite_lock_past_the_bound_exits_3_naming_the_wait(tmp_path):
    repo = _repo(tmp_path)
    _cfg(repo, hold_wait_s=0.6)
    p = _holder(repo, 30)
    t0 = time.monotonic()
    r = _write(repo, "doc:w1", 'set title "never"')
    p.kill(); p.wait()
    assert time.monotonic() - t0 >= 0.6
    assert r.returncode == 3 and f"live pid {p.pid} after waiting 0.6s" in r.stderr, r.stderr[-300:]
    assert _commits(repo) == 0


def test_concurrent_same_node_writers_are_never_refused_as_a_hand_edit(tmp_path):
    repo = _repo(tmp_path)
    errs: list = []

    def writer(i: int) -> None:
        for n in range(4):
            r = _write(repo, "doc:w0", f'set title "w0 {i}.{n}"')
            errs.append((r.returncode, r.stderr))

    ts = [threading.Thread(target=writer, args=(i,)) for i in range(5)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert not [e for _, e in errs if "already dirty" in e or "hand edit" in e]
    assert all(rc == 0 for rc, _ in errs), [e[-200:] for rc, e in errs if rc]
    assert _dirty(repo) == [] and _commits(repo) == 20


def test_pre_dirty_waits_a_live_peer_marker_and_ignores_a_dead_one(tmp_path):
    sys.path.insert(0, str(BIN))
    import write  # noqa: PLC0415
    repo = _repo(tmp_path)
    root, node = repo / ".agi", repo / ".agi" / "nodes" / "doc" / "w1.md"
    node.write_text(node.read_text() + "peer bytes\n")
    peer = subprocess.Popen([sys.executable, "-c", "import time;time.sleep(30)"])
    write._inflight(root, [str(node)], True)
    marker = next((root / "sessions" / "write-inflight").iterdir())
    live = marker.with_name(f"{marker.name.split('.')[0]}.{peer.pid}.x")
    marker.rename(live); write._INFLIGHT.clear()
    def peer_commits():
        subprocess.run(["git", "-C", str(repo), "commit", "-qam", "peer"], capture_output=True)
        live.unlink()
    threading.Timer(0.6, peer_commits).start()
    t0 = time.monotonic()
    assert write._pre_dirty(root, "doc:w1") == set() and time.monotonic() - t0 >= 0.5
    write._inflight_clear(); peer.kill(); peer.wait()
    node.write_text(node.read_text() + "hand edit\n")                # no live marker: a real hand edit
    dead = live.with_name(f"{live.name.split('.')[0]}.{peer.pid}.x")
    dead.write_text("x")                                             # stale (dead pid): ignored + removed
    assert write._pre_dirty(root, "doc:w1") == {str(node)} and not dead.exists()
    write._inflight_clear()


def test_a_marker_with_pid_zero_or_not_an_int_is_stale_not_a_stall(tmp_path):
    sys.path.insert(0, str(BIN))
    import write  # noqa: PLC0415
    root = tmp_path / ".agi"
    d = root / "sessions" / "write-inflight"
    d.mkdir(parents=True)
    k = write.hashlib.sha1(b"/n.md").hexdigest()[:16]
    bad = [d / f"{k}.{x}.r" for x in ("0", "-3", "abc", "", "99999999999999999999")]
    [b.write_text("") for b in bad]
    t0 = time.monotonic()
    assert write._inflight(root, ["/n.md"]) == [] and not any(b.exists() for b in bad)
    assert time.monotonic() - t0 < 2
    mine = write._inflight(root, ["/n.md"], True)                    # this call's markers only
    other = write._inflight(root, ["/n.md"], True)
    write._inflight_clear(other)
    assert all(f.exists() for f in mine) and not any(f.exists() for f in other)
    write._inflight_clear()


def test_hold_wait_s_rejects_inf_nan_negative_with_one_warning(tmp_path, capsys):
    sys.path.insert(0, str(BIN))
    import verification  # noqa: PLC0415
    assert verification.suite_lock_policy(tmp_path)["hold_wait_s"] == 90.0     # STOPGAP default
    (tmp_path / "config.json").write_text("")
    for bad in ("inf", "nan", -1, "x"):
        verification._SUITE_LOCK_REFUSED.clear()
        (tmp_path / ".agi").mkdir(exist_ok=True)
        (tmp_path / ".agi" / "config.json").write_text(json.dumps(
            {"values": {"core": {"suite_lock": {"hold_wait_s": bad}}}}))
        assert verification.suite_lock_policy(tmp_path)["hold_wait_s"] == 90.0, bad
        assert verification.suite_lock_policy(tmp_path)["hold_wait_s"] == 90.0
        assert capsys.readouterr().err.count("hold_wait_s") == 1, bad


def test_a_lock_taken_mid_retry_refuses_instead_of_committing_under_it(tmp_path):
    repo = _repo(tmp_path)
    _cfg(repo, hold_wait_s=0.3, write_commit_wait_s=20)
    idx = repo / ".git" / "index.lock"
    idx.write_text("busy")
    p = subprocess.Popen([sys.executable, "-c", "import time;time.sleep(30)"])
    def take():
        (repo / ".agi" / "sessions").mkdir(exist_ok=True)
        (repo / ".agi" / "sessions" / "verify-suite.lock").write_text(f"{p.pid}\n")
        idx.unlink()                       # the next retry could commit -- but the lock is now held
    threading.Timer(0.6, take).start()
    r = _write(repo, "doc:w1", 'set title "under the lock"')
    p.kill(); p.wait()
    assert r.returncode == 3 and f"live pid {p.pid} after waiting 0.3s" in r.stderr, r.stderr[-300:]
    assert _commits(repo) == 0
