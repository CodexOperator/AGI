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
``<post>:<scheme>:<sig_hex>`` over the record's CANONICAL BYTES (the
INJECTIVE canonical JSON form: one object carrying the record kind and its
fields, field pairs sorted by key, each value type-tagged -- see
canonical_bytes -- so the sign side and the verify side always see exactly
the same bytes and no key/value/kind content can fuse two records).

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
from datetime import datetime, timezone
from pathlib import Path
import secrets
import time

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
    is the same recursively type-tagged ``_enc`` encoding canonical_bytes
    uses, so two distinct values (a tuple vs a list, a dict keyed by the
    int ``1`` vs its ``"1"`` str twin) never fuse into one line. The
    persisted record stores these STRING fields, which round-trip through
    frontmatter/JSON losslessly, so a reader recomputes the exact canonical
    bytes the signer covered."""
    if isinstance(value, str):
        return value
    import json as _json

    return _json.dumps(_enc(value), ensure_ascii=False,
                       separators=(",", ":"))


def _type_tag(value) -> str:
    """Canonical JSON type tag for a field value, so two distinct Python
    values can NEVER share a serialization. ``json`` already distinguishes
    ``"1"`` (str) from ``1`` (int) from ``True`` from ``None`` in its
    output, but the tag makes the distinction explicit and structural at
    the cost of a few bytes -- belt and braces a reader owns outright.
    ``bool`` MUST be checked before ``int`` (bool subclasses int).

    Distinct tags, and within one tag json.dumps is injective, so a tag
    pair ``[tag, dumped_value]`` is injective over all field values.
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, tuple):
        return "tuple"
    if isinstance(value, dict):
        return "object"
    return "other"


def _dump(value) -> str:
    """Deterministic canonical JSON for ONE value: every scalar, dict key
    and container recursively tagged by ``_enc`` so the emitted bytes are
    INJECTIVE at every depth. Non-ASCII emitted raw so the sign side and the
    verify side always produce byte-identical UTF-8. (The canonical_bytes
    PURE function needs no randomness or time -- freshness is carried in as
    FIELDS, never here.)"""
    import json as _json

    return _json.dumps(_enc(value), ensure_ascii=False, separators=(",", ":"))


def _enc(value):
    """Recursively tag ONE value as [tag, content] so the emitted canonical
    JSON is INJECTIVE at every depth (kid B closes kid A's two holes: a dict
    whose keys are not all str must not fuse with its str-keyed twin, and a
    tuple must not share a tag with a list). ``content`` is a JSON-able
    structure (a scalar, or nested [tag, content] pairs) and every container
    -- dict keys AND values -- is tagged the same way.

    A dict is emitted as [object, [[key_tag, value_tag], ...]] with the pairs
    sorted by their key's dumped bytes, so an int key ``1`` (tagged int) is
    forever distinct from the str key ``"1"`` (tagged str) and ordering never
    depends on caller insertion order. A tuple is tagged ``tuple``, a list
    ``list``, so the two container types can never fuse.
    """
    import json as _json

    tag = _type_tag(value)
    if tag == "null":
        return [tag, None]
    if tag == "bool":
        return [tag, bool(value)]
    if tag in ("int", "float"):
        return [tag, value]
    if tag == "str":
        return [tag, value]
    if tag in ("list", "tuple"):
        return [tag, [_enc(x) for x in value]]
    if tag == "object":
        items = [[_enc(k), _enc(v)] for k, v in value.items()]
        items.sort(key=lambda kv: _json.dumps(kv[0], ensure_ascii=False,
                                              separators=(",", ":")))
        return [tag, items]
    # anything not JSON-native (a custom object) serializes by repr -- the
    # tag still names the type so two distinct objects can never share bytes
    return [tag, str(value)]


