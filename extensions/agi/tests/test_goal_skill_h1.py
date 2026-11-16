"""skill agi-goal: the body file starts at `## Why this exists`, because `write_node` writes the `# goal:<id>` heading itself.

DGo1's finding (aio 14:04:26Z, SM's placement 14:1xZ 11-16): 63 of 811 goal nodes carried the heading twice. The template a poster copies
(skill section 3) began with `# goal:gX.Y`, and write_node ALWAYS writes `# <node_id>` before the body, so following the skill minted two.

Rows, each with its mutant:
 h1 TEXT   section 3's fenced template has no `# goal:` first line, and section 1 says the body starts at `## Why this exists`;
           mutant: the old first line put back = the row reads RED
 h2 MINT   write_node on a body that starts where the skill says (`## Why this exists`) mints the heading ONCE;
           control (h2m): the counter itself reads a doubled heading as 2, so h2 can read RED
The writer's own behaviour on a body that already carries the heading is the engine leaf's (a later tip) and is NOT asserted here.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "extensions" / "agi" / "bin"))

import node_writer  # noqa: E402

SKILL = REPO / "skills" / "agi-goal" / "SKILL.md"


def template_first_line(text: str) -> str:
    """The first line inside the ``` fence that follows the '## 3 ·' heading."""
    after = text.split("## 3 ·", 1)[1]
    fence = after.split("```", 2)[1]
    return fence.lstrip("\n").splitlines()[0]


def heading_count(text: str, goal_id: str) -> int:
    return len(re.findall(rf"^# goal:{re.escape(goal_id)}\s*$", text, re.M))


def test_h1_the_skill_template_does_not_start_with_the_heading_and_section_1_says_where_the_body_starts():
    text = SKILL.read_text()
    first = template_first_line(text)
    assert not first.startswith("# goal:"), f"section 3's template still starts with the heading: {first!r}"
    assert "STARTS AT `## Why this exists`" in text, "section 1 must say where the body starts"


def test_h1m_mutant_the_old_first_line_back_is_red():
    text = SKILL.read_text()
    old = text.replace("(the `# goal:gX.Y` heading is written by write_node (§1): the body file starts at the next line)\n", "# goal:gX.Y\n", 1)
    assert old != text, "the mutant must change the text (anchor missing)"
    assert template_first_line(old).startswith("# goal:"), "the mutant must read the old first line"


def _mint(tmp_path: Path, goal_id: str, body: str) -> str:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "context").symlink_to(REPO / ".agi" / "context")
    parent = graph / "nodes" / "goal" / "g1.md"
    parent.write_text("---\nid: goal:g1\ntype: goal\nmint_id: 00000000000000000000000000000001\ntitle: parent\ngoal_id: G1\ngoal_kind: perpetual\n"
                      "status: active\norigin: goal\nseeds: []\nconfidence: 0.5\ntags: []\nparents: []\n---\n\n# goal:g1\n")
    r = node_writer.write_node(str(graph), "goal", goal_id, ["goal:g1"], extra_fm={
        "goal_id": goal_id.upper(), "goal_kind": "subgoal", "status": "active", "confidence": 0.5, "origin": "goal",
        "seeds": [], "tags": [], "title": f"{goal_id.upper()}: scratch"}, body=body)
    assert r.status == "written", (r.status, r.reason)
    return (graph / "nodes" / "goal" / f"{goal_id}.md").read_text()


def test_h2_a_body_that_starts_where_the_skill_says_mints_the_heading_once(tmp_path):
    text = _mint(tmp_path, "g1.1", "## Why this exists\nx\n")
    assert heading_count(text, "g1.1") == 1, text


def test_h2m_the_counter_notices_a_doubled_heading():
    """The reader must SEE a doubled heading, or h2 could never read RED. A pure-text control: it does not depend on the writer, so the
    engine leaf (write_node skipping its own heading) cannot make it stale."""
    doubled = "# goal:g1.2\n\n# goal:g1.2\n\n## Why this exists\nx\n"
    assert heading_count(doubled, "g1.2") == 2
    assert heading_count("# goal:g1.2\n\n## Why this exists\nx\n", "g1.2") == 1
