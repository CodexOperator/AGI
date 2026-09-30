"""SCOPED falsifier 2 for goal:g1.31.4.1 -- runnable where the goal's own
negative falsifier is unsatisfiable.

The goal greps `.agi/nodes` WHOLE, so its two legitimate quotes of the
retired caveat (end-state line 33, falsifier line 42) satisfy the bar
themselves: a later reader gets 2 and cannot tell a live residue from the
goal's own text. The goal text is NOT touched by this round (a bar is never
loosened by the reviewer who wanted it green). Instead the check gets a
stated, defensible scope in `agi.bin.caveat_residue`:

  green  -- the phrase is absent from every node kind that ASSERTS a finding
  red    -- the phrase appears in one of those kinds
  the goal's own two quotes are EXCLUDED BY NAME, and that exclusion is
           asserted here so a future round cannot quietly widen the scope.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import caveat_residue, locations  # noqa: E402


def _live_nodes():
    root = locations.find_project_root(Path(__file__).resolve())
    assert root is not None, "no project root with .agi/ config.json"
    nodes = root / "nodes"
    assert nodes.is_dir(), f"{nodes} is not a nodes dir"
    return nodes


def test_live_graph_carries_no_residue_in_asserting_node_kinds():
    hits = caveat_residue.scan(_live_nodes())
    assert hits == [], (
        "the retired caveat 'bad --target is not caught' is ASSERTED again in "
        f"a round node: {hits}"
    )


def test_the_excluded_goal_quote_exists_and_is_excluded_by_name(tmp_path):
    # The exclusion is not a convenient filter: the goal really does carry the
    # phrase, and the check really does not see it.
    goal = tmp_path / "goal"
    goal.mkdir()
    (goal / "g.md").write_text(
        "the caveat (\"bad --target is not caught by dry-run\") no longer holds\n",
        encoding="utf-8",
    )
    assert caveat_residue.scan(tmp_path) == []
    assert "goal" not in caveat_residue.SCOPE


def test_negative_self_test_the_check_can_go_red(tmp_path):
    # PLANT the phrase in a scratch node under an asserting kind -> red.
    d = tmp_path / "experiment"
    d.mkdir()
    (d / "e.md").write_text("bad --target is not caught by dry-run\n", encoding="utf-8")
    hits = caveat_residue.scan(tmp_path)
    assert len(hits) == 1
    rel, ln, text = hits[0]
    assert rel == "experiment/e.md" and ln == 1 and "bad --target" in text
    # and the alias spelling is caught too, and clearing it turns green
    (d / "e.md").write_text("bad --target uncaught by the dry run\n", encoding="utf-8")
    assert len(caveat_residue.scan(tmp_path)) == 1
    (d / "e.md").write_text("dry-run refuses the same target\n", encoding="utf-8")
    assert caveat_residue.scan(tmp_path) == []


def test_scope_is_the_asserting_kinds_only():
    assert set(caveat_residue.SCOPE) == {
        "experiment", "hypothesis", "verdict", "build", "mvp", "outcome",
    }
    assert "goal" not in caveat_residue.SCOPE
