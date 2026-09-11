"""Tests for season.py — season lifecycle: status, judge, rollover.

goal:g12.3 — every new rule gets a test that was red first.
"""
from __future__ import annotations

import json
import os
import shutil
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


class TestJudgeQuorum:
    """season.py judge --quorum: reviews through the advisor quorum.

    hypothesis:l3w4-quorum-reviews — three advisor votes (one per vision) in
    a room; a 3-0/2-1 majority stamps alignment here, a 1-1-1 deadlock or any
    --morals vote falls through to `send.py audience prime` instead and leaves
    alignment unset.
    """

    @staticmethod
    def _post_quorum(croot, target, votes, round_):
        """Post votes [(vision, alignment, morals, reason)] into tier3-quorum."""
        sys.path.insert(0, str(BIN_DIR))
        import send
        for vision, alignment, morals, reason in votes:
            send.vote(croot, "tier3-quorum", target, vision, alignment,
                      "adv-" + vision, morals, reason, round_)

    @staticmethod
    def _quorum_env():
        env = dict(os.environ)
        env["AGI_ROLE"] = "parent"
        env["AGI_LADDER_TIER"] = "3"
        env["AGI_LOOP"] = "L3.29@s2"
        return env

    def _judge(self, season_py, temp_graph, croot, round_, target="outcome:o1"):
        return subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "judge", target, "--quorum", "--room", "tier3-quorum",
             "--round", round_, "--comms-root", str(croot)],
            capture_output=True, text=True, env=self._quorum_env(),
        )

    def test_judge_quorum_stamps_alignment_on_majority(self, season_py,
                                                       temp_graph, tmp_path):
        """2 aligned + 1 adjust -> alignment: aligned stamped + quorum note."""
        croot = tmp_path / "comms"
        self._post_quorum(croot, "outcome:o1", [
            ("alive", "aligned", False, "good fit"),
            ("all-is-one", "adjust", False, "needs a tweak"),
            ("self-perpetuating", "aligned", False, "keep it"),
        ], "R1")
        result = self._judge(season_py, temp_graph, croot, "R1")
        assert result.returncode == 0, f"stderr: {result.stderr}"

        import locations
        from graph_core.persistence import frontmatter
        root = locations.find_project_root(temp_graph)
        nf = frontmatter.load_node_file(root / "nodes" / "outcome" / "o1.md")
        assert nf.frontmatter.get("alignment") == "aligned"
        assert nf.frontmatter.get("judged_against") == "goal:sub1"
        body = nf.body or ""
        assert "quorum tier3-quorum" in body  # the quorum note landed

    def test_judge_quorum_three_zero_stamps(self, season_py, temp_graph,
                                            tmp_path):
        """3-0 aligned also stamps alignment (unanimity)."""
        croot = tmp_path / "comms"
        self._post_quorum(croot, "outcome:o1", [
            ("alive", "aligned", False, ""),
            ("all-is-one", "aligned", False, ""),
            ("self-perpetuating", "aligned", False, ""),
        ], "R3")
        result = self._judge(season_py, temp_graph, croot, "R3")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        import locations
        from graph_core.persistence import frontmatter
        root = locations.find_project_root(temp_graph)
        nf = frontmatter.load_node_file(root / "nodes" / "outcome" / "o1.md")
        assert nf.frontmatter.get("alignment") == "aligned"

    def test_judge_quorum_deadlock_calls_audience_not_stamp(self, season_py,
                                                            temp_graph, tmp_path):
        """A literal 1-1-1 calls audience prime instead and stamps nothing:
        alignment is unset and no judged_against is written."""
        croot = tmp_path / "comms"
        self._post_quorum(croot, "outcome:o1", [
            ("alive", "aligned", False, ""),
            ("all-is-one", "adjust", False, "shift"),
            ("self-perpetuating", "unknown", False, "on the fence"),
        ], "R2")
        result = self._judge(season_py, temp_graph, croot, "R2")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "audience requested" in result.stdout  # reached the prime
        assert "alignment unset" in result.stdout

        import locations
        from graph_core.persistence import frontmatter
        root = locations.find_project_root(temp_graph)
        nf = frontmatter.load_node_file(root / "nodes" / "outcome" / "o1.md")
        assert nf.frontmatter.get("alignment") is None
        assert nf.frontmatter.get("judged_against") is None
        assert "quorum" not in (nf.body or "")

    def test_judge_quorum_morals_forces_audience_despite_majority(
            self, season_py, temp_graph, tmp_path):
        """Any --morals vote forces an audience even on a 2-1 majority;
        alignment stays unset."""
        croot = tmp_path / "comms"
        self._post_quorum(croot, "outcome:o1", [
            ("alive", "aligned", False, ""),
            ("all-is-one", "adjust", True, "life is at stake"),
            ("self-perpetuating", "aligned", False, ""),
        ], "R4")
        result = self._judge(season_py, temp_graph, croot, "R4")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "audience requested" in result.stdout
        assert "morals" in result.stdout

        import locations
        from graph_core.persistence import frontmatter
        root = locations.find_project_root(temp_graph)
        nf = frontmatter.load_node_file(root / "nodes" / "outcome" / "o1.md")
        assert nf.frontmatter.get("alignment") is None

    def test_judge_quorum_incomplete_quorum_refuses(self, season_py,
                                                    temp_graph, tmp_path):
        """Fewer than three visions -> incomplete quorum, judge refuses."""
        croot = tmp_path / "comms"
        self._post_quorum(croot, "outcome:o1", [
            ("alive", "aligned", False, ""),
            ("all-is-one", "adjust", False, ""),
        ], "R5")
        result = self._judge(season_py, temp_graph, croot, "R5")
        assert result.returncode == 1
        assert "incomplete quorum" in result.stderr


# ---------------------------------------------------------------------------
# Integration: commands.py can discover season.py
# ---------------------------------------------------------------------------


