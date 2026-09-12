"""Fixture proof for `cli.py loop-prune` — prune a v3 town-first loop branch
`<town>/season<m>/posts/<post>/loops/<round>/<agent>` iff it is MERGED into
its post main `<town>/season<m>/posts/<post>/main` (derived through
branches.derive_names from the SAME tuple — never hand-spelled a second
time). hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-
trunk-pair-per-level-reaches-origin.

Builds a THROWAWAY git repo in tmp_path (never the live tree) with a real
BARE origin whose refs/heads cover the rule at once:

  KEEP (remote-visible)     master, season2/main, core/main, core/season2/main
  POST                        core/season2/posts/a/main
  MERGED loop                 core/season2/posts/a/loops/L4.999/ag1
                             (its commit IS an ancestor of the post main)
  UNMERGED loop               core/season2/posts/a/loops/L4.999/ag2
                             (its commit is NOT an ancestor of the post main)

Asserts:
  * `loop-prune --apply` prunes the MERGED loop (local + origin gone) and
    NEVER the unmerged one (asserted both by branch existence and by the
    per-branch "unmerged: ... -> NOT pruned" output line).
  * dry-run (the DEFAULT) prints the plan and changes NOTHING byte-for-byte
    (ref count, worktree list and tree digest identical before/after).
  * the prune never uses --force/-f and never deletes master or any
    remote-visible name (branches.is_remote_visible over the surviving refs).
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
CLI = BIN / "cli.py"

KEEP = ["master", "season2/main", "core/main", "core/season2/main"]
POST = "core/season2/posts/a/main"
MERGED = "core/season2/posts/a/loops/L4.999/ag1"
UNMERGED = "core/season2/posts/a/loops/L4.999/ag2"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    """Run git inside `repo` — the ONLY git a test may run, always cwd-bound
    to the tmp fixture."""
    return subprocess.run(["git", *args], cwd=repo, capture_output=True,
                          text=True)


def _run_cli(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLI), "loop-prune", "--root", str(root), *args],
        capture_output=True, text=True)


def _write(repo: Path, rel: str, text: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def _build_repo(tmp_path: Path) -> Path:
    """Real git repo: bare origin with the full branch shape, a main checkout
    on master (never renamed). Everything stays cwd-bound to tmp."""
    r = tmp_path / "repo"
    r.mkdir()
    bare = tmp_path / "origin.git"
    bare.mkdir()
    _git(bare, "init", "-q", "--bare")
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@t")
    _git(r, "config", "user.name", "t")

    _write(r, "README", "hi\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "seed")

    _git(r, "remote", "add", "origin", str(bare))

    # KEEP trunk-pair names exist locally first (master already is HEAD), so
    # the push below has a source ref to move — `git push src:refs/heads/dst`
    # silently pushes nothing when the source branch does not exist.
    for name in KEEP:
        if name != "master":
            _git(r, "branch", name)

    # post branch at seed.
    _git(r, "branch", POST)
    # MERGED loop: a commit on top of seed, merged (fast-forward) into the
    # post so its tip becomes an ancestor of the post main. Its upstream is
    # set to the post so `git branch -d` (non-force) accepts the delete.
    _git(r, "checkout", "-q", "-b", MERGED)
    _write(r, "merged.txt", "merged round work\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "merged round work")
    _git(r, "checkout", "-q", POST)
    _git(r, "merge", "-q", "--no-edit", MERGED)
    _git(r, "branch", "--set-upstream-to", POST, MERGED)
    # UNMERGED loop: a commit NOT in the post main -> never an ancestor.
    _git(r, "checkout", "-q", "-b", UNMERGED)
    _write(r, "unmerged.txt", "unmerged round work\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "unmerged round work")

    # back on master, then push the whole shape to the bare origin.
    _git(r, "checkout", "-q", "master")
    for name in KEEP + [POST, MERGED, UNMERGED]:
        _git(r, "push", "-q", "origin", f"{name}:refs/heads/{name}")
    # materialise refs/remotes/origin/* so both namespace views are live.
    _git(r, "fetch", "-q", "origin")
    return r


def _local_heads(repo: Path) -> set[str]:
    r = _git(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads")
    return {b for b in r.stdout.split() if b}


def _origin_heads(repo: Path) -> set[str]:
    r = _git(repo, "for-each-ref", "--format=%(refname:short)",
             "refs/remotes")
    out = set()
    for b in r.stdout.split():
        if b.startswith("origin/") and len(b) > len("origin/"):
            out.add(b[len("origin/"):])
    return out


def _snapshot(repo: Path) -> dict:
    """Byte/tree snapshot of the fixture: ref count, worktree list and a
    working-tree digest — drives the 'changes nothing' assertions."""
    refs = _git(repo, "for-each-ref").stdout
    count = len([ln for ln in refs.splitlines() if ln.strip()])
    wts = _git(repo, "worktree", "list", "--porcelain").stdout
    h = hashlib.sha256()
    for p in sorted(repo.rglob("*")):
        if ".git" in p.parts:
            continue
        if p.is_file():
            h.update(str(p.relative_to(repo)).encode())
            h.update(p.read_bytes())
    return {"ref_count": count, "worktrees": wts, "tree_digest": h.hexdigest()}


@pytest.fixture()
def repo(tmp_path) -> Path:
    return _build_repo(tmp_path)


# ---- test 1: --apply prunes the MERGED loop, keeps the UNMERGED one ------
def test_loop_prune_apply_prunes_merged_only(repo: Path):
    res = _run_cli(repo / ".agi", "--apply")
    assert res.returncode == 0, res.stdout + res.stderr
    # merged loop gone locally and on origin
    assert MERGED not in _local_heads(repo), "merged loop must be pruned local"
    ls = _git(repo, "ls-remote", "origin",
              f"refs/heads/{MERGED}").stdout
    assert ls.strip() == "", "merged loop must be pruned on origin"
    # unmerged loop kept locally and on origin
    assert UNMERGED in _local_heads(repo), "unmerged loop must survive local"
    ls = _git(repo, "ls-remote", "origin",
              f"refs/heads/{UNMERGED}").stdout
    assert ls.strip(), "unmerged loop must survive on origin"
    # post main survives
    assert POST in _local_heads(repo), "post main must never be pruned"


# ---- test 2: unmerged branch is named per-branch and NEVER pruned ---------
def test_loop_prune_unmerged_named_and_kept(repo: Path):
    res = _run_cli(repo / ".agi", "--apply")
    assert res.returncode == 0, res.stdout + res.stderr
    assert UNMERGED in _local_heads(repo)
    ls = _git(repo, "ls-remote", "origin",
              f"refs/heads/{UNMERGED}").stdout
    assert ls.strip()
    # the per-branch output NAMES the refused branch and quotes the reason
    assert f"unmerged: {UNMERGED} -> NOT pruned" in res.stdout, res.stdout


# ---- test 3: dry-run (the DEFAULT) changes NOTHING, byte-for-byte ---------
def test_loop_prune_dry_run_changes_nothing(repo: Path):
    before = _snapshot(repo)
    res = _run_cli(repo / ".agi")  # no --apply -> dry-run
    assert res.returncode == 0, res.stdout + res.stderr
    assert "dry-run: nothing changed" in res.stdout, res.stdout
    # the plan names the MERGED loop it WOULD prune and the unmerged refusal
    assert MERGED in res.stdout, res.stdout
    assert f"unmerged: {UNMERGED} -> NOT pruned" in res.stdout, res.stdout
    after = _snapshot(repo)
    assert before == after, "dry-run must not change a single byte"
    assert MERGED in _local_heads(repo), "dry-run must not prune the loop"


# ---- test 4: never --force/-f; master and every remote-visible name remain
def test_loop_prune_never_forces_keeps_remote_visible(repo: Path):
    res = _run_cli(repo / ".agi", "--apply")
    assert res.returncode == 0, res.stdout + res.stderr
    # no destructive force switch anywhere in the prune pass
    assert "--force" not in res.stdout
    assert not any(" -f " in ln or ln.rstrip().endswith("-f")
                   for ln in res.stdout.splitlines()), res.stdout
    # master and every remote-visible name survive the prune
    sys.path.insert(0, str(BIN))
    import branches  # noqa: E402
    surviving = _local_heads(repo) | _origin_heads(repo)
    for name in KEEP:
        assert name in surviving, \
            f"remote-visible name {name} must survive loop-prune"
        assert branches.is_remote_visible(name)
    # and no surviving non-visible name was a displaced remote-visible one:
    # every surviving ref is either remote-visible or a post/loop leaf we own
    for name in surviving:
        if not branches.is_remote_visible(name):
            assert name.startswith("core/season2/posts/"), name
    ls = _git(repo, "ls-remote", "origin", "refs/heads/master").stdout
    assert ls.strip(), "master must survive loop-prune on the bare origin"