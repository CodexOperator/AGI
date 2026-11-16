"""goal:g7.16.1.11.46.38 -- write_node mints ONE heading for its node whatever the body begins with.

`write_node` built `# <node_id>` and appended ANY body after it (node_writer.py, scaffold_body), so a body that already began with the
node's own heading, bare or titled, minted it twice. It now skips its own when the body's FIRST non-blank line is `# <node_id>` followed
by end of line or whitespace (a TOKEN boundary, not a prefix). Every row counts with that same token-boundary form, so the titled shape
counts (an exact counter would read it as 0 and F4's RED could not fire).

Rows (each with a mutant, run by patching the one helper or scaffold_hash):
 F2 own heading in the body        -> ONE.            mutant: the writer adds its own anyway = two
 F3 no heading in the body         -> the writer's.   mutant: always skip = zero
 F4 titled own id                  -> ONE, titled.    mutant: exact-only match = two
 F5 token boundary g1.2 vs g1.25.1 -> both kept.      mutant: prefix match swallows the writer's
 F6 others: `# Overview`, a fence, heading=False.     mutants: always skip / any-line scan
 F7 idempotent: the stored scaffold_hash is the hash of the bytes written.  mutant: hash over the pre-skip body
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "extensions" / "agi" / "bin"))

import node_writer  # noqa: E402


def _mint(tmp_path: Path, goal_id: str, body: str, heading: bool = True) -> str:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "goal").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text("{}")
    if not (graph / "context").exists():
        (graph / "context").symlink_to(REPO / ".agi" / "context")
    parent = graph / "nodes" / "goal" / "g1.md"
    parent.write_text("---\nid: goal:g1\ntype: goal\nmint_id: 00000000000000000000000000000001\ntitle: parent\ngoal_id: G1\ngoal_kind: perpetual\n"
                      "status: active\norigin: goal\nseeds: []\nconfidence: 0.5\ntags: []\nparents: []\n---\n\n# goal:g1\n")
    r = node_writer.write_node(str(graph), "goal", goal_id, ["goal:g1"], extra_fm={
        "goal_id": goal_id.upper(), "goal_kind": "subgoal", "status": "active", "confidence": 0.5, "origin": "goal",
        "seeds": [], "tags": [], "title": f"{goal_id.upper()}: scratch"}, body=body, heading=heading)
    assert r.status == "written", (r.status, r.reason)
    return (graph / "nodes" / "goal" / f"{goal_id}.md").read_text()


def own(text: str, goal_id: str) -> int:
    """The token-boundary counter: `# goal:<id>` then whitespace or the end of the line."""
    return len(re.findall(rf"^# goal:{re.escape(goal_id)}(\s|$)", text, re.M))


def h1s(text: str) -> list[str]:
    return [l for l in text.splitlines() if l.startswith("# ")]


# ---- the mutants: each replaces the ONE helper -------------------------------------------------------------------------------------
def m_adds_anyway(body, node_id): return False
def m_always_skips(body, node_id): return True
def m_exact_only(body, node_id):
    first = next((l for l in body.splitlines() if l.strip()), "")
    return first.rstrip() == f"# {node_id}"
def m_prefix(body, node_id):
    first = next((l for l in body.splitlines() if l.strip()), "")
    return first.startswith(f"# {node_id}")
def m_any_line(body, node_id):
    return any(re.match(rf"# {re.escape(node_id)}(\s|$)", l) for l in body.splitlines())


def patched(monkeypatch, fn):
    monkeypatch.setattr(node_writer, "_body_opens_with_own_heading", fn)


BARE = "# goal:g1.2\n\n## Why this exists\nx\n"
TITLED = "# goal:g1.2 — a title\n\n## Why this exists\nx\n"
OTHER = "# goal:g1.25.1 — other\n\n## Why this exists\nx\n"
FENCE = "```\n# goal:g1.2\n```\n\n## Why this exists\nx\n"
LATE = "## Why this exists\nx\n\n# goal:g1.2\n"


def test_f2_a_body_with_its_own_heading_mints_one(tmp_path):
    assert own(_mint(tmp_path, "g1.2", BARE), "g1.2") == 1


def test_f2m_mutant_the_writer_adds_its_own_anyway_is_red(tmp_path, monkeypatch):
    patched(monkeypatch, m_adds_anyway)
    assert own(_mint(tmp_path, "g1.2", BARE), "g1.2") == 2


def test_f3_a_body_with_no_heading_gets_the_writers_one(tmp_path):
    assert own(_mint(tmp_path, "g1.2", "## Why this exists\nx\n"), "g1.2") == 1


def test_f3m_mutant_always_skip_mints_zero(tmp_path, monkeypatch):
    patched(monkeypatch, m_always_skips)
    assert own(_mint(tmp_path, "g1.2", "## Why this exists\nx\n"), "g1.2") == 0


def test_f4_a_titled_own_id_mints_one_and_it_is_the_titled_one(tmp_path):
    text = _mint(tmp_path, "g1.2", TITLED)
    assert own(text, "g1.2") == 1
    assert "# goal:g1.2 — a title" in text


def test_f4m_mutant_exact_only_keeps_the_bare_heading_too(tmp_path, monkeypatch):
    patched(monkeypatch, m_exact_only)
    assert own(_mint(tmp_path, "g1.2", TITLED), "g1.2") == 2


def test_f5_g1_2_is_not_swallowed_by_g1_25_1(tmp_path):
    text = _mint(tmp_path, "g1.2", OTHER)
    assert own(text, "g1.2") == 1 and own(text, "g1.25.1") == 1, h1s(text)


def test_f5m_mutant_a_prefix_match_swallows_the_writers_heading(tmp_path, monkeypatch):
    patched(monkeypatch, m_prefix)
    assert own(_mint(tmp_path, "g1.2", OTHER), "g1.2") == 0


def test_f6_overview_keeps_both(tmp_path):
    text = _mint(tmp_path, "g1.2", "# Overview\n\nx\n")
    assert h1s(text).count("# goal:g1.2") == 1 and "# Overview" in h1s(text)


def test_f6_heading_false_adds_none_and_skips_none(tmp_path):
    assert own(_mint(tmp_path, "g1.2", "## Why\nx\n", heading=False), "g1.2") == 0
    assert own(_mint(tmp_path / "b", "g1.2", BARE, heading=False), "g1.2") == 1


def test_f6_a_fence_or_a_late_heading_is_never_the_first_heading(tmp_path):
    assert own(_mint(tmp_path / "f", "g1.2", FENCE), "g1.2") == 2  # the writer's, and the one inside the fence
    assert own(_mint(tmp_path / "l", "g1.2", LATE), "g1.2") == 2   # the writer's, and the late one


def test_f6m_mutants_always_skip_and_any_line_read_red(tmp_path, monkeypatch):
    patched(monkeypatch, m_always_skips)
    assert "# goal:g1.2" not in h1s(_mint(tmp_path / "a", "g1.2", "# Overview\n\nx\n"))  # Overview row would now read RED
    patched(monkeypatch, m_any_line)
    assert own(_mint(tmp_path / "b", "g1.2", LATE), "g1.2") == 1  # the late heading swallowed the writer's: the fence/late row reads RED


def test_f7_the_stored_scaffold_hash_is_the_hash_of_the_bytes_written(tmp_path):
    text = _mint(tmp_path, "g1.2", BARE)
    sp = node_writer.split_frontmatter(text)
    stored = re.search(r"^scaffold_hash: (\S+)", text, re.M).group(1)
    assert stored == node_writer.scaffold_hash(sp[1])


def test_f7m_mutant_a_hash_over_the_pre_skip_body_is_red(tmp_path, monkeypatch):
    real = node_writer.scaffold_hash
    monkeypatch.setattr(node_writer, "scaffold_hash", lambda b: real("\n# goal:g1.2\n\n" + b.lstrip("\n")))
    text = _mint(tmp_path, "g1.2", BARE)
    sp = node_writer.split_frontmatter(text)
    stored = re.search(r"^scaffold_hash: (\S+)", text, re.M).group(1)
    assert stored != real(sp[1])


# F5b (sp 14:31:41Z): the id's dots are regex wildcards unless escaped: `goal:g1x2` must not read as a heading for `goal:g1.2`
XDOT = "# goal:g1x2 — other\n\n## Why this exists\nx\n"


def m_unescaped(body, node_id):
    first = next((l for l in body.splitlines() if l.strip()), "")
    return re.match(r"# " + node_id + r"(\s|$)", first) is not None


def test_f5b_a_dot_in_the_id_is_not_a_wildcard(tmp_path):
    assert own(_mint(tmp_path, "g1.2", XDOT), "g1.2") == 1


def test_f5bm_mutant_an_unescaped_id_swallows_the_writers_heading(tmp_path, monkeypatch):
    patched(monkeypatch, m_unescaped)
    assert own(_mint(tmp_path, "g1.2", XDOT), "g1.2") == 0


def test_f7b_is_complete_reads_the_same_with_or_without_the_heading_in_the_body(tmp_path):
    """alive 14:33:30Z: the stamp is what completion reads; a body carrying its own heading must read as the same mint without one."""
    import completion
    _mint(tmp_path / "a", "g1.2", BARE)
    _mint(tmp_path / "b", "g1.2", "## Why this exists\nx\n")
    assert completion.is_complete(tmp_path / "a" / ".agi", "goal:g1.2") == completion.is_complete(tmp_path / "b" / ".agi", "goal:g1.2")
