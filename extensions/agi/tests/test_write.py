"""goal:g13 — the write half: gated in-place edits, and the link layer.

Two modules under test, and they answer the goal's three settled questions
between them:

- `node_writer.update_node` — the routine that did not exist. Every fix,
  retag and field addition was a hand edit until now: no schema check, no
  `THOUGHT` guarantee, no record a write happened. `goal:g13.1` names it
  exactly — a hand edit is "a completely stray and untraceable commit".
- `write.py` — `link_ref`, `self`, and the two chosen failure behaviours.

The load-bearing test in this file is
`test_an_update_cannot_destroy_the_authored_thought_region`. `goal:g2.10` is
the standing proof that a writer which rewrites a body destroys authored
content and nobody notices for 8,034 fields.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import node_writer  # noqa: E402
import write  # noqa: E402

THOUGHT = ("<!-- THOUGHT:BEGIN — authored, not derived; carried across "
           "regenerating scans. The reasoning behind THIS version. -->\n"
           "why this version differs\n"
           "<!-- THOUGHT:END -->")


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """A minimal graph root: `.agi/` with a config and a nodes tree."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    return graph


def _node(project: Path, node_id: str, fm_lines: list[str], body: str) -> Path:
    ntype, slug = node_id.split(":", 1)
    path = project / "nodes" / ntype / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + "\n".join(fm_lines) + "\n---\n\n" + body)
    return path


# --------------------------------------------------------------------------
# update_node — the gated in-place edit
# --------------------------------------------------------------------------

def test_an_update_cannot_destroy_the_authored_thought_region(project):
    """goal:g2.10's defect, made impossible rather than discouraged.

    A generator rewrote the whole body each run, so filling an authored field
    lasted until the next scan. An update that replaces the body must carry
    the authored region across.
    """
    _node(project, "hypothesis:h1",
          ['id: "hypothesis:h1"', "type: hypothesis",
           "mint_id: abc123", 'title: "t"', 'testable_claim: "c"'],
          "the old body\n\n" + THOUGHT + "\n")

    res = node_writer.update_node(project, "hypothesis:h1",
                                  body="a completely new body\n")
    assert res.status == node_writer.UPDATED

    text = res.path.read_text()
    assert "a completely new body" in text
    assert "THOUGHT:BEGIN" in text, "the authored region was destroyed"
    assert "why this version differs" in text


def test_a_new_body_that_brings_its_own_thought_keeps_it(project):
    """The writer of a version is entitled to say why it differs."""
    _node(project, "hypothesis:h1",
          ['id: "hypothesis:h1"', "type: hypothesis", "mint_id: abc123",
           'title: "t"', 'testable_claim: "c"'],
          "old\n\n" + THOUGHT.replace("why this version differs", "OLD REASON") + "\n")

    new = "new body\n\n" + THOUGHT.replace("why this version differs", "NEW REASON")
    res = node_writer.update_node(project, "hypothesis:h1", body=new)

    text = res.path.read_text()
    assert "NEW REASON" in text
    assert "OLD REASON" not in text, "thought is rewritten per version, not accumulated"
    assert text.count("THOUGHT:BEGIN") == 1


def test_frontmatter_is_merged_not_replaced(project):
    _node(project, "hypothesis:h1",
          ['id: "hypothesis:h1"', "type: hypothesis", "mint_id: abc123",
           'title: "keep me"', 'testable_claim: "c"', "confidence: 0.4"],
          "body\n")

    res = node_writer.update_node(project, "hypothesis:h1",
                                  set_fm={"confidence": 0.9})
    assert res.status == node_writer.UPDATED
    text = res.path.read_text()
    assert "keep me" in text, "an untouched key must survive"
    assert "confidence: 0.9" in text


def test_unset_drops_a_key(project):
    _node(project, "hypothesis:h1",
          ['id: "hypothesis:h1"', "type: hypothesis", "mint_id: abc123",
           'title: "t"', 'testable_claim: "c"', "stale_key: gone"],
          "body\n")
    node_writer.update_node(project, "hypothesis:h1", unset_fm=["stale_key"])
    assert "stale_key" not in (project / "nodes/hypothesis/h1.md").read_text()


def test_an_update_that_changes_nothing_writes_nothing(project):
    """`grid.py commit --all` must not mint a version recording no change.

    Versions record change, not time.
    """
    path = _node(project, "hypothesis:h1",
                 ['id: "hypothesis:h1"', "type: hypothesis", "mint_id: abc123",
                  'title: "t"', 'testable_claim: "c"'], "body\n")
    before = path.read_text()
    mtime = path.stat().st_mtime_ns

    res = node_writer.update_node(project, "hypothesis:h1", set_fm={"title": "t"})
    assert res.status == node_writer.UNCHANGED
    assert path.read_text() == before
    assert path.stat().st_mtime_ns == mtime, "the file was rewritten anyway"


def test_a_missing_node_is_rejected_not_created(project):
    res = node_writer.update_node(project, "hypothesis:nope", set_fm={"x": 1})
    assert res.status == node_writer.REJECTED
    assert "no node file" in res.reason
    assert not (project / "nodes/hypothesis/nope.md").exists(), (
        "update must never create — that is write_node's job")


