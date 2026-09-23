"""Hermetic tests for bin/ingest_session.py (goal:g7.32.1).

Every run points --root at a throwaway graph under tmp_path, so nothing here
touches the live .agi/nodes/. A live run over the real root writes the same
bytes; the only difference is which root --root names.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin" / "ingest_session.py"

ARTIFACT = {
    "harness": "grok-bot",
    "session_id": "grok-sess-2026-09-23-test",
    "path": "sessions/grok/x.json",
    "summary": "a director helper round",
}


def run(root, *artifacts):
    return subprocess.run(
        [sys.executable, str(BIN), "--root", str(root), *map(str, artifacts)],
        capture_output=True, text=True,
    )


def node_files(root):
    return sorted(p.name for p in (root / "nodes").rglob("*.md"))


def fm_of(path):
    return yaml.safe_load(path.read_text().split("---", 2)[1])


def fixture(tmp_path, name="a.json", **overrides):
    root = tmp_path / ".agi"
    (root / "nodes").mkdir(parents=True, exist_ok=True)
    p = tmp_path / name
    p.write_text(json.dumps({**ARTIFACT, **overrides}))
    return root, p


def test_first_ingest_writes_node_and_prints_id(tmp_path):
    root, art = fixture(tmp_path)
    res = run(root, art)
    assert res.returncode == 0, res.stderr
    files = node_files(root)
    assert len(files) == 1
    node_id = next(p.stem for p in (root / "nodes").rglob("*.md"))
    assert node_id in res.stdout, res.stdout


def test_rerun_is_idempotent(tmp_path):
    root, art = fixture(tmp_path)
    first = run(root, art)
    second = run(root, art)
    assert first.returncode == second.returncode == 0
    assert first.stdout.split()[0] == second.stdout.split()[0]
    assert "exists" in second.stdout
    assert len(node_files(root)) == 1


def test_parent_and_provenance_preserved(tmp_path):
    root, art = fixture(tmp_path)
    run(root, art)
    node = next((root / "nodes").rglob("*.md"))
    fm = fm_of(node)
    assert fm["parents"] == ["goal:g7.32.1"]
    assert fm["edited_by"] == "ingest_session"
    assert fm["thought_session"] == ""
    assert fm["ingest_harness"] == "grok-bot"


def test_edited_by_flag_is_preserved(tmp_path):
    root, art = fixture(tmp_path)
    res = subprocess.run(
        [sys.executable, str(BIN), "--root", str(root),
         "--edited-by", "a00-test", "--thought-session", "sess-x", str(art)],
        capture_output=True, text=True,
    )
    assert res.returncode == 0, res.stderr
    fm = fm_of(next((root / "nodes").rglob("*.md")))
    assert fm["edited_by"] == "a00-test"
    assert fm["thought_session"] == "sess-x"


def test_malformed_is_refused_by_name(tmp_path):
    root, art = fixture(tmp_path, session_id="")
    res = run(root, art)
    assert res.returncode != 0
    assert "REFUSED" in res.stderr and "session_id" in res.stderr
    assert "Traceback" not in res.stderr
    assert node_files(root) == []


@pytest.mark.parametrize("value,typename", [
    ([ARTIFACT], "list"),
    (None, "NoneType"),
    (42, "int"),
    ("x", "str"),
])
def test_non_object_json_is_refused(tmp_path, value, typename):
    root, _ = fixture(tmp_path)
    p = tmp_path / "nonobject.json"
    p.write_text(json.dumps(value))
    res = run(root, p)
    assert res.returncode != 0
    assert "REFUSED" in res.stderr
    assert "nonobject.json" in res.stderr and typename in res.stderr
    assert "Traceback" not in res.stderr
    assert node_files(root) == []


def test_empty_agi_named_dir_without_nodes_is_refused(tmp_path):
    root = tmp_path / ".agi"
    root.mkdir()
    p = tmp_path / "a.json"
    p.write_text(json.dumps(ARTIFACT))
    res = run(root, p)
    assert res.returncode != 0
    assert "REFUSED" in res.stderr and "--root" in res.stderr
    assert not (root / "nodes").exists()


def test_non_graph_root_is_refused(tmp_path):
    root, art = fixture(tmp_path)
    bogus = tmp_path / "plain"
    bogus.mkdir()
    res = run(bogus, art)
    assert res.returncode != 0
    assert "REFUSED" in res.stderr
    assert not (bogus / "nodes").exists()


def test_two_sessions_do_not_collide(tmp_path):
    root, a = fixture(tmp_path, "a.json")
    b = tmp_path / "b.json"
    b.write_text(json.dumps({**ARTIFACT, "session_id": "other-session"}))
    run(root, a, b)
    assert len(node_files(root)) == 2