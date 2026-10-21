#!/usr/bin/env python3
"""goal:g5.4.2 M5 (council 11:57Z amendment 3): the C15 re-check, 0 spend, no render. The transcriber writes a spoken '47 percent' as '47%'; media_fidelity strips '%', so the protected word
'percent' had no match and a sound take was flagged RED. The RULE (generic on the hypothesis, never the reference's words written into it): '<digits>%' -> '<digits> percent'
(the checker already spells digits). Applied to a stored transcript; media_fidelity.py itself is NOT edited (that rides with the next walk run).
  media_recheck.py REF.txt TRANSCRIPT.txt     e.g. the chunk's text and walk/C15/c0-a2.txt: prints the verdict, exit 0 GREEN / 1 RED"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import media_fidelity  # noqa: E402


def percent_rule(hyp):
    return re.sub(r"(\d[\d,]*(?:\.\d+)?)\s*%", r"\1 percent", hyp)


def recheck(ref, hyp, echo=True):
    red, errs, runs = media_fidelity.score(ref, percent_rule(hyp))
    if echo:
        print(f"{'RED' if red else 'GREEN'} ({errs} error ops)" + "".join(f"\n  {r}" for r in runs))
    return red, errs, runs


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(recheck(open(sys.argv[1], encoding="utf-8").read(), open(sys.argv[2], encoding="utf-8").read())[0])
