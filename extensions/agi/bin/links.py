#!/usr/bin/env python3
"""links.py — the link layer of `goal:g13`'s one write path.

**Renamed from `write.py` on 2026-09-03.** This module never wrote the write
path; it resolves what a node points *at* — `link_ref`, `self`, `MissingLink`,
and the `broken_links` count. The name `write.py` now belongs to the verb layer
(formerly `edit.py`), which is the thing a human or an agent actually drives.
Two honest names beat one name doing two jobs.

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
   the goal body is the whole goal (GOALS.md retired). **A reader never branches on
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

import re
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


class MalformedNode(Exception):
    """A frontmatter key the sanctioned writer could never have written.

    Raised by `resolve` on the single-node path BY NAME (node id + key), so a
    glued line is refused here instead of riding on as a defaulted `self` link
    with nothing anywhere saying so (hypothesis:a-node-frontmatter-that-is-
    not-the-writers-shape-is-refused). The rule is
    `node_writer.writer_key_shape` — the writer owns it; links asks. NOT a
    `MissingLink`: damage to the NODE, not a missing payload, so it is never
    counted as a broken link.
    """


def off_shape_keys(frontmatter: dict) -> list[str]:
    """Keys of one node's frontmatter that `set` could never have written."""
    return [str(k) for k in frontmatter if not node_writer.writer_key_shape(k)]

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


def link_path(root, ref: str, location: str | None = None) -> Path | None:
    """Where `ref` resolves on disk, or None for `self`.

    Against the node's own named `location`, which defaults to `source_root`
    — the repo enclosing `.agi/` — because that is where `payload_ref` has
    always resolved (`goal:g11`). Naming the base rather than hardcoding it is
    `goal:g13.1`: a tree that moves becomes a config edit instead of a sweep
    over every node. `locations.payload_base` is the one place the name is
    turned into a path.
    """
    if ref == SELF:
        return None
    return locations.resolve_payload_path(Path(root), ref, location)


