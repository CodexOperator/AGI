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
        g, seat="aa", generation=2, session_id="sid", window="w", pid=1,
        rekey=True)
    assert "authority: OK" in out, out
    _git(repo, "fetch", "-q", "origin", "season2/main")
    rows, _sha, _ref = send._pushed_seats(g, "origin/season2/main", True)
    assert next(r for r in rows if r["name"] == "aa")["pubkey"] == _NEW


# ---------------------------------------------------------------------------
# EF.51 (experiment:a00-1838a1cd-bf0d92) — the four conjuncts the parent
# ordered BUILT on the pre-fix bytes:
#   C1 publish fires only on a real re-key (not every spawn-row commit)
#   C2 publish refuses by name while a RUNG 3 prime veto is frozen
#   C3 the pending successor-key swap waits for the AUTHORITY publish
#   C4 a first seating publishes its NEW row (or refuses by name)
# ---------------------------------------------------------------------------


def _fixture_no_seat(tmp_path, seat="aa"):
    """A bare origin + repo whose authority carries only `bb` -- the seat
    `aa` has NO row on the authority (a FIRST seating)."""
    repo = tmp_path / "repo"
    g = repo / ".agi"
    (g / "nodes" / ".geometry").mkdir(parents=True)
    (g / "config.json").write_text("{}", encoding="utf-8")
    posts = g / "nodes" / ".geometry" / "posts.md"
    rows = [{"name": "bb", "role": "kid", "pubkey": "c" * 64}]
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
    return repo, g, posts, bare


def _freeze_prime(g):
    """Write an ACTIVE (unanswered) prime-scope gate into the tmp graph's
    vetoes.md through the engine's own writer (never the real tree)."""
    from seatsig import veto as _veto
    geom = _veto.read(g)
    geom["active_gates"] = [{
        "scope": "prime", "since": "2026-09-23T00:00:00Z",
        "reason": "council+Keep veto", "veto_ref": "veto:001",
        "answered": "",
    }]
    _veto.save(g, geom)
    assert _veto.is_frozen(g, "prime")[0]


def test_c1_publish_fires_only_on_a_rekey(tmp_path):
    """C1: a plain spawn-row commit (rekey=False) leaves the authority ref
    untouched; a re-key commit (rekey=True) advances it by exactly one."""
    repo, g, posts, _bare = _fixture(tmp_path)
    pre = _git(repo, "rev-parse", "origin/season2/main").stdout.strip()
    # a plain row commit: no mint -> NO authority line, NO authority move.
    text = posts.read_text()
    posts.write_text(text.replace('"generation": 2', '"generation": 3')
                     if '"generation": 2' in text else
                     text.replace(f'"pubkey": "{_NEW}"',
                                  f'"pubkey": "{_NEW}", "generation": 3'))
    out = rotate._commit_spawn_row(
        g, seat="aa", generation=3, session_id="sid", window="w", pid=1,
        rekey=False)
    assert "authority" not in out, out
    _git(repo, "fetch", "-q", "origin", "season2/main")
    assert _git(repo, "rev-parse",
                "origin/season2/main").stdout.strip() == pre, \
        "a non-rekey spawn-row commit must not touch the authority ref"
    # a real re-key: the authority advances by exactly one commit. The
    # re-mint is only in the WORKING tree (uncommitted), as a rotate would
    # leave it.
    posts.write_text(posts.read_text().replace(
        f'"pubkey": "{_NEW}"', f'"pubkey": "{"d" * 64}"'))
    out2 = rotate._commit_spawn_row(
        g, seat="aa", generation=4, session_id="sid", window="w", pid=1,
        rekey=True)
    assert "authority: OK" in out2, out2
    _git(repo, "fetch", "-q", "origin", "season2/main")
    post = _git(repo, "rev-parse", "origin/season2/main").stdout.strip()
    assert _git(repo, "rev-list", "--count",
                f"{pre}..{post}").stdout.strip() == "1"


def test_c2_publish_refuses_while_prime_scope_is_frozen(tmp_path):
    """C2: a frozen RUNG 3 prime gate REFUSES the publish by name (HELD) and
    origin/season2/main does not move."""
    repo, g, posts, _bare = _fixture(tmp_path)
    _freeze_prime(g)
    pre = _git(repo, "rev-parse", "origin/season2/main").stdout.strip()
    out = rotate._publish_row_to_authority(g, "aa", posts.read_text())
    assert out.startswith("authority: HELD"), out
    assert "FROZEN" in out or "gate" in out, out
    _git(repo, "fetch", "-q", "origin", "season2/main")
    assert _git(repo, "rev-parse",
                "origin/season2/main").stdout.strip() == pre


