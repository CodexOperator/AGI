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
#: a BARE key-shaped value: `sk-` after any non-alnum (`h/` `a.` `_` `--`), never mid-word (`task-`); a path named sk-* over-refuses.
_BARE = re.compile(r"""(?<![A-Za-z0-9])sk-[\w./+:-]{5,}""")


def _git(repo, *args, binary=False):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       text=not binary, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(f"git {args[0]} exit {p.returncode}")  # the VERB and the code, never git's stderr BYTES (they carry this box's absolute paths)
    return p.stdout


def _payload_refs(graph):
    """Every distinct ref the nodes link to — the paths broken_link must resolve,
    read off links' OWN corpus walk (the key names are imported, not copied)."""
    rows = (links.link_ref(fm)[0] for _i, fm, _b in links._iter_corpus(graph))
    return sorted(set(rows) - {links.SELF})


def _extract(repo, rev, dest, payloads=True):
    """`rev`'s GRAPH into a tmp dir — `.agi/` plus, when broken_link is wanted, the payload paths its nodes link to — NOT the whole tree."""
    dest.mkdir(parents=True, exist_ok=True)
    graph = dest / locations.GRAPH_DIR_NAME

    def archive(paths):
        with tarfile.open(fileobj=io.BytesIO(
                _git(repo, "archive", "--format=tar", rev, "--", *paths, binary=True))) as tf:
            tf.extractall(dest, filter="data")

    archive([locations.GRAPH_DIR_NAME])
    present = (set(_git(repo, "ls-tree", "-r", "--name-only", rev).splitlines())
               if payloads else set())
    if extra := [p for p in _payload_refs(graph) if p in present]:
        archive(extra)
    return graph

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
            or any(dispatch._looks_like_secret(nm, v) for nm, v in _ASSIGN.findall(line))
            or any(dispatch._looks_like_secret("", v) for v in _BARE.findall(line))]


def _node_deletions(repo, old, new, old_graph, new_graph):
    """Node ids whose file is gone at NEW. A move into deprecated/ KEEPS its
    mint_id, so `--no-renames` plus the mint index — not git's similarity
    guess — is what says a node survived."""
    index = links.mint_index(new_graph)
    ids = {str(fm["id"]) for fm in
           links.frontmatter_rows(Path(new_graph) / "nodes").values() if fm.get("id")}
    at_old = {str(fm["id"]) for fm in links.frontmatter_rows(Path(old_graph) / "nodes").values() if fm.get("id")}
    out = []
    for path in _git(repo, "diff", "--diff-filter=D", "--no-renames", "--name-only",
                     old, new, "--", "*/nodes/*").splitlines():
        text = _git(repo, "show", f"{old}:{path}") if path.endswith(".md") else ""
        mint = re.search(r"^mint_id:\s*(\S+)", text, re.M)
        node = re.search(r"^id:\s*(\S+)", text, re.M)
        try:
            hit = links.resolve_mint(new_graph, mint.group(1), index=index) if mint else None
            # it survives only when its mint rides the SAME node, or one that did
            # not exist at OLD: a mint a pre-EXISTING other node carries is a
            # deletion wearing the mint as a disguise (DG3.54 item 1).
            alive = (hit is not None and not (hit[0] != node.group(1) and hit[0] in at_old)
                     if mint else bool(node) and node.group(1) in ids)
        except Exception as exc:  # fail CLOSED: an index that cannot answer is rc 2
            raise RuntimeError(f"node_deletion: {type(exc).__name__}") from None
        if node and not alive:
            out.append(node.group(1))
    return out


_FM = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)


def _broken_parents(graph):
    """`node->parent` for a `parents:` id that resolves to NO node at this tree —
    the backbone links.broken_by_status cannot see (payload links only, P13).
    The FRONTMATTER block only: a body line naming an id is prose, not a link."""
    rows = links.frontmatter_rows(Path(graph) / "nodes")
    live = {fm["id"] for fm in rows.values() if fm.get("id")}
    out = []
    for rel, fm in rows.items():
        if not fm.get("id"):
            continue
        text = (Path(graph) / "nodes" / rel).read_text(encoding="utf-8", errors="replace")
        blk = (_FM.match(text).group(1) if _FM.match(text) else "")
        named = re.search(r"^parents:[ \t]*(\[[^\]]*\]|(?:\n[ \t]*-[ \t]*\S+[ \t]*)+)", blk, re.M)
        if not named:
            continue
        pids = re.findall(r"[\w:.\-/+]+", re.sub(r"^[ \t]*-[ \t]*", "", named.group(1), flags=re.M))
        out += [f"{fm['id']}->{p}" for p in pids if p not in live]
    return out


def _broken_links(old_graph, new_graph):
    """`node->ref` broken at NEW and NOT at OLD — links' resolver at both ends
    for a payload link, and a `parents:` id at both ends for a graph edge."""
    def keys(graph):
        broken = [e for half in links.broken_by_status(graph) for e in half]  # BOTH halves: live AND retired
        return ({f"{e.node_id}->{e.ref}" for e in broken} | set(_broken_parents(graph)))
    return sorted(keys(new_graph) - keys(old_graph))


def _classes(root):
    """The cell `merge_gate.red_classes`; absent, empty or naming no known class
    = all three + ONE WARN. A name that is not a class never SILENCES one."""
    cfg = locations.config_path(root)
    try:
        cell = (json.loads(cfg.read_text(encoding="utf-8")).get("merge_gate") or {}
                if cfg and cfg.is_file() else {})
    except ValueError as exc:  # a config that does not parse is rc 2, never a traceback
        raise RuntimeError(f"red_classes: {cfg.name} does not parse ({type(exc).__name__})") from None
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
    try:
        want = _classes(root)
        with tempfile.TemporaryDirectory(prefix="reds-") as td:
            pay = "broken_link" in want
            old_g, new_g = (_extract(repo, a.old, Path(td) / "old", pay),
                            _extract(repo, a.new, Path(td) / "new", pay))
            red = {c: (f() if c in want else []) for c, f in (
                ("secrets", lambda: _secrets(repo, a.old, a.new, root)),
                ("node_deletion", lambda: _node_deletions(repo, a.old, a.new, old_g, new_g)),
                ("broken_link", lambda: _broken_links(old_g, new_g)))}
    except Exception as exc:  # a git that cannot answer is rc 2, never a silent 0
        print(f"reds: {exc if type(exc) is RuntimeError else type(exc).__name__}", file=sys.stderr); return 2
    print(f"reds: {a.old}..{a.new} — " + ", ".join(sorted(want)))
    for cls in CLASSES:
        names = red.get(cls) or []
        if names:
            print(f"RED {cls} {len(names)}: " + " ".join(names[:20]) + (" ..." if len(names) > 20 else ""))
    if not any(red.values()):
        print("RED none")
    return 1 if any(red.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
