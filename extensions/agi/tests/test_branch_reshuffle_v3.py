"""Fixture proof for `cli.py branch-reshuffle --delete-old`'s delete set being
DERIVED from the ONE predicate branches.is_remote_visible plus the two
never-delete carve-outs — never a hand-spelled stale-name list
(hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-
pair-per-level-reaches-origin).

Builds a THROWAWAY git repo in tmp_path (never the live tree) with a fake
BARE origin whose refs/heads cover the whole rule at once:

  REMOTE-VISIBLE keep   master, season2/main, core/main, core/season2/main
  SUB-TOP-LEVEL delete  core/season2/posts/sanctuary-director/main
                        core/season2/posts/sanctuary-director/loops/L4.332/a00-x
  STALE pre-rename del  season/s2, seat/sanctuary-director@s2,
                        post/sanctuary-director@s2, town/core@s2
  FOREIGN untouched     copilot/whatever, collaborator-branch

Asserts:
  * the --dry-run --delete-old plan names EVERY sub-top-level + stale name and
    NO foreign/master/remote-visible name, and is_remote_visible AGREES with
    the keep set on every fixture name.
  * --dry-run --delete-old writes NOTHING AT ALL (ref count, worktree list and
    a working-tree digest all byte-identical before/after; the resumability
    plan file is ABSENT) — while a plain --dry-run (no --delete-old) still
    writes exactly the one gitignored sessions/branch-reshuffle-plan.json.
  * --delete-old never forces (no --force / -f anywhere in the delete
    commands) and never touches master: refs/heads/master still exists on the
    bare origin after the planned pass.
  * a push helper handed a sub-top-level name REFUSES BY NAME: it must raise
    branches.assert_remote_visible's ValueError naming the branch (exit != 0
    at a CLI boundary), while a remote-visible name pushes cleanly.
"""
from __future__ import annotations

import hashlib
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


# The fixture's full branch set, grouped by what the rule does with each.
KEEP = ["master", "season2/main", "core/main", "core/season2/main"]
DELETE = [
    "core/season2/posts/sanctuary-director/main",
    "core/season2/posts/sanctuary-director/loops/L4.332/a00-x",
    "season/s2",
    "seat/sanctuary-director@s2",
    "post/sanctuary-director@s2",
    "town/core@s2",
]
FOREIGN = ["copilot/whatever", "collaborator-branch"]


def _build_repo(tmp_path: Path):
    """Real git repo: bare origin whose refs/heads cover the whole rule, a
    main checkout on master (never renamed — master is the frozen season-1
    name the delete must always keep). Everything stays cwd-bound to tmp."""
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
    for name in KEEP + DELETE + FOREIGN:
        # full ref-path push so sub-top-level names reach refs/heads even
        # though git would refuse `git push origin <name>` guessing a branch
        _git(r, "branch", name)
        _git(r, "push", "-q", "origin", f"{name}:refs/heads/{name}")
    return r


def _snapshot(repo: Path) -> dict:
    """Byte/tree snapshot of the fixture: ref count, worktree list and a
    working-tree digest (walking every file except .git). Drives the
    'changes nothing' assertions."""
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
def repo(tmp_path):
    return _build_repo(tmp_path)


# ---- test 1: is_remote_visible AGREES with the keep set on every fixture ----
def test_is_remote_visible_agrees_with_keep_set(repo: Path):
    sys.path.insert(0, str(BIN))
    import branches  # noqa: E402
    for name in KEEP:
        assert branches.is_remote_visible(name), f"keep set member not visible: {name}"
    for name in DELETE + FOREIGN:
        assert not branches.is_remote_visible(name), \
            f"non-visible name reported visible: {name}"


