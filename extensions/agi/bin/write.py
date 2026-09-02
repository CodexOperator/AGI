#!/usr/bin/env python3
"""write.py — the link layer of `goal:g13`'s one write path.

`goal:g13` says a node body is **a marker, not a payload**: what a node asserts
lives in a file the node points at, resolved at read time, and what sits in the
node file is a placeholder saying *where the body goes*. `payload_ref` on build
nodes is the prototype — a node that links a file rather than copying it, with
`grid.py` already versioning node and payload as one tree. This module
generalises that from one node type to every node type.

**Three questions the goal recorded unanswered, answered by the owner on
2026-09-02, and this module is where all three become code:**

1. **`THOUGHT` stays in the node body.** A node file carries a marker *and*
   exactly one authored region and they coexist, so nothing here moves, hides
   or rewrites a thought. Enforcement lives one layer down, in
   `node_writer.update_node`, which carries the authored region across any
   body it is handed — this module never writes a body at all.
2. **A goal node links to itself** — `link_ref: self`. The body *is* the data,
   said uniformly rather than as an absent field, so `goal:g6.9` stands and
   `GOALS.md` keeps rendering *from* goal bodies. **A reader never branches on
   `type == goal`;** it resolves `self` like any other link. That is the whole
   difference between an exception with a name and a hole.
3. **A missing link raises where a caller can act and is counted where it
   cannot.** `resolve` raises `MissingLink`; `resolve_many` returns a typed
   `MissingLinkSentinel` per node and a count. This is `goal:g13`'s founding
   finding applied to itself — the defect was never divergent *parsing*, it was
   divergent *failure semantics*, so the fix is not one behaviour everywhere
   but **two chosen** behaviours: loud where a caller can fix it, survivable
   where one bad node must not kill a scan of nine hundred.

## Declared self vs defaulted self

`link_ref: self` and no `link_ref` at all both resolve to the node's own body,
and the resolver reports **which of the two it got**. That distinction is the
same one `envfile.Resolution.from_node` makes for the same reason: *"the graph
said so"* and *"the fallback guessed"* are not the same claim, and a migration
cannot tell what is done from what was never started unless the two are
distinguishable.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import node_writer  # noqa: E402

#: The value that means "this node's body is its own data".
SELF = "self"

#: The field this module owns. `payload_ref` is read as its predecessor so the
#: 222 build nodes that already carry one are linked without being rewritten —
#: they proved the mechanism and do not have to be migrated to keep it.
LINK_FIELD = "link_ref"
LEGACY_LINK_FIELD = "payload_ref"

#: How the link was determined, reported alongside every resolution.
FROM_NODE = "declared"      # the node says `link_ref:`
FROM_LEGACY = "payload_ref"  # the node says `payload_ref:`
FROM_DEFAULT = "defaulted"   # the node says neither; the body is the data


class MissingLink(Exception):
    """A node links a file that is not there.

    Raised only by `resolve`, the single-node path, where a caller is in a
    position to do something about it. Bulk scans get a sentinel instead —
    see the module docstring.
    """

    def __init__(self, node_id: str, ref: str, path: Path):
        self.node_id = node_id
        self.ref = ref
        self.path = path
        super().__init__(
            f"{node_id} links {ref!r}, which does not exist at {path}. "
            f"A deprecated node whose file is gone must not fail quietly "
            f"(goal:g13); either restore the file or clear its {LINK_FIELD}."
        )


@dataclass(frozen=True)
class MissingLinkSentinel:
    """What a bulk scan gets instead of content, and instead of an exception.

    Typed rather than `None` on purpose: `None` is what three of the six
    readers `goal:g13` surveyed already returned, and it is indistinguishable
    from an empty body. A reader that mistakes this for content gets a
    `TypeError`, which is the loudest failure available to something that must
    not raise.
    """

    node_id: str
    ref: str
    path: Path

    def __bool__(self) -> bool:
        return False


@dataclass(frozen=True)
class Link:
    """One node's link, resolved. `content` is the body the node asserts."""

    node_id: str
    ref: str
    source: str            # FROM_NODE | FROM_LEGACY | FROM_DEFAULT
    path: Path | None      # None when the link is `self`
    content: str

    @property
    def is_self(self) -> bool:
        return self.ref == SELF


