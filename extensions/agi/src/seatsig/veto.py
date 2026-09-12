"""seatsig.veto -- the rung-3 HUMAN GATE: a council+Keep majority can freeze a
Prime-scope gated act with an EXPIRING, RATE-LIMITED, LOGGED veto; an
UNANSWERED gate freezes, never frees.

RUNG 3 of the owner's eight-rung multisig ladder
(hypothesis:l4-a-veto-freezes-never-frees, town all; serial behind rung 2).
The unit of authority is a rings DECISION CELL (rung 2's shape) of kind
``veto``: the council+Keep majority that vetoes is an m-of-n quorum over the
FULL veto decision fields, verified by ``rings.verify_decision`` -- never new
crypto, and never a bare boolean. A veto below quorum is a minority and does
nothing; a veto past its expiry is INERT; a scope may be vetoed at most
``rate_limit_per_window`` times per ``window_seconds`` (the N+1th is refused);
and every veto/expiry/answer is logged to ONE geometry node.

ONCE A GATE IS SET IT STAYS FROZEN UNTIL AN OWNER ANSWERS. The freeze lives
in shared geometry state (``active_gates``), not in an actor, a pid or a
process, so a timeout, a restart or a rotation NEVER auto-releases it: the
only thing that clears an active gate is a recorded owner answer in the same
node. A held veto's OWN expiry only says it can no longer SET a fresh gate; it
does not and must not free a gate it already set.

Geometry cell (the "one geometry node for rate limits/expiry", the log):

    veto_room: veto            # the named room an owner answers in (send.py)
    rate_limit_per_window: 2   # at most N vetoes per scope per window
    window_seconds: 3600
    expiry_seconds: 86400      # a veto older than this (that has not already
                               # set a gate and been answered) is INERT
    active_gates:              # the human_gate state: what stays frozen
      - scope: prime
        since: "2026-09-12T00:00:00Z"
        reason: "<short human reason>"
        veto_ref: "veto:001"
        answered: ""           # an owner answer clears the gate (never empty
                               # while frozen)
    vetoes:                    # the log -- every veto/expiry/answer, one file
      - veto_ref: veto:001
        scope: prime
        filed_at: "2026-09-12T00:00:00Z"
        expires_at: "2026-09-12T00:00:00Z"
        answer: ""             # filled when the owner answers / an expiry note

RINGS ARE OPT-IN, and so is THIS GATE: a scope with no VETOES cell, or an
``active_gates`` list with no matching entry, is free. The gate seams
(write.py's config-edit gate, verification.py's merge-up push, rotate.py's
other-post rotation, viewport.py --live) call :func:`is_frozen` and refuse BY
NAME a gated act while the scope is frozen.

The decision functions below are pure (dict in, dict out) so they are
fixture-testable without touching the real posts/seats tree: a geometry dict
is handed in, a new geometry dict comes back. :func:`read` and :func:`save`
bridge a real tree through the engine's own node loader/writer (the SAME
loader rings.py reads through) so an integration gate reads live state, but
no test ever writes to the real tree.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import seatsig  # noqa: F401  (guarantees the engine spelling, mur-39 (e))
from seatsig import rings

#: The one geometry node the vetoes/human-gate state lives in
#: (`<root>/nodes/.geometry/vetoes.md`). Sibling of the rings.md cell.
VETOES_CELL = Path("nodes") / ".geometry" / "vetoes.md"

#: Defaults -- a VETOES cell that omits a key degrades to these, so an
#: absent cell reads as a free tree and an over-lax one still bounds.
_DEFAULTS = {
    "veto_room": "veto",
    "rate_limit_per_window": 1,
    "window_seconds": 3600,
    "expiry_seconds": 86400,
    "active_gates": [],
    "vetoes": [],
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_iso(value) -> datetime | None:
    """Parse an ISO-8601 timestamp back for expiry arithmetic, or None when
    unparseable (an unparseable expiry is treated as INERT -- never a durable
    freeze)."""
    if not value:
        return None
    s = str(value)
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def read(root, path: Path | None = None) -> dict:
    """The VETOES geometry node state as a plain dict (never mode).

    ``root`` may be a graph root (the ``.agi``/config dir) or None; an absent
    or unparseable cell reads as the defaults (a free tree). Read through the
    SAME engine loader rings.py uses -- never a hand-rolled frontmatter read.
    """
    out = dict(_DEFAULTS)
    # Copy the LIST defaults so no caller can mutate the module-level shared
    # list and pollute every later read (a real once -- a frozen-geometry
    # default leaked into every write-gate gate in a shared pytest process).
    out["active_gates"] = [dict(g) for g in _DEFAULTS["active_gates"]]
    out["vetoes"] = [dict(v) for v in _DEFAULTS["vetoes"]]
    if root is None:
        return out
    cell = Path(root) / (path or VETOES_CELL)
    if not cell.is_file():
        return out
    try:
        from graph_core.persistence import frontmatter

        nf = frontmatter.load_node_file(cell)
        for key in _DEFAULTS:
            if key in nf.frontmatter:
                out[key] = nf.frontmatter[key]
    except Exception:  # noqa: BLE001  (an unreadable cell is an absent cell)
        pass
    if not isinstance(out.get("active_gates"), list):
        out["active_gates"] = []
    if not isinstance(out.get("vetoes"), list):
        out["vetoes"] = []
    return out


def active_gate(geom: dict, scope: str) -> dict | None:
    """The current active human-gate entry for ``scope``, or None.

    "Current" means it is in ``active_gates`` AND its ``answered`` cell is
    empty. A scope with no such entry is FREE. This is the whole freeze
    test -- :func:`is_frozen` is a thin wrapper over it for the seams.
    """
    for gate in geom.get("active_gates") or []:
        if isinstance(gate, dict) and gate.get("scope") == scope \
                and not gate.get("answered"):
            return gate
    return None


def is_frozen(root, scope: str, geom: dict | None = None,
              now=None, path: Path | None = None):
    """The gate seam: (frozen: bool, reason: str) for ``scope`` today.

    Frozen iff the VETOES geometry node currently records an ACTIVE
    (unanswered) gate for ``scope``. There is deliberately NO notion of
    "the freeze expired": only an owner answer clears an active gate (a
    timeout, a restart or a rotation must never auto-free -- the claim). An
    expiry governs only whether a veto can SET a fresh gate, handled by
    :func:`evaluate_veto`, not whether a set gate frees.
    """
    g = geom if geom is not None else read(root, path)
    gate = active_gate(g, scope)
    if gate is None:
        return False, f"scope {scope!r} is not under a human gate"
    return True, (
        f"{scope!r} is FROZEN by a human gate (veto {gate.get('veto_ref')}) "
        f"since {gate.get('since')}; it is never auto-released -- only an "
        f"owner answer in {g.get('veto_room')!r} clears it"
    )


def _vetoes_in_window(geom: dict, scope: str, now) -> list:
    """The filed vetoes for ``scope`` whose ``filed_at`` falls inside the
    current ``window_seconds`` -- the set the rate limit counts."""
    limit = int(geom.get("window_seconds") or 0)
    entries = []
    for v in geom.get("vetoes") or []:
        if not isinstance(v, dict) or v.get("scope") != scope:
            continue
        filed = _parse_iso(v.get("filed_at"))
        if filed is None:
            continue
        if limit <= 0 or (now - filed).total_seconds() <= limit:
            entries.append(v)
    return entries


def rate_refusal(geom: dict, scope: str, now=None) -> str | None:
    """The rate-limit refusal for a NEW veto on ``scope``, or None if the
    veto may be filed (under the limit). Called BEFORE the quorum evidence
    is even weighed so the N+1th is refused by name."""
    limit = int(geom.get("rate_limit_per_window") or 0)
    if limit <= 0:
        return None  # an unbounded cell binds nothing
    if len(_vetoes_in_window(geom, scope, now)) >= limit:
        return (
            f"scope {scope!r} may be vetoed at most {limit} "
            f"time(s) per {geom.get('window_seconds')}s window "
            f"(rate-limited by the vetoes geometry node); the "
            f"{limit + 1}th is refused"
        )
    return None


def veto_fields(scope: str, reason: str,
                expires_at: str | None = None) -> dict:
    """The canonical VETO decision fields a veto's signatures cover (the
    same fields on the file and the read side, so verify_decision recomputes
    the exact canonical bytes). ``expires_at`` is an ISO timestamp; when
    omitted, :func:`evaluate_veto` derives it from expiry_seconds -- the
    caller keeps ONE spelling so an unexpired veto cannot be relabelled as
    inert by an inconsistent field."""
    f = {"scope": scope, "reason": reason, "kind": "veto"}
    if expires_at is not None:
        f["expires_at"] = expires_at
    return f


def _effective_expiry(fields: dict, geom: dict, now) -> datetime | None:
    """The veto's effective authority expiry: an explicit ``expires_at``
    field the signatures covered, ELSE now + the cell's ``expiry_seconds``
    (a just-filed veto without an explicit window is live for the whole
    default window). None when neither path yields a timestamp."""
    explicit = fields.get("expires_at")
    if explicit:
        return _parse_iso(explicit)
    exp = int(geom.get("expiry_seconds") or 0)
    if exp <= 0:
        return None
    import datetime as _dt

    base = now if getattr(now, "tzinfo", None) else _now_dt()
    return base + _dt.timedelta(seconds=exp)


def _now_dt() -> datetime:
    return datetime.now(timezone.utc)


def veto_expired(fields: dict, geom: dict, now) -> bool:
    """True when the veto decision's authority window has passed -- it is
    INERT and can no longer SET a gate. Uses the effective expiry: an
    explicit ``expires_at`` field the signatures covered, else the cell's
    ``expiry_seconds``. An explicit timestamp that does not parse reads as
    expired (fail-closed: never a durable freeze from a malformed veto)."""
    explicit = fields.get("expires_at")
    if explicit is not None:
        parsed = _parse_iso(explicit)
        if parsed is None:
            return True
        return now > parsed
    exp = int(geom.get("expiry_seconds") or 0)
    if exp <= 0:
        return True
    return False  # a just-filed veto derives the full default window


def evaluate_veto(geom: dict, scope: str, decision: dict, *,
                  ring: dict | None, pubkey_for_post=None,
                  now=None) -> tuple[str | None, dict]:
    """Decide a FILED veto decision against the geometry state.

    ``decision`` is a rings DECISION CELL (kind ``veto``, fields the
    signatures covered, signatures) from a council+Keep majority. Verifies
    the quorum through ``rings.verify_decision`` (m-of-n over the FULL veto
    fields -- never our own crypto), then applies expiry and rate-limit.
    Returns ``(reason, new_geom)`` where ``reason`` is None when the veto
    is ACCEPTED (the gate is set) and is the by-name refusal otherwise.

    A veto FREEZES only when ALL hold: quorum satisfied (majority), not
    expired, and under the per-window rate limit. A minority veto, an
    expired veto, or the N+1th is refused and never sets a gate. On accept
    the veto is logged and an ``active_gates`` freeze entry for ``scope`` is
    created with an EMPTY ``answered`` -- from this point only an owner
    answer frees it (see :func:`record_answer`).
    """
    now = now or datetime.now(timezone.utc)

    # 1. quorum: a council+Keep majority is m-of-n over the veto fields.
    if ring is None:
        return ("no council+Keep ring is declared for a veto; the veto is "
                "refused (rings are opt-in, a no-ring veto gates nothing)",
                dict(geom))
    res = rings.verify_decision(decision, ring, pubkey_for_post=pubkey_for_post)
    if not res.ok:
        return (f"minority veto refused: {res.summary()}", dict(geom))

    # 2. rate limit: the N+1th is refused before it can set anything.
    rl = rate_refusal(geom, scope, now)
    if rl:
        return (rl, dict(geom))

    # 3. expiry: a veto past its authority window is inert.
    fields = dict(decision.get("fields") or {})
    if veto_expired(fields, geom, now):
        return (f"expired veto is inert for scope {scope!r}: its authority "
                f"window passed and it cannot set a gate", dict(geom))

    # ACCEPT: log the veto and set (or keep) an active freeze on the scope.
    new = dict(geom)
    new["vetoes"] = [dict(v) for v in new.get("vetoes") or []]
    new["active_gates"] = [dict(g) for g in new.get("active_gates") or []]
    ref = f"veto:{len(new['vetoes']) + 1:03d}"
    expires = fields.get("expires_at") or _now_iso()
    new["vetoes"].append({
        "veto_ref": ref, "scope": scope, "filed_at": _now_iso(),
        "expires_at": expires, "answer": "",
    })
    # keep ONE active freeze per scope: an accepted veto on a scope already
    # frozen stays frozen and just re-logs (never a stacked freeze to clear).
    existing = active_gate(new, scope)
    if existing is None:
        new["active_gates"].append({
            "scope": scope, "since": _now_iso(),
            "reason": fields.get("reason") or "council+Keep majority veto",
            "veto_ref": ref, "answered": "",
        })
    return (None, new)


def record_answer(geom: dict, scope: str, answer: str) -> dict:
    """An OWNER ANSWER clears the freeze on ``scope`` -- the ONLY thing that
    does. Fills the gate's ``answered`` cell AND the latest veto's ``answer``
    so the log carries the whole lifecycle (filed -> frozen -> answered)."""
    new = dict(geom)
    new["active_gates"] = []
    for gate in geom.get("active_gates") or []:
        g = dict(gate)
        if g.get("scope") == scope:
            g["answered"] = answer
        else:
            new["active_gates"].append(g)  # drop the answered scope
    new["vetoes"] = []
    for v in geom.get("vetoes") or []:
        e = dict(v)
        if e.get("scope") == scope and not e.get("answer"):
            e["answer"] = answer
        new["vetoes"].append(e)
    return new


def save(root, geom: dict, path: Path | None = None) -> Path:
    """Persist the geometry state to the VETOES node (the ONE log file).

    Integration gates write through this; no test calls it against the real
    tree. Writes through graph_core's node writer so the round-trip is the
    same loader rings/veto read on the way out and in."""
    cell = Path(root) / (path or VETOES_CELL)
    cell.parent.mkdir(parents=True, exist_ok=True)
    try:
        from graph_core.persistence import frontmatter

        fm = dict(_DEFAULTS) if not cell.is_file() else \
            frontmatter.load_node_file(cell).frontmatter
        for key in _DEFAULTS:
            fm[key] = geom.get(key, _DEFAULTS[key])
        fm["id"] = "config:vetoes"
        fm["type"] = "config"
        fm["edited_by"] = fm.get("edited_by", "belam")
        fm["parents"] = fm.get("parents") or ["goal:g15"]
        out = "---\n" + _dump_yaml(fm) + "---\n"
        cell.write_text(out, encoding="utf-8")
    except Exception:  # noqa: BLE001  (never make the save crash a gate)
        raise
    return cell


def _dump_yaml(fm: dict) -> str:
    """Minimal YAML-ish serialization for the toString frontmatter the loader
    round-trips (keys sorted, rows as JSON). Kept local so save() needs no
    yaml dependency the engine does not already carry."""
    import json as _json

    lines = []
    for key, value in sorted(fm.items()):
        if isinstance(value, (list, dict)):
            lines.append(f"{key}:")
            for row in value:
                lines.append(f"  - {_json.dumps(row, sort_keys=True)}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"