# ---- test 2: the delete plan names every sub-top-level + stale name, and ----
# ---- NO foreign/master/remote-visible name -------------------------------
def test_delete_plan_names_every_delete_and_nothing_else(repo: Path):
    res = _run_cli(repo / ".agi", "--dry-run", "--delete-old", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 0, res.stdout + res.stderr
    out = res.stdout
    for name in DELETE:
        assert f"[DRY ] branch delete (remote): git push origin --delete {name}" \
            in out, (name, out)
    # master is add-only, never a delete target — the standing notice names it
    assert "master: add-only" in out, out
    for name in KEEP + FOREIGN:
        assert f"git push origin --delete {name}" not in out, (name, out)


# ---- test 2b: the DISCRIMINATING default-kinds test (L4.332) -----
# kid 2's suite asserted the delete set with ALL FOUR kinds named explicitly,
# which cannot see the DEFAULT-set defect: with default kinds {post,town_main}
# a v3 loop branch is NOT a delete job, and with {loop} it IS. A test that
# names every kind is not evidence about the default (Hypothesis
# l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-
# level-reaches-origin).
def test_delete_default_kinds_never_take_a_v3_loop(repo: Path):
    res = _run_cli(repo / ".agi", "--dry-run", "--delete-old")  # --kinds ABSENT -> default
    assert res.returncode == 0, res.stdout + res.stderr
    out = res.stdout
    loop = "core/season2/posts/sanctuary-director/loops/L4.332/a00-x"
    post = "core/season2/posts/sanctuary-director/main"
    # DEFAULT kinds {post,town_main}: the post main IS a delete job, the loop
    # branch under it is NOT
    assert f"git push origin --delete {post}" in out, out
    assert f"git push origin --delete {loop}" not in out, \
        "DEFAULT kinds must never take a v3 loop branch (the /posts/ prefix " \
        "must not win; the loop kind is reachable only when named)"


def test_delete_named_loops_kind_takes_the_v3_loop(repo: Path):
    res = _run_cli(repo / ".agi", "--dry-run", "--delete-old", "--kinds", "loop")
    assert res.returncode == 0, res.stdout + res.stderr
    out = res.stdout
    loop = "core/season2/posts/sanctuary-director/loops/L4.332/a00-x"
    assert f"git push origin --delete {loop}" in out, out
    post = "core/season2/posts/sanctuary-director/main"
    assert f"git push origin --delete {post}" not in out, \
        "--kinds loop must take ONLY the loop, never the post"


# ---- test 3: --dry-run --delete-old writes NOTHING AT ALL -----------------
def test_dry_run_delete_old_changes_nothing(repo: Path):
    before = _snapshot(repo)
    plan = repo / ".agi" / "sessions" / "branch-reshuffle-plan.json"
    assert not plan.exists(), "pre-run plan file must be absent"

    res = _run_cli(repo / ".agi", "--dry-run", "--delete-old", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 0, res.stderr
    after = _snapshot(repo)
    assert before == after, (before, after)
    # no plan/baseline file written either — a --delete-old dry run is a pure
    # preview (the resumability plan is a --apply/normal-dry-run concern)
    assert not plan.exists(), "delete-old dry run must not write the plan file"
    assert not list((repo / ".agi" / "sessions").glob("*.json"))


# ---- test 4: plain --dry-run (no --delete-old) still writes ONLY the plan --
def test_plain_dry_run_writes_only_the_plan_file(repo: Path):
    before = _snapshot(repo)
    plan = repo / ".agi" / "sessions" / "branch-reshuffle-plan.json"
    assert not plan.exists()

    res = _run_cli(repo / ".agi", "--dry-run", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 0, res.stderr
    # exactly the one gitignored plan file appeared
    assert plan.exists(), "plain --dry-run must write the resumability plan"
    after = _snapshot(repo)
    # the plan file itself is the only diff (it is under .agi/sessions/, which
    # the tree digest includes, so re-write its bytes into a snapshot == before)
    plan_saved = plan.read_bytes()
    plan.unlink()
    after_without_plan = _snapshot(repo)
    assert before == after_without_plan, (before, after_without_plan)
    plan.write_bytes(plan_saved)


# ---- test 5: never force; master still on origin after the planned pass ----
def test_delete_old_never_forces_and_keeps_master(repo: Path):
    res = _run_cli(repo / ".agi", "--dry-run", "--delete-old", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 0, res.stderr
    # no destructive force switch anywhere in the delete pass
    assert "--force" not in res.stdout
    assert not any(f" -f " in ln or ln.rstrip().endswith("-f")
                   for ln in res.stdout.splitlines()), res.stdout
    # refs/heads/master still exists on the bare origin after the pass
    ls = _git(repo, "ls-remote", "origin", "refs/heads/master").stdout
    assert ls.strip(), "master must survive --delete-old on the bare origin"


# ---- test 6: a push of a sub-top-level name is REFUSED BY NAME -------------
def _push_remote_visible(repo: Path, name: str, src: str) -> None:
    """The CLI-boundary push helper: it REFUSES any refs/heads write whose name
    is not remote-visible — via branches.assert_remote_visible, so the refusal
    names the branch AND the rule (and would be a non-zero CLI exit)."""
    sys.path.insert(0, str(BIN))
    import branches  # noqa: E402
    branches.assert_remote_visible(name)  # raises ValueError by name
    _git(repo, "push", "-q", "origin", f"{src}:refs/heads/{name}")


def test_push_helper_refuses_sub_top_level_by_name(repo: Path):
    with pytest.raises(ValueError) as ei:
        _push_remote_visible(repo, "core/season2/posts/x/main", "master")
    assert "core/season2/posts/x/main" in str(ei.value), ei.value
    # the refused name never reached origin
    ls = _git(repo, "ls-remote", "origin",
              "refs/heads/core/season2/posts/x/main").stdout
    assert ls.strip() == "", "refused sub-top-level name must not be pushed"


def test_push_helper_allows_remote_visible(repo: Path):
    # a trunk-pair name pushes cleanly (assert_remote_visible returns None)
    _push_remote_visible(repo, "core/main", "master")
    ls = _git(repo, "ls-remote", "origin", "refs/heads/core/main").stdout
    assert ls.strip(), "remote-visible name must push cleanly"