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
