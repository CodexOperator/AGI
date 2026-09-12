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
