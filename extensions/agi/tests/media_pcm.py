#!/usr/bin/env python3
"""media_pcm.py FILE.pcm CHARS [--rate=24000]: the Gemini PCM check of goal:g5.4.2 round 3 (council 07:06Z (E)).
OpenRouter's Gemini TTS returns raw signed 16-bit mono PCM at 24 kHz (its own two-voice cookbook). A wrong rate changes the voice's pitch and speed and the owner would
judge a distorted voice. The decoded duration must fit the text: CHARS at the measured 14-16 characters per second (round 2's plain takes ran 15.2-16.0, round 1 14.4+).
RED (exit 1) when the decoded duration is outside 0.8x .. 1.25x of the 14-16 c/s window (about 17-30 s for the 344-character sample): a doubled rate reads ~0.5x, a halved rate ~2x."""
import os
import sys

LOW_CPS, HIGH_CPS = 14.0, 16.0


def duration(nbytes, rate):
    return nbytes / (2 * rate)


def window(chars):
    return 0.8 * chars / HIGH_CPS, 1.25 * chars / LOW_CPS


def check(nbytes, chars, rate=24000, echo=True):
    d = duration(nbytes, rate)
    lo, hi = window(chars)
    ok = lo <= d <= hi
    if echo:
        print(f"pcm_bytes={nbytes} rate={rate} duration={d:.2f}s window={lo:.1f}..{hi:.1f}s chars={chars} verdict={'GREEN' if ok else 'RED'}")
    return 0 if ok else 1


def best_rate(nbytes, chars, rates=(24000, 16000, 22050, 44100, 48000)):
    """Of `rates`, the one whose decoded duration fits and sits nearest chars/15 s, for a re-encode with NO new request; None if none does."""
    fits = [r for r in rates if check(nbytes, chars, r, echo=False) == 0]
    return min(fits, key=lambda r: abs(duration(nbytes, r) - chars / 15.0)) if fits else None    # the one nearest the 15 characters per second centre


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) != 2:
        sys.exit(__doc__)
    rate = int(next((x.split("=")[1] for x in sys.argv[1:] if x.startswith("--rate=")), 24000))
    sys.exit(check(os.path.getsize(a[0]), int(a[1]), rate))
