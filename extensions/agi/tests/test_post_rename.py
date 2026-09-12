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
    (r / ".gitignore").write_text(".agi/worktrees/\n.agi/sessions/\n")
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
                  "--delete-old", "fetch"):
        assert token in out, f"dry-run must print a {token!r} step\n{out}"
    assert "remote delete is NOT implied by --apply" in out, out
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


def test_apply_remote_ref_survives_when_remote_present(repo):
    """With a bare `origin` remote, --apply pushes post/<name>@s2 but NEVER
    deletes the old seat/<name>@s2 — the remote delete is the separate
    --delete-old step (hypothesis:l4-post-rename-apply-re-points-every-
    upstream-and-deletes-nothing), so after --apply origin still holds
    seat/<name>@s2."""
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
        # old remote ref SURVIVES --apply (the L4.316 fix: --apply deletes nothing)
        has_old = _git(repo, "ls-remote", "origin",
                       f"refs/heads/seat/{name}@s2").stdout.strip()
        has_new = _git(repo, "ls-remote", "origin",
                       f"refs/heads/post/{name}@s2").stdout.strip()
        assert has_old != "", f"--apply deleted old remote seat/{name}@s2"
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
    rows, sha, _ref = send._pushed_seats(r, "HEAD", do_fetch=False)
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
    rows, sha, _ref = send._pushed_seats(r, "HEAD", do_fetch=False)
    names = [x.get("name") for x in rows]
    assert "a" in names and "b" in names, names
    # posts.md is the authority; seats.md is gone from the tree entirely.
    gone = subprocess.run(
        ["git", "cat-file", "-e", "HEAD:.agi/nodes/.geometry/seats.md"],
        cwd=r, capture_output=True).returncode
    assert gone != 0


# ---------------------------------------------------------------------------
# hypothesis:l4-a-seat-is-a-post-everywhere — L4.306 FIX-ONLY. The migration
# must (1) set an upstream after each branch rename, (2) commit + push posts.md
# as its own step so --apply leaves a CLEAN tree, (3) be resumable/idempotent
# so a second --apply is a no-op, (4) still leave a --dry-run byte-identical
# with no plan file written. All against the throwaway fixture, never the tree.
# ---------------------------------------------------------------------------

def _add_origin(repo):
    """A bare origin in tmp to receive pushes, seeded with master + seat refs."""
    bare = repo.parent / "bare.git"
    _git(repo, "init", "--bare", "-q", str(bare))
    _git(repo, "remote", "add", "origin", str(bare))
    _git(repo, "push", "-q", "origin", "master")
    for name in ("a", "b"):
        _git(repo, "push", "-q", "origin", f"seat/{name}@s2")
    return bare


def test_apply_sets_upstream_and_commits_posts_clean(repo):
    """(a)+(b) With an origin, --apply: commits posts.md as its own step so
    `git status` for it is clean, pushes the current branch (master, carrying
    the posts.md commit) to origin, and sets each renamed branch's upstream to
    origin/post/<n>@s2."""
    _add_origin(repo)
    g = repo / ".agi"
    RESULT = _run_cli(g, "--apply")
    assert RESULT.returncode == 0, RESULT.stdout + RESULT.stderr

    # (b) posts.md is COMMITTED: clean status for it, and it is at HEAD
    st = _git(repo, "status", "--porcelain",
              "--", ".agi/nodes/.geometry/posts.md")
    assert st.stdout.strip() == "", f"posts.md left dirty:\n{st.stdout}"
    head = _git(repo, "show", "--format=%H", "--name-only", "HEAD")
    assert ".agi/nodes/.geometry/posts.md" in head.stdout
    # the current branch was PUSHED with that commit (local == origin)
    local = _git(repo, "rev-parse", "master").stdout.strip()
    remote = _git(repo, "rev-parse", "origin/master").stdout.strip()
    assert local and local == remote, f"master not pushed: {local} != {remote}"

    # (a) upstream set on each renamed branch
    for name in ("a", "b"):
        up = _git(repo, "rev-parse", "--abbrev-ref",
                  f"post/{name}@s2@{{upstream}}").stdout.strip()
        assert up == f"origin/post/{name}@s2", f"upstream for {name}: {up!r}"


