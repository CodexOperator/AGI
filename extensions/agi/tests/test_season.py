"""Tests for season.py — season lifecycle: status, judge, rollover.

goal:g12.3 — every new rule gets a test that was red first.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
BIN_DIR = TESTS_DIR.parent / "bin"
SRC_DIR = TESTS_DIR.parent / "src"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def engine_on_path(monkeypatch):
    monkeypatch.syspath_prepend(str(BIN_DIR))
    monkeypatch.syspath_prepend(str(SRC_DIR))
    yield


@pytest.fixture()
def season_py():
    """Return the absolute path to season.py."""
    return BIN_DIR / "season.py"


@pytest.fixture
def temp_graph(tmp_path, engine_on_path):
    """Create a minimal temp graph with a ladder node for testing."""
    import locations
    # Write a minimal ladder node inside .agi/nodes/.geometry/
    # (find_project_root returns the .agi/ directory)
    ladder_dir = tmp_path / ".agi" / "nodes" / ".geometry"
    ladder_dir.mkdir(parents=True)
    ladder = """---
id: ladder:ladder
type: ladder
current_season: 1
caps_apply_from_season: 2
caps:
  moral: 5
  vision: 3
tiers:
  - tier: 0
    plan_types: [subgoal, short-term goal]
    report_type: outcome
    judged_against: its (sub)goal
    lens: the long-term goal above
    cadence: the loop (weekly)
  - tier: 1
    plan_types: [long-term goal]
    report_type: bigger_outcome
    judged_against: its LT goal
    lens: the vision above
    cadence: mid-season
  - tier: 2
    plan_types: [vision]
    report_type: overview
    judged_against: its vision
    lens: the morals above
    cadence: season rollover (quarterly)
  - tier: 3
    plan_types: [moral]
    report_type: null
    judged_against: —
    lens: —
    cadence: never by machine; hand only
---
# ladder:ladder

Test ladder node.
"""
    (ladder_dir / "ladder.md").write_text(ladder)

    # Write a config so the project root is detected
    cfg_dir = tmp_path / ".agi"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    cfg = cfg_dir / "config.json"
    cfg.write_text('{"project": "test"}')

    # Write some test nodes inside .agi/nodes/
    goals_dir = tmp_path / ".agi" / "nodes" / "goal"
    goals_dir.mkdir(parents=True)

    # A subgoal with status active
    subgoal = """---
id: goal:sub1
type: goal
goal_kind: subgoal
status: active
parents: []
---
# subgoal 1
Test subgoal.
"""
    (goals_dir / "sub1.md").write_text(subgoal)

    # A short-term goal
    short = """---
id: goal:short1
type: goal
goal_kind: short-term
status: active
parents: []
---
# short-term 1
"""
    (goals_dir / "short1.md").write_text(short)

    # A long-term goal
    lt = """---
id: goal:lt1
type: goal
goal_kind: long-term
status: active
parents: []
---
# long-term 1
"""
    (goals_dir / "lt1.md").write_text(lt)

    # An outcome (report for tier 0)
    outcomes_dir = tmp_path / ".agi" / "nodes" / "outcome"
    outcomes_dir.mkdir(parents=True)
    outcome = """---
id: outcome:o1
type: outcome
status: active
parents: [goal:sub1]
---
# outcome 1
"""
    (outcomes_dir / "o1.md").write_text(outcome)

    # A second outcome with no judged_against
    outcome2 = """---
id: outcome:o2
type: outcome
status: active
parents: [goal:sub1]
---
# outcome 2
"""
    (outcomes_dir / "o2.md").write_text(outcome2)

    # A vision
    visions_dir = tmp_path / ".agi" / "nodes" / "vision"
    visions_dir.mkdir(parents=True)
    vision = """---
id: vision:v1
type: vision
status: active
parents: [goal:lt1]
---
# vision 1
"""
    (visions_dir / "v1.md").write_text(vision)

    # A moral
    morals_dir = tmp_path / ".agi" / "nodes" / "moral"
    morals_dir.mkdir(parents=True)
    moral = """---