def canonical_bytes(kind: str, fields: dict) -> bytes:
    """The INJECTIVE, self-delimiting canonical bytes a record's signatures
    cover. Canonical JSON: ONE object carrying both the kind and the fields,
    the field pairs SORTED by their canonical key bytes and every key AND
    value recursively TYPE-TAGGED::

        {"kind":["str","g"],"fields":[[["str","x"],["str","1"]]]}

    Sorted keys are chosen over preserving caller dict order so the bytes do
    NOT depend on the insertion order a config row happened to arrive in --
    the sign side and the verify side can only agree if they compute the
    same bytes from the SAME kind+fields, and order-independence makes that
    true regardless of how either side parsed the persisted cell. Sorting is
    deterministic; order was never a record property worth pinning.

    JSON is self-delimiting, so no ``k``, ``v`` or the kind itself can fuse
    two distinct records: a key or value containing ``\\n``, ``:``, ``\\\\`` or
    any byte round-trips through JSON escaping, and the type tags keep
    ``"1"`` (str) from colliding with ``1`` (int), ``[1]`` from ``(1,)``,
    and a dict keyed by the int ``1`` from its ``"1"`` str-keyed twin
    (kid B closes kid A's two measured holes -- every value AND every dict
    key is tagged, so no two distinct decisions share bytes).
    """
    import json as _json

    def _ksort(kv):
        return _json.dumps(_enc(kv[0]), ensure_ascii=False, separators=(",", ":"))

    flds = [[_enc(k), _enc(v)] for k, v in sorted(
        fields.items(), key=_ksort)]
    return _json.dumps({"kind": kind, "fields": flds},
                       ensure_ascii=False, separators=(",", ":")).encode("utf-8")

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


# ---------------------------------------------------------------------------
# FRESHNESS (kid B): a ring decision's signatures cover the decision fields;
# today those fields carry NO time and NO nonce, so a persisted quorum
# REPLAYS ACROSS TIME -- the same signed suite-grant is valid forever.
# Freshness is carried in as FIELDS (canonical_bytes stays PURE: no time, no
# randomness). A producer adds a reserved ``_fresh`` field ("<ts>|<nonce>")
# through fresh_fields; a gate does not sign until freshness_refusal admits
# the record BY NAME. The per-ring max_age_s is read from the ring row when
# present, else DEFAULT_MAX_AGE_S, and load_rings/ring_by_name carry that key
# through unchanged (the raw row dict is passed along).
# ---------------------------------------------------------------------------

DEFAULT_MAX_AGE_S = 900
#: a fresh timestamp may be at most this far in the future before a gate
#: names clock-skew.
MAX_FUTURE_SKEW_S = 300
#: the reserved key freshness rides in; a caller may not reuse it (a granted
#: ``_fresh`` in the input fields is overwritten, never merged -- see
#: fresh_fields, and the test that pins it).
FRESH_KEY = "_fresh"
#: how long a remembered nonce stays in the on-disk ledger before pruning.
NONCE_LEDGER_TTL_S = 86400


#: where nonce_ledger keeps the admitted-nonce log: a FILENAME ONLY, resolved
#: at call time under the project's SHARED sessions dir (locations
#: shared_sessions_dir) so every git worktree shares ONE ledger -- never under
#: `<root>/nodes/.geometry`, which is committed graph content and would churn
#: commits once a ring is live (RUNG 2b clause 5).
NONCE_LEDGER_FILE = "ring-nonces.json"


class LedgerWriteError(Exception):
    """A nonce_ledger.remember() write could not be completed.

    Raised instead of swallowing (RUNG 2b clause 3): a nonce is NEVER spent
    silently -- if the admitted-nonce ledger cannot be written, the caller (a
    ring gate) converts this into a by-name refusal so the decision is not
    admitted with an unremembered nonce (an admitted replayed record would
    otherwise become possible after a failed ledger write)."""


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_ts(value) -> float | None:
    """Parse an RFC3339/ISO-8601 UTC timestamp ('2026-09-12T16:45:56Z') back
    to unix epoch, or None when unparseable (an unparseable fresh ts reads as
    REFUSED by name -- never a window a reader cannot judge)."""
    if not value:
        return None
    s = str(value)
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(s).timestamp()
    except ValueError:
        return None