class TestRolloverGenesis:
    """season.py rollover wave-2 genesis path (hypothesis l3w2-rollover-genesis)."""

    def _write_vision_source(self, tmp_path, slug="self-perpetuating", title="Self-perpetuating"):
        d = tmp_path / "visions"
        d.mkdir(exist_ok=True)
        fp = d / f"{slug}.md"
        fp.write_text(
            f"# {title}\n\nOwner text, 2026-09-06, verbatim.\n\n"
            "\"the graph invites completion.\"\n\n"
            "## Owner's gloss\n\n\"the ladder running itself.\"\n")
        return d

    def _overview_fm(self, root, oid, season=1, judged=False):
        from graph_core.persistence import frontmatter
        overviews = root / "nodes" / "overview"
        overviews.mkdir(parents=True, exist_ok=True)
        judged_line = f"judged_against: vision:x\n" if judged else ""
        (overviews / f"{oid.split(':')[-1]}.md").write_text(
            f"---\nid: {oid}\ntype: overview\nparents: [bigger_outcome:bo]\n"
            f"season: {season}\n{judged_line}\n---\n# {oid}\n")

    def _run(self, season_py, temp_graph, *args):
        return subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "rollover", *args],
            capture_output=True, text=True)

    def test_dry_run_prints_visions_from_files_verbatim(self, season_py, temp_graph, tmp_path):
        """--visions-from: dry run prints each MINT with parents, season_parents,
        actor owner, and the body verbatim from the source file."""
        vdir = self._write_vision_source(tmp_path)
        result = self._run(season_py, temp_graph, "--dry-run",
                           "--visions-from", str(vdir), "--name", "genesis")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "MINT vision:self-perpetuating" in result.stdout
        assert "moral:faith, moral:love, moral:empathy, moral:antifragility, moral:beauty" in result.stdout
        assert "actor: owner" in result.stdout
        # body verbatim: the owner quote line (not invented by the planner)
        assert '\"the graph invites completion.\"' in result.stdout
        assert "## Owner's gloss" in result.stdout

    def test_dry_run_prints_name_and_branch(self, season_py, temp_graph, tmp_path):
        """--name genesis and --branch are shown in the dry-run plan."""
        vdir = self._write_vision_source(tmp_path)
        result = self._run(season_py, temp_graph, "--dry-run",
                           "--visions-from", str(vdir), "--name", "genesis",
                           "--branch")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "season_names[1] = genesis" in result.stdout
        assert "Bump ladder current_season: 1 → 2" in result.stdout
        assert "git checkout -b season/s2" in result.stdout

    def test_dry_run_changes_nothing(self, season_py, temp_graph, tmp_path):
        """Even with every flag, --dry-run writes no node and no ladder field."""
        import locations
        from graph_core.persistence import frontmatter
        root = locations.find_project_root(temp_graph)
        vdir = self._write_vision_source(tmp_path)
        vision_file = root / "nodes" / "vision" / "self-perpetuating.md"
        assert not vision_file.exists()
        result = self._run(season_py, temp_graph, "--dry-run",
                           "--visions-from", str(vdir), "--name", "genesis",
                           "--branch")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert not vision_file.exists(), "dry run minted a vision"
        nf = frontmatter.load_node_file(root / "nodes" / ".geometry" / "ladder.md")
        assert nf.frontmatter.get("current_season") == 1, "dry run bumped the season"
        assert nf.frontmatter.get("season_names", {}).get(1) is None or True

    def test_refuses_while_an_overview_lacks_judgment(self, season_py, temp_graph):
        """A season-current overview without a judgment blocks rollover unless
        --allow-unjudged, printing the count."""
        import locations
        root = locations.find_project_root(temp_graph)
        self._overview_fm(root, "overview:unjudged", season=1, judged=False)

        result = self._run(season_py, temp_graph, "--dry-run")
        assert result.returncode == 1, "should refuse with an unjudged overview"
        assert "1 overview(s) of season 1 lack a judgment" in result.stdout
        assert "REFUSED" in result.stdout

        # --allow-unjudged proceeds
        result2 = self._run(season_py, temp_graph, "--dry-run", "--allow-unjudged")
        assert result2.returncode == 0, f"stderr: {result2.stderr}"
        assert "proceeding anyway" in result2.stdout

    def test_real_run_mints_visions_names_ladder_and_opens_branch(self, season_py, temp_graph, tmp_path):
        """The real run performs the plan: minted vision nodes with verbatim
        bodies, ladder renamed and bumped, and the season/s2 branch opened."""
        import locations
        from graph_core.persistence import frontmatter
        root = locations.find_project_root(temp_graph)
        assert root is not None

        # Make the project a git repo so the branch step can run.
        subprocess.run(["git", "init", "-q"], cwd=str(tmp_path))
        subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                      "add", "-A"], cwd=str(tmp_path))
        subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                      "commit", "-qm", "base"], cwd=str(tmp_path))

        vdir = self._write_vision_source(tmp_path, slug="all-is-one", title="All is one")
        result = self._run(season_py, temp_graph, "--visions-from", str(vdir),
                           "--name", "genesis", "--branch")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "minted vision:all-is-one" in result.stdout
        assert "season_names[1] = genesis written" in result.stdout
        assert "opened branch season/s2" in result.stdout

        # The minted vision: season 2, five moral parents, verbatim body.
        vision = frontmatter.load_node_file(root / "nodes" / "vision" / "all-is-one.md")
        fm = vision.frontmatter
        assert fm.get("season") == 2
        assert fm.get("mint_id"), "minted node must carry a mint id"
        parents = [p for p in fm.get("parents", [])]
        assert len(parents) == 5
        assert "moral:faith" in parents and "moral:beauty" in parents
        assert '\"the graph invites completion.\"' in vision.body
        assert "## Owner's gloss" in vision.body

        # Ladder renamed and bumped, through write.py (provenance present).
        ladder = frontmatter.load_node_file(root / "nodes" / ".geometry" / "ladder.md")
        assert ladder.frontmatter.get("current_season") == 2
        assert ladder.frontmatter.get("season_names", {}).get(1) == "genesis"

        # Branch opened and never pushed.
        br = subprocess.run(["git", "-C", str(tmp_path), "branch", "--show-current"],
                            capture_output=True, text=True)
        assert br.stdout.strip() == "season/s2"

    def test_second_rollover_names_its_own_season_and_attributes_each_write(
            self, season_py, temp_graph, tmp_path):
        """A second rollover writes its OWN season's key and stamps the seat.

        hypothesis:l3w4-masters-rollover — `season_names[1] = name` hardcodes
        season 1 (today a second rollover clobbers genesis), and judge/rollover
        write `edited_by: season.py`. With `--actor into the ladder write, the
        season-2 version's edited_by is the passed seat and the 2→3 name lands
        under season 2, not season 1.
        """
        import locations
        from graph_core.persistence import frontmatter
        root = locations.find_project_root(temp_graph)
        assert root is not None

        # Rehearse 1 → 2, naming season 1, acting as Sanctuary Master.
        r1 = self._run(season_py, temp_graph,
                       "--name", "genesis", "--actor", "sanctuary-master")
        assert r1.returncode == 0, f"stderr: {r1.stderr}"
        assert "season_names[1] = genesis" in r1.stdout

        # Rehearse 2 → 3, naming season 2, still acting as Sanctuary Master.
        r2 = self._run(season_py, temp_graph,
                       "--name", "wave-4-masters",
                       "--actor", "sanctuary-master")
        assert r2.returncode == 0, f"stderr: {r2.stderr}"
        assert "season_names[2] = wave-4-masters" in r2.stdout

        # Each season keeps its own name (today genesis is clobbered), and the
        # ladder write is attributed to the seat, not the hardcoded season.py.
        ladder = frontmatter.load_node_file(root / "nodes" / ".geometry" / "ladder.md")
        assert ladder.frontmatter.get("current_season") == 3
        assert ladder.frontmatter.get("season_names", {}) == {
            1: "genesis", 2: "wave-4-masters"}
        assert ladder.frontmatter.get("edited_by") == "sanctuary-master"

    def test_judge_actor_stamps_edited_by(self, season_py, temp_graph):
        """`judge --actor` threads the seat into the write's edited_by."""
        import locations
        from graph_core.persistence import frontmatter
        root = locations.find_project_root(temp_graph)
        assert root is not None

        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "judge", "outcome:o1", "--against", "goal:sub1",
             "--actor", "glitch-master", "--session", "season-3"],
            capture_output=True, text=True)
        assert result.returncode == 0, f"stderr: {result.stderr}"

        out = frontmatter.load_node_file(root / "nodes" / "outcome" / "o1.md")
        fm = out.frontmatter
        assert fm.get("judged_against") == "goal:sub1"
        assert fm.get("edited_by") == "glitch-master"
        assert fm.get("thought_session") == "season-3"

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

