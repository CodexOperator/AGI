"""Falsifier for goal:g7.32.1 -- a session transcript becomes ONE graph node,
idempotently, and a malformed input is refused by name rather than dropped.

Three conjuncts, one test each:
  1. fresh ingest mints a node file under <root>/nodes/ and prints its id;
  2. a second ingest of the same fixture prints the SAME id and mints nothing;
  3. a malformed / non-session input exits non-zero with a readable reason.

The schema is copied from the live graph so the gate is the real one, not a
relaxed fixture.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
BIN = REPO / "extensions" / "agi" / "bin"
CLI = BIN / "ingest_session.py"
SESSION = "019ddd0f-6751-75bc-a374-6c0fe036e262"


def _fixture(path):
    rows = [
        {"type": "session", "version": 3, "id": SESSION,
         "timestamp": "2026-04-30T06:24:27.474Z", "cwd": "/home/ubuntu/.hermes/agi"},
        {"type": "message", "id": "m1",
         "message": {"role": "user", "content": [{"type": "text", "text": "hello graph"}]}},
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


@pytest.fixture
def graph(tmp_path):
    root = tmp_path / "graph"
    (root / "nodes").mkdir(parents=True)
    shutil.copytree(REPO / ".agi" / "context", root / "context")
    return root


def run(session, root, *extra):
    return subprocess.run(
        [sys.executable, str(CLI), str(session), "--out-root", str(root), *extra],
        capture_output=True, text=True)


def test_fresh_ingest_mints_one_node_under_nodes(graph, tmp_path):
    session = _fixture(tmp_path / "s.jsonl")
    p = run(session, graph)
    assert p.returncode == 0, p.stderr
    assert re.match(r"INGEST ok doc:grok-session-\S+$", p.stdout.strip()), p.stdout
    node_id = p.stdout.split()[-1]
    files = list((graph / "nodes").rglob("*.md"))
    assert len(files) == 1 and files[0].name == f"{node_id.split(':')[1]}.md"
    text = files[0].read_text(encoding="utf-8")
    assert f"source_session: {SESSION}" in text
    assert "edited_by: ingest_session.py" in text


def test_reingest_is_idempotent(graph, tmp_path):
    session = _fixture(tmp_path / "s.jsonl")
    first = run(session, graph)
    node = list((graph / "nodes").rglob("*.md"))[0]
    mint = re.search(r"^mint_id: (\S+)$", node.read_text(encoding="utf-8"), re.M).group(1)
    second = run(session, graph)
    assert second.returncode == 0, second.stderr
    assert second.stdout.split()[-1] == first.stdout.split()[-1]
    assert second.stdout.strip().startswith("INGEST skip")
    files = list((graph / "nodes").rglob("*.md"))
    assert len(files) == 1
    assert re.search(r"^mint_id: (\S+)$", files[0].read_text(encoding="utf-8"), re.M).group(1) == mint


@pytest.mark.parametrize("body", ["", '{"type":"model_change"}\n'])
def test_malformed_input_is_refused_by_name(graph, tmp_path, body):
    bad = tmp_path / "bad.jsonl"
    bad.write_text(body, encoding="utf-8")
    p = run(bad, graph)
    assert p.returncode != 0
    assert "INGEST refuse" in p.stderr
    assert "no-session-record" in p.stderr
    assert list((graph / "nodes").rglob("*.md")) == []


def _fixture_id(path, sid):
    rows = [{"type": "session", "version": 3, "id": sid, "cwd": "/tmp"},
            {"type": "message", "id": "m1",
             "message": {"role": "user", "content": [{"type": "text", "text": "hi"}]}}]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


def test_distinct_ids_never_collapse_to_one_node(graph, tmp_path):
    """The falsifier: two DISTINCT session ids that sanitize alike must yield
    two distinct node files (or a named refusal) -- never one node for two
    sessions (goal:g7.32.1, no silent drop)."""
    a = _fixture_id(tmp_path / "a.jsonl", "Probe-aaaa-1111")
    b = _fixture_id(tmp_path / "b.jsonl", "probe_aaaa_1111")
    pa, pb = run(a, graph), run(b, graph)
    assert pa.returncode == 0, pa.stderr
    assert pb.returncode == 0, pb.stderr
    assert pa.stdout.split()[-1] != pb.stdout.split()[-1]
    files = sorted(p.name for p in (graph / "nodes").rglob("*.md"))
    assert len(files) == 2, files
    assert {f"{i.split(':')[-1]}.md" for i in (pa.stdout.split()[-1], pb.stdout.split()[-1])} == set(files)
    # and each node carries its OWN raw id, so neither session's identity is lost
    text = "\n".join(p.read_text(encoding="utf-8")
                      for p in (graph / "nodes").rglob("*.md"))
    assert "source_session: Probe-aaaa-1111" in text
    assert "source_session: probe_aaaa_1111" in text


def test_reversible_suffix_separates_hash_colliding_pair(graph, tmp_path):
    """The parent's KNOWN falsifier: two distinct raw ids that share both a
    sanitized canon and (under the old `sha256(raw)[:8]` suffix) the same
    suffix. With a reversible hex-of-bytes suffix they must mint TWO distinct
    node files, each carrying its own raw source_session -- never one node for
    two sessions (goal:g7.32.1, no silent drop)."""
    a = _fixture_id(tmp_path / "a.jsonl", "x_-x:x.x.x_~-x-x_~x.x~x~x")
    b = _fixture_id(tmp_path / "b.jsonl", "x__x._x:.x._x~x_-x_-.x__~x_-x-x")
    pa, pb = run(a, graph), run(b, graph)
    assert pa.returncode == 0, pa.stderr
    assert pb.returncode == 0, pb.stderr
    assert pa.stdout.split()[-1] != pb.stdout.split()[-1]
    files = sorted(p.name for p in (graph / "nodes").rglob("*.md"))
    assert len(files) == 2, files
    text = "\n".join(p.read_text(encoding="utf-8")
                      for p in (graph / "nodes").rglob("*.md"))
    assert "source_session: x_-x:x.x.x_~-x-x_~x.x~x~x" in text
    assert "source_session: x__x._x:.x._x~x_-x_-.x__~x_-x-x" in text


def test_overlong_id_is_refused_by_name_not_truncated(graph, tmp_path):
    """A reversible suffix can push the slug past the filesystem limit. The
    only safe answer is a NAMED refusal: truncating would reintroduce the very
    collision the encoding removes, and an OSError is not a reason."""
    long = _fixture_id(tmp_path / "long.jsonl", "L" * 300)
    p = run(long, graph)
    assert p.returncode == 2, p.stdout
    assert "INGEST refuse slug-too-long" in p.stderr
    assert "refusing rather than truncating" in p.stderr
    assert list((graph / "nodes").rglob("*.md")) == []


def test_slug_length_boundary_is_accept_at_limit_refuse_above(graph, tmp_path):
    """The guard has an edge, not a fudge: a slug of exactly the 200-char
    limit is written; one two chars longer is refused by name. Both sides of
    the boundary are pinned so a later refactor cannot silently move it."""
    at = _fixture_id(tmp_path / "at.jsonl", "ab-" + "~" * 89)      # slug 200
    over = _fixture_id(tmp_path / "over.jsonl", "ab-" + "~" * 90)  # slug 202
    p_at, p_over = run(at, graph), run(over, graph)
    assert p_at.returncode == 0, p_at.stderr
    assert len(p_at.stdout.split()[-1]) == len("doc:") + 200
    assert p_over.returncode == 2 and "slug-too-long" in p_over.stderr
    assert len(list((graph / "nodes").rglob("*.md"))) == 1


SESSION_LINE = '{"type":"session","id":"X"}'


@pytest.mark.parametrize("body,reason", [
    ("[1,2,3]\n", "malformed-record"),
    ("42\n", "malformed-record"),
    (SESSION_LINE + '\n{"type":"message","id":"m","message":"oops"}\n',
     "malformed-message"),
    (SESSION_LINE + '\n{"type":"message","id":"m","message":{"content":["oops"]}}\n',
     "malformed-content"),
    (SESSION_LINE + '\n{"type":"message","id":"m","message":{"content":{"a":1}}}\n',
     "malformed-content"),
])
def test_non_dict_shape_is_refused_by_name_not_traceback(graph, tmp_path, body, reason):
    """goal:g7.32.1 residue 1: a JSONL line that is not an object, or a
    `message`/`content`/content-block of the wrong shape, must be a NAMED
    refusal (exit 2, `INGEST refuse <reason>` on stderr) -- never an
    AttributeError traceback with exit 1, and never a silent node."""
    bad = tmp_path / "bad.jsonl"
    bad.write_text(body, encoding="utf-8")
    p = run(bad, graph)
    assert p.returncode == 2, (p.returncode, p.stdout, p.stderr)
    assert "INGEST refuse" in p.stderr
    assert reason in p.stderr
    assert "Traceback" not in p.stderr
    assert list((graph / "nodes").rglob("*.md")) == []


@pytest.mark.parametrize("value", [123, ["a"], {"a": 1}])
def test_non_string_text_is_refused_by_name_not_traceback(graph, tmp_path, value):
    """goal:g7.32.1 residue 1, one level deeper: a well-formed text block
    whose PRESENT `text` value is not a string used to reach `" ".join` and
    die with a TypeError / exit 1. It must instead be a NAMED refusal (exit 2,
    `INGEST refuse malformed-content: ... text is not a string`), no
    traceback, no node -- never a silent drop."""
    body = (SESSION_LINE + '\n{"type":"message","id":"m","message":'
            '{"content":[{"type":"text","text":' + json.dumps(value)
            + '}]}}\n')
    bad = tmp_path / "bad.jsonl"
    bad.write_text(body, encoding="utf-8")
    p = run(bad, graph)
    assert p.returncode == 2, (p.returncode, p.stdout, p.stderr)
    assert "INGEST refuse" in p.stderr
    assert "malformed-content: line 2: text is not a string" in p.stderr
    assert "Traceback" not in p.stderr
    assert list((graph / "nodes").rglob("*.md")) == []


def test_valid_session_with_no_message_records_still_ingests(graph, tmp_path):
    """The happy path is not weakened by the shape guards: a session with no
    `message` records, an empty content list, and a text block with no `text`
    key all still ingest."""
    rows = [{"type": "session", "id": "S-nomsg"},
            {"type": "message", "id": "m1", "message": {"content": []}},
            {"type": "message", "id": "m2", "message": {"content": [{"type": "text"}]}}]
    good = tmp_path / "good.jsonl"
    good.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    p = run(good, graph)
    assert p.returncode == 0, p.stderr
    assert p.stdout.strip().startswith("INGEST ok")
    assert len(list((graph / "nodes").rglob("*.md"))) == 1


def test_canonical_uuid_keeps_bare_slug_and_case_is_idempotent(graph, tmp_path):
    """Continuity: a real-corpus UUID keeps `grok-session-<uuid>` (the node
    already in the graph for SESSION), and its upper-cased spelling is the SAME
    session, not a second node."""
    low = _fixture_id(tmp_path / "low.jsonl", SESSION)
    up = _fixture_id(tmp_path / "up.jsonl", SESSION.upper())
    pl, pu = run(low, graph), run(up, graph)
    assert pl.stdout.strip() == f"INGEST ok doc:grok-session-{SESSION}"
    assert pu.stdout.strip() == f"INGEST skip doc:grok-session-{SESSION}"
    assert len(list((graph / "nodes").rglob("*.md"))) == 1


RESIDUE_DOC = ".agi/nodes/doc/grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262.md"
SCOPE_AGENT = "a00-a960d972"


def _scope_check(*own):
    argv = [sys.executable, str(REPO / "extensions" / "agi" / "bin" / "cli.py"),
            "scope-check", "--agent-id", SCOPE_AGENT]
    for o in own:
        argv += ["--own", o]
    return subprocess.run(argv, input=RESIDUE_DOC + "\0", capture_output=True,
                          text=True, cwd=REPO)


def test_residue_node_is_committable_exactly_when_owned():
    """goal:g7.32.1 conjunct 2: the real-corpus ingest residue is unowned to a
    round that does not name it and owned to one that does."""
    assert _scope_check().returncode == 1
    assert _scope_check(RESIDUE_DOC).returncode == 0