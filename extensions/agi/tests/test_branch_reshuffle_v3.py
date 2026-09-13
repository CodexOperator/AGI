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


# ---- test 4: plain --dry-run (no --delete-old) writes NOTHING (I-3a-2) ----
# Old behaviour: plain --dry-run wrote the gitignored resumability plan file.
# The round moves the plan-file write to --apply / an explicit --plan-out PATH,
# so --dry-run is a pure preview again: no plan file, no baseline, nothing.
def test_plain_dry_run_writes_nothing(repo: Path):
    before = _snapshot(repo)
    plan = repo / ".agi" / "sessions" / "branch-reshuffle-plan.json"
    assert not plan.exists()

    res = _run_cli(repo / ".agi", "--dry-run", "--kinds",
                   "main,posts,towns,loops")
    assert res.returncode == 0, res.stderr
    after = _snapshot(repo)
    # the dry run changes NOTHING, and writes no plan/baseline file either
    assert before == after, (before, after)
    assert not plan.exists(), "--dry-run must NOT write the resumability plan"
    assert not list((repo / ".agi" / "sessions").glob("*.json")), \
        "--dry-run must leave the sessions dir clean of JSON"


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

# --------------------------------------------------------------------------
# I-3a-2 Region A — the v3 TOWN-FIRST plan (hypothesis:l4-the-reshuffle-
# plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-
# lands-inert). These fixture proofs cover kinds main/towns/posts planning:
# the TOWN SET source (town:* nodes vs ladder fallback), every planned town
# name == branches.derive_names(...) output, the trunk-pair CREATE + the
# assert_remote_visible-first push lines, the local-only v3 post renames,
# --dry-run writing nothing, and the --plan-out semantics. No apply, no
# delete, no live tree.
# --------------------------------------------------------------------------

_FALLBACK_TOWNS = [("core", 2), ("streaming-suite", 1), ("web-app-suite", 1)]


