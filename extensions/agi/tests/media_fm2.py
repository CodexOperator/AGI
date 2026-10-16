#!/usr/bin/env python3
"""media_fm2.py SCRIPT.md [REPO]: Fm2 + the claim/cite pairs of goal:g5.4.2's explainer script (M2).

pair lines (the council reads every pair):   pair: CLAIM TEXT => SHA:PATH:Lx-Ly ~ NEEDLE
  the range must exist at SHA and CONTAIN the NEEDLE (a fixed string): the cite implements the claim, it is not merely a range (pairs_bad).
Fm2   inside a `### narration` or `### html` section, with {{slots}}, `pair:` lines, `fn:`/`live:`/`uncalled:`/`sha:` lines,
      @@excerpt blocks and ~~~~ fences removed, the prose carries NO digit and NO number word (zero..twenty, thirty..ninety, hundred,
      thousand, million, billion); a number reaches the narrator only through a slot (bare_numbers).
      slots:  {{bytes:PIECE}}  the byte length of a piece's fenced body at the chapter's sha
              {{lines:PIECE}}  its line count
              {{val:SHA:PATH:Lx:REGEX}}  group 1 of REGEX on line x of PATH at SHA (unresolved slot if it does not match)
              {{spell:WORD}} is NOT a slot; spelled-out letters ("A G I") are plain words and fine.
Prints `pairs=N slots=N words_narration=N words_html=N`, `pairs_bad=N`, `bare_numbers=N`, `bad_slots=N`; exit = their sum.
`render(text, repo, sha)` returns the text with every slot replaced by its SPOKEN form (a number in words), for the voice run.
"""
import re
import subprocess
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import media_fm1  # noqa: E402

NUMWORDS = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen "
               "nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion".split())
SLOT = re.compile(r"\{\{(bytes|lines|val):([^}]*)\}\}")
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def spoken(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000:
        return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + spoken(n % 100))
    if n < 1000000:
        return spoken(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + spoken(n % 1000))
    return str(n)


def slot_value(kind, arg, repo, sha):
    if kind in ("bytes", "lines"):
        body = media_fm1.piece_body(repo, sha, arg)
        if body is None:
            return None
        return len(body.encode("utf-8", "surrogateescape")) if kind == "bytes" else body.count("\n") + 1
    m = re.match(r"^([0-9a-f]{7,40}):(.+):L(\d+):(.+)$", arg)
    if not m:
        return None
    s, path, ln, rx = m.groups()
    raw = media_fm1.show(repo, s, path)
    lines = [] if raw is None else raw.decode("utf-8", "surrogateescape").split("\n")
    if int(ln) > len(lines):
        return None
    g = re.search(rx, lines[int(ln) - 1])
    return int(g.group(1)) if g and g.group(1).isdigit() else None


def render(text, repo, sha):
    def one(m):
        v = slot_value(m.group(1), m.group(2), repo, sha)
        if v is None:
            raise ValueError("unresolved slot " + m.group(0))
        return spoken(v)
    return SLOT.sub(one, text)


def check(path, repo):
    text = open(path, encoding="utf-8").read().split("\n")
    sha, section = None, None
    pairs, bad_pairs, bare, bad_slots = 0, [], [], []
    n_slots, w = 0, {"narration": 0, "html": 0}
    in_fence = False
    for i, ln in enumerate(text):
        m = re.match(r"^sha: *([0-9a-f]{7,40})\s*$", ln)
        if m:
            sha = m.group(1)
        if re.match(r"^~~~~", ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^### (narration|html)\b", ln)
        if m:
            section = m.group(1)
            continue
        if re.match(r"^##+ ", ln) and not re.match(r"^### (narration|html)\b", ln):
            section = None
        m = re.match(r"^pair: (.+?) => ([0-9a-f]{7,40}):(.+?):L(\d+)-L(\d+) ~ (.+)$", ln)
        if m:
            pairs += 1
            claim, s, p, a, b, needle = m.groups()
            raw = media_fm1.show(repo, s, p)
            rng = "" if raw is None else "\n".join(raw.decode("utf-8", "surrogateescape").split("\n")[int(a) - 1:int(b)])
            if not rng or needle not in rng or not claim.strip():
                bad_pairs.append(f"line {i + 1}: {needle!r} not in {s}:{p}:L{a}-L{b}")
            continue
        if section is None or re.match(r"^(@@excerpt|fn:|live:|uncalled:|sha:|pair:)", ln):
            continue
        for sm in SLOT.finditer(ln):
            n_slots += 1
            if slot_value(sm.group(1), sm.group(2), repo, sha) is None:
                bad_slots.append(f"line {i + 1}: {sm.group(0)} @ {sha}")
        prose = SLOT.sub(" ", ln)
        words = re.findall(r"[A-Za-z][A-Za-z'-]*", prose)
        w[section] += len(words)
        hit = re.findall(r"\d+", prose) + [t for t in re.findall(r"[a-z]+", prose.lower()) if t in NUMWORDS]
        if hit:   # one finding per line, however many number tokens it carries ("five thousand" is one typed count)
            bare.append(f"line {i + 1}: bare number {' '.join(hit)!r}")
    print(f"pairs={pairs} slots={n_slots} words_narration={w['narration']} words_html={w['html']}")
    print(f"pairs_bad={len(bad_pairs)}")
    for x in bad_pairs:
        print("  PAIR", x)
    print(f"bare_numbers={len(bare)}")
    for x in bare[:30]:
        print("  BARE", x)
    print(f"bad_slots={len(bad_slots)}")
    for x in bad_slots:
        print("  SLOT", x)
    return len(bad_pairs) + len(bare) + len(bad_slots) + (1 if pairs == 0 else 0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(min(check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "."), 99))