def resolve(root, node_id: str, frontmatter: dict, body: str) -> Link:
    """One node's content. **Raises `MissingLink`** if its file is gone.

    The single-node path, where the caller asked about this node specifically
    and can act on the answer.
    """
    ref, source = link_ref(frontmatter)
    off = off_shape_keys(frontmatter)
    if off:
        raise MalformedNode(
            f"{node_id}: frontmatter key(s) not in the sanctioned writer's "
            f"shape (a hand-appended line, not a `set` field): "
            + ", ".join(k[:60] for k in off))
    if ref == SELF:
        return Link(node_id=node_id, ref=SELF, source=source, path=None,
                    content=body)
    path = link_path(root, ref, frontmatter.get("location"))
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

    🔴 **A retired node's missing payload is not damage, and reconciling that
    took until 2026-09-03 because no build node had ever been retired.**
    `build:bin-render-context` was deprecated and its file deleted — the
    documented end state of retirement, with every byte still in the node's
    grid ref. `broken_links` went to 1 and stayed there, which would have made
    a standing invariant permanently red for doing the right thing.

    Worse, the schema will not let the contradiction be edited away: `[build]`
    **requires** `payload_ref`, so the write gate correctly refuses to remove
    it from a deprecated node. The field must keep naming a path that is
    deliberately gone.

    So the rule is: **damage is a broken link on a LIVE node.** A deprecated
    node's unresolvable payload is reported separately by `broken_by_status`
    and excluded here, because an alarm that cannot be cleared by correct
    action stops being read.
    """
    live, _retired = broken_by_status(root)
    return len(live)


def broken_by_status(root) -> tuple[list, list]:
    """`(broken_on_live_nodes, broken_on_deprecated_nodes)`.

    Both halves are returned rather than one, so "we retired 40 build nodes"
    is visible as a number instead of vanishing into an exclusion.
    """
    live_broken, retired_broken = [], []
    for nid, fm, body in _iter_corpus(root):
        try:
            resolve(root, nid, fm, body)
        except MissingLink as exc:
            if str(fm.get("status") or "").strip().lower() == "deprecated":
                retired_broken.append(exc)
            else:
                live_broken.append(exc)
    return live_broken, retired_broken


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
        if off_shape_keys(nf.frontmatter):
            # A key `set` could never have written resolves as a defaulted
            # `self` link and reads clean: refuse it, and NAME it below.
            continue
        node_id = str(nf.frontmatter.get("id") or path.stem)
        yield node_id, nf.frontmatter, nf.body


def off_shape_nodes(root) -> list[str]:
    """`node_id: key` for every corpus node whose frontmatter is off-shape —
    the name the links read path owes the corpus, even though such a node is
    excluded from the link metrics (as an unparseable one always was)."""
    from graph_core.persistence import frontmatter as fm_reader

    out = []
    for path in sorted((Path(root) / "nodes").rglob("*.md")):
        try:
            fm = fm_reader.load_node_file(path).frontmatter
        except Exception:
            continue
        for key in off_shape_keys(fm):
            out.append(f"{fm.get('id') or path.stem}: {key[:60]}")
    return out


#: The ONE `links` config cell, on a `config` NODE -- `.agi/config.json` is refused by `done`.
LINKS_CONFIG_ID = "config:links"
_LINKS_DEFAULTS = {
    "scanned": [".agi/nodes/**/*.md", "extensions/agi/briefs/**/*", ".agi/sessions/quorum/*.md", "CLAUDE.md", "QUICKSTART.md", "skills/agi/SKILL.md"],
    "exempt": [".agi/nodes/deprecated/", "THOUGHT", "lens", "judged_against"],
    "line_template": "{file}:{line} {old} \u2192 {succ}",
}
_GOAL_RE = re.compile(r"goal:[\w.-]+")
#: The explicit marker a retired node uses to RECORD a successor. A bare
#: mention of another goal inside the THOUGHT is a cause, not a successor.
_SUCCESSOR_MARKER = "Superseded"


def _goal_id(token: str) -> str:
    """A matched `goal:` token with sentence punctuation stripped, so
    `goal:g15.` -> `goal:g15` and `goal:g7.25.` -> `goal:g7.25`; an interior
    dot is part of a real id and is kept."""
    return token.rstrip(".-")


def _successor(thought: str) -> str:
    """The successor a retired node's THOUGHT RECORDS, or `none`.

    Requires the explicit `Superseded` marker; the successor is a `goal:` id
    in that marked clause (not necessarily the token right after `by`)."""
    for line in thought.splitlines():
        if _SUCCESSOR_MARKER in line:
            m = _GOAL_RE.search(line)
            if m:
                return _goal_id(m.group(0))
    return "none"


def _links_config(root) -> dict:
    for nid, fm, _body in _iter_corpus(root):
        if nid == LINKS_CONFIG_ID:
            return {**_LINKS_DEFAULTS, **(fm.get("links") or {})}
    return dict(_LINKS_DEFAULTS)


def scan_retired_refs(root, cfg=None) -> list[tuple[str, int, str, str]]:
    """`[(rel, line, old_id, successor)]`: every LIVE ref to a retired or absent
    goal id. Report only; never edits. A retired node's own refs are not live."""
    from graph_core.persistence import frontmatter as fm_reader

    cfg = cfg or _links_config(root)
    known, retired = set(), {}
    for nid, fm, body in _iter_corpus(root):   # deprecated tree is status: deprecated
        known.add(nid)
        if str(fm.get("status") or "").lower() == "retired":
            b = node_writer.thought_text(body)
            retired[nid] = _successor(b) if b is not None else "none"
    src, nodes = locations.source_root(Path(root)), Path(root) / "nodes"
    no_path = [str(e) for e in cfg["exempt"] if str(e).endswith("/")]
    no_field = {str(e) for e in cfg["exempt"] if not str(e).endswith("/") and e != "THOUGHT"}
    hits = []
    for pattern in cfg["scanned"]:
        for path in sorted(src.glob(pattern)):
            rel = str(path.relative_to(src))
            if not path.is_file() or any(rel.startswith(e) for e in no_path):
                continue
            lines = path.read_text("utf-8", "replace").splitlines()
            if path.is_relative_to(nodes):         # node -> frontmatter only
                try:
                    fm = fm_reader.load_node_file(path).frontmatter
                except Exception:
                    continue
                if str(fm.get("status") or "").lower() == "retired":
                    continue
                end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
                skip = {i for i, l in enumerate(lines[:end], 1)
                        if (m := re.match(r'\s*-?\s*"?([A-Za-z_]\w*)"?\s*:', l))
                        and m.group(1) in no_field}
            else:                                  # surface -> whole file, no THOUGHT
                end, skip, inside = len(lines), set(), False
                for i, l in enumerate(lines, 1):
                    inside = inside or "THOUGHT:BEGIN" in l
                    if inside:
                        skip.add(i)
                    if "THOUGHT:END" in l:
                        inside = False
            for i, line in enumerate(lines[:end], 1):
                if i in skip:
                    continue
                for token in _GOAL_RE.findall(line):
                    old = _goal_id(token)
                    if old in retired or old not in known:
                        hits.append((rel, i, old, retired.get(old, "none")))
    return hits


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


