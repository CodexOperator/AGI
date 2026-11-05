#!/usr/bin/env python3
"""media_fm2.py SCRIPT.md [REPO]: Fm2 + the claim/cite pairs of goal:g5.4.2's explainer script (M2).

pair lines (the council reads every pair):   pair Cn.k: CLAIM TEXT => SHA:PATH:Lx-Ly ~ NEEDLE      (Cn.k = the pair's id, k from 1 in the chapter)
  the range must exist at SHA and CONTAIN the NEEDLE (a fixed string): the cite implements the claim, it is not merely a range (pairs_bad).
TAGS  every sentence of a `### narration` or `### html` section ends with a tag: `[Cn.k]` / `[Cn.k,Cn.j]` (it states what the engine does or is, and
      the pair(s) named, IN THE SAME CHAPTER, carry the proof) or `[image]` (a greeting, a picture, a transition: it claims nothing about
      the engine; the council reads these). An untagged sentence, a segment that holds more than one sentence before its tag, or a tag that
      names a pair that does not exist is a finding (untagged / bad_tags). Tags are stripped before the numbers are scanned and before the voice.
Fm2   inside a `### narration` or `### html` section, with {{slots}}, `pair:` lines, `fn:`/`live:`/`uncalled:`/`sha:` lines,
      @@excerpt blocks and ~~~~ fences removed, the prose carries NO digit and NO number word (zero..twenty, thirty..ninety, hundred,
      thousand, million, billion); a number reaches the narrator only through a slot (bare_numbers).
      slots:  {{bytes:PIECE}}  the byte length of a piece's fenced body at the chapter's sha
              {{lines:PIECE}}  its line count
              {{val:SHA:PATH:Lx:REGEX}}  group 1 of REGEX on line x of PATH at SHA (unresolved slot if it does not match)
              {{spell:WORD}} is NOT a slot; spelled-out letters ("A G I") are plain words and fine.
Prints `pairs=N slots=N images=N words_narration=N words_html=N`, `pairs_bad`, `untagged`, `bad_tags`, `bare_numbers`, `bad_slots`; exit = their sum.
`render(text, repo, sha)` returns the text with every slot replaced by its SPOKEN form (a number in words), for the voice run.
"""
import re
import subprocess
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import media_fm1  # noqa: E402

NUMWORDS = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen "
               "nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion".split())
TAG = re.compile(r"\[(image|C\d+\.\d+(?:,C\d+\.\d+)*)\]")
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"(])")


def split_sentences(text):
    return [x for x in SENT.split(text.strip()) if x.strip()]


def strip_tags(text):
    return re.sub(r"\s*" + TAG.pattern, "", text)


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
    text = strip_tags(text)
    def one(m):
        v = slot_value(m.group(1), m.group(2), repo, sha)
        if v is None:
            raise ValueError("unresolved slot " + m.group(0))
        return spoken(v)
    return SLOT.sub(one, text)


