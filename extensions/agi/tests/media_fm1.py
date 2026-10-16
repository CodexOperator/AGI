#!/usr/bin/env python3
"""media_fm1.py OUTLINE.md [REPO] [--chapters=N]: Fm1 + Fm1b of goal:g5.4.2 (the season media set) on an explainer outline or script node.

Fm1   every `@@excerpt SHA:PATH:Lx-Ly` is followed by a ~~~~ fenced block that BYTE-EQUALS `git show SHA:PATH | sed -n x,yp`
      (mismatches), and every `fn:` token resolves at the SHA of its chapter (unresolved):
        fn: piece:NAME          a `### NAME ` heading in a .agi/nodes/.geometry/engine*.md at the SHA
        fn: def:PATH:NAME       a `def NAME` / `class NAME` line in PATH at the SHA
        fn: cell:PATH:KEY       the text KEY in PATH at the SHA
Fm1b  every `live: NAME <- piece:CALLER | file:PATH` finds NAME as a word in the caller at the SHA (unresolved_live); a step the
      outline names with `uncalled: NAME` must have NO caller outside its own definition and the tests (checked: `uncalled_wrong`).
The SHA of a chapter is the `sha:` line above it (the outline's header carries one). Prints one `key=count` line per class, then
`mismatches=N unresolved=N` and exits with their sum (0 = green). Read-only: it runs `git show`, `git grep`, nothing else.
"""
import re
import subprocess
import sys

ENGINE = ".agi/nodes/.geometry/"
# where a CALLER of an engine step can live: code, hooks, units, cells and skills (not tests, not node prose)
CALLER_PATHS = ["extensions/agi/bin", "extensions/agi/src", "extensions/agi/lib", "extensions/agi/hooks", "extensions/agi/guard",
                "extensions/agi/boxkit", "extensions/agi/templates", "extensions/agi/scripts", "extensions/agi/workflows",
                "extensions/agi/driver.sh", "skills", ".agi/nodes/.geometry", ".agi/config.json"]


def git(repo, *a):
    r = subprocess.run(["git", "-C", repo, *a], capture_output=True)
    return r.returncode, r.stdout


def show(repo, sha, path):
    rc, out = git(repo, "show", f"{sha}:{path}")
    return out if rc == 0 else None


def engine_files(repo, sha):
    rc, out = git(repo, "ls-tree", "--name-only", sha, ENGINE)
    return [p for p in out.decode().split() if re.search(r"/engine[^/]*\.md$", p)] if rc == 0 else []


def piece_body(repo, sha, name):
    """The fenced body of `### name ` in any engine*.md at sha, or None."""
    for p in engine_files(repo, sha):
        txt = (show(repo, sha, p) or b"").decode("utf-8", "surrogateescape").split("\n")
        for i, ln in enumerate(txt):
            if re.match(r"^###* " + re.escape(name) + r" ", ln):
                body, inside = [], False
                for ln2 in txt[i + 1:]:
                    if ln2.startswith("~~~"):
                        if inside:
                            return "\n".join(body)
                        inside = True
                    elif inside:
                        body.append(ln2)
                    elif ln2.startswith("##"):
                        break
    return None