def test_an_unparseable_node_is_rejected_rather_than_rewritten(project):
    """Turning an unreadable node into a wrong one is worse than leaving it."""
    path = project / "nodes" / "hypothesis" / "broken.md"
    path.write_text("---\nid: [unclosed\n---\nbody\n")
    res = node_writer.update_node(project, "hypothesis:broken", set_fm={"x": 1})
    assert res.status == node_writer.REJECTED
    assert "could not be parsed" in res.reason
    assert path.read_text().startswith("---\nid: [unclosed")


# --------------------------------------------------------------------------
# The link layer — goal:g13's three answers
# --------------------------------------------------------------------------

def test_absent_link_defaults_to_self_but_says_it_defaulted():
    """'The graph said so' and 'the fallback guessed' are not the same claim."""
    assert write.link_ref({}) == (write.SELF, write.FROM_DEFAULT)
    assert write.link_ref({"link_ref": "self"}) == (write.SELF, write.FROM_NODE)


def test_payload_ref_is_read_as_the_predecessor_it_is():
    """The 220 build nodes that carry one are linked without being rewritten."""
    ref, source = write.link_ref({"payload_ref": "extensions/agi/bin/cli.py"})
    assert ref == "extensions/agi/bin/cli.py"
    assert source == write.FROM_LEGACY


def test_link_ref_wins_over_payload_ref():
    ref, source = write.link_ref({"link_ref": "a.py", "payload_ref": "b.py"})
    assert (ref, source) == ("a.py", write.FROM_NODE)


def test_self_resolves_to_the_nodes_own_body_without_branching_on_type(tmp_path):
    """A goal is not a special case in the reader — it declares `self`.

    That is the whole difference between an exception with a name and a hole.
    """
    link = write.resolve(tmp_path, "goal:g1", {"link_ref": "self"}, "the body")
    assert link.is_self
    assert link.content == "the body"
    assert link.path is None


def test_a_single_read_of_a_missing_link_raises(tmp_path):
    """Loud where a caller can act."""
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}")
    with pytest.raises(write.MissingLink) as exc:
        write.resolve(tmp_path / ".agi", "build:gone", {"link_ref": "no/such.py"}, "")
    assert "must not fail quietly" in str(exc.value)
    assert exc.value.node_id == "build:gone"


def test_a_bulk_scan_of_a_missing_link_returns_a_sentinel_and_keeps_going(tmp_path):
    """Survivable where one bad node must not kill a scan of nine hundred."""
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}")
    root = tmp_path / ".agi"

    resolved, broken = write.resolve_many(root, [
        ("goal:g1", {"link_ref": "self"}, "body one"),
        ("build:gone", {"link_ref": "no/such.py"}, ""),
        ("goal:g2", {}, "body two"),
    ])

    assert [l.node_id for l in resolved] == ["goal:g1", "goal:g2"], (
        "the scan continued past the broken node")
    assert [s.node_id for s in broken] == ["build:gone"]


def test_the_sentinel_is_falsey_and_is_not_a_string(tmp_path):
    """`None` is what three of the six surveyed readers already returned, and
    it is indistinguishable from an empty body. A reader that mistakes this
    for content gets a TypeError — the loudest failure available to something
    that must not raise."""
    sentinel = write.MissingLinkSentinel("n:1", "x.py", Path("/x.py"))
    assert not sentinel
    assert not isinstance(sentinel, str)
    with pytest.raises(TypeError):
        "prefix" + sentinel        # type: ignore[operator]


def test_set_link_goes_through_the_gated_writer(project, monkeypatch):
    """This module must not become the second write path in the goal that
    exists to remove them."""
    _node(project, "hypothesis:h1",
          ['id: "hypothesis:h1"', "type: hypothesis", "mint_id: abc123",
           'title: "t"', 'testable_claim: "c"'], "body\n")

    calls = []
    real = node_writer.update_node
    monkeypatch.setattr(node_writer, "update_node",
                        lambda *a, **kw: (calls.append((a, kw)), real(*a, **kw))[1])

    write.set_link(project, "hypothesis:h1", write.SELF)
    assert calls, "set_link wrote the field itself instead of going through update_node"
    assert "link_ref: self" in (project / "nodes/hypothesis/h1.md").read_text()


def test_the_resolver_has_no_type_branch_in_its_executable_lines():
    """`self` must resolve without the reader learning what a goal is.

    Asserted with `ast` rather than `grep`, because a first attempt used
    `grep -c "type == goal"` and got **1** — the phrase is in the module
    docstring, describing the invariant. A text search for a concept cannot
    tell prose from code, which is the same class of mistake as a smoke check
    passing on a traceback: the tool answered a different question.
    """
    import ast

    src = (BIN / "write.py").read_text()
    tree = ast.parse(src)
    in_string: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            in_string.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))

    offenders = []
    for lineno, line in enumerate(src.splitlines(), 1):
        code = line.split("#", 1)[0].lower()
        if lineno in in_string:
            continue
        if "goal" in code and "type" in code:
            offenders.append((lineno, line.strip()))

    assert offenders == [], (
        f"the resolver branches on node type: {offenders}. `link_ref: self` is "
        f"an exception WITH A NAME; a type check turns it back into a hole.")
