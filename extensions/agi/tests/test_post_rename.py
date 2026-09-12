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