def fresh_fields(fields: dict, *, ts=None, nonce=None) -> dict:
    """A NEW dict = ``fields`` plus the reserved freshness field ``_fresh``
    whose value is ``"<ts>|<nonce>"`` (ts RFC3339/ISO-8601 UTC seconds,
    nonce ``secrets.token_hex(16)``). ts/nonce default to freshly generated
    -- the ONLY place time and randomness enter; canonical_bytes stays pure.
    The input dict is never mutated, and a caller-supplied ``_fresh`` key is
    OVERWRITTEN, never merged (the reserved key cannot be spoofed)."""
    if ts is None:
        ts = _now_iso()
    if nonce is None:
        nonce = secrets.token_hex(16)
    out = dict(fields)
    out[FRESH_KEY] = f"{ts}|{nonce}"
    return out


def parse_ring_fresh(value) -> tuple | None:
    """Parse a `--ring-fresh <ts>|<nonce>` CLI argument into the (ts, nonce)
    pair a gate threads into fresh_fields(), or None when the flag is absent.
    Refuses a malformed value (one with no '|') by raising ValueError naming
    it -- a bad flag is never silently treated as "mint fresh" (that would
    make an out-of-process signer's bytes legally unmatchable and only fail
    hours later as a replay refusal instead of a parse error)."""
    if value is None:
        return None
    s = str(value)
    if "|" not in s:
        raise ValueError(
            f"--ring-fresh expects '<ts>|<nonce>', got {value!r} "
            "(e.g. '2026-09-12T16:45:56Z|0123abc...')")
    ts, nonce = s.split("|", 1)
    return ts, nonce


def render_ring_fields(kind: str, fields: dict, canonical: bytes | None = None) -> str:
    """The FOUR-LINE, parseable `--ring-fields` report for one decision: the
    kind, the EXACT fields dict as sorted JSON (so a reader sees precisely
    what is covered), and the canonical bytes the gate verifies BOTH as text
    (for a human) and as a hex line (for a machine -- a signer can
    ``bytes.fromhex(<hex>)`` and sign over exactly the bytes the gate checks,
    so the printed thing IS the verified thing; acceptance test D).

    This is a PERMANENT no-op on state: it only renders the bytes a real run
    would verify -- it never writes a ledger, never spawns, never demands a
    quorum (the signer's view, hyp...the-write-itself)."""
    import json as _json

    if canonical is None:
        canonical = canonical_bytes(kind, fields)
    return (
        f"ring-fields.kind: {kind}\n"
        f"ring-fields.json: {_json.dumps(fields, ensure_ascii=False, sort_keys=True)}\n"
        f"ring-canonical-bytes: {canonical.decode('utf-8')}\n"
        f"ring-canonical-hex: {canonical.hex()}"
    )


def _effective_max_age_s(ring: dict | None) -> int:
    """The per-ring replay window: the ring row's own ``max_age_s`` when
    present and coercible, else DEFAULT_MAX_AGE_S (rings are opt-in, so an
    over-lax row still degrades to the default window)."""
    if ring is None:
        return DEFAULT_MAX_AGE_S
    val = ring.get("max_age_s")
    try:
        return int(val) if val is not None else DEFAULT_MAX_AGE_S
    except (TypeError, ValueError):
        return DEFAULT_MAX_AGE_S


