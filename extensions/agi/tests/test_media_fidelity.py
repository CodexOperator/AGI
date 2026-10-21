"""goal:g5.4.2 fidelity check (council 06:49Z, 06:53Z 10-16). One ERROR-RUN class (>= N consecutive error ops, sub/del/ins mixed, bridged over a
single matched word). Mutants, each RED: a sentence deleted; a spoken tag; a truncated tail; a 4-word PARAPHRASE (substitutions); a 3-word drop
next to a mis-heard word; a 4-word drop at EVERY position of the text (the run split on a matched common word); 2 inserted words + 1 sub + 1
inserted word. Green: the identical text, STT noise, digits for number words, an unspoken tag, `agi` heard as `a g i` (recorded normalisation),
a transcriber's audio event (stripped and listed). The memory guard refuses a whole-script call."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_fidelity as f  # noqa: E402

REF = ("Well now, good evening, friends, and welcome. Pull up a chair and make yourself comfortable, for we have a long road ahead of us "
       "tonight. I intend to walk it slowly, the way a gentleman walks a porch at sundown. We begin with a few bytes, and a tool small "
       "enough to hold in your hand. Let us ride out together, and see what the machine does with a single word.")


def test_the_same_text_is_green(capsys):
    assert f.check(REF, REF) == 0


def test_stt_noise_is_green(capsys):
    hyp = REF.lower().replace(",", "").replace("friends", "friend").replace("a porch", "the porch")
    assert f.check(REF, hyp) == 0


def test_mutant_one_sentence_deleted_is_red(capsys):
    hyp = REF.replace("I intend to walk it slowly, the way a gentleman walks a porch at sundown. ", "")
    assert f.check(REF, hyp) == 1
    assert "ERROR_RUN" in capsys.readouterr().out


def test_mutant_a_spoken_tag_is_red(capsys):
    hyp = "Low steady voice. " + REF
    assert f.check("[Low, steady voice] " + REF, hyp) == 1          # the tag is stripped from the reference; the voice read it aloud
    assert f.check(REF, hyp) == 1
    assert "heard [low steady voice]" in capsys.readouterr().out


def test_a_tag_in_the_sent_text_that_is_not_spoken_is_green(capsys):
    assert f.check("[Low, steady voice] " + REF, REF) == 0


def test_mutant_truncated_tail_is_red(capsys):
    assert f.check(REF, REF[: len(REF) - 70]) == 1


def test_mutant_a_four_word_paraphrase_is_red(capsys):
    """The reworded sentence is substitutions only: the old pure dropped / added runs and a long chunk's WER (about 0.02) missed it."""
    long_ref = " ".join([REF] * 6)
    hyp = long_ref.replace("the way a gentleman walks a porch", "like a squire strolls a veranda", 1)
    assert f.check(long_ref, hyp, wer_max=0.10) == 1
    assert "ERROR_RUN" in capsys.readouterr().out


def test_mutant_a_three_word_drop_next_to_a_misheard_word_is_red(capsys):
    long_ref = " ".join([REF] * 6)
    hyp = long_ref.replace("walk it slowly, the way", "walk it slowly", 1).replace("gentleman", "gentlemen's", 1)
    assert f.check(long_ref, hyp) == 1


def test_mutant_a_four_word_drop_at_every_position_is_red(capsys):
    """The run split: a common word that matches inside a deleted span must not break the run. Every position of the text, every time."""
    w = f.words(REF, True)
    bad = []
    for i in range(len(w) - 4):
        hyp = " ".join(w[:i] + w[i + 4:])
        if f.check(REF, hyp, wer_max=0.5, echo=False) != 1:      # WER alone cannot save it: the run class must
            bad.append((i, w[i:i + 4]))
    assert bad == []


def test_mutant_two_inserted_one_sub_one_inserted_is_red(capsys):
    hyp = REF.replace("make yourself comfortable", "make so very yourselves oh comfortable")   # ins ins sub ins, no match between
    assert f.check(REF, hyp, wer_max=0.5) == 1


def test_scattered_noise_with_matches_between_is_green(capsys):
    """Two inserted words split by a matched word and a sub elsewhere are STT noise, not a run (the floor the calibration measures)."""
    hyp = REF.replace("make yourself comfortable", "make well yourself indeed comfortable").replace("long road", "tall road")
    assert f.check(REF, hyp, wer_max=0.5) == 0


