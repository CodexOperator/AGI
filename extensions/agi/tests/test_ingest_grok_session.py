"""Tests for bin/ingest_grok_session.py (goal:g7.32.1 first ingest kid).

Falsifier conjuncts under test: (1) a fixture yields >=1 node id on stdout and
a file under nodes/agent_session/; (2) a re-ingest reuses the same node address
and does not fork a second mint_id; (3) a malformed fixture is refused BY NAME
with no node written. The wire is `node_writer.write_node`, so one test spies
that call site rather than trusting the file's existence alone.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import ingest_grok_session  # noqa: E402
import node_writer  # noqa: E402
from frontmatter import read_frontmatter  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "grok_session_sample.jsonl"


def _temp_graph(tmp_path: Path) -> Path:
    """A minimal graph root: the activated schema, shape geometry, one goal parent."""
    schemas = tmp_path / "context" / "schemas"
    schemas.mkdir(parents=True)
    for name in ("[agent_session].md", "[shape].md"):
        shutil.copy(REPO / ".agi" / "context" / "schemas" / name, schemas / name)
    goal = tmp_path / "nodes" / "goal"
    goal.mkdir(parents=True)
    (goal / "g7.32.1.md").write_text(
        "---\nid: goal:g7.32.1\nmint_id: deadbeef\ntype: goal\ntitle: target\n---\n",
        encoding="utf-8")
    return tmp_path


def _fm(path: Path) -> dict:
    return read_frontmatter(path.read_text(encoding="utf-8"))


def test_fixture_mints_one_node_and_reports_its_id(tmp_path):
    root = _temp_graph(tmp_path)
    result = ingest_grok_session.ingest(root, FIXTURE)
    assert result["status"] == node_writer.WRITTEN, result["reason"]
    assert result["node_id"].startswith("agent_session:")
    files = list((root / "nodes" / "agent_session").glob("*.md"))
    assert len(files) == 1
    fm = _fm(files[0])
    assert fm["id"] == result["node_id"]
    assert fm["parents"] == ["goal:g7.32.1"]
    assert fm["edited_by"] == "grok-bot"
    assert fm["thought_session"] == "owner-ask-2026-09-21"
    assert fm["session_id"] == "grok-9f3a2b7c-2026-09-22"
    assert fm["tags"] == ["agent-session", "grok", "session-ingest"]


def test_reingest_reuses_the_node_and_mint_id(tmp_path):
    root = _temp_graph(tmp_path)
    first = ingest_grok_session.ingest(root, FIXTURE)
    mint_before = _fm(
        root / "nodes" / "agent_session" / (first["node_id"].split(":", 1)[1] + ".md"))["mint_id"]
    second = ingest_grok_session.ingest(root, FIXTURE)
    assert second["node_id"] == first["node_id"]
    assert second["status"] == node_writer.SKIPPED
    files = list((root / "nodes" / "agent_session").glob("*.md"))
    assert len(files) == 1, [f.name for f in files]
    assert _fm(files[0])["mint_id"] == mint_before


def test_malformed_fixtures_are_refused_by_name(tmp_path):
    root = _temp_graph(tmp_path)
    for name, text in (
        ("empty.jsonl", ""),
        ("no_header.jsonl", '{"turns": []}\n'),
        ("bad_turn.jsonl", '{"session_id": "s", "agent_id": "a"}\nnot json\n'),
    ):
        bad = tmp_path / name
        bad.write_text(text, encoding="utf-8")
        with pytest.raises(ingest_grok_session.Refusal) as exc:
            ingest_grok_session.ingest(root, bad)
        assert str(exc.value)
    assert not list((root / "nodes" / "agent_session").glob("*.md"))


def test_creation_goes_through_the_gated_writer(tmp_path, monkeypatch):
    root = _temp_graph(tmp_path)
    calls = []
    real = node_writer.write_node

    def spy(*args, **kwargs):
        calls.append((args, kwargs))
        return real(*args, **kwargs)

    monkeypatch.setattr(node_writer, "write_node", spy)
    ingest_grok_session.ingest(root, FIXTURE)
    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args[0] == root and args[1] == "agent_session"
    assert kwargs["parents"] == ["goal:g7.32.1"]


def test_cli_prints_node_id_then_named_refusal_on_reuse(tmp_path):
    root = _temp_graph(tmp_path)
    env = {"PATH": "/usr/bin:/bin"}
    cmd = [sys.executable, str(BIN / "ingest_grok_session.py"),
           "--fixture", str(FIXTURE), "--root", str(root)]
    first = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(REPO))
    assert first.returncode == 0
    assert first.stdout.strip().splitlines()[-1].startswith("agent_session:")
    bad = tmp_path / "bad.jsonl"
    bad.write_text('{"turns": []}\n', encoding="utf-8")
    second = subprocess.run(
        [cmd[0], cmd[1], "--fixture", str(bad), "--root", str(root)],
        capture_output=True, text=True, env=env, cwd=str(REPO))
    assert second.returncode == 2
    assert second.stdout.strip().splitlines()[-1].startswith("refused: missing-session_id")
