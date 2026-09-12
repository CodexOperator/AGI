"""Fixture proof for `cli.py branch-reshuffle` (hypothesis:l4-branches-follow-
the-season-grammar, clause 3 — the migration script). Builds a THROWAWAY git
repo in pytest tmp_path (never the live tree) with a BARE origin, a MAIN
checkout, two linked worktrees on legacy branches, legacy season branches
(season/s2, seat/post-*@s2, loop/x@s2, town/core/season/s2) and a fake
refs/grid ref so the byte-identity comparison is non-trivial. Every git call
runs cwd-bound to the tmp fixture or via `--root`.

Asserts:
  * `--dry-run` exits 0, names every branch-rename job + the worktree re-point
    + the ladder cell proposal, and changes NOTHING (git status clean).
  * `--apply` renames local branches (old gone, canonical present), pushes the
    new remote branches to the bare origin, re-points the linked worktrees
    onto the canonical names, NEVER touches refs/grid (byte-identical
    before/after), and does NOT delete the legacy remote branches.
  * `--delete-old` REFUSES (exit 3) without a green suite stamp and leaves the
    legacy remote branch in place.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
CLI = BIN / "cli.py"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    """Run git inside `repo` (the checkout top). The ONLY git a test may run —
    always cwd-bound to the tmp fixture."""
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)


def _run_cli(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLI), "branch-reshuffle", "--root", str(root), *args],
        capture_output=True, text=True)


def _write(repo: Path, rel: str, text: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def _build_repo(tmp_path: Path):
    """Real git repo: bare origin, main checkout on legacy season/s2, the two
    geometry cells (ladder + rotations with a legacy spelling each), two linked
    post worktrees, a fake refs/grid ref, and legacy branches. All git inside
    this tmp."""
    r = tmp_path / "repo"
    r.mkdir()
    bare = tmp_path / "origin.git"
    bare.mkdir()
    _git(bare, "init", "-q", "--bare")
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@t")
    _git(r, "config", "user.name", "t")

    # main checkout + geometry cells (Prime-owned cells the migration proposes)
    _write(r, "README", "hi\n")
    _write(r, ".agi/nodes/.geometry/ladder.md",
           "---\nid: config:ladder\ncurrent_season: 2\n---\n\ncells:\n  core: season/s2\n")
    _write(r, ".agi/nodes/.geometry/rotations.md",
           "---\nid: config:rotations\n---\n\n- F14: merge `season/s2` into your worktree\n")
    _write(r, ".gitignore", ".agi/sessions/\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "seed")

    # seed commit sha -> move the default branch to the legacy main spelling
    sha = _git(r, "rev-parse", "HEAD").stdout.strip()
    _git(r, "branch", "-m", "-q", "master", "season/s2")

    # fake refs/grid member so the identity assertion is non-trivial
    _git(r, "update-ref", "refs/grid/test/deadbeef", sha)

    # remote = BARE origin; push every legacy branch up front
    _git(r, "remote", "add", "origin", str(bare))
    _git(r, "branch", "seat/post-a@s2")
    _git(r, "branch", "loop/x@s2")
    _git(r, "branch", "town/core/season/s2")

    # linked post worktrees on two legacy branches
    _git(r, "worktree", "add", "-q", ".agi/worktrees/post-a", "seat/post-a@s2")
    _git(r, "worktree", "add", "-q", ".agi/worktrees/post-b", "loop/x@s2")

    _git(r, "checkout", "-q", "season/s2")
    _git(r, "push", "-q", "origin", "season/s2", "seat/post-a@s2", "loop/x@s2",
         "town/core/season/s2")
    _git(r, "fetch", "-q", "origin")  # create origin/* tracking refs
    return r


@pytest.fixture()
def repo(tmp_path):
    return _build_repo(tmp_path)


def _refs_grid(repo: Path) -> str:
    r = _git(repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/grid")
    return "\n".join(sorted(r.stdout.splitlines())) + "\n"


def test_dry_run_changes_nothing_and_names_jobs(repo: Path):
    before_status = _git(repo, "status", "--porcelain").stdout
    grid_before = _refs_grid(repo)

    res = _run_cli(repo / ".agi", "--dry-run")
    assert res.returncode == 0, res.stderr
    out = res.stdout

    # every branch-rename job named
    for old, new in [
        ("season/s2", "season2/main"),
        ("seat/post-a@s2", "season2/posts/post-a"),
        ("loop/x@s2", "season2/loops/x"),
        ("town/core/season/s2", "season2/core/season2/main"),
    ]:
        assert old in out and new in out, (old, new, out)

    # worktree re-point proposed for a worktree on a legacy branch
    assert "checkout season2/posts/post-a" in out

    # ladder + rotations cell proposals printed, never written
    assert "ladder.md:7: season/s2 -> season2/main" in out
    assert "rotations.md:5: season/s2 -> season2/main" in out  # the F14 cell

    # nothing changed
    assert _git(repo, "status", "--porcelain").stdout == before_status
    assert _refs_grid(repo) == grid_before
    # legacy branches still present, canonical absent
    assert "season2/main" not in _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "season/s2" in _git(repo, "branch", "--format=%(refname:short)").stdout


def test_apply_renames_pushes_repoints_and_keeps_grid_identical(repo: Path):
    grid_before = _refs_grid(repo)

    res = _run_cli(repo / ".agi", "--apply")
    assert res.returncode == 0, res.stderr
    out = res.stdout

    # local renames done
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout.split()
    for new in ["season2/main", "season2/posts/post-a", "season2/loops/x",
                "season2/core/season2/main"]:
        assert new in branches, (new, branches)
    for old in ["season/s2", "seat/post-a@s2", "loop/x@s2", "town/core/season/s2"]:
        assert old not in [b for b in branches if b not in ("master",)], old

    # canonical pushed to the bare origin
    origin = _git(repo, "branch", "-r", "--format=%(refname:short)").stdout
    assert "origin/season2/main" in origin
    assert "origin/season2/posts/post-a" in origin

    # legacy remote branches NOT deleted by --apply (delete is separate)
    assert "origin/season/s2" in origin

    # worktree re-pointed onto the canonical name
    wt_cur = _git(repo / ".agi/worktrees/post-a", "branch",
                  "--show-current").stdout.strip()
    assert wt_cur == "season2/posts/post-a", wt_cur

    # refs/grid BYTE-IDENTICAL before/after
    assert _refs_grid(repo) == grid_before
    assert "IDENTICAL" in out

    # --apply never implies the remote delete and never writes the cells
    assert "delete-old" in out
    assert "season/s2" in (repo / ".agi/nodes/.geometry/ladder.md").read_text()


def test_delete_old_refuses_without_green_stamp(repo: Path):
    grid_before = _refs_grid(repo)
    origin_before = _git(repo, "branch", "-r", "--format=%(refname:short)").stdout

    res = _run_cli(repo / ".agi", "--delete-old")
    assert res.returncode == 3, res.stdout
    assert "refuses" in res.stderr or "refuses" in res.stdout

    # legacy remote branch still present, grid untouched
    assert "origin/season/s2" in _git(repo, "branch", "-r",
                                      "--format=%(refname:short)").stdout
    assert origin_before == _git(repo, "branch", "-r",
                                 "--format=%(refname:short)").stdout
    assert _refs_grid(repo) == grid_before


sys.path.insert(0, str(BIN))
import cli  # noqa: E402


# --- --kinds filter (Prime XIV ruling at the mur-44 window, 04:18Z): ---
# `--kinds main,posts,towns` runs FIRST; the dead loop/* branches keep the
# names harvest notes and experiment nodes cite.

def test_reshuffle_kinds_parses_aliases_and_refuses_unknown():
    assert cli._reshuffle_kinds("") == set()
    assert cli._reshuffle_kinds("main,posts,towns") == {"main", "post", "town_main"}
    assert cli._reshuffle_kinds("loops") == {"loop"}
    with pytest.raises(SystemExit):
        cli._reshuffle_kinds("bogus")


def test_reshuffle_kind_of_canonical_names():
    assert cli._reshuffle_kind("season2/main") == "main"
    assert cli._reshuffle_kind("season2/posts/foo") == "post"
    assert cli._reshuffle_kind("season2/loops/x-a00-12345678") == "loop"
    assert cli._reshuffle_kind("season2/web-app-suite/season1/main") == "town_main"
    assert cli._reshuffle_kind("not/a/grammar/name/at/all/@@") == ""

def _town_alias_repo(tmp_path: Path):
    """The live-tree legacy town spelling (town/<t>@s2 — the mur-44 defect-4
    name that the old second-parser regex could NOT match)."""
    r = _build_repo(tmp_path)
    _git(r, "branch", "town/streaming-suite@s2")
    _git(r, "branch", "town/web-app-suite@s2")
    _git(r, "push", "-q", "origin", "town/streaming-suite@s2",
         "town/web-app-suite@s2")
    _git(r, "fetch", "-q", "origin")
    return r


# ---- defect 1: --delete-old actually EXECUTES the listed deletes --------
def test_delete_old_executes_deletes_when_stamp_present(repo: Path):
    (repo / ".agi/sessions").mkdir(parents=True, exist_ok=True)
    (repo / ".agi/sessions/verified.stamp").write_text("green")

    res = _run_cli(repo / ".agi", "--delete-old")
    assert res.returncode == 0, res.stderr
    origin = _git(repo, "branch", "-r", "--format=%(refname:short)").stdout
    for old in ["season/s2", "seat/post-a@s2", "loop/x@s2",
                "town/core/season/s2"]:
        assert f"origin/{old}" not in origin, (old, origin)
    # remote-only: local legacy branches stay (a later decide renames those)
    local = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "season/s2" in local and "seat/post-a@s2" in local


# ---- defect 2: --apply is RESUMABLE + defect 3: upstream re-pointed ----
def test_apply_sets_upstream_and_is_resumable(repo: Path):
    res = _run_cli(repo / ".agi", "--apply")
    assert res.returncode == 0, res.stderr
    for old, new in [("season/s2", "season2/main"),
                     ("seat/post-a@s2", "season2/posts/post-a")]:
        up = _git(repo, "rev-parse", "--abbrev-ref",
                  f"{new}@{{upstream}}").stdout.strip()
        assert up == f"origin/{new}", (new, up)
    # re-running --apply after a full apply RESUMES: origin still lists the
    # legacy names (delete-old is separate), so each job is skipped BY NAME as
    # already renamed -- never a hard fail on git branch -m.
    res2 = _run_cli(repo / ".agi", "--apply")
    assert res2.returncode == 0, res2.stderr
    assert "already renamed" in res2.stdout


def test_apply_refuses_origin_moved_by_name(tmp_path: Path):
    r = _build_repo(tmp_path)
    root = r / ".agi"
    # baseline the dry-run plan (records each old branch's origin tip)
    res_dry = _run_cli(root, "--dry-run")
    assert res_dry.returncode == 0, res_dry.stderr
    # move origin's season/s2 tip externally
    _write(r, "moved", "x\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "move origin tip")
    _git(r, "push", "-q", "origin", "HEAD:refs/heads/season/s2")

    res = _run_cli(root, "--apply")
    assert res.returncode == 1, res.stdout
    assert "REFUSES season/s2" in res.stderr, res.stderr
    # the refused branch was not renamed; the tree was not swept wholesale
    local = _git(r, "branch", "--format=%(refname:short)").stdout
    assert "season/s2" in local


# ---- defect 4: --kinds towns matches the LIVE legacy town spelling -------
def test_dry_run_plans_live_legacy_town_at_alias(tmp_path: Path):
    r = _town_alias_repo(tmp_path)
    res = _run_cli(r / ".agi", "--dry-run", "--kinds", "towns")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert "town/streaming-suite@s2" in out
    assert "season2/streaming-suite/season1/main" in out
    assert "town/web-app-suite@s2" in out
    assert "season2/web-app-suite/season1/main" in out


# ---- defect 5: branch-reshuffle COMPOSES after post-rename --------------
def test_post_rename_output_post_at_composes(tmp_path: Path):
    r = _build_repo(tmp_path)
    _git(r, "branch", "post/post-x@s2")
    _git(r, "push", "-q", "origin", "post/post-x@s2")
    _git(r, "fetch", "-q", "origin")
    res = _run_cli(r / ".agi", "--dry-run")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert "post/post-x@s2" in out
    assert "season2/posts/post-x" in out


# ---- KID D contract: last line of --dry-run is the one-line runbook note --
def test_dry_run_last_line_is_runbook_note(repo: Path):
    res = _run_cli(repo / ".agi", "--dry-run")
    assert res.returncode == 0, res.stderr
    nonempty = [ln for ln in res.stdout.splitlines() if ln.strip()]
    assert nonempty, "dry-run output empty"
    assert nonempty[-1].startswith("runbook:"), nonempty[-1]

