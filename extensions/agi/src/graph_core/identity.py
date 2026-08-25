"""Identity scheme for graph-core (T-005 / R3).

ID scheme: ``<type-prefix>:<short-slug>``
- Slug is kebab-case, 2..5 tokens, derived deterministically from source text.
- Collisions append ``:n`` starting at ``:2`` in stable insertion order (R3.2).
- IDs longer than 40 chars trigger a non-fatal :class:`UserWarning` (R3.3).
- Same source text yields same id across rebuilds (R3.4).

---

Second scheme, added alongside the one above without changing it (goal:g2.5,
``level3:src-graph-core-identity@v2``): **fixed-width hierarchical addresses**.

Ids under this scheme are addresses, not lineage. Every real node gets a fixed
7-character id; a zoomed-out view groups the *same* nodes into supernodes by
truncating that id (``id[:6]``, ``id[:5]``, ...) — no join, no index, nothing
stored for the supernode itself. See ``mint_address``, ``supernode``,
``is_valid_address`` and ``plan_reid`` below. This is purely additive: nothing
above this line changes, and ``mint_id``/``IdRegistry`` remain the scheme the
loaders use until a migration (not this change) applies ``plan_reid``'s output.
"""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
import uuid
import warnings
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional

# Module-level config (R3.1: 2..5 tokens). Override per-call via min_tokens/max_tokens kwargs.
DEFAULT_MIN_TOKENS = 2
DEFAULT_MAX_TOKENS = 5
LENGTH_WARN_THRESHOLD = 40

_PUNCT_RE = re.compile(r"[^a-z0-9\s-]")
_WS_RE = re.compile(r"\s+")