def test_apply_second_run_is_idempotent_noop(repo):
    """(c) A second --apply after a full first one is a no-op: still exits 0,
    the tree stays clean, and refs/upstreams are unchanged."""
    _add_origin(repo)
    g = repo / ".agi"
    assert _run_cli(g, "--apply").returncode == 0
    first_status = _git(repo, "status", "--porcelain").stdout
    first_refs = _git(repo, "rev-parse", "master", "post/a@s2").stdout

    R2 = _run_cli(g, "--apply")
    assert R2.returncode == 0, R2.stdout + R2.stderr
    assert "rename applied" in R2.stdout, R2.stdout
    assert _git(repo, "status", "--porcelain").stdout == first_status
    assert _git(repo, "rev-parse", "master", "post/a@s2").stdout == first_refs
    for name in ("a", "b"):
        up = _git(repo, "rev-parse", "--abbrev-ref",
                  f"post/{name}@s2@{{upstream}}").stdout.strip()
        assert up == f"origin/post/{name}@s2"


def test_dry_run_writes_no_plan_file_and_leaves_bytes_same(repo):
    """(d) --dry-run still changes NOTHING (git status clean, no posts.md) and
    writes NO plan file — resumability state only ever appears under --apply."""
    g = repo / ".agi"
    before = _git(repo, "status", "--porcelain").stdout
    R = _run_cli(g, "--dry-run")
    assert R.returncode == 0, R.stdout + R.stderr
    assert not (g / "sessions" / "post-rename-plan.json").exists(), (
        "dry-run must not write the plan file")
    assert _git(repo, "status", "--porcelain").stdout == before
    assert (g / "nodes" / ".geometry" / "seats.md").exists()
    assert not (g / "nodes" / ".geometry" / "posts.md").exists()


def test_apply_records_plan_and_rerun_resumes(repo):
    """(c) Resumability: --apply records every finished step in the plan file,
    and a re-run skips the already-done git mv (posts.md present, seats.md
    gone) — still exits 0 cleanly on a fully-migrated tree."""
    g = repo / ".agi"
    R1 = _run_cli(g, "--apply")          # no origin: pure local migration
    assert R1.returncode == 0, R1.stdout + R1.stderr
    plan = g / "sessions" / "post-rename-plan.json"
    assert plan.exists(), "apply must write the plan file"
    done = json.loads(plan.read_text()).get("steps", {})
    for key in ("git_mv", "commit_posts", "worktree_move",
                "branch_rename", "branch_push", "branch_upstream"):
        assert done.get(key) is True, f"step {key} not recorded done: {done}"

    R2 = _run_cli(g, "--apply")
    assert R2.returncode == 0, R2.stdout + R2.stderr
    # migrated tree: seats.md gone, posts.md committed, worktrees moved
    assert not (g / "nodes" / ".geometry" / "seats.md").exists()
    assert (g / "nodes" / ".geometry" / "posts.md").exists()
    assert (g / "worktrees" / "post-a").is_dir()


# ---------------------------------------------------------------------------
# hypothesis:l4-a-seat-is-a-post-everywhere — L4.315 FIX-ONLY (resumability +
# pathspec). (1) `_post_rename_jobs` now ALSO accepts `post-<name>` cells (the
# spelling step 2 already rewrote to), so a re-run over a HALF-renamed tree
# still derives the jobs and completes steps 4-7 instead of finding nothing to
# do; the step-4 worktree move derives source/target from the NAME so it works
# whether the cell says seat- or post-. (2) step 3 commits BY pathspec ONLY
# (`git commit -m msg -- <paths>`), so another agent's already-staged files are
# never swept in, and prints a real rollback only when a commit was actually
# created (a bare HEAD~1 rollback on a "nothing to commit" skip would destroy
# an unrelated commit).
# ---------------------------------------------------------------------------

def test_apply_pathspec_commit_names_only_the_geometry_file(repo):
    """(2) With a foreign file already STAGED by another agent, --apply's step-3
    commit names ONLY the geometry file — the foreign staged file is left staged
    and uncommitted, so the migration cannot sweep an unrelated index in."""
    g = repo / ".agi"
    foreign = g / "nodes" / "foreign-agent.txt"
    foreign.write_text("someone else's staged work\n")
    rel = str(foreign.relative_to(repo))
    _git(repo, "add", rel)

    R = _run_cli(g, "--apply")
    assert R.returncode == 0, R.stdout + R.stderr

    # the step-3 commit named ONLY the geometry path (the rename)
    names = _git(repo, "show", "--format=", "--name-only", "HEAD").stdout.split()
    assert ".agi/nodes/.geometry/posts.md" in names, names
    assert "foreign-agent.txt" not in names, names

    # and the foreign file is still staged (index has it), not consumed
    st = _git(repo, "status", "--porcelain").stdout
    assert rel.split("/")[-1] in st, f"foreign file vanished from index:\n{st}"
    # no stray seats.md in the commit either (the rename is one clean commit)
    assert not _git(repo, "ls-files", ".agi/nodes/.geometry/seats.md").stdout.strip()


