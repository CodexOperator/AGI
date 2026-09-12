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
    # L4.320 (KID A): seed the DEFECT'S precondition — every legacy branch
    # TRACKS origin/<old>. The old truthy gate (`if not _post_rename_upstream`)
    # never re-pointed a branch that carried origin/<old> through `git branch
    # -m`; without the tracking these fixtures made that gate test green.
    for _legacy in ["season/s2", "seat/post-a@s2", "loop/x@s2",
                    "town/core/season/s2"]:
        _git(r, "branch", "--set-upstream-to", f"origin/{_legacy}", _legacy)
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

    # prime ruling window-46 (goal:g17.1): an unfiltered --dry-run DEFAULTS to
    # posts,towns, so only the post and town jobs are planned, and the default
    # is PRINTED in the plan (a reader of the dry-run sees the filter applied).
    assert "defaulted to kinds posts,towns" in out, out
    for old, new in [
        ("seat/post-a@s2", "season2/posts/post-a"),
        ("town/core/season/s2", "season2/core/season2/main"),
    ]:
        assert old in out and new in out, (old, new, out)
    # main and loop are NOT planned under the default (substring-safe: check
    # the exact rename command line, not the bare branch token)
    for old, new in [("season/s2", "season2/main"),
                     ("loop/x@s2", "season2/loops/x")]:
        assert f"[DRY ] branch rename (local): git branch -m {old} {new}" \
            not in out, (old, new, out)

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

    # explicit all-four kinds preserves the FULL coverage that the old
    # unfiltered default used to give (ruling: explicit list means all four)
    res = _run_cli(repo / ".agi", "--apply", "--kinds", "main,posts,towns,loops")
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


# ---- L4.319 residue (mur-46, verbatim): an explicit --kinds that parses ----
# ---- to the EMPTY set (`,`, ` , `, any separator/whitespace string) is ----
# ---- NOT the absent case. It refuses BY NAME, exit 1, never unfiltered. ---
def test_explicit_empty_kinds_refuses_by_name_and_lists_nothing(repo: Path):
    for spec in [",", " , ", ",,,"]:
        res = _run_cli(repo / ".agi", "--dry-run", "--kinds", spec)
        assert res.returncode == 1, (spec, res.stdout, res.stderr)
        assert f"--kinds: {spec!r} parsed to no kinds" in res.stderr, \
            (spec, res.stderr)
        assert "one of main, posts, loops, towns" in res.stderr, res.stderr
        # no jobs listed, no defaulting line, nothing about a default
        assert "branch rename" not in res.stdout, (spec, res.stdout)
        assert "defaulted to kinds" not in res.stdout, (spec, res.stdout)
        assert res.stdout.strip() == "", (spec, res.stdout)


def test_explicit_empty_kinds_refuses_under_delete_old(repo: Path):
    # --delete-old is where the UNFILTERED hazard is worst; the empty set
    # must refuse there too, before any delete step is considered.
    res = _run_cli(repo / ".agi", "--delete-old", "--kinds", ",")
    assert res.returncode == 1, (res.stdout, res.stderr)
    assert "--kinds: ',' parsed to no kinds" in res.stderr, res.stderr
    assert "defaulted to kinds" not in res.stdout, res.stdout


def test_unknown_kind_still_refuses_by_name(repo: Path):
    # L4.319 behaviour, unchanged: an UNKNOWN word is refused inside
    # _reshuffle_kinds, before any plan is produced.
    res = _run_cli(repo / ".agi", "--dry-run", "--kinds", "posts,bogus")
    assert res.returncode == 1, (res.stdout, res.stderr)
    assert "--kinds: unknown kind 'bogus'" in res.stderr, res.stderr
    assert "branch rename" not in res.stdout, res.stdout


