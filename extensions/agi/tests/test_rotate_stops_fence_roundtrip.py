"""The where-it-stops slot must not COMPOUND its fence (belam 09-24, PASS 3
residue): a card slot whose stops text is fed back as the model's own prior
rendered block grew one backtick per rotation, and the rotate-out commit
subject became literally a backtick run. `_render_stops_block` UNWRAPS a text
that is exactly one fence-wrapped block, so render -> re-render is
idempotent; a text that genuinely carries a fence AS ONE PART still nests in
a longer outer fence."""
import sys
import tempfile
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


# ── the LIVE WRITE SEAM (DH.409) ───────────────────────────────────────────
# The render seam is a fixed point, but the SEAM THAT WRITES was not: the
# card is the prompt, so a handback of the slot carries the slot's OWN
# exterior prose as well as its block, and the rewrite writes that prose back
# from the card -- leaving the copy inside the block re-nested it, one deeper
# per rotation. Measured live before the fix: a genuine inner ``` block went
# 4 -> 5 -> 6 over three rotations and a plain slot gained one copy of its
# lead-in line per rotation (experiment:a00-a066dc22-5cb6c8).

CARD = "# belam\n\n## 🔴 Where it stops\n{seed}\n"


def _rotate_n(seed: str, n: int = 4) -> list[str]:
    """Drive the LIVE write seam N times, feeding back exactly what the model
    would copy out of the slot: the whole slot region of the card."""
    out = []
    for _ in range(n):
        with tempfile.TemporaryDirectory() as d:
            card = Path(d) / "card.md"
            card.write_text(CARD.format(seed=seed), encoding="utf-8")
            full, slot = rotate._write_stops_section(card, "belam", seed)
            assert full is not None and slot == "replaced", (full, slot)
            seed = full.split("stops\n", 1)[1].strip("\n")
            out.append(seed)
    return out


def _max_run(region: str) -> int:
    return max((rotate._fence_run(l) for l in region.splitlines()), default=0)


def test_write_seam_is_a_fixed_point_with_exterior_prose():
    for seed in (
            "card edit landed; waiting on the suite\n```\n"
            "prior edit done\nnext: run suite\n```",              # lead-in
            "card edit landed\n```\npytest -q\n```\n"
            "next: rotate out",                                  # both sides
            "```\nprior edit done\nnext: run suite\n```",        # no prose
    ):
        cards = _rotate_n(seed)
        assert len(set(cards)) == 1, cards          # byte-identical
        assert _max_run(cards[0]) == 3, cards


def test_write_seam_does_not_grow_a_real_pre_fix_residue_card():
    """A card an EARLIER broken rotation already duplicated is left alone --
    it stops growing, and the ambiguous duplicate is not silently deleted."""
    seed = ("card edit landed; waiting on the suite\n```\n"
            "card edit landed; waiting on the suite\n"
            "card edit landed; waiting on the suite\n"
            "prior edit done\nnext: run suite\n```")
    cards = _rotate_n(seed)
    assert len(set(cards)) == 1, cards
    assert _max_run(cards[0]) == 3, cards


def test_empty_handback_falls_back_instead_of_dropping_the_slot_body():
    cards = _rotate_n("```\n```")
    assert len(set(cards)) == 1, cards
    assert rotate.STOPS_SUBJECT_FALLBACK in cards[0], cards
    assert _body_lines(cards[0]) == [rotate.STOPS_SUBJECT_FALLBACK]


def test_drop_exterior_prose_touches_only_the_cards_own_prose():
    ext = {"lead-in", "sign-off"}
    # a FOREIGN line outside the fence is the model's own: never dropped
    foreign = "not the card's line\n```\nbody\n```\nsign-off"
    assert rotate._drop_slot_exterior_prose(foreign, ext) == foreign
    # ours, on both sides: dropped, the block kept whole
    ours = "lead-in\n```\nbody\n```\nsign-off"
    assert rotate._drop_slot_exterior_prose(ours, ext) == "```\nbody\n```"
    # a line INSIDE the block that repeats the prose is the model's content
    inside = "lead-in\n```\nlead-in\nbody\n```\nsign-off"
    assert rotate._drop_slot_exterior_prose(inside, ext) == \
        "```\nlead-in\nbody\n```"
    # no fence at all, or no exterior prose: untouched
    assert rotate._drop_slot_exterior_prose("just prose", ext) == "just prose"
    assert rotate._drop_slot_exterior_prose(ours, set()) == ours


def test_slot_exterior_prose_reads_only_outside_the_fence():
    lines = ["lead-in", "```", "body", "lead-in", "```", "sign-off"]
    assert rotate._slot_exterior_prose(lines) == {"lead-in", "sign-off"}
    assert rotate._slot_exterior_prose(["```", "body", "```"]) == set()


# --- an UNPAIRED fence run in the slot's exterior (experiment a00-a177f505)
def test_unpaired_fence_run_in_exterior_does_not_compound_over_n_rotations():
    """A stray (unpaired) ``` in the slot's PROSE position -- below the block
    and after the sign-off -- grew the slot by one nesting level and one copied
    sign-off on EVERY rotation (depth 3 -> 4 -> 5 -> 6, measured live before
    the fix). An unpaired run is a delimiter in prose position, not an opener,
    so it is the card's own exterior line like any other, and the block is the
    handback's FIRST fence PAIR, not everything to the last run."""
    seed = ("card edit landed; waiting on the suite\n```\n"
            "prior edit done\nnext: run suite\n```\n"
            "sign-off prose\n```")
    cards = _rotate_n(seed)
    assert len(set(cards)) == 1, cards          # byte-identical over N
    assert _max_run(cards[0]) == 3, cards
    assert cards[0].count("sign-off prose") == 1, cards


def test_unpaired_run_counts_as_exterior_prose_and_never_swallows_the_tail():
    lines = ["lead-in", "```", "body", "```", "sign-off", "```"]
    assert rotate._slot_exterior_prose(lines) == \
        {"lead-in", "sign-off", "```"}
    # the block is the FIRST pair, so the sign-off below it is droppable
    assert rotate._drop_slot_exterior_prose(
        "\n".join(lines), rotate._slot_exterior_prose(lines)) == \
        "```\nbody\n```"
    # still fail-closed: a FOREIGN line in the tail is the model's own
    foreign = "\n".join(["lead-in", "```", "body", "```",
                         "the model says more", "```"])
    assert rotate._drop_slot_exterior_prose(
        foreign, rotate._slot_exterior_prose(lines)) == foreign