def frontmatter_rows(nodes_dir) -> "dict[str, dict]":
    """rel path -> {id, mint_id, type, title, status} of every node file under
    `nodes_dir`, from ONE `git grep` (no yaml, no cache, no walk). FRONTMATTER
    lines only: a key counts between line 1's `---` and the next fence, so a
    body line `mint_id: x` is never read. A grep that cannot look raises
    rotation_record.GrepError (fails closed). goal:g4.18.6.1 + .2.2."""
    import subprocess
    import rotation_record
    try:
        # SM 127: -a -- a NUL byte anywhere in a file's first 8 KB made git print
        # "Binary file <path> matches" instead of its rows: the node vanished
        r = subprocess.run(["git", "grep", "--no-index", "-aznE",
                            r"^(---\s*$|(id|mint_id|type|title|status):)", "--", "*.md"],
                           cwd=Path(nodes_dir), capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        raise rotation_record.GrepError(f"git grep could not run: {exc}") from None
    err = r.stderr.decode("utf-8", "surrogateescape").strip()
    if r.returncode >= 2 or (r.returncode == 1 and err):
        raise rotation_record.GrepError(f"git grep exit {r.returncode}: {err}")
    files: dict = {}
    # SM 121: split on \n only (str.splitlines also splits U+2028, \x0c, a bare
    # \r) and never raise on a non-UTF-8 byte -- one odd byte is no collision
    for line in r.stdout.decode("utf-8", "surrogateescape").split("\n"):
        if line.count("\0") < 2:
            continue
        rel, n, text = line.split("\0", 2)
        fm = files.setdefault(rel, {"_fences": 0})
        if text.rstrip() == "---":
            fm["_fences"] += 1 if (fm["_fences"] or n == "1") else 2
        elif fm["_fences"] == 1:
            key, _, val = text.partition(":")
            fm.setdefault(key, _scalar(val.strip()))
    for rel in [k for k, fm in files.items() if fm["_fences"] == 1]:   # SM 120a
        _warn_once(nodes_dir, f"warn: {rel}: frontmatter never closes -- not indexed")
        del files[rel]
    return files


def _scalar(val: str) -> str:
    """One frontmatter scalar as YAML reads it: a quoted one is YAML-decoded
    (escapes like \" -- the quoted titles, DG2; `'it''s'`), a plain one ends
    at YAML's comment (` #`, SM 123: an unquoted title holding ` ## x`)."""
    if val[:1] in "\"'":
        import yaml  # noqa: PLC0415
        try:
            out = yaml.safe_load(val)
            return val if out is None else str(out)
        except yaml.YAMLError:
            return val[1:-1] if len(val) > 1 and val[0] == val[-1] else val
    return "" if val.startswith("#") else re.split(r"\s#", val, maxsplit=1)[0].rstrip()


_WARNED: set = set()


def _warn_once(where, line: str) -> None:
    """An index warning, once per process and tree -- never once per create /
    resolve (SM run 12 note)."""
    if (key := (str(Path(where).resolve()), line)) not in _WARNED:
        _WARNED.add(key)
        print(line, file=sys.stderr)


def mint_index(root) -> "dict[str, list[tuple[str, str, str, str, bool]]]":
    """goal:g4.18.6.1 -- mint_id -> [(id, type, title, status, retired)], every
    node carrying it, read off `frontmatter_rows` (one grep per read). A list,
    so a collision stays visible."""
    out: dict = {}
    for rel, fm in frontmatter_rows(Path(root) / "nodes").items():
        if fm.get("mint_id") and not fm.get("id"):   # SM 120b: named, never silent
            _warn_once(root, f"warn: {rel}: mint_id {fm['mint_id']} but no id -- not indexed")
        if fm.get("mint_id") and fm.get("id"):
            out.setdefault(fm["mint_id"], []).append(
                (fm["id"], fm.get("type", ""), fm.get("title", ""), fm.get("status", ""),
                 rel.startswith("deprecated/")))
    return out


def resolve_mint(root, mint: str, *, index=None) -> "tuple[str, str, str] | None":
    """goal:g4.18.6.1 -- THE mint-id resolver: mint_id -> (id, title, status)
    of the ONE node carrying it, read off `mint_index`: LIVE first, then a
    retired sibling under deprecated/ (CLAUDE.md: a grid ref outlives its file;
    SM 104) -- `status` says which. NO shape check: off-shape mints are
    accepted as found, the gate is "is a node's mint_id" (the Prime, signed
    22:1xZ 09-29, verbatim on goal:g4.18.6.4.1). A mint two nodes of one tier carry raises ValueError by
    name, never a silent pick; empty or absent -> None; a grep that cannot look
    raises GrepError (fails closed). `index` = a prebuilt mint_index, so a
    batch reader pays ONE grep, never one per item (DG2 fork)."""
    if not (mint or "").strip():
        return None
    hits = (mint_index(root) if index is None else index).get(mint, [])
    for tier in (False, True):
        same = [h for h in hits if h[4] == tier]
        if len(same) > 1:
            raise ValueError(f"mint id {mint} is carried by {len(same)} "
                             f"{'retired' if tier else 'live'} nodes: "
                             + ", ".join(sorted(h[0] for h in same)))
        if same:
            i, _type, title, status, _ = same[0]
            return (i, title, status or ("deprecated" if tier else ""))
    return None


def address_resolver(root):
    """goal:g4.18.6.3.1 -- the `resolve` a graph_core loader takes: an id ->
    the address of the ONE node whose mint_id it is, else None. The one index
    is built on the first call only (a graph with no mint-id parent pays no
    grep); a collision answers None, so the item stays dangling, never picked.
    An address (`type:slug`) answers None at once: no live mint carries a ':'
    (5284/5284, 09-30), so a family-B caller's `resolve(x) or x` greps nothing
    for a graph written in addresses (goal:g4.18.6.3.2)."""
    index = []

    def resolve(ref: str):
        if not isinstance(ref, str) or ":" in ref or not ref.strip():
            return None
        if not index:
            index.append(mint_index(root))
        try:
            hit = resolve_mint(root, ref, index=index[0])
        except ValueError:
            return None
        return hit[0] if hit else None
    return resolve


from graph_core.identity import is_valid_mint_id as is_mint_id  # noqa: E402  (node_writer put src on the path)


class _ByAddress:
    """goal:g4.18.6.3.3 -- an address-keyed index (a gate's type index, the
    evidence corpus) that answers a MINT id as its address twin, through THE
    resolver: a key it lacks goes to address_resolver (lazy -- an index read
    only by addresses never greps; a collision stays a miss)."""
    _resolve = staticmethod(lambda k: None)

    def address(self, k):
        return k if super().__contains__(k) else (self._resolve(k) or k)

    def __contains__(self, k):
        return super().__contains__(self.address(k))


class ResolvingDict(_ByAddress, dict):
    def get(self, k, default=None):
        return super().get(self.address(k), default)

    def __getitem__(self, k):
        return super().__getitem__(self.address(k))


class ResolvingSet(_ByAddress, frozenset):
    pass


def gate_resolver(nodes_dir):
    """THE address_resolver for a gate holding `nodes_dir`: built only when it
    is `<root>/nodes` (the tree mint_index reads), and a grep that cannot look
    is a MISS (None, remembered) -- a gate's `in` / `get` never raises."""
    import rotation_record
    r = [address_resolver(Path(nodes_dir).parent) if Path(nodes_dir).name == "nodes" else None]

    def resolve(ref):
        try:
            return r[0] and r[0](ref)
        except rotation_record.GrepError:
            r[0] = None
            return None
    return resolve


def resolving(index, *nodes_dirs):
    """`index` (a dict or a frozenset) behind the gate_resolver of each nodes
    dir, first hit wins (cli's corpus unions worktree trees)."""
    out = (ResolvingDict if isinstance(index, dict) else ResolvingSet)(index)
    rs = [gate_resolver(d) for d in nodes_dirs]
    out._resolve = lambda k: next(filter(None, (r(k) for r in rs)), None)
    return out


_MAP_CACHE: dict = {}


def _sha_map_path(root) -> "Path | None":
    """g133 -- the ONE map path: cell `paths.local_maxxing.scrub_commit_map`, through
    the ONE project-root discovery + `locations.load_config`; no second rule."""
    graph = locations.find_project_root(Path(root).resolve())
    if graph is None:
        return None
    cell = (locations.load_config(graph).get("paths") or {}).get("local_maxxing") or {}
    rel = str(cell.get("scrub_commit_map") or "").strip()
    return locations.repo_root(graph) / rel if rel else None


def _git_commit(root, rev) -> str:
    """g133 -- git alone says what is a commit; a failed subprocess is a miss."""
    import subprocess
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"],
            capture_output=True, text=True, timeout=15)
        return proc.stdout.strip() if proc.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def _map_rows(p) -> list:
    """g133 -- ONE read per (path, mtime): a CLI-scale caller resolves many ids.
    An UNREADABLE map is no rows, never a raise, never a print."""
    try:
        key = (str(p), p.stat().st_mtime_ns)
    except (OSError, ValueError):   # a row the reader cannot open is a MISS
        return []
    if key not in _MAP_CACHE:
        if len(_MAP_CACHE) > 8: _MAP_CACHE.clear()
        try:
            _MAP_CACHE[key] = [re.split(r"[\s,]+", ln.strip()) for ln in
                               p.read_text(encoding="utf-8", errors="replace").splitlines()
                               if ln.strip() and not ln.startswith("#")]
        except (OSError, ValueError):
            pass   # uncached: the next call retries, and judges nothing
    return _MAP_CACHE.get(key, [])