def test_absent_kinds_still_defaults_and_prints(repo: Path):
    # L4.319 behaviour, unchanged: an ABSENT --kinds defaults to posts,towns
    # and PRINTS the defaulting line.
    res = _run_cli(repo / ".agi", "--dry-run")
    assert res.returncode == 0, res.stderr
    assert "defaulted to kinds posts,towns" in res.stdout, res.stdout
    assert "--kinds" not in res.stderr, res.stderr


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
def _apply_kinds(root: Path, kinds: str) -> None:
    """Run `--apply` for a specific kind list (mirroring what the matching
    --delete-old would gate on), so exactly those branches are renamed and
    re-pointed while the others stay local legacy."""
    res = _run_cli(root, "--apply", "--kinds", kinds)
    assert res.returncode == 0, res.stdout + res.stderr


def _apply_all(root: Path) -> None:
    """Run `--apply` with the explicit full kind list so every legacy branch
    is renamed and its upstream re-pointed onto origin/<new>. B2 (L4.320)
    gates --delete-old on that upstream, so any delete test must migrate first
    just like the live run does (repoint --apply, THEN the final delete)."""
    _apply_kinds(root, "main,posts,towns,loops")


def test_delete_old_executes_deletes_when_stamp_present(repo: Path):
    # migrate ONLY posts,towns (the default delete set) so main+loop branches
    # stay local legacy -- the delete default then mirrors the apply set and
    # leaves their origin refs untouched.
    _apply_kinds(repo / ".agi", "posts,towns")
    (repo / ".agi/sessions").mkdir(parents=True, exist_ok=True)
    (repo / ".agi/sessions/verified.stamp").write_text("green")

    # prime ruling window-46: an UNFILTERED --delete-old defaults to
    # posts,towns — it touches NO loop and NO main/master branch, the default
    # is printed, and the delete set equals posts,towns.
    res = _run_cli(repo / ".agi", "--delete-old")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "defaulted to kinds posts,towns" in res.stdout, res.stdout
    origin = _git(repo, "branch", "-r", "--format=%(refname:short)").stdout
    for old in ["seat/post-a@s2", "town/core/season/s2"]:
        assert f"origin/{old}" not in origin, (old, origin)
    # loop and main are NOT delete jobs under the default
    assert "origin/loop/x@s2" in origin, "default must NOT delete the loop"
    assert "origin/season/s2" in origin, "default must NOT delete the main"
    # remote-only: the non-renamed local legacy branches stay
    local = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "season/s2" in local and "loop/x@s2" in local, local


# ---- prime ruling window-46: --kinds loops is the ONLY way a loop deletes --
def test_delete_old_loop_deletes_only_under_explicit_loops(repo: Path):
    # the explicit full list still means ALL FOUR (ruling forbids the
    # UNFILTERED default, not an explicit full list) -- checked on an
    # UN-migrated tree, where every legacy branch is still present to list.
    res0 = _run_cli(repo / ".agi", "--dry-run", "--kinds",
                    "main,posts,towns,loops")
    assert res0.returncode == 0, res0.stderr
    assert "defaulted to kinds posts,towns" not in res0.stdout, res0.stdout
    for old, new in [("season/s2", "season2/main"),
                     ("seat/post-a@s2", "season2/posts/post-a"),
                     ("loop/x@s2", "season2/loops/x"),
                     ("town/core/season/s2", "season2/core/season2/main")]:
        assert f"[DRY ] branch rename (local): git branch -m {old} {new}" \
            in res0.stdout, (old, new, res0.stdout)

    # migrate ONLY the loop (the kind --delete-old --kinds loops will gate on)
    _apply_kinds(repo / ".agi", "loops")
    (repo / ".agi/sessions").mkdir(parents=True, exist_ok=True)
    (repo / ".agi/sessions/verified.stamp").write_text("green")

    # `--kinds loops` lists ONLY the loop for deletion (no post/town/main)
    res = _run_cli(repo / ".agi", "--delete-old", "--kinds", "loops")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "origin --delete loop/x@s2" in res.stdout, res.stdout
    assert "origin --delete seat/post-a@s2" not in res.stdout, res.stdout
    assert "origin --delete town/core/season/s2" not in res.stdout, res.stdout
    assert "origin --delete season/s2" not in res.stdout, res.stdout
    origin = _git(repo, "branch", "-r", "--format=%(refname:short)").stdout
    assert "origin/loop/x@s2" not in origin
    for kept in ["origin/seat/post-a@s2", "origin/town/core/season/s2",
                 "origin/season/s2"]:
        assert kept in origin, kept


