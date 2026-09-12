"""Tests for the git-commit guard (hypothesis:l2-agent-git-commit-guard).

Three layers tested:
1. The pre-commit hook rejects git commit when AGI_TIER=kid|parent IN the project repo
2. The pre-commit hook ALLOWS commits in NON-project repos even under AGI_TIER=kid|parent
3. The pre-push hook follows the same scoped logic
4. dispatch.py populates spawn_env with AGI_TIER + GIT_CONFIG + AGI_PROJECT_ROOT
"""
from __future__ import annotations

import importlib.util
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
HOOKS = BIN.parent / "hooks" / "agent-git"


def hook_env() -> dict:
    """os.environ with the injected git config REPLACED, not merged.

    This environment pins core.hooksPath at the MAIN checkout's hooks dir via
    GIT_CONFIG_COUNT/KEY_0/VALUE_0, which overrides both .git/hooks and any
    local core.hooksPath — so tests would silently exercise a stale hook from
    another worktree instead of the copy under test (review of
    hypothesis:l3-parent-brief-forbids-the-only-commit: the loop-branch allow
    existed in this tree and the test still failed because git was reading the
    main checkout's hook). Point the injected config at HOOKS instead."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_CONFIG_")}
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "core.hooksPath"
    env["GIT_CONFIG_VALUE_0"] = str(HOOKS)
    return env

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("agi_locations", BIN / "locations.py")
_locations = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_locations)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def temp_repo(tmp_path: Path) -> Path:
    """A bare-minimum git repo so hook tests can attempt commits."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, capture_output=True, check=True)
    (repo / "readme.md").write_text("# test")
    subprocess.run(["git", "add", "."], cwd=repo, capture_output=True, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, capture_output=True, check=True)
    return repo


def with_hook(repo: Path, hook_name: str = "pre-commit") -> Path:
    """Install one of the agent-git hooks into the test repo's hooks dir,
    so git finds it without GIT_CONFIG trickery.

    Also points the repo's LOCAL core.hooksPath at the source hooks dir
    under test: a global core.hooksPath (set on this box for the live
    project) overrides .git/hooks entirely, so without this the tests
    silently exercise whichever checkout that global path points at —
    not the copy in this tree (hypothesis:l3-parent-brief-forbids-the-only-commit
    review fix; the loop-branch allow was being tested against the stale hook)."""
    hook_dir = repo / ".git" / "hooks"
    hook_dir.mkdir(parents=True, exist_ok=True)
    src = HOOKS / hook_name
    dst = hook_dir / hook_name
    dst.write_text(src.read_text())
    dst.chmod(0o755)
    subprocess.run(
        ["git", "config", "core.hooksPath", str(HOOKS)],
        cwd=repo, capture_output=True, check=True,
    )
    return dst