def resolve_old_sha(root, sha: str) -> "str | None":
    """g133 -- THE pre-rewrite commit-id resolver. Git first; else a map row whose
    OLD id the input prefixes EXACTLY once, whose NEW id is non-zero and a commit
    git knows; else None -- silently, never a raise. A dropped commit is no commit."""
    sha = (sha or "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{4,40}", sha):
        return None
    if hit := _git_commit(root, sha):
        return hit
    p = _sha_map_path(root)
    if p is None or not p.is_file():   # is_file() swallows OSError -> False
        return None
    hits = [r[1] for r in _map_rows(p) if len(r) >= 2 and r[0].lower().startswith(sha)]
    new = hits[0] if len(hits) == 1 else ""   # ambiguous -> no row
    return _git_commit(root, new) or None     # a dropped commit is not a commit


def main(argv: list[str] | None = None) -> int:
    """`write.py links [--broken]` — report the corpus's link state."""
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", nargs="?", default="links",
                    choices=["links", "schema", "roles", "mint", "sha"])
    ap.add_argument("mint_id", nargs="?", default="",
                    help="mint: the mint id to resolve, any shape (goal:g4.18.6.1)")
    ap.add_argument("--root", default=".", help="any path inside the project")
    ap.add_argument("--broken", action="store_true", help="list broken links only")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when a live reference to a retired or absent "
                         "goal id remains")
    ap.add_argument("--fix", action="store_true",
                    help="schema: actually backfill derivable fields "
                         "(default is a dry run)")
    args = ap.parse_args(argv)

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    if args.action == "sha":   # hypothesis:g133: ONE id in, ONE id out
        if not args.mint_id:   # an absent id is refused BY NAME, never resolved as ""
            print("ERR: sha needs a commit id", file=sys.stderr)
            return 2
        hit = resolve_old_sha(root, args.mint_id)
        if hit is None:
            print("unknown commit id", file=sys.stderr)   # the input id never echoes
            return 1
        print(hit)
        return 0

    if args.action == "schema":
        return _schema_report(root, fix=args.fix)

    if args.action == "roles":
        return _roles_report(root)

    if args.action == "mint":   # goal:g4.18.6.1: a link is a mint id
        import rotation_record
        try:
            hit = resolve_mint(root, args.mint_id)
        except ValueError as exc:
            print(f"ERR: {exc}", file=sys.stderr)
            return 2
        except rotation_record.GrepError as exc:   # SM 102: never a traceback, never rc 1
            print(f"ERR: mint lookup could not look: {exc}", file=sys.stderr)
            return 2
        if hit is None:
            print(f"ERR: no live node carries mint id {args.mint_id}", file=sys.stderr)
            return 1
        print("\t".join(hit))
        return 0

    resolved, broken = resolve_many(root, _iter_corpus(root))
    by_source: dict[str, int] = {}
    for link in resolved:
        by_source[link.source] = by_source.get(link.source, 0) + 1

    # Split the same way the metric does, and SHOW the retired count rather
    # than quietly excluding it — an exclusion nobody can see is how an
    # invariant rots into a number that is always green.
    live_broken, retired_broken = broken_by_status(root)
    cfg = _links_config(root)
    retired_refs = scan_retired_refs(root, cfg)

    if not args.broken:
        print(f"links: {len(resolved)} resolved, {len(live_broken)} broken"
              + (f" ({len(retired_broken)} retired payload(s), not damage)"
                 if retired_broken else ""))
        for source in (FROM_NODE, FROM_LEGACY, FROM_DEFAULT):
            print(f"  {source:12} {by_source.get(source, 0)}")
        print(f"retired: {len(retired_refs)} live reference(s) to a retired or absent goal id")
        for rel, lineno, old, succ in retired_refs:
            print("  " + cfg["line_template"].format(
                file=rel, line=lineno, old=old, succ=succ))
        off = off_shape_nodes(root)
        if off:
            print(f"off-shape: {len(off)} frontmatter key(s) refused by name "
                  f"(not the writer's shape; not link damage)")
            for name in off:
                print(f"  MALFORMED {name}")
    for sentinel in live_broken:
        print(f"  BROKEN {sentinel.node_id} -> {sentinel.ref} ({sentinel.path})")
    for sentinel in retired_broken:
        print(f"  retired {sentinel.node_id} -> {sentinel.ref} "
              f"(deprecated; bytes in the grid ref)")
    if args.strict and retired_refs:
        return 1
    return 1 if live_broken and args.broken else 0


