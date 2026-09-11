"""hypothesis:l4-startup-is-one-script-or-a-driven-prompt — 0b kid 3, the
INJECTION half.

The hook's job (claim 1, verbatim): "the SessionStart hook injects it as one
block when the session is a seat successor — so a successor wakes KNOWING its
state and spends zero tool calls deriving it." Proved on a TEMP HOME fixture:
the `.next` hook copy (cc-session-start.next.sh — NOT the live hook, NOT
~/.claude) is driven the way CC drives it (scrubbed env, cwd = project root),
and asserted for all four gates:
  (a) fresh record  -> the bootstrap block IS emitted, carrying its facts;
  (b) stale record  -> REFUSED, block NOT emitted (stale state is never
                       injected);
  (c) no record     -> silence + exit 0 (a non-seat session is untouched);
  (d) outside a project -> silence + exit 0 (the hook's load-bearing
                       invariant — its global registration is only safe
                       because it prints nothing there).
The live hook cc-session-start.sh and ~/.claude/settings.json are the
PRIME's install step; this test touches neither.
"""
import json
import os
import subprocess
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[3] / "extensions" / "agi"
NEXT_HOOK = PLUGIN / "hooks" / "cc-session-start.next.sh"

BOOTSTRAP_MARKER = "bootstrap: adv-alive successor handover"


def _git(root: Path, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True, text=True)


@pytest.fixture()
def project(tmp_path):
    """A minimal PROJECT that is also a git repo with one committed node, so
    `_git_head` resolves a real HEAD and staleness is provable either way."""
    root = tmp_path / "proj"
    (root / "nodes").mkdir(parents=True)
    (root / "context").mkdir(parents=True)
    (root / "agi-tree.config.json").write_text("{}")
    (root / "nodes" / "n.md").write_text(
        '---\nid: "goal:n"\ntype: goal\n---\n\nbody\n')
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "init")
    # a fresh, extant INJECTION.md so the hook's build-gate passes and only
    # the bootstrap section is under test (inject.py on a bare fixture has
    # no graph to render, so the map would otherwise be absent).
    (root / "context" / "INJECTION.md").write_text(
        "## map\n\nfake map\n", encoding="utf-8")
    return root


def _head(root: Path) -> str:
    out = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True, check=True)
    return out.stdout.strip()


def _write_bootstrap(root: Path, *, seat: str = "adv-alive", **doc) -> Path:
    p = root / "sessions" / "seats" / f"{seat}.bootstrap.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    doc.setdefault("seat", seat)
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def _run_hook(cwd: Path, *, home: Path, seat: str):
    """Drive the .next hook copy the way CC drives the live hook: scrubbed
    env, cwd at the project root, HOME pointed at a TEMP firewalled dir."""
    env = dict(os.environ)
    env.pop("AGI_TREE_PROJECT_ROOT", None)
    env.pop("AUTORESEARCH_TREE_PROJECT_ROOT", None)
    env["HOME"] = str(home)
    env["AGI_SEAT"] = seat
    return subprocess.run(["bash", str(NEXT_HOOK)], cwd=str(cwd),
                          capture_output=True, text=True, env=env)


# (a) a FRESH record -> the block IS emitted, carrying its facts
def test_fresh_record_emits_block_with_facts(project, tmp_path):
    head = _head(project)
    _write_bootstrap(
        project, seat="adv-alive", shape="v1", generation=1,
        commit=head, measured_at={"seed": head, "model": head},
        telemetry={"seed": "s-7", "model": "claude-sonnet-5", "ack": "continue"})
    r = _run_hook(project, home=tmp_path / "home", seat="adv-alive")
    assert r.returncode == 0
    assert BOOTSTRAP_MARKER in r.stdout
    assert "- seed: s-7" in r.stdout
    assert "- model: claude-sonnet-5" in r.stdout
    assert "- ack: continue" in r.stdout
    # it is ONE small, diagram-shaped block — not a dump.
    assert "## ⚓ bootstrap" in r.stdout


# (b) a STALE record -> REFUSED, the block is NOT emitted
def test_stale_record_refused_not_emitted(project, tmp_path):
    head = _head(project)
    _write_bootstrap(
        project, seat="adv-alive", shape="v1", generation=1, commit=head,
        # a fact measured at a commit that is NOT live HEAD => refuse.
        measured_at={"seed": "deadbeef", "model": head},
        telemetry={"seed": "s-7", "model": "claude-sonnet-5"})
    r = _run_hook(project, home=tmp_path / "home", seat="adv-alive")
    assert r.returncode == 0
    assert BOOTSTRAP_MARKER not in r.stdout
    assert "## ⚓ bootstrap" not in r.stdout


# (c) NO record -> silence + exit 0 (a non-seat session is untouched)
def test_no_record_is_silent(project, tmp_path):
    r = _run_hook(project, home=tmp_path / "home", seat="adv-alive")
    assert r.returncode == 0
    assert BOOTSTRAP_MARKER not in r.stdout
    assert "## ⚓ bootstrap" not in r.stdout


# (d) OUTSIDE a project -> silence + exit 0 (the load-bearing invariant)
def test_outside_project_is_silent(tmp_path):
    outside = tmp_path / "not-a-project"
    outside.mkdir()
    (outside / "some.txt").write_text("hi", encoding="utf-8")
    r = _run_hook(outside, home=tmp_path / "home", seat="adv-alive")
    assert r.returncode == 0
    assert r.stdout.strip() == ""
    assert BOOTSTRAP_MARKER not in r.stdout