"""goal:g7.16.1.7.1.2 -- a post's first turn is a render of its LIVE card.

The card NODE wins over a copied card file (a rotation flattens the quorum
link into a copy that goes stale); the first turn names the card's id, mint
id and version and the active formation line (row F, config:formations at
render time); a recovered director renders instead of being handed a raw file,
and a refused render still carries the live card.
"""
import json
import re
import sys
from pathlib import Path

_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

from test_brief_render import BIN, _root, _write, brief  # noqa: E402

CARD = ("---\nid: doc:card-some-post\nmint_id: m1a2b3\ntype: doc\n---\n"
        "# doc:card-some-post\n\n{body}\n")


def _card_root(tmp_path):
    root = _root(tmp_path, parts={"director": ["head", "card"]},
                 card="STALE-COPY-SENTINEL\n")
    node = _write(root, "nodes/doc/card-some-post.md",
                  CARD.format(body="CARD-V1-SENTINEL"))
    return root, node


def test_a_second_render_carries_the_card_node_edit(tmp_path):
    root, node = _card_root(tmp_path)
    copy = str(root / "sessions" / "quorum" / "some-post.md")
    first = brief.render(post="some-post", project_root=root, card_file=copy)
    assert "CARD-V1-SENTINEL" in first and "STALE-COPY-SENTINEL" not in first
    assert "[card] doc:card-some-post · mint m1a2b3" in first
    node.write_text(CARD.format(body="CARD-V2-SENTINEL"), encoding="utf-8")
    second = brief.render(post="some-post", project_root=root, card_file=copy)
    assert "CARD-V2-SENTINEL" in second and "CARD-V1-SENTINEL" not in second


def test_a_named_file_that_is_a_node_link_wins(tmp_path):
    """A caller-named path that links INTO nodes/ (the seat tree's own node)
    is read -- it is the node, not a copy."""
    root, node = _card_root(tmp_path)
    other = _write(root, "wt/nodes/doc/card-some-post.md",
                   CARD.format(body="SEAT-TREE-NODE-SENTINEL"))
    link = root / "sessions" / "quorum" / "linked.md"
    link.symlink_to(other)
    out = brief.render(post="some-post", project_root=root, card_file=str(link))
    assert "SEAT-TREE-NODE-SENTINEL" in out


def test_the_first_turn_prints_the_active_formation_line(tmp_path):
    root, _node = _card_root(tmp_path)
    fm = _write(root, "nodes/.geometry/formations.md",
                "---\nid: config:formations\ntype: config\nactive: doc:f-one\n"
                "templates:\n  doc:f-one: g9.1\n  doc:f-two: g9.2\n---\nbody\n")
    assert "[formation] doc:f-one · goal:g9.1" in brief.render(
        post="some-post", project_root=root)
    fm.write_text(fm.read_text().replace("active: doc:f-one", "active: doc:f-two"))
    assert "[formation] doc:f-two · goal:g9.2" in brief.render(
        post="some-post", project_root=root)


def test_a_copy_with_no_node_is_named_as_a_copy(tmp_path):
    root = _root(tmp_path, parts={"director": ["head", "card"]},
                 card="ONLY-COPY-SENTINEL\n")
    out = brief.render(post="some-post", project_root=root)
    assert "ONLY-COPY-SENTINEL" in out
    assert "[card] some-post.md -- a copied file, not a card node" in out


def test_a_refused_render_still_carries_the_live_card(tmp_path, monkeypatch):
    """rotate's legacy fallback (render refused) appends the card through
    brief.card_text: the NODE, never the stale copy."""
    sys.path.insert(0, str(BIN))
    import rotate
    root, _node = _card_root(tmp_path)
    _write(root, "config.json", json.dumps({"brief": {"parts": {}}}))
    seen = {}
    monkeypatch.setattr(
        rotate, "_build_harness_command",
        lambda harness, **kw: (seen.setdefault("prompt", kw["prompt_text"]), ["x"])[1])
    rotate._assembled_successor_command(
        name="some-post", tier="director", model=None, effort=None,
        settings=None, debug_file="/dev/null", project_root=root,
        card_file=str(root / "sessions" / "quorum" / "some-post.md"))
    assert "CARD-V1-SENTINEL" in seen["prompt"]
    assert "STALE-COPY-SENTINEL" not in seen["prompt"]


def test_no_launch_path_reads_a_card_file_itself():
    """Negative: heal and rotate never read a quorum card themselves and
    heal never hands one over as the whole prompt -- the card is read by
    brief.card_text only."""
    for name in ("heal.py", "rotate.py"):
        src = (BIN / name).read_text(encoding="utf-8")
        assert not re.search(r"quorum[^\n]*read_text|read_text[^\n]*quorum", src), name
    heal_src = (BIN / "heal.py").read_text(encoding="utf-8")
    assert "prompt_file = str(card)" not in heal_src