def _verdict_class_disagreements(root) -> list[str]:
    """A verdict's class must equal the class its evidence experiment recorded.
    `:N` is stripped; an experiment with no `verdict:` records no class and is
    silent; report only, never write.
    """
    k = lambda v: str(v or "").strip().split(":")[0]
    norm = lambda v: v if isinstance(v, list) else ([] if v is None else [v])
    corpus = {nid: fm for nid, fm, _ in _iter_corpus(root)}
    out, r = [], address_resolver(root)   # goal:g4.18.6.3.2: a mint-id ref reads as its address
    for nid, fm in corpus.items():
        if fm.get("type") != "verdict":
            continue
        refs = norm(fm.get("evidence_runs")) + norm(fm.get("parents"))
        for ref in dict.fromkeys(r(str(x)) or str(x) for x in refs):
            ef = corpus.get(ref) or {}
            ec = k(ef.get("verdict"))
            if ef.get("type") == "experiment" and ec and ec != k(fm.get("verdict")) and ec != k(fm.get("demoted_from")):
                out.append(f"verdict-class: {nid} says {k(fm.get('verdict'))}, {ref} says {ec}")
    return out


def outside_repo_path(root, ref, location=None):
    """Resolved path of `ref` when it lands OUTSIDE the repo tree, else None.
    ONE predicate: the schema report and write.py's refusal both call it."""
    if not ref or str(ref).strip() == SELF:
        return None
    p = locations.resolve_payload_path(Path(root), str(ref).strip(), location).resolve()
    return None if p.is_relative_to(locations.source_root(Path(root))) else p


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

    verdict_class = _verdict_class_disagreements(root)
    outside = [f"outside-ref: {nid} {f} -> {p}"
               for nid, fm, _ in _iter_corpus(root)
               for f in (LINK_FIELD, LEGACY_LINK_FIELD)
               if (p := outside_repo_path(root, fm.get(f), fm.get("location")))]
    total = sum(len(v) for v in by_type.values())
    print(f"schema: {total} node(s) missing a required field, "
          f"{len(verdict_class)} verdict-class disagreement(s), "
          f"{len(outside)} outside-ref(s)")
    print("\n".join(verdict_class + outside),
          end="\n" if verdict_class or outside else "")
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