def test_apply_resumes_hand_rewritten_cells_without_plan(repo):
    """(1) A re-run over a tree whose cells ALREADY spell `post-<name>` — one
    where step 2's rewrite already ran, with NO plan file (e.g. the scratch
    plan was lost, or a human hand-rewrote the cells) — still derives the jobs
    and COMPLETES the remaining steps (worktree move + branch renames), instead
    of finding nothing to do. Simulated by migrating seats.md->posts.md BY HAND
    and committing it, leaving the worktree dirs and branches at seat-."""
    g = repo / ".agi"
    seats = g / "nodes" / ".geometry" / "seats.md"
    posts = g / "nodes" / ".geometry" / "posts.md"
    _git(repo, "mv", ".agi/nodes/.geometry/seats.md",
         ".agi/nodes/.geometry/posts.md")
    text = posts.read_text(encoding="utf-8")
    text = text.replace("id: config:seats", "id: config:posts")
    text = text.replace("seats:", "posts:", 1)
    text = text.replace('".agi/worktrees/seat-a"', '".agi/worktrees/post-a"')
    text = text.replace('".agi/worktrees/seat-b"', '".agi/worktrees/post-b"')
    posts.write_text(text, encoding="utf-8")
    _git(repo, "add", ".agi/nodes/.geometry/posts.md")
    _git(repo, "commit", "-qm", "hand post-rename")
    # the worktree DIRS and branches stay at seat-, and there is NO plan file.
    assert (g / "worktrees" / "seat-a").is_dir()
    assert _git(repo, "branch", "--list", "seat/a@s2").stdout.strip() != ""
    assert not (g / "sessions" / "post-rename-plan.json").exists()

    R = _run_cli(g, "--apply")
    assert R.returncode == 0, R.stdout + R.stderr
    # remaining steps completed: worktree dirs moved, branches renamed, clean
    assert (g / "worktrees" / "post-a").is_dir()
    assert (g / "worktrees" / "post-b").is_dir()
    assert not (g / "worktrees" / "seat-a").exists()
    assert _git(repo, "branch", "--list", "post/a@s2").stdout.strip() != ""
    assert _git(repo, "branch", "--list", "seat/a@s2").stdout.strip() == ""
    assert not (g / "nodes" / ".geometry" / "seats.md").exists()
    assert _git(repo, "status", "--porcelain").stdout.strip() == ""


def test_apply_second_run_prints_its_skips_no_duplicate_commit(repo):
    """(1)+(2) On a FINISHED fixture a second --apply is a clean no-op: it
    prints what it SKIPS, leaves the tree byte-clean, and does NOT mint a second
    post-rename commit."""
    _add_origin(repo)
    g = repo / ".agi"
    assert _run_cli(g, "--apply").returncode == 0

    R2 = _run_cli(g, "--apply")
    assert R2.returncode == 0, R2.stdout + R2.stderr
    out = R2.stdout
    assert "skip" in out, f"re-run must print skip markers, not redo work:\n{out}"
    assert "git commit" not in out, out   # commit step fully skipped (no re-commit)
    assert _git(repo, "status", "--porcelain").stdout.strip() == ""
    # exactly ONE post-rename commit ever on master (no duplicate)
    msgs = _git(repo, "log", "--format=%s", "master").stdout.splitlines()
    assert msgs.count("post-rename: seats.md -> posts.md") == 1, msgs


# ---------------------------------------------------------------------------
# hypothesis:l4-post-rename-apply-re-points-every-upstream-and-deletes-nothing
# -- L4.316 FIX-ONLY. (A) --apply re-points the upstream of EVERY renamed
# branch: git branch -m CARRIES the old upstream, so a fixture whose branch
# already tracks origin/seat/<n>@s2 when --apply runs must end at
# origin/post/<n>@s2 (the L4.312-demoted defect). (B) --apply deletes NO old
# remote name (origin/seat/<n>@s2 survives); the delete is the separate
# --delete-old step, which reads the upstream gate green for every renamed
# branch first and refuses by name (deleting NOTHING) otherwise.
# ---------------------------------------------------------------------------

