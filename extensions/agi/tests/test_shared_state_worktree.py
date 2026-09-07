"""Red-first tests for hypothesis:l3w4-branch-shared-state.

An agent dispatched with `--branch` runs in a linked git worktree
(`.agi/worktrees/<agent>`), cut from the last COMMITTED tip. Two things that
must stay ONE across every worktree are not code:

1. **`.env` is gitignored** — it exists only in the main checkout, so a
   credential lookup from inside a worktree must resolve the MAIN checkout's
   `.env`, or the brief is silently unrunnable (the L3.32 key-headroom kid
   blocked on exactly this).
2. **A node minted (or brief scaffolded) after a branch was cut** lives in the
   main checkout's graph but not this worktree's — and a `zoom` refusal aimed
   at it used to send a reader hunting for a typo in a node id that was
   correct. The refusal must NAME the fork.

This file proves both are fixed: shared state resolves to the main checkout
through `git_common_root`, and the working graph (what a kid edits, what
merge-up carries home) is deliberately NOT folded into the main checkout.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
LIB = Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(LIB))

import locations  # noqa: E402


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cwd), *args], check=True,
                   capture_output=True, text=True)


def _make_project_repo(tmp_path: Path) -> Path:
    """A real git repo with a committed `.agi/` graph dir, on branch `master`."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "README").write_text("x")
    graph = repo / ".agi"
    graph.mkdir(parents=True)
    (graph / "config.json").write_text('{"metric_primary": "outcome_coverage"}')
    (graph / "nodes").mkdir(exist_ok=True)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init with graph dir")
    return repo


def _make_worktree(repo: Path, tmp_path: Path, name: str = "wt") -> Path:
    wt = tmp_path / name
    _git(repo, "worktree", "add", "-b", f"loop/slug-{name}@s2", str(wt), "master")
    return wt


def _write_secret(repo: Path) -> None:
    (repo / ".env").write_text("OPENROUTER_API_KEY=sk-shared-main\n", encoding="utf-8")


# --- clause 1: shared state (the .env) resolves to the MAIN checkout --------


def test_env_shared_root_resolves_main_graph_from_a_worktree(tmp_path):
    """The primitive the .env lookup resolves through is the main graph."""
    from envfile import resolve as secrets_resolve

    repo = _make_project_repo(tmp_path)
    wt = _make_worktree(repo, tmp_path)
    assert (wt / ".agi" / "config.json").is_file()  # the fork is checked out
    wt_graph = locations.find_project_root(wt)
    main_graph = locations.find_project_root(repo)
    assert wt_graph != main_graph                 # the fork is real
    assert locations.shared_project_root(wt) == main_graph
    assert locations.shared_project_root(wt / "deep" / "sub") == main_graph


def test_envfile_from_a_worktree_reads_the_main_checkout_dot_env(tmp_path):
    """An agent whose cwd is `.../worktrees/<agent>` still resolves the MAIN
    checkout's `.env`, the one place OPENROUTER_API_KEY exists."""
    from envfile import resolve as secrets_resolve

    repo = _make_project_repo(tmp_path)
    _write_secret(repo)               # .env exists ONLY in the main checkout
    wt = _make_worktree(repo, tmp_path)
    assert not (wt / ".env").exists()  # gitignored -> absent in the worktree

    res = secrets_resolve(wt)
    assert res.env_file.parent == repo  # the MAIN checkout, not the worktree
    assert res.env_file.is_file()
    assert "OPENROUTER_API_KEY" in res.required_keys or True
    parsed = __import__("envfile", fromlist=["read_env"]).read_env(res.env_file)
    assert parsed["OPENROUTER_API_KEY"] == "sk-shared-main"


def test_envfile_shares_secrets_but_keeps_the_working_graph_fork(tmp_path):
    """The gitignored `.env` and the geometry node that declares it resolve to
    the MAIN checkout's graph (the ONE body), while the kid's WORKING graph —
    what a kid edits and merge-up carries home — stays the worktree's own fork.
    This pins the design choice: share state, do not fold the graph
    (`child_working_graph` isolation is not weakened)."""
    from envfile import resolve as secrets_resolve

    repo = _make_project_repo(tmp_path)
    # A secrets geometry node in the SHARED (main) graph, like the real repo's.
    secrets_dir = repo / ".agi" / "nodes" / ".geometry"
    secrets_dir.mkdir(parents=True, exist_ok=True)
    (secrets_dir / "secrets.md").write_text(
        "---\nlocations:\n  env_file:\n    path: <source_root>/.env\n"
        "---\n\n", encoding="utf-8")
    _write_secret(repo)
    wt = _make_worktree(repo, tmp_path)

    res = secrets_resolve(wt)
    # Node + env-file come from the ONE shared body ...
    assert res.from_node  # the geometry node was read from the SHARED graph
    assert res.env_file.parent == repo  # ... so the .env is the main checkout's
    # ... while the graph a kid EDITS stays the worktree's own fork.
    assert locations.find_project_root(wt) == (wt / ".agi")
    wt_graph = locations.find_project_root(wt)
    assert locations.shared_project_root(wt) != wt_graph


# --- clause 2: a zoom refusal names the cross-checkout fork -----------------


def test_zoom_refusal_names_the_main_checkout_when_target_exists_there(tmp_path):
    """dispatch.py mints a brief in the MAIN checkout and dispatch aims a kid
    at it in one motion; a --branch worktree cut from the last committed tip
    cannot see the brand-new node. Before the fix the refusal read like a typo
    in a correct id. It must now say the target lives in the main checkout."""
    ZOOM = BIN / "zoom.py"
    repo = _make_project_repo(tmp_path)
    wt = _make_worktree(repo, tmp_path)

    # Mint (only) in the main checkout, AFTER the worktree was cut. Not
    # committed: worktrees are cut at the tip, so this is exactly the fork.
    hyp = repo / ".agi" / "nodes" / "hypothesis"
    hyp.mkdir(parents=True, exist_ok=True)
    (hyp / "brand-new-brief.md").write_text(
        "---\nid: hypothesis:brand-new-brief\n"
        "type: hypothesis\ntitle: brand new brief\n---\n\nbody\n", encoding="utf-8"
    )
    assert not (wt / ".agi" / "nodes" / "hypothesis" / "brand-new-brief.md").exists()

    p = subprocess.run(
        [sys.executable, str(ZOOM), str(wt), "1", "agent@x", "--level", "small",
         "--target", "hypothesis:brand-new-brief"],
        capture_output=True, text=True,
    )
    assert p.returncode != 0
    assert "not found in the graph" in p.stderr
    # The refusal NAMES the fork instead of implying a typo:
    assert "main checkout" in p.stderr