def test_c3_swap_defers_unless_the_authority_publish_succeeded(tmp_path):
    """C3: `_apply_successor_key_gated` completes the deferred swap ONLY when
    the commit carries an `authority: OK` leg; an `authority: FAILED` refusal
    defers it and the seat key file stays byte-identical."""
    import json as _json
    from agi.bin import send as bin_send
    key_path = tmp_path / "seats" / "aa.key"
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(_json.dumps({"scheme": "ed25519",
                                     "priv_hex": "11" * 32}))
    before = key_path.read_bytes()
    kr = {"pending_key": {"path": str(key_path), "scheme": "ed25519",
                          "priv_hex": "22" * 32}}
    # authority FAILED -> defer, key byte-identical, named line.
    r = rotate._apply_successor_key_gated(
        kr, "config:seats row aa: ...",
        "spawn_row_commit: committed (sha abc)\npush: push: OK -- trunk\n"
        "authority: FAILED -- remote refused")
    assert "NOT applied" in r or "deferred" in r, r
    assert key_path.read_bytes() == before, "authority failure must not flip"
    # a HELD refusal defers too (a non-origin SKIP is likewise not OK).
    r2 = rotate._apply_successor_key_gated(
        kr, "config:seats row aa: ...",
        "spawn_row_commit: committed (sha abc)\npush: push: OK -- trunk\n"
        "authority: HELD -- prime FROZEN")
    assert "NOT applied" in r2 or "deferred" in r2, r2
    assert key_path.read_bytes() == before
    # authority OK -> the swap completes and the key flips.
    r3 = rotate._apply_successor_key_gated(
        kr, "config:seats row aa: ...",
        "spawn_row_commit: committed (sha abc)\npush: push: OK -- trunk\n"
        "authority: OK -- abc -> season2/main")
    assert "key_replace: wrote" in r3, r3
    assert key_path.read_bytes() != before
    assert _json.loads(key_path.read_text())["priv_hex"] == "22" * 32


def test_c3_persisted_swap_defers_when_the_authority_leg_fails(tmp_path):
    """C3 (persisted half): a real `_commit_spawn_row` whose authority leg is
    HELD (a frozen prime gate) defers the pending `<seat>.key.pending` swap
    even though the trunk push succeeded -- the key file stays identical."""
    import json as _json
    from agi.bin import send as bin_send
    repo, g, posts, _bare = _fixture(tmp_path)
    seat_key = bin_send._seat_key_path(g, "aa")
    seat_key.parent.mkdir(parents=True, exist_ok=True)
    seat_key.write_text(_json.dumps({"scheme": "ed25519",
                                     "priv_hex": "11" * 32}))
    _json.dump({"scheme": "ed25519", "priv_hex": "22" * 32,
                "pub_hex": send.seatsig.get("ed25519").public_from_secret(
                    bytes.fromhex("22" * 32)).hex(),
                "gen_after": 5, "minted_at": ""},
               open(str(seat_key) + ".pending", "w"))
    before = seat_key.read_bytes()
    _freeze_prime(g)
    text = posts.read_text()
    posts.write_text(text.replace(f'"pubkey": "{_NEW}"',
                                  f'"pubkey": "{_NEW}", "generation": 5'))
    out = rotate._commit_spawn_row(
        g, seat="aa", generation=5, session_id="sid", window="w", pid=1,
        rekey=True)
    assert "authority: HELD" in out, out
    assert seat_key.read_bytes() == before, \
        "a HELD authority must defer the persisted swap"
    assert (seat_key.parent / (seat_key.name + ".pending")).is_file()


def test_c4_first_seating_appends_its_new_row(tmp_path):
    """C4: a seat ABSENT from the authority publishes its NEW row (append),
    never the silent `SKIPPED -- no ... row to replace`; every foreign row
    stays byte-identical."""
    repo, g, posts, _bare = _fixture_no_seat(tmp_path)
    rows = [{"name": "bb", "role": "kid", "pubkey": "c" * 64},
            {"name": "aa", "role": "parent", "pubkey": _NEW}]
    pre = _git(repo, "rev-parse", "origin/season2/main").stdout.strip()
    old_bytes = _git(repo, "show",
                     f"{pre}:.agi/nodes/.geometry/posts.md").stdout
    out = rotate._publish_row_to_authority(g, "aa", _posts_text(rows))
    assert out.startswith("authority: OK"), out
    assert "SKIPPED" not in out, out
    _git(repo, "fetch", "-q", "origin", "season2/main")
    post = _git(repo, "rev-parse", "origin/season2/main").stdout.strip()
    assert _git(repo, "rev-list", "--count",
                f"{pre}..{post}").stdout.strip() == "1"
    new_bytes = _git(repo, "show",
                     "origin/season2/main:.agi/nodes/.geometry/posts.md").stdout
    assert '"name": "aa"' in new_bytes and _NEW in new_bytes
    for name in ("bb",):
        assert [ln for ln in old_bytes.splitlines()
                if f'"name": "{name}"' in ln] == \
               [ln for ln in new_bytes.splitlines()
                if f'"name": "{name}"' in ln]
    # C4 parse-back: the engine's OWN reader must see the seated row. A raw
    # `"name": "aa"` in the file is not enough -- the parent probe showed an
    # append after the closing `---` satisfies that and is still unreadable.
    rows_back, sha_back, ref_back = send._pushed_seats(
        g, "origin/season2/main", True)
    seated = next((r for r in rows_back if r.get("name") == "aa"), None)
    assert seated is not None and seated["pubkey"] == _NEW, rows_back
    assert sha_back and ref_back == "origin/season2/main"
    # C4 refusal: new content with NO `aa` row must refuse BY NAME -- never
    # SKIPPED -- and leave the authority ref exactly where it was.
    repo2, g2, _posts2, _bare2 = _fixture_no_seat(tmp_path / "refuse")
    pre2 = _git(repo2, "rev-parse", "origin/season2/main").stdout.strip()
    out2 = rotate._publish_row_to_authority(g2, "aa", _posts_text(
        [{"name": "bb", "role": "kid", "pubkey": "c" * 64}]))
    assert out2.startswith("authority: REFUSED"), out2
    assert "'aa'" in out2 and "SKIPPED" not in out2, out2
    assert _git(repo2, "rev-parse",
                "origin/season2/main").stdout.strip() == pre2