def _add_origin_tracked(repo):
    """A bare origin (master + seat refs) AND each seat branch tracking its
    OLD remote: the pre-seeded variant — the branch ALREADY has upstream
    origin/seat/<name>@s2 when --apply runs, exactly what git branch -m
    would carry forward on the live tree (bare `git push` without -u never
    creates it, which is why the old green test only covered the unset path)."""
    _add_origin(repo)
    for name in ("a", "b"):
        _git(repo, "branch", "--set-upstream-to", f"origin/seat/{name}@s2",
             f"seat/{name}@s2")


def test_apply_repoints_preseeded_upstream(repo):
    """(A) FAILS pre-fix, PASSES post-fix: a branch already carrying
    upstream origin/seat/<n>@s2 when --apply runs must be RE-POINTED to
    origin/post/<n>@s2 — not skipped by a truthy upstream gate."""
    _add_origin_tracked(repo)
    g = repo / ".agi"
    # prove the seeded state: every branch already tracks the OLD name
    for name in ("a", "b"):
        up = _git(repo, "rev-parse", "--abbrev-ref",
                  f"seat/{name}@s2@{{upstream}}").stdout.strip()
        assert up == f"origin/seat/{name}@s2", up

    RESULT = _run_cli(g, "--apply")
    assert RESULT.returncode == 0, RESULT.stdout + RESULT.stderr
    for name in ("a", "b"):
        up = _git(repo, "rev-parse", "--abbrev-ref",
                  f"post/{name}@s2@{{upstream}}").stdout.strip()
        assert up == f"origin/post/{name}@s2", \
            f"upstream for {name} not re-pointed: {up!r}"


def test_apply_preseeded_upstream_second_run_resumes_cleanly(repo):
    """(A)+(4) With the pre-seeded upstream, a SECOND --apply after a full
    first one resumes as a clean no-op: exits 0, prints no commit, still ends
    on the re-pointed upstream (resumability from L4.315 unbroken)."""
    _add_origin_tracked(repo)
    g = repo / ".agi"
    assert _run_cli(g, "--apply").returncode == 0

    R2 = _run_cli(g, "--apply")
    assert R2.returncode == 0, R2.stdout + R2.stderr
    assert "rename applied" in R2.stdout, R2.stdout
    for name in ("a", "b"):
        up = _git(repo, "rev-parse", "--abbrev-ref",
                  f"post/{name}@s2@{{upstream}}").stdout.strip()
        assert up == f"origin/post/{name}@s2", up


def _migrate_with_origin(repo):
    """Run --apply on a repo with a bare origin, so the tree is migrated
    (posts.md, worktrees moved, branches renamed, new name pushed, upstream
    re-pointed) but origin/seat/<name>@s2 still EXISTS (--apply deletes
    nothing)."""
    _add_origin(repo)
    g = repo / ".agi"
    RESULT = _run_cli(g, "--apply")
    assert RESULT.returncode == 0, RESULT.stdout + RESULT.stderr
    return g


def test_delete_old_removes_old_remote_refs_only_after_gate_green(repo):
    """(B-green) --delete-old, on a migrated tree whose renamed branches DO
    read upstream origin/post/<name>@s2, deletes origin/seat/<name>@s2 and
    leaves the new refs + upstreams untouched."""
    g = _migrate_with_origin(repo)
    # the gate is green before the delete: both upstreams read post
    for name in ("a", "b"):
        assert _git(repo, "rev-parse", "--abbrev-ref",
                    f"post/{name}@s2@{{upstream}}").stdout.strip() == \
            f"origin/post/{name}@s2"

    RESULT = _run_cli(g, "--delete-old")
    assert RESULT.returncode == 0, RESULT.stdout + RESULT.stderr
    for name in ("a", "b"):
        has_old = _git(repo, "ls-remote", "origin",
                       f"refs/heads/seat/{name}@s2").stdout.strip()
        assert has_old == "", f"origin/seat/{name}@s2 not deleted:\n{has_old}"
        has_new = _git(repo, "ls-remote", "origin",
                       f"refs/heads/post/{name}@s2").stdout.strip()
        assert has_new != "", f"new remote post/{name}@s2 missing"
        up = _git(repo, "rev-parse", "--abbrev-ref",
                  f"post/{name}@s2@{{upstream}}").stdout.strip()
        assert up == f"origin/post/{name}@s2", up


