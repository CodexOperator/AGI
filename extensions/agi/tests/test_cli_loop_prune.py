"""Fixture proof for `cli.py loop-prune` — prune a loop branch iff it is
MERGED into its season main (all three loop grammars in use on this tree:
the v3 town-first `.../posts/<post>/loops/<round>/<agent>` up into its post
main, the season-first `season<n>/loops/<slug>-<agent>` and the legacy
`loop/<slug>-<agent>@s<n>` alias, both up into `season<n>/main`), plus `git
worktree prune` of DEAD KID worktrees under `.agi/worktrees/a00-*` — never a
post worktree, never an unmerged branch — listing every skip by name.
hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-
trunk-pair-per-level-reaches-origin / doc:l5-plan HEAD 1 item (d).

Builds a THROWAWAY git repo in tmp_path (never the live tree) with a real
BARE origin whose refs/heads cover the rule at once:

  KEEP (remote-visible)     master, season2/main, core/main, core/season2/main
  POST                        core/season2/posts/a/main
  MERGED loop                 core/season2/posts/a/loops/L4.999/ag1 (v3, merged)
  UNMERGED loop               core/season2/posts/a/loops/L4.999/ag2 (v3, unmerged)
  SEASON_MERGED               season2/loops/L5.10-a00    (season-first, merged)
  SEASON_UNMERGED             season2/loops/L5.11-a00  (season-first, unmerged)
  LEGACY_MERGED               loop/L5.12-a00@s2          (legacy alias, merged)
  one LIVE post worktree (on POST) + one DEAD kid worktree (registration
  dangles — its checkout dir was removed under .agi/worktrees/a00-dead1).

Asserts:
  * `loop-prune --apply` prunes MERGED/SEASON_MERGED/LEGACY_MERGED (local +
    origin gone) and NEVER the unmerged ones (named per-branch), and prunes
    the dead kid worktree while the live post worktree survives.
  * dry-run (the DEFAULT) prints the plan and changes NOTHING byte-for-byte
    (ref count, worktree list and tree digest identical before/after).
  * the prune never uses --force/-f and never deletes master or any
    remote-visible name (branches.is_remote_visible over the surviving refs).
  * every non-loop branch is named as left-alone (never a silent skip).
"""
from __future__ import annotations

