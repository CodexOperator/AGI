"""Fixture proof for `cli.py post-rename` (hypothesis:l4-a-seat-is-a-post-
everywhere, kid 3 — the migration script). Builds a THROWAWAY git repo in
pytest tmp_path (never the live tree) with a MAIN checkout, two linked
worktrees, a `seats.md` geometry config whose rows carry `seat-<name>`
worktree cells, and `seat/<name>@s2` branches. Every git call runs with
cwd=<tmp> or `--root <tmp>`.

Asserts:
  * `--dry-run` exits 0 and changes NOTHING (git status clean, seats.md still
    present, branches unchanged).
  * `--apply` renames IN ORDER: posts.md exists and seats.md gone (via git),
    mint_id BYTE-IDENTICAL, frontmatter id == config:posts, list key `posts:`,
    worktree cells seat-a/b -> post-a/b, worktree DIRECTORIES moved, local
    branches renamed (old remote ref deleted when a remote fixture is used).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
CLI = BIN / "cli.py"

# Byte-stable stamps the tests anchor on.
MINT_A = "a" * 32
MINT_B = "b" * 32


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    """Run git inside `repo` (the checkout top). The ONLY git a test may run --
    always cwd-bound to the tmp fixture."""
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)


def _row(name: str, *cells: str) -> str:
    d = {"name": name, "role": "kid", "tier": 0, "harness": "pi",
         "worktree": f".agi/worktrees/seat-{name}"}
    for k, v in cells:
        d[k] = v
    return "  - " + json.dumps(d, sort_keys=True)


def _seats_md(body_anchor: str = "body") -> str:
    return (
        f"---\nid: config:seats\nmint_id: {MINT_A}\ntype: config\n"
        f"seats:\n" + _row("a") + "\n" + _row("b") + "\n" + "---\n"
        f"\n# {body_anchor}\n"
    )


def _build_repo(tmp_path):
    """A real git repo: main checkout with the geometry config, two linked
    worktrees, and the `seat/<name>@s2` branches. All git inside this tmp."""
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@t")
    _git(r, "config", "user.name", "t")

    g = r / ".agi" / "nodes" / ".geometry"
    g.mkdir(parents=True)
    (g / "seats.md").write_text(_seats_md())
    (r / "README").write_text("hi\n")
    (r / ".gitignore").write_text(".agi/worktrees/\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "seed")

    for name in ("a", "b"):
        _git(r, "worktree", "add", "-q", "-b", f"seat/{name}@s2",
             f".agi/worktrees/seat-{name}", "master")

    _git(r, "checkout", "-q", "master")
    return r


@pytest.fixture()
def repo(tmp_path):
    return _build_repo(tmp_path)


def _run_cli(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CLI), "post-rename", "--root",
                           str(root), *args], capture_output=True, text=True)


def test_dry_run_changes_nothing(tmp_path):
    """--dry-run prints every step, exits 0, and leaves the repo byte-same:
    git status clean, seats.md still present, both branches unchanged, and no
    posts.md."""
    r = _build_repo(tmp_path)
    g = r / ".agi"

    RESULT = _run_cli(g, "--dry-run")
    assert RESULT.returncode == 0, RESULT.stderr
    out = RESULT.stdout
    for token in ("git mv", "git worktree move", "git branch -m",
                  "git push origin --delete", "fetch"):
        assert token in out, f"dry-run must print a {token!r} step\n{out}"
    assert "nothing changed" in out, out

    # NOTHING changed: clean status, seats.md still there, no posts.md, branches intact.
    status = _git(r, "status", "--porcelain")
    assert status.stdout.strip() == "", f"dry-run dirtied the repo:\n{status.stdout}"
    assert (g / "nodes" / ".geometry" / "seats.md").exists()
    assert not (g / "nodes" / ".geometry" / "posts.md").exists()
    assert (r / ".agi" / "worktrees" / "seat-a").is_dir()
    assert (r / ".agi" / "worktrees" / "post-a").is_dir() is False
    for name in ("a", "b"):
        br = _git(r, "branch", "--list", f"seat/{name}@s2")
        assert br.stdout.strip() != ""


def test_apply_renames_in_order_with_mint_id_intact(repo):
    """--apply performs the full rename: posts.md replaces seats.md, the id
    and list key flip, mint_id stays BYTE-IDENTICAL, worktree cells spell
    post-<name>, the worktree DIRECTORIES move, and the local branches are
    renamed to post/<name>@s2."""
    g = repo / ".agi"
    original_seats = (g / "nodes" / ".geometry" / "seats.md").read_text()

    RESULT = _run_cli(g, "--apply")
    assert RESULT.returncode == 0, RESULT.stdout + RESULT.stderr
    assert "rename applied" in RESULT.stdout, RESULT.stdout

    # seats.md GONE via git, posts.md present via git
    ls = _git(repo, "ls-files", ".agi/nodes/.geometry/")
    assert "posts.md" in ls.stdout
    assert "seats.md" not in ls.stdout
    assert not (g / "nodes" / ".geometry" / "seats.md").exists()
    posts = (g / "nodes" / ".geometry" / "posts.md").read_text()
    assert "id: config:posts" in posts
    assert "seats:" not in posts.split("---")[1]
    assert "posts:" in posts.split("---")[1]

    # mint_id BYTE-IDENTICAL
    assert "mint_id: " + MINT_A in posts

    # worktree cell spelling flipped
    assert '"worktree": ".agi/worktrees/post-a"' in posts
    assert '"worktree": ".agi/worktrees/post-b"' in posts
    assert "seat-a\"" not in posts.split("---")[1]
    # every row value but the worktree cell is untouched (name/role/harness/pin)
    assert '"name": "a"' in posts and '"role": "kid"' in posts

    # worktree DIRECTORIES moved
    assert (g / "worktrees" / "post-a").is_dir()
    assert (g / "worktrees" / "post-b").is_dir()
    assert not (g / "worktrees" / "seat-a").exists()
    assert not (g / "worktrees" / "seat-b").exists()

    # local branches renamed
    for name in ("a", "b"):
        assert _git(repo, "branch", "--list", f"post/{name}@s2").stdout.strip() != ""
        assert _git(repo, "branch", "--list", f"seat/{name}@s2").stdout.strip() == ""


def test_apply_mint_id_byte_identical_to_before(repo):
    """The mint_id in the renamed file is the EXACT same bytes as the source —
    not merely present, but unchanged (hypothesis clause 3: never edit mint_id)."""
    g = repo / ".agi"
    before = (g / "nodes" / ".geometry" / "seats.md").read_text()
    _run_cli(g, "--apply")
    after = (g / "nodes" / ".geometry" / "posts.md").read_text()
    src_line = next(l for l in before.splitlines() if l.startswith("mint_id:"))
    dst_line = next(l for l in after.splitlines() if l.startswith("mint_id:"))
    assert src_line == dst_line


def test_apply_worktree_directories_moved(repo):
    """The seat-<name> worktree top dirs are gone and post-<name> hold a valid
    worktree (registered, with the renamed HEAD) -- the directory rename really
    moved the linked worktrees."""
    g = repo / ".agi"
    _run_cli(g, "--apply")
    mv = _git(repo, "worktree", "list", "--porcelain")
    assert ".agi/worktrees/post-a" in mv.stdout.replace("\t", "")
    assert ".agi/worktrees/post-b" in mv.stdout.replace("\t", "")
    assert "seat-a" not in mv.stdout.replace("\t", "").replace("post-", "")


def test_apply_remote_ref_deleted_when_remote_present(repo):
    """With a bare `origin` remote, --apply pushes post/<name>@s2 and deletes
    the old seat/<name>@s2 LAST (git push origin --delete)."""
    # a bare remote in tmp to receive pushes
    bare = repo.parent / "bare.git"
    _git(repo, "init", "--bare", "-q", str(bare))
    _git(repo, "remote", "add", "origin", str(bare))
    _git(repo, "push", "-q", "origin", "master")
    for name in ("a", "b"):
        _git(repo, "push", "-q", "origin", f"seat/{name}@s2")

    g = repo / ".agi"
    RESULT = _run_cli(g, "--apply")
    assert RESULT.returncode == 0, RESULT.stdout + RESULT.stderr

    for name in ("a", "b"):
        # old remote ref deleted
        has_old = _git(repo, "ls-remote", "origin",
                       f"refs/heads/seat/{name}@s2").stdout.strip()
        has_new = _git(repo, "ls-remote", "origin",
                       f"refs/heads/post/{name}@s2").stdout.strip()
        assert has_old == "", f"old remote seat/{name}@s2 not deleted: {has_old}"
        assert has_new != "", f"new remote post/{name}@s2 not pushed"

# ---------------------------------------------------------------------------
# hypothesis:l4-a-seat-is-a-post-everywhere — L4.300 WRITE-PATH FIX-ONLY.
# A migrated (posts.md) tree must not refuse its own acks. These build the
# post-migration fixture by ACTUALLY running `post-rename --apply` on a
# throwaway repo, then prove the residues (a-c) live on the migrated bytes —
# plus the pre-migration (seats.md) path still resolves and works.
# ---------------------------------------------------------------------------

def _config_schema(repo: Path) -> None:
    """A `[config].md` schema whose self_row declares `list_key: seats` (the
    one-season alias spelling, left as-is by (c1)). With (c1) the write guard
    resolves the list key POST-FIRST from geometry_config, so this same schema
    admits both the pre-migration seats layout and the migrated posts layout."""
    schemas = repo / ".agi" / "context" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, "
        "fields: [session_ref, session_id, generation, window, pid]}\n"
        "---\nbody\n", encoding="utf-8")


def _config_json(repo: Path) -> None:
    """A minimal `.agi/config.json` marker so the write API's descend-only
    root resolver (`_resolve_api_root`) recognises the graph root (the
    post_rename `_build_repo` fixture deliberately carries none)."""
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')


def _migrate(tmp_path):
    """Build a seat-layout repo, ACTUALLY run `post-rename --apply`, add the
    schema, and commit the migrated state so a pushed-ref reader can resolve
    posts.md at HEAD. Returns (repo_top, .agi_graph_root)."""
    r = _build_repo(tmp_path)
    _config_schema(r)
    _config_json(r)
    g = r / ".agi"
    RESULT = _run_cli(g, "--apply")
    assert RESULT.returncode == 0, RESULT.stdout + RESULT.stderr
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "post-migrate")
    return r, g


def test_pre_migration_write_path_still_resolves_seats(tmp_path):
    """(pre) On a PRE-migration (seats.md only) repo the write path still
    resolves `seats`: `_write_identity_cells` lands config:seats/seats.md,
    write's self_row guard admits an own-row seats write through submit, and
    `--dry-run` leaves the seats.md line count unchanged."""
    import node_writer  # noqa: PLC0415
    import rotate  # noqa: PLC0415
    import write  # noqa: PLC0415
    r = _build_repo(tmp_path)
    _config_schema(r)
    _config_json(r)
    g = r / ".agi"
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "seed-schema")

    seats_md = g / "nodes" / ".geometry" / "seats.md"
    before_lines = seats_md.read_text().count("\n")
    DRY = _run_cli(g, "--dry-run")
    assert DRY.returncode == 0, DRY.stdout + DRY.stderr
    assert seats_md.exists() and not (g / "nodes" / ".geometry" / "posts.md").exists()
    assert seats_md.read_text().count("\n") == before_lines, (
        "dry-run must not change the seats.md line count")

    # (a) _write_identity_cells resolves config:seats / seats on pre-migration.
    out = rotate._write_identity_cells(
        g, seat="a", actor="a", role="kid",
        cells={"session_ref": "ref-pre", "generation": 7})
    assert out == "wrote identity cells for seat 'a' into MAIN seats.md"
    row = next(x for x in write._load_seats(g) if x.get("name") == "a")
    assert row["session_ref"] == "ref-pre" and row["generation"] == 7
    assert "id: config:seats" in seats_md.read_text()

    # (c1) write's self_row guard still admits an OWN-row seats write.
    old = write._load_seats(g)
    nr = []
    for x in old:
        nx = dict(x)
        if nx.get("name") == "a":
            nx["pid"] = 55
        nr.append(nx)
    res = write.submit(g, write.Edit(node_id="config:seats",
                                     set_fm={"seats": nr}),
                       actor="a", role="kid")
    assert res.status == node_writer.UPDATED, res.reason

    # (b) send._pushed_seats resolves the pushed rows from the seats.md
    # fallback path of the post-first list reader (posts.md absent here).
    import send  # noqa: PLC0415
    rows, sha = send._pushed_seats(r, "HEAD", do_fetch=False)
    names = [x.get("name") for x in rows]
    assert "a" in names and "b" in names, names
    assert sha
    # posts.md does not exist at HEAD, so the seats path is the authority.
    has_post = subprocess.run(
        ["git", "cat-file", "-e", "HEAD:.agi/nodes/.geometry/posts.md"],
        cwd=r, capture_output=True).returncode
    assert has_post != 0


def test_post_migrated_ack_shaped_self_row_write_and_foreign_refused(tmp_path):
    """(c1) On a MIGRATED (posts.md only) tree the WRITE path no longer
    refuses its own acks: an ack-shaped `Edit(node_id="config:posts")` with
    `set_fm["posts"]` and one own-row identity cell changed SUCCEEDS through
    `write.submit`; a FOREIGN-row write is still refused. (a)
    `_write_identity_cells` wrote through config:posts/posts (the changed cell
    reads back from posts.md). (b) `send._pushed_seats` resolves the pushed
    rows from posts.md."""
    import node_writer  # noqa: PLC0415
    import rotate  # noqa: PLC0415
    import send  # noqa: PLC0415
    import write  # noqa: PLC0415
    r, g = _migrate(tmp_path)
    posts_md = g / "nodes" / ".geometry" / "posts.md"

    # (c1) ACK-SHAPED own-row write SUCCEEDS through write.submit.
    old = write._load_seats(g)
    nr = []
    for x in old:
        nx = dict(x)
        if nx.get("name") == "a":
            nx["pid"] = 1234        # ONE own-row identity cell changed
        nr.append(nx)
    res = write.submit(g, write.Edit(node_id="config:posts",
                                     set_fm={"posts": nr}),
                       actor="a", role="kid")
    assert res.status == node_writer.UPDATED, res.reason
    # (a) written through config:posts / posts.md — readable back.
    book = posts_md.read_text()
    assert "id: config:posts" in book and "posts:" in book.split("---")[1]
    assert '"name": "a"' in book and '"pid": 1234' in book
    assert not (g / "nodes" / ".geometry" / "seats.md").exists()

    # FOREIGN-row write still refused (the c1 guard is intact on posts layout).
    foreign = []
    for x in old:
        nx = dict(x)
        if nx.get("name") == "b":
            nx["pid"] = 777         # b is NOT actor a's own row
        foreign.append(nx)
    with pytest.raises(write.EditError, match="own row"):
        write.submit(g, write.Edit(node_id="config:posts",
                                   set_fm={"posts": foreign}),
                     actor="a", role="kid")

    # (a) _write_identity_cells on the migrated tree resolves config:posts.
    out = rotate._write_identity_cells(
        g, seat="a", actor="a", role="kid",
        cells={"session_ref": "ref-post", "generation": 9})
    assert out == "wrote identity cells for seat 'a' into MAIN posts.md"
    row = next(x for x in write._load_seats(g) if x.get("name") == "a")
    assert row["session_ref"] == "ref-post" and row["generation"] == 9

    # (b) send._pushed_seats resolves the pushed rows from posts.md.
    rows, sha = send._pushed_seats(r, "HEAD", do_fetch=False)
    names = [x.get("name") for x in rows]
    assert "a" in names and "b" in names, names
    # posts.md is the authority; seats.md is gone from the tree entirely.
    gone = subprocess.run(
        ["git", "cat-file", "-e", "HEAD:.agi/nodes/.geometry/seats.md"],
        cwd=r, capture_output=True).returncode
    assert gone != 0
