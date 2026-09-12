"""RUNG 4 SLICE 3 -- the untrusted lane itself.

hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts, SLICE 3,
conjunct (2): 'the row's worktree is the only place it may write, dispatch
refuses it as a spawner, the merge-up recipe refuses its branch, and its
per-spawn key cap is the row's budget cell; every refusal names the tier'.

Proves on FIXTURE geometry configs only (never the live tree): each refusal
fires BY NAME for an untrusted row and does NOT fire for a trusted row (the
negative control is the point -- a gate that refuses everyone proves
nothing), and the budget cap is the row's `budget` cell, with a no-budget
untrusted row keeping today's default exactly.

FILE SCOPE (slice-cut): dispatch.py, season.py, provisioning.py -- tested
through their helpers -- plus this test file only. send.py/rings.py/veto.py/
rotate.py/verification.py/cli.py/write.py/brief.py are untouched.
"""

from __future__ import annotations

import json
from pathlib import Path

import dispatch
import season
import provisioning
import geometry_config


def _rows_md(rows, key="posts"):
    body = "\n".join(f"  - {r!r}" for r in rows)
    return (
        f"---\nid: config:{key}\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        f"type: config\nparents:\n  - goal:g17\n{key}:\n{body}\n"
        "---\n\n# config\n\nfixture body\n"
    )


def _project(tmp_path, rows):
    """A tmp project whose posts.md carries the given rows. Returns the
    GRAPH dir (<proj>/.agi) -- the root the dispatch/season/provisioning
    helpers expect, exactly as the live callers pass it."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(
        json.dumps({"metric_primary": "outcome_coverage"}))
    d = root / ".agi" / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    (d / "posts.md").write_text(_rows_md(rows))
    return root / ".agi"


_UNTRUSTED = {"name": "lurker", "tier": "untrusted",
              "worktree": "worktrees/lurker", "budget": 0.4, "harness": "pi"}
_TRUSTED = {"name": "belam", "role": "prime_director", "tier": 3}
_TRUSTED_ROW = {"name": "alice", "role": "director", "tier": 2}
_UNTRUSTED_NO_BUDGET = {"name": "ghost", "tier": "untrusted",
                        "worktree": "worktrees/ghost"}


# --- (a) dispatch refuses an untrusted spawner ----------------------------

def test_dispatch_refuses_untrusted_spawner_by_name(tmp_path):
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    msg = dispatch._refuse_untrusted_spawner(root, "lurker")
    assert msg is not None
    assert "lurker" in msg
    assert "untrusted" in msg
    assert "REFUSED" in msg


def test_dispatch_admits_trusted_spawner(tmp_path):
    """Negative control: a trusted row's seat is NOT refused."""
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    assert dispatch._refuse_untrusted_spawner(root, "alice") is None


def test_dispatch_absent_seat_fails_open(tmp_path):
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    assert dispatch._refuse_untrusted_spawner(root, None) is None


def test_dispatch_unknown_seat_fails_open(tmp_path):
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    assert dispatch._refuse_untrusted_spawner(root, "nobody") is None


# --- (b) season.merge-kids refuses an untrusted branch --------------------

def test_merge_kids_refuses_untrusted_branch_by_name(tmp_path):
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    # the untrusted row's branch is its name or its worktree cell
    for branch in ("lurker", "worktrees/lurker"):
        msg = season._refuse_untrusted_merge(root, branch)
        assert msg is not None, f"branch {branch!r} should be refused"
        assert "lurker" in msg and "untrusted" in msg and "REFUSED" in msg


def test_merge_kids_admits_trusted_branch(tmp_path):
    """Negative control: a trusted row's branch IS merged."""
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    assert season._refuse_untrusted_merge(root, "alice") is None
    assert season._refuse_untrusted_merge(root, "belam") is None


def test_merge_kids_unrelated_branch_admitted(tmp_path):
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    assert season._refuse_untrusted_merge(
        root, "loop/research-a00b0000@s2") is None


# --- (c) provisioning caps the untrusted post at the row's budget cell ----

def test_untrusted_post_capped_by_row_budget(tmp_path):
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    cfg = {}
    assert provisioning.post_limit_usd("lurker", cfg, root) == 0.4


def test_trusted_post_keeps_default(tmp_path):
    """Negative control: a trusted post gets None (default stands)."""
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    cfg = {}
    assert provisioning.post_limit_usd("alice", cfg, root) is None
    assert provisioning.post_limit_usd("belam", cfg, root) is None


def test_untrusted_post_without_budget_keeps_default(tmp_path):
    """A capped-less untrusted row keeps today's default exactly."""
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED_NO_BUDGET])
    assert provisioning.post_limit_usd("ghost", {}, root) is None


def test_absent_post_fails_open(tmp_path):
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    assert provisioning.post_limit_usd(None, {}, root) is None
    assert provisioning.post_limit_usd("nobody", {}, root) is None


# --- worktree-only conjunct read -----------------------------------------

def test_worktree_only_is_a_convention_not_a_mechanism(tmp_path):
    """Honest reading of the worktree-only conjunct: the untrusted post's
    worktree cell exists on its row and is what the refusals key on, but no
    mechanism in dispatch/season/provisioning here confines an untrusted
    process's writes to that worktree -- that confinement (if it exists at
    all) lives in the spawn environment (AGI_TREE_PROJECT_ROOT), not in
    these three files. State it plainly rather than inventing a writer-gate.
    """
    root = _project(tmp_path, [_TRUSTED, _UNTRUSTED])
    # read the row through the public reader so the cell is observable
    rows = geometry_config.load_rows(root)
    lurker = next(r for r in rows if r["name"] == "lurker")
    assert lurker["worktree"] == "worktrees/lurker"
    assert lurker["tier"] == "untrusted"
    # this test deliberately does NOT assert a write-confinement mechanism.