def link_ref(frontmatter: dict) -> tuple[str, str]:
    """`(ref, source)` for one node's frontmatter. Never raises.

    Resolution order, and each step is a decision rather than a fallback:

    1. `link_ref:` — what this module owns.
    2. `payload_ref:` — the prototype, read so build nodes are already linked.
    3. `self` — the body is the data, reported as **defaulted** so a migration
       can tell an untouched node from one that has declared itself.
    """
    ref = (frontmatter.get(LINK_FIELD) or "").strip()
    if ref:
        return ref, FROM_NODE
    legacy = (frontmatter.get(LEGACY_LINK_FIELD) or "").strip()
    if legacy:
        return legacy, FROM_LEGACY
    return SELF, FROM_DEFAULT


def link_path(root, ref: str) -> Path | None:
    """Where `ref` resolves on disk, or None for `self`.

    Against `locations.source_root` — the repo enclosing `.agi/` — because
    that is where `payload_ref` already resolves and this generalises that
    field rather than inventing a second base (`goal:g11`).
    """
    if ref == SELF:
        return None
    return Path(locations.source_root(root)) / ref


def resolve(root, node_id: str, frontmatter: dict, body: str) -> Link:
    """One node's content. **Raises `MissingLink`** if its file is gone.

    The single-node path, where the caller asked about this node specifically
    and can act on the answer.
    """
    ref, source = link_ref(frontmatter)
    if ref == SELF:
        return Link(node_id=node_id, ref=SELF, source=source, path=None,
                    content=body)
    path = link_path(root, ref)
    if path is None or not path.is_file():
        raise MissingLink(node_id, ref, path if path else Path(ref))
    return Link(node_id=node_id, ref=ref, source=source, path=path,
                content=path.read_text(encoding="utf-8"))


def resolve_many(root, nodes) -> tuple[list[Link], list[MissingLinkSentinel]]:
    """`(resolved, broken)` over many nodes. **Never raises for a broken link.**

    `nodes` is an iterable of `(node_id, frontmatter, body)`. One node whose
    file is gone must not end a scan of the corpus — that is the *survivable*
    half of the two chosen behaviours, and the sentinel plus the returned list
    is what keeps it from also being silent.
    """
    resolved: list[Link] = []
    broken: list[MissingLinkSentinel] = []
    for node_id, frontmatter, body in nodes:
        try:
            resolved.append(resolve(root, node_id, frontmatter, body))
        except MissingLink as exc:
            broken.append(MissingLinkSentinel(node_id=exc.node_id, ref=exc.ref,
                                              path=exc.path))
    return resolved, broken


def count_broken_links(root) -> int:
    """`broken_links` for `metrics.py`. Zero is the healthy value.

    Same shape as `unevidenced_decisive_verdicts`: a number that should be 0,
    where nonzero names a specific repairable defect rather than a mood.
    """
    _resolved, broken = resolve_many(root, _iter_corpus(root))
    return len(broken)


def _iter_corpus(root):
    """Every live and deprecated node as `(id, frontmatter, body)`.

    Reads the deprecated tree too, live-first, because a reader that stops
    seeing a retired node fails quietly and in its own way — which is the
    documented hazard this whole goal exists to remove, and it would be a poor
    joke to reintroduce it inside the fix.
    """
    from graph_core.persistence import frontmatter as fm_reader

    nodes_dir = Path(root) / "nodes"
    if not nodes_dir.is_dir():
        return
    for path in sorted(nodes_dir.rglob("*.md")):
        if path.name.startswith("."):
            continue
        try:
            nf = fm_reader.load_node_file(path)
        except Exception:
            # A node that will not parse is the READ half's problem and is
            # already counted there. Skipping it here keeps this metric about
            # links and nothing else.
            continue
        node_id = str(nf.frontmatter.get("id") or path.stem)
        yield node_id, nf.frontmatter, nf.body


