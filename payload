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

Detection matches the actual HTML comment opening tag (`<!-- THOUGHT:BEGIN`),
not a bare substring search for `THOUGHT:BEGIN` anywhere in the file. That
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

#: The real marker, anchored on its HTML comment open — not a bare substring
#: match, which a node's own prose can legitimately quote as documentation
#: (see module docstring).
THOUGHT_OPEN_RE = re.compile(r"<!--\s*THOUGHT:BEGIN")


def _count_thought_blocks(text: str) -> int:
    return len(THOUGHT_OPEN_RE.findall(text))


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
        count = _count_thought_blocks(nf.read_text(encoding="utf-8", errors="replace"))
        if count > 1:
            offenders.append((str(nf.relative_to(root)), count))

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
