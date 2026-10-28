#!/usr/bin/env python3
"""reader_census.py -- goal:g7.16.1.11.46.18 G1b-2 slice (b), falsifier 2 (rows 11 + 12): every reader that NAMES the trunk, classed.

    reader_census.py repo  [--rev REV] [--table PATH]
    reader_census.py homes [--rev REV] [--table PATH] [--root DIR] [--main-hooks FILE]

OPTION (3) (council 3/3, alive [decision] 10:07:47Z 10-28): posts/<P> keeps its name, so this census migrates nothing. It proves
every reader that names the trunk does so by a NAMED mechanism, and it fails a reader no row classes.

`repo` (U1 + I16 + A21 + C1 + B2): over extensions, skills and .agi/nodes/.geometry AT A COMMIT (git grep <rev>: never the working
tree, so an uncommitted file is not read), every line matching the LITERAL names (LITERAL) or a COMPOSED name (COMPOSED: posts/ or
season followed by a substitution) is a hit. Each hit takes the class of the FIRST table row whose path is the hit's file and whose
match is `*` or a substring of the line. Classes (CLASSES): posts (reads posts/<P>), alias (reads the alias season3/main or
season/s3), remote (a remote-tracking or pushed ref), prose (a comment, a doc, a message, test data), fixture (a scratch repo's own
ref), family (another branch family, e.g. season<n>/posts/<name>). Red, each by path, rc 1: a hit no row classes (`unclassed`); a
`fixture` row outside a test file that builds its repo on mktemp / tmp_path (`bad-fixture`, B2); a row that classes no hit
(`stale`). The floor: the files scanned and the files with a hit are printed; 0 files scanned = `unread`, rc 1.
MODULE (U-b3 + U-b3b + A-N5, council 3/3 11:1xZ): in a NON-TEST file (not under extensions/agi/tests/, not test_*) outside
bin/branches.py, every `branches.<fn>(` call and every `import branches` / `from branches import` line is a hit too, and a module hit
takes only a row whose match is a SUBSTRING (a `*` row never classes one): the row names the function, so its class says what that
function returns (alias: season_main, derive_names, merge_target, ref_candidates, town_main; remote: the mirror functions; family:
post_branch, loop_branch; grammar: parse, the predicates, a plain import). An ALIASED import (`from branches import f as _g`) is
classed by a row whose match names f: its later `_g(` calls are not grepped, so that row is the reading.
I-M1: that class is CHECKED against FN_CLASS (every public def of branches.py at the rev): a row whose class is not what the called
or imported function returns = `bad-module-class` ('prose' holds only on a line starting '#', '*' or a backtick); a public def FN_CLASS
does not name = `unmapped branches.<fn>`; A-N6 + A2: a call the line builds into a remote name (`origin/{...`, or a quoted
`origin/` + in either quote, each also as refs/remotes/origin/, right before it) owes `remote`; U1: `from <pkg> import branches` owes grammar
like `import branches`; a docstring opener (three quotes) is a prose start (A1). LIMIT: a remote name built on an EARLIER line (a variable
holding 'origin/') is not read; a call to a name branches.py does not define (a local dict) is left to its row.
LIMIT: a reader that names no ref at all (the main checkout's files, HEAD) is outside by construction; it follows posts/<P> by ff. A name DERIVED through
branches.py is caught at its call (MODULE) only: a call through a name bound by assignment (`f = branches.season_main`) or getattr, and
the `_g(` calls of an aliased import, are not grepped (the import row is their reading).

`homes` (A15 read-only + B1): the homes are a LISTING of --root (each entry with a bin/ is a home; its count is printed), plus the
main repo's own .git/hooks/reference-transaction (--main-hooks, DEFAULT <git common dir>/hooks/reference-transaction; unreadable =
`unread MAIN`, A-N2) and the table's `extra` globs. 0 homes listed or 0 files hashed = `unread homes`,
rc 1 (U-b1). Every file there that matches LITERAL
or COMPOSED is printed as `<home> <path> <sha256> <names it reads>`. A root entry that cannot be listed is `unread <home>` unless a
`home <name> not-in-the-boot-set` row names it; a file whose sha256 cannot be read is `unread <home> <path>`, never a pass.
Nothing is written anywhere.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import os
import re
import subprocess
import sys

SCOPE = ["extensions", "skills", ".agi/nodes/.geometry"]
LITERAL = r"posts/belam|refs/heads/posts/|season3/main|season/s3"
COMPOSED = r"(posts/|season)(\{|%[sd]|\$\{?[A-Za-z_])"
#: a COMPOSED name that IS the trunk: season<subst>/main or posts/<subst> not under another branch prefix (W1's guard on `family`)
TRUNK_COMPOSED = r"(^|[^/\w])(season(\{[^}]*\}|%[sd]|\$\{?\w+\}?)/main|posts/(\{|\$))"
#: MODULE (U-b3): a branches.py call or import -- the derived names have no literal to grep
MODULE = r"\bbranches\.[A-Za-z_][A-Za-z0-9_]*\(|^[[:space:]]*(import[[:space:]]+branches\b|from[[:space:]]+branches[[:space:]]+import\b|from[[:space:]]+[^[:space:]]+[[:space:]]+import[[:space:]].*\bbranches\b)"
CLASSES = ("posts", "alias", "remote", "prose", "fixture", "family", "grammar")
#: I-M1 (all-is-one 12:1xZ): the class of a module hit is CHECKED, not authored: every public def of branches.py -> what it returns
FN_CLASS = {"season_main": "alias", "town_main": "alias", "derive_names": "alias", "merge_target": "alias", "ref_candidates": "alias",
            "mirror_ref": "remote", "mirror_ref_for_branch": "remote", "mirror_and_prove": "remote",
            "post_branch": "family", "loop_branch": "family",
            "parse": "grammar", "is_legal_branch": "grammar", "is_remote_visible": "grammar", "assert_remote_visible": "grammar"}
TABLE = "extensions/agi/bin/reader_census.tsv"
NAMES = {"posts/<P>": r"posts/belam|refs/heads/posts/|posts/\$|posts/\{", "alias": r"season3/main|season/s3|season\{|season%",
         "composed": COMPOSED}


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True)


def read_table(rev: str, path: str) -> tuple[list[tuple], list[tuple], list[tuple], str | None]:
    """(hit rows, home rows, extra rows, problem), read from the table AT `rev` (the committed bytes, never the disk)."""
    r = git("show", f"{rev}:{path}")
    if r.returncode != 0:
        return [], [], [], f"the table {path} is not in {rev}"
    hits, homes, extras = [], [], []
    for n, line in enumerate(r.stdout.decode("utf-8", "replace").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        if f[0] == "hit" and len(f) == 5 and f[2] in CLASSES:
            hits.append((f[1], f[2], f[3], n))
        elif f[0] == "home" and len(f) == 4 and f[2] == "not-in-the-boot-set":
            homes.append((f[1], n))
        elif f[0] == "extra" and len(f) == 4 and f[2] in CLASSES:
            extras.append((f[1], f[2], n))
        else:                                            # a row that does not parse is never skipped
            return [], [], [], f"{path}:{n} is not 'hit<TAB>path<TAB>class<TAB>match<TAB>why' | 'home<TAB>name<TAB>not-in-the-boot-set<TAB>why' | 'extra<TAB>glob<TAB>class<TAB>why'"
    return hits, homes, extras, None


def cmd_repo(rev: str, table: str) -> int:
    r = git("rev-parse", "-q", "--verify", f"{rev}^{{commit}}")
    if r.returncode != 0:
        print(f"census: unread ({rev} does not name a commit)")
        return 1
    sha = r.stdout.decode().strip()
    print(f"census: rev {rev} = {sha}")
    hits_rows, _, _, problem = read_table(sha, table)
    if problem:
        print(f"census: unread ({problem})")
        return 1
    ls = git("ls-tree", "-r", "--name-only", sha, "--", *SCOPE)
    scanned = [p for p in ls.stdout.decode().splitlines() if p] if ls.returncode == 0 else []
    if not scanned:
        print(f"census: unread (0 files scanned under {' '.join(SCOPE)} at {sha[:12]}; ls-tree rc {ls.returncode})")
        return 1
    g = git("grep", "-n", "-I", "-E", f"{LITERAL}|{COMPOSED}", sha, "--", *SCOPE)
    if g.returncode not in (0, 1):
        print(f"census: unread (git grep rc {g.returncode})")
        return 1
    m = git("grep", "-n", "-I", "-E", MODULE, sha, "--", *SCOPE)
    if m.returncode not in (0, 1):
        print(f"census: unread (git grep MODULE rc {m.returncode})")
        return 1
    lines = g.stdout.decode("utf-8", "replace").splitlines()
    seen = {ln.split(":", 3)[1] + ":" + ln.split(":", 3)[2] for ln in lines}
    module: set[str] = set()
    for ln in m.stdout.decode("utf-8", "replace").splitlines():
        _, path, num, _t = ln.split(":", 3)
        if not is_module_scope(path):
            continue
        module.add(f"{path}:{num}")
        if f"{path}:{num}" not in seen:
            lines.append(ln)
    bad: list[str] = []
    # I-M1 (2): a public def of branches.py AT the rev that FN_CLASS does not name = unmapped (a new builder cannot be excused by a row)
    defs = set(re.findall(r"(?m)^def ([a-z][A-Za-z0-9_]*)\(", git("show", f"{sha}:extensions/agi/bin/branches.py").stdout.decode("utf-8", "replace")))
    if module and not defs:                              # a module hit owes a class only branches.py's defs can give
        bad.append(f"unread branches.py (0 public defs at {sha[:12]}, {len(module)} module hit(s) to class)")
    bad += [f"unmapped branches.{fn} (a public def of extensions/agi/bin/branches.py that FN_CLASS does not name)" for fn in sorted(defs - set(FN_CLASS))]
    family: list[tuple[str, str, str]] = []
    used: set[int] = set()
    by_class: dict[str, int] = {c: 0 for c in CLASSES}
    files: set[str] = set()
    for line in lines:
        _, path, num, text = line.split(":", 3)
        files.add(path)
        mod = f"{path}:{num}" in module
        row = next((x for x in hits_rows if x[0] == path and ((x[2] == "*" and not mod) or (x[2] != "*" and x[2] in text))), None)
        if row is None:
            bad.append(f"unclassed{' module' if mod else ''} {path}:{num}: {text.strip()[:100]}")
            continue
        used.add(row[3])
        by_class[row[1]] += 1
        if mod:                                          # I-M1 (1): the row's class must be what the called / imported function returns
            want = module_classes(text, defs)
            stripped = text.strip()
            if want and row[1] not in want and not (row[1] == "prose" and prose_start(stripped)):
                bad.append(f"bad-module-class {path}:{num} (row {table}:{row[3]} says {row[1]}, branches.py returns {'|'.join(sorted(want))})")
        if row[1] == "family" and (re.search(LITERAL, text) or re.search(TRUNK_COMPOSED, text)):
            family.append((path, num, text))
    for path, num, text in family:                       # W1 (aio): a family hit names no trunk, literally or composed
        bad.append(f"bad-family {path}:{num} (classed family but names the trunk: {text.strip()[:80]})")
    for path in sorted({x[0] for x in hits_rows if x[1] == "fixture"}):
        body = git("show", f"{sha}:{path}").stdout
        if not path.startswith("extensions/agi/tests/") or not re.search(rb"mktemp|tmp_path", body):
            bad.append(f"bad-fixture {path} (B2: 'fixture' holds only in a test file that builds its repo on mktemp / tmp_path)")
    bad += [f"stale {table}:{x[3]} {x[0]} {x[2]!r} (classes no hit)" for x in hits_rows if x[3] not in used]
    # A-N4 (alive 11:05:52Z): outside tests/, a prose row on a CODE file names a substring, never `*` (a live read added later would pass as prose);
    # the census's own two files keep `*` (they name the patterns they look for)
    bad += [f"bad-prose-row {table}:{x[3]} {x[0]} (a catch-all prose row on a code file)" for x in hits_rows
            if x[1] == "prose" and x[2] == "*" and not x[0].startswith("extensions/agi/tests/") and not x[0].endswith(".md")
            and x[0] not in (TABLE, "extensions/agi/bin/reader_census.py")]
    print(f"census: {len(scanned)} files scanned, {len(files)} with a hit ({len(module)} module hit(s)); " + ", ".join(f"{c} {n}" for c, n in by_class.items()))
    for b in bad:
        print(f"  {b}")
    print(f"census: {len(bad)} red" if bad else "census: every hit classed")
    return 1 if bad else 0


#: A-N6 + A2 (alive 13:53:50Z): the remote BUILD right before a call: origin/{.. or a quoted 'origin/' + (either quote), each with or without refs/remotes/
REMOTE_BUILD = r"""(?:refs/remotes/)?origin/\{[^}]*$|["'](?:refs/remotes/)?origin/["']\s*\+\s*$"""


def prose_start(stripped: str) -> bool:
    """I-M1's prose escape + A1 (alive 13:53:50Z): a comment, a doc bullet, a backtick, or a docstring opener (three quotes, either kind)."""
    return stripped[:1] in ("#", "*", "`") or stripped[:3] in ('"""', "'''")


def module_classes(text: str, defs: set[str]) -> set[str]:
    """I-M1: the classes a module hit's line owes (FN_CLASS of each branches.py def it calls or imports; a plain import = grammar).
    A call to a name that is not a def of branches.py (rotate.py's local dict `branches`) owes nothing: its row stands (I-M1 (3))."""
    out: set[str] = set()
    for c in re.finditer(r"\bbranches\.([A-Za-z_][A-Za-z0-9_]*)\(", text):
        fn = c.group(1)
        if fn not in defs or fn not in FN_CLASS:
            continue
        # A-N6 = I-M1r (alive, sp 12:19Z): a call whose result the line BUILDS into a remote name reads a remote ref; the strip form
        # (ref[len("origin/"):]) is not a build and keeps FN_CLASS
        before = text[:c.start()]
        out.add("remote" if re.search(REMOTE_BUILD, before) else FN_CLASS[fn])
    fns: list[str] = []
    m = re.match(r"\s*from\s+branches\s+import\s+(.*)", text)
    if m:
        fns += re.findall(r"([A-Za-z_][A-Za-z0-9_]*)(?:\s+as\s+[A-Za-z_][A-Za-z0-9_]*)?\s*(?:,|$|#)", m.group(1).split("#")[0] + ",")
    elif re.match(r"\s*import\s+branches\b", text):
        return {"grammar"}
    elif re.match(r"\s*from\s+\S+\s+import\s+(.*,\s*)?branches\b", text):   # U1 (sp p2): the package form of the plain import
        return {"grammar"}
    return out | {FN_CLASS[f] for f in fns if f in defs and f in FN_CLASS}


def is_module_scope(path: str) -> bool:
    """MODULE's scope: a non-test file outside branches.py itself and the census's own two files (they name the patterns; U-b3)."""
    return (not path.startswith("extensions/agi/tests/") and not os.path.basename(path).startswith("test_")
            and path not in ("extensions/agi/bin/branches.py", TABLE, "extensions/agi/bin/reader_census.py"))


def sha256(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def names_in(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            text = f.read().decode("utf-8", "replace")
    except OSError:
        return None
    got = [k for k, pat in NAMES.items() if re.search(pat, text)]
    return ",".join(got)


def cmd_homes(rev: str, table: str, root: str, main_hooks: str | None) -> int:
    _, home_rows, extras, problem = read_table(rev, table)
    if problem:
        print(f"homes: unread ({problem})")
        return 1
    try:
        entries = sorted(os.listdir(root))
    except OSError as e:
        print(f"homes: unread (the homes root {root}: {e.strerror})")
        return 1
    skip = {h for h, _ in home_rows}
    bad: list[str] = []
    # A-N3 (alive 11:05:52Z): a not-in-the-boot-set row never names a seat of config:posts, and a row whose entry is listable or absent is stale
    seats = set(re.findall(r'"name": "([^"]+)"', git("show", f"{rev}:.agi/nodes/.geometry/posts.md").stdout.decode("utf-8", "replace")))
    if not seats:                                        # A-N3b (alive): 0 seats parsed = the seat guard reads nothing, never a pass
        bad.append(f"unread config:posts (0 seats parsed from {rev}:.agi/nodes/.geometry/posts.md)")
    for h, n in home_rows:
        d = os.path.join(root, h)
        if h in seats:
            bad.append(f"bad-home {table}:{n} {h} (a seat of config:posts cannot be excused as not in the boot set)")
        elif not os.path.isdir(d) or os.access(d, os.R_OK | os.X_OK):
            bad.append(f"stale {table}:{n} home {h} (the entry is absent or listable: the row excuses nothing)")
    homes: list[tuple[str, str]] = []
    for e in entries:
        d = os.path.join(root, e)
        if not os.path.isdir(d):
            continue
        try:
            os.listdir(d)
        except OSError:
            if e in skip and e not in seats:
                print(f"  {e}: not in the boot set (table row)")
            else:
                bad.append(f"unread {e} (the home cannot be listed)")
            continue
        if os.path.isdir(os.path.join(d, "bin")):
            homes.append((e, os.path.join(d, "bin")))
    targets: list[tuple[str, str]] = []
    for h, b in homes:
        try:
            names = sorted(os.listdir(b))
        except OSError:
            bad.append(f"unread {h} (its bin/ cannot be listed)")
            continue
        targets += [(h, os.path.join(b, n)) for n in names if os.path.isfile(os.path.join(b, n))]
    if main_hooks is None:                               # A-N2: MAIN's own hook is read by DEFAULT (any process without core.hooksPath runs it)
        r = git("rev-parse", "--path-format=absolute", "--git-common-dir")
        main_hooks = os.path.join(r.stdout.decode().strip(), "hooks", "reference-transaction") if r.returncode == 0 else ""
    if not os.path.isfile(main_hooks) or not os.access(main_hooks, os.R_OK):
        bad.append(f"unread MAIN {main_hooks or '(no git common dir)'} (its reference-transaction hook cannot be read)")
    else:
        targets.append(("MAIN", main_hooks))
    for g, cls, _ in extras:
        hits = sorted(glob.glob(g))
        top = g.split("*", 1)[0].rsplit("/", 1)[0] or "/"
        if not hits and not os.access(top, os.R_OK | os.X_OK):
            bad.append(f"unread extra {g} ({top} cannot be listed by this uid: its owner reads this row)")
        elif not hits:
            bad.append(f"unread extra {g} (the glob matches nothing)")
        targets += [("extra:" + cls, p) for p in hits]
    if not homes:                                        # U-b1 (sp 10:29:01Z): a listing that finds nothing is no reading
        bad.append(f"unread homes (0 homes with bin/ under {root})")
    pieces = hashed = 0
    print(f"homes: {len(homes)} homes with bin/ under {root} + MAIN {main_hooks or '(none)'} + {len(extras)} extra glob(s)")
    for h, p in targets:
        names, digest = names_in(p), sha256(p)
        if names is None or digest is None:
            bad.append(f"unread {h} {p} (its bytes cannot be read)")
            continue
        hashed += 1
        if names:
            pieces += 1
            print(f"  {h} {p} {digest} {names}")
    if not hashed:
        bad.append("unread homes (0 pieces hashed)")
    for b in bad:
        print(f"  {b}")
    print(f"homes: {hashed} file(s) hashed, {pieces} reader(s) name the trunk; {len(bad)} unread" if bad else f"homes: {pieces} reader(s) name the trunk; 0 unread")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("repo", "homes"):
        s = sub.add_parser(name)
        s.add_argument("--rev", default="HEAD")
        s.add_argument("--table", default=TABLE)
    sub.choices["homes"].add_argument("--root", default="/var/lib/agi")
    sub.choices["homes"].add_argument("--main-hooks", default=None)
    a = ap.parse_args(argv)
    if a.cmd == "repo":
        return cmd_repo(a.rev, a.table)
    return cmd_homes(a.rev, a.table, a.root, a.main_hooks)


if __name__ == "__main__":
    sys.exit(main())
