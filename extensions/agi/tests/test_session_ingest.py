import json, subprocess, sys
from pathlib import Path

CLI = Path(__file__).parents[1] / "bin" / "cli.py"

def run(root, artifact):
    return subprocess.run([sys.executable, str(CLI), "ingest", str(artifact), "--root", str(root)], text=True, capture_output=True)

def setup(tmp_path):
    root = tmp_path / ".agi"; (root / "config.json").parent.mkdir(parents=True); (root / "config.json").write_text("{}")
    return root, tmp_path / "session.jsonl"

def test_stable_reingest_update_provenance_and_empty(tmp_path):
    root, artifact = setup(tmp_path)
    artifact.write_text(json.dumps({"session_id": "grok-7", "actor": "grok", "thought_session": "run-7", "text": "hello", "goal": "g7"}) + "\n")
    first = run(root, artifact)
    assert first.returncode == 0 and first.stdout == "doc:session-grok-7\n"
    artifact.write_text(json.dumps({"session_id": "grok-7", "actor": "grok", "thought_session": "run-8", "text": "changed"}) + "\n")
    second = run(root, artifact)
    assert second.returncode == 0 and second.stdout == first.stdout
    files = list((root / "nodes" / "doc").glob("*.md")); assert len(files) == 1
    text = files[0].read_text(); assert "changed" in text and "run-8" in text and "run-7" not in text
    assert 'edited_by: "grok"' in text and 'parents: [\'goal:g7\']' in text
    bad = tmp_path / "bad.jsonl"; bad.write_text("")
    refused = run(root, bad)
    assert refused.returncode == 2 and "refusing" in refused.stderr

def test_rejects_traversal_non_scalar_yaml_and_malformed(tmp_path):
    root, artifact = setup(tmp_path)
    for value, reason in [("x/../../../escaped", "path"), ({"x": 1}, "scalar"), ("a:b", "YAML")]:
        artifact.write_text(json.dumps({"session_id": value}) + "\n")
        got = run(root, artifact)
        assert got.returncode == 2 and reason.lower() in got.stderr.lower()
    artifact.write_text("not json\n")
    got = run(root, artifact)
    assert got.returncode == 2 and "refusing" in got.stderr
    assert not (root.parent / "escaped.md").exists()
    assert not (root / "nodes" / "doc").exists() or not any((root / "nodes" / "doc").glob("*.md"))
