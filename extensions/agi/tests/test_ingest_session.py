"""Falsifier for goal:g7.32.1 — extensions/agi/bin/ingest_session.py.

Session artifact -> graph node, idempotently, with provenance, and a refusal
path that writes nothing. All runs point --root at a tmp `.agi/`; the real
graph is snapshotted before and after and must be byte-untouched.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
CLI = BIN / "ingest_session.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "grok_session_fixture.json"
REAL_NODES = Path(__file__).resolve().parents[3] / ".agi" / "nodes"

SHAPE = """---
name: shape
structural: true
parentless_types:
  - goal:long-term
  - goal:short-term
max_parents_ceiling: 2
canonical_type_spelling: underscore
---
shape
"""
HYP = ("---\nname: hypothesis\nvalidation:\n  required: [id, type, mint_id, title, "
       "testable_claim]\nspawn:\n  allowed_parents: [idea, goal, experiment, hypothesis]\n"
       "  min_parents: 1\n  max_parents: 2\n---\nhypothesis\n")
EXP = ("---\nname: experiment\nspawn:\n  allowed_parents: [hypothesis, idea]\n"
       "  min_parents: 1\n  max_parents: 2\n---\nexperiment\n")


@pytest.fixture
def graph(tmp_path):
    """A throwaway graph root shaped `<tmp>/.agi/`, with the schemas it needs."""
    root = tmp_path / ".agi"
    sd = root / "context" / "schemas"
    sd.mkdir(parents=True)
    (sd / "[shape].md").write_text(SHAPE)
    (sd / "[hypothesis].md").write_text(HYP)
    (sd / "[experiment].md").write_text(EXP)
    gd = root / "nodes" / "goal"
    gd.mkdir(parents=True)
    (gd / "g1.md").write_text(
        "---\nid: goal:g1\ntype: goal\nmint_id: deadbeef\n---\n\na goal\n")
    return root


def _run(*args):
    return subprocess.run([sys.executable, str(CLI), *args],
                          capture_output=True, text=True)


def _nodes(root):
    return sorted((root / "nodes").rglob("grok-session-*.md"))


def _snapshot(root):
    return {str(p): p.stat().st_mtime_ns for p in root.rglob("*.md")} if root.exists() else {}


def _mint_id(path):
    for line in path.read_text().splitlines():
        if line.startswith("mint_id:"):
            return line.split(":", 1)[1].strip()
    return ""


def test_ingest_writes_then_skips_same_node(graph, tmp_path):
    before_real = _snapshot(REAL_NODES)
    r1 = _run(str(FIXTURE), "--parent", "goal:g1", "--root", str(graph))
    assert r1.returncode == 0, r1.stderr
    assert r1.stdout.startswith("written hypothesis:"), r1.stdout
    node_id = r1.stdout.split()[1]

    files = _nodes(graph)
    assert len(files) == 1, files
    text = files[0].read_text()
    assert "edited_by: grok-bot-742" in text
    assert "thought_session: grok-session-fixture-2026-09-23" in text
    mint1 = _mint_id(files[0])
    assert mint1

    r2 = _run(str(FIXTURE), "--parent", "goal:g1", "--root", str(graph))
    assert r2.returncode == 0, r2.stderr
    assert r2.stdout.startswith("skipped "), r2.stdout
    assert "already exists" in r2.stdout
    assert r2.stdout.split()[1] == node_id
    assert len(_nodes(graph)) == 1
    assert _mint_id(_nodes(graph)[0]) == mint1

    assert _snapshot(REAL_NODES) == before_real


@pytest.mark.parametrize("bad", ["empty", "malformed", "missing"])
def test_refusal_writes_no_node(graph, tmp_path, bad):
    before = len(_nodes(graph))
    if bad == "empty":
        art = tmp_path / "empty.json"
        art.write_text("")
    elif bad == "malformed":
        art = tmp_path / "broken.json"
        art.write_text("{not json")
    else:
        art = tmp_path / "nope.json"
    r = _run(str(art), "--parent", "goal:g1", "--root", str(graph))
    assert r.returncode != 0
    assert "refused:" in r.stderr
    assert len(_nodes(graph)) == before
