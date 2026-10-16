"""goal:g5.4.2 fidelity check (council 06:49Z 10-16). Mutants: one sentence deleted from the transcript -> RED (dropped); a spoken tag
(three words the text does not have) -> RED (added); a truncated tail -> RED; a transcript equal to the text -> green; STT noise on a few
words (casing, punctuation, one substituted word, digits for number words) -> green."""
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
    assert "DROPPED" in capsys.readouterr().out


def test_mutant_a_spoken_tag_is_red(capsys):
    hyp = "Low steady voice. " + REF
    assert f.check("[Low, steady voice] " + REF, hyp) == 1          # the tag is stripped from the reference; the voice read it aloud
    assert f.check(REF, hyp) == 1
    assert "ADDED low steady voice" in capsys.readouterr().out


def test_a_tag_in_the_sent_text_that_is_not_spoken_is_green(capsys):
    assert f.check("[Low, steady voice] " + REF, REF) == 0


def test_mutant_truncated_tail_is_red(capsys):
    assert f.check(REF, REF[: len(REF) - 70]) == 1


def test_digits_match_number_words(capsys):
    assert f.check("There were twenty three posts and one trunk.", "There were 23 posts and 1 trunk.") == 0


def test_empty_reference_is_not_green(capsys):
    assert f.check("[just a tag]", "anything") == 1