def test_delete_old_refuses_names_branch_and_deletes_nothing(repo):
    """(B-refuse) --delete-old REFUSES (non-zero, naming the offending
    branch) when a renamed branch's upstream is not origin/post/<name>@s2. B4
    (L4.320): it no longer ABORTS at the first refusal — it deletes what IS
    gated green and lists the refusals, returning non-zero only because some
    were refused."""
    g = _migrate_with_origin(repo)
    # sabotage ONE branch's upstream back to the old name; b stays correct.
    _git(repo, "branch", "--set-upstream-to", "origin/seat/b@s2", "post/b@s2")

    RESULT = _run_cli(g, "--delete-old")
    assert RESULT.returncode != 0, RESULT.stdout + RESULT.stderr
    assert "post/b@s2" in RESULT.stderr, RESULT.stderr
    # the GREEN a was deleted; the un-pointed b was NOT
    has_a = _git(repo, "ls-remote", "origin",
                 "refs/heads/seat/a@s2").stdout.strip()
    assert has_a == "", "origin/seat/a@s2 should have been deleted (it was green)"
    has_b = _git(repo, "ls-remote", "origin",
                 "refs/heads/seat/b@s2").stdout.strip()
    assert has_b != "", "origin/seat/b@s2 must survive (it was refused)"


def test_delete_old_is_resumeable_second_run_exits_zero(repo):
    """(B4-resume) After a first run deleted the green a and refused the
    un-pointed b, a SECOND run (once b is re-pointed) deletes ONLY what
    remains (b) and exits 0. With nothing left, a THIRD run exits 0 too."""
    g = _migrate_with_origin(repo)
    # sabotage b's upstream so the FIRST run refuses it
    _git(repo, "branch", "--set-upstream-to", "origin/seat/b@s2", "post/b@s2")
    R1 = _run_cli(g, "--delete-old")
    assert R1.returncode != 0 and "post/b@s2" in R1.stderr, R1.stderr
    assert _git(repo, "ls-remote", "origin",
                "refs/heads/seat/a@s2").stdout.strip() == ""
    assert _git(repo, "ls-remote", "origin",
                "refs/heads/seat/b@s2").stdout.strip() != ""

    # re-point b onto the new name, then a second run deletes only b
    _git(repo, "branch", "--set-upstream-to", "origin/post/b@s2", "post/b@s2")
    R2 = _run_cli(g, "--delete-old")
    assert R2.returncode == 0, R2.stdout + R2.stderr
    assert _git(repo, "ls-remote", "origin",
                "refs/heads/seat/b@s2").stdout.strip() == ""
    # already-pointed a was skipped (resume), not re-deleted
    assert "origin/seat/a@s2" not in R2.stdout, R2.stdout

    # nothing remains: a THIRD run exits 0 with no deletes
    R3 = _run_cli(g, "--delete-old")
    assert R3.returncode == 0, R3.stdout + R3.stderr


def test_delete_old_dry_run_prints_and_runs_none(repo):
    """(B3) --dry-run --delete-old prints every delete as a `[DRY ]` line,
    runs NONE, needs no green upstream gate, and leaves the remote holding
    every old ref."""
    g = _migrate_with_origin(repo)
    RESULT = _run_cli(g, "--dry-run", "--delete-old")
    assert RESULT.returncode == 0, RESULT.stdout + RESULT.stderr
    assert "dry-run: nothing changed" in RESULT.stdout, RESULT.stdout
    for name in ("a", "b"):
        assert f"[DRY ] branch delete (remote): git push origin --delete " \
               f"seat/{name}@s2" in RESULT.stdout, (name, RESULT.stdout)
        has_old = _git(repo, "ls-remote", "origin",
                       f"refs/heads/seat/{name}@s2").stdout.strip()
        assert has_old != "", f"origin/seat/{name}@s2 was deleted by a dry run"


