"""ingest_grok_session.py pins the falsifiers of `goal:g7.32.1`.

1. a fixture grok session produces a real node id on stdout and a file under
   `.agi/nodes/`;
2. re-ingest of the SAME fixture returns the same id and forks no second
   `mint_id` (mint ids are random, so the `source_session` lookup IS the
   idempotency);
3. a malformed/empty artifact is refused by name and writes no node;
4. missing provenance is refused by name and writes no node;
5. `--scan DIR` ingests every artifact in stable sorted order, a per-artifact
   refusal does not abort the batch, a second scan mints nothing new, and the
   exit code is non-zero iff zero artifacts ingested.

The root is a throwaway graph, never the live one.
"""

import importlib.util
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
FIXDIR = Path(__file__).resolve().parent / "fixtures"
FIXTURE = FIXDIR / "grok-session-sample.jsonl"
BATCH_B = FIXDIR / "grok-session-batch-b.jsonl"
MALFORMED = FIXDIR / "grok-session-malformed.jsonl"
EMPTY = FIXDIR / "grok-session-empty.jsonl"
# Provenance is required; flagless tests must supply it like any other caller.
PROV = ["--actor", "tester", "--thought-session", "test-session"]

SHAPE = """\
---
name: shape
structural: true
parentless_types:
  - goal:long-term
  - idea
max_parents_ceiling: 2
canonical_type_spelling: underscore
---
shape
"""

SCHEMAS = {
    "[hypothesis].md": "allowed_parents: [goal, idea, hypothesis, experiment]\n  min_parents: 1\n  max_parents: 2",
    "[goal].md": "allowed_parents: [goal]\n  min_parents: 1\n  max_parents: 2",
}


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ingest = _load("ingest_grok_session")
fm_reader = ingest.fm_reader


def _project(tmp_path):
    g = tmp_path / ".agi"
    (g / "context" / "schemas").mkdir(parents=True)
    (g / "config.json").write_text("{}")
    (g / "context" / "schemas" / "[shape].md").write_text(SHAPE)
    for fname, spawn in SCHEMAS.items():
        (g / "context" / "schemas" / fname).write_text(
            f"---\nname: {fname[1:-4]}\nspawn:\n  {spawn}\n---\n{fname[1:-4]}\n")
    goal = g / "nodes" / "goal"
    goal.mkdir(parents=True)
    (goal / "g7.32.1.md").write_text(
        "---\nid: goal:g7.32.1\ntype: goal\n---\n\nbody\n")
    return g


def _node_files(root):
    return sorted((root / "nodes").rglob("*.md"))


def test_ingest_mints_node_with_provenance(tmp_path, capsys):
    root = _project(tmp_path)
    before = len(_node_files(root))
    rc = ingest.main([str(FIXTURE), "--root", str(tmp_path), *PROV])
    out = capsys.readouterr().out.strip()
    assert rc == 0, out
    assert out.startswith("hypothesis:grok-")
    node = ingest.node_writer.find_node_file(root, out)
    assert node is not None and node.exists()
    assert len(_node_files(root)) == before + 1
    fm = fm_reader.load_node_file(node, body=False).frontmatter
    assert fm["source_session"] == "grok-2026-09-22-abc123"
    assert fm["ingest_source"] == "grok-session"
    assert fm["parents"] == ["goal:g7.32.1"]
    assert fm["mint_id"]


def test_reingest_returns_same_id_no_second_mint(tmp_path, capsys):
    root = _project(tmp_path)
    first = ingest.main([str(FIXTURE), "--root", str(tmp_path), *PROV])
    id1 = capsys.readouterr().out.strip()
    assert first == 0
    mint = fm_reader.load_node_file(ingest.node_writer.find_node_file(root, id1), body=False).frontmatter["mint_id"]
    after_first = len(_node_files(root))
    second = ingest.main([str(FIXTURE), "--root", str(tmp_path), *PROV])
    id2 = capsys.readouterr().out.strip()
    assert second == 0 and id2 == id1
    assert len(_node_files(root)) == after_first
    assert fm_reader.load_node_file(ingest.node_writer.find_node_file(root, id2), body=False).frontmatter["mint_id"] == mint