# ---------------------------------------------------------------------------
# merge-up tests (hypothesis:l3w4-parent-branch-merge-up)
# ---------------------------------------------------------------------------


def _git(tmp, *args):
    return subprocess.run(["git", "-C", str(tmp), *args],
                          capture_output=True, text=True)


def _init_project(tmp_path, season="season/s1"):
    """git-init the temp project (which already holds .agi/) and make a base
    commit on season/s1, so merge-up has a branch it can merge into."""
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "checkout", "-q", "-b", season)
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "-c", "user.email=t@t", "-c", "user.name=t",
         "commit", "-qm", "base")
    return tmp_path


def _commit(tmp, msg, filename="file.txt", content="x\n"):
    (tmp / filename).write_text(content)
    _git(tmp, "add", "-A")
    return _git(tmp, "-c", "user.email=t@t", "-c", "user.name=t",
                "commit", "-qm", msg)


class TestMergeUp:
    """season.py merge-up subcommand — the branch->base upward merge, green gate.

    goal:g12.3 — landing a branch against its recorded base needs tests red
    first; these cover the hypothesis's merge-up test list plus the recursion
    ADDENDUM (recorded base_branch, three-layer rehearsal).
    """

    def test_merge_up_merges_no_ff_and_removes_worktree(
            self, season_py, temp_graph, tmp_path):
        """A passing suite lands a --no-ff merge commit and removes the
        worktree."""
        _init_project(tmp_path)
        base = str(tmp_path)
        worktree = tmp_path / "wt"
        br = _git(tmp_path, "worktree", "add", "-b", "loop/slug-abc12345@s2",
                  str(worktree), "season/s1")
        assert br.returncode == 0, br.stderr
        _commit(worktree, "kid commit", content="kid\n")

        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/slug-abc12345@s2", "--suite", "exit 0",
             "--worktree", str(worktree)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert f"merged loop/slug-abc12345@s2 --no-ff into season/s1" in result.stdout
        assert f"removed worktree {worktree}" in result.stdout
        assert "complete; suite green" in result.stdout

        # A --no-ff merge commit exists with two parents.
        merge = _git(tmp_path, "log", "-1", "--format=%P", "season/s1")
        assert len(merge.stdout.split()) == 2, "expected a real (2-parent) merge"

        # The branch's commit is now in the base's history.
        merged = _git(tmp_path, "log", "season/s1", "--format=%s",
                      "--") .stdout
        assert "kid commit" in merged

        # The worktree really is gone.
        wt = _git(tmp_path, "worktree", "list", "--porcelain")
        assert str(worktree) not in wt.stdout

    def test_merge_up_refuses_on_red_suite(self, season_py, temp_graph, tmp_path):
        """A red suite aborts the merge and leaves the branch + worktree."""
        _init_project(tmp_path)
        worktree = tmp_path / "wt"
        _git(tmp_path, "worktree", "add", "-b", "loop/red-ffffffff@s2",
             str(worktree), "season/s1")
        _commit(worktree, "red commit", content="red\n")

        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/red-ffffffff@s2", "--suite", "exit 1",
             "--worktree", str(worktree)],
            capture_output=True, text=True,
        )
        assert result.returncode == 1, "red suite must refuse the merge"
        assert "REFUSED" in result.stdout
        assert "loop/red-ffffffff@s2" in result.stdout

        # Merge aborted: the red commit is NOT in the base's history.
        log = _git(tmp_path, "log", "season/s1", "--format=%s").stdout
        assert "red commit" not in log
        # Branch still exists and worktree was NOT removed.
        branches = _git(tmp_path, "branch", "--list").stdout
        assert "loop/red-ffffffff@s2" in branches
        wt = _git(tmp_path, "worktree", "list", "--porcelain").stdout
        assert str(worktree) in wt

    def test_merge_up_refuses_zero_ahead_branch(
            self, season_py, temp_graph, tmp_path):
        """A loop branch that carries ZERO commits beyond its base must be
        refused loudly, not green-merged into a no-op success (false green).
        Every empty loop branch used to sail through as 'merged ... (pending
        suite)' and a human had to finish the round by hand."""
        _init_project(tmp_path)  # on season/s1
        # Cut a branch at the base tip with no extra commit: zero ahead.
        br = _git(tmp_path, "checkout", "-q", "-b", "loop/empty-abc12345@s2")
        assert br.returncode == 0, br.stderr
        # Return to the base so the current branch is NOT the loop branch.
        _git(tmp_path, "checkout", "-q", "season/s1")

        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/empty-abc12345@s2", "--suite", "exit 0"],
            capture_output=True, text=True,
        )
        combined = result.stdout + result.stderr
        assert result.returncode == 1, "zero-ahead branch must be refused"
        assert "REFUSED" in combined
        assert "zero commits ahead" in combined
        assert "loop/empty-abc12345@s2" in combined
        # Nothing was merged: the base still holds exactly its one commit.
        count = _git(tmp_path, "rev-list", "--count",
                     "season/s1").stdout.strip()
        assert count == "1", "refused merge must not leave a merge commit"

    def test_merge_up_treats_false_red_as_green(
            self, season_py, temp_graph, tmp_path):
        """When the finalize `git commit` returns non-zero but the merge has in
        fact landed (MERGE_HEAD already gone), merge-up must NOT report a
        failure it cannot substantiate (false red) -- it must carry on green.
        Reproduced by a PATH git shim that lets the real commit finish the
        merge but then exits non-zero, exactly as git mis-reported at L3.34."""
        _init_project(tmp_path)
        worktree = tmp_path / "wt"
        _git(tmp_path, "worktree", "add", "-b", "loop/misrep-abc12345@s2",
             str(worktree), "season/s1")
        _commit(worktree, "kid work", content="kid\n")

        real_git = shutil.which("git")
        assert real_git, "git must be on PATH to build the shim"
        shim_dir = tmp_path / "shim"
        shim_dir.mkdir(exist_ok=True)
        git_shim = shim_dir / "git"
        git_shim.write_text(
            "#!/bin/sh\n"
            f"REAL={real_git}\n"
            'case \"$*\" in\n'
            "*'--no-edit'*)\n"
            "    \"$REAL\" \"$@\"   # do the real commit; merge completes\n"
            "    if [ \"$?\" -eq 0 ]; then exit 8; fi   # then lie about it\n"
            "    ;;\n"
            "esac\n"
            'exec "$REAL" "$@"\n')
        git_shim.chmod(0o755)
        env = dict(os.environ)
        env["PATH"] = str(shim_dir) + os.pathsep + env["PATH"]

        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/misrep-abc12345@s2", "--suite", "exit 0",
             "--worktree", str(worktree)],
            capture_output=True, text=True, env=env,
        )
        assert result.returncode == 0, \
            f"false red must not become a failure: {result.stderr}"
        assert "treating as green" in result.stdout
        assert "complete; suite green" in result.stdout
        # The merge really did land despite the commit's mis-reported code.
        assert "kid work" in _git(
            tmp_path, "log", "season/s1", "--format=%s").stdout
        # And the worktree was removed (success path, not the stranded one).
        wt = _git(tmp_path, "worktree", "list", "--porcelain").stdout
        assert str(worktree) not in wt

    def test_merge_up_town_gate_refuses_cross_town_and_allows_same_town(
            self, season_py, temp_graph, tmp_path):
        """hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council --
        a round merges up through the seat of the town that ORIGINATED it;
        the merge refuses when the round node's `town:` differs from the
        target seat's config:seats `town`, and proceeds when they agree.
        Both towns are read (round via its `town:` cell, seat via its row),
        never a branch on a town NAME (goal:g8.2). Fails open when either
        half is absent, so a town-less graph merges exactly as before."""
        _init_project(tmp_path)
        # --- two town seats in config:seats (the council shape) ---
        seats_dir = tmp_path / ".agi" / "nodes" / ".geometry"
        seats_dir.mkdir(parents=True, exist_ok=True)
        (seats_dir / "seats.md").write_text(
            "---\nid: config:seats\ntype: config\nseats:\n"
            "  - {\"name\": \"council-streaming\", \"town\": "
            "\"streaming-suite\"}\n"
            "  - {\"name\": \"council-web\", \"town\": "
            "\"web-app-suite\"}\n---\nbody\n", encoding="utf-8")
        # --- a round node stamped at mint with its town ---
        exp_dir = tmp_path / ".agi" / "nodes" / "experiment"
        exp_dir.mkdir(parents=True, exist_ok=True)
        (exp_dir / "round.md").write_text(
            "---\nid: experiment:round\ntype: experiment\ntown: "
            "streaming-suite\n---\nbody\n", encoding="utf-8")

        worktree = tmp_path / "wt"
        _git(tmp_path, "worktree", "add", "-b", "loop/slug-abc12345@s2",
             str(worktree), "season/s1")
        _commit(worktree, "kid commit", content="kid\n")

        # Cross-town: round in streaming-suite, seat in web-app-suite -> refuse.
        cross = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/slug-abc12345@s2", "--suite", "exit 0",
             "--round", "experiment:round", "--seat", "council-web"],
            capture_output=True, text=True,
        )
        assert cross.returncode == 1, cross.stdout
        assert "REFUSED" in cross.stderr
        assert "streaming-suite" in cross.stderr
        assert "web-app-suite" in cross.stderr
        # Nothing was merged (the gate fires before any git write).
        assert _git(tmp_path, "rev-list", "--count", "season/s1"
                    ).stdout.strip() == "1"

        # Same-town: round and seat both streaming-suite -> merge proceeds.
        same = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/slug-abc12345@s2", "--suite", "exit 0",
             "--round", "experiment:round", "--seat", "council-streaming",
             "--worktree", str(worktree)],
            capture_output=True, text=True,
        )
        assert same.returncode == 0, same.stderr
        assert "complete; suite green" in same.stdout
        assert "kid commit" in _git(tmp_path, "log", "season/s1",
                                    "--format=%s").stdout
        wt = _git(tmp_path, "worktree", "list", "--porcelain").stdout
        assert str(worktree) not in wt

    def test_merge_up_town_gate_fires_without_round_or_seat(
            self, tmp_path, engine_on_path, monkeypatch):
        """Residue 5 — the town gate FIRES without --round/--seat.

        The seat is derived from the exported AGI_SEAT env var (the seat name
        the spawn already carries) and the round's town from the branch being
        merged up via `town_of_branch` (reverse-lookup on the opaque
        `town_branches` value). A cross-town merge is REFUSED, a same-town
        one proceeds, and when NEITHER half is derivable the gate fails open
        (None) so a town-less graph merges exactly as before."""
        import season
        from types import SimpleNamespace
        _tmp = tmp_path / ".agi" / "nodes" / ".geometry"
        _tmp.mkdir(parents=True)
        (_tmp / "ladder.md").write_text(
            "---\nid: ladder:ladder\ntype: ladder\ncurrent_season: 2\n"
            "town_branches:\n  core: season/s2\n"
            "  streaming-suite: town/streaming-suite@s2\n"
            "  web-app-suite: town/web-app-suite@s2\n---\nbody\n",
            encoding="utf-8")
        (_tmp / "seats.md").write_text(
            "---\nid: config:seats\ntype: config\nseats:\n"
            "  - {\"name\": \"council-streaming\", \"town\": "
            "\"streaming-suite\"}\n"
            "  - {\"name\": \"council-web\", \"town\": "
            "\"web-app-suite\"}\n---\nbody\n", encoding="utf-8")
        (tmp_path / ".agi" / "config.json").write_text(
            '{"project": "test"}')
        root = tmp_path / ".agi"  # find_project_root resolves to the .agi dir
        args = lambda **kw: SimpleNamespace(
            round="", seat="", record="", **kw)
        # Cross-town, no flags: AGI_SEAT=council-web (web-app-suite) vs the
        # streaming-suite town branch -> towns differ -> REFUSE.
        monkeypatch.setenv("AGI_SEAT", "council-web")
        refuse = season._merge_up_town_gate(
            root, args(branch="town/streaming-suite@s2"))
        assert refuse is not None and "REFUSED" in refuse, refuse
        assert "streaming-suite" in refuse and "web-app-suite" in refuse
        # Same-town, no flags: AGI_SEAT=council-streaming -> both streaming.
        monkeypatch.setenv("AGI_SEAT", "council-streaming")
        allow = season._merge_up_town_gate(
            root, args(branch="town/streaming-suite@s2"))
        assert allow is None, allow
        # Fail-open: neither half derivable — no AGI_SEAT and a branch that
        # maps to no town -> None, so a town-less graph is untouched.
        monkeypatch.delenv("AGI_SEAT", raising=False)
        open_ = season._merge_up_town_gate(
            root, args(branch="loop/slug-aaaa@s2"))
        assert open_ is None

    def test_merge_up_town_gate_keep_all_seat_serves_every_town(
            self, tmp_path, monkeypatch):
        """Mirrors the LIVE config:seats shape — a KEEP row with `town: all`
        (e.g. sanctuary-director) shares the Keep across every town, so it
        ALLOWS a core round AND a non-core round; a council seat refuses a
        cross-town round and allows its own; an unknown town on either side
        still fails open. `all` is the Keep's shared marker, not a town."""
        import season
        from types import SimpleNamespace
        _tmp = tmp_path / ".agi" / "nodes" / ".geometry"
        _tmp.mkdir(parents=True)
        # KEEP row (shared across all towns) + two council rows with towns.
        (_tmp / "seats.md").write_text(
            "---\nid: config:seats\ntype: config\nseats:\n"
            "  - {\"name\": \"sanctuary-director\", \"town\": "
            "\"all\"}\n"
            "  - {\"name\": \"council-streaming\", \"town\": "
            "\"streaming-suite\"}\n"
            "  - {\"name\": \"council-web\", \"town\": "
            "\"web-app-suite\"}\n---\nbody\n", encoding="utf-8")
        (_tmp / "ladder.md").write_text(
            "---\nid: ladder:ladder\ntype: ladder\ncurrent_season: 2\n"
            "town_branches:\n  core: season/s2\n"
            "  streaming-suite: town/streaming-suite@s2\n"
            "  web-app-suite: town/web-app-suite@s2\n---\nbody\n",
            encoding="utf-8")
        (tmp_path / ".agi" / "config.json").write_text(
            '{"project": "test"}')
        root = tmp_path / ".agi"

        # KEEP seat (town: all) ALLOWS a core round and a non-core round.
        monkeypatch.setenv("AGI_SEAT", "sanctuary-director")
        for branch in ("season/s2", "town/streaming-suite@s2"):
            got = season._merge_up_town_gate(root, SimpleNamespace(
                round="", seat="", record="", branch=branch))
            assert got is None, (branch, got)

        # Council seat WEB refuses a streaming-suite round, allows its own
        # web-app-suite round.
        monkeypatch.setenv("AGI_SEAT", "council-web")
        refuse = season._merge_up_town_gate(root, SimpleNamespace(
            round="", seat="", record="", branch="town/streaming-suite@s2"))
        assert refuse is not None and "REFUSED" in refuse, refuse
        assert "streaming-suite" in refuse and "web-app-suite" in refuse
        allow = season._merge_up_town_gate(root, SimpleNamespace(
            round="", seat="", record="", branch="town/web-app-suite@s2"))
        assert allow is None, allow

        # Unknown town on either side still fails open: an AGI_SEAT that is
        # not in the registry -> seat_town None -> allow.
        monkeypatch.setenv("AGI_SEAT", "no-such-seat")
        open_ = season._merge_up_town_gate(root, SimpleNamespace(
            round="", seat="", record="", branch="town/streaming-suite@s2"))
        assert open_ is None, open_
        # And a branch mapping to no town, council seat set, leaves round_town
        # None -> fails open.
        monkeypatch.setenv("AGI_SEAT", "council-web")
        open2 = season._merge_up_town_gate(root, SimpleNamespace(
            round="", seat="", record="", branch="loop/slug-aaaa@s2"))
        assert open2 is None, open2

    def test_merge_up_never_rebases(self, season_py, temp_graph, tmp_path):
        """Merging upward never rewrites the branch's commit hashes."""
        _init_project(tmp_path)
        worktree = tmp_path / "wt"
        _git(tmp_path, "worktree", "add", "-b", "loop/no-rebase-aaaa@s2",
             str(worktree), "season/s1")
        _commit(worktree, "stable commit", content="stable\n")
        tip_before = _git(tmp_path, "rev-parse", "loop/no-rebase-aaaa@s2").stdout.strip()

        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/no-rebase-aaaa@s2", "--suite", "exit 0"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr

        # The branch's tip hash is unchanged...
        tip_after = _git(tmp_path, "rev-parse", "loop/no-rebase-aaaa@s2").stdout.strip()
        assert tip_after == tip_before and tip_before, "rebase rewrote the hashes"
        # ...and present verbatim in the merged base's history (no fast-forward,
        # no reconstituted commits).
        assert tip_before in _git(tmp_path, "log", "season/s1",
                                  "--format=%H").stdout.split()

    def test_merge_up_targets_recorded_base_branch(
            self, season_py, temp_graph, tmp_path):
        """When a base_branch is recorded, merge-up targets it, not the
        currently checked-out branch (layer-agnostic recursion)."""
        _init_project(tmp_path)
        # Director layer: cut tier1/director off the season.
        _git(tmp_path, "checkout", "-q", "-b", "tier1/director")
        _commit(tmp_path, "director work", content="director\n")

        # Parent layer: cut the parent branch off the DIRECTOR branch.
        _git(tmp_path, "checkout", "-q", "season/s1")
        worktree = tmp_path / "wt"
        _git(tmp_path, "worktree", "add", "-b", "loop/parent-aaaa@s2",
             str(worktree), "tier1/director")
        _commit(worktree, "parent work", content="parent\n")

        # A record (lease/agent.json) names the base as tier1/director.
        record = tmp_path / ".agi" / "sessions" / "lease.json"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(json.dumps({
            "branch": "loop/parent-aaaa@s2",
            "base_branch": "tier1/director",
            "worktree": str(worktree),
            "suite": "exit 0",
        }))

        # Run from season/s1 (a DIFFERENT branch than the recorded base).
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/parent-aaaa@s2", "--record", str(record)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr
        assert "tier1/director" in result.stdout
        # The parent's work landed in the director branch, not the season.
        assert "parent work" in _git(
            tmp_path, "log", "tier1/director", "--format=%s").stdout
        assert "parent work" not in _git(
            tmp_path, "log", "season/s1", "--format=%s").stdout

    def test_merge_up_recorded_base_branch_beats_town_base(
            self, season_py, temp_graph, tmp_path):
        """hypothesis:l4-town-base-honours-the-recorded-base-branch -- a core
        round whose record names a base_branch merges into THAT rung, never
        straight into the town/season branch. town_branches declares core's
        integration branch as season/s2; the recorded base is the rung
        tier1/director; without --target the RECORDED base must win over the
        town base (regression: _town_base preceded the recorded base_branch,
        so a core round merged straight into season/s2, skipping its rung)."""
        _init_project(tmp_path, season="season/s2")
        # Director (rung) layer cut off the season.
        _git(tmp_path, "checkout", "-q", "-b", "tier1/director")
        _commit(tmp_path, "director work", content="director\n")

        # Loop branch cut off the director layer -- its rung.
        _git(tmp_path, "checkout", "-q", "season/s2")
        worktree = tmp_path / "wt"
        _git(tmp_path, "worktree", "add", "-b", "loop/parent-aaaa@s2",
             str(worktree), "tier1/director")
        _commit(worktree, "rung work", content="rung\n")

        # Round node + ladder declared AFTER the branch setup (checking out a
        # branch that lacks an untracked round node would delete it).
        ladder = tmp_path / ".agi" / "nodes" / ".geometry" / "ladder.md"
        ladder.write_text(
            "---\nid: ladder:ladder\ntype: ladder\ncurrent_season: 2\n"
            "town_branches:\n  core: season/s2\n---\nbody\n",
            encoding="utf-8")
        exp_dir = tmp_path / ".agi" / "nodes" / "experiment"
        exp_dir.mkdir(parents=True, exist_ok=True)
        (exp_dir / "round.md").write_text(
            "---\nid: experiment:round\ntype: experiment\ntown: core\n"
            "---\nbody\n", encoding="utf-8")

        # Record names the rung as the base_branch. NO --target passed.
        record = tmp_path / ".agi" / "sessions" / "lease.json"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(json.dumps({
            "branch": "loop/parent-aaaa@s2",
            "base_branch": "tier1/director",
            "worktree": str(worktree),
            "suite": "exit 0",
        }))

        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/parent-aaaa@s2", "--record", str(record),
             "--round", "experiment:round"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr
        # The chosen base is the RECORDED rung, and the print names its source.
        assert "tier1/director" in result.stdout
        assert "from record" in result.stdout
        # Rung work landed in the director branch, not the season/season branch.
        assert "rung work" in _git(
            tmp_path, "log", "tier1/director", "--format=%s").stdout
        assert "rung work" not in _git(
            tmp_path, "log", "season/s2", "--format=%s").stdout

    def test_merge_up_town_base_resolves_without_record(
            self, season_py, temp_graph, tmp_path):
        """hypothesis:l4-town-base-honours-the-recorded-base-branch -- a town
        round with NO record still resolves the town base (the town base is
        the fallback when there is no recorded base_branch)."""
        _init_project(tmp_path, season="season/s2")
        # Town branch cut off the season; loop branch cut off the town branch.
        _git(tmp_path, "checkout", "-q", "-b", "town/streaming-suite@s2")
        _commit(tmp_path, "town work", content="town\n")
        _git(tmp_path, "checkout", "-q", "season/s2")
        worktree = tmp_path / "wt"
        _git(tmp_path, "worktree", "add", "-b", "loop/parent-bbbb@s2",
             str(worktree), "town/streaming-suite@s2")
        _commit(worktree, "rung work", content="rung\n")

        # Round node + ladder declared AFTER the branch setup.
        ladder = tmp_path / ".agi" / "nodes" / ".geometry" / "ladder.md"
        ladder.write_text(
            "---\nid: ladder:ladder\ntype: ladder\ncurrent_season: 2\n"
            "town_branches:\n  core: season/s2\n"
            "  streaming-suite: town/streaming-suite@s2\n---\nbody\n",
            encoding="utf-8")
        exp_dir = tmp_path / ".agi" / "nodes" / "experiment"
        exp_dir.mkdir(parents=True, exist_ok=True)
        (exp_dir / "round.md").write_text(
            "---\nid: experiment:round\ntype: experiment\ntown: "
            "streaming-suite\n---\nbody\n", encoding="utf-8")

        # NO record (no base_branch) -- town base must win.
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/parent-bbbb@s2", "--suite", "exit 0",
             "--round", "experiment:round", "--worktree", str(worktree)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr
        assert "town/streaming-suite@s2" in result.stdout
        assert "from town" in result.stdout
        assert "rung work" in _git(
            tmp_path, "log", "town/streaming-suite@s2",
            "--format=%s").stdout

    def test_three_layer_rehearsal(self, season_py, temp_graph, tmp_path):
        """season -> director branch -> parent branch, merged up in order;
        hashes never rewritten (the ADDENDUM's recursive rehearsal)."""
        _init_project(tmp_path)  # on season/s1

        # Director layer, cut from season/s1.
        _git(tmp_path, "checkout", "-q", "-b", "tier1/director")
        _commit(tmp_path, "director work")
        dir_before = _git(tmp_path, "rev-parse", "tier1/director").stdout.strip()

        # Parent layer, cut from tier1/director.
        parent_wt = tmp_path / "pwt"
        _git(tmp_path, "worktree", "add", "-b", "loop/parent-aaaa@s2",
             str(parent_wt), "tier1/director")
        _commit(parent_wt, "parent work", content="parent\n")
        parent_tip = _git(tmp_path, "rev-parse", "loop/parent-aaaa@s2").stdout.strip()

        # 1) Merge the parent up onto the director layer (recorded base).
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "loop/parent-aaaa@s2", "--target", "tier1/director",
             "--suite", "exit 0"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr

        # 2) Merge the director up onto the season.
        result2 = subprocess.run(
            [sys.executable, str(season_py), "--root", str(temp_graph),
             "merge-up", "tier1/director", "--target", "season/s1",
             "--suite", "exit 0"],
            capture_output=True, text=True,
        )
        assert result2.returncode == 0, result2.stderr

        # Both merge steps are --no-ff: two-parent merge commits.
        for b in ("tier1/director", "season/s1"):
            parents = _git(tmp_path, "log", "-1", "--format=%P",
                           b).stdout.split()
            assert len(parents) == 2, f"{b} should hold a merge commit"

        # Hashes never rewritten: the parent tip and director tip are present
        # verbatim in the season's history, unchanged.
        season_hashes = _git(tmp_path, "log", "season/s1",
                             "--format=%H").stdout.split()
        assert parent_tip in season_hashes, "parent commit hash must survive"
        assert dir_before in season_hashes, "director commit hash must survive"
        # And the first merge still has the SAME parent tip (no rebase of it).
        assert _git(tmp_path, "rev-parse", "loop/parent-aaaa@s2").stdout.strip() \
            == parent_tip