def test_apply_and_delete_old_are_mutually_exclusive(repo):
    """(--delete-old shape) --apply and --delete-old cannot be combined; the
    refusal names --delete-old as the separate final step."""
    g = repo / ".agi"
    RESULT = _run_cli(g, "--apply", "--delete-old")
    assert RESULT.returncode != 0, RESULT.stdout
    assert "mutually exclusive" in RESULT.stderr and \
        "separate final step" in RESULT.stderr, RESULT.stderr


# ---------------------------------------------------------------------------
# hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-
# true — L4.318 FIX-ONLY, Region A. The --dry-run step-3 pathspec is built by
# the SAME code path --apply uses (the shared `_post_rename_commit_targets`),
# carrying the staged-pending INDEX check, so the dry-run plan names exactly
# the files --apply would commit for the same tree state. Before the fix the
# dry-run HARDCODED `[dest, seats_rel]`; on a tree where the seats.md delete
# was already committed it printed a `git commit -- posts.md seats.md` that
# --apply would never run and that would ERROR verbatim (path not in index).
# Both tests seed the state, capture the dry-run path set from the printed
# step-3 line, run --apply on the same state, and assert plan == apply.
# ---------------------------------------------------------------------------

def _step3_paths(R, mode: str) -> list:
    """The path list a commit-posts.md line names after its `--` pathspec
    separator, for either the `DRY ` (--dry-run) or `APPLY` mode. Strips the
    trailing rollback tail first so its `--soft`/`git mv` tokens are never read
    as paths. The apply branch prints this SAME line with the targets it really
    uses, so comparing dry-run vs apply pathspecs on one state proves the two
    branches agree on what --apply would commit."""
    line = next(
        l for l in R.stdout.splitlines()
        if l.startswith(f"[{mode}] commit posts.md:") and ' -- ' in l)
    body = line.split("  -- rollback:", 1)[0]   # drop rollback tail
    _, _, spec = body.partition(' -- ')
    return sorted(spec.strip().split())


def test_dry_run_names_both_while_seats_delete_pending(repo):
    """(Region A/a) While the seats.md DELETE is still PENDING in the index
    (as the git mv staged it), the --dry-run step-3 pathspec names BOTH
    posts.md and seats.md — and the string --apply prints for the same state
    names exactly those same two paths. Plan and apply agree."""
    g = repo / ".agi"
    seats = g / "nodes" / ".geometry" / "seats.md"
    posts = g / "nodes" / ".geometry" / "posts.md"
    _git(repo, "mv", str(seats.relative_to(repo)),
         str(posts.relative_to(repo)))   # stages: seats delete + posts add

    plan = _step3_paths(_run_cli(g, "--dry-run"), "DRY ")
    names = {p.rsplit("/", 1)[-1] for p in plan}
    assert "seats.md" in names and "posts.md" in names, plan

    R = _run_cli(g, "--apply")
    assert R.returncode == 0, R.stdout + R.stderr
    applied = _step3_paths(R, "APPLY")
    assert plan == applied, (f"dry-run plan {plan} != apply pathspec {applied}")


def test_dry_run_names_only_posts_after_seats_delete_committed(repo):
    """(Region A/b) Once the seats.md DELETE is already COMMITTED (mv + commit
    done), the --dry-run step-3 pathspec names ONLY posts.md — never a stale
    seats.md that would make `git commit -- ... seats.md` ERROR verbatim. With
    a freshly staged posts.md edit, the string --apply prints for the same state
    names exactly posts.md: plan and apply agree."""
    g = repo / ".agi"
    seats = g / "nodes" / ".geometry" / "seats.md"
    posts = g / "nodes" / ".geometry" / "posts.md"
    _git(repo, "mv", str(seats.relative_to(repo)),
         str(posts.relative_to(repo)))
    _git(repo, "commit", "-qm", "seed: seats->posts rename")  # delete committed
    posts.write_text("\n# touched-after-commit\n", encoding="utf-8")
    _git(repo, "add", str(posts.relative_to(repo)))   # something to commit

    plan = _step3_paths(_run_cli(g, "--dry-run"), "DRY ")
    names = {p.rsplit("/", 1)[-1] for p in plan}
    assert "posts.md" in names and "seats.md" not in names, plan

    R = _run_cli(g, "--apply")
    assert R.returncode == 0, R.stdout + R.stderr
    applied = _step3_paths(R, "APPLY")
    assert plan == applied, (f"dry-run plan {plan} != apply pathspec {applied}")
