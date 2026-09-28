"""goal:g13 — the write half: gated in-place edits, and the link layer.

Two modules under test, and they answer the goal's three settled questions
between them:

- `node_writer.update_node` — the routine that did not exist. Every fix,
  retag and field addition was a hand edit until now: no schema check, no
  `THOUGHT` guarantee, no record a write happened. `goal:g13.1` names it
  exactly — a hand edit is "a completely stray and untraceable commit".
- `links.py` — `link_ref`, `self`, and the two chosen failure behaviours.

The load-bearing test in this file is
`test_an_update_cannot_destroy_the_authored_thought_region`. `goal:g2.10` is
the standing proof that a writer which rewrites a body destroys authored
content and nobody notices for 8,034 fields.
"""
from __future__ import annotations

import sys
import json
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import locations  # noqa: E402
import node_writer  # noqa: E402
import links  # noqa: E402

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
    assert links.link_ref({}) == (links.SELF, links.FROM_DEFAULT)
    assert links.link_ref({"link_ref": "self"}) == (links.SELF, links.FROM_NODE)


def test_payload_ref_is_read_as_the_predecessor_it_is():
    """The 220 build nodes that carry one are linked without being rewritten."""
    ref, source = links.link_ref({"payload_ref": "extensions/agi/bin/cli.py"})
    assert ref == "extensions/agi/bin/cli.py"
    assert source == links.FROM_LEGACY


def test_link_ref_wins_over_payload_ref():
    ref, source = links.link_ref({"link_ref": "a.py", "payload_ref": "b.py"})
    assert (ref, source) == ("a.py", links.FROM_NODE)


def test_self_resolves_to_the_nodes_own_body_without_branching_on_type(tmp_path):
    """A goal is not a special case in the reader — it declares `self`.

    That is the whole difference between an exception with a name and a hole.
    """
    link = links.resolve(tmp_path, "goal:g1", {"link_ref": "self"}, "the body")
    assert link.is_self
    assert link.content == "the body"
    assert link.path is None


def test_a_single_read_of_a_missing_link_raises(tmp_path):
    """Loud where a caller can act."""
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}")
    with pytest.raises(links.MissingLink) as exc:
        links.resolve(tmp_path / ".agi", "build:gone", {"link_ref": "no/such.py"}, "")
    assert "must not fail quietly" in str(exc.value)
    assert exc.value.node_id == "build:gone"