def derive_slug(
    source_text: str,
    min_tokens: int = DEFAULT_MIN_TOKENS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """Derive a kebab-case slug from arbitrary text deterministically (R3.1)."""
    if not source_text or not source_text.strip():
        return "untitled"
    s = source_text.lower()
    s = _PUNCT_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    tokens = [t for t in s.split(" ") if t]
    if not tokens:
        return "untitled"
    tokens = tokens[:max_tokens]
    if len(tokens) < min_tokens:
        # Pad nothing — return what we have. Slug stability over min-token enforcement.
        pass
    return "-".join(tokens)


def _build_id(type_prefix: str, slug: str) -> str:
    return f"{type_prefix}:{slug}"


class IdRegistry:
    """Mints stable ids and tracks collisions (T-005 / R3.2, R3.4)."""

    def __init__(self) -> None:
        self._issued: dict[str, int] = {}  # base id -> last suffix used (1 means base)

    def mint(
        self,
        type_prefix: str,
        source_text: str,
        min_tokens: int = DEFAULT_MIN_TOKENS,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:
        """Mint an id. Same (type_prefix, source_text) yields same base; collisions append :n.

        Stability: feeding the same source text twice in distinct registries yields the
        same id (no collision suffix). Within ONE registry, the second call collides and
        receives ``:2``.
        """
        slug = derive_slug(source_text, min_tokens=min_tokens, max_tokens=max_tokens)
        base = _build_id(type_prefix, slug)
        if base not in self._issued:
            self._issued[base] = 1
            final = base
        else:
            self._issued[base] += 1
            final = f"{base}:{self._issued[base]}"
        if len(final) > LENGTH_WARN_THRESHOLD:
            warnings.warn(
                f"id '{final}' exceeds {LENGTH_WARN_THRESHOLD} chars",
                UserWarning,
                stacklevel=2,
            )
        return final

    def issued(self) -> set[str]:
        """Return the full set of issued ids (including suffixed variants)."""
        result: set[str] = set()
        for base, count in self._issued.items():
            result.add(base)
            for n in range(2, count + 1):
                result.add(f"{base}:{n}")
        return result


def mint_id(
    type_prefix: str,
    source_text: str,
    registry: Optional[IdRegistry] = None,
    min_tokens: int = DEFAULT_MIN_TOKENS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """Convenience wrapper. Without a registry, returns the base id (no collision tracking)."""
    if registry is None:
        slug = derive_slug(source_text, min_tokens=min_tokens, max_tokens=max_tokens)
        out = _build_id(type_prefix, slug)
        if len(out) > LENGTH_WARN_THRESHOLD:
            warnings.warn(
                f"id '{out}' exceeds {LENGTH_WARN_THRESHOLD} chars",
                UserWarning,
                stacklevel=2,
            )
        return out
    return registry.mint(type_prefix, source_text, min_tokens=min_tokens, max_tokens=max_tokens)


# --- goal:g2.5 — fixed-width hierarchical addresses ---

# Lowercase alphanumeric, 36 symbols. Deliberately case-INsensitive: git refs
# are case-sensitive (refs/grid/node/<id>), but case-insensitive filesystems
# exist in this project's own deployment story, and a 62-symbol (0-9a-zA-Z)
# scheme that breaks on one of the two is not worth the extra ~26 slots per
# character. Headroom, if 36 ever binds: switch to "0123456789" + string
# .ascii_lowercase + string.ascii_uppercase for 62 symbols/char — every
# function below takes ALPHABET as ambient state, not a hardcoded literal, so
# that switch is a one-line change plus a corpus-wide re-migration, not a
# rewrite.
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
assert len(ALPHABET) == 36 and len(set(ALPHABET)) == 36

DEFAULT_ADDRESS_WIDTH = 7
DEFAULT_GROUP_WIDTH = 6  # placeholder supernode prefix width until goal:g2.6 tags exist


def _digest_int(seed: str) -> int:
    """Stable hash of ``seed`` as a non-negative int.

    Uses blake2b, not Python's built-in ``hash()``. ``hash()`` is salted per
    process (``PYTHONHASHSEED`` randomization for str/bytes) specifically to
    resist DoS collision attacks — exactly the property that makes it useless
    here, since the whole point is that the same seed yields the same address
    in every process, forever. blake2b needs no extra dependency (stdlib
    ``hashlib``) and is fast enough for this corpus's size.
    """
    digest = hashlib.blake2b(seed.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big")


def _to_base_alphabet(value: int, width: int, alphabet: str = ALPHABET) -> str:
    """Render ``value`` as a fixed-``width`` string over ``alphabet`` (big-endian, zero-padded)."""
    base = len(alphabet)
    chars = []
    v = value
    for _ in range(width):
        v, rem = divmod(v, base)
        chars.append(alphabet[rem])
    return "".join(reversed(chars))


def mint_address(
    seed: str,
    taken: set[str],
    *,
    width: int = DEFAULT_ADDRESS_WIDTH,
) -> str:
    """Deterministically mint a fixed-``width`` address for ``seed``.

    **Stable under insertion, and here is why.** The address is
    ``hash(seed)`` truncated to ``width`` characters and nothing else — it
    does not read corpus size, sort position, or any other node's address.
    So in the overwhelmingly common case (no collision — the address space is
    36**7 ≈ 78 billion slots against a corpus in the hundreds), minting a new
    node can never change an existing node's address, because an existing
    node's address was never a function of "how many other nodes exist" to
    begin with. Contrast the scheme this replaces: a sort-position or
    counter-derived id renumbers every later node when one is inserted
    earlier. This one cannot, by construction.

    **Collision handling.** If the base hash is already in ``taken``, probe
    deterministically by rehashing ``f"{seed}#{n}"`` for n = 1, 2, 3, ... until
    a free slot is found. This is a pure function of ``(seed, taken)`` — same
    inputs, same output, regardless of what code path built up ``taken`` or in
    what order. A collision is resolved by moving the *new* seed to its next
    deterministic candidate; ``taken`` is only ever added to, never mutated to
    evict an existing entry, so an already-assigned node is never renumbered
    by a later collision.

    Batch callers (see ``plan_reid``) that want the *set* of resulting
    addresses to be independent of the order the caller happened to iterate
    seeds in must impose their own canonical order (e.g. sorted seeds) before
    calling this repeatedly — this function only promises purity given a
    concrete ``(seed, taken)`` pair, since which of two *simultaneously*
    colliding seeds "wins" the shared base slot is a batch-level decision,
    not a single-seed one.
    """
    base = _to_base_alphabet(_digest_int(seed), width)
    if base not in taken:
        return base
    counter = 1
    while True:
        candidate = _to_base_alphabet(_digest_int(f"{seed}#{counter}"), width)
        if candidate not in taken:
            return candidate
        counter += 1


def supernode(node_id: str, level: int) -> str:
    """Truncate ``node_id`` to its ``level``-character containing supernode.

    Truncation *is* the lookup (goal:g2.5): ``supernode("j8ids93", 6) ==
    "j8ids9"``, ``supernode("j8ids93", 5) == "j8ids"``. No join, no index, no
    stored node for the supernode — the renderer computes this on demand.
    Total and trivial by design: any ``level <= len(node_id)`` just slices.
    """
    return node_id[:level]


def is_valid_address(value: str, *, width: int = DEFAULT_ADDRESS_WIDTH) -> bool:
    """True iff ``value`` is exactly ``width`` characters, all drawn from ALPHABET."""
    return len(value) == width and all(c in ALPHABET for c in value)


def plan_reid(
    nodes: Iterable[Mapping[str, Any]],
    *,
    width: int = DEFAULT_ADDRESS_WIDTH,
    group_width: int = DEFAULT_GROUP_WIDTH,
    out_path: Optional[str | Path] = None,
) -> dict[str, Any]:
    """Plan (never apply) a corpus-wide old-id -> new fixed-width-address mapping.

    **This is a planner only. It writes no node file, touches no grid ref,
    and performs no corpus rewrite** — the migration that applies this
    mapping is a separate, reviewed step. The one file this function writes
    is the plan itself, at ``out_path`` (default: a fixed path under the
    system temp dir), as a record for that later review.

    ``nodes`` is an iterable of frontmatter-shaped mappings, each with at
    least an ``"id"`` key, and optionally ``"parents"`` (list), ``"supersedes"``
    (str) and ``"evidence_runs"`` (list) — the three reference kinds goal:g2.5
    calls out as needing rewriting if this mapping is ever applied. Anything
    else in the mapping is ignored, so callers can pass raw parsed frontmatter
    dicts directly.

    **Idempotent.** The output mapping is a pure function of the *set* of
    input ids: ids are sorted into a canonical order before any address is
    minted, so the result does not depend on the order ``nodes`` was iterated
    in, and running this twice over an unchanged corpus yields byte-identical
    output.

    **Grouping is a placeholder, not the design.** Until goal:g2.6's tag
    taxonomy exists, this assigns the ``group_width``-character supernode
    prefix from the *same* hash as the address itself (``supernode(new_id,
    group_width)``) — arbitrary relative to any human category, but stable
    (same id, same group, forever) and balanced (uniform hash distribution,
    not skewed by any one tag being popular). **When G2.6 tags land, they
    become what determines the prefix, and a node's address changes when its
    tag-derived group changes** — that is G2.5's open tension stated in
    ``GOALS.md``: the grid keys version history by id, so a re-tag becomes an
    id change becomes a grid-ref migration, unless the grid is repointed at a
    permanent mint-time key first. This function does not resolve that
    tension; it is recorded here so the placeholder is never mistaken for the
    real grouping rule.

    Returns a dict with:
    - ``mapping``: ``{old_id: new_id}`` for every input node.
    - ``supernode_groups``: number of distinct ``group_width``-char groups.
    - ``max_group_size``: largest membership of any one group.
    - ``groups_over_capacity``: count of groups whose membership exceeds 36
      (the alphabet size — the hard cap the last address character can
      distinguish within a shared prefix).
    - ``references``: ``{"parents": n, "supersedes": n, "evidence_runs": n,
      "total": n}`` — counts of individual references (not unique nodes) that
      resolve to an id in this corpus and would need rewriting if the mapping
      were applied.
    - ``out_path``: where the plan was written (str).
    """
    node_list = list(nodes)
    old_ids: list[str] = []
    seen: set[str] = set()
    for n in node_list:
        nid = n.get("id")
        if not isinstance(nid, str) or not nid:
            raise ValueError(f"plan_reid: node missing a string 'id': {n!r}")
        if nid in seen:
            raise ValueError(f"plan_reid: duplicate id in input corpus: {nid!r}")
        seen.add(nid)
        old_ids.append(nid)

    # Canonical order — independent of how `nodes` was iterated, so the
    # mapping is a pure function of the input *set*.
    mapping: dict[str, str] = {}
    taken: set[str] = set()
    for old_id in sorted(old_ids):
        new_id = mint_address(old_id, taken, width=width)
        taken.add(new_id)
        mapping[old_id] = new_id

    groups: dict[str, list[str]] = {}
    for new_id in mapping.values():
        groups.setdefault(supernode(new_id, group_width), []).append(new_id)
    max_group_size = max((len(members) for members in groups.values()), default=0)
    groups_over_capacity = sum(1 for members in groups.values() if len(members) > len(ALPHABET))

    def _as_list(value: Any) -> list:
        # Corpus frontmatter is hand- and model-written, not schema-enforced —
        # a field that is normally a list occasionally shows up as a bare
        # scalar (observed: `evidence_runs: 3` instead of a list). Treat
        # anything that isn't already a list as contributing zero references
        # rather than raising, since this function only counts, it never
        # validates the corpus's shape.
        return value if isinstance(value, list) else []

    ref_counts = {"parents": 0, "supersedes": 0, "evidence_runs": 0}
    for n in node_list:
        for parent in _as_list(n.get("parents")):
            if isinstance(parent, str) and parent in seen:
                ref_counts["parents"] += 1
        supersedes = n.get("supersedes")
        if isinstance(supersedes, str) and supersedes in seen:
            ref_counts["supersedes"] += 1
        for ev in _as_list(n.get("evidence_runs")):
            if isinstance(ev, str) and ev in seen:
                ref_counts["evidence_runs"] += 1
    ref_counts["total"] = sum(ref_counts.values())

    if out_path is None:
        out_path = Path(tempfile.gettempdir()) / "graph_core_plan_reid.json"
    out_path = Path(out_path)

    result = {
        "mapping": mapping,
        "supernode_groups": len(groups),
        "max_group_size": max_group_size,
        "groups_over_capacity": groups_over_capacity,
        "references": ref_counts,
        "out_path": str(out_path),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return result


# --- goal:g2.5 "Tension resolved 2026-08-25" — the OTHER identifier ---------
#
# `mint_address` above is deliberately re-derivable: retag a node, its group
# changes, its address changes. That is the point of an address. But
# `grid.py` keys version history on *some* id, and keying it on the thing
# that is designed to change on every regroup means every regroup becomes a
# ref migration — four of those forked live on 2026-08-24 and priced exactly
# how expensive that is. So the graph carries a second, disjoint identifier
# whose only job is to never move:
#
# | | mint id | address |
# |---|---|---|
# | Assigned | once, at node creation | derived, re-derived freely |
# | Ever changes | never | on every regroup/retag |
# | Shape | uuid or equivalent, opaque | 7 chars, alphanumeric, hierarchical |
# | Keys | `refs/grid/node/<mint-id>` | addressing, zoom, prefixes |
#
# Naming note: the *existing* `mint_id()` function above (T-005/R3) mints the
# `<type-prefix>:<slug>` scheme and predates this goal by a long way. Renaming
# it would break every caller across the corpus, so the permanent identifier
# gets a new, non-colliding name instead: `mint_permanent_id`.

MINT_ID_RE = re.compile(r"^[0-9a-f]{32}$")


def mint_permanent_id() -> str:
    """Mint a new permanent node id: opaque, immutable, collision-free
    without coordination, and a git ref path component with NO escaping
    required.

    **Format: 32 lowercase hex characters (``uuid.uuid4().hex``).** Chosen
    over the dashed ``8-4-4-4-12`` uuid rendering specifically so this
    function's own alphabet subsets ``grid.py``'s ref-safe character class —
    ``sanitize()`` becomes the identity function on its output (no colon to
    split on, nothing outside ``[0-9a-f]`` to percent-encode), which is the
    property this id needs to key a ref path directly. 122 bits of entropy
    (uuid4 clears 6 fixed version/variant bits) makes an accidental
    collision astronomically unlikely for a corpus in the thousands, so
    unlike ``mint_address`` above this function takes no ``taken`` set and
    performs no collision probing — coordination-free is the point, not a
    shortcut around it.

    **Never derived from node content, title or existing id.** A derived
    permanent id would recreate exactly the coupling this design removes: an
    id that changes when the text it was derived from changes. Contrast
    ``mint_address``, which is *supposed* to be a pure function of its seed
    — that is what makes an address cheap to re-derive. A mint id has the
    opposite job, so it is a pure function of *nothing* — freshly random
    every call, which is what "assigned once, at node creation" requires: if
    it were derivable, two independent callers minting for the "same" node
    could produce the same id without ever having coordinated, silently
    merging two nodes' grid histories.

    Callers mint once, at node creation, and persist the result verbatim in
    the node's ``mint_id`` frontmatter field forever — this function itself
    has no memory of what it has already minted and enforces no rewrite
    protection; that guarantee belongs to the writer (see
    ``bin/backfill-mint-ids.py``'s idempotence, and ``grid.py``'s refusal to
    write a version under any key except a node's own ``mint_id``).
    """
    return uuid.uuid4().hex


def is_valid_mint_id(value: str) -> bool:
    """True iff ``value`` is exactly 32 lowercase hex characters.

    Kept independent of ``mint_permanent_id``'s implementation so it can
    validate ids minted by *any* conforming producer, not just this one call
    site — e.g. a backfill script checking a value read back off disk.
    """
    return bool(MINT_ID_RE.fullmatch(value))
