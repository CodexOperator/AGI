import json, shutil, subprocess, sys
from pathlib import Path

CLI = Path(__file__).parents[1] / "bin" / "cli.py"
REPO = Path(__file__).parents[3]

def run(root, artifact, *args):
    return subprocess.run([sys.executable, str(CLI), "ingest", str(artifact), "--root", str(root), *args], text=True, capture_output=True)

def setup(tmp_path):
    root = tmp_path / ".agi"
    (root / "config.json").parent.mkdir(parents=True)
    (root / "config.json").write_text("{}")
    shutil.copytree(REPO / ".agi" / "context", root / "context")
    goal_dir = root / "nodes" / "goal"
    goal_dir.mkdir(parents=True)
    shutil.copy(REPO / ".agi" / "nodes" / "goal" / "g7.32.1.md", goal_dir / "g7.32.1.md")
    return root, tmp_path / "session.jsonl"

def test_cli_controls_ingest_real_pi_shape_and_refuse_conflicts(tmp_path):
    root, artifact = setup(tmp_path)
    artifact.write_text(json.dumps({"tool": "read", "timestamp": "now", "text": "first"}) + "\n")
    got = run(root, artifact, "--session-id", "external-1", "--goal", "g7.32.1")
    assert got.returncode == 0, got.stderr
    assert got.stdout.strip().startswith("doc:session-external-1-")
    assert "first" in next((root / "nodes" / "doc").glob("*.md")).read_text()
    conflict = run(root, artifact, "--session-id", "external-1", "--goal", "g7.32.1")
    assert conflict.returncode == 0
    artifact.write_text(json.dumps({"session_id": "embedded", "goal": "g7.32.1"}) + "\n")
    bad = run(root, artifact, "--session-id", "external-2", "--goal", "g7.32.1")
    assert bad.returncode == 2 and "conflicting CLI session_id" in bad.stderr


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

def test_mixed_jsonl_preserves_non_object_records(tmp_path):
    root, artifact = setup(tmp_path)
    artifact.write_text("\n".join([
        json.dumps({"session_id": "mixed", "goal": "g7.32.1", "text": "object"}),
        json.dumps("important scalar transcript record"),
        json.dumps([1, 2]),
        "null",
    ]) + "\n")
    got = run(root, artifact)
    assert got.returncode == 0, got.stderr
    node = next((root / "nodes" / "doc").glob("*.md")).read_text()
    assert "important scalar transcript record" in node
    assert '"text": "object"' in node
    assert '[\n    1,\n    2\n  ]' in node
    assert "\n  null\n" in node


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

    artifact.write_text("   \n")
    got = run(root, artifact)
    assert got.returncode == 2 and "empty session artifact" in got.stderr

    artifact.write_text(json.dumps({
        "session_id": "safe-id", "goal": "../../../outside"}) + "\n")
    got = run(root, artifact)
    assert got.returncode == 2
    assert "does not resolve" in got.stderr or "path" in got.stderr.lower()
    assert not (root.parent / "outside.md").exists()


def test_latest_n_is_completed_only_stable_and_reports_every_failure(tmp_path):
    root, _ = setup(tmp_path)
    sessions = tmp_path / "sessions"
    for agent, finished, status, text in [
        ("a-old", 10, "done", json.dumps({"text": "old"})),
        ("a-new", 20, "done", "not-json"),
        ("a-live", 30, "running", json.dumps({"text": "must skip selection"})),
    ]:
        session = sessions / agent
        session.mkdir(parents=True)
        (session / "trajectory.jsonl").write_text(text + "\n")
        (session / "agent.json").write_text(json.dumps({
            "status": status, "started_at": finished, "finished_at": finished}))

    def batch():
        return subprocess.run([
            sys.executable, str(CLI), "ingest", "--sessions-root", str(sessions),
            "--last", "2", "--root", str(root), "--goal", "g7.32.1",
        ], text=True, capture_output=True)

    first = batch()
    assert first.returncode == 1
    assert first.stdout.strip().startswith("doc:session-a-old-")
    assert f"REFUSED {sessions / 'a-new' / 'trajectory.jsonl'}" in first.stderr
    assert "a-live" not in first.stdout + first.stderr
    assert len(list((root / "nodes" / "doc").glob("*.md"))) == 1

    (sessions / "a-new" / "trajectory.jsonl").write_text(
        json.dumps({"text": "checkpoint update"}) + "\n")
    second = batch()
    assert second.returncode == 0
    ids = second.stdout.splitlines()
    assert len(ids) == 2 and ids[1].startswith("doc:session-a-new-")
    assert len(list((root / "nodes" / "doc").glob("*.md"))) == 2
    assert batch().stdout == second.stdout