def parse_written_by(wb):
    """The admitted-writers set a `written_by` schema value denotes.

    The ONE parse for the field, shared by the report (`_roles_report`'s
    `_admitted`) and the write enforcer (`write.py._enforce_written_by`), so
    the two can never disagree about what the field may hold
    (hypothesis:l4-written-by-message-and-shape). Accepts a comma/space
    separated str, a list, or None. Returns None when the field is absent
    (undeclared) so a caller can tell "gates nothing" from "has writers".
    Passes through to `links.py roles` semantics unchanged.
    """
    if wb is None:
        return None
    if isinstance(wb, str):
        return {v for v in wb.replace(",", " ").split() if v}
    return set(wb)


def _roles_report(root) -> int:
    """Report the writer-coverage GAP and the violations, dry by default.

    A role report compares a node's recorded writer against what its TYPE
    admits, and today almost no type admits anything: only `[moral].md`
    declares `written_by:` at all. So a violations-only report would print a
    near-empty list and read as a clean bill of health when the truth is that
    almost nothing is CHECKABLE yet. This prints BOTH halves:

      (a) the coverage census — for every node type present in the corpus,
          whether its schema declares `written_by:` and how many nodes it
          holds, so the unchecked types are VISIBLE and counted;
      (b) for the types that DO declare one, every node whose recorded
          writer is not admitted, named with its node id and the writer
          found, and every node that records no writer, said as UNRECORDED
          rather than guessed or skipped silently.

    The recorded writer is read from what already exists — frontmatter
    `role:`, then `edited_by:`. This changes nothing: no node written, no
    schema edited, no `--fix`. Dry by default and loudly so.
    """
    from schema_registry import load_schemas_from_dir

    schemas_dir = Path(root) / "context" / "schemas"
    reg = load_schemas_from_dir(schemas_dir) if schemas_dir.is_dir() else None

    def _admitted(ntype):
        """The set of writers a type's schema admits, or None if undeclared."""
        if reg is None:
            return None
        s = reg.get(node_writer.canonical_node_type(ntype))
        if s is None:
            return None
        return parse_written_by((s.frontmatter or {}).get("written_by"))

    # type -> {admitted, count, nodes:[(node_id, writer or None)]}
    census: dict[str, dict] = {}
    for node_id, fm, _body in _iter_corpus(root):
        ntype = str(fm.get("type") or "unknown")
        e = census.setdefault(ntype, {"admitted": None, "count": 0, "nodes": []})
        if e["admitted"] is None:
            e["admitted"] = _admitted(ntype)
        e["count"] += 1
        role = fm.get("role")
        edited_by = fm.get("edited_by")
        writer = None
        if role not in (None, ""):
            writer = str(role)
        elif edited_by not in (None, ""):
            writer = str(edited_by)
        e["nodes"].append((node_id, writer))

    declared = {t: e for t, e in census.items() if e["admitted"] is not None}
    gap = {t: e for t, e in census.items() if e["admitted"] is None}

    # Half (a): the coverage census — the gap IS the finding today.
    print(f"roles: {len(census)} node type(s) in the corpus; "
          f"{len(declared)} declare(s) written_by, "
          f"{len(gap)} do not (the coverage gap)")
    print(f"  coverage census ({len(census)} type(s)):")
    print(f"    {'type':16} {'nodes':>6}  written_by")
    for ntype in sorted(census):
        e = census[ntype]
        wb = e["admitted"]
        shown = ",".join(sorted(wb)) if wb else "(none)"
        print(f"    {ntype:16} {e['count']:6}  {shown}")

    # Half (b): violations + unrecorded, only for types that declare a writer.
    violations: list[tuple[str, str, str]] = []   # (ntype, node_id, writer)
    unrecorded: list[tuple[str, str]] = []        # (ntype, node_id)
    for ntype, e in sorted(declared.items()):
        for node_id, writer in e["nodes"]:
            if writer is None:
                unrecorded.append((ntype, node_id))
            elif writer not in e["admitted"]:
                violations.append(
                    (ntype, node_id, writer))

    if violations:
        print(f"roles: {len(violations)} writer violation(s) "
              f"(recorded writer not admitted by the type's schema):")
        for ntype, node_id, writer in violations:
            admitted = ",".join(sorted(census[ntype]["admitted"]))
            print(f"  {node_id} -> wrote as {writer!r} (admitted: {admitted})")
    if unrecorded:
        print(f"roles: {len(unrecorded)} UNRECORDED node(s) in declared types "
              f"(no `role:` or `edited_by:` to check):")
        for ntype, node_id in unrecorded:
            print(f"  {node_id} -> UNRECORDED")
    if not violations and not unrecorded:
        print(f"roles: {len(declared)} declared type(s) — every recorded writer "
              f"is admitted, none unrecorded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