def test_one_isolated_error_is_green(capsys):
    assert f.check(REF, REF.replace("machine", "machin")) == 0


def test_digits_match_number_words(capsys):
    assert f.check("There were twenty three posts and one trunk.", "There were 23 posts and 1 trunk.") == 0


def test_agi_heard_as_letters_is_green_by_the_recorded_normalisation(capsys):
    assert f.check("The agi engine runs the loop.", "The A G I engine runs the loop.") == 0


def test_an_audio_event_is_stripped_and_listed(capsys):
    assert f.check(REF, "(laughs) " + REF + " [breath]") == 0
    assert "stripped=['(laughs)', '[breath]']" in capsys.readouterr().out


def test_a_strip_that_would_eat_a_spoken_phrase_shows_in_the_list(capsys):
    """A bracketed spoken phrase is stripped by design but never silently: it is in `stripped=`, so the count on the run doc shows it."""
    f.check(REF, "Well now (good evening) friends, " + REF.split("friends,", 1)[1])
    assert "stripped=['(good evening)']" in capsys.readouterr().out


def test_empty_reference_is_not_green(capsys):
    assert f.check("[just a tag]", "anything") == 1


def test_memory_guard_refuses_a_whole_script_call(capsys):
    big = " ".join(["word"] * 8600)
    assert f.check(big, big) == 2
    assert "REFUSED" in capsys.readouterr().out


NEG = "The tool is never gated by hand, and nothing is committed until the turn ends. It cannot move a peer's branch, so no post is harmed. " + REF


def test_mutant_a_dropped_never_is_red_whatever_the_wer(capsys):
    """alive RAN 'an edit is never gated' -> 'an edit is gated' = GREEN: one isolated error is green by design, a negation is PROTECTED."""
    assert f.check(NEG, NEG) == 0
    assert f.check(NEG, NEG.replace("is never gated", "is gated"), wer_max=0.5) == 1
    assert "PROTECTED sent [never]" in capsys.readouterr().out


def test_mutant_each_protected_token_dropped_or_added_is_red(capsys):
    for tok, base, bad in [("nothing", "nothing is committed", "is committed"), ("cannot", "It cannot move", "It can move"),
                           ("no", "so no post is harmed", "so a post is harmed"), ("not", "It is not done", "It is done"),
                           ("none", "none of them", "some of them"), ("without", "went without it", "went with it")]:
        assert f.check(base, bad, wer_max=0.9) == 1, tok
    assert f.check("The engine runs it.", "The engine does not run it.", wer_max=0.9) == 1       # a negation ADDED inverts a claim too


def test_contractions_are_spelled_out_so_dont_vs_do_not_is_green(capsys):
    assert f.check("It doesn't move and it can't leave.", "It does not move and it cannot leave.") == 0


def test_an_isolated_error_on_a_plain_word_is_still_green(capsys):
    assert f.check(NEG, NEG.replace("committed", "comitted")) == 0


def test_curly_apostrophes_are_ascii_so_a_clean_take_is_green(capsys):
    """alive RAN 'a post cannot move a peer ref' vs 'a post can\u2019t move ...' -> PROTECTED RED: a clean take written with a curly apostrophe
    (as an STT often writes it) must read GREEN, never poison the noise floor."""
    assert f.check("A post cannot move a peer ref.", "A post can\u2019t move a peer ref.") == 0
    assert f.check("It doesn't move and it won't leave.", "It doesn\u2019t move and it won\u2019t leave.") == 0
    assert f.check("A post cannot move a peer ref.", "A post can move a peer ref.") == 1           # a real drop is still RED


def test_mutant_one_number_word_swapped_in_a_long_chunk_is_red(capsys):
    """alive RAN a 96-word chunk with 'fourteen' -> 'forty' once -> GREEN. Number words are PROTECTED, in a ~300-word chunk too."""
    long_ref = " ".join([REF] * 4) + " There were fourteen posts on the road and two hundred and fourteen nodes."
    assert len(f.words(long_ref, True)) > 280
    assert f.check(long_ref, long_ref) == 0
    assert f.check(long_ref, long_ref.replace("fourteen posts", "forty posts")) == 1
    assert "PROTECTED sent [fourteen] heard [forty]" in capsys.readouterr().out
    assert f.check(long_ref, long_ref.replace("two hundred and fourteen", "two hundred and forty")) == 1
    assert f.check(long_ref, long_ref.replace("fourteen posts", "14 posts")) == 0                    # digits for the same number word are fine