def test_malformed_refused_writes_nothing(tmp_path, capsys):
    root = _project(tmp_path)
    before = _node_files(root)
    rc = ingest.main([str(MALFORMED), "--root", str(tmp_path), *PROV])
    out = capsys.readouterr().out.strip()
    assert rc == 2
    assert out.startswith("refused:")
    assert _node_files(root) == before


def test_empty_refused_writes_nothing(tmp_path, capsys):
    root = _project(tmp_path)
    before = _node_files(root)
    rc = ingest.main([str(EMPTY), "--root", str(tmp_path), *PROV])
    out = capsys.readouterr().out.strip()
    assert rc == 2 and out.startswith("refused:")
    assert _node_files(root) == before


def test_default_env_supplies_provenance(tmp_path, capsys, monkeypatch):
    """No --actor/--thought-session flags: AGI_ACTOR + AGI_THOUGHT_SESSION
    are used, and the minted node carries BOTH, non-empty."""
    root = _project(tmp_path)
    monkeypatch.setenv("AGI_ACTOR", "env-actor")
    monkeypatch.setenv("AGI_THOUGHT_SESSION", "env-session")
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    rc = ingest.main([str(FIXTURE), "--root", str(tmp_path)])
    out = capsys.readouterr().out.strip()
    assert rc == 0, out
    node = ingest.node_writer.find_node_file(root, out)
    fm = fm_reader.load_node_file(node, body=False).frontmatter
    assert fm["edited_by"] == "env-actor"
    assert fm["thought_session"] == "env-session"


def test_missing_provenance_refused_writes_nothing(tmp_path, capsys, monkeypatch):
    """No flags AND no env: refuse BY NAME, write no node. Never a silent
    anonymous write -- the exact defect this round fixes."""
    root = _project(tmp_path)
    for key in ("AGI_ACTOR", "AGI_AGENT_ID", "AGI_THOUGHT_SESSION"):
        monkeypatch.delenv(key, raising=False)
    before = _node_files(root)
    rc = ingest.main([str(FIXTURE), "--root", str(tmp_path)])
    out = capsys.readouterr().out.strip()
    assert rc == 2 and out.startswith("refused:")
    assert _node_files(root) == before


def test_scan_ingests_all_sorted_and_is_idempotent(tmp_path, capsys):
    """A directory with two good artifacts and one malformed one: the refusal
    does not abort the batch, ids print in stable sorted order, and a second
    scan returns the same ids with no new files."""
    root = _project(tmp_path)
    d = tmp_path / "sessions"
    d.mkdir()
    (d / "b.jsonl").write_text(BATCH_B.read_text())
    (d / "a.jsonl").write_text(FIXTURE.read_text())
    (d / "c.jsonl").write_text(MALFORMED.read_text())
    before = len(_node_files(root))
    rc = ingest.main(["--scan", str(d), "--root", str(tmp_path), *PROV])
    lines = capsys.readouterr().out.strip().splitlines()
    assert rc == 0, lines
    assert len(lines) == 3, lines
    assert lines[0].startswith("hypothesis:grok-2026-09-22-abc123"), lines
    assert lines[1].startswith("hypothesis:grok-2026-09-22-batch222"), lines
    assert lines[2].startswith("refused: c.jsonl:"), lines
    assert len(_node_files(root)) == before + 2
    again = ingest.main(["--scan", str(d), "--root", str(tmp_path), *PROV])
    lines2 = capsys.readouterr().out.strip().splitlines()
    assert again == 0
    assert lines2 == lines
    assert len(_node_files(root)) == before + 2


def test_scan_all_refused_exits_nonzero(tmp_path, capsys):
    """Exit-code policy: non-zero iff ZERO artifacts ingested."""
    root = _project(tmp_path)
    d = tmp_path / "empty_sessions"
    d.mkdir()
    before = _node_files(root)
    rc = ingest.main(["--scan", str(d), "--root", str(tmp_path), *PROV])
    out = capsys.readouterr().out.strip()
    assert rc == 2
    assert _node_files(root) == before


def test_scan_refuses_bad_directory(tmp_path, capsys):
    root = _project(tmp_path)
    before = _node_files(root)
    rc = ingest.main(["--scan", str(tmp_path / "nope"), "--root", str(tmp_path), *PROV])
    out = capsys.readouterr().out.strip()
    assert rc == 2 and out.startswith("refused:")
    assert _node_files(root) == before