def set_link(root, node_id: str, ref: str) -> Path:
    """Declare a node's link, through the one gated write routine.

    Goes through `node_writer` rather than editing the file, because
    `goal:s17`'s whole point is that there is one routine that writes a node
    and everything else reaches it. Writing `link_ref` by hand here would make
    this module the second write path in the goal that exists to remove them.
    """
    path = node_writer.find_node_file(root, node_id)
    if path is None:
        raise MissingLink(node_id, ref, Path(str(node_id)))
    if ref != SELF:
        target = link_path(root, ref)
        if target is None or not target.is_file():
            raise MissingLink(node_id, ref, target if target else Path(ref))
    result = node_writer.update_node(root, node_id, set_fm={LINK_FIELD: ref})
    if result.status == node_writer.REJECTED:
        raise ValueError(f"could not link {node_id}: {result.reason}")
    return path


def main(argv: list[str] | None = None) -> int:
    """`write.py links [--broken]` — report the corpus's link state."""
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", nargs="?", default="links",
                    choices=["links", "schema"])
    ap.add_argument("--root", default=".", help="any path inside the project")
    ap.add_argument("--broken", action="store_true", help="list broken links only")
    ap.add_argument("--fix", action="store_true",
                    help="schema: actually backfill derivable fields "
                         "(default is a dry run)")
    args = ap.parse_args(argv)

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    if args.action == "schema":
        return _schema_report(root, fix=args.fix)

    resolved, broken = resolve_many(root, _iter_corpus(root))
    by_source: dict[str, int] = {}
    for link in resolved:
        by_source[link.source] = by_source.get(link.source, 0) + 1

    if not args.broken:
        print(f"links: {len(resolved)} resolved, {len(broken)} broken")
        for source in (FROM_NODE, FROM_LEGACY, FROM_DEFAULT):
            print(f"  {source:12} {by_source.get(source, 0)}")
    for sentinel in broken:
        print(f"  BROKEN {sentinel.node_id} -> {sentinel.ref} ({sentinel.path})")
    return 1 if broken and args.broken else 0


def _schema_report(root, fix: bool = False) -> int:
    """Which nodes violate their type's `required` list, and optionally fix them.

    `goal:s31` closed the *new-node* half: a scaffold is now born with every
    required field this engine can derive, and says so when it cannot. This is
    the **existing corpus**, which accumulated invalid nodes for as long as
    nothing validated at write time.

    Dry by default and loudly so. A backfill rewrites hundreds of nodes and
    mints a grid version for each; that is reversible but it is not the
    director's call to make silently, and the report is the useful half either
    way.

    Only ever fills what can be DERIVED — `title` from the slug, and any field
    a body states under its own heading. A field nothing can supply stays
    missing and stays counted, because inventing one would put exactly the
    `TODO(model)` placeholder into the corpus that `goal:g2.10` spent 8,034
    fields teaching this project to fear.
    """
    from graph_core.persistence import frontmatter as fm_reader

    nodes_dir = Path(root) / "nodes"
    by_type: dict[str, list[tuple[str, list[str]]]] = {}
    for path in sorted(nodes_dir.rglob("*.md")):
        if path.name.startswith("."):
            continue
        ntype = node_writer.canonical_node_type(path.parent.name)
        required = node_writer.required_fields(root, ntype)
        if not required:
            continue
        try:
            nf = fm_reader.load_node_file(path)
        except Exception:
            continue
        node_id = str(nf.frontmatter.get("id") or f"{ntype}:{path.stem}")
        missing = node_writer.missing_required(root, ntype, nf.frontmatter, node_id)
        if missing:
            by_type.setdefault(ntype, []).append((node_id, missing))

    total = sum(len(v) for v in by_type.values())
    print(f"schema: {total} node(s) missing a required field")
    for ntype, entries in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
        fields: dict[str, int] = {}
        for _nid, missing in entries:
            for name in missing:
                fields[name] = fields.get(name, 0) + 1
        summary = ", ".join(f"{k}x{v}" for k, v in sorted(fields.items()))
        print(f"  {ntype:14} {len(entries):4}   {summary}")

    if not fix:
        if total:
            print("dry run — re-run with --fix to backfill derivable fields")
        return 0

    fixed = still = 0
    for entries in by_type.values():
        for node_id, _missing in entries:
            res = node_writer.derive_required_from_body(root, node_id)
            if res.status == node_writer.UPDATED:
                fixed += 1
            else:
                still += 1
    print(f"schema: backfilled {fixed}, {still} still incomplete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
