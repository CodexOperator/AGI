#!/usr/bin/env python3
"""media_fidelity.py REF.txt HYP.txt [--wer=0.10] [--run=3]: the fidelity check of goal:g5.4.2's voice run (council 06:49Z 10-16).

REF is the text SENT for one chunk (tags stripped, slots spoken: media_fm2.render), HYP the transcript of the audio that came back. Both are
normalised (lower case, punctuation gone, a bare integer spelled as its words, `[...]` tags removed from REF only: a tag the voice READ ALOUD
shows up in HYP as words REF does not have). A chunk is RED when
  wer      the word error rate (substitutions + deletions + insertions over the REF words) is above --wer;
  dropped  a run of --run or more consecutive REF words has no counterpart in HYP (a deleted sentence, a truncated tail);
  added    a run of --run or more consecutive HYP words has no counterpart in REF (a spoken tag, a repeated line).
Prints `ref_words=N hyp_words=N wer=0.xxx dropped=N added=N` and one line per run; exit = 0 green, 1 RED. The transcript is made elsewhere
(a local STT under agi.slice 4600 MiB, else a priced STT counted in the $25); this file only compares.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import media_fm2  # noqa: E402


def words(text, drop_tags):
    if drop_tags:
        text = re.sub(r"\[[^\]]*\]", " ", text)
    text = text.lower().replace("-", " ")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    out = []
    for w in text.split():
        w = w.strip("'")
        if w.isdigit() and int(w) < 1000000:
            out.extend(media_fm2.spoken(int(w)).split())
        elif w:
            out.append(w)
    return out


def align(ref, hyp):
    """Levenshtein alignment. Returns (errors, [("del"|"ins"|"sub", ref_index_or_None, hyp_index_or_None)])."""
    n, m = len(ref), len(hyp)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]))
    ops, i, j = [], n, m
    while i or j:
        if i and j and d[i][j] == d[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]):
            if ref[i - 1] != hyp[j - 1]:
                ops.append(("sub", i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i and d[i][j] == d[i - 1][j] + 1:
            ops.append(("del", i - 1, None))
            i -= 1
        else:
            ops.append(("ins", None, j - 1))
            j -= 1
    return d[n][m], ops[::-1]


def runs(idx):
    out, cur = [], []
    for x in idx:
        if cur and x != cur[-1] + 1:
            out.append(cur)
            cur = []
        cur.append(x)
    return out + ([cur] if cur else [])


def check(ref_text, hyp_text, wer_max=0.10, run_max=3, echo=True):
    ref, hyp = words(ref_text, True), words(hyp_text, False)
    if not ref:
        print("nothing to compare: the reference text has no words")
        return 1
    errs, ops = align(ref, hyp)
    wer = errs / len(ref)
    dropped = [r for r in runs([i for k, i, _ in ops if k == "del"]) if len(r) >= run_max]
    added = [r for r in runs([j for k, _, j in ops if k == "ins"]) if len(r) >= run_max]
    if echo:
        print(f"ref_words={len(ref)} hyp_words={len(hyp)} wer={wer:.3f} dropped={len(dropped)} added={len(added)}")
        for r in dropped:
            print("  DROPPED", " ".join(ref[r[0]:r[-1] + 1]))
        for r in added:
            print("  ADDED", " ".join(hyp[r[0]:r[-1] + 1]))
    return 1 if (wer > wer_max or dropped or added) else 0


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) != 2:
        sys.exit(__doc__)
    opt = {x.split("=")[0]: x.split("=")[1] for x in sys.argv[1:] if x.startswith("--") and "=" in x}
    sys.exit(check(open(a[0], encoding="utf-8").read(), open(a[1], encoding="utf-8").read(),
                   float(opt.get("--wer", 0.10)), int(opt.get("--run", 3))))