def freshness_refusal(fields: dict, *, max_age_s=DEFAULT_MAX_AGE_S,
                      now=None, seen=None, remember=None) -> str | None:
    """The by-name refusal for a record's freshness, or None to admit.

    Judges the ``_fresh`` field: absent / malformed / too old (past
    max_age_s) / too far in the future (clock-skew guard) / replayed nonce
    (a nonce already in ``seen``) -- each names exactly what is wrong, never
    a bare False. When the record is ADMITTED and ``remember`` is given, the
    nonce is handed to it only then, so a refused record never burns a
    nonce. ``now`` defaults to time.time() (unix epoch)."""
    if not isinstance(fields, dict) or FRESH_KEY not in fields:
        return ("carries no _fresh (ts|nonce) freshness field; refusing "
                "replay-by-age on a ring-authorized record")
    raw = fields[FRESH_KEY]
    s = str(raw)
    if "|" not in s:
        return f"malformed _fresh value {raw!r} (expected '<ts>|<nonce>')"
    ts, nonce = s.split("|", 1)
    parsed = _parse_ts(ts)
    if parsed is None:
        return f"unparseable _fresh timestamp {ts!r} in {raw!r}"
    nk = now if now is not None else time.time()
    age = nk - parsed
    if age > max_age_s:
        return (f"record is stale: age {age:.0f}s > window {max_age_s}s "
                f"(ts {ts})")
    if (parsed - nk) > MAX_FUTURE_SKEW_S:
        return (f"record carries a future _fresh timestamp: ts {ts} is "
                f"{parsed - nk:.0f}s ahead (clock-skew guard)")
    if seen is not None and nonce in seen:
        return (f"replayed nonce {nonce!r}: a record with this _fresh "
                "nonce was already admitted")
    if remember is not None:
        remember(nonce)
    return None


def _ledger_path(root) -> Path:
    """The admitted-nonce ledger path for a project: the shared sessions dir
    (``locations.shared_sessions_dir(root)``) plus NONCE_LEDGER_FILE, so a
    seat in a linked worktree reads/writes the SAME room the parent does.
    Imported lazily/defensively because rings.py lives under src/ while
    locations.py lives in bin/ (the bin scripts that put bin/ on sys.path
    already import it); if that import fails, fall back to
    ``<root>/sessions`` so a bare/off-tree caller still gets a sane path."""
    try:
        import locations  # type: ignore  # noqa: PLC0415

        base = Path(locations.shared_sessions_dir(root))  # type: ignore
    except Exception:  # noqa: BLE001
        base = Path(root) / "sessions"
    return base / NONCE_LEDGER_FILE


def nonce_ledger(root) -> tuple:
    """A (seen, remember) pair over the on-disk admitted-nonce ledger, a JSON
    list of {nonce, ts, kind}, re-read fresh on every call/query. An absent
    file reads as an empty seen set. remember() prunes entries older than 24h
    and appends the freshly admitted nonce; refused records never reach it.
    remember() RAISES LedgerWriteError (naming the ledger path and the
    underlying error) when the ledger cannot be written -- a nonce is never
    spent silently."""
    lpath = _ledger_path(root)

    def _read() -> list:
        try:
            import json as _json
            d = _json.loads(lpath.read_text(encoding="utf-8"))
            return d if isinstance(d, list) else []
        except Exception:  # noqa: BLE001
            return []

    def _fresh(entries: list) -> list:
        now = time.time()
        out = []
        for e in entries:
            if not isinstance(e, dict) or not e.get("nonce"):
                continue
            t = _parse_ts(e.get("ts"))
            if t is not None and (now - t) <= NONCE_LEDGER_TTL_S:
                out.append(e)
        return out

    def remember(nonce: str):
        import json as _json
        entries = _fresh(_read())
        entries.append({"nonce": nonce, "ts": _now_iso(), "kind": "fresh"})
        try:
            lpath.parent.mkdir(parents=True, exist_ok=True)
            lpath.write_text(_json.dumps(entries, indent=2, ensure_ascii=False),
                             encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            raise LedgerWriteError(
                f"could not write the nonce ledger at {lpath}: {exc} -- "
                "the admitted nonce was NOT remembered, so the decision is "
                "not admitted (a nonce is never spent silently)") from exc

    class _Seen:
        """A container whose __contains__ hits the ledger fresh each time."""

        def __contains__(self, item):
            return any(e.get("nonce") == item for e in _fresh(_read()))

    return _Seen(), remember


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