id: moral:faith
type: moral
status: active
parents: []
---
# moral:faith
"""
    (morals_dir / "faith.md").write_text(moral)

    return tmp_path


# ---------------------------------------------------------------------------
# Status tests
# ---------------------------------------------------------------------------


class TestStatus:
    """season.py status subcommand."""

    def test_status_prints_tier_table(self, season_py, temp_graph):
        """status prints per-tier plan/report info."""
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "status"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "Tier 0" in result.stdout
        assert "Tier 1" in result.stdout
        assert "Tier 2" in result.stdout
        assert "Tier 3" in result.stdout

    def test_status_shows_plan_counts(self, season_py, temp_graph):
        """status shows active/total plan counts."""
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "status"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        # Tier 0 has subgoal (1) + short-term (1) = 2 plans total, 2 active
        assert "2 active / 2 total" in result.stdout

    def test_status_shows_report_counts(self, season_py, temp_graph):
        """status shows active/total report counts."""
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "status"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        # Tier 0 has 2 outcomes
        assert "2 active / 2 total" in result.stdout

    def test_status_shows_orphan_reports(self, season_py, temp_graph):
        """status shows reports with no judged_against."""
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "status"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "judged_against" in result.stdout


class TestRollover:
    """season.py rollover subcommand."""

    def test_rollover_dry_run_prints_plan(self, season_py, temp_graph):
        """rollover --dry-run prints what would happen without writing."""
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "rollover", "--dry-run"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "DRY RUN" in result.stdout
        assert "Rollover: season 1 → 2" in result.stdout
        assert "Bump ladder" in result.stdout

    def test_rollover_dry_run_shows_cap_applied_correctly(self, season_py, temp_graph):
        """rollover --dry-run counts visions of new season only against cap."""
        # Rollover from season 1 → 2: no visions of season 2 exist, so cap of 3 allows 3
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "rollover", "--dry-run"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        # Should offer up to 3 new visions (cap for new season, 0 existing)
        assert "Mint up to 3 new vision(s)" in result.stdout, \
            f"expected 'Mint up to 3 new vision(s)' in: {result.stdout}"

    def test_rollover_dry_run_does_not_write_ladder(self, season_py, temp_graph):
        """rollover --dry-run must not change the ladder node."""
        import locations
        from graph_core.persistence import frontmatter

        root = locations.find_project_root(temp_graph)
        assert root is not None

        # Read season before
        nf = frontmatter.load_node_file(root / "nodes" / ".geometry" / "ladder.md")
        before = nf.frontmatter.get("current_season")

        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "rollover", "--dry-run"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0

        # Read season after — must be unchanged
        nf = frontmatter.load_node_file(root / "nodes" / ".geometry" / "ladder.md")
        after = nf.frontmatter.get("current_season")
        assert before == after, "dry-run changed the ladder node"


class TestJudge:
    """season.py judge subcommand."""

    def test_judge_refuses_non_report_type(self, season_py, temp_graph):
        """judge refuses when the target is not a report type."""
        # A vision is not a report type
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "judge", "vision:v1"],
            capture_output=True, text=True,
        )
        assert result.returncode == 1
        assert "not a report type" in result.stderr

    def test_judge_scaffolds_moral_audit_on_overview(self, season_py, temp_graph):
        """judge on an overview scaffolds moral_audit with all 5 keys unknown."""
        import locations
        from graph_core.persistence import frontmatter

        root = locations.find_project_root(temp_graph)
        assert root is not None

        # Create a vision for the overview to parent to
        visions_dir = root / "nodes" / "vision"
        vision_with_parent = """---
id: vision:v2
season: 1
type: vision
status: active
parents: [goal:lt1]
---
# vision v2
"""
        (visions_dir / "v2.md").write_text(vision_with_parent)

        # Create an overview node
        overviews_dir = root / "nodes" / "overview"
        overviews_dir.mkdir(parents=True, exist_ok=True)
        overview = """---
id: overview:test1
type: overview
status: active
parents: [vision:v2]
season: 1
---
# overview:test1
"""
        (overviews_dir / "test1.md").write_text(overview)

        # Run judge with explicit --against
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "judge", "overview:test1", "--against", "vision:v2"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "moral_audit scaffolded" in result.stdout

        # Verify moral_audit was written
        nf = frontmatter.load_node_file(overviews_dir / "test1.md")
        audit = nf.frontmatter.get("moral_audit", {})
        assert isinstance(audit, dict)
        for mk in ("faith", "love", "empathy", "antifragility", "beauty"):
            assert mk in audit, f"missing moral key: {mk}"
            assert audit[mk].get("value") == "unknown", f"{mk} value not unknown"
            assert audit[mk].get("evidence") is None, f"{mk} evidence not null"

    def test_judge_preserves_existing_moral_audit_keys(self, season_py, temp_graph):
        """judge on an overview with partial moral_audit fills only missing keys."""
        import locations
        from graph_core.persistence import frontmatter

        root = locations.find_project_root(temp_graph)
        assert root is not None

        # Create a vision
        visions_dir = root / "nodes" / "vision"
        vision_v3 = """---
