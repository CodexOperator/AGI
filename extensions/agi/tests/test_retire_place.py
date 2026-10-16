"""goal:g4.18.5.4 -- a retirement is status AND move, one act; a status-only deprecate is refused.

The false state this closes: 6 nodes carried `status: deprecated` in live dirs, written by three
pre-verb writers that set the status without the move. Rows, both directions:

- r1  `retire` sets the status, moves the file to nodes/deprecated/<type>/, keeps the mint id and the
      bytes otherwise; active + deprecated (the node-file total) is unchanged.
- r2  a status-only deprecate (`set status deprecated`, update_node) is REFUSED by name and writes nothing.
- r3  the verb through write.py (`retire <note>`) does the same, note landing as deprecated_note.
- r4  a node already carrying the status in a live dir (the 6) is MOVED by retire, content untouched.
- r5  a name collision at the target refuses and leaves the node where it was, status unchanged.
- r6  retired-place: 0 outside / 0 inside on a clean tree; the stub mutant (status only) -> outside 1;
      a file inside deprecated/ without the status -> inside 1; the total is the same in all three.
- r7  dispatch's orphan-scaffold retirement goes through the same verb (no status-only half).
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
import verification  # noqa: E402
import write  # noqa: E402
from tests.veto_cell import write_free_veto  # noqa: E402

NODE = ('---\nid: "hypothesis:{n}"\ntype: hypothesis\nmint_id: {mint}\ntitle: "t"\n'
        'testable_claim: "c"\nscaffold_hash: deadbeef\nstatus: {status}\n---\n\nthe body\n')


def _put(graph: Path, rel: str, n: str, mint: str, status: str) -> Path:
    p = graph / "nodes" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(NODE.format(n=n, mint=mint, status=status))
    return p


@pytest.fixture()
def graph(tmp_path: Path) -> Path:
    g = tmp_path / ".agi"
    (g / "nodes" / "hypothesis").mkdir(parents=True)
    (g / "config.json").write_text("{}")
    write_free_veto(g / "nodes" / ".geometry")
    _put(g, "hypothesis/h1.md", "h1", "m1", "pending")
    _put(g, "hypothesis/h2.md", "h2", "m2", "pending")
    return g


def _total(g: Path) -> int:
    return len(list((g / "nodes").rglob("*.md")))


def test_r1_retire_is_status_and_move_with_the_mint_id_kept(graph):
    before = _total(graph)
    res = node_writer.retire_node(graph, "hypothesis:h1", note="superseded")
    assert res.status == node_writer.UPDATED
    assert not (graph / "nodes/hypothesis/h1.md").exists()
    moved = graph / "nodes/deprecated/hypothesis/h1.md"
    text = moved.read_text()
    assert "status: deprecated" in text and "mint_id: m1" in text and "deprecated_note: superseded" in text
    assert "the body" in text
    assert _total(graph) == before


def test_r2_a_status_only_deprecate_is_refused_by_name_and_writes_nothing(graph):
    p = graph / "nodes/hypothesis/h1.md"
    was = p.read_text()
    res = node_writer.update_node(graph, "hypothesis:h1", set_fm={"status": "deprecated"})
    assert res.status == node_writer.REJECTED
    assert "status: deprecated without the move" in res.reason and "retire" in res.reason
    assert p.read_text() == was
    e = write.Edit("hypothesis:h1")
    write.verb_set(e, "status", "deprecated")
    assert write.submit(graph, e, actor="t").status == node_writer.REJECTED
    assert p.read_text() == was


def test_r2b_other_status_writes_still_land(graph):
    res = node_writer.update_node(graph, "hypothesis:h1", set_fm={"status": "active"})
    assert res.status == node_writer.UPDATED


def test_r3_the_verb_through_write_py(graph):
    e = write.Edit("hypothesis:h2")
    write.verb_retire(e, "folded into h1")
    res = write.submit(graph, e, actor="t")
    assert res.status == node_writer.UPDATED
    text = (graph / "nodes/deprecated/hypothesis/h2.md").read_text()
    assert "status: deprecated" in text and "deprecated_note: folded into h1" in text
    assert not (graph / "nodes/hypothesis/h2.md").exists()
    assert "retire" in write.VERBS and write.ARITY["retire"] == 1 and "retire" in write.VERB_EXAMPLES


def test_r4_a_live_dir_node_already_marked_deprecated_is_moved_not_rewritten(graph):
    p = _put(graph, "hypothesis/h3.md", "h3", "m3", "deprecated")
    was = p.read_text()
    res = node_writer.retire_node(graph, "hypothesis:h3")
    assert res.status == node_writer.UNCHANGED
    dest = graph / "nodes/deprecated/hypothesis/h3.md"
    assert dest.read_text() == was and not p.exists()


def test_r5_a_namesake_at_the_target_refuses_and_leaves_the_node(graph):
    _put(graph, "deprecated/hypothesis/h1.md", "h1-old", "m9", "deprecated")
    p = graph / "nodes/hypothesis/h1.md"
    was = p.read_text()
    res = node_writer.retire_node(graph, "hypothesis:h1")
    assert res.status == node_writer.REJECTED and "already exists" in res.reason
    assert p.read_text() == was


def test_r6_retired_place_both_directions_and_the_stub_mutant(graph):
    base = verification.check_retired_place(graph)
    assert base.status == "PASS" and base.number["outside"] == 0 and base.number["inside"] == 0
    total = base.number["total"]
    # the mutant: a stub given the status only
    p = graph / "nodes/hypothesis/h1.md"
    p.write_text(p.read_text().replace("status: pending", "status: deprecated"))
    mut = verification.check_retired_place(graph)
    assert mut.status == "FAIL" and mut.number["outside"] == 1 and mut.number["inside"] == 0
    assert "hypothesis/h1.md" in mut.note and mut.number["total"] == total
    # the quoted spelling the parser retires is the same node (a line anchor misses it)
    p.write_text(p.read_text().replace("status: deprecated", 'status: "Deprecated"'))
    assert verification.check_retired_place(graph).number["outside"] == 1
    # healed through the verb: back to 0/0, same total
    assert node_writer.retire_node(graph, "hypothesis:h1").status == node_writer.UPDATED   # the spelling is normalised
    healed = verification.check_retired_place(graph)
    assert healed.status == "PASS" and healed.number == {"outside": 0, "inside": 0, "total": total}
    # the other direction: a file in deprecated/ without the status
    _put(graph, "deprecated/hypothesis/h4.md", "h4", "m4", "pending")
    inv = verification.check_retired_place(graph)
    assert inv.status == "FAIL" and inv.number["inside"] == 1 and inv.number["outside"] == 0
    assert "deprecated/hypothesis/h4.md" in inv.note


def test_r6b_the_pass_carries_the_check_at_rotation_and_full():
    src = (BIN / "verification.py").read_text()
    assert "results.append(check_retired_place(groot))" in src


def test_r7_dispatch_orphan_retirement_is_the_verb(graph):
    import dispatch
    assert dispatch._deprecate_orphan_scaffold(graph, "hypothesis:h1", "agent-x") is True
    assert (graph / "nodes/deprecated/hypothesis/h1.md").is_file()
    assert not (graph / "nodes/hypothesis/h1.md").exists()
    assert verification.check_retired_place(graph).status == "PASS"
