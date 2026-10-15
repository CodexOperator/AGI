"""Regression: a node carries at most one authored THOUGHT:BEGIN block
(goal:g2.11).

The schema allows exactly one such block per node, rewritten from scratch on
every version, never appended to. `.agi/nodes/.geometry/crons.md` carried two
before this fix: an older one about the node's own parentage left at the
bottom, and a newer one about retiring two cadences added at the top — because
every past edit to that node replaced the `crons_live` boolean through the
whole body (including inside the old THOUGHT block's prose) without ever
removing the stale block underneath it. It was the only node of 814 in that
state.

`test_the_real_corpus_has_no_node_with_two_thought_blocks` is the test that
would have caught it: it scans this repo's own live `.agi/nodes/`, not a
fixture, so a future edit that reintroduces the same replace-all mistake on
any node fails here rather than being found by inspection again.

Detection is node_writer's ONE definition (`thought_blocks`): both markers at
column 0. An indented or inline marker is a QUOTATION -- the 15 "offenders" an
unanchored count named on 09-29 were all quoted review evidence
(verdict:dg2-b-thought-marker), and they stay byte-unchanged. Before that,
detection matched the HTML comment opening tag (`<!-- THOUGHT:BEGIN`), not a
bare substring search for `THOUGHT:BEGIN` anywhere in the file. That
distinction is not cosmetic: the node this fix itself produced
(`mvp:g11-crons-metrics-residual`) documents the `grep -c 'THOUGHT:BEGIN'
...` gate command in its own body, as plain text inside a fenced code block —
a bare substring count would flag that node as a second offender for
*describing* the marker, not for carrying two of them. Matching the real
opening tag is both more correct and is what avoids that false positive.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import locations  # noqa: E402
import node_writer  # noqa: E402


def _count_thought_blocks(text: str) -> int:
    return len(node_writer.thought_blocks(text))


#: A column-0 BEGIN line. `thought_blocks` pairs a BEGIN with the next END, so
#: a second BEGIN with no END of its own (B,B,E) or an unclosed one (BE,B) is
#: silently one block; counting the openers keeps the row as strict as it was
#: before the detector moved to the one definition (mur wf_a56d005b-d6b row 9).
_COL0_BEGIN = re.compile(r"^<!--\s*THOUGHT:BEGIN", re.MULTILINE)


def _offends(text: str) -> bool:
    blocks = _count_thought_blocks(text)
    return blocks > 1 or len(_COL0_BEGIN.findall(text)) != blocks


def _project_root() -> Path | None:
    return locations.find_project_root(Path(__file__).resolve())


def test_the_real_corpus_has_no_node_with_two_thought_blocks():
    """The actual regression, over the real corpus rather than a fixture —
    `nodes_dir.rglob` reads the live-first + deprecated-sibling layout the same
    way `stitch.py`/`level3.py`/`zoom.py` do, so a retired node is checked too."""
    root = _project_root()
    if root is None:
        pytest.skip("not running inside an agi project checkout")
    nodes_dir = root / "nodes"
    if not nodes_dir.is_dir():
        pytest.skip(f"no nodes/ under resolved project root {root}")

    offenders = []
    for nf in sorted(nodes_dir.rglob("*.md")):
        text = nf.read_text(encoding="utf-8", errors="replace")
        if _offends(text):
            offenders.append((str(nf.relative_to(root)), _count_thought_blocks(text),
                              len(_COL0_BEGIN.findall(text))))

    assert offenders == [], (
        "node(s) carrying more than one THOUGHT:BEGIN block (schema allows "
        f"exactly one, rewritten from scratch per version): {offenders}"
    )


def test_a_node_with_two_blocks_is_the_shape_this_test_catches():
    """Hermetic sanity check on the detection itself, independent of whatever
    the real corpus currently contains: two real markers must count as two."""
    text = (
        "---\nid: \"idea:x\"\ntype: idea\n---\n\n"
        "<!-- THOUGHT:BEGIN -->\nold reasoning, should have been replaced\n"
        "<!-- THOUGHT:END -->\n\nbody prose here\n\n"
        "<!-- THOUGHT:BEGIN -->\nnew reasoning, added instead of replacing\n"
        "<!-- THOUGHT:END -->\n"
    )
    assert _count_thought_blocks(text) == 2


def test_a_node_with_one_block_is_the_shape_that_passes():
    text = (
        "---\nid: \"idea:x\"\ntype: idea\n---\n\n"
        "<!-- THOUGHT:BEGIN -->\nonly one, as the schema requires\n"
        "<!-- THOUGHT:END -->\n\nbody prose here\n"
    )
    assert _count_thought_blocks(text) == 1


def test_a_node_with_no_block_is_also_fine():
    """Absent is a valid state (the THOUGHT region is optional) — only a
    *second* block is the defect."""
    text = "---\nid: \"idea:x\"\ntype: idea\n---\n\nbody prose here, no thought at all\n"
    assert _count_thought_blocks(text) == 0


def test_quoting_the_marker_as_documentation_is_not_a_false_positive():
    """The exact case this fix's own node hits: a node's body may need to show
    the literal gate command (`grep -c 'THOUGHT:BEGIN' path`) as plain text
    while still carrying only one real marker. A bare substring count would
    misread that as two; anchoring on the HTML comment open must not."""
    text = (
        "---\nid: \"mvp:x\"\ntype: mvp\n---\n\n"
        "Ran the gate:\n\n"
        "```\n$ grep -c 'THOUGHT:BEGIN' .agi/nodes/.geometry/crons.md\n1\n```\n\n"
        "<!-- THOUGHT:BEGIN -->\nthe one real block\n<!-- THOUGHT:END -->\n"
    )
    assert text.count("THOUGHT:BEGIN") == 2       # the naive count would flag this
    assert _count_thought_blocks(text) == 1        # the real count does not


# --- goal:g7.16.1.1.1 · hypothesis:thought-verb-edits-only-the-top-level-thought-block
# The falsifier rows (council bundle 1, director-general-2): RED on the trunk at
# 32ef9a785, green since director-general-3's build (column-0 _THOUGHT_RE).
_CLAIM = "hypothesis:thought-verb-edits-only-the-top-level-thought-block"
_QUOTED = ("    <!-- THOUGHT:BEGIN -->\n    quoted review evidence\n"
           "    <!-- THOUGHT:END -->\n")
_TOP = "<!-- THOUGHT:BEGIN -->\nreal top-level thought\n<!-- THOUGHT:END -->\n"


def _nw():
    import node_writer
    return node_writer


def test_extract_thought_skips_an_indented_quoted_pair():
    body = "# n\n\n## Review\n" + _QUOTED + "\n" + _TOP
    assert "real top-level thought" in (_nw().extract_thought(body) or "")


def test_a_body_with_only_a_quoted_pair_has_no_thought():
    assert _nw().extract_thought("# n\n\n## Review\n" + _QUOTED) is None


def test_a_version_write_carries_the_real_block_past_a_quoted_one():
    old = "# n\n\n## Review\n" + _QUOTED + "\n" + _TOP
    new = "# n\n\n## Review\n" + _QUOTED + "\nbody v2\n"
    assert "real top-level thought" in _nw()._carry_thought(old, new)


def test_no_thought_marker_regex_outside_node_writer():
    """A raw-string pattern carrying the marker is a regex copy. The surface is
    every engine .py outside tests/ plus the graph's context/ tree (the sql
    mirror lives there), not bin/ alone (mur wf_a56d005b-d6b row 10); tests/
    holds fixture patterns by design. node_writer.py is exempt by PATH."""
    raw = re.compile(r"""\br["'][^"']*THOUGHT:BEGIN""")
    skip = {"tests", "__pycache__", "node_modules", ".venv", "venv"}
    root = _project_root()
    surfaces = [BIN.parent] + ([root / "context"] if root else [])
    copies = [f"{p}:{i}" for s in surfaces for p in sorted(s.rglob("*.py"))
              if p != BIN / "node_writer.py" and not skip & set(p.relative_to(s).parts)
              for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1)
              if raw.search(line)]
    assert copies == []