# ---- defect 2: --apply is RESUMABLE + defect 3: upstream re-pointed ----
def test_apply_sets_upstream_and_is_resumable(repo: Path):
    # explicit all-four kinds so season/s2 (kind main) is an apply job
    res = _run_cli(repo / ".agi", "--apply", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 0, res.stderr
    for old, new in [("season/s2", "season2/main"),
                     ("seat/post-a@s2", "season2/posts/post-a")]:
        up = _git(repo, "rev-parse", "--abbrev-ref",
                  f"{new}@{{upstream}}").stdout.strip()
        assert up == f"origin/{new}", (new, up)
    # re-running --apply after a full apply RESUMES: origin still lists the
    # legacy names (delete-old is separate), so each job is skipped BY NAME as
    # already renamed -- never a hard fail on git branch -m.
    res2 = _run_cli(repo / ".agi", "--apply", "--kinds",
                    "main,posts,towns,loops")
    assert res2.returncode == 0, res2.stderr
    assert "already renamed" in res2.stdout


# ---- L4.320 (KID A): carried-upstream re-point (falsifier for A1) ----
def test_apply_repoints_a_branch_that_carried_origin_old(repo: Path):
    # A branch that ALREADY TRACKED origin/<old> before --apply must be
    # re-pointed onto origin/<new>. The old truthy gate (`if not
    # _post_rename_upstream`) skipped any Truthy carried-origin/<old> upstream,
    # so it stayed stale. FAILS before A1, PASSES after.
    assert _git(repo, "rev-parse", "--abbrev-ref",
                "season/s2@{upstream}").stdout.strip() == "origin/season/s2"
    res = _run_cli(repo / ".agi", "--apply", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 0, res.stderr
    up = _git(repo, "rev-parse", "--abbrev-ref",
              "season2/main@{upstream}").stdout.strip()
    assert up == "origin/season2/main", up


# ---- L4.320 (KID A): master is ADD-ONLY in --apply too (A4) -----------
def test_apply_keeps_master_standing_and_pushes_new_name_from_its_tip(
        tmp_path):
    r = _master_repo(tmp_path)
    master_tip = _git(r, "rev-parse", "master").stdout.strip()
    res = _run_cli(r / ".agi", "--apply", "--kinds", "main,posts,towns,loops")
    assert res.returncode == 0, res.stderr
    # local master still stands (never `git branch -m`'d), no local season1/main
    local = _git(r, "branch", "--format=%(refname:short)").stdout
    assert "master" in local, local
    assert "season1/main" not in local, local
    # the new name (season1/main) got master's tip on origin
    ls = _git(r, "ls-remote", "origin", "refs/heads/season1/main").stdout.split()
    assert ls and ls[0] == master_tip, (ls, master_tip)
    # master still tracks origin/master
    up = _git(r, "rev-parse", "--abbrev-ref", "master@{upstream}").stdout.strip()
    assert up == "origin/master", up


def test_apply_refuses_origin_moved_by_name(tmp_path: Path):
    r = _build_repo(tmp_path)
    root = r / ".agi"
    # explicit all-four kinds so season/s2 (kind main) is a job under the ruling
    kinds = ["main,posts,towns,loops"]
    # baseline the dry-run plan (records each old branch's origin tip)
    res_dry = _run_cli(root, "--dry-run", "--kinds", *kinds)
    assert res_dry.returncode == 0, res_dry.stderr
    # move origin's season/s2 tip externally
    _write(r, "moved", "x\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "move origin tip")
    _git(r, "push", "-q", "origin", "HEAD:refs/heads/season/s2")

    res = _run_cli(root, "--apply", "--kinds", *kinds)
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


# ---- KID 2 (L4.316): delete ORDER posts->towns->mains, master ADD-ONLY --
def _master_repo(tmp_path: Path):
    """The base fixture PLUS a `master` branch (which reshuffles to
    season1/main, kind main) on the local branches and the bare origin."""
    r = _build_repo(tmp_path)
    _git(r, "branch", "master")
    _git(r, "push", "-q", "origin", "master")
    _git(r, "fetch", "-q", "origin")
    _git(r, "branch", "--set-upstream-to", "origin/master", "master")
    return r


def _first(haystack: str, needle: str) -> int:
    return haystack.index(needle)


def test_delete_old_orders_posts_towns_mains_and_keeps_master(tmp_path: Path):
    r = _master_repo(tmp_path)
    _apply_all(r / ".agi")
    (r / ".agi/sessions").mkdir(parents=True, exist_ok=True)
    (r / ".agi/sessions/verified.stamp").write_text("green")

    res = _run_cli(r / ".agi", "--delete-old", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    # delete order is post(s) -> town(s) -> main(s) -> loop(s), by OLD name
    posts = "origin --delete seat/post-a@s2"
    towns = "origin --delete town/core/season/s2"
    mains = "origin --delete season/s2"
    loops = "origin --delete loop/x@s2"
    assert _first(out, posts) < _first(out, towns) < _first(out, mains)\
        < _first(out, loops), out
    # master is add-only: it is NOT a delete job, and the add-only line names it
    assert "origin --delete master" not in out
    assert "master: add-only" in out
    # master's remote name is KEPT
    ls = _git(r, "ls-remote", "origin", "refs/heads/master").stdout
    assert ls.strip(), "origin/master must survive --delete-old"
    # the rest WERE deleted remotely
    origin = _git(r, "branch", "-r", "--format=%(refname:short)").stdout
    for old in ["season/s2", "seat/post-a@s2", "loop/x@s2",
                "town/core/season/s2"]:
        assert f"origin/{old}" not in origin, (old, origin)


# ---- KID 2 (B2, L4.320): --delete-old is GATED on upstream=origin/<new> --
def test_delete_old_refuses_by_name_and_deletes_nothing_when_unpointed(tmp_path: Path):
    """(B2) AFTER a full migration, if ANY delete target's upstream drifts
    back to its carried origin/<old>, `--delete-old` REFUSES by NAME and
    deletes NOTHING — not even the branches that ARE still pointed (the gate
    is all-or-nothing, so a stranded branch can never be deleted/stripped).
    This is the falsifier for the B2 gate: drop the gate and this test's
    `assert origin/seat/post-a@s2 still present` flips."""
    r = _build_repo(tmp_path)
    _apply_all(r / ".agi")
    (r / ".agi/sessions").mkdir(parents=True, exist_ok=True)
    (r / ".agi/sessions/verified.stamp").write_text("green")
    # sabotage ONE migration target's upstream back to the carried old name
    _git(r, "branch", "--set-upstream-to", "origin/seat/post-a@s2",
         "season2/posts/post-a")
    for name in ["season2/main", "season2/core/season2/main",
                 "season2/loops/x"]:
        assert _git(r, "rev-parse", "--abbrev-ref",
                    f"{name}@{{upstream}}").stdout.strip() == f"origin/{name}", name

    res = _run_cli(r / ".agi", "--delete-old", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 1, res.stdout + res.stderr
    assert "season2/posts/post-a" in res.stderr, res.stderr
    # ALL-OR-NOTHING: the well-pointed branches are NOT deleted either
    origin = _git(r, "branch", "-r", "--format=%(refname:short)").stdout
    for old in ["season/s2", "seat/post-a@s2", "town/core/season/s2",
                "loop/x@s2"]:
        assert f"origin/{old}" in origin, (old, origin)


# ---- KID 2 (B1, L4.320): --dry-run --delete-old prints [DRY ] runs none --
def test_delete_old_dry_run_prints_zero_runs(tmp_path: Path):
    """(B1) `--dry-run --delete-old` prints every delete as a `[DRY ]` line
    and runs NONE of them — the remote still holds every old branch, and the
    run needs no green-suite stamp (a dry run deletes nothing)."""
    r = _build_repo(tmp_path)
    _apply_all(r / ".agi")
    res = _run_cli(r / ".agi", "--dry-run", "--delete-old", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "dry-run: nothing changed" in res.stdout, res.stdout
    # every legacy branch names its [DRY ] delete line
    for old in ["season/s2", "seat/post-a@s2", "town/core/season/s2",
                "loop/x@s2"]:
        assert f"[DRY ] branch delete (remote): git push origin --delete {old}" \
            in res.stdout, (old, res.stdout)
    # ...and NONE executed: the remote still holds every old branch
    origin = _git(r, "branch", "-r", "--format=%(refname:short)").stdout
    for old in ["season/s2", "seat/post-a@s2", "town/core/season/s2",
                "loop/x@s2"]:
        assert f"origin/{old}" in origin, (old, origin)


# ---- KID 2: the origin-moved refusal never re-baselines -----------------
def test_apply_refuses_origin_moved_a_second_time_same_branch(tmp_path: Path):
    r = _build_repo(tmp_path)
    root = r / ".agi"
    kinds = ["main,posts,towns,loops"]
    res_dry = _run_cli(root, "--dry-run", "--kinds", *kinds)
    assert res_dry.returncode == 0, res_dry.stderr
    # move origin's season/s2 tip externally, AFTER the baseline was taken
    _write(r, "moved", "x\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "move origin tip")
    _git(r, "push", "-q", "origin", "HEAD:refs/heads/season/s2")

    res1 = _run_cli(root, "--apply", "--kinds", *kinds)
    assert res1.returncode == 1, res1.stdout
    assert "REFUSES season/s2" in res1.stderr, res1.stderr

    # a SECOND --apply must be refused the SAME way: --apply never
    # overwrote the baseline, so it still compares against the pre-move shas.
    res2 = _run_cli(root, "--apply", "--kinds", *kinds)
    assert res2.returncode == 1, res2.stdout
    assert "REFUSES season/s2" in res2.stderr, res2.stderr
    # the twice-refused branch was never locally renamed
    local = _git(r, "branch", "--format=%(refname:short)").stdout
    assert "season/s2" in local


# ---- KID D contract: last line of --dry-run is the one-line runbook note --
def test_dry_run_last_line_is_runbook_note(repo: Path):
    res = _run_cli(repo / ".agi", "--dry-run")
    assert res.returncode == 0, res.stderr
    nonempty = [ln for ln in res.stdout.splitlines() if ln.strip()]
    assert nonempty, "dry-run output empty"
    assert nonempty[-1].startswith("runbook:"), nonempty[-1]



# ---- L4.319 (KID B): a `post/<n>@s2` intermediate branch maps to season2/posts/<n> ----
# branches.py now parses the `post/<name>@s<N>` intermediate spelling (the
# seat->post rename's mid-point). A dry-run plan over a `post/post-y@s2` branch
# must NAME the canonical `season2/posts/post-y` target with NO-MATCH absent
# and no wrong kind (hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-
# post-n-maps-to-season2-posts). --dry-run only — never --apply.
def test_dry_run_plans_intermediate_post_at_to_canonical(tmp_path: Path):
    r = _build_repo(tmp_path)
    _git(r, "branch", "post/post-y@s2")
    _git(r, "push", "-q", "origin", "post/post-y@s2")
    _git(r, "fetch", "-q", "origin")
    res = _run_cli(r / ".agi", "--dry-run")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert "post/post-y@s2" in out
    assert "season2/posts/post-y" in out
    assert "NO-MATCH" not in out
