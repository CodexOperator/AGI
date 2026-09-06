"""Tests for the git-commit guard (hypothesis:l2-agent-git-commit-guard).

Three layers tested:
1. The pre-commit hook rejects git commit when AGI_TIER=kid|parent
2. The pre-push hook rejects git push when AGI_TIER=kid|parent
3. dispatch.py populates spawn_env with AGI_TIER + GIT_CONFIG for kid/parent
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
    so git finds it without GIT_CONFIG trickery."""
    hook_dir = repo / ".git" / "hooks"
    hook_dir.mkdir(parents=True, exist_ok=True)
    src = HOOKS / hook_name
    dst = hook_dir / hook_name
    dst.write_text(src.read_text())
    dst.chmod(0o755)
    return dst


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
        env={**os.environ, "AGI_TIER": ""},
    )
    assert result.returncode == 0, f"hook rejected human commit: {result.stderr}"


def test_pre_commit_rejects_kid(temp_repo: Path):
    """A commit with AGI_TIER=kid must be rejected."""
    with_hook(temp_repo)
    (temp_repo / "file3.md").write_text("kid change")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "kid commit"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**os.environ, "AGI_TIER": "kid"},
    )
    assert result.returncode == 1, f"hook allowed kid commit: {result.stdout}"
    assert "kid may not commit" in result.stderr


def test_pre_commit_rejects_parent(temp_repo: Path):
    """A commit with AGI_TIER=parent must be rejected."""
    with_hook(temp_repo)
    (temp_repo / "file4.md").write_text("parent change")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "parent commit"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**os.environ, "AGI_TIER": "parent"},
    )
    assert result.returncode == 1, f"hook allowed parent commit: {result.stdout}"
    assert "parent may not commit" in result.stderr


def test_pre_push_script_rejects_kid():
    """The pre-push hook script itself exits 1 for AGI_TIER=kid."""
    pre_push = HOOKS / "pre-push"
    assert pre_push.exists()
    result = subprocess.run(
        ["bash", str(pre_push)],
        capture_output=True, text=True,
        env={**os.environ, "AGI_TIER": "kid"},
    )
    assert result.returncode == 1
    assert "kid may not push" in result.stderr


def test_pre_push_script_allows_human():
    """The pre-push hook script exits 0 when no AGI_TIER is set."""
    pre_push = HOOKS / "pre-push"
    result = subprocess.run(
        ["bash", str(pre_push)],
        capture_output=True, text=True,
        env={**os.environ, "AGI_TIER": ""},
    )
    assert result.returncode == 0
    assert result.stderr == ''


def test_git_read_commands_work_despite_hook(temp_repo: Path):
    """`git status`, `git diff`, `git log` must succeed under AGI_TIER=kid."""
    with_hook(temp_repo)
    (temp_repo / "file_status.md").write_text("staged change")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    # git status — no hook involved but verify environment isn't broken
    result = subprocess.run(
        ["git", "status"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**os.environ, "AGI_TIER": "kid"},
    )
    assert result.returncode == 0, f"git status failed under AGI_TIER=kid: {result.stderr}"
    assert "file_status.md" in result.stdout

    # git diff --cached
    result = subprocess.run(
        ["git", "diff", "--cached"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**os.environ, "AGI_TIER": "kid"},
    )
    assert result.returncode == 0, f"git diff failed under AGI_TIER=kid: {result.stderr}"

    # git log
    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        cwd=temp_repo, capture_output=True, text=True,
        env={**os.environ, "AGI_TIER": "kid"},
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
        env={**os.environ, "AGI_TIER": ""},
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
    module = _load_dispatch()
    # We can't easily call main() without a full project, but we can verify
    # the env-var injection pattern by inspecting the source.
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


# ---------------------------------------------------------------------------
# Test the GIT_CONFIG mechanism end-to-end (belt's actual effect)
# ---------------------------------------------------------------------------

def test_git_config_hooks_path_rejects_commit(temp_repo: Path):
    """When GIT_CONFIG_COUNT=1 + GIT_CONFIG_KEY_0=core.hooksPath points
    at agent-git/, a git commit under AGI_TIER=kid must fail."""
    (temp_repo / "file_gitcfg.md").write_text("git config test")
    subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True)
    env = {
        **os.environ,
        "AGI_TIER": "kid",
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_dispatch():
    spec = importlib.util.spec_from_file_location("agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module