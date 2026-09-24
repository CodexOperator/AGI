import json, shutil, subprocess, sys
from pathlib import Path

CLI = Path(__file__).parents[1] / "bin" / "cli.py"
REPO = Path(__file__).parents[3]

def run(root, artifact):
    return subprocess.run([sys.executable, str(CLI), "ingest", str(artifact), "--root", str(root)], text=True, capture_output=True)

def setup(tmp_path):
    root = tmp_path / ".agi"
    (root / "config.json").parent.mkdir(parents=True)
    (root / "config.json").write_text("{}")
    shutil.copytree(REPO / ".agi" / "context", root / "context")
    goal_dir = root / "nodes" / "goal"
    goal_dir.mkdir(parents=True)
    shutil.copy(REPO / ".agi" / "nodes" / "goal" / "g7.32.1.md", goal_dir / "g7.32.1.md")
    return root, tmp_path / "session.jsonl"

def test_distinct_safe_ids_and_exact_id_update_preserve_provenance(tmp_path):
    root, artifact = setup(tmp_path)
    outputs = []
    for sid, text in [("A.B", "dot"), ("A-B", "dash")]:
        artifact.write_text(json.dumps({
            "session_id": sid, "actor": f"actor-{sid}", "text": text,
            "thought_session": f"thought-{sid}", "goal": "g7.32.1"}) + "\n")
        got = run(root, artifact)
        assert got.returncode == 0, got.stderr
        outputs.append(got.stdout)
    assert outputs[0] != outputs[1]
    files = list((root / "nodes" / "doc").glob("*.md"))
    assert len(files) == 2
    combined = "\n".join(path.read_text() for path in files)
    assert '["str","A.B"]' in combined and '["str","A-B"]' in combined
    assert "actor-A.B" in combined and "actor-A-B" in combined
    assert "dot" in combined and "dash" in combined

    artifact.write_text(json.dumps({"session_id": "A.B", "text": "changed"}) + "\n")
    updated = run(root, artifact)
    assert updated.returncode == 0 and updated.stdout == outputs[0]
    assert len(list((root / "nodes" / "doc").glob("*.md"))) == 2
    node = next(path for path in files if "A.B" in path.read_text())
    text = node.read_text()
    assert "changed" in text and "actor-A.B" in text
    assert "parents:" in text and "goal:g7.32.1" in text

def test_requires_resolved_live_goal_and_keeps_refusals(tmp_path):
    root, artifact = setup(tmp_path)
    artifact.write_text(json.dumps({"session_id": "no-goal", "text": "orphan"}) + "\n")
    got = run(root, artifact)
    assert got.returncode == 2 and "no live goal" in got.stderr
    assert not (root / "nodes" / "doc").exists() or not list((root / "nodes" / "doc").glob("*.md"))

    artifact.write_text(json.dumps({"session_id": "bad-goal", "goal": "g-does-not-exist"}) + "\n")
    got = run(root, artifact)
    assert got.returncode == 2 and "does not resolve" in got.stderr

    for value, reason in [("x/../../../escaped", "path"), ({"x": 1}, "scalar"), ("a:b", "YAML")]:
        artifact.write_text(json.dumps({"session_id": value, "goal": "g7.32.1"}) + "\n")
        got = run(root, artifact)
        assert got.returncode == 2 and reason.lower() in got.stderr.lower()
    artifact.write_text("not json\n")
    got = run(root, artifact)
    assert got.returncode == 2 and "refusing" in got.stderr
    assert not (root.parent / "escaped.md").exists()
