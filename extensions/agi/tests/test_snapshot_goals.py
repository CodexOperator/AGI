"""Tests for bin/snapshot-goals.py — GOALS.md → nodes/goal/ (TODO L15)."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin" / "snapshot-goals.py"
spec = importlib.util.spec_from_file_location("snapshot_goals", BIN)
sg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sg)


GOALS_DOC = """# GOALS.md — sample

Preamble prose that must be ignored, including a stray G9 mention.

---

## G1 — Playable dungeon crawler (sandbox ladder) — status: active

Upgrade the scene one node at a time.

## G2 — Persistent ideation system — status: active

Adapt the research loop.

## G3 — Marketplace with proof-of-playtime — status: horizon

Design sketch only.

## G5 — Retired experiment — status: mothballed

Status value outside the taxonomy.

## G4 — Movement system

No status clause here.
"""


def run(project: Path, *args):
    """Run the script in-process-ish via subprocess for isolation."""
    return subprocess.run(
        [sys.executable, str(BIN), "--project", str(project), *args],
        capture_output=True, text=True,
    )


@pytest.fixture()
def project(tmp_path):
    (tmp_path / "GOALS.md").write_text(GOALS_DOC, encoding="utf-8")
    (tmp_path / "nodes").mkdir()
    return tmp_path


def fm_of(path: Path) -> dict:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    return yaml.safe_load(parts[1]) or {}


def goal_nodes(project: Path) -> dict:
    out = {}
    for p in sorted((project / "nodes" / "goal").glob("*.md")):
        out[fm_of(p)["id"]] = (p, fm_of(p))
    return out


def write_node(project: Path, rel: str, fm: dict, body: str = "body"):
    path = project / "nodes" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    sg.write_frontmatter(path, fm, body)
    return path


# --- 1. parsing ------------------------------------------------------------


def test_parses_ids_titles_statuses(project):
    r = run(project)
    assert r.returncode == 0, r.stderr
    nodes = goal_nodes(project)
    assert set(nodes) == {"goal:g1", "goal:g2", "goal:g3", "goal:g4", "goal:g5"}

    path, fm = nodes["goal:g1"]
    assert fm["goal_id"] == "G1"
    assert fm["title"] == "G1: Playable dungeon crawler (sandbox ladder)"
    assert fm["status"] == "active"
    assert fm["type"] == "goal"
    assert fm["origin"] == "goals-doc"
    assert fm["tags"] == ["goal", "root"]
    assert fm["confidence"] == 1.0
    assert path.name.startswith("g1-playable-dungeon-crawler")
    assert "Upgrade the scene one node at a time." in path.read_text()
    # preamble ignored, body stops at the next `## ` heading
    assert "Preamble prose" not in path.read_text()
    assert "Adapt the research loop" not in path.read_text()

    # missing `status:` clause defaults to active
    assert nodes["goal:g4"][1]["status"] == "active"
    assert nodes["goal:g4"][1]["title"] == "G4: Movement system"


def test_no_next_edges_emitted(project):
    run(project)
    for _path, fm in goal_nodes(project).values():
        assert "next_edges" not in fm
        assert "parents" not in fm


# --- 2. unknown status -----------------------------------------------------


def test_unknown_status_preserved_and_warns(project):
    r = run(project)
    assert r.returncode == 0
    assert goal_nodes(project)["goal:g5"][1]["status"] == "mothballed"
    assert "WARN: goal G5 has unrecognized status 'mothballed'" in r.stderr


def test_horizon_is_a_known_status(project):
    # `horizon` is in the taxonomy: a goal declared but not yet being worked.
    r = run(project)
    assert goal_nodes(project)["goal:g3"][1]["status"] == "horizon"
    assert "horizon" not in r.stderr


# --- 3. seeds from parents -------------------------------------------------


def test_seeds_populated_from_parent_pointer(project):
    write_node(project, "idea/seed-a.md",
               {"id": "idea:seed-a", "type": "idea", "parents": ["goal:g1"]})
    write_node(project, "idea/seed-b.md",
               {"id": "idea:seed-b", "type": "idea", "parents": ["goal:g1"]})
    r = run(project)
    assert r.returncode == 0
    nodes = goal_nodes(project)
    assert nodes["goal:g1"][1]["seeds"] == ["idea:seed-a", "idea:seed-b"]
    assert nodes["goal:g2"][1]["seeds"] == []


# --- 4. referential integrity ---------------------------------------------


def test_unknown_goal_ref_warns_but_exits_zero(project):
    write_node(project, "idea/orphan.md",
               {"id": "idea:orphan", "type": "idea", "parents": ["goal:g99"]})
    r = run(project)
    assert r.returncode == 0
    assert "INTEGRITY" in r.stderr
    assert "unknown goal 'goal:g99'" in r.stderr
    assert "orphan.md" in r.stderr


def test_unknown_goal_ref_fails_under_strict(project):
    write_node(project, "idea/orphan.md",
               {"id": "idea:orphan", "type": "idea", "parents": ["goal:g99"]})
    r = run(project, "--strict")
    assert r.returncode == 1
    assert "INTEGRITY" in r.stderr
    # goal nodes are still written even in strict mode
    assert set(goal_nodes(project)) == {"goal:g1", "goal:g2", "goal:g3", "goal:g4", "goal:g5"}


def test_strict_exits_zero_when_all_refs_resolve(project):
    write_node(project, "idea/seed-a.md",
               {"id": "idea:seed-a", "type": "idea", "parents": ["goal:g2"]})
    r = run(project, "--strict")
    assert r.returncode == 0


# --- 5. pruning ------------------------------------------------------------


def test_prune_removes_stale_goals_doc_but_spares_agent_nodes(project):
    stale = write_node(project, "goal/g42-obsolete.md",
                       {"id": "goal:g42", "type": "goal", "origin": "goals-doc"})
    agent = write_node(project, "goal/hand-written.md",
                       {"id": "goal:hand-written", "type": "goal"})
    other = write_node(project, "goal/from-build-site.md",
                       {"id": "goal:bs", "type": "goal", "origin": "build-site"})
    r = run(project)
    assert r.returncode == 0
    assert not stale.exists()
    assert agent.exists()
    assert other.exists()


def test_prune_removes_renamed_slug_duplicate(project):
    old = write_node(project, "goal/g1-old-title.md",
                     {"id": "goal:g1", "type": "goal", "origin": "goals-doc"})
    r = run(project)
    assert r.returncode == 0
    assert not old.exists()
    assert len(list((project / "nodes" / "goal").glob("g1-*.md"))) == 1


# --- 6. missing GOALS.md ---------------------------------------------------


def test_missing_goals_md_is_noop_and_prunes_nothing(tmp_path):
    (tmp_path / "nodes").mkdir()
    keep = write_node(tmp_path, "goal/g1-existing.md",
                      {"id": "goal:g1", "type": "goal", "origin": "goals-doc"})
    r = run(tmp_path)
    assert r.returncode == 0
    assert "skipping" in r.stdout
    assert keep.exists()


# --- 7. idempotence --------------------------------------------------------


def test_idempotent_byte_identical(project):
    write_node(project, "idea/seed-a.md",
               {"id": "idea:seed-a", "type": "idea", "parents": ["goal:g1"]})
    assert run(project).returncode == 0
    first = {p.name: p.read_bytes()
             for p in sorted((project / "nodes" / "goal").glob("*.md"))}
    assert run(project).returncode == 0
    second = {p.name: p.read_bytes()
              for p in sorted((project / "nodes" / "goal").glob("*.md"))}
    assert first == second
    assert first  # non-empty


# --- parser unit -----------------------------------------------------------


def test_parse_goals_body_cap():
    text = "## G1 — Big — status: active\n\n" + ("x" * 6000)
    goals = sg.parse_goals(text)
    assert len(goals[0]["body"]) == 4000


# --------------------------------------------- H0i: re-snapshot must not strip

def test_resnapshot_preserves_fields_the_snapshot_does_not_own(project):
    """Regression: rebuilding frontmatter from GOALS.md dropped everything else.

    The same defect in snapshot-build-site.py severed `next_edges` on 15 nodes
    of the live agi-tree corpus — chain structure deleted by a render pass.
    """
    assert run(project).returncode == 0
    node = next((project / "nodes" / "goal").glob("g1-*.md"))

    text = node.read_text(encoding="utf-8")
    head, body = text.split("---", 2)[1], text.split("---", 2)[2]
    node.write_text(
        f"---{head}next_edges:\n  - idea:seeded\nembedding_coords: [0.1, 0.2]\n"
        f"---{body}",
        encoding="utf-8",
    )

    assert run(project).returncode == 0
    fm = fm_of(node)
    assert fm["next_edges"] == ["idea:seeded"]
    assert "embedding_coords" in fm
    # Snapshot-owned fields still come from GOALS.md, not the old file.
    assert fm["status"] == "active"
    assert fm["goal_id"] == "G1"
