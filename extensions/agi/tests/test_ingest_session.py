"""Falsifier for goal:g7.32.1 -- a session transcript becomes ONE graph node,
idempotently, and a malformed input is refused by name rather than dropped.

Three conjuncts, one test each:
  1. fresh ingest mints a node file under <root>/nodes/ and prints its id;
  2. a second ingest of the same fixture prints the SAME id and mints nothing;
  3. a malformed / non-session input exits non-zero with a readable reason.

The schema is copied from the live graph so the gate is the real one, not a
relaxed fixture.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
BIN = REPO / "extensions" / "agi" / "bin"
CLI = BIN / "ingest_session.py"
SESSION = "019ddd0f-6751-75bc-a374-6c0fe036e262"


def _fixture(path):
    rows = [
        {"type": "session", "version": 3, "id": SESSION,
         "timestamp": "2026-04-30T06:24:27.474Z", "cwd": "/home/ubuntu/.hermes/agi"},
        {"type": "message", "id": "m1",
         "message": {"role": "user", "content": [{"type": "text", "text": "hello graph"}]}},
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


@pytest.fixture
def graph(tmp_path):
    root = tmp_path / "graph"
    (root / "nodes").mkdir(parents=True)
    shutil.copytree(REPO / ".agi" / "context", root / "context")
    return root


def run(session, root, *extra):
    return subprocess.run(
        [sys.executable, str(CLI), str(session), "--out-root", str(root), *extra],
        capture_output=True, text=True)


def test_fresh_ingest_mints_one_node_under_nodes(graph, tmp_path):
    session = _fixture(tmp_path / "s.jsonl")
    p = run(session, graph)
    assert p.returncode == 0, p.stderr
    assert re.match(r"INGEST ok doc:grok-session-\S+$", p.stdout.strip()), p.stdout
    node_id = p.stdout.split()[-1]
    files = list((graph / "nodes").rglob("*.md"))
    assert len(files) == 1 and files[0].name == f"{node_id.split(':')[1]}.md"
    text = files[0].read_text(encoding="utf-8")
    assert f"source_session: {SESSION}" in text
    assert "edited_by: ingest_session.py" in text


def test_reingest_is_idempotent(graph, tmp_path):
    session = _fixture(tmp_path / "s.jsonl")
    first = run(session, graph)
    node = list((graph / "nodes").rglob("*.md"))[0]
    mint = re.search(r"^mint_id: (\S+)$", node.read_text(encoding="utf-8"), re.M).group(1)
    second = run(session, graph)
    assert second.returncode == 0, second.stderr
    assert second.stdout.split()[-1] == first.stdout.split()[-1]
    assert second.stdout.strip().startswith("INGEST skip")
    files = list((graph / "nodes").rglob("*.md"))
    assert len(files) == 1
    assert re.search(r"^mint_id: (\S+)$", files[0].read_text(encoding="utf-8"), re.M).group(1) == mint


@pytest.mark.parametrize("body", ["", '{"type":"model_change"}\n'])
def test_malformed_input_is_refused_by_name(graph, tmp_path, body):
    bad = tmp_path / "bad.jsonl"
    bad.write_text(body, encoding="utf-8")
    p = run(bad, graph)
    assert p.returncode != 0
    assert "INGEST refuse" in p.stderr
    assert "no-session-record" in p.stderr
    assert list((graph / "nodes").rglob("*.md")) == []