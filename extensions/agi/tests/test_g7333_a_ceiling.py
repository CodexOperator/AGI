"""g7.33.3(a) NO-PI focused pins — CEILING engine-units wording + measured↔recorded."""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.skip(reason='retired engine surface (symbol or CLI is gone); skipped instead of keeping dead code green: source-suffix ceiling wording is retired')

import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import brief  # noqa: E402
import cli  # noqa: E402


def test_brief_ceiling_says_source_suffix_engine_units():
    """g7.33.3(a): brief CEILING line names engine units, not vague 'paths'."""
    kid = "\n".join(brief._kid(
        agent_id="a00-test",
        iter_n=1,
        cli_py="/x/cli.py",
        scaffold=None,
        line_ceiling=40,
        ceiling_source="clause",
    ))
    assert "source-suffix lines" in kid
    assert "data files never count" in kid
    assert "ENGINE UNITS" in kid
    assert "git diff --numstat" in kid
    assert "production paths you were given" not in kid


def test_hypothesis_schema_ceiling_says_source_suffix():
    """g7.33.3(a): [hypothesis] schema CEILING says source-suffix; data never count."""
    root = Path(__file__).resolve().parents[3]
    schema = root / ".agi" / "context" / "schemas" / "[hypothesis].md"
    if not schema.is_file():
        schema = root / "context" / "schemas" / "[hypothesis].md"
    text = schema.read_text(encoding="utf-8")
    assert "source-suffix lines; data files never count" in text
    assert "10-12 production lines per conjunct" not in text


def test_kid_budget_notes_prints_measured_beside_recorded(tmp_path, monkeypatch):
    """g7.33.3(a): harvest notes carry measured= beside recorded=."""
    graph = tmp_path / ".agi"
    nodes = graph / "nodes" / "experiment"
    nodes.mkdir(parents=True)
    nid = "experiment:kid-a"
    nf = nodes / "kid-a.md"
    nf.write_text(
        "---\nid: experiment:kid-a\ntype: experiment\n"
        "title: real title\nproduction_lines: 12\nline_ceiling: 40\n---\n"
        "body\n",
        encoding="utf-8",
    )
    (graph / "config.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(cli, "_find_node_file",
                        lambda root, node_id: nf if node_id == nid else None)
    monkeypatch.setattr(cli, "_kid_measured_lines",
                        lambda root, agent_id: 15)
    monkeypatch.setattr(cli, "_kid_line_ceiling",
                        lambda root, fm, target=None: 40)

    notes = cli._kid_budget_notes(
        graph, [{"id": "a00-kid", "node_id": nid, "target": nid}])
    assert f"lines=[{nid} measured=15 recorded=12]" in notes
