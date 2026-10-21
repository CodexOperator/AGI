"""goal:g5.4.2 round 3 (E): the Gemini PCM duration check. A 344-character take at 24 kHz is about 23 s: GREEN. Mutant: the SAME bytes decoded at 48 kHz are about 11.5 s -> RED;
at 12 kHz about 46 s -> RED. A wrong rate is found and the right one named, for a re-encode with no new request."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_pcm as p  # noqa: E402

N = int(23.0 * 24000 * 2)        # a 23 s take at 24 kHz, 16-bit mono


def test_the_cookbook_rate_is_green():
    assert p.check(N, 344, 24000) == 0


def test_mutant_the_same_bytes_at_48khz_are_red():
    assert p.check(N, 344, 48000) == 1


def test_mutant_the_same_bytes_at_12khz_are_red():
    assert p.check(N, 344, 12000) == 1


def test_best_rate_names_the_right_one():
    assert p.best_rate(N, 344) == 24000
    assert p.best_rate(int(23.0 * 48000 * 2), 344) == 48000       # the bytes of a 23 s take made at 48 kHz decode to 46 s at 24 kHz (RED); 48 kHz fits
    assert p.best_rate(10, 344) is None


def test_window_is_about_17_to_30_seconds_for_the_sample():
    lo, hi = p.window(344)
    assert 17 <= lo <= 18 and 30 <= hi <= 31