def test_a_begin_without_its_own_end_is_an_offender():
    B, E = "<!-- THOUGHT:BEGIN -->\n", "<!-- THOUGHT:END -->\n"
    assert _offends(B + "a\n" + B + "b\n" + E)          # B,B,E
    assert _offends(B + "a\n" + E + B + "b\n")          # BE,B (unclosed)
    assert not _offends(B + "a\n" + E)
    assert not _offends(_QUOTED + B + "a\n" + E)


def test_the_thought_verb_rewrites_the_real_block_and_leaves_the_quote():
    body = "# n\n\n## Review\n" + _QUOTED + "\n" + _TOP
    out = _nw().replace_thought(body, "<!-- THOUGHT:BEGIN -->\nv2\n<!-- THOUGHT:END -->")
    assert _QUOTED in out and "\nv2\n" in out and "real top-level thought" not in out


def test_an_inline_end_marker_inside_the_real_block_does_not_close_it():
    """4 live experiment nodes quote the END marker inline inside their block."""
    body = ("<!-- THOUGHT:BEGIN -->\nthe verb matched `<!-- THOUGHT:END -->` first\n"
            "kept\n<!-- THOUGHT:END -->\n")
    assert _nw().thought_text(body).endswith("kept")


# --- goal:g7.16.1.2.7 · hypothesis:node-writer-owns-the-thought-marker-strings
# (council bundle 2, director-general-2). Strict xfail: RED on the trunk at
# ef73dec71 -- snapshot-goals.py:258/:260 and write.py:2918/:2920 spelled them;
# green since director-general-3's build (node_writer.THOUGHT_BEGIN/END).
def test_the_marker_strings_live_in_node_writer_only():
    nw = _nw()
    assert nw.THOUGHT_BEGIN.startswith("<!-- THOUGHT:BEGIN") and nw.THOUGHT_END == "<!-- THOUGHT:END -->"
    for name in ("snapshot-goals.py", "write.py"):
        text = (BIN / name).read_text(encoding="utf-8")
        assert "<!-- THOUGHT:BEGIN" not in text and "<!-- THOUGHT:END" not in text, name