def check(path, repo):
    text = open(path, encoding="utf-8").read().split("\n")
    sha, section, chap = None, None, None
    ids, chap_ids = {}, {}
    pairs, bad_pairs, bare, bad_slots, untagged, bad_tags = 0, [], [], [], [], []
    n_slots, n_img, w = 0, 0, {"narration": 0, "html": 0}
    in_fence = False
    block = []          # the current paragraph of a narration/html section: [(line_no, text)]

    def flush():
        nonlocal n_img
        if not block or section is None:
            block.clear()
            return
        joined = " ".join(t for _, t in block)
        first = block[0][0]
        parts = TAG.split(joined)       # text, tag-body, text, tag-body, ... , tail
        for k in range(0, len(parts), 2):
            seg = parts[k].strip()
            tag = parts[k + 1] if k + 1 < len(parts) else None
            if not seg:
                continue
            sents = split_sentences(seg)
            if tag is None:
                untagged.append(f"line {first}: {seg[:70]!r}")
                continue
            if len(sents) > 1:
                for x in sents[:-1]:
                    untagged.append(f"line {first}: {x[:70]!r} (no tag of its own)")
            if tag == "image":
                n_img += 1
            else:
                for pid in tag.split(","):
                    if pid not in chap_ids.get(chap, set()):
                        bad_tags.append(f"line {first}: [{pid}] names no pair of this chapter")
        prose = SLOT.sub(" ", TAG.sub(" ", joined))
        w[section] += len(re.findall(r"[A-Za-z][A-Za-z'-]*", prose))
        hit = re.findall(r"\d+", prose) + [t for t in re.findall(r"[a-z]+", prose.lower()) if t in NUMWORDS]
        if hit:
            bare.append(f"line {first}: bare number {' '.join(hit)!r}")
        for sm in SLOT.finditer(joined):
            nonlocal_slots.append(1)
            if slot_value(sm.group(1), sm.group(2), repo, sha) is None:
                bad_slots.append(f"line {first}: {sm.group(0)} @ {sha}")
        block.clear()

    nonlocal_slots = []
    # pass 1: the pair ids of every chapter (a tag may cite any pair of its own chapter)
    for ln in text:
        m = re.match(r"^## (C\d+)\b", ln)
        if m:
            chap = m.group(1)
        m = re.match(r"^pair (C\d+\.\d+): ", ln)
        if m:
            chap_ids.setdefault(chap, set()).add(m.group(1))
    chap = None
    for i, ln in enumerate(text):
        m = re.match(r"^## (C\d+)\b", ln)
        if m:
            flush()
            chap, section = m.group(1), None
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
            flush()
            section = m.group(1)
            continue
        if re.match(r"^##+ ", ln):
            flush()
            section = None
        m = re.match(r"^pair (C\d+\.\d+): (.+?) => ([0-9a-f]{7,40}):(.+?):L(\d+)-L(\d+) ~ (.+)$", ln)
        if m:
            pairs += 1
            pid, claim, s_, p_, a_, b_, needle = m.groups()
            raw = media_fm1.show(repo, s_, p_)
            fl = [] if raw is None else raw.decode("utf-8", "surrogateescape").split("\n")
            if fl and fl[-1] == "":
                fl.pop()
            rng = "" if raw is None or int(b_) > len(fl) or int(a_) < 1 else "\n".join(fl[int(a_) - 1:int(b_)])
            if not rng or needle not in rng or not claim.strip():
                bad_pairs.append(f"{pid} line {i + 1}: {needle!r} not in {s_}:{p_}:L{a_}-L{b_}")
            continue
        if re.match(r"^pair: ", ln):
            bad_pairs.append(f"line {i + 1}: a pair without an id (pair Cn.k:)")
            continue
        if section is None or re.match(r"^(@@excerpt|fn:|live:|uncalled:|sha:)", ln):
            if not ln.strip():
                pass
            continue
        if not ln.strip():
            flush()
        else:
            block.append((i + 1, ln.strip()))
    flush()
    print(f"pairs={pairs} slots={len(nonlocal_slots)} images={n_img} words_narration={w['narration']} words_html={w['html']}")
    print(f"pairs_bad={len(bad_pairs)}")
    for x in bad_pairs:
        print("  PAIR", x)
    print(f"untagged={len(untagged)}")
    for x in untagged[:30]:
        print("  UNTAGGED", x)
    print(f"bad_tags={len(bad_tags)}")
    for x in bad_tags[:30]:
        print("  TAG", x)
    print(f"bare_numbers={len(bare)}")
    for x in bare[:30]:
        print("  BARE", x)
    print(f"bad_slots={len(bad_slots)}")
    for x in bad_slots:
        print("  SLOT", x)
    return len(bad_pairs) + len(untagged) + len(bad_tags) + len(bare) + len(bad_slots) + (1 if pairs == 0 else 0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(min(check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "."), 99))