def test_the_four_normalised_pairs_are_green(capsys):
    """council 07:01Z (T): a correctly spoken line must not go RED for its form."""
    assert f.check("There were one thousand nodes.", "There were 1,000 nodes.") == 0
    assert f.check("It cost zero point one zero dollars.", "It cost $0.10.") == 0
    assert f.check("It was the twenty third post.", "It was the 23rd post.") == 0
    assert f.check("A post cannot move it.", "A post can not move it.") == 0
    assert f.words("1,000 nodes", False) == ["one", "thousand", "nodes"]
    assert f.words("the 1st, 2nd, 3rd, 5th, 12th, 20th and 21st", False) == (
        "the first second third fifth twelfth twentieth and twenty first".split())


def test_mutant_twenty_three_to_thirty_three_in_a_long_chunk_is_red(capsys):
    long_ref = " ".join([REF] * 4) + " It was the twenty third post of the road."
    assert len(f.words(long_ref, True)) > 280
    assert f.check(long_ref, long_ref) == 0
    assert f.check(long_ref, long_ref.replace("twenty third", "thirty third")) == 1
    assert f.check(long_ref, long_ref.replace("twenty third", "23rd")) == 0
    assert f.check(long_ref, long_ref.replace("twenty third", "33rd")) == 1
    assert f.check("There were one thousand nodes.", "There were 1,100 nodes.", wer_max=0.9) == 1


def test_dollar_falsifier_ten_cents_vs_ten_dollars(capsys):
    """council 07:04Z (vi): REF 'ten cents' vs HYP 'ten cents' GREEN, vs 'ten dollars' RED (a swapped unit is a changed fact). The script today has
    no $ or decimal (grep over the 621 rendered sentences: 0 hits), so this guards a line that ever does."""
    ref = " ".join([REF] * 4) + " It cost ten cents."
    assert f.check(ref, ref) == 0
    assert f.check(ref, ref.replace("ten cents", "ten dollars")) == 1
    assert f.check(ref, ref.replace("ten cents", "10 cents")) == 0
    assert f.check(ref.replace("ten cents", "$0.10"), ref.replace("ten cents", "$0.10")) == 0
    assert f.check(ref.replace("ten cents", "$0.10"), ref.replace("ten cents", "$0.10").replace("$0.10", "zero point one zero dollars")) == 0


def test_mutant_a_normalise_entry_mapping_to_nothing_is_refused():
    import pytest
    with pytest.raises(ValueError):
        f.validate_normalise([(r"\\bsect\\b", "")])
    with pytest.raises(ValueError):
        f.validate_normalise([(r"\\bsect\\b", "   ")])
    assert f.validate_normalise([(r"\\bp y\\b", "py")])
    assert f.NORMALISE == f.validate_normalise(f.NORMALISE)


def test_jargon_spelling_entries_from_the_c2_chunk_are_green(capsys):
    """key S, schedar-c2a (07:51Z): `worktree` heard as `work tree` and `bin dot new` written `bin.new` are the SAME words, not errors."""
    ref = "It attaches a worktree to it. It writes the block into a fresh directory named bin dot new. Each block becomes executable."
    assert f.check(ref, "It attaches a work tree to it. It writes the block into a fresh directory named bin.new. Each block becomes executable.") == 0
    assert f.words("bin.new", False) == ["bin", "dot", "new"]
    assert f.words("A work tree", False) == ["a", "worktree"]


def test_a_dropped_dot_word_is_still_an_isolated_error_not_a_normalisation(capsys):
    """`sed` heard as `said` is NOT normalised (a mispronunciation is the owner's ears, scope (iii)): it stays one plain-word error."""
    ref = " ".join([REF] * 3) + " the very same sed range we studied."
    hyp = ref.replace("sed range", "said range")
    assert f.check(ref, hyp) == 0                       # one isolated plain-word error is green by design
    assert f.check(ref, hyp.replace("very same", "")) == 1      # but a drop beside it makes a run
