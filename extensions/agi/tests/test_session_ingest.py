"""`goal:g7.32.1` falsifiers 1 and 2, on a tiny fixture.

Falsifier 1: given a session artifact, ingest prints >=1 node id and a file
appears under `.agi/nodes/`.
Falsifier 2: re-ingesting the SAME fixture mints no second node — the same
node id, the same `mint_id`, no fork.

The graph these run against is a THROWAWAY project root built in `tmp_path`
(one goal node, one copied `[doc].md` schema), because a test that ingested
into the live graph would leave a residue behind on every suite run — the
exact stranded-file shape this goal exists to end.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(BIN.parent / "src"))

import session_ingest  # noqa: E402

PARENT = "goal:g7.32.1"


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A minimal agi project: config, nodes/, context/schemas/[doc].md."""
    root = tmp_path / "proj"
    (root / ".agi" / "nodes" / "goal").mkdir(parents=True)
    (root / ".agi" / "context" / "schemas").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text("{}\n", encoding="utf-8")
    (root / ".agi" / "nodes" / "goal" / "g7.32.1.md").write_text(
        "---\nid: goal:g7.32.1\nmint_id: " + "a" * 32 +
        "\ntype: goal\nparents: []\n---\n\n# goal:g7.32.1\n",
        encoding="utf-8")
    src = Path(__file__).resolve().parents[3] / ".agi" / "context" / "schemas" / "[doc].md"
    (root / ".agi" / "context" / "schemas" / "[doc].md").write_text(
        src.read_text(encoding="utf-8"), encoding="utf-8")
    return root


def fixture_session(path: Path, n: int = 3) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for i in range(n):
            fh.write(json.dumps({"role": "user" if i % 2 == 0 else "assistant",
                                 "text": f"line {i}"}) + "\n")
    return path


def test_falsifier1_mints_a_node(project: Path, tmp_path: Path):
    artifact = fixture_session(tmp_path / "s" / "sess.jsonl")
    out = session_ingest.main([str(artifact), "--parent", PARENT,
                               "--root", str(project), "--json"])
    assert out == session_ingest.EXIT_OK
    minted = list((project / ".agi" / "nodes" / "doc").glob("*.md"))
    assert len(minted) == 1, "falsifier 1: no node file under .agi/nodes/"
    text = minted[0].read_text(encoding="utf-8")
    assert "type: doc" in text and "ingest_sha256:" in text
    assert "roles: assistant×1, user×2" in text, "the summary lost its actors"


def test_falsifier2_reingest_does_not_fork(project: Path, tmp_path: Path,
                                           capsys):
    artifact = fixture_session(tmp_path / "sess.jsonl")
    args = [str(artifact), "--parent", PARENT, "--root", str(project)]
    assert session_ingest.main(args) == session_ingest.EXIT_OK
    first = capsys.readouterr().out.strip()
    assert session_ingest.main(args) == session_ingest.EXIT_OK
    second = capsys.readouterr().out.strip()
    assert first == second and first.startswith("doc:session-")
    files = sorted((project / ".agi" / "nodes" / "doc").glob("*.md"))
    assert len(files) == 1, "falsifier 2: re-ingest forked a second node"
    mint = [ln for ln in files[0].read_text(encoding="utf-8").splitlines()
            if ln.startswith("mint_id:")]
    assert len(mint) == 1


def test_refusal_is_named_and_nonzero(project: Path, tmp_path: Path,
                                      capsys):
    """No silent drop: a non-session file refuses BY NAME, exit 2."""
    junk = tmp_path / "junk.jsonl"
    junk.write_text("not json at all\n", encoding="utf-8")
    code = session_ingest.main([str(junk), "--parent", PARENT,
                                "--root", str(project)])
    assert code == session_ingest.EXIT_REFUSED
    assert "no-parseable-events" in capsys.readouterr().err
    assert not list((project / ".agi" / "nodes" / "doc").glob("*.md"))


def test_grown_session_is_a_different_node(project: Path, tmp_path: Path):
    """The known limit, asserted rather than implied: a session that GREW
    hashes differently and mints a second node. Supersession is not built."""
    artifact = fixture_session(tmp_path / "sess.jsonl", n=3)
    args = [str(artifact), "--parent", PARENT, "--root", str(project)]
    session_ingest.main(args)
    fixture_session(artifact, n=4)
    session_ingest.main(args)
    assert len(list((project / ".agi" / "nodes" / "doc").glob("*.md"))) == 2