@pytest.fixture()
def project(tmp_path: Path) -> Path:   # the throwaway `.agi/` graph test_write.py builds (one hypothesis node)
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "hypothesis" / "h1.md").write_text(
        '---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
        'title: "t"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
        'status: pending\n---\n\nthe body\n\n<!-- THOUGHT:BEGIN -->\nthe old reason\n<!-- THOUGHT:END -->\n')
    return graph


# g1.31 #12 (PASS B3, verify_thought-verb-edits-only-the-top-level-thought-block):
# falsifier 2's second half had no row -- a body that only QUOTES a THOUGHT pair
# (indented or `> `-quoted, never column 0) and holds NO real block: `thought`
# ADDS one top-level block (replace_thought's append branch, reached through
# _compose_body) and leaves the quotation byte-identical, the quote at the end
# of the body too; the dry run writes nothing.
@pytest.mark.parametrize("quote", [
    "    <!-- THOUGHT:BEGIN -->\n    quoted review evidence\n    <!-- THOUGHT:END -->",
    "> <!-- THOUGHT:BEGIN -->\n> quoted review evidence\n> <!-- THOUGHT:END -->"])
@pytest.mark.parametrize("tail", ["\n\nafter the quote\n", "\n"])
def test_g131_12_thought_on_a_quoted_only_body_adds_one_block_and_keeps_the_quote(project, quote, tail):
    import write
    node = project / "nodes/hypothesis/h1.md"
    body = "\n# h1\n\n## Review\n\n" + quote + tail
    node.write_text(node.read_text().split("\n---\n", 1)[0] + "\n---\n" + body)
    assert node_writer.thought_blocks(body) == [] and node_writer.extract_thought(body) is None
    before, root = node.read_text(), ["--root", str(project)]
    assert write.main(["hypothesis:h1", "thought the new reason", "--dry-run"] + root) == 0
    assert node.read_text() == before
    assert write.main(["hypothesis:h1", "thought the new reason"] + root) == 0
    after = write._read_body_text(project, "hypothesis:h1")
    blocks = node_writer.thought_blocks(after)
    assert len(blocks) == 1 and "the new reason" in blocks[0], after
    assert after.count(quote) == 1 and after.index(quote) < after.index(blocks[0]), after
    assert after.count("quoted review evidence") == 1
    assert ("after the quote" in after) == (tail != "\n"), after
    block = f"{node_writer.THOUGHT_BEGIN}\nv\n{node_writer.THOUGHT_END}"
    out = node_writer.replace_thought(body, block)   # the reviewer's pure-function probe
    assert out.count(quote) == 1 and node_writer.thought_blocks(out) == [block]