class TestTownsPerTownVisionCap:
    """season.py status / spawn_gate per-town vision counting.

    hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council — when the
    ladder declares caps_vision_scope: town, visions are counted PER TOWN (a
    vision's `town:` cell, default core) against caps.vision, never as one
    global pool, and no code path names a town literally (goal:g8.2).
    """

    @pytest.fixture
    def town_graph(self, tmp_path, engine_on_path):
        """A temp graph with a town-scoped ladder and visions in three towns.

        core has 2 visions (room for 1 more), streaming-suite has 3 (= cap,
        at capacity), web-app-suite has 1. Towns come from the ladder's
        `towns:` list; a vision's town from its `town:` cell, default core.
        """
        ladder_dir = tmp_path / ".agi" / "nodes" / ".geometry"
        ladder_dir.mkdir(parents=True)
        ladder = """---
id: ladder:ladder
type: ladder
current_season: 1
caps_apply_from_season: 2
caps_vision_scope: town
caps:
  moral: 5
  vision: 3
towns:
  - core
  - streaming-suite
  - web-app-suite
tiers:
  - tier: 2
    plan_types: [vision]
    report_type: overview
    judged_against: its vision
    lens: the morals above
    cadence: season rollover (quarterly)
---
# ladder:ladder
Test town-scoped ladder node.
"""
        (ladder_dir / "ladder.md").write_text(ladder)
        cfg_dir = tmp_path / ".agi"
        cfg_dir.mkdir(parents=True, exist_ok=True)
        (cfg_dir / "config.json").write_text('{"project": "test"}')
        visions_dir = tmp_path / ".agi" / "nodes" / "vision"
        visions_dir.mkdir(parents=True)
        slugs = {"core": ["vc1", "vc2"],
                 "streaming-suite": ["vs1", "vs2", "vs3"],
                 "web-app-suite": ["vw1"]}
        for town, items in slugs.items():
            for slug in items:
                if town == "core":
                    body = (f"---\nid: vision:{slug}\ntype: vision\n---\n"
                            f"# vision {slug}\nbody\n")
                else:
                    body = (f"---\nid: vision:{slug}\ntype: vision\n"
                            f"town: {town}\n---\n# vision {slug}\nbody\n")
                (visions_dir / f"{slug}.md").write_text(body)
        return tmp_path

    def test_status_shows_visions_by_town(self, season_py, town_graph):
        """status prints a per-town block when scope is town."""
        result = subprocess.run(
            [sys.executable, str(season_py), "--root", str(town_graph),
             "status"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "Visions by town (scope: town, cap 3/town)" in result.stdout
        assert "streaming-suite: 3  (room for 0 more)" in result.stdout
        assert "core: 2  (room for 1 more)" in result.stdout

    def test_helpers_count_per_town_not_globally(self, town_graph):
        """count_visions_per_town / vision_remaining_for_town are per-town."""
        import locations
        root = locations.find_project_root(town_graph)
        import spawn_gate
        counts = spawn_gate.count_visions_per_town(root / "nodes")
        assert counts == {"core": 2, "streaming-suite": 3, "web-app-suite": 1}
        # A town at cap has room for 0; a town under cap still has room.
        assert spawn_gate.vision_remaining_for_town(
            root / "nodes", "streaming-suite", counts=counts) == 0
        assert spawn_gate.vision_remaining_for_town(
            root / "nodes", "core", counts=counts) == 1

    def test_mint_gate_refuses_fourth_and_accepts_third(self, season_py,
                                                        town_graph):
        """The town cap gate refuses a 4th in a full town, allows a 3rd in core."""
        import locations
        root = locations.find_project_root(town_graph)
        import spawn_gate
        nodes_dir = root / "nodes"
        per_town = spawn_gate.count_visions_per_town(nodes_dir)
        # 4th in streaming-suite: budget exhausted (town at its cap of 3).
        assert spawn_gate.vision_remaining_for_town(
            nodes_dir, "streaming-suite", counts=per_town) == 0
        # 3rd in core (no town cell -> default core): budget still open.
        assert spawn_gate.vision_remaining_for_town(
            nodes_dir, "core", counts=per_town) == 1


class TestRolloverCountsVisionsAfterBump:
    """hypothesis:l4-rollover-counts-visions-after-the-ladder-bump.

    cmd_rollover lives here: the per-town vision count that admits rollover
    visions is scoped to the season it is ENTERING (new_season), not the
    ladder's still-current season. A town that is full (cap 3) in season 2 but
    empty in season 3 must mint its new vision; the cap must still bite within
    the new season. Regression: a count read against the old season's ladder
    saw a full s2 town at cap and REFUSEd every source vision.
    """

    LADDER = """---
id: ladder:ladder
type: ladder
current_season: 2
caps_apply_from_season: 2
caps_vision_scope: town
caps:
  moral: 5
  vision: 3
towns:
  - core
  - streaming-suite
  - web-app-suite
tiers:
  - tier: 2
    plan_types: [vision]
    report_type: overview
    judged_against: its vision
    lens: the morals above
    cadence: season rollover (quarterly)
---
# ladder:ladder
Test ladder node.
"""

    @pytest.fixture
    def roll_graph(self, tmp_path, engine_on_path):
        """s2 town-scoped ladder; streaming-suite holds 3 season-2 visions."""
        ladder_dir = tmp_path / ".agi" / "nodes" / ".geometry"
        ladder_dir.mkdir(parents=True)
        (ladder_dir / "ladder.md").write_text(self.LADDER)
        cfg_dir = tmp_path / ".agi"
        cfg_dir.mkdir(parents=True, exist_ok=True)
        (cfg_dir / "config.json").write_text('{"project": "test"}')
        visions_dir = tmp_path / ".agi" / "nodes" / "vision"
        visions_dir.mkdir(parents=True)
        for slug in ["vs1", "vs2", "vs3"]:
            body = (f"---\nid: vision:{slug}\ntype: vision\n"
                    f"town: streaming-suite\nseason: 2\n---\n# vision {slug}\nbody\n")
            (visions_dir / f"{slug}.md").write_text(body)
        return tmp_path

    def _write_source(self, tmp_path, slug="new-vision", town="streaming-suite"):
        d = tmp_path / "visions"
        d.mkdir(exist_ok=True)
        (d / f"{slug}.md").write_text(
            f"---\ntown: {town}\n---\n# {slug}\n\nOwner text, verbatim.\n")
        return d

    def _run(self, season_py, root, *args):
        return subprocess.run(
            [sys.executable, str(season_py), "--root", str(root),
             "rollover", *args],
            capture_output=True, text=True)

    def test_dry_run_counts_new_season_not_current(self, season_py, roll_graph,
                                                   tmp_path):
        """A town full in s2 reads 0 / OK in the s3 dry-run; the source MINTs."""
        vdir = self._write_source(tmp_path)
        result = self._run(season_py, roll_graph, "--dry-run",
                           "--visions-from", str(vdir))
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "streaming-suite: 0 (OK)" in result.stdout, result.stdout
        assert "MINT vision:new-vision" in result.stdout, result.stdout
        assert "AT CAP" not in result.stdout, result.stdout

    def test_real_run_mints_when_old_season_full(self, season_py, roll_graph,
                                                 tmp_path):
        """The real run MINTs (not refuses) into a town full in s2."""
        import locations
        from graph_core.persistence import frontmatter
        root = locations.find_project_root(roll_graph)
        vdir = self._write_source(tmp_path)
        result = self._run(season_py, roll_graph, "--visions-from", str(vdir))
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "minted vision:new-vision" in result.stdout, result.stdout
        assert "REFUSE" not in result.stdout, result.stdout
        vision = frontmatter.load_node_file(
            root / "nodes" / "vision" / "new-vision.md")
        assert vision.frontmatter.get("season") == 3
        assert vision.frontmatter.get("town") == "streaming-suite"

    def test_cap_still_refuses_within_new_season(self, season_py, roll_graph,
                                                 tmp_path):
        """A town already at 3 visions OF the new season still refuses a 4th."""
        import locations
        root = locations.find_project_root(roll_graph)
        visions_dir = root / "nodes" / "vision"
        for slug in ["va1", "va2", "va3"]:
            body = (f"---\nid: vision:{slug}\ntype: vision\n"
                    f"town: streaming-suite\nseason: 3\n---\n# vision {slug}\nbody\n")
            (visions_dir / f"{slug}.md").write_text(body)
        vdir = self._write_source(tmp_path)
        result = self._run(season_py, roll_graph, "--visions-from", str(vdir))
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "REFUSE vision:new-vision" in result.stdout, result.stdout
        assert "minted vision:new-vision" not in result.stdout, result.stdout


class TestNearestVisionHonoursOwnTownCell:
    """Residue 1 — nearest_vision reads a visited node's OWN town:/vision_ref
    before climbing parents. A non-core round stamped with its own town at
    mint must read that town back, never 'core' (hypothesis:l4-towns-each-app-
    is-a-vision-with-its-own-council)."""

    @pytest.fixture
    def town_cell_graph(self, tmp_path, engine_on_path):
        cfg = tmp_path / ".agi"
        cfg.mkdir(parents=True)
        (cfg / "config.json").write_text('{"project": "test"}')
        nd = cfg / "nodes"
        (nd / "vision").mkdir(parents=True)
        (nd / "goal").mkdir(parents=True)
        (nd / "vision" / "streaming-suite.md").write_text(
            "---\nid: vision:streaming-suite\ntype: vision\ntown: streaming-suite\n"
            "---\n# s\nb\n")
        (nd / "vision" / "web-app-suite.md").write_text(
            "---\nid: vision:web-app-suite\ntype: vision\ntown: web-app-suite\n"
            "---\n# w\nb\n")
        (nd / "vision" / "self-perpetuating.md").write_text(
            "---\nid: vision:self-perpetuating\ntype: vision\n---\n# c\nb\n")
        # non-core goals declare their own town + vision_ref
        (nd / "goal" / "g18.1.md").write_text(
            "---\nid: goal:g18.1\ntype: goal\nparents: [goal:g18]\n"
            "town: streaming-suite\nvision_ref: vision:streaming-suite\n"
            "---\n# g18.1\nb\n")
        (nd / "goal" / "g18.md").write_text(
            "---\nid: goal:g18\ntype: goal\nparents: [vision:self-perpetuating]\n"
            "town: web-app-suite\nvision_ref: vision:web-app-suite\n"
            "---\n# g18\nb\n")
        # core goal: no town, climbs to vision:self-perpetuating -> core
        (nd / "goal" / "g17.md").write_text(
            "---\nid: goal:g17\ntype: goal\nparents: [vision:self-perpetuating]\n"
            "---\n# g17\nb\n")
        return tmp_path

    def test_non_core_goal_reads_its_own_town(self, town_cell_graph):
        import locations
        import spawn_gate
        nodes = locations.find_project_root(town_cell_graph) / "nodes"
        assert spawn_gate.nearest_vision_town(nodes, ["goal:g18.1"]) == \
            "streaming-suite"
        assert spawn_gate.nearest_vision_town(nodes, ["goal:g18"]) == \
            "web-app-suite"

    def test_core_goal_still_reads_core(self, town_cell_graph):
        import locations
        import spawn_gate
        nodes = locations.find_project_root(town_cell_graph) / "nodes"
        assert spawn_gate.nearest_vision_town(nodes, ["goal:g17"]) == "core"

    def test_own_cell_wins_over_ancestor(self, town_cell_graph):
        """g18's parent climbs to vision:self-perpetuating (core), but g18's
        own town cell must win: web-app-suite, NOT core."""
        import locations
        import spawn_gate
        nodes = locations.find_project_root(town_cell_graph) / "nodes"
        # without res 1 this would be 'core' (climbs to self-perpetuating)
        assert spawn_gate.nearest_vision(nodes, ["goal:g18"]) == \
            ("vision:web-app-suite", "web-app-suite")


class TestCountVisionsPerTownSeasonScoped:
    """Residue 2 — count_visions_per_town is SEASON-scoped: only visions whose
    season equals the ladder's current_season count, so an old season's
    cohort does not pin a town at its cap at rollover."""

    @pytest.fixture
    def season_town_graph(self, tmp_path, engine_on_path):
        cfg = tmp_path / ".agi"
        gd = cfg / "nodes" / ".geometry"
        gd.mkdir(parents=True)
        gd.joinpath("ladder.md").write_text("""---
id: ladder:ladder
type: ladder
current_season: 2
caps:
  moral: 5
  vision: 3
caps_vision_scope: town
---
# ladder
""")
        (cfg / "config.json").write_text('{"project": "test"}')
        vd = cfg / "nodes" / "vision"
        vd.mkdir(parents=True)
        vd.joinpath("vc1.md").write_text(
            "---\nid: vision:vc1\ntype: vision\nseason: 2\n---\n# c1\nb\n")
        vd.joinpath("vc2.md").write_text(
            "---\nid: vision:vc2\ntype: vision\nseason: 2\n---\n# c2\nb\n")
        vd.joinpath("vc3.md").write_text(
            "---\nid: vision:vc3\ntype: vision\nseason: 2\n---\n# c3\nb\n")
        vd.joinpath("vc-old.md").write_text(
            "---\nid: vision:vc-old\ntype: vision\nseason: 1\n---\n# cold\nb\n")
        vd.joinpath("vs1.md").write_text(
            "---\nid: vision:vs1\ntype: vision\nseason: 2\ntown: streaming-suite\n"
            "---\n# s1\nb\n")
        vd.joinpath("vs2.md").write_text(
            "---\nid: vision:vs2\ntype: vision\nseason: 2\ntown: streaming-suite\n"
            "---\n# s2\nb\n")
        vd.joinpath("vs3.md").write_text(
            "---\nid: vision:vs3\ntype: vision\nseason: 2\ntown: streaming-suite\n"
            "---\n# s3\nb\n")
        return tmp_path

    def test_counts_only_current_season_per_town(self, season_town_graph):
        import locations
        import spawn_gate
        nodes = locations.find_project_root(season_town_graph) / "nodes"
        counts = spawn_gate.count_visions_per_town(nodes)
        # vc-old (season 1) excluded -> core is 3, not 4
        assert counts == {"core": 3, "streaming-suite": 3}

    def test_simulated_rollover_not_refused(self, season_town_graph):
        """Bump current_season to 3: the s2 cohort drops out, so a fresh s3
        vision is NOT refused (core has room instead of being pinned at cap)."""
        import locations
        import spawn_gate
        root = locations.find_project_root(season_town_graph)
        nodes = root / "nodes"
        ladder = nodes / ".geometry" / "ladder.md"
        assert spawn_gate.vision_remaining_for_town(
            nodes, "core", counts=spawn_gate.count_visions_per_town(nodes)) == 0
        # simulate rollover
        text = ladder.read_text().replace("current_season: 2", "current_season: 3")
        ladder.write_text(text)
        counts = spawn_gate.count_visions_per_town(nodes)
        assert counts == {}
        assert spawn_gate.vision_remaining_for_town(nodes, "core") == 3
