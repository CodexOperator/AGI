"""seatsig.rings -- multisig rings: m-of-n signatures over decision records.

RUNG 2 of the owner's eight-rung multisig ladder
(goal:g15; hypothesis:l4-a-ring-decision-carries-m-of-n-signatures, the
Prime's cell, town all). A ring is a config row naming its members' POST KEYS
and its threshold ``m``:

    rings:
      - name: approval
        m: 2
        members: [belam, sanctuary-director, sensei-director]

A DECISION RECORD (a merge-up grant, a spawn over the budget, a config:posts
row edit outside self_row) carries ``signatures:`` -- a list of
``<post>:<scheme>:<sig_hex>`` over the record's CANONICAL BYTES (rung 1's
injective canonical form: the record kind then its fields, one ``k:v`` per
line, each colliding byte string collapses to ONE line sequence, so the sign
side and the verify side always see exactly the same bytes).

The gates verify m-of-n through the SAME seatsig Scheme interface as send.py
(``seatsig.get(name).verify(pub, msg, sig)`` -- never their own crypto), and
a record short of m is REFUSED by name with the count. RINGS ARE OPT-IN: a
record type no ring names passes unchanged; every gate asks the rings cell
first and only then, if a ring is named, demands the quorum.

Member public keys are resolved by a pluggable ``pubkey_for_post`` callable
so the gate can use whatever the record type already knows (the posts config
rows' ``pubkey`` cell, the fixtures a test hands it, ...). DEFAULT_PUBKEY
reads the posts/seats geometry rows through geometry_config -- the same
row source send.py's verify labels against -- so a ring on a real tree
verifies exactly the keys send.py would. Nothing here writes.

Labels (rung-1 FORGED vocabulary inherited from send.py's inbox reader):
``VERIFIED``  the sig verifies under the member's current pubkey
``FORGED``    a member's sig that does NOT verify
``OUTSIDE``   a sig whose post is not a member of the ring
``UNKEYED``   a member whose current pubkey cannot be resolved (nothing to
              refute it with -- not counted toward m)
``WRONG_SCHEME``  the sig names a scheme seatsig does not know
Returns the distinct valid member count and per-sig labels, so a gate that
refuses can name the record, the ring, the m-of-n count, and the offending
labels -- never a bare boolean.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import seatsig

#: The one geometry cell the rings live in (Prime's cell, sibling of the
#: posts.md the write/inbox readers use): `<root>/nodes/.geometry/rings.md`
#: carrying a frontmatter `rings:` list. READ ONLY -- never a live ring here.
RINGS_CELL = Path("nodes") / ".geometry" / "rings.md"


def json_field(value) -> str:
    """One record field's canonical STRING serialization, so a gate can
    hand canonical_bytes the same bytes on the sign and the verify side for
    ANY value shape (a config-row edit's set_fm values are lists/dicts). A
    plain string passes through unchanged (already injective); anything else
    is deterministic-sorted JSON so two distinct values can never fuse into
    one line. The persisted record stores these STRING fields, which round-
    trip through frontmatter/JSON losslessly, so a reader recomputes the
    exact canonical bytes the signer covered."""
    if isinstance(value, str):
        return value
    import json as _json

    return _json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_bytes(kind: str, fields: dict) -> bytes:
    """The injective canonical bytes a record's signatures cover.

    ``kind\n`` then each field as ``key:value\n`` in the caller's given
    order (a dict preserves insertion order, so the caller controls the
    field order; the SAME kind+fields dict order must be used on both the
    sign and verify side). Two distinct records can never collide: the kind
    is the first line and every field is one ``k:v`` line, so a ``k`` or a
    ``v`` that itself contains ``\\n`` cannot fuse two records into one.
    """
    lines = [kind]
    for key, value in fields.items():
        lines.append(f"{key}:{value}")
    return ("\n".join(lines) + "\n").encode()


def decision_cell(ring_name: str, kind: str, fields: dict, signatures: list):
    """The ON-DISK cell one ring-authorized decision persists into the record
    that gate already writes: the ring that approved it, the record kind, the
    EXACT (string-serialized) fields the gate signed, and the signatures.

    Re-verification is argv-free by construction: a reader recomputes
    canonical_bytes(kind, fields) from the cell's OWN kind+fields (never a
    --ring-sig flag) and checks the cell's signatures m-of-n. Any field
    tamper changes the canonical bytes, so a signature valid for a different
    decision fails to verify; removing a signature reads short-of-m by name.
    """
    return {
        "ring": ring_name,
        "kind": kind,
        "fields": dict(fields),
        "signatures": list(signatures or []),
    }


@dataclass
class _Tampered:
    """RingResult shaped like verify_ring's, for a cell that cannot be read:
    not a dict, no kind, or the reader picked a different ring. These are
    REFUSED BY NAME (never a bare False) so a tampered record names what is
    wrong."""

    ring_name: str
    threshold: int
    member_count: int = 0
    n_valid: int = 0
    ok: bool = False
    labels: dict = field(default_factory=dict)
    refused: str = ""

    def summary(self) -> str:
        return self.refused or f"{self.ring_name}: tampered record"


def verify_decision(decision, ring: dict, get_scheme=seatsig.get,
                    pubkey_for_post=None) -> RingResult:
    """RE-verify a PERSISTED decision cell against a ring, WITHOUT any argv.

    ``decision`` is the cell decision_cell() produced (the ``ring_decision``
    key a gate persisted onto the record it already writes); ``ring`` is the
    ring definition (loaded, by ``decision['ring']``, from the rings cell by
    the reader). Canonical bytes come from decision['kind']+decision['fields']
    -- the exact bytes the signer covered -- and the signatures from
    decision['signatures']. A missing/empty signatures list verifies
    short-of-m BY NAME (the tampered record), and a tampered field changes the
    canonical bytes so a signature for a different decision reads FORGED.
    """
    name = ring.get("name", "?")
    threshold = int(ring.get("m", 0) or 0)
    if not isinstance(decision, dict) or not decision.get("kind"):
        return _Tampered(
            name, threshold, len(ring.get("members") or []),
            refused=(f"record carries no readable ring decision cell for "
                     f"{name!r} (tampered or absent); it needs {threshold} "
                     f"valid signature(s)"))
    canonical = canonical_bytes(decision["kind"], decision.get("fields") or {})
    return verify_ring(ring, canonical, decision.get("signatures") or [],
                       get_scheme=get_scheme, pubkey_for_post=pubkey_for_post)


def load_rings(root, path: Path | None = None) -> list:
    """The `rings:` rows from the geometry cell, or [] when absent/unparseable.

    Reads through the SAME engine node loader the geometry rows use
    (graph_core.persistence.frontmatter) -- never a hand-rolled copy of the
    frontmatter read. A malformed cell degrades to [] so an absent or broken
    rings cell can never make a gate demand a quorum (rings are opt-in).
    """
    cell = Path(root) / (path or RINGS_CELL)
    if not cell.is_file():
        return []
    try:
        from graph_core.persistence import frontmatter

        nf = frontmatter.load_node_file(cell)
        rows = nf.frontmatter.get("rings") or []
        if isinstance(rows, list):
            return [r for r in rows if isinstance(r, dict)]
    except Exception:  # noqa: BLE001  (an unreadable cell is an absent cell)
        pass
    return []


def ring_by_name(rings: list, name: str) -> dict | None:
    """The ring whose ``name`` equals ``name``, or None (opt-in: no ring
    named -> no quorum demanded)."""
    for ring in rings:
        if ring.get("name") == name:
            return ring
    return None


def _default_pubkey_for_post(post: str):
    """Resolve a member's CURRENT public key from the posts/seats geometry
    rows (the same row source send.py's verify labels against). None when
    the post has no resolvable key -- a ring then reads UNKEYED for it."""
    try:
        import geometry_config

        rows = geometry_config.load_rows(None)
    except Exception:  # noqa: BLE001
        return None
    for row in rows:
        if row.get("name") == post:
            return row.get("pubkey") or None
    return None


@dataclass
class RingResult:
    """Outcome of an m-of-n check on one record against one ring.

    ``ok`` True iff `distinct valid member sigs` >= ``ring.m``. ``refused``
    carries the one-line reason (naming the m-of-n count and any bad labels)
    when not ok, so a gate can REFUSE BY NAME. ``labels`` is
    post -> label for every signature handed in.
    """

    ring_name: str
    threshold: int
    member_count: int
    n_valid: int = 0
    ok: bool = False
    labels: dict = field(default_factory=dict)
    refused: str = ""

    def summary(self) -> str:
        """One human line: `name: m-of-n satisfied` or `name: m-of-n but N
        valid (need m); labels post=FORGED post2=OUTSIDE`."""
        if self.ok:
            return (
                f"{self.ring_name}: {self.n_valid}-of-{len(self.labels)} "
                f"satisfied (threshold {self.threshold})"
            )
        return (
            f"{self.ring_name}: {self.n_valid}-of-{len(self.labels)} valid "
            f"(need {self.threshold}); "
            + ", ".join(f"{p}={lbl}" for p, lbl in sorted(self.labels.items()))
        )


def verify_ring(ring: dict, canonical: bytes, signatures: list,
                get_scheme=seatsig.get,
                pubkey_for_post=None) -> RingResult:
    """Verify m-of-n signatures over ``canonical`` for one ring.

    ``ring`` is a dict with ``name``/``m``/``members`` (a list of POST KEYS).
    ``signatures`` is the record's ``signatures:`` list of
    ``<post>:<scheme>:<sig_hex>``. ``get_scheme`` defaults to
    ``seatsig.get`` (the ONE registry); ``pubkey_for_post`` defaults to the
    posts-rows resolver. Every sig is checked through ``scheme.verify`` --
    never a hand-rolled verifier -- and a record short of ``m`` is REFUSED
    (``ok`` False, ``refused`` naming the count).
    """
    name = ring.get("name", "?")
    threshold = int(ring.get("m", 0) or 0)
    members = set(ring.get("members") or [])
    resolve_pub = pubkey_for_post or _default_pubkey_for_post

    result = RingResult(name, threshold, len(members))
    valid_posts = set()
    for sig in signatures or []:
        # <post>:<scheme>:<sig_hex> -- split on the first two colons so a
        # hex sig (or a scheme name) may itself contain a colon safely.
        parts = str(sig).split(":", 2)
        if len(parts) != 3:
            result.labels["<malformed>"] = "MALFORMED"
            continue
        post, scheme_name, sig_hex = parts
        try:
            sig_bytes = bytes.fromhex(sig_hex)
        except ValueError:
            result.labels[post] = "BAD_HEX"
            continue
        if post not in members:
            result.labels[post] = "OUTSIDE"
            continue
        try:
            scheme = get_scheme(scheme_name)
        except KeyError:
            result.labels[post] = "WRONG_SCHEME"
            continue
        pub = resolve_pub(post)
        if not pub:
            result.labels[post] = "UNKEYED"
            continue
        try:
            if scheme.verify(bytes.fromhex(pub), canonical, sig_bytes):
                result.labels[post] = "VERIFIED"
                valid_posts.add(post)
            else:
                result.labels[post] = "FORGED"
        except Exception:  # noqa: BLE001  (a bad pub/sig must label, not raise)
            result.labels[post] = "FORGED"

    result.n_valid = len(valid_posts)
    result.ok = result.n_valid >= threshold
    if not result.ok:
        bad = ", ".join(
            f"{p}={lbl}" for p, lbl in sorted(result.labels.items())
            if lbl not in ("VERIFIED",)
        ) or "<none checked>"
        result.refused = (
            f"record needs {threshold} valid ring signature(s) from " 
            f"{name!r} (m-of-n), got {result.n_valid}; {bad}"
        )
    return result