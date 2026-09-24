from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import session_ingest

def _graph(tmp_path):
    (tmp_path / "config.json").parent.mkdir(exist_ok=True)
    (tmp_path / "config.json").write_text("{}")
    (tmp_path / "nodes" / "goal").mkdir(parents=True)
    (tmp_path / "nodes" / "goal" / "g7.32.1.md").write_text("---\nid: goal:g7.32.1\ntype: goal\n---\n")
    (tmp_path / "context" / "schemas").mkdir(parents=True)
    (tmp_path / "context" / "schemas" / "[experiment].md").write_text("---\nname: experiment\nspawn:\n  allowed_parents: [hypothesis, idea]\n  min_parents: 1\n  max_parents: 2\n---\n")
    return tmp_path

def test_fixture_lands_node_and_reingest_is_idempotent(tmp_path):
    root = _graph(tmp_path)
    artifact = tmp_path / "fixture.json"
    artifact.write_text(json.dumps({"session_id": "grok-42", "actor": "seat"}))
    first = session_ingest.ingest(root, artifact, parent="goal:g7.32.1", actor="seat")
    second = session_ingest.ingest(root, artifact, parent="goal:g7.32.1", actor="seat")
    assert first.status == "written" and first.path.exists()
    assert first.node_id == second.node_id == "experiment:grok-session-grok-42"
    assert second.status == "skipped"
    assert first.path.read_text().count('mint_id:') == 1
    assert "edited_by: seat" in first.path.read_text()
    assert "thought_session: grok-42" in first.path.read_text()

def test_session_id_changes_identity_not_filename(tmp_path):
    root = _graph(tmp_path)
    a = tmp_path / "one.json"; a.write_text('{"session_id":"alpha"}')
    b = tmp_path / "two.json"; b.write_text('{"session_id":"beta"}')
    assert session_ingest.ingest(root, a).node_id != session_ingest.ingest(root, b).node_id