def test_a_bulk_scan_of_a_missing_link_returns_a_sentinel_and_keeps_going(tmp_path):
    """Survivable where one bad node must not kill a scan of nine hundred."""
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}")
    root = tmp_path / ".agi"

    resolved, broken = links.resolve_many(root, [
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
    sentinel = links.MissingLinkSentinel("n:1", "x.py", Path("/x.py"))
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

    # Patch on `links.node_writer` -- the exact object `write` calls through --
    # not on this file's own `node_writer` name. Other test modules load
    # engine modules by file path (`spec_from_file_location`), which creates
    # SEPARATE module objects, so "the same import" is not guaranteed to be
    # the same object once the whole suite runs in one process. Patching the
    # caller's own reference is correct either way; patching a name that
    # happens to resolve to it usually is, and this one stopped.
    calls = []
    real = links.node_writer.update_node
    monkeypatch.setattr(links.node_writer, "update_node",
                        lambda *a, **kw: (calls.append((a, kw)), real(*a, **kw))[1])

    links.set_link(project, "hypothesis:h1", links.SELF)
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

    src = (BIN / "links.py").read_text()
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


# --------------------------------------------------------------------------
# goal:g13 / mvp:route-every-writer-through-update-node — the writers route
# through the gate now, and these are the invariants that made that safe.
# --------------------------------------------------------------------------

def test_an_update_is_judged_on_the_delta_not_the_state(project):
    """An update is rejected for fields it BREAKS, never for fields already
    missing when it arrived.

    Rejecting on state would have been a live regression the moment real
    writers routed through here: 115 nodes in this corpus are already
    schema-invalid (`goal:s31`), so recording a verdict on one would have been
    refused for a defect it did not cause and could not fix. A gate that
    punishes the wrong write teaches callers to pass `validate=False`, which
    is how a gate stops existing.
    """
    _node(project, "hypothesis:invalid",
          ['id: "hypothesis:invalid"', "type: hypothesis", "mint_id: abc123"],
          "body\n")   # no title, no testable_claim — already invalid
    (project / "context" / "schemas").mkdir(parents=True, exist_ok=True)
    (project / "context" / "schemas" / "[hypothesis].md").write_text(
        "---\nname: hypothesis\nvalidation:\n  required: [id, type, mint_id, "
        "title, testable_claim]\nspawn:\n  allowed_parents: [goal]\n"
        "  min_parents: 1\n  max_parents: 2\n---\n\nbody\n")

    ok = node_writer.update_node(project, "hypothesis:invalid",
                                 set_fm={"verdict": "pending"})
    assert ok.status == node_writer.UPDATED, (
        "an unrelated edit to an already-invalid node must go through")

    _node(project, "hypothesis:valid",
          ['id: "hypothesis:valid"', "type: hypothesis", "mint_id: abc",
           'title: "t"', 'testable_claim: "c"'], "body\n")
    bad = node_writer.update_node(project, "hypothesis:valid",
                                  unset_fm=["title"])
    assert bad.status == node_writer.REJECTED
    assert "may not REMOVE" in bad.reason


def _post_wire():
    import importlib.util
    spec = importlib.util.spec_from_file_location("pw", BIN / "post_wire.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_post_wire_computes_its_delta_by_diffing_not_by_listing(project):
    """`evidence_gate.stamp()` writes keys the call site does not name.

    A hand-listed delta would silently drop exactly the demotion stamps the
    gate exists to record, which is why the diff is against the frontmatter as
    read rather than against a list of fields this code believes it changed.
    """
    _node(project, "hypothesis:h1",
          ['id: "hypothesis:h1"', "type: hypothesis", "mint_id: abc",
           'title: "t"', 'testable_claim: "c"'], "body\n")
    pw = _post_wire()

    original = {"id": "hypothesis:h1", "type": "hypothesis", "mint_id": "abc",
                "title": "t", "testable_claim": "c"}
    mutated = dict(original)
    mutated["verdict"] = "inconclusive_lean_proved:50"
    mutated["demoted_from"] = "proved"          # a key the call site never names
    mutated["demote_reason"] = "no evidence"

    pw._update_via_writer(project, "hypothesis:h1",
                          project / "nodes/hypothesis/h1.md",
                          original, mutated, "body\n", "body\n")

    text = (project / "nodes/hypothesis/h1.md").read_text()
    assert "demoted_from: proved" in text, "a stamp the call site never named was dropped"
    assert "demote_reason: no evidence" in text


def test_post_wire_writes_nothing_when_nothing_changed(project):
    """This path runs on every completed node every iteration. An
    unconditional rewrite would mint a grid version per node per iteration and
    *versions record change, not time* would stop being true."""
    path = _node(project, "hypothesis:h1",
                 ['id: "hypothesis:h1"', "type: hypothesis", "mint_id: abc",
                  'title: "t"', 'testable_claim: "c"'], "body\n")
    mtime = path.stat().st_mtime_ns
    same = {"id": "hypothesis:h1", "type": "hypothesis", "mint_id": "abc",
            "title": "t", "testable_claim": "c"}

    _post_wire()._update_via_writer(project, "hypothesis:h1", path,
                                    same, dict(same), "body\n", "body\n")
    assert path.stat().st_mtime_ns == mtime


def test_a_refused_gated_write_still_records_the_wire(project, capsys, monkeypatch):
    """`goal:g7` outranks `goal:g13`: a wire that cannot be recorded is worse
    than one recorded outside the gate."""
    path = _node(project, "hypothesis:h1",
                 ['id: "hypothesis:h1"', "type: hypothesis", "mint_id: abc",
                  'title: "t"', 'testable_claim: "c"'], "body\n")
    pw = _post_wire()
    original = {"id": "hypothesis:h1", "type": "hypothesis", "mint_id": "abc",
                "title": "t", "testable_claim": "c"}
    mutated = dict(original)
    mutated["verdict"] = "pending"

    # Force the gate to refuse. Via `monkeypatch`, NOT by assigning on the
    # module: `pw.node_writer` IS the imported `node_writer` module object, so
    # a bare assignment leaks into every test that runs afterwards. The first
    # version did that and broke a test in another file that passed in
    # isolation -- visible only in full-suite order, which is the worst place
    # for a failure to first appear.
    monkeypatch.setattr(pw.node_writer, "update_node",
                        lambda *a, **k: node_writer.NodeWrite(
                            node_id="hypothesis:h1",
                            status=node_writer.REJECTED, reason="forced"))

    pw._update_via_writer(project, "hypothesis:h1", path,
                          original, mutated, "body\n", "body\n")
    assert "verdict: pending" in path.read_text(), "the wire was lost"
    assert "writing directly so the wire is not lost" in capsys.readouterr().err


# --------------------------------------------------------------------------
# `links.py roles` — the third, dry role/coverage report (goal:g13, L4.05)
# --------------------------------------------------------------------------

def _schema(project: Path, ntype: str, written_by: str) -> Path:
    """A schema in the fixture corpus declaring who may write `ntype`."""
    d = project / "context" / "schemas"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"[{ntype}].md"
    p.write_text("---\nname: " + ntype + "\nwritten_by: " + written_by
                 + "\n---\n")
    return p


def test_roles_report_names_a_violation_and_writes_nothing(project, capsys):
    """Hypothesis:l4-links-roles-report, proof (3).

    A schema declares `written_by: owner` for one type; the corpus holds a
    node recorded against a DIFFERENT writer. `links.py roles` must NAME that
    node with the writer found, show the coverage census for every type, and
    still write nothing (no node, no schema).
    """
    _schema(project, "hypothesis", "owner")
    (project / "nodes" / "mvp").mkdir(parents=True, exist_ok=True)
    _node(project, "hypothesis:h-owner",
          ['id: "hypothesis:h-owner"', "type: hypothesis", "mint_id: aa",
           "role: owner", 'title: "t"', 'testable_claim: "c"'], "b\n")
    _node(project, "hypothesis:h-kid",
          ['id: "hypothesis:h-kid"', "type: hypothesis", "mint_id: bb",
           "role: kid", 'title: "t"', 'testable_claim: "c"'], "b\n")
    # A second type with NO schema at all -> part of the coverage gap, and a
    # node file we can prove is untouched by the report.
    mvp = _node(project, "mvp:m1",
                ['id: "mvp:m1"', "type: mvp", "mint_id: cc", 'title: "t"'],
                "b\n")
    mvp_before = mvp.read_text()

    assert links.main(["roles", "--root", str(project)]) == 0
    out = capsys.readouterr().out

    # Half (a): the census, named per type, gap visible and counted.
    assert "coverage census" in out
    # Half (b): the violation is NAMED with the writer found.
    assert "hypothesis:h-kid" in out
    assert "'kid'" in out
    assert "admitted: owner" in out
    # The admitted node is not a violation; the unchecked type stays a gap.
    assert "hypothesis:h-owner" not in out.split("violation")[1]

    # And nothing was written: the node file is byte-identical.
    assert mvp.read_text() == mvp_before, "roles wrote to a node file"


def test_roles_report_marks_unrecorded_without_guessing(project, capsys):
    """A node in a declared type with no writer is UNRECORDED, not skipped."""
    _schema(project, "hypothesis", "owner")
    _node(project, "hypothesis:h-unnamed",
          ['id: "hypothesis:h-unnamed"', "type: hypothesis", "mint_id: dd",
           'title: "t"', 'testable_claim: "c"'], "b\n")

    links.main(["roles", "--root", str(project)])
    out = capsys.readouterr().out
    assert "UNRECORDED" in out
    assert "hypothesis:h-unnamed" in out


# --------------------------------------------------------------------------
# The writer's shape, asked of the writer — refused BY NAME on the read path
# --------------------------------------------------------------------------
GLUED = 'probes=["wire: (parent a00-a0e8250e, RAN) - one, two'


def test_the_writer_owns_the_field_shape():
    """One definition: `set k=v` is not `set`'s grammar, a structured key is
    not a bare `key:` line, a plain key is."""
    assert not node_writer.writer_key_shape('probes=["wire')
    assert not node_writer.writer_key_shape("FILE SCOPE")
    assert not node_writer.writer_key_shape("a b")
    for key in ("id", "type", "parents", "next_edges", "testable_claim",
                "a00-1556127c-9fb395"):
        assert node_writer.writer_key_shape(key), key


#: ITEM 8: the rule is NOT this tuple, it is node_writer's own definition --
#: every spelling whose rendered `key: x` line does not read back as a
#: DIFFERENT string is in shape, which is the whole YAML 1.1 resolver word
#: set (bool, null, int, float, date) in any case. The tuple below is a
#: SAMPLE of that set, not its bound: it is generated, so a new case variant
#: cannot be forgotten the way `nil` was (`nil` is not a YAML 1.1 null word --
#: it was already in shape before the fix, so listing it was decoration).
COLLAPSING_KEYS = ("on", "off", "yes", "no", "true", "false", "null", "~",
                   "On", "NO", "TRUE", "Off", "2024", "1.5", "2024-01-01")


def test_a_resolver_collapsed_key_is_the_writers_shape(project):
    """ITEMS 1/2/8: `set <key> <value>` spells no key character class, so a
    bare `key: v` line that YAML 1.1 folds to a bool/int/float/date/None key
    is still a field the writer emits. Measured end to end: each of these
    used to be refused by the bool-only forgiveness set (`2024`) and `pop`ped
    by `_ensure_frontmatter` (see the probe output on the node)."""
    import cli
    for key in COLLAPSING_KEYS:
        assert node_writer.writer_key_shape(key), key
        assert node_writer._render_value(key, "v") == [f"{key}: v"]
        assert cli._off_shape_keys({key: "v", "id": "x"}) == [], key


def test_the_repair_keeps_a_collapsed_key_field_end_to_end(project):
    """Same family through `_ensure_frontmatter`, the one place the rename
    bites. `on: yes` comes back as the bool key `True`: the surviving SPELLING
    is `True` because `render_frontmatter` is handed the re-parsed mapping and
    never sees the header (ITEM 1 residual, outside scope, cli.py:429-432).
    Pinned: the field SURVIVES the repair, on a PARSED key, never a substring."""
    import cli
    # NO `parents`/`mint_id`: either keeps `_ensure_frontmatter` out of its
    # re-salvage branch (`frontmatter ok`, nothing rewritten). The manifest
    # supplies the parent the repair needs.
    path = _node(project, "experiment:e1",
                 ['id: "experiment:e1"', "type: experiment", "on: yes",
                  "notes: keep"], "b\n")
    ap = project / "agent.json"
    ap.write_text(json.dumps({"node_id": "experiment:e1", "parent": "hypothesis:h1"}))
    ok, msg = cli._ensure_frontmatter(project, path, ap, "experiment:e1")
    assert ok, msg
    text = path.read_text()
    ok2, fm2, defect2 = cli._load_frontmatter(text)
    assert ok2, defect2
    assert cli._off_shape_keys(fm2) == []
    assert fm2["parents"] == ["hypothesis:h1"]   # the repair really ran
    # A KEY on the PARSED mapping: `"on" in text` passes whether or not the
    # repair ran; `True in text` is a TypeError.
    assert True in fm2, sorted(map(str, fm2))
    # ITEM 2: two non-leading keys is the case that used to raise
    # `TypeError: '<' not supported between 'bool' and 'str'` and kill `done`.
    assert [l for l in text.splitlines() if l.startswith("notes")] == ["notes: keep"]


def test_links_refuses_a_glued_key_by_name(project):
    """The claim's second conjunct: refused at links, not silently defaulted."""
    path = _node(project, "hypothesis:h-glued",
                 ['id: "hypothesis:h-glued"', "type: hypothesis",
                  "mint_id: abc123", 'title: "t"', 'testable_claim: "c"',
                  GLUED], "b\n")
    from graph_core.persistence import frontmatter as fm_reader

    fm = fm_reader.load_node_file(path).frontmatter
    with pytest.raises(links.MalformedNode) as exc:
        links.resolve(project, "hypothesis:h-glued", fm, "b\n")
    assert "hypothesis:h-glued" in str(exc.value)      # node id AND field
    assert "probes=[" in str(exc.value)
    assert any("h-glued" in n for n in links.off_shape_nodes(project))
    assert all(nid != "hypothesis:h-glued" for nid, _fm, _b in
               links._iter_corpus(project))
    # ITEM 5: the old `count_broken_links(project) == 0` here was green BECAUSE
    # it asserted the defect -- the fixture `h-glued` carries no `link_ref` at
    # all, so the count is structurally blind to the node it was supposedly
    # checking. Deleted rather than dressed: `all(... not in _iter_corpus)`,
    # asserted immediately above, is the real measurement.


def test_the_gate_and_links_ask_the_same_definition(project):
    """cli.py no longer restates the shape: one owner, two callers."""
    import cli

    path = _node(project, "hypothesis:h-glued",
                 ['id: "hypothesis:h-glued"', "type: hypothesis",
                  "mint_id: abc123", 'title: "t"', GLUED], "b\n")
    ok, _fm, defect = cli._load_frontmatter(path.read_text())
    assert not ok and "probes=[" in defect
    assert cli._off_shape_keys({"probes": 1, "id": "x"}) == []


def test_a_repaired_artifact_loads_clean(project):
    """ITEM 8 (fixture half): the repaired SHAPE is pinned on a tmp node, so
    this test does not ride on mutable live bytes -- the property of the
    repair (a glued `probes` value recovered under its real key) is a
    property of the code, not of one node's current text."""
    import cli
    path = _node(project, "experiment:a00-fe05fdae-a240f5",
                 ['id: "experiment:a00-fe05fdae-a240f5"', "type: experiment",
                  "mint_id: abc123", "parents: ['hypothesis:h1']",
                  'probes:', "  - one", "  - two", "  - three"], "b\n")
    ok, fm, defect = cli._load_frontmatter(path.read_text())
    assert ok, defect
    assert len(fm["probes"]) == 3
    assert cli._off_shape_keys(fm) == []


def _writer_shaped_probes(value) -> bool:
    """ITEM 1: TRUTHINESS is not a shape. `probes: one` and `probes:\\n  a: 1`
    are both truthy, and `_off_shape_keys` only asks about KEYS, so both were
    certified as "the recovered artifact" the docstring promises is a real
    list. Ask the WRITER rather than restate list-ness: a value the sanctioned
    writer would render and that reads back unchanged IS a list of its making.
    """
    if not isinstance(value, list) or not value:
        # ITEM 4: `probes: []` IS writer-shaped (it round-trips) and it is
        # LEGAL -- a goal with no seeds is exactly `seeds: []`, so the LOADER
        # must not refuse it. The EVIDENCE rule is the consumer's: a recovered
        # artifact with no probes is not evidence, so this gate asks for a
        # non-empty list and the `assert fm["probes"]` below can never go red
        # on a node this function returned.
        return False
    import yaml
    back = yaml.safe_load("".join(l + "\n" for l in node_writer._render_value("probes", value)))
    return isinstance(back, dict) and back.get("probes") == value


def _live_recovered_probes_node(root, cli):
    """The live pin's SUBJECT, not its address. Retire = move to
    `.agi/nodes/deprecated/<type>/` and renames are routine, so one hard-coded
    filename turns a legal graph event red (FileNotFoundError). Prefer the
    named artifact; else the first live experiment node, in sorted order, whose
    `probes` value is a real list that loads in shape. Early-exit: measured
    16ms to the first hit, vs 5.3s to parse all 1962."""
    named = root / "nodes" / "experiment" / "a00-fe05fdae-a240f5.md"
    if named.is_file():
        # ITEM 2: this exit carried NO gate, so a NAMED artifact holding a
        # scalar `probes:` was returned as the recovered evidence and the pin
        # passed on it. Both exits now ask the same question; an off-shape
        # named artifact falls through to the scan instead of being returned.
        text = named.read_text(errors="replace")
        ok, fm, _defect = cli._load_frontmatter(text)
        if ok and _writer_shaped_probes((fm or {}).get("probes")) \
                and not cli._off_shape_keys(fm):
            return named, "the named artifact"
    for path in sorted((root / "nodes" / "experiment").glob("*.md")):
        text = path.read_text(errors="replace")
        if "probes" not in text:
            continue
        ok, fm, _defect = cli._load_frontmatter(text)
        if ok and _writer_shaped_probes(fm.get("probes")) and not cli._off_shape_keys(fm):
            return path, f"first recovered live subject (named artifact retired)"
    return None, "no live experiment node carries a recovered `probes` list"


def test_the_LIVE_repaired_artifact_is_still_in_shape():
    """ITEM 6: the round DELETED the file's only live pin on
    `.agi/nodes/experiment/a00-fe05fdae-a240f5.md` -- the exact artifact the
    parent claim's repair conjunct is about, hand-landed at 5a24ccfbd. With
    it gone nothing held that repair in place. Restored, and narrow: it
    reads the LIVE file and asserts only that a real recovered `probes` list
    still loads clean and in shape. It SKIPS rather than divides when there
    is no `.agi` to pin -- the one way the old `find_project_root` version
    died (`TypeError: ... for /: 'NoneType' and 'str'`, reproduced by the
    parent; fixed by the guard below)."""
    import cli
    root = locations.find_project_root(Path(__file__).resolve())
    if root is None:                      # plugin-only tree: nothing to pin
        pytest.skip("no .agi above this checkout; the live pin has no subject")
    live, why = _live_recovered_probes_node(root, cli)
    if live is None:                      # the subject is gone AND unreplaceable
        pytest.skip(f"live pin has no subject: {why}")
    ok, fm, defect = cli._load_frontmatter(live.read_text(errors="replace"))
    assert ok, defect
    assert fm["probes"], live
    assert cli._off_shape_keys(fm) == []

def test_the_live_pin_survives_its_subjects_legal_absence(project):
    """The death mode the hard-coded address had: retire = MOVE. With the
    named artifact gone the pin must still find a live recovered subject, and
    skip with a naming reason when none exists."""
    import cli
    _node(project, "experiment:a00-other",
          ['id: "experiment:a00-other"', "type: experiment",
           "mint_id: abc123", 'title: "t"', "parents: ['hypothesis:h1']",
           "probes:", "  - one"], "b\n")
    live, why = _live_recovered_probes_node(project, cli)
    assert live is not None and live.name == "a00-other.md", why

    live.unlink()
    live, why = _live_recovered_probes_node(project, cli)
    assert live is None and "no live experiment node" in why


def test_the_live_pin_refuses_a_probes_value_that_is_not_a_list(project):
    """ITEM 5: the sibling docstring claims "whose `probes` value is a real
    list"; the gate asked only for truthiness, so a scalar and a mapping both
    passed. Red without the ITEM 1 fix (failure pasted on
    experiment:a00-85c23976-f70650)."""
    import cli
    base = ['id: "x"', "type: experiment", "mint_id: abc123", 'title: "t"',
            "parents: ['hypothesis:h1']"]
    _node(project, "experiment:a00-scalar",
          ['id: "experiment:a00-scalar"'] + base[1:] + ["probes: one"], "b\n")
    _node(project, "experiment:a00-mapping",
          ['id: "experiment:a00-mapping"'] + base[1:] + ["probes:", "  a: 1"], "b\n")
    live, why = _live_recovered_probes_node(project, cli)
    assert live is None and "no live experiment node" in why

    _node(project, "experiment:a00-list",
          ['id: "experiment:a00-list"'] + base[1:] + ["probes:", "  - one"], "b\n")
    live, why = _live_recovered_probes_node(project, cli)
    assert live is not None and live.name == "a00-list.md", why


def test_the_named_artifact_exit_asks_the_same_gate_as_the_fallback(project):
    """ITEM 2: the resolver had TWO exits and only one of them asked. A named
    artifact whose `probes:` is the scalar `one` was returned as the recovered
    evidence, and the live pin's `assert fm["probes"]` passed on it. ITEM 4 as
    well: `probes: []` is writer-shaped but is not evidence, so it is refused
    here and neither is the named artifact it hides behind."""
    import cli
    base = ["type: experiment", "mint_id: abc123", 'title: "t"',
            "parents: ['hypothesis:h1']"]
    _node(project, "experiment:a00-fe05fdae-a240f5",
          ['id: "experiment:a00-fe05fdae-a240f5"'] + base + ["probes: one"], "b\n")
    _node(project, "experiment:a00-empty",
          ['id: "experiment:a00-empty"'] + base + ["probes: []"], "b\n")
    _node(project, "experiment:a00-good",
          ['id: "experiment:a00-good"'] + base + ["probes:", "  - one"], "b\n")
    live, why = _live_recovered_probes_node(project, cli)
    assert live is not None and live.name == "a00-good.md", why
    ok, fm, defect = cli._load_frontmatter(live.read_text())
    assert ok and fm["probes"] == ["one"], defect


def test_a_declared_container_field_off_the_writers_shape_is_refused_by_name(project):
    """ITEM 1, the production half: the schema's `fields:` block is where a
    key's type is written down, and `cli._load_frontmatter` certified a value
    no `set` produced. Red before the gate, and the defect NAMES the key. A
    bare `tags:` (the writer renders it as the bare line) and an empty list
    stay legal: the writer can write both, and only the CONSUMER gets to call
    an empty field useless."""
    import cli
    sdir = project / "context" / "schemas"
    sdir.mkdir(parents=True)
    (sdir / "[experiment].md").write_text(
        "---\nname: experiment\nfields:\n  probes: {type: list}\n"
        "  tags: {type: list}\nvalidation:\n  required: [id]\n---\n\n# experiment\n")
    base = ["type: experiment", "mint_id: abc123", 'title: "t"',
            "parents: ['hypothesis:h1']"]
    for slug, extra, want_ok in (("off-scalar", ["probes: one"], False),
                                 ("off-mapping", ["probes:", "  a: 1"], False),
                                 ("ok-empty", ["probes: []"], True),
                                 ("ok-bare", ["tags:"], True),
                                 ("ok-list", ["probes:", "  - one"], True)):
        p = _node(project, f"experiment:a00-{slug}",
                  [f'id: "experiment:a00-{slug}"'] + base + extra, "b\n")
        ok, _fm, defect = cli._load_frontmatter(p.read_text(), project)
        assert ok is want_ok, (extra, ok, defect)
        if not ok:
            assert "probes" in defect and "writer" in defect, defect


def _declare(project, kind: str) -> None:
    # A one-field `[experiment]` schema: `probes: {type: kind}`.
    sdir = project / "context" / "schemas"
    sdir.mkdir(parents=True, exist_ok=True)
    (sdir / "[experiment].md").write_text(
        f"---\nname: experiment\nfields:\n  probes: {{type: {kind}}}\n---\n\n# experiment\n")


def test_an_off_shape_value_is_REFUSED_and_the_file_is_left_alone(project):
    """ITEM 1, the headline safety property, as a DELETION probe: the refusal
    branch in `_ensure_frontmatter` (cli.py:463-470) is deletable and the suite
    stays green. Pinned on the FILE: bytes unchanged, refusal told."""
    import cli
    _declare(project, "list")
    p = _node(project, "experiment:a00-refuse",
              ['id: "experiment:a00-refuse"', "type: experiment", "mint_id: abc",
               'title: "t"', "parents: ['hypothesis:h1']", "probes: one"], "b\n")
    before = p.read_bytes()
    # NO manifest (`ap=None`): the refusal must not depend on one.
    ok, msg = cli._ensure_frontmatter(project, p, None, "experiment:a00-refuse")
    assert not ok and "probes" in msg, msg
    assert p.read_bytes() == before, "the node was rewritten by a rebuild"


def test_the_writer_ROUND_TRIP_is_load_bearing_not_just_the_declared_type(project):
    """ITEM 2: the round-trip clause `back.get(k) != v` was removable with no
    test going red -- the "ask the WRITER" half was decoration. A MAPPING whose
    two keys COLLAPSE (`1`, `"1"`) passes the type gate; the writer cannot
    spell it -- re-rendered, one key eats the other."""
    import cli
    _declare(project, "mapping")
    p = _node(project, "experiment:a00-collide",
              ['id: "experiment:a00-collide"', "type: experiment", "mint_id: abc",
               'title: "t"', "parents: ['hypothesis:h1']", "probes:", "  1: two",
               '  "1": one'], "b\n")
    ok, fm, defect = cli._load_frontmatter(p.read_text(), project)
    assert isinstance(fm.get("probes"), dict), fm        # the type gate PASSES
    assert not ok and "probes" in defect, defect          # the ROUND TRIP refuses