def _v3_repo(tmp_path: Path, with_town_nodes: bool) -> Path:
    """Real git repo with a bare origin carrying the live-ish head set and a
    graph root that either HAS a town:* node (town_tuples path) or does not
    (ladder fallback path)."""
    r = tmp_path / "repo"
    r.mkdir()
    bare = tmp_path / "origin.git"
    bare.mkdir()
    _git(bare, "init", "-q", "--bare")
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@t")
    _git(r, "config", "user.name", "t")
    _write(r, "README", "hi\n")
    _write(r, ".gitignore", ".agi/sessions/\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "seed")
    _git(r, "remote", "add", "origin", str(bare))
    for name in ["season2/main",
                 "season2/streaming-suite/season1/main",
                 "season2/web-app-suite/season1/main",
                 "season2/posts/sanctuary-director",
                 "season2/posts/sanctuary-helper"]:
        _git(r, "branch", name)
        _git(r, "push", "-q", "origin", f"master:refs/heads/{name}")
    _git(r, "fetch", "-q", "origin")
    agi = r / ".agi"
    # loot ladder: current_season + the towns: list the FALLBACK path reads
    _write(r, ".agi/nodes/.geometry/ladder.md",
           "---\ncurrent_season: 2\ntowns: [core, streaming-suite, "
           "web-app-suite]\n---\n")
    if with_town_nodes:
        # L4.338: the loader refuses a dangling vision id by name, so the
        # fixture's towns need their vision NODES or the town set silently
        # falls back to the ladder (director fix at the L4.339 harvest).
        for town, _ts in _FALLBACK_TOWNS:
            _write(r, f".agi/nodes/vision/{town}.md",
                   f"---\nid: vision:{town}\ntype: vision\ntitle: {town}\n---\n")
        _write(r, ".agi/nodes/.geometry/posts.md",
               "---\nposts:\n  - name: core\n  - name: streaming-suite\n"
               "  - name: web-app-suite\n---\n")
        for town, season in _FALLBACK_TOWNS:
            _write(r, f".agi/nodes/town/{town}.md",
                   f"---\nid: town:{town}\ntype: town\nvisions: "
                   f"[vision:{town}]\ncouncil: {town}\nseason: "
                   f"{season}\n---\n")
    return r


def _v3_plan_stdout(root: Path, kinds: str) -> str:
    res = _run_cli(root, "--dry-run", "--kinds", kinds)
    assert res.returncode == 0, res.stdout + res.stderr
    return res.stdout


def test_v3_town_set_uses_town_nodes_when_present(tmp_path: Path):
    r = _v3_repo(tmp_path, with_town_nodes=True)
    out = _v3_plan_stdout(r / ".agi", "towns")
    assert "town set: town:* nodes (3 towns)" in out, out


def test_v3_town_set_falls_back_to_ladder_without_town_nodes(tmp_path: Path):
    r = _v3_repo(tmp_path, with_town_nodes=False)
    out = _v3_plan_stdout(r / ".agi", "towns")
    assert "town set: ladder fallback (3 towns; no town:* node)" in out, out


def test_v3_planned_town_names_equal_derive_names_output(tmp_path: Path):
    r = _v3_repo(tmp_path, with_town_nodes=True)
    sys.path.insert(0, str(BIN))
    import branches  # noqa: E402
    out = _v3_plan_stdout(r / ".agi", "towns")
    for town, season in _FALLBACK_TOWNS:
        d = branches.derive_names(town, season)
        for target in (d["town_main"], d["town_season_main"]):
            assert f"git branch {target} " in out, (target, out)
            assert f"git push -u origin {target}" in out, (target, out)
    # the trunk pair per level is remote-visible: every push line names one
    for ln in out.splitlines():
        if "git push -u origin " in ln:
            name = ln.split("git push -u origin ", 1)[1].strip()
            assert branches.is_remote_visible(name), \
                f"planned push of a NON-remote-visible name: {name!r}"


def test_v3_planned_post_renames_are_local_and_derive_names_targets(
        tmp_path: Path):
    r = _v3_repo(tmp_path, with_town_nodes=True)
    sys.path.insert(0, str(BIN))
    import branches  # noqa: E402
    out = _v3_plan_stdout(r / ".agi", "posts")
    for p in ["sanctuary-director", "sanctuary-helper"]:
        target = branches.derive_names("core", 2, p)["post_main"]
        # the plan names the v3 rename target derived from the same tuple
        assert f"git branch -m season2/posts/{p} {target}" in out, (p, out)
        # local-only: NO push of the post name, and its upstream is UNSET
        assert f"git push -u origin {target}" not in out, out
        assert f"git branch --unset-upstream {target}" in out, out
    # a --kinds posts plan has NO push lines at all (posts are not
    # remote-visible; the trunk-pair push belongs to kinds towns)
    assert "git push " not in out, out


def test_v3_main_kind_keep_line(tmp_path: Path):
    r = _v3_repo(tmp_path, with_town_nodes=False)
    out = _v3_plan_stdout(r / ".agi", "main")
    assert "v3 main: season<n>/main stays (remote-visible); master " \
           "add-only, kept (frozen season-1 name)" in out, out


def test_v3_dry_run_writes_nothing_and_plan_out_is_explicit(tmp_path: Path):
    r = _v3_repo(tmp_path, with_town_nodes=True)
    root = r / ".agi"
    sessions = root / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    default_plan = sessions / "branch-reshuffle-plan.json"

    # plain --dry-run: no plan file anywhere
    _v3_plan_stdout(root, "towns")
    assert not default_plan.exists(), "dry-run must not write the plan"
    assert not [p for p in sessions.glob("*.json") if p.name], \
        "dry-run must leave the sessions dir free of plan JSON"

    # --plan-out writes EXACTLY that file and nothing else
    out_path = root / "sessions" / "explicit-plan.json"
    res = _run_cli(root, "--dry-run", "--kinds", "towns", "--plan-out",
                   str(out_path))
    assert res.returncode == 0, res.stderr
    assert out_path.exists(), "--plan-out must write the named file"
    assert not default_plan.exists(), \
        "--plan-out must not ALSO write the default plan path"


# --------------------------------------------------------------------------
# I-3a-2 Region A — the v3 APPLY (the target node's PROOF: --apply on the
# fixture yields EXACTLY the planned refs, worktree HEADs follow the post
# renames, and the local-only post branches have NO upstream afterwards).
# Runs ONLY against the tmp fixture (never the live tree — no live push, no
# live ref change). --dry-run then --apply with --kinds main,posts,towns:
#   * refs/heads after == before | {trunk-pair creates} | {renamed post
#     mains} MINUS {old post sources} (for-each-ref), and each new trunk
#     points at its planned source tip;
#   * a linked worktree whose HEAD is an old post source is re-pointed onto
#     the renamed post main;
#   * the renamed local post branch has NO upstream (`@ {u}` fails).
# --------------------------------------------------------------------------

def _heads(repo: Path) -> set[str]:
    out = _git(repo, "for-each-ref", "--format=%(refname:short)",
               "refs/heads").stdout
    return {b for b in out.split() if b}


def _v3_apply_repo(tmp_path: Path) -> Path:
    """_v3_repo plus (a) two linked worktrees ON the v3 post SOURCE branches,
    so the apply re-point path is exercised, and (b) the default checkout
    moved OFF master: master is the add-only v2 job whose LOCAL rename target
    (season1/main) is never created, so leaving the default worktree on master
    would make the v2 worktree re-point attempt `git checkout season1/main`
    (a missing branch) and fail the apply."""
    r = _v3_repo(tmp_path, with_town_nodes=True)
    _git(r, "worktree", "add", "-q", str(r / "wt-director"),
         "season2/posts/sanctuary-director")
    _git(r, "worktree", "add", "-q", str(r / "wt-helper"),
         "season2/posts/sanctuary-helper")
    _git(r, "checkout", "-q", "season2/main")
    return r


def test_v3_apply_creates_trunk_pairs_renames_posts_locally_and_repoints(
        tmp_path: Path):
    r = _v3_apply_repo(tmp_path)
    root = r / ".agi"
    sys.path.insert(0, str(BIN))
    import branches  # noqa: E402

    gs = 2  # the fixture's ladder current_season
    # planned NEW refs, derived through the SAME grammar the impl uses
    trunk_pairs: set[str] = set()
    for town, season in _FALLBACK_TOWNS:
        d = branches.derive_names(town, season)
        trunk_pairs.add(d["town_main"])
        trunk_pairs.add(d["town_season_main"])
    post_renames = {
        old: branches.derive_names("core", gs, p)["post_main"]
        for old, p in [("season2/posts/sanctuary-director",
                        "sanctuary-director"),
                       ("season2/posts/sanctuary-helper", "sanctuary-helper")]
    }
    old_posts = set(post_renames)

    before = _heads(r)

    res = _run_cli(root, "--apply", "--kinds", "main,posts,towns")
    assert res.returncode == 0, res.stdout + res.stderr

    after = _heads(r)
    # EXACTLY the planned set: before + new trunks + renamed post mains,
    # with the old post source names gone
    expected = (before | trunk_pairs | set(post_renames.values())) - old_posts
    assert after == expected, (sorted(after), sorted(expected),
                               res.stdout + res.stderr)

    # each new trunk branch points at its planned source tip
    for town, season in _FALLBACK_TOWNS:
        tip = (f"season{gs}/main" if season == gs
               else f"season{gs}/{town}/season{season}/main")
        d = branches.derive_names(town, season)
        for target in (d["town_main"], d["town_season_main"]):
            got = _git(r, "rev-parse", f"{target}^{{commit}}").stdout.strip()
            want = _git(r, "rev-parse", f"{tip}^{{commit}}").stdout.strip()
            assert got == want, (target, got, want)

    # linked worktree HEADs follow the renamed post main
    wt_dir = _git(r / "wt-director", "branch", "--show-current").stdout.strip()
    assert wt_dir == post_renames["season2/posts/sanctuary-director"], wt_dir
    wt_hlp = _git(r / "wt-helper", "branch", "--show-current").stdout.strip()
    assert wt_hlp == post_renames["season2/posts/sanctuary-helper"], wt_hlp

    # the renamed LOCAL post branch has NO upstream: `@ {u}` must fail
    for old, new in post_renames.items():
        up = _git(r, "rev-parse", "--abbrev-ref", f"{new}@{{u}}")
        assert up.returncode != 0, (new, up.stdout, up.stderr)
        assert "_post_rename" not in up.stdout


# --------------------------------------------------------------------------
# l4-apply-runs-the-v3-tail (claim a): --apply with ZERO legacy rename jobs
# must NOT be bypassed by the zero-legacy early return — the v3 apply tail
# (trunk-pair creates / local post renames) is INDEPENDENT of the v2 renames,
# so an empty legacy list still runs the v3 plan. Only a tmp fixture.
# --------------------------------------------------------------------------

def _v3_zero_legacy_repo(tmp_path: Path) -> Path:
    """_v3_repo (declared town set) with the ONE legacy alias erased: the
    default `master` ref is a season-grammar alias (master -> season1/main),
    so deleting it after moving the checkout leaves ZERO legacy rename jobs —
    exactly the zero-jobs surface claim (a) guards. Every other branch is a
    canonical season name (never an alias)."""
    r = _v3_repo(tmp_path, with_town_nodes=True)
    _git(r, "checkout", "-q", "season2/main")
    _git(r, "branch", "-D", "master")
    return r


def test_v3_apply_zero_legacy_jobs_still_runs_the_v3_tail(tmp_path: Path):
    # claim (a): with jobs == [] under --apply, the zero-legacy early return
    # must still reach the v3 apply tail (rc-honest, dry=False) — the
    # local-only v3 post renames perform even when there is nothing to rename
    # in the v2 legacy stream.
    r = _v3_zero_legacy_repo(tmp_path)
    root = r / ".agi"
    posts = {"season2/posts/sanctuary-director",
             "season2/posts/sanctuary-helper"}
    before = _heads(r)
    assert posts <= before, before
    assert "master" not in before, before  # the zero-jobs premise

    res = _run_cli(root, "--apply", "--kinds", "posts")
    assert res.returncode == 0, res.stdout + res.stderr
    # the zero-jobs notice AND the v3 APPLY tail both appear
    assert "no legacy branches to reshuffle" in res.stdout, res.stdout
    assert "[APPLY] branch rename (local, v3)" in res.stdout, res.stdout
    assert "apply: local renames + worktree re-points done; remote legacy " \
        "branches NOT deleted (see --delete-old)" in res.stdout, res.stdout
    # the local-only v3 post renames ACTUALLY happened (sources gone, v3
    # post_mains present), all on the tmp fixture with its bare origin
    after = _heads(r)
    assert posts.isdisjoint(after), (posts & after, sorted(after))
    for new in ("core/season2/posts/sanctuary-director/main",
                "core/season2/posts/sanctuary-helper/main"):
        assert new in after, (new, sorted(after))
        up = _git(r, "rev-parse", "--abbrev-ref", f"{new}@{{u}}")
        assert up.returncode != 0, (new, up.stdout, up.stderr)  # no upstream


# --------------------------------------------------------------------------
# I-3a-2 Region B — the KIND LOOPS plan (dry-only). A v3 town-first loop
# branch is classified by the EXISTING loop-prune rule over the SAME derived
# post_main: merged (ancestor of the post) -> a would-prune [DRY ] line;
# unmerged -> NOT pruned by name; a legacy loop (loop/...@s<N> or
# season<N>/loops/...) -> HELD BY NAME. --dry-run writes nothing and changes
# no ref, and the loop plan emits NO push line. Only a tmp fixture — never the
# live tree.
# --------------------------------------------------------------------------

def _v3_loops_repo(tmp_path: Path) -> Path:
    """_v3_repo plus a v3 post_main for sanctuary-director, a MERGED v3 loop,
    an UNMERGED v3 loop and two LEGACY loop branches."""
    r = _v3_repo(tmp_path, with_town_nodes=True)
    post_main = "core/season2/posts/sanctuary-director/main"
    base = _git(r, "rev-parse",
                "season2/posts/sanctuary-director^{commit}").stdout.strip()
    _git(r, "branch", post_main, base)

    # MERGED loop: points at the post_main's OWN commit (equal = ancestor, so
    # merge-base --is-ancestor rc 0).
    merged = "core/season2/posts/sanctuary-director/loops/L4.333/a00-m"
    _git(r, "branch", merged, base)

    # UNMERGED loop: a divergent commit NOT an ancestor of post_main.
    _git(r, "checkout", "-q", "-b", "tmp-fork")
    _write(r, "fork.txt", "unmerged\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "fork")
    fork_sha = _git(r, "rev-parse", "HEAD").stdout.strip()
    unmerged = "core/season2/posts/sanctuary-director/loops/L4.333/a00-u"
    _git(r, "branch", unmerged, fork_sha)
    _git(r, "checkout", "-q", "master")

    # LEGACY loops: never a v3 shape (HELD BY NAME).
    _git(r, "branch", "loop/hypothesis-l4-foo@s2", base)
    _git(r, "branch", "season2/loops/hypothesis-l4-bar-a00-zzz", base)
    return r


def test_v3_loops_plan_merged_unmerged_held_by_name(tmp_path: Path):
    r = _v3_loops_repo(tmp_path)
    res = _run_cli(r / ".agi", "--dry-run", "--kinds", "loops")
    assert res.returncode == 0, res.stdout + res.stderr
    out = res.stdout
    merged = "core/season2/posts/sanctuary-director/loops/L4.333/a00-m"
    unmerged = "core/season2/posts/sanctuary-director/loops/L4.333/a00-u"
    post_main = "core/season2/posts/sanctuary-director/main"
    # (a) merged -> would-prune line
    assert f"[DRY ] loop prune: {merged}" in out, out
    # (b) unmerged -> named NOT pruned
    assert f"unmerged: {unmerged} -> NOT pruned: {post_main}" in out, out
    # (c) legacy loops -> HELD BY NAME
    assert "HELD BY NAME: loop/hypothesis-l4-foo@s2" in out, out
    assert "HELD BY NAME: season2/loops/hypothesis-l4-bar-a00-zzz" in out, out
    # the loop plan NEVER pushes or deletes a v3 loop name, and never
    # mutates for real
    assert not any("git push" in ln and name in ln
                   for ln in out.splitlines()
                   for name in (merged, unmerged)), out
    assert "git branch -d" not in out, out
    # the unmerged loop still exists after (dry-run is a plan)
    assert _git(r, "rev-parse", "--verify",
                f"{unmerged}^{{commit}}").returncode == 0, \
        "unmerged loop must survive the dry-run"


def test_v3_loops_dry_run_writes_nothing_changes_no_ref(tmp_path: Path):
    r = _v3_loops_repo(tmp_path)
    root = r / ".agi"
    sessions = root / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    before_refs = _git(r, "for-each-ref").stdout
    res = _run_cli(root, "--dry-run", "--kinds", "main,posts,towns,loops")
    assert res.returncode == 0, res.stdout + res.stderr
    # (d) --dry-run leaves refs byte-identical and the sessions dir plan-free
    after_refs = _git(r, "for-each-ref").stdout
    assert before_refs == after_refs, "dry-run must not change any ref"
    assert not list(sessions.glob("*.json")), \
        "dry-run must not write a plan JSON into the sessions dir"

# --------------------------------------------------------------------------
# I-3a-3 (g15 fix-only) — the LEGACY job stream YIELDS to the v3 plan
# (hypothesis:l4-the-legacy-job-stream-yields-to-the-v3-plan-and-no-push-
# leaves-the-trunk-pair). On a tree with a DECLARED town set the legacy
# season-first renames of loop/post/town aliases are NOT performed: a legacy
# loop is HELD BY NAME exactly once (the v3 loop section), a legacy post/seat
# is folded into the v3 posts LOCAL rename (no push, upstream UNSET), a legacy
# town maps ONLY to the v3 create pair, and only main-kind jobs keep the old
# rename+push — while EVERY push line the planner emits passes
# branches.assert_remote_visible first (a non-remote-visible push is refused
# by name). Each legacy alias source name appears exactly once. --dry-run
# writes nothing. The v2 fixtures above exercise the town-less (v3-OFF) path,
# where the old season-first-only stream stays and the header says the yield
# is inert.
# --------------------------------------------------------------------------

def _v3_yield_repo(tmp_path: Path) -> Path:
    """_v3_repo (a DECLARED town set + canonical season2/main + season2/posts
    + town mains) PLUS legacy alias branches the v2 stream would season-first-
    rename: a legacy loop, a legacy post/seat alias, and a legacy town alias,
    each pushed + tracked so they resolve to reshuffle jobs. Only main-kind
    job is `master -> season1/main` (the init default branch), kept add-only."""
    r = _v3_repo(tmp_path, with_town_nodes=True)
    for name in ("loop/legacy-report-a00-x@s2",
                 "seat/legacy-post@s2",
                 "town/streaming-suite@s2"):
        _git(r, "branch", name)
        _git(r, "push", "-q", "origin", name)
    _git(r, "fetch", "-q", "origin")
    for name in ("loop/legacy-report-a00-x@s2",
                 "seat/legacy-post@s2",
                 "town/streaming-suite@s2"):
        _git(r, "branch", "--set-upstream-to", f"origin/{name}", name)
    return r


def _push_targets(out: str) -> list[str]:
    """The handled push targets named by `branch push (new)` lines (the v3
    `-u origin <new>` form and the plain `origin <new>` form; master's
    `origin <old>:<new>` yields its post-colon target)."""
    targets = []
    for ln in out.splitlines():
        if "branch push (new)" not in ln or "git push" not in ln:
            continue
        _, cmd = ln.split("branch push (new):", 1)
        parts = cmd.split()
        tok = parts[-1] if parts and parts[-1] != "-u" else None
        if tok:
            targets.append(tok.split(":", 1)[-1])
        elif len(parts) >= 3 and parts[-1] == "-u":
            # unreachable: a `-u` line always carries the ref after origin
            continue
    return targets


def test_v3_yield_routes_legacy_stream_by_kind(tmp_path: Path):
    r = _v3_yield_repo(tmp_path)
    res = _run_cli(r / ".agi", "--dry-run", "--kinds", "main,posts,towns,loops")
    assert res.returncode == 0, res.stdout + res.stderr
    out = res.stdout
    sys.path.insert(0, str(BIN))
    import branches  # noqa: E402
    # the legacy loop / post / town aliases are NOT season-first-renamed (the
    # v2 FULL command is absent), and no season2/loops or season2/posts name
    # is pushed
    assert "git branch -m loop/legacy-report-a00-x@s2 " \
        "season2/loops/legacy-report-a00-x" not in out, out
    assert "git push origin season2/loops/" not in out, out
    assert "git branch -m seat/legacy-post@s2 season2/posts/legacy-post" \
        not in out, out
    assert "git push origin season2/posts/" not in out, out
    assert "git branch -m town/streaming-suite@s2 " \
        "season2/streaming-suite/season1/main" not in out, out
    # the legacy loop is HELD BY NAME exactly once (the v3 loop section)
    assert out.count("HELD BY NAME: loop/legacy-report-a00-x@s2") == 1, out
    # the legacy post/seat alias was folded into the v3 posts LOCAL rename:
    # upstream unset, and its derived post_main is never pushed
    assert "git branch --unset-upstream " \
           "core/season2/posts/legacy-post/main" in out, out
    assert "git push -u origin core/season2/posts/legacy-post/main" not in out, out
    # the legacy town alias maps ONLY to the v3 create pair (routing note)
    assert "legacy town town/streaming-suite@s2" in out, out
    assert "git branch town/streaming-suite@s2" not in out, out
    # EVERY push target the planner emits is remote-visible
    targets = _push_targets(out)
    assert targets, "a full-kinds plan must plan at least one push: " + out
    for t in targets:
        assert branches.is_remote_visible(t), (t, out)


def test_v3_yield_each_legacy_branch_named_exactly_once(tmp_path: Path):
    r = _v3_yield_repo(tmp_path)
    res = _run_cli(r / ".agi", "--dry-run", "--kinds", "main,posts,towns,loops")
    assert res.returncode == 0, res.stdout + res.stderr
    out = res.stdout
    # loop in its HELD line, post in its v3 rename, town in its routing note —
    # never in two sections and never both renamed and held
    for src in ("loop/legacy-report-a00-x@s2",
                "seat/legacy-post@s2",
                "town/streaming-suite@s2"):
        assert out.count(src) == 1, (src, out)


def test_v3_yield_header_declares_active_and_dry_run_writes_nothing(
        tmp_path: Path):
    r = _v3_yield_repo(tmp_path)
    root = r / ".agi"
    before = _snapshot(r)
    res = _run_cli(root, "--dry-run", "--kinds", "main,posts,towns,loops")
    assert res.returncode == 0, res.stdout + res.stderr
    out = res.stdout
    assert "v3 YIELD active (declared town set)" in out, out
    after = _snapshot(r)
    assert before == after, "the yield dry-run must change no ref and write nothing"
    assert not list((root / "sessions").glob("*.json")), \
        "--dry-run must not write the plan JSON"


# --------------------------------------------------------------------------
# I-3a-3 coherence (g15 fix-only) — the post/seat COALESCE collision. A
# legacy `post/<p>@s<N>` and `seat/<p>@s<N>` BOTH canonically season-first
# rename to the SAME `season<N>/posts/<p>`, so when a canonical branch of
# that name already exists (the normal post-rename state — the v3 post
# rename section already renames `season<N>/posts/<p> -> <post_main>` and
# the fold-in dedupes the aliases away), BOTH aliases fold to NOTHING and
# vanish from the plan — a coherence hole. The fix: a post-kind job whose
# target is already owned is a DEPRECATED DUPLICATE, named BY NAME in a
# routing line (left to --delete-old), never renamed onto the owned target
# (two refs -> one name) and never pushed. This fixture reproduces the
# real-tree shape: a canonical `season2/posts/legacy-post` PLUS a post and a
# seat alias that both collide onto it.
# --------------------------------------------------------------------------

def _v3_yield_collision_repo(tmp_path: Path) -> Path:
    """_v3_repo (declared town set + remote names) PLUS a canonical post
    source with BOTH colliding legacy aliases: post/<p>@s2 AND seat/<p>@s2,
    each pushed + tracked so they resolve to reshuffle jobs. The canonical
    season2/posts/legacy-post owns the post_main target, so neither alias
    can fold into the v3 rename — each is a deprecated duplicate."""
    r = _v3_repo(tmp_path, with_town_nodes=True)
    for name in ("season2/posts/legacy-post",
                 "post/legacy-post@s2", "seat/legacy-post@s2"):
        _git(r, "branch", name)
        _git(r, "push", "-q", "origin", name)
    _git(r, "fetch", "-q", "origin")
    for name in ("post/legacy-post@s2", "seat/legacy-post@s2"):
        _git(r, "branch", "--set-upstream-to", f"origin/{name}", name)
    return r


def _v3_cli_jobs(repo: Path) -> list[dict]:
    """The SAME job set the CLI plans from (in-process, read-only)."""
    sys.path.insert(0, str(BIN))
    import cli  # noqa: E402  (same-dir module, like the other branches imports)
    return cli._reshuffle_jobs(repo, 0)


def test_v3_yield_every_job_old_named_at_least_once(tmp_path: Path):
    """The coherence hole as a count over ALL jobs, not a sample: every
    legacy job old-name must be NAMED somewhere in the dry-run plan (a
    vanished alias is a hole). Uses the collision fixture so the post/seat
    coalesce case is exercised. At-least-once, not literal-exactly-once:
    `master` also appears in the v3 main-keep notice prose and a town alias's
    name can repeat inside the ladder/rotations cell re-spelling proposals
    — extra PROSE occurrences are not a second fate, so the assertion is the
    strong one that matters: no job may be ABSENT."""
    r = _v3_yield_collision_repo(tmp_path)
    res = _run_cli(r / ".agi", "--dry-run", "--kinds", "main,posts,towns,loops")
    assert res.returncode == 0, res.stdout + res.stderr
    out = res.stdout
    missing = [j["old"] for j in _v3_cli_jobs(r) if out.count(j["old"]) == 0]
    assert not missing, f"legacy jobs never named in the plan: {missing}"


def test_v3_yield_colliding_post_seat_aliases_named_duplicate_each(
        tmp_path: Path):
    """The exact hole's fix: BOTH colliding aliases (post/x@s2 and seat/x@s2
    onto the SAME canonical) appear EXACTLY once, as a named deprecated
    duplicate left to --delete-old; the canonical is the ONE that renames to
    the derived post_main; no alias is renamed (two refs would collide onto
    one target) and no post/seat alias is pushed."""
    r = _v3_yield_collision_repo(tmp_path)
    res = _run_cli(r / ".agi", "--dry-run", "--kinds", "main,posts,towns,loops")
    assert res.returncode == 0, res.stdout + res.stderr
    out = res.stdout
    for src in ("post/legacy-post@s2", "seat/legacy-post@s2"):
        # each appears exactly once, in ITS OWN routing line
        assert out.count(src) == 1, (src, out)
        assert f"legacy post {src} -> duplicate of " \
               "season2/posts/legacy-post; left to --delete-old" in out, \
            (src, out)
        # never renamed onto the owned target (two refs -> one name)
        assert f"git branch -m {src} " not in out, (src, out)
        assert f"git push origin {src}" not in out, (src, out)
    # the canonical source is the ONE branch that renames to the post_main
    target = "core/season2/posts/legacy-post/main"
    assert f"git branch -m season2/posts/legacy-post {target}" in out, out
    # the derived post_main is never pushed
    assert f"git push -u origin {target}" not in out, out