def repo_toplevel(repo: Path) -> str:
    """Return the resolved toplevel of a git repo, for AGI_PROJECT_ROOT."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=repo, capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# Hook-level tests (belt)
# ---------------------------------------------------------------------------

def test_pre_commit_allows_human_when_no_tier(temp_repo: Path):
    """A commit with AGI_TIER unset must succeed (human/director)."""
    with_hook(temp_repo)
    (temp_repo / "file2.md").write_text("change")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "human commit"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": ""},
    )
    assert result.returncode == 0, f"hook rejected human commit: {result.stderr}"


def test_pre_commit_rejects_kid_in_project_repo(temp_repo: Path):
    """A commit with AGI_TIER=kid in a repo matching AGI_PROJECT_ROOT must be rejected."""
    with_hook(temp_repo)
    toplevel = repo_toplevel(temp_repo)
    (temp_repo / "file3.md").write_text("kid change")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "kid commit"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid", "AGI_PROJECT_ROOT": toplevel},
    )
    assert result.returncode == 1, f"hook allowed kid commit: {result.stdout}"
    assert "kid may not commit" in result.stderr


@pytest.fixture
def g11_repo(tmp_path: Path) -> Path:
    """A repo in the goal:g11 one-repo layout: the graph root is a `.agi/`
    directory INSIDE the repo, so AGI_PROJECT_ROOT (the graph root) is a child
    of the git toplevel, never equal to it."""
    repo = tempfile.mkdtemp(dir=tmp_path)
    subprocess.run(["git", "init"], cwd=repo, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, capture_output=True, check=True)
    (Path(repo) / "readme.md").write_text("# test")
    subprocess.run(["git", "add", "."], cwd=repo, capture_output=True, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, capture_output=True, check=True)
    # graph root: a .agi dir holding config.json, exactly as dispatch.py sees it
    graph_dir = Path(repo) / ".agi"
    graph_dir.mkdir()
    (graph_dir / "config.json").write_text('{"metric_primary": "x", "metric_unit": "", "best_direction": "higher"}')
    return Path(repo)


def _graph_root(g11_repo: Path) -> Path:
    """The graph root of a g11 repo, asserted through the real resolver so the
    test is tied to locations.find_project_root, not a hard-coded literal."""
    resolved = _locations.find_project_root(g11_repo)
    assert resolved is not None, "resolver did not find the .agi graph root"
    assert resolved == (g11_repo / ".agi").resolve(), (
        f"resolver returned {resolved}, expected {g11_repo}/.agi"
    )
    return resolved


def test_pre_commit_rejects_kid_in_g11_layout(g11_repo: Path):
    """goal:g11 — AGI_PROJECT_ROOT is the GRAPH root (<repo>/.agi), a child of
    the git toplevel. A dispatched kid must be refused. Red on the current hook:
    it compares AGI_PROJECT_ROOT raw against toplevel, they differ, it exits 0."""
    with_hook(g11_repo)
    graph_root = _graph_root(g11_repo)
    (g11_repo / "file_g11.md").write_text("kid change in g11 repo")
    subprocess.run(["git", "add", "."], cwd=g11_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "kid commit in g11 repo"],
        cwd=g11_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid", "AGI_PROJECT_ROOT": str(graph_root)},
    )
    assert result.returncode == 1, (
        f"g11 kid commit allowed: {result.stdout} / {result.stderr}"
    )
    assert "kid may not commit" in result.stderr


def test_pre_push_rejects_kid_in_g11_layout(g11_repo: Path):
    """goal:g11 — the pre-push hook must refuse a kid push when AGI_PROJECT_ROOT
    is the graph root (<repo>/.agi). Red on the current hook (exits 0)."""
    graph_root = _graph_root(g11_repo)
    result = subprocess.run(
        ["bash", str(HOOKS / "pre-push")],
        capture_output=True, text=True,
        cwd=g11_repo,
        env={**hook_env(), "AGI_TIER": "kid", "AGI_PROJECT_ROOT": str(graph_root)},
    )
    assert result.returncode == 1, (
        f"g11 kid push allowed: {result.stdout} / {result.stderr}"
    )
    assert "kid may not push" in result.stderr


def test_pre_commit_allows_kid_in_non_project_repo(temp_repo: Path):
    """A commit with AGI_TIER=kid in a repo NOT matching AGI_PROJECT_ROOT must succeed.

    The guard is scoped to the project repo only — test repos under /tmp
    must be allowed even under AGI_TIER=kid.
    """
    with_hook(temp_repo)
    # AGI_PROJECT_ROOT points to a non-matching directory
    other_root = temp_repo.parent / "other-project"
    other_root.mkdir()
    (temp_repo / "file3.md").write_text("kid change outside project")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "kid commit outside"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid", "AGI_PROJECT_ROOT": str(other_root)},
    )
    assert result.returncode == 0, (
        f"hook rejected kid commit in non-project repo: {result.stderr}"
    )


def test_pre_commit_allows_kid_when_project_root_unset(temp_repo: Path):
    """A commit with AGI_TIER=kid but no AGI_PROJECT_ROOT must succeed.

    When AGI_PROJECT_ROOT is unset the hook cannot scope the guard and
    must allow all commits. This preserves backward compatibility for
    any environment that sets AGI_TIER but not AGI_PROJECT_ROOT.
    """
    with_hook(temp_repo)
    (temp_repo / "file_no_root.md").write_text("no project root")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "kid commit no root"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid"},
    )
    assert result.returncode == 0, (
        f"hook rejected when AGI_PROJECT_ROOT unset: {result.stderr}"
    )


def test_pre_commit_rejects_parent(temp_repo: Path):
    """A commit with AGI_TIER=parent in a repo matching AGI_PROJECT_ROOT must be rejected."""
    with_hook(temp_repo)
    toplevel = repo_toplevel(temp_repo)
    (temp_repo / "file4.md").write_text("parent change")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "parent commit"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "parent", "AGI_PROJECT_ROOT": toplevel},
    )
    assert result.returncode == 1, f"hook allowed parent commit: {result.stdout}"
    assert "parent may not commit" in result.stderr


def test_pre_commit_allows_parent_on_loop_branch(temp_repo: Path):
    """hypothesis:l3-parent-brief-forbids-the-only-commit — the ONE authorised
    parent commit: a --branch parent committing onto its own loop/* branch.
    The loop branch is the only route its kids' work has to the season branch;
    a branch left at base merges as nothing and reports green (L3.39 loss). So
    the guard must permit exactly this parent commit and no other.

    Red on the pre-change hook: it refused every parent commit in the project
    repo regardless of branch, so the brief's authorisation would have been
    theatre."""
    with_hook(temp_repo)
    toplevel = repo_toplevel(temp_repo)
    subprocess.run(["git", "checkout", "-b", "loop/slug-a00-x@s2"],
                   cwd=temp_repo, capture_output=True, check=True)
    (temp_repo / "file_loop.md").write_text("parent loop-branch commit")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "loop: loop/slug-a00-x@s2 -- accepted kid:n"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "parent", "AGI_PROJECT_ROOT": toplevel},
    )
    assert result.returncode == 0, (
        f"hook blocked the one authorised parent commit: {result.stdout} / {result.stderr}"
    )


def test_pre_commit_still_rejects_parent_on_loop_branch_in_wrong_repo(temp_repo: Path):
    """The loop/* allowance is scoped to the PROJECT repo. A parent on a
    loop/* branch in a repo that is NOT AGI_PROJECT_ROOT must still be allowed
    (non-project repos pass the scope check and exit 0 regardless of tier) --
    this pins that the branch allowance never weakens the OUTSIDE-project rule."""
    with_hook(temp_repo)
    other_root = temp_repo.parent / "other-project"
    other_root.mkdir()
    subprocess.run(["git", "checkout", "-b", "loop/slug-a00-x@s2"],
                   cwd=temp_repo, capture_output=True, check=True)
    (temp_repo / "file_loop2.md").write_text("change")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "parent commit outside"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "parent", "AGI_PROJECT_ROOT": str(other_root)},
    )
    assert result.returncode == 0, (
        f"hook blocked parent commit in non-project repo: {result.stderr}"
    )


def test_pre_commit_allows_parent_on_canonical_loop_branch(temp_repo: Path):
    """hypothesis:l4-branches-follow-the-season-grammar — dispatch.py now
    emits the CANONICAL loop branch name through branches.loop_branch(), i.e.
    season<n>/loops/<slug>-<agent>, not the legacy loop/<slug>-<agent>@s<n>.
    The ONE authorised parent commit must be allowed on the canonical name too
    — red on the pre-fix hook, whose case pattern only matched `loop/*`."""
    with_hook(temp_repo)
    toplevel = repo_toplevel(temp_repo)
    subprocess.run(["git", "checkout", "-b", "season2/loops/slug-a00-x"],
                   cwd=temp_repo, capture_output=True, check=True)
    (temp_repo / "file_canonical_loop.md").write_text("parent canonical loop commit")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "loop: season2/loops/slug-a00-x -- accepted kid:n"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "parent", "AGI_PROJECT_ROOT": toplevel},
    )
    assert result.returncode == 0, (
        f"hook blocked the authorised parent commit on canonical loop branch: "
        f"{result.stdout} / {result.stderr}"
    )


def test_pre_commit_still_rejects_kid_on_loop_branch(g11_repo: Path):
    """The loop/* allowance is for PARENT only. A KID on a loop/* branch in
    the project repo stays blocked -- kids commit nothing, ever."""
    with_hook(g11_repo)
    graph_root = _graph_root(g11_repo)
    subprocess.run(["git", "checkout", "-b", "loop/slug-a00-y@s2"],
                   cwd=g11_repo, capture_output=True, check=True)
    (g11_repo / "file_kid_loop.md").write_text("kid change on loop branch")
    subprocess.run(["git", "add", "."], cwd=g11_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "kid loop commit"],
        cwd=g11_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid", "AGI_PROJECT_ROOT": str(graph_root)},
    )
    assert result.returncode == 1, (
        f"hook allowed kid commit on loop branch: {result.stdout}"
    )
    assert "kid may not commit" in result.stderr


def test_pre_push_script_rejects_kid_in_project_repo(temp_repo: Path):
    """The pre-push hook script exits 1 for AGI_TIER=kid in the project repo."""
    toplevel = repo_toplevel(temp_repo)
    pre_push = HOOKS / "pre-push"
    assert pre_push.exists()
    result = subprocess.run(
        ["bash", str(pre_push)],
        capture_output=True, text=True,
        cwd=temp_repo,
        env={**hook_env(), "AGI_TIER": "kid", "AGI_PROJECT_ROOT": toplevel},
    )
    assert result.returncode == 1
    assert "kid may not push" in result.stderr


def test_pre_push_script_allows_kid_in_non_project_repo(temp_repo: Path):
    """The pre-push hook allows pushes for AGI_TIER=kid in a non-project repo."""
    other_root = temp_repo.parent / "other-project"
    other_root.mkdir()
    pre_push = HOOKS / "pre-push"
    result = subprocess.run(
        ["bash", str(pre_push)],
        capture_output=True, text=True,
        cwd=temp_repo,
        env={**hook_env(), "AGI_TIER": "kid", "AGI_PROJECT_ROOT": str(other_root)},
    )
    assert result.returncode == 0
    # When hook allows, stderr is empty (no message)
    assert result.stderr.strip() == '' or 'may not push' not in result.stderr


def test_pre_push_script_allows_human():
    """The pre-push hook script exits 0 when AGI_TIER is unset."""
    pre_push = HOOKS / "pre-push"
    result = subprocess.run(
        ["bash", str(pre_push)],
        capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": ""},
    )
    assert result.returncode == 0
    assert result.stderr.strip() == ''


def test_git_read_commands_work_despite_hook(temp_repo: Path):
    """`git status`, `git diff`, `git log` must succeed under AGI_TIER=kid."""
    with_hook(temp_repo)
    (temp_repo / "file_status.md").write_text("staged change")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    # git status — no hook involved but verify environment isn't broken
    result = subprocess.run(
        ["git", "status"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid"},
    )
    assert result.returncode == 0, f"git status failed under AGI_TIER=kid: {result.stderr}"
    assert "file_status.md" in result.stdout

    # git diff --cached
    result = subprocess.run(
        ["git", "diff", "--cached"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid"},
    )
    assert result.returncode == 0, f"git diff failed under AGI_TIER=kid: {result.stderr}"

    # git log
    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid"},
    )
    assert result.returncode == 0, f"git log failed under AGI_TIER=kid: {result.stderr}"


def test_hook_exits_zero_for_human_on_pre_push(temp_repo: Path):
    """No AGI_TIER set → pre-push should allow the push.

    Git push fails because no remote, but the hook must not be the reason.
    If the hook exits 0, git proceeds to push and fails with 'no remote'.
    """
    with_hook(temp_repo, "pre-push")
    result = subprocess.run(
        ["git", "push", "origin", "master"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": ""},
    )
    combined = result.stdout + result.stderr
    assert "may not push" not in combined, (
        f"hook rejected human push: {combined}"
    )


# ---------------------------------------------------------------------------
# GIT_CONFIG env-var injection tests (belt's activation mechanism)
# ---------------------------------------------------------------------------

def test_spawn_env_contains_AGI_TIER():
    """dispatch.py sets AGI_TIER in spawn_env for every tier."""
    src = (BIN / "dispatch.py").read_text()
    assert 'spawn_env["AGI_TIER"] = args.tier' in src, (
        "AGI_TIER injection missing from dispatch.py"
    )


def test_spawn_env_contains_GIT_CONFIG_for_kid():
    """dispatch.py must set GIT_CONFIG_COUNT and related vars for kid tier."""
    src = (BIN / "dispatch.py").read_text()
    assert 'spawn_env["GIT_CONFIG_COUNT"] = "1"' in src
    assert 'spawn_env["GIT_CONFIG_KEY_0"] = "core.hooksPath"' in src
    assert "agent-git" in src


def test_spawn_env_contains_AGI_PROJECT_ROOT_for_kid():
    """dispatch.py must set AGI_PROJECT_ROOT for kid tier to scope the guard."""
    src = (BIN / "dispatch.py").read_text()
    assert 'spawn_env["AGI_PROJECT_ROOT"]' in src, (
        "AGI_PROJECT_ROOT injection missing from dispatch.py"
    )
    # Find the line with spawn_env["AGI_PROJECT_ROOT"] and verify it resolves
    for line in src.splitlines():
        if 'spawn_env["AGI_PROJECT_ROOT"]' in line:
            assert "root.resolve" in line, (
                "AGI_PROJECT_ROOT should use .resolve() for a canonical path"
            )
            break
    else:
        pytest.fail("No line sets spawn_env[AGI_PROJECT_ROOT]")


# ---------------------------------------------------------------------------
# Test the GIT_CONFIG mechanism end-to-end (belt's actual effect)
# ---------------------------------------------------------------------------

def test_git_config_hooks_path_rejects_commit_in_project(temp_repo: Path):
    """When GIT_CONFIG+Hooks point at agent-git/ and AGI_PROJECT_ROOT matches,
    a git commit under AGI_TIER=kid must fail."""
    toplevel = repo_toplevel(temp_repo)
    (temp_repo / "file_gitcfg.md").write_text("git config test")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    env = {
        **hook_env(),
        "AGI_TIER": "kid",
        "AGI_PROJECT_ROOT": toplevel,
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "core.hooksPath",
        "GIT_CONFIG_VALUE_0": str(HOOKS),
    }
    result = subprocess.run(
        ["git", "commit", "-m", "git config test"],
        cwd=temp_repo, capture_output=True, text=True, env=env,
    )
    assert result.returncode == 1, (
        f"git commit succeeded despite GIT_CONFIG guard: {result.stdout}"
    )
    assert "kid may not commit" in result.stderr


def test_git_config_hooks_path_allows_commit_outside_project(temp_repo: Path):
    """When GIT_CONFIG+Hooks point at agent-git/ but AGI_PROJECT_ROOT does
    NOT match the temp repo's toplevel, a commit under AGI_TIER=kid must
    succeed — the guard is scoped to the project repo only.

    This is the exact scenario that caused 99 test failures before the scoping
    fix: engine tests create temp repos and commit in them, but the hooks
    refused every commit regardless of which repo it was in.
    """
    other_root = temp_repo.parent / "other-project"
    other_root.mkdir()
    (temp_repo / "file_outside.md").write_text("outside project test")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    env = {
        **hook_env(),
        "AGI_TIER": "kid",
        "AGI_PROJECT_ROOT": str(other_root),
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "core.hooksPath",
        "GIT_CONFIG_VALUE_0": str(HOOKS),
    }
    result = subprocess.run(
        ["git", "commit", "-m", "outside project commit"],
        cwd=temp_repo, capture_output=True, text=True, env=env,
    )
    assert result.returncode == 0, (
        f"hook blocked commit outside project repo: {result.stderr}"
    )


# ---------------------------------------------------------------------------
# Two-checkout same-repo tests (hypothesis:l4-commit-guard-worktree-toplevel-bypass)
# ---------------------------------------------------------------------------

def test_pre_commit_rejects_kid_from_main_into_same_repo_other_checkout(tmp_path: Path):
    """hypothesis:l4-commit-guard-worktree-toplevel-bypass — under --branch
    dispatch AGI_PROJECT_ROOT is the kid's OWN WORKTREE. A process whose CWD
    is the MAIN checkout of the SAME repo (two checkouts share one git common
    dir) must be REFUSED, not slipped through by the `different toplevel`
    allow rule. Red on the pre-fix hook: REAL_TOPLEVEL (main) != REAL_PROJECT
    (worktree), so it exited 0 and let a kid commit into the shared main
    checkout — the sweep-up hazard the guard exists to stop."""
    main = tmp_path / "main"
    main.mkdir()
    subprocess.run(["git", "init"], cwd=main, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=main, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=main, capture_output=True, check=True)
    (main / "readme.md").write_text("# main")
    subprocess.run(["git", "add", "."], cwd=main, capture_output=True, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=main, capture_output=True, check=True)
    # second checkout of the SAME repo, exactly what dispatch.py --branch authors
    wt = tmp_path / "wt"
    subprocess.run(["git", "worktree", "add", "-b", "loop/slug-a00-x@s2", str(wt)],
                   cwd=main, capture_output=True, check=True)
    with_hook(main)
    (main / "file_wt.md").write_text("change in main checkout")
    subprocess.run(["git", "add", "."], cwd=main, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "kid commit from main checkout"],
        cwd=main, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid", "AGI_PROJECT_ROOT": str(wt)},
    )
    assert result.returncode == 1, (
        f"kid commit into same-repo other checkout allowed: {result.stdout} / {result.stderr}"
    )
    assert "kid may not commit" in result.stderr
    subprocess.run(["git", "worktree", "remove", "--force", str(wt)],
                   cwd=main, capture_output=True)


def test_pre_push_rejects_kid_from_main_into_same_repo_other_checkout(tmp_path: Path):
    """pre-push mirrors pre-commit: refusing a push whose CWD is a DIFFERENT
    checkout of the same project (shared git-common-dir) even when
    AGI_PROJECT_ROOT points at the dispatched worktree."""
    main = tmp_path / "main"
    main.mkdir()
    subprocess.run(["git", "init"], cwd=main, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=main, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=main, capture_output=True, check=True)
    (main / "readme.md").write_text("# main")
    subprocess.run(["git", "add", "."], cwd=main, capture_output=True, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=main, capture_output=True, check=True)
    wt = tmp_path / "wt"
    subprocess.run(["git", "worktree", "add", "-b", "loop/slug-a00-x@s2", str(wt)],
                   cwd=main, capture_output=True, check=True)
    result = subprocess.run(
        ["bash", str(HOOKS / "pre-push")],
        cwd=main, capture_output=True, text=True,
        env={**hook_env(), "AGI_TIER": "kid", "AGI_PROJECT_ROOT": str(wt)},
    )
    assert result.returncode == 1, (
        f"kid push from same-repo other checkout allowed: {result.stderr}"
    )
    assert "kid may not push" in result.stderr
    subprocess.run(["git", "worktree", "remove", "--force", str(wt)],
                   cwd=main, capture_output=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_dispatch():
    spec = importlib.util.spec_from_file_location("agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module