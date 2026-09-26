"""The where-it-stops slot must not COMPOUND its fence (belam 09-24, PASS 3
residue): a card slot whose stops text is fed back as the model's own prior
rendered block grew one backtick per rotation, and the rotate-out commit
subject became literally a backtick run. `_render_stops_block` UNWRAPS a text
that is exactly one fence-wrapped block, so render -> re-render is
idempotent; a text that genuinely carries a fence AS ONE PART still nests in
a longer outer fence."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate


def _depth(block: str) -> int:
    return rotate._fence_run(block.splitlines()[0])


def _body_lines(block: str) -> list[str]:
    return block.splitlines()[1:-1]


def test_render_round_trip_keeps_fence_depth_three_over_n_rotations():
    text = ("prior agent finished the card edit\n"
            "next: run the suite")
    b1 = rotate._render_stops_block(text, None)
    assert _depth(b1) == 3
    assert _body_lines(b1) == text.splitlines()
    b2 = rotate._render_stops_block(b1, None)
    b3 = rotate._render_stops_block(b2, None)
    for b in (b1, b2, b3):
        assert _depth(b) == 3, b
        assert _body_lines(b) == text.splitlines(), b


def test_re_render_through_replace_keeps_depth_three():
    """The REPLACE seam too: `_stops_replace_fenced_region` feeds the prior
    block back through `_render_stops_block` -- the depth must not move."""
    text = "first line\nsecond line"
    lines = rotate._render_stops_block(text, None).splitlines()
    for _ in range(3):
        new = rotate._stops_replace_fenced_region(
            list(lines), rotate._render_stops_block(
                "\n".join(lines), None))
        assert new is not None
        lines = new
    assert _depth("\n".join(lines)) == 3
    assert _body_lines("\n".join(lines)) == text.splitlines()


def test_inner_fence_is_content_and_outer_run_exceeds_it():
    """A stops text that GENUINELY contains a ``` block keeps nesting in a
    LONGER outer fence (goal:g15.25 residue (iii)) -- the regression the
    unwrap must not cause -- and the block round-trips at that same depth."""
    text = ("ran the suite; snippet kept for the next agent:\n"
            "```\npytest -q\n```\n"
            "next: rotate out")
    b1 = rotate._render_stops_block(text, None)
    assert _depth(b1) == 4, b1
    assert _body_lines(b1) == text.splitlines()
    b2 = rotate._render_stops_block(b1, None)
    b3 = rotate._render_stops_block(b2, None)
    for b in (b1, b2, b3):
        assert _depth(b) == 4, b
        assert _body_lines(b) == text.splitlines(), b
    # the inner ``` is CONTENT, and CommonMark pairs the outer fence
    assert rotate._fence_run(b3.splitlines()[2]) == 3


def test_subject_tail_is_never_a_fence_run():
    for text in ("```\n\n```\n````\n",
                 "```\nreal prose here\n```\n",
                 "```",
                 "   \n\n",
                 "```\nran the suite\n```\n\ndiff requested: -"):
        tail = rotate._stops_subject_tail(text)
        assert rotate._fence_run(tail) == 0, (text, tail)
        assert tail, text
    assert rotate._stops_subject_tail("```\n\n```\n````\n") == \
        rotate.STOPS_SUBJECT_FALLBACK
    assert rotate._stops_subject_tail(
        "```\n" + "x" * 200 + "\n```") .startswith("x")
    assert len(rotate._stops_subject_tail("x" * 200)) == 80