id: vision:v3
season: 1
type: vision
status: active
parents: [goal:lt1]
---
# vision v3
"""
        (visions_dir / "v3.md").write_text(vision_v3)

        # Create an overview with partial moral_audit
        overviews_dir = root / "nodes" / "overview"
        overviews_dir.mkdir(parents=True, exist_ok=True)
        overview = """---
id: overview:test2
type: overview
status: active
parents: [vision:v3]
season: 1
moral_audit:
  faith: {value: aligned, evidence: "exp:abc"}
---
# overview:test2
"""
        (overviews_dir / "test2.md").write_text(overview)

        # Run judge with explicit --against
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "judge", "overview:test2", "--against", "vision:v3"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "moral_audit scaffolded" in result.stdout

        # Verify faith is untouched and others were filled
        nf = frontmatter.load_node_file(overviews_dir / "test2.md")
        audit = nf.frontmatter.get("moral_audit", {})
        assert isinstance(audit, dict)
        # faith preserved
        assert audit["faith"]["value"] == "aligned"
        assert audit["faith"]["evidence"] == "exp:abc"
        # others filled
        for mk in ("love", "empathy", "antifragility", "beauty"):
            assert mk in audit, f"missing moral key: {mk}"
            assert audit[mk].get("value") == "unknown"
            assert audit[mk].get("evidence") is None


# ---------------------------------------------------------------------------
# Integration: commands.py can discover season.py
# ---------------------------------------------------------------------------


class TestCommandDiscovery:
    """season.py is discoverable via commands.py list or json."""

    def test_commands_json_includes_season_py(self, engine_on_path):
        """season.py is reachable from bin/ (tested via import)."""
        # Just verify the module can be imported without error
        import importlib
        spec = importlib.util.find_spec("season")
        assert spec is not None, "season.py not findable on sys.path"
        # We can also call --help
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, BIN_DIR / "season.py", "--help"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "status" in result.stdout
        assert "judge" in result.stdout
        assert "rollover" in result.stdout


# ---------------------------------------------------------------------------
# Retag tests
# ---------------------------------------------------------------------------


class TestRetag:
    """season.py retag subcommand — backfill the season stamp."""

    def _load_fm(self, root, rel):
        from graph_core.persistence import frontmatter
        nf = frontmatter.load_node_file(root / rel)
        return nf.frontmatter

    def _collect(self, season_py, temp_graph, *args):
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "retag", *args],
            capture_output=True, text=True,
        )
        return result

    def _unstamped_paths(self, root):
        from graph_core.persistence import frontmatter
        out = []
        for f in sorted((root / "nodes").rglob("*.md")):
            try:
                nf = frontmatter.load_node_file(f)
            except Exception:
                continue
            if nf.frontmatter.get("id") and nf.frontmatter.get("season") is None:
                out.append(f.relative_to(root / "nodes"))
        return out

    def test_retag_stamps_all_unstamped(self, season_py, temp_graph):
        """After retag, every node carries season: 1."""
        import locations
        root = locations.find_project_root(temp_graph)
        assert root is not None
        assert len(self._unstamped_paths(root)) >= 3, "fixture must have unstamped nodes"

        result = self._collect(season_py, temp_graph)
        assert result.returncode == 0, f"stderr: {result.stderr}"

        unstamped = self._unstamped_paths(root)
        assert unstamped == [], f"nodes still unstamped: {unstamped}"
        # spot-check one goal and the moral node
        from graph_core.persistence import frontmatter
        sub = frontmatter.load_node_file(root / "nodes" / "goal" / "sub1.md")
        assert sub.frontmatter.get("season") == 1
        faith = frontmatter.load_node_file(root / "nodes" / "moral" / "faith.md")
        assert faith.frontmatter.get("season") == 1

    def test_retag_never_overwrites_existing(self, season_py, temp_graph):
        """A node that already has a season is left untouched."""
        import locations
        root = locations.find_project_root(temp_graph)
        assert root is not None
        # Give the outcome a season that is NOT the retag value.
        from graph_core.persistence import frontmatter
        o2 = root / "nodes" / "outcome" / "o2.md"
        text = o2.read_text().replace("status: active", "status: active\nseason: 2")
        o2.write_text(text)

        result = self._collect(season_py, temp_graph)
        assert result.returncode == 0, f"stderr: {result.stderr}"
        # o2 keeps its hand-set season
        o2fm = frontmatter.load_node_file(o2).frontmatter
        assert o2fm.get("season") == 2, "explicit existing season was overwritten"
        # everything else got 1
        for p in self._unstamped_paths(root):
            if p == (root / "nodes" / "outcome" / "o2.md").relative_to(root / "nodes"):
                continue
            fm = frontmatter.load_node_file(root / "nodes" / p).frontmatter
            assert fm.get("season") == 1, f"{p} not stamped: {fm.get('season')}"

    def test_retag_dry_run_writes_nothing(self, season_py, temp_graph):
        """--dry-run reports counts but writes no season fields."""
        import locations
        root = locations.find_project_root(temp_graph)
        assert root is not None
        before = self._unstamped_paths(root)
        assert before, "fixture must have unstamped nodes"

        result = self._collect(season_py, temp_graph, "--dry-run")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "DRY RUN" in result.stdout
        # nothing changed
        assert self._unstamped_paths(root) == before

    def test_retag_reports_before_after_counts(self, season_py, temp_graph):
        """stdout reports counts before and after the pass."""
        result = self._collect(season_py, temp_graph)
        assert result.returncode == 0, f"stderr: {result.stderr}"
        # before figure
        assert "with season: 0" in result.stdout
        assert "without season: 8" in result.stdout
        # after figure
        assert "after: 8 with season / 0 without" in result.stdout

    def test_retag_preserves_owner_provenance_on_moral(self, season_py, temp_graph):
        """Moral nodes keep their owner edited_by/thought_session after retag."""
        import locations
        root = locations.find_project_root(temp_graph)
        assert root is not None
        faith = root / "nodes" / "moral" / "faith.md"
        # Give the moral node owner provenance that retag must not clobber.
        text = faith.read_text().replace(
            "status: active", "status: active\nedited_by: owner\nthought_session: agi-master-2026-09-06")
        faith.write_text(text)

        result = self._collect(season_py, temp_graph)
        assert result.returncode == 0, f"stderr: {result.stderr}"
        from graph_core.persistence import frontmatter
        fm = frontmatter.load_node_file(faith).frontmatter
        assert fm.get("season") == 1, "moral not stamped"
        assert fm.get("edited_by") == "owner", "moral edited_by clobbered"
        assert fm.get("thought_session") == "agi-master-2026-09-06", \
            "moral thought_session clobbered by scripted pass"

    def test_retag_covers_deprecated(self, season_py, temp_graph):
        """Nodes under nodes/deprecated/ are retagged too."""
        import locations
        root = locations.find_project_root(temp_graph)
        assert root is not None
        dep = root / "nodes" / "deprecated" / "experiment"
        dep.mkdir(parents=True, exist_ok=True)
        old = """---
id: experiment:ancient
mint_id: 11111111111111111111111111111111
type: experiment
parents: []
status: deprecated
---
# ancient
"""
        (dep / "ancient.md").write_text(old)

        result = self._collect(season_py, temp_graph)
        assert result.returncode == 0, f"stderr: {result.stderr}"
        from graph_core.persistence import frontmatter
        fm = frontmatter.load_node_file(dep / "ancient.md").frontmatter
        assert fm.get("season") == 1


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


class TestErrorHandling:
    """season.py error states."""

    def test_requires_subcommand(self, season_py, temp_graph):
        """Running season.py with no subcommand exits 2."""
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph)],
            capture_output=True, text=True,
        )
        assert result.returncode == 2

    def test_unknown_subcommand(self, season_py, temp_graph):
        """Running season.py with an unknown subcommand exits 2."""
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "foobar"],
            capture_output=True, text=True,
        )
        assert result.returncode == 2

    def test_outside_project(self, season_py, tmp_path):
        """Running season.py outside an agi project exits 1."""
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(tmp_path),
             "status"],
            capture_output=True, text=True,
        )
        assert result.returncode == 1
        assert "not an agi project" in result.stderr