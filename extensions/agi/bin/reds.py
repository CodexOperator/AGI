#!/usr/bin/env python3
"""reds.py — the ONE mechanical RED check over a commit range, before any
model (hypothesis:g716103). Git reads and tmp extracts only: no model, no
network, no write. The rules are IMPORTED, never copied: `anonymize` (box
tokens, email, scan), `links` (mint index, broken links), `dispatch` (the key
shape). Output is counts and NAMES — `path:line`, a node id — never a value's
bytes. The ONE cell `merge_gate.red_classes` names the classes; absent = all
three + a WARN (fail closed). rc 0 none, 1 at least one, 2 usage/git error.
"""
from __future__ import annotations
import argparse, io, json, re, subprocess, sys, tarfile, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import anonymize, links, locations  # noqa: E402

CLASSES = ("secrets", "node_deletion", "broken_link")
_ASSIGN = re.compile(r"""(?:^|[\s"'`])([A-Za-z_]\w*)\s*[:=]\s*["']?([\w./+:-]{8,})""")


def _git(repo, *args, binary=False):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       text=not binary, timeout=300)
    if p.returncode != 0:
        err = p.stderr if isinstance(p.stderr, str) else p.stderr.decode("utf-8", "replace")
        raise RuntimeError(f"git {' '.join(args[:2])} failed: " + err.strip()[:160])
    return p.stdout


def _extract(repo, rev, dest):
    """`rev`'s tree into a tmp dir; the graph root inside it is `.agi/`."""
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(_git(repo, "archive", "--format=tar", rev, binary=True))) as tf:
        tf.extractall(dest, filter="data")
    return dest / ".agi"

def _added(repo, old, new):
    """[(path, line, text)] — one entry per ADDED line, never joined (row 36)."""
    out, path, lineno = [], None, 0
    for l in _git(repo, "diff", "--unified=0", "--no-color", old, new).splitlines():
        if l.startswith("+++ b/"):
            path = l[6:]
        elif l.startswith("@@"):
            m = re.search(r"\+(\d+)", l); lineno = int(m.group(1)) - 1 if m else 0
        elif l.startswith("+") and not l.startswith("+++"):
            lineno += 1; out.append((path, lineno, l[1:]))
    return out


def _secrets(repo, old, new, root):
    """`path:line` of every added line carrying a secret. A line, never a value."""
    import dispatch  # late: keeps a pre-model gate cheap
    toks, allow = anonymize.box_tokens(root), anonymize.email_allow(root)
    return [f"{p}:{n}" for p, n, line in _added(repo, old, new)
            if anonymize.scan(line, toks, allow)
            or any(dispatch._looks_like_secret(nm, v) for nm, v in _ASSIGN.findall(line))]


def _node_deletions(repo, old, new, new_graph):
    """Node ids whose file is gone at NEW. A move into deprecated/ KEEPS its
    mint_id, so `--no-renames` plus the mint index — not git's similarity
    guess — is what says a node survived."""
    index = links.mint_index(new_graph)
    ids = {str(fm["id"]) for fm in
           links.frontmatter_rows(Path(new_graph) / "nodes").values() if fm.get("id")}
    out = []
    for path in _git(repo, "diff", "--diff-filter=D", "--no-renames", "--name-only",
                     old, new, "--", "*/nodes/*").splitlines():
        text = _git(repo, "show", f"{old}:{path}") if path.endswith(".md") else ""
        mint = re.search(r"^mint_id:\s*(\S+)", text, re.M)
        node = re.search(r"^id:\s*(\S+)", text, re.M)
        try:
            alive = (links.resolve_mint(new_graph, mint.group(1), index=index) is not None
                     if mint else bool(node) and node.group(1) in ids)
        except Exception:  # an index that cannot answer never claims a deletion
            alive = True
        if node and not alive:
            out.append(node.group(1))
    return out


def _broken_links(old_graph, new_graph):
    """`node->ref` broken at NEW and NOT at OLD — links' resolver, both ends."""
    def keys(graph):
        return {f"{e.node_id}->{e.ref}" for e in links.broken_by_status(graph)[0]}
    return sorted(keys(new_graph) - keys(old_graph))


def _classes(root):
    """The cell `merge_gate.red_classes`; absent, empty or naming no known class
    = all three + ONE WARN. A name that is not a class never SILENCES one."""
    cfg = locations.config_path(root)
    cell = (json.loads(cfg.read_text(encoding="utf-8")).get("merge_gate") or {}
            if cfg and cfg.is_file() else {})
    named = cell.get("red_classes")

    def warn(why, extra=""):
        print(f"WARN reds: {why}{extra} — running all of {', '.join(CLASSES)} (fail closed)", file=sys.stderr)

    if not isinstance(named, list) or not all(isinstance(c, str) for c in named):
        warn("no merge_gate.red_classes cell")
        return set(CLASSES)
    known = {c for c in CLASSES if c in named}
    if not known:
        warn("merge_gate.red_classes names no class", f" ({', '.join(sorted(set(named)))})")
        return set(CLASSES)
    if unknown := sorted(set(named) - set(CLASSES)):
        print(f"WARN reds: unknown red_classes ignored: {', '.join(unknown)}", file=sys.stderr)
    return known


def main(argv=None):
    ap = argparse.ArgumentParser(description="mechanical RED check over a commit range")
    ap.add_argument("verb", choices=["check"])
    ap.add_argument("old", help="a rev at the range's start")
    ap.add_argument("new", help="a rev at the range's end")
    ap.add_argument("--root", help="the project (default: the nearest enclosing .agi/)")
    ap.add_argument("--repo", help="the git repo (default: the source root)")
    a = ap.parse_args(argv)
    root = locations.find_project_root(a.root) if a.root else locations.find_project_root()
    if root is None:
        print("reds: no agi project found", file=sys.stderr); return 2
    repo = Path(a.repo) if a.repo else locations.source_root(root)
    want = _classes(root)
    try:
        with tempfile.TemporaryDirectory(prefix="reds-") as td:
            old_g, new_g = _extract(repo, a.old, Path(td) / "old"), _extract(repo, a.new, Path(td) / "new")
            red = {c: (f() if c in want else []) for c, f in (
                ("secrets", lambda: _secrets(repo, a.old, a.new, root)),
                ("node_deletion", lambda: _node_deletions(repo, a.old, a.new, new_g)),
                ("broken_link", lambda: _broken_links(old_g, new_g)))}
    except Exception as exc:  # a git that cannot answer is rc 2, never a silent 0
        print(f"reds: {exc}", file=sys.stderr); return 2
    print(f"reds: {a.old}..{a.new} — " + ", ".join(sorted(want)))
    for cls in CLASSES:
        names = red.get(cls) or []
        if names:
            print(f"RED {cls} {len(names)}: " + " ".join(names[:20]) + (" ..." if len(names) > 20 else ""))
    print("RED none" if not any(red.values()) else "")
    return 1 if any(red.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