def check(outline, repo, expect_chapters=None):
    text = open(outline, encoding="utf-8").read().split("\n")
    sha = None
    miss, unres, ulive, uwrong, n_ex, n_fn, n_live = [], [], [], [], 0, 0, 0
    nosha, chap, chap_open, n_chap = [], None, False, 0   # a token with no sha above it; a `## C` chapter and whether it has an fn:
    i = 0
    while i < len(text):
        ln = text[i]
        m = re.match(r"^## (C\d+)\b", ln)
        if m:
            if chap and not chap_open:
                nosha.append(f"chapter {chap} has no fn: token")
            chap, chap_open, n_chap = m.group(1), False, n_chap + 1
        elif re.match(r"^## ", ln):
            if chap and not chap_open:
                nosha.append(f"chapter {chap} has no fn: token")
            chap = None
        if re.match(r"^fn: *(piece|def|cell):", ln):
            chap_open = True
        if re.match(r"^(fn|live|uncalled): ", ln) and not sha:
            nosha.append(f"{ln.strip()}: no `sha:` line above it (outline line {i + 1})")
        m = re.match(r"^sha: *([0-9a-f]{7,40})\s*$", ln)
        if m:
            sha = m.group(1)
        m = re.match(r"^@@excerpt ([0-9a-f]{7,40}):(.+):L(\d+)-L(\d+)\s*$", ln)
        if m:
            n_ex += 1
            s, path, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
            j = i + 1
            if j < len(text) and text[j].startswith("~~~~"):
                body = []
                j += 1
                while j < len(text) and not text[j].startswith("~~~~"):
                    body.append(text[j])
                    j += 1
                have = "\n".join(body)
                raw = show(repo, s, path)
                flines = [] if raw is None else raw.decode("utf-8", "surrogateescape").split("\n")
                if flines and flines[-1] == "":
                    flines.pop()   # the empty piece after the final newline is not a line
                want = None if raw is None or a < 1 or b < a or b > len(flines) else "\n".join(flines[a - 1:b])   # a range past EOF is cut short by the slice: that is a mismatch
                if want is None or have != want:
                    miss.append(f"{s}:{path}:L{a}-L{b} (outline line {i + 1})")
                i = j
            else:
                miss.append(f"{s}:{path}:L{a}-L{b}: no ~~~~ block follows (outline line {i + 1})")
        m = re.match(r"^fn: *(piece|def|cell):(.+?)\s*$", ln)
        if m and sha:
            n_fn += 1
            kind, arg = m.group(1), m.group(2)
            ok = False
            if kind == "piece":
                ok = piece_body(repo, sha, arg) is not None
            elif kind == "def":
                path, _, name = arg.rpartition(":")
                body = (show(repo, sha, path) or b"").decode("utf-8", "surrogateescape")
                ok = re.search(r"^\s*(def|class) " + re.escape(name) + r"\b", body, re.M) is not None
            else:
                path, _, key = arg.rpartition(":")
                ok = key in (show(repo, sha, path) or b"").decode("utf-8", "surrogateescape")
            if not ok:
                unres.append(f"{ln.strip()} @ {sha} (outline line {i + 1})")
        m = re.match(r"^live: *(\S+) *<- *(piece|file):(\S+)\s*$", ln)
        if m and sha:
            n_live += 1
            name, kind, arg = m.groups()
            if kind == "piece":
                body = piece_body(repo, sha, arg)
            else:
                raw = show(repo, sha, arg)
                body = None if raw is None else raw.decode("utf-8", "surrogateescape")
            if body is None or not re.search(r"(?<![\w.-])" + re.escape(name) + r"(?![\w-])", body):
                ulive.append(f"{ln.strip()} @ {sha} (outline line {i + 1})")
        m = re.match(r"^uncalled: *(\S+)", ln)
        if m and sha:
            name = m.group(1)
            rc, out = git(repo, "grep", "-nIE", "--", r"(^|[^A-Za-z0-9_-])" + re.escape(name) + r"([^A-Za-z0-9_-]|$)", sha, "--", *CALLER_PATHS)
            # a caller is any hit outside the definition's own piece heading/comment and the engine map line
            hits = [h for h in out.decode().split("\n") if h and not re.search(r"engine[^:]*\.md:\d+:(###|#|" + re.escape(name) + r" )", h)
                    and not re.search(r"engine\.md:\d+:" + re.escape(name), h) and not re.search(r"THOUGHT|\bOWNER\b|^\S+:\.agi/nodes/\.geometry/engine-\w+\.md:\d+:g\d", h)]
            if hits:
                uwrong.append(f"uncalled: {name} has {len(hits)} caller line(s), first {hits[0][:140]}")
        i += 1
    if chap and not chap_open:
        nosha.append(f"chapter {chap} has no fn: token")
    # a green on text it never checked is a failure: nothing to check, or a token that could not be checked
    if n_chap == 0:
        nosha.append("no `## C<n>` chapter heading: nothing was checked")
    if expect_chapters is not None and n_chap != expect_chapters:
        nosha.append(f"chapters={n_chap}, the outline has {expect_chapters}")
    if n_ex == 0:
        nosha.append("no @@excerpt in the file: nothing was checked")
    if n_fn == 0:
        nosha.append("no fn: token resolved: nothing was checked")
    print(f"excerpts={n_ex} fn={n_fn} live={n_live} chapters={n_chap}")
    print(f"mismatches={len(miss)}")
    for x in miss:
        print("  MISMATCH", x)
    print(f"unresolved={len(unres) + len(ulive) + len(uwrong) + len(nosha)}")
    for x in unres + ulive + uwrong + nosha:
        print("  UNRESOLVED", x)
    return len(miss) + len(unres) + len(ulive) + len(uwrong) + len(nosha)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    args = [a for a in sys.argv[1:] if not a.startswith("--chapters=")]
    want = next((int(a.split("=")[1]) for a in sys.argv[1:] if a.startswith("--chapters=")), None)
    sys.exit(min(check(args[0], args[1] if len(args) > 1 else ".", want), 99))
