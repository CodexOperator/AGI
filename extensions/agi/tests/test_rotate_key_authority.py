"""hypothesis:rotation-publishes-a-reminted-seat-key-to-the-key-authority --
conjunct 2 (route B): a re-key publishes its ONE seat row to the key authority
ref as a one-row commit + fast-forward push, so the successor's first dm
verifies. Real tmp bare repo only; never the real origin.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402
from agi.bin import send  # noqa: E402

_OLD = "a" * 64
_NEW = "b" * 64


def _git(repo, *args, check=True, **kw):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=check, **kw)


def _posts_text(rows):
    body = "---\nid: config:posts\ntype: config\nposts:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    return body


def _fixture(tmp_path):
    """A bare origin + a repo; origin/season2/main carries the OLD `aa` row,
    the checked-out `trunk` carries the NEW one (a re-key)."""
    repo = tmp_path / "repo"
    g = repo / ".agi"
    (g / "nodes" / ".geometry").mkdir(parents=True)
    (g / "config.json").write_text("{}", encoding="utf-8")
    posts = g / "nodes" / ".geometry" / "posts.md"
    rows = [{"name": "aa", "role": "parent", "pubkey": _OLD},
            {"name": "bb", "role": "kid", "pubkey": "c" * 64}]
    posts.write_text(_posts_text(rows), encoding="utf-8")
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    subprocess.run(["git", "-C", str(repo), "init", "-q", "-b", "trunk"],
                   check=True)
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    _git(repo, "remote", "add", "origin", str(bare))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "authority seed")
    _git(repo, "push", "-q", "origin", "HEAD:refs/heads/season2/main")
    _git(repo, "push", "-q", "-u", "origin", "trunk")
    # the re-key lands on the trunk only
    rows[0] = dict(rows[0], pubkey=_NEW)
    posts.write_text(_posts_text(rows), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "re-key on trunk")
    _git(repo, "push", "-q", "origin", "trunk")
    return repo, g, posts, bare


def _advance_authority(repo, branch, rel, text):
    """ONE commit on top of the CURRENT origin/<branch>, pushed -- the non-ff
    race the helper must survive."""
    _git(repo, "fetch", "-q", "origin", branch)
    fd, idx = tempfile.mkstemp()
    os.close(fd)
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    try:
        def run(*a, **kw):
            return subprocess.run(["git", "-C", str(repo), *a], env=env,
                                  capture_output=True, text=True, **kw)
        run("read-tree", "FETCH_HEAD")
        blob = run("hash-object", "-w", "--stdin", input=text).stdout.strip()
        run("update-index", "--add", "--cacheinfo", f"100644,{blob},{rel}")
        tree = run("write-tree").stdout.strip()
        sha = run("commit-tree", tree, "-p", "FETCH_HEAD",
                  "-m", "race").stdout.strip()
        _git(repo, "push", "-q", "origin", f"{sha}:refs/heads/{branch}")
    finally:
        os.unlink(idx)


def test_authority_row_content_replaces_only_the_seat_row():
    base = ('-  {"name": "aa", "pubkey": "old"}\n'
            '-  {"name": "bb", "pubkey": "keep"}\n')
    new = ('-  {"name": "aa", "pubkey": "new"}\n'
           '-  {"name": "bb", "pubkey": "keep"}\n')
    assert rotate._authority_row_content(base, new, "aa") == (
        '-  {"name": "aa", "pubkey": "new"}\n'
        '-  {"name": "bb", "pubkey": "keep"}\n')
    # FIRST seating: no `aa` row in base -> base byte-unchanged.
    first = '-  {"name": "bb", "pubkey": "keep"}\n'
    assert rotate._authority_row_content(first, new, "aa") == first


def test_publish_lands_one_row_on_the_authority_and_whois_reads_it(tmp_path):
    repo, g, posts, _bare = _fixture(tmp_path)
    pre = _git(repo, "rev-parse", "origin/season2/main").stdout.strip()
    out = rotate._publish_row_to_authority(g, "aa", posts.read_text())
    assert out.startswith("authority: OK"), out
    _git(repo, "fetch", "-q", "origin", "season2/main")
    post = _git(repo, "rev-parse", "origin/season2/main").stdout.strip()
    assert post != pre
    assert _git(repo, "rev-list", "--count",
                f"{pre}..{post}").stdout.strip() == "1"
    old_bytes = _git(repo, "show",
                     f"{pre}:.agi/nodes/.geometry/posts.md").stdout
    new_bytes = _git(repo, "show",
                     "origin/season2/main:.agi/nodes/.geometry/posts.md").stdout
    assert _NEW in new_bytes and _OLD not in new_bytes
    # EVERY foreign row is byte-identical; exactly ONE line changed.
    for name in ("bb",):
        assert [ln for ln in old_bytes.splitlines()
                if f'"name": "{name}"' in ln] == \
               [ln for ln in new_bytes.splitlines()
                if f'"name": "{name}"' in ln]
    diff = _git(repo, "diff", pre, post, "--",
                ".agi/nodes/.geometry/posts.md").stdout
    adds = [ln for ln in diff.splitlines()
            if ln.startswith("+") and not ln.startswith("+++")]
    dels = [ln for ln in diff.splitlines()
            if ln.startswith("-") and not ln.startswith("---")]
    assert len(adds) == 1 and len(dels) == 1, diff
    # the authority ref itself now answers with the re-minted pubkey.
    rows, sha, ref = send._pushed_seats(g, "origin/season2/main", True)
    assert next(r for r in rows if r["name"] == "aa")["pubkey"] == _NEW
    assert sha and ref == "origin/season2/main"


def test_publish_refetches_and_recomposes_on_a_non_ff_race(tmp_path,
                                                           monkeypatch):
    repo, g, posts, bare = _fixture(tmp_path)
    real = rotate._blob_text
    state = {"moved": 0}

    def wrapper(top, rev):
        out = real(top, rev)
        if rev.startswith("FETCH_HEAD:") and state["moved"] == 0:
            state["moved"] = 1
            _advance_authority(repo, "season2/main",
                               ".agi/nodes/.geometry/notes.txt", "race\n")
        return out

    monkeypatch.setattr(rotate, "_blob_text", wrapper)
    out = rotate._publish_row_to_authority(g, "aa", posts.read_text())
    assert state["moved"] == 1
    assert out.startswith("authority: OK"), out
    _git(repo, "fetch", "-q", "origin", "season2/main")
    show = _git(repo, "show",
                "origin/season2/main:.agi/nodes/.geometry/posts.md").stdout
    assert _NEW in show and _OLD not in show
    race = _git(repo, "show",
                "origin/season2/main:.agi/nodes/.geometry/notes.txt",
                check=False)
    assert race.returncode == 0 and race.stdout == "race\n"  # race survived


def test_commit_spawn_row_publishes_to_authority_end_to_end(tmp_path):
    """The call site: a rotation's own-row commit reaches the authority."""
    repo, g, posts, _bare = _fixture(tmp_path)
    # the spawn write: an identity cell moves in the working tree (the row the
    # rotation is about to commit), so HEAD differs from the written row.
    text = posts.read_text()
    posts.write_text(text.replace(f'"pubkey": "{_NEW}"',
                                  f'"pubkey": "{_NEW}", "generation": 2'))
    out = rotate._commit_spawn_row(
        g, seat="aa", generation=2, session_id="sid", window="w", pid=1)
    assert "authority: OK" in out, out
    _git(repo, "fetch", "-q", "origin", "season2/main")
    rows, _sha, _ref = send._pushed_seats(g, "origin/season2/main", True)
    assert next(r for r in rows if r["name"] == "aa")["pubkey"] == _NEW
