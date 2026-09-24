import json, subprocess, sys
from pathlib import Path

CLI = Path(__file__).parents[1] / "bin" / "cli.py"

def run(root, artifact):
    return subprocess.run([sys.executable, str(CLI), "ingest", str(artifact), "--root", str(root)], text=True, capture_output=True)

def test_first_reingest_and_refusal(tmp_path):
    root = tmp_path / ".agi"; (root / "config.json").parent.mkdir(parents=True); (root / "config.json").write_text("{}")
    artifact = tmp_path / "session.jsonl"
    artifact.write_text(json.dumps({"session_id": "grok-7", "actor": "grok", "thought_session": "run-7", "text": "hello"}) + "\n")
    first = run(root, artifact)
    assert first.returncode == 0 and first.stdout.startswith("doc:session-grok-7-")
    second = run(root, artifact)
    assert second.returncode == 0 and second.stdout == first.stdout
    assert len(list((root / "nodes" / "doc").glob("*.md"))) == 1
    assert "edited_by: grok" in (root / "nodes" / "doc").glob("*.md").__next__().read_text()
    bad = tmp_path / "bad.jsonl"; bad.write_text("")
    refused = run(root, bad)
    assert refused.returncode == 2 and "refusing" in refused.stderr
