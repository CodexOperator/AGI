#!/usr/bin/env python3
"""media_fidelity.py REF.txt HYP.txt [--wer=0.10] [--run=3] [--bridge=1]: the fidelity check of goal:g5.4.2's voice run (council 06:49Z, 06:53Z 10-16).

REF is the text SENT for one chunk (tags stripped, slots spoken: media_fm2.render), HYP the transcript of the audio that came back. Both are
normalised (lower case, punctuation gone, a bare integer spelled as its words); `[...]` tags are removed from REF only (a tag the voice READ ALOUD
shows up in HYP as words REF does not have); the bracketed AUDIO EVENTS a transcriber writes are removed from HYP and listed (`stripped=`).
The two word lists are aligned (Levenshtein, tie-break: the cheapest path that keeps errors together). A chunk is RED when
  wer         substitutions + deletions + insertions over the REF words is above --wer;
  protected   ANY error op on a negation or a number word (PROTECTED: not no never nothing none nor cannot without, zero..ninety, hundred thousand
              million, dollar(s) cent(s) percent; curly apostrophes become ASCII and n't contractions are spelled out first, can't -> cannot): one dropped "never" inverts a
              claim, "fourteen" -> "forty" changes a fact, and an isolated error is green by design, so these are RED regardless of N or WER;
  error_run   a run of >= --run ERROR ops (substitution, deletion, insertion, mixed) in alignment order with no exact match between them,
              except that a run is bridged over up to --bridge single matched words (a common word that happens to match inside a deleted or
              reworded span does not split it). It covers a deleted sentence, a paraphrase, a spoken tag, a repeated line and a truncated tail.
Number forms are spelled by spell_numbers() (1,000 / $0.10 / 23rd) and `can not` is `cannot`. Jargon goes through NORMALISE (a recorded list: spelling in either text -> one form), never a looser threshold.
Memory guard: align() is a full O(n*m) table; len(ref)*len(hyp) > MAX_CELLS is refused (exit 2), never run.
Prints `ref_words=N hyp_words=N wer=0.xxx longest_run=N error_runs=N stripped=[...]` and one line per run; exit 0 green, 1 RED, 2 refused.
The transcript is made elsewhere (a local STT under agi.slice 4600 MiB, else a priced STT counted in the $25); this file only compares.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import media_fm2  # noqa: E402

MAX_CELLS = 4_000_000
NUMBERS = set(media_fm2.ONES) | {w for w in media_fm2.TENS if w != "_"} | {"hundred", "thousand", "million"}
UNITS = {"dollar", "dollars", "cent", "cents", "percent"}     # a swapped unit changes a fact ("ten cents" -> "ten dollars"), like a swapped number
PROTECTED = {"not", "no", "never", "nothing", "none", "nor", "cannot", "without"} | NUMBERS | UNITS    # a swapped number word ("fourteen" -> "forty") changes a fact
# recorded normalisation: a regex over the joined, normalised words -> the one form both texts get
NORMALISE = [(r"\ba g i\b", "agi"),
             (r"\bwork tree\b", "worktree")]      # key S, schedar-c2a (07:51Z): scribe-v2 writes the one word `worktree` as two; the SAME words


def validate_normalise(entries):
    """A NORMALISE entry maps a spelling to a spelling of the SAME words (council 07:04Z (ii)): an empty replacement would delete heard words from the
    comparison, so it is refused. Raises ValueError."""
    for rx, to in entries:
        if not isinstance(to, str) or not to.strip():
            raise ValueError(f"NORMALISE entry {rx!r} maps to an empty string: refused")
        re.compile(rx)
    return entries


validate_normalise(NORMALISE)
EVENT = re.compile(r"\[[^\]]*\]|\((?:[A-Za-z ]{1,30})\)")


def strip_events(text):
    """(text without a transcriber's bracketed audio events, [the stripped strings]); the strings are recorded, never silent."""
    found = EVENT.findall(text)
    return EVENT.sub(" ", text), found


ORD_IRREG = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth", "nine": "ninth", "twelve": "twelfth"}


def ordinal_words(n):
    """23 -> 'twenty third': the spoken cardinal with its last word made ordinal."""
    ws = media_fm2.spoken(n).split()
    last = ws[-1]
    ws[-1] = ORD_IRREG.get(last, last[:-1] + "ieth" if last.endswith("y") else last + "th")
    return " ".join(ws)


def spell_numbers(text):
    """The recorded number forms (council 07:01Z): '1,000' joins its digit groups; '$0.10' / '0.10' -> 'zero point one zero (dollars)', the digits
    after the point one by one; '23rd' -> 'twenty third'. Done before punctuation is dropped, so a correctly spoken line is never RED for its form."""
    text = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", text)
    text = re.sub(r"(?<=[A-Za-z])\.(?=[A-Za-z])", " dot ", text)     # `bin.new` is `bin dot new` (key S, schedar-c2a: scribe-v2 wrote the file name as it is written)
    text = re.sub(r"\$\s*(\d+(?:\.\d+)?)", r"\1 dollars", text)
    text = re.sub(r"(\d+)\.(\d+)", lambda m: m.group(1) + " point " + " ".join(m.group(2)), text)
    return re.sub(r"\b(\d+)(?:st|nd|rd|th)\b", lambda m: ordinal_words(int(m.group(1))) if int(m.group(1)) < 1000000 else m.group(0), text)


def words(text, drop_tags):
    if drop_tags:
        text = re.sub(r"\[[^\]]*\]", " ", text)
    text = spell_numbers(text)
    text = text.replace("\u2019", "'").replace("\u2018", "'").lower().replace("-", " ").replace("can't", "cannot").replace("won't", "will not").replace("n't", " not")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    out = []
    for w in text.split():
        w = w.strip("'")
        if w.isdigit() and int(w) < 1000000:
            out.extend(media_fm2.spoken(int(w)).split())
        elif w:
            out.append(w)
    joined = re.sub(r"\bcan not\b", "cannot", " ".join(out))
    for rx, to in NORMALISE:
        joined = re.sub(rx, to, joined)
    return joined.split()


def align(ref, hyp):
    """Levenshtein alignment over the full table. Returns (errors, [(kind, ref_i, hyp_j)]) with kind in match|sub|del|ins."""
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
        if i and j and ref[i - 1] == hyp[j - 1] and d[i][j] == d[i - 1][j - 1]:
            ops.append(("match", i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i and d[i][j] == d[i - 1][j] + 1:
            ops.append(("del", i - 1, None))
            i -= 1
        elif j and d[i][j] == d[i][j - 1] + 1:
            ops.append(("ins", None, j - 1))
            j -= 1
        else:
            ops.append(("sub", i - 1, j - 1))
            i, j = i - 1, j - 1
    return d[n][m], ops[::-1]


def error_runs(ops, bridge):
    """[[error ops]] — maximal runs of error ops, bridged over <= `bridge` consecutive matches between two errors."""
    out, cur, gap = [], [], 0
    for op in ops:
        if op[0] == "match":
            if cur:
                gap += 1
                if gap > bridge:
                    out.append(cur)
                    cur, gap = [], 0
        else:
            cur.append(op)
            gap = 0
    if cur:
        out.append(cur)
    return out


def check(ref_text, hyp_text, wer_max=0.10, run_max=3, bridge=1, echo=True, strip=True):
    stripped = []
    if strip:
        hyp_text, stripped = strip_events(hyp_text)
    ref, hyp = words(ref_text, True), words(hyp_text, False)
    if not ref:
        print("nothing to compare: the reference text has no words")
        return 1
    if len(ref) * len(hyp) > MAX_CELLS:
        print(f"REFUSED: {len(ref)} x {len(hyp)} = {len(ref) * len(hyp)} cells > {MAX_CELLS}; compare one chunk at a time")
        return 2
    errs, ops = align(ref, hyp)
    wer = errs / len(ref)
    runs = error_runs(ops, bridge)
    longest = max((len(r) for r in runs), default=0)
    red_runs = [r for r in runs if len(r) >= run_max]
    prot = [o for o in ops if o[0] != "match" and ((o[1] is not None and ref[o[1]] in PROTECTED) or (o[2] is not None and hyp[o[2]] in PROTECTED))]
    if echo:
        print(f"ref_words={len(ref)} hyp_words={len(hyp)} wer={wer:.3f} longest_run={longest} error_runs={len(red_runs)} protected={len(prot)} stripped={stripped}")
        for r in red_runs:
            rw = " ".join(ref[o[1]] for o in r if o[1] is not None)
            hw = " ".join(hyp[o[2]] for o in r if o[2] is not None)
            print(f"  ERROR_RUN {len(r)} ops: sent [{rw}] heard [{hw}]")
        for o in prot:
            print(f"  PROTECTED sent [{ref[o[1]] if o[1] is not None else ''}] heard [{hyp[o[2]] if o[2] is not None else ''}] ({o[0]})")
    return 1 if (wer > wer_max or red_runs or prot) else 0


def score(ref_text, hyp_text, wer_max=0.10, run_max=3, bridge=1):
    """The walk's W3 (council 10-16 08:08Z): the same verdict as check() plus how bad it is, so two RED takes can be ranked.
    -> (red 0/1, error ops, ["sent [..] heard [..]" per red run and protected op]); a refused/empty compare is (1, 10**9, [why])."""
    hyp_text, _ = strip_events(hyp_text)
    ref, hyp = words(ref_text, True), words(hyp_text, False)
    if not ref or len(ref) * len(hyp) > MAX_CELLS:
        return 1, 10 ** 9, ["no comparison possible"]
    errs, ops = align(ref, hyp)
    red_runs = [r for r in error_runs(ops, bridge) if len(r) >= run_max]
    prot = [o for o in ops if o[0] != "match" and ((o[1] is not None and ref[o[1]] in PROTECTED) or (o[2] is not None and hyp[o[2]] in PROTECTED))]
    lines = [f"sent [{' '.join(ref[o[1]] for o in r if o[1] is not None)}] heard [{' '.join(hyp[o[2]] for o in r if o[2] is not None)}]" for r in red_runs]
    lines += [f"protected sent [{ref[o[1]] if o[1] is not None else ''}] heard [{hyp[o[2]] if o[2] is not None else ''}]" for o in prot]
    return (1 if (errs / len(ref) > wer_max or red_runs or prot) else 0), errs, lines


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) != 2:
        sys.exit(__doc__)
    opt = {x.split("=")[0]: x.split("=")[1] for x in sys.argv[1:] if x.startswith("--") and "=" in x}
    sys.exit(check(open(a[0], encoding="utf-8").read(), open(a[1], encoding="utf-8").read(),
                   float(opt.get("--wer", 0.10)), int(opt.get("--run", 3)), int(opt.get("--bridge", 1))))