def test_malformed_agent_metadata_refuses_without_substitution(tmp_path):
    root, _ = setup(tmp_path)
    sessions = tmp_path / "sessions"
    for name, metadata in (("good", json.dumps({"status": "done", "finished_at": 1})),
                           ("newer-broken", "not-json")):
        session = sessions / name
        session.mkdir(parents=True)
        (session / "trajectory.jsonl").write_text('{"text": "visible"}\\n')
        (session / "agent.json").write_text(metadata)
    got = subprocess.run([
        sys.executable, str(CLI), "ingest", "--sessions-root", str(sessions),
        "--last", "1", "--root", str(root), "--goal", "g7.32.1",
    ], text=True, capture_output=True)
    assert got.returncode == 2
    assert str(sessions / "newer-broken" / "trajectory.jsonl") in got.stderr
    assert "unreadable agent metadata" in got.stderr
    assert not got.stdout
    assert not (root / "nodes" / "doc").exists() or not list((root / "nodes" / "doc").glob("*.md"))


def test_batch_requires_goal_and_never_partially_selects_short_set(tmp_path):
    root, _ = setup(tmp_path)
    sessions = tmp_path / "sessions"
    session = sessions / "a-one"
    session.mkdir(parents=True)
    (session / "trajectory.jsonl").write_text(json.dumps({"text": "one"}) + "\n")
    (session / "agent.json").write_text(json.dumps({"status": "done", "finished_at": 1}))
    base = [sys.executable, str(CLI), "ingest", "--sessions-root", str(sessions),
            "--last", "1", "--root", str(root)]
    assert subprocess.run(base, text=True, capture_output=True).returncode == 2
    short = subprocess.run(base + ["--goal", "g7.32.1", "--last", "2"],
                           text=True, capture_output=True)
    assert short.returncode == 2 and "only 1 completed artifacts" in short.stderr
    assert not (root / "nodes" / "doc").exists() or not list((root / "nodes" / "doc").glob("*.md"))


def test_live_cli_assigns_one_mint_and_update_keeps_it(tmp_path):
    root, artifact = setup(tmp_path)
    artifact.write_text(json.dumps({
        "session_id": "mint-once", "actor": "original-actor",
        "thought_session": "original-thought", "seat": "prime",
        "goal": "g7.32.1"}) + "\n")
    created = run(root, artifact)
    assert created.returncode == 0, created.stderr
    nid = created.stdout.strip()
    assert nid.startswith("doc:session-mint-once-")

    node = next((root / "nodes" / "doc").glob("*.md"))
    first = node.read_text()
    mint_line = next(line for line in first.splitlines() if line.startswith("mint_id:"))
    assert mint_line.removeprefix("mint_id: ").strip()

    artifact.write_text(json.dumps({
        "session_id": "mint-once", "text": "second checkpoint"}) + "\n")
    updated = run(root, artifact)
    assert updated.returncode == 0, updated.stderr
    assert updated.stdout.strip() == nid
    assert list((root / "nodes" / "doc").glob("*.md")) == [node]
    second = node.read_text()
    assert next(line for line in second.splitlines() if line.startswith("mint_id:")) == mint_line
    for preserved in ("original-actor", "original-thought", "prime", "goal:g7.32.1"):
        assert preserved in second
    assert "second checkpoint" in second