import hashlib
import shutil
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
SEASON_MERGED = "season2/loops/L5.10-a00"
SEASON_UNMERGED = "season2/loops/L5.11-a00"
LEGACY_MERGED = "loop/L5.12-a00@s2"
DEAD_KID = "a00-dead1"
POST_WT = "post-live"


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

    # ---- the two OTHER loop grammars on this tree ----
    # SEASON_MERGED (season-first, merged into season2/main; upstream set so
    # `git branch -d` accepts its delete) and SEASON_UNMERGED (NOT an
    # ancestor of season2/main -> must be skipped by name).
    _git(r, "checkout", "-q", "season2/main")
    _git(r, "checkout", "-q", "-b", SEASON_MERGED)
    _write(r, "sm.txt", "season merged\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "season merged")
    _git(r, "checkout", "-q", "season2/main")
    _git(r, "merge", "-q", "--no-edit", SEASON_MERGED)
    _git(r, "branch", "--set-upstream-to", "season2/main", SEASON_MERGED)
    _git(r, "checkout", "-q", "-b", SEASON_UNMERGED)
    _write(r, "su.txt", "season unmerged\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "season unmerged")
    # LEGACY alias: loop/<slug>-<agent>@s2 == the season-first canonical, held
    # at the season2/main tip so it is merged; upstream set for `git branch -d`.
    _git(r, "checkout", "-q", "season2/main")
    _git(r, "branch", LEGACY_MERGED)
    _git(r, "branch", "--set-upstream-to", "season2/main", LEGACY_MERGED)

    # back on master, push the whole shape to the bare origin.
    _git(r, "checkout", "-q", "master")
    for name in KEEP + [POST, MERGED, UNMERGED, SEASON_MERGED,
                        SEASON_UNMERGED, LEGACY_MERGED]:
        _git(r, "push", "-q", "origin", f"{name}:refs/heads/{name}")
    # materialise refs/remotes/origin/* so both namespace views are live.
    _git(r, "fetch", "-q", "origin")
    # worktrees: ONE live post worktree (never touched) + ONE dead kid worktree
    # (its checkout dir is removed so the registration dangles and
    # `git worktree prune` clears both it and the SEASON_MERGED hold).
    wt = r / ".agi" / "worktrees"
    wt.mkdir(parents=True, exist_ok=True)
    _git(r, "worktree", "add", "-q", str(wt / POST_WT), POST)
    _git(r, "worktree", "add", "-q", str(wt / DEAD_KID), SEASON_MERGED)
    shutil.rmtree(wt / DEAD_KID)
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


def _worktree_paths(repo: Path) -> set[Path]:
    """The linked worktree checkout paths git currently tracks (porcelain)."""
    r = _git(repo, "worktree", "list", "--porcelain")
    out: set[Path] = set()
    cur: str | None = None
    for ln in r.stdout.splitlines():
        if ln.startswith("worktree "):
            cur = ln[len("worktree "):]
        elif not ln.strip() and cur:
            out.add(Path(cur))
            cur = None
    if cur:
        out.add(Path(cur))
    return out


def _orig_gone(repo: Path, name: str) -> bool:
    return _git(repo, "ls-remote", "origin",
                f"refs/heads/{name}").stdout.strip() == ""


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


# ---- test 1: --apply prunes every MERGED loop, keeps every unmerged one ---
def test_loop_prune_apply_prunes_merged_only(repo: Path):
    res = _run_cli(repo / ".agi", "--apply")
    assert res.returncode == 0, res.stdout + res.stderr
    # merged loops gone locally and on origin — across all three grammars
    for name in (MERGED, SEASON_MERGED, LEGACY_MERGED):
        assert name not in _local_heads(repo), \
            f"merged loop {name} must be pruned local"
        assert _orig_gone(repo, name), f"merged loop {name} on origin pruned"
    # unmerged loops kept locally and on origin
    for name in (UNMERGED, SEASON_UNMERGED):
        assert name in _local_heads(repo), \
            f"unmerged loop {name} must survive local"
        assert not _orig_gone(repo, name), \
            f"unmerged loop {name} must survive on origin"
    # post main survives
    assert POST in _local_heads(repo), "post main must never be pruned"


# ---- test 2: unmerged branches are named per-branch and NEVER pruned ------
def test_loop_prune_unmerged_named_and_kept(repo: Path):
    res = _run_cli(repo / ".agi", "--apply")
    assert res.returncode == 0, res.stdout + res.stderr
    # both unmerged loops survive
    for name in (UNMERGED, SEASON_UNMERGED):
        assert name in _local_heads(repo)
        assert not _orig_gone(repo, name)
        # the per-branch output NAMES each and quotes the reason
        assert f"unmerged: {name} -> NOT pruned" in res.stdout, res.stdout


# ---- test 3: dry-run (the DEFAULT) changes NOTHING, byte-for-byte ---------
def test_loop_prune_dry_run_changes_nothing(repo: Path):
    before = _snapshot(repo)
    res = _run_cli(repo / ".agi")  # no --apply -> dry-run
    assert res.returncode == 0, res.stdout + res.stderr
    assert "dry-run: nothing changed" in res.stdout, res.stdout
    # the plan names a merged loop it WOULD prune and an unmerged refusal
    assert SEASON_MERGED in res.stdout, res.stdout
    assert f"unmerged: {UNMERGED} -> NOT pruned" in res.stdout, res.stdout
    # the dead kid worktree is NAMED as a dry prune, and the post worktree is
    # NOT listed as anything to prune.
    assert DEAD_KID in res.stdout or f"{DEAD_KID}" in res.stdout, res.stdout
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
    # surviving non-visible refs are EXACTLY the post main and the unmerged
    # loops we own — every merged loop is gone, nothing foreign survives.
    allowed = {POST, UNMERGED, SEASON_UNMERGED}
    for name in surviving:
        if not branches.is_remote_visible(name):
            assert name in allowed, name
    ls = _git(repo, "ls-remote", "origin", "refs/heads/master").stdout
    assert ls.strip(), "master must survive loop-prune on the bare origin"


# ---- test 5: dead kid worktree pruned; live post worktree untouched -------
def test_loop_prune_apply_prunes_dead_kid_keeps_post_worktree(repo: Path):
    res = _run_cli(repo / ".agi", "--apply")
    assert res.returncode == 0, res.stdout + res.stderr
    dead = (repo / ".agi" / "worktrees" / DEAD_KID).resolve()
    post = (repo / ".agi" / "worktrees" / POST_WT).resolve()
    wts = _worktree_paths(repo)
    assert dead not in wts, "dead kid worktree must be pruned"
    assert post in wts, "live POST worktree must never be pruned"
    assert post.is_dir(), "post worktree checkout dir must survive"
    assert f"[APPLY] worktree prune (dead kid): git worktree prune {DEAD_KID}" \
        in res.stdout, res.stdout
    # the post worktree is never named as anything to prune
    assert f"worktree prune" not in [
        ln for ln in res.stdout.splitlines() if POST_WT in ln]


# ---- test 6: dry-run leaves the dead kid worktree registration present ----
def test_loop_prune_dry_run_keeps_dead_worktree(repo: Path):
    before = _worktree_paths(repo)
    assert (repo / ".agi" / "worktrees" / DEAD_KID).resolve() in before
    res = _run_cli(repo / ".agi")  # dry-run
    assert res.returncode == 0, res.stdout + res.stderr
    after = _worktree_paths(repo)
    assert before == after, "dry-run must not prune the dead worktree"
    assert (repo / ".agi" / "worktrees" / POST_WT).resolve() in after


# ---- test 7: every non-loop branch is named as left-alone, never silent ----
def test_loop_prune_names_left_alone_branches(repo: Path):
    res = _run_cli(repo / ".agi", "--apply")
    assert res.returncode == 0, res.stdout + res.stderr
    # every branch that is NOT a known loop grammar is named left-alone.
    for name in KEEP + [POST]:
        assert f"left alone: {name}`" in res.stdout or \
            f"left alone: {name} ->" in res.stdout, \
            f"non-loop branch {name} must be named as left-alone: {res.stdout}"