#!/usr/bin/env python3
"""hierarchy.py — one source of truth for the command structure
(hypothesis:l3w4-hierarchy-one-source, goal:g17).

The command structure is declared EXACTLY ONCE, in machine-readable
frontmatter:

  * config:seats  (.agi/nodes/.geometry/seats.md)  `seats:`  — the instance
    registry. Authoritative for anything that HAS a seat.
  * ladder:ladder (.agi/nodes/.geometry/ladder.md) `roles:`  — the CLASS
    default table. Authoritative only where no seat exists.

`hierarchy.py render` emits THE chart from those two declarations and
nothing else. `hierarchy.py --check` is the drift checker: it exits zero on
the tree as it stands and nonzero, one line per violation, on every drift
class measured live on 2026-09-08. THIS FILE is the single reader; anything
that draws the seat/ladder structure (viewport's hierarchy layer, seat_status)
should read through it, so the graph and the human/llm renderings cannot
disagree the way the prose sources used to.

## Precedence (measured by sanctuary-master, verified here)

A seat row overrides the ladder (tier,role) class table, which overrides
config.harnesses. `dispatch.py resolve_seat_spec` (L538) says this verbatim.
So config:seats wins where a seat exists, ladder:ladder fills in where none
does. The word "role" is overloaded across two axes — a spawn-profile name
for `rotate.py spawn --tier` and a ladder role for dispatch — and `render`
states that rather than tidying it away.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "src"))  # graph_core package
from graph_core.persistence import frontmatter as _fm  # noqa: E402
import geometry_config as _gc  # noqa: E402

#: Session-named pins (`a00-<8 hex>`) belong to spawned agents, NOT to seats:
#: the brief says pi parents/kids were never granted seats. They were not
#: flagged as "seat with a pin and no row", which is a SEAT drift class.
_AGENT_PIN = re.compile(r"^a00-[0-9a-f]{8}$")

#: `rotated_by` may name a real seat row (sanctuary-master, master-sensei) or a
#: standing roleclass that is not itself a seat (the quorum, the prime). The
#: latter are legitimate and must not be flagged.
_ROLECLASS_ROTATORS = {"quorum", "prime"}

# Column tokens that identify each frontmatter list when the body carries a
# duplicate markdown table of it (class 6). Keyed by the list name returned by
# the node loader; value is the ordered header tokens used to align a body
# table's cells to a frontmatter row.
_TABLE_DEFS = {
    "roles": ("tier", "role", "harness", "model", "effort", "settings"),
    "tiers": ("tier", "plan_types", "report_type", "judged_against", "lens",
              "cadence"),
}


# --------------------------------------------------------------------------- #
# Loading (one reader: nothing re-reads the files)
# --------------------------------------------------------------------------- #
def load_seats(root: Path) -> list:
    """`config:posts`'s `posts:` rows (post-first, one-season config:seats
    fallback), or [] when absent. Shared resolver: geometry_config.load_rows."""
    return _gc.load_rows(root)


def load_ladder(root: Path) -> dict:
    """`ladder:ladder` frontmatter, or {} when absent."""
    p = Path(root) / "nodes" / ".geometry" / "ladder.md"
    if not p.is_file():
        return {}
    try:
        nf = _fm.load_node_file(p)
        return dict(nf.frontmatter or {})
    except Exception:                                                # noqa: BLE001
        return {}


def load_body(root: Path, node: str) -> str:
    """The body text of a `.geometry` node, or "" when absent."""
    p = Path(root) / "nodes" / ".geometry" / f"{node}.md"
    if not p.is_file():
        return ""
    try:
        return _fm.load_node_file(p).body or ""
    except Exception:                                                # noqa: BLE001
        return ""


def seat_sessions_dir(root: Path) -> Path:
    """The dir seats write their meter pins into: the SHARED sessions dir.

    Meter pins are ONE room across every git worktree (a seat in a worktree
    and the main checkout must read the same pin — the boundary face this
    whole cluster tracks). Routes through `locations.shared_sessions_dir`;
    a non-git root is the identity, so fixtures are unchanged."""
    import locations  # noqa: E402 (same bin dir; lazy to avoid import cycle)
    return locations.shared_sessions_dir(root)


# --------------------------------------------------------------------------- #
# Meter pin resolution (mirrors rotate.py's read path, never re-derived)
# --------------------------------------------------------------------------- #
def _pin_target(root: Path, name: str):
    """The resolved transcript a seat's pin names, or None (no pin / dead)."""
    pin = seat_sessions_dir(root) / f"{name}.meter"
    if not pin.is_file():
        return None
    try:
        raw = pin.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not raw:
        return None
    target = raw.partition("\t")[2].strip() if "\t" in raw else raw.strip()
    if not target:
        return None
    lp = Path(target).expanduser().resolve()
    return lp if lp.exists() else None


def _has_pin(root: Path, name: str) -> bool:
    return (seat_sessions_dir(root) / f"{name}.meter").is_file()


# --------------------------------------------------------------------------- #
# The six drift classes
# --------------------------------------------------------------------------- #
def check_orphan_pins(root: Path) -> list:
    """Class 1 — a seat pin with no seat row.

    A `.agi/sessions/<name>.meter` whose `<name>` is not a seat AND is not an
    agent-id pin is an orphan: nobody can meter, rotate or account for it.
    """
    out = []
    sdir = seat_sessions_dir(root)
    if not sdir.is_dir():
        return out
    names = {str(s.get("name", "")) for s in load_seats(root)}
    for pin in sorted(sdir.glob("*.meter")):
        stem = pin.stem
        if stem in names:
            continue
        if _AGENT_PIN.match(stem):
            continue
        out.append(f"orphan_pin: {stem}.meter has no seat row in config:seats")
    return out


def check_duplicate_transcripts(root: Path) -> list:
    """Class 2 — two rows whose pins resolve to the same transcript."""
    out = []
    seen = {}
    for s in load_seats(root):
        name = s.get("name")
        if not name:
            continue
        target = _pin_target(root, name)
        if target is None:
            continue
        if target in seen:
            out.append(
                f"duplicate_transcript: {seen[target]} and {name} both pin to "
                f"{target} — one will rotate on the other's number")
        else:
            seen[target] = name
    return out


def check_rotated_by(root: Path) -> list:
    """Class 3 — rotated_by naming a seat (or roleclass) that has no row."""
    out = []
    rows = load_seats(root)
    names = {str(s.get("name", "")) for s in rows}
    for s in rows:
        rb = str(s.get("rotated_by", "") or "").strip()
        if not rb:
            continue
        if rb in names or rb in _ROLECLASS_ROTATORS:
            continue
        out.append(f"rotated_by: {s.get('name')} names '{rb}', no such seat")
    return out


def check_director_kids(root: Path) -> list:
    """Class 4 — tier-1 director-kids above ladder caps.director_kids.

    A director-kid is (role==director AND tier==1 AND owning_goal non-empty),
    per the owner: "strictly for tier1 director-kids that own a specific
    perpetual goal". The owner's same-day correction that "a quorum seat owns
    no goal" is honoured by the counting predicate itself: quorum rows carry no
    owning_goal, so they never count.
    """
    out = []
    ladder = load_ladder(root)
    cap = ((ladder.get("caps") or {}).get("director_kids")
           if isinstance(ladder.get("caps"), dict) else None)
    if cap is None:
        return out
    hits = []
    for s in load_seats(root):
        if (str(s.get("role", "")) == "director"
                and int(s.get("tier", -1)) == 1
                and str(s.get("owning_goal", "") or "").strip()):
            hits.append(s.get("name"))
    if len(hits) > int(cap):
        out.append(
            f"director_kids: {len(hits)} director-kids ({', '.join(sorted(hits))}) "
            f"above caps.director_kids={cap}")
    return out


def check_unresolved(root: Path) -> list:
    """Class 5 — a seat row whose (tier,role) has no ladder row AND no model."""
    out = []
    ladder = load_ladder(root)
    classes = {
        (int(r.get("tier", -1)), str(r.get("role", "")))
        for r in ladder.get("roles") or [] if isinstance(r, dict)
    }
    for s in load_seats(root):
        key = (int(s.get("tier", -1)), str(s.get("role", "")))
        if key in classes:
            continue
        if str(s.get("model", "") or "").strip() and str(s.get("harness", "")):
            continue  # seat-level model resolves it directly
        out.append(
            f"unresolved: seat {s.get('name')} (tier {key[0]}, role {key[1]}) "
            f"has no ladder row and no seat-level model")
    return out


def _is_separator(line: str) -> bool:
    """True when a pipe row is an alignment separator (``|--|:--|``)."""
    cells = _split_cells(line)
    return bool(cells) and all(
        set(c) <= {"-", ":", " "} for c in cells)


def _markdown_tables(body: str) -> list:
    """Split a body into markdown pipe tables (list of line-lists).

    Consecutive pipe rows form one table; a bare non-pipe line ends it. The
    ``|--|--|`` alignment separator row is kept inside the table and stripped
    by the consumer, so it never fragments a table into single-row stubs nor
    leaks through as a fake data row.
    """
    tables, cur = [], []
    for line in body.splitlines():
        if re.match(r"^\s*\|.*\|\s*$", line):
            cur.append(line.strip())
        elif cur:
            tables.append(cur)
            cur = []
    if cur:
        tables.append(cur)
    kept = []
    for t in tables:
        nonsep = [r for r in t if not _is_separator(r)]
        if len(nonsep) >= 2:
            kept.append(nonsep)
    return kept


def _split_cells(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def check_body_tables(root: Path) -> list:
    """Class 6 — a body table whose cells disagree with its own frontmatter.

    A hand-maintained table in a node body is a lie the moment the frontmatter
    moves. For each `.geometry` body that owns a `roles:`/`tiers:` list, any
    pipe table whose header matches that list's tokens is aligned row by row to
    the frontmatter rows by the leading key columns, and every shared column is
    compared. A table that cannot be aligned (different shape) is left silent
    rather than guessed at — the class is about tables that DISAGREE with the
    frontmatter, not about tables we cannot parse.
    """
    out = []
    # the fields live in node files whose names differ from the field names:
    # both `roles:` and `tiers:` are declared in ladder.md.
    node_file = {"roles": "ladder", "tiers": "ladder",
                 "seats": "seats"}.get
    for node, columns in _TABLE_DEFS.items():
        body = load_body(root, node_file(node))
        if not body:
            continue
        fm_rows = load_ladder(root).get(node) or []
        if node == "seats":
            fm_rows = load_seats(root)
        fm_by_key = {
            tuple(str(r.get(c, "")) for c in columns[:2]): r
            for r in fm_rows if isinstance(r, dict)
        }
        if not fm_by_key:
            continue
        for table in _markdown_tables(body):
            if len(table) < 2:
                continue
            header = _split_cells(table[0])
            if not all(h.lower() in columns for h in header if h):
                continue
            # position -> token for shared columns; the first two are the key
            tok_at = {i: t.lower() for i, t in enumerate(header)
                      if t.lower() in columns}
            key_cols = [i for i in range(len(header)) if i in tok_at]
            for row in table[1:]:
                cells = _split_cells(row)
                if len(cells) < 2:
                    continue
                key = tuple(
                    cells[i] if i < len(cells) else "" for i in key_cols[:2])
                row = fm_by_key.get(tuple(key))
                if row is None:
                    out.append(
                        f"body_table: {node} prose row {cells} has no "
                        f"frontmatter (tier,role)={key}")
                    continue
                for i, tok in tok_at.items():
                    if i >= len(cells):
                        continue
                    want = str(row.get(tok, "") or "")
                    if want and cells[i] != want:
                        out.append(
                            f"body_table: {node} prose {tok}={cells[i]!r} "
                            f"disagrees with frontmatter {tok}={want!r} "
                            f"for (tier,role)={key}")
    return out


# --------------------------------------------------------------------------- #
# Class 7 & 8 — the role card grammar and the decides.writes join
# (hypothesis:l4-card-grammar-and-the-written-by-join)
#
# A CARD is a `seat` node under nodes/seat/ (the plan's migration target under
# goal:g17) whose frontmatter carries the typed duty slice: what/where/cost/to/
# trigger/channel/options/decides/writes. CLASS 7 is the per-field grammar;
# CLASS 8 is the join from decides.writes back to the written-by type.
#
# WHERE THE MATRIX LIVES: the duty caps (at most 2 reads, at most 2 tells,
# exactly 1 decides) are Belam XVI's input (plan §2 -> "at most 2 / at most 2 /
# exactly 1"). A card may override them via `caps: {tracks, tells}` on the
# ladder frontmatter, so "the matrix as declared" is the ladder's own numbers.
# THE ASYMMETRY IS A REQUIREMENT: declaring MORE than the matrix allows REFUSES
# (a violation, exit nonzero); declaring FEWER WARNS and exits ZERO.
#
# CARD VALIDATION LIVES HERE, IN hierarchy.py, DELIBERATELY NOT IN write_guard.py
# -- whose whole decision is byte identity. This is a recorded deviation from
# the prime's own earlier position (A:152). written_by is read through the
# shared links.parse_written_by parser, never a second one (goal:s17); .where
# resolves through links.link_path, never a second resolver.
# --------------------------------------------------------------------------- #
from dataclasses import dataclass, field

# `wake` IS DELIBERATELY ABSENT from .cost: a track that needs another session
# to answer is polling, and polling rebuilds the chatter the owner removed.
_CLOSED_COST = {"read", "run"}
# `brief` IS NOT IN THIS SET AND DOES NOT EXIST (A:162): a card naming it is a
# violation, and the validator must not add it.
_CLOSED_CHANNEL = {"dm", "room", "ask", "report", "escalate", "audience",
                   "vote"}
# staccato is trigger-bound: a cadence-looking trigger is a violation.
_CADENCE_RE = re.compile(r"every|hourly|daily|periodic", re.I)
_DEF_TRACKS = 2
_DEF_TELLS = 2


@dataclass
class _CheckResult:
    """Card checkers can both refuse (violations) and warn (fewer than the
    matrix). Classes 1-6 return plain lists and stay untouched."""
    violations: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


def _matrix_caps(ladder: dict) -> tuple[int, int]:
    caps = ladder.get("caps") if isinstance(ladder.get("caps"), dict) else {}
    t = int(caps.get("tracks", _DEF_TRACKS))
    tl = int(caps.get("tells", _DEF_TELLS))
    return t, tl


def load_cards(root: Path) -> list:
    """The `seat` card nodes under nodes/seat/, each with its frontmatter."""
    d = Path(root) / "nodes" / "seat"
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("*.md")):
        try:
            nf = _fm.load_node_file(p)
            fm = dict(nf.frontmatter or {})
        except Exception:                                              # noqa: BLE001
            continue
        out.append((p.stem, fm))
    return out


def check_card_grammar(root: Path):
    """Class 7 — per-field card grammar. MORE than the matrix refuses;
    FEWER warns. wake/brief/cadence-lint each refuse by reason."""
    res = _CheckResult()
    cards = load_cards(root)
    if not cards:
        return res
    ladder = load_ladder(root)
    track_cap, tell_cap = _matrix_caps(ladder)
    from links import link_path  # the EXISTING resolver, never a second one
    roles = {str(r.get("role", "")) for r in ladder.get("roles") or []
             if isinstance(r, dict)}
    seats = {str(s.get("name", "")) for s in load_seats(root)}
    known_targets = {x for x in (roles | seats) if x}

    for cid, c in cards:
        def row_v(field, msg):
            return f"card_grammar[{field}]: {cid} {msg}"
        # .what — at most 80 chars
        what = str(c.get("what", "") or "")
        if len(what) > 80:
            res.violations.append(row_v("what", f"is {len(what)} chars, over 80"))
        # .where — resolves through the EXISTING links.py resolver
        where = str(c.get("where", "") or "").strip()
        if where:
            try:
                p = link_path(root, where)
            except Exception:                                          # noqa: BLE001
                p = None
            if p is None or not p.exists():
                res.violations.append(row_v(
                    "where", f"'{where}' does not resolve (broken_links must stay 0)"))
        # .cost — CLOSED to {read, run}; wake deliberately absent
        cost = str(c.get("cost", "") or "").strip().lower()
        if cost and cost not in _CLOSED_COST:
            res.violations.append(row_v(
                "cost", f"'{cost}' not in {{read, run}}; `wake` is deliberately absent"))
        # .to — a ladder role or a registered seat, FAIL-CLOSED
        to = str(c.get("to", "") or "").strip()
        if to and to not in known_targets:
            res.violations.append(row_v(
                "to", f"names '{to}', not a ladder role or registered seat (fail-closed)"))
        # .trigger — an EVENT; cadence lint refuses /every|hourly|daily|periodic/i
        trig = str(c.get("trigger", "") or "")
        if trig and _CADENCE_RE.search(trig):
            res.violations.append(row_v(
                "trigger", f"'{trig}' looks like a cadence, not an event "
                            f"(staccato is trigger-bound)"))
        # .channel — CLOSED set; brief is NOT in it and does not exist
        ch = str(c.get("channel", "") or "").strip().lower()
        if ch and ch not in _CLOSED_CHANNEL:
            res.violations.append(row_v(
                "channel", f"'{ch}' not in {{dm,room,ask,report,escalate,"
                            f"audience,vote}}; `brief` does not exist"))
        # options 2-4 lowercase CLOSED tokens
        opts = c.get("options")
        if isinstance(opts, list) and opts:
            if not (2 <= len(opts) <= 4):
                res.violations.append(row_v(
                    "options", f"has {len(opts)} options, must be 2-4"))
            bad = [o for o in opts if str(o) != str(o).lower()]
            if bad:
                res.violations.append(row_v(
                    "options", f"must be lowercase closed tokens, found {bad}"))
        # decides — EXACTLY ONE (the owner's sentence is singular)
        dec = c.get("decides")
        if dec is None:
            res.warnings.append(row_v("decides", "declares none (matrix wants exactly 1)"))
        elif isinstance(dec, (list, tuple, set)) or "," in str(dec) or ";" in str(dec):
            res.violations.append(row_v(
                "decides", "must be EXACTLY ONE decision, got more than one"))
        # THE ASYMMETRY (MORE refuses, FEWER warns)
        tracks = c.get("tracks") or []
        tells = c.get("tells") or []
        if isinstance(tracks, list) and len(tracks) > track_cap:
            res.violations.append(row_v(
                "tracks", f"{len(tracks)} tracks > matrix cap {track_cap} (MORE refuses)"))
        elif isinstance(tracks, list) and tracks and len(tracks) < track_cap:
            res.warnings.append(row_v(
                "tracks", f"{len(tracks)} tracks < matrix cap {track_cap} (fewer warns)"))
        if isinstance(tells, list) and len(tells) > tell_cap:
            res.violations.append(row_v(
                "tells", f"{len(tells)} tells > matrix cap {tell_cap} (MORE refuses)"))
        elif isinstance(tells, list) and tells and len(tells) < tell_cap:
            res.warnings.append(row_v(
                "tells", f"{len(tells)} tells < matrix cap {tell_cap} (fewer warns)"))
    return res


def _type_written_by(root: Path, ntype: str):
    """(admitted, seat_predicate) for a node type's schema, read through the
    SHARED links.parse_written_by — never a second parser."""
    from links import parse_written_by
    p = Path(root) / "context" / "schemas" / f"[{ntype}].md"
    if not p.is_file():
        return None, None
    try:
        nf = _fm.load_node_file(p)
    except Exception:                                                  # noqa: BLE001
        return None, None
    fm = nf.frontmatter or {}
    admitted = parse_written_by(fm.get("written_by"))
    pred = fm.get("seat_predicate")
    return admitted, (str(pred) if pred not in (None, "") else None)


_PRED_NS = {"__builtins__": {"True": True, "False": False, "None": None}}


def check_written_by_join(root: Path):
    """Class 8 — the §1↔§2 join: a card whose decides.writes names a type must
    have THAT type's written_by admit this row's role AND satisfy its
    seat_predicate. The parse is links.parse_written_by, the one the write
    enforcer already uses, so a list or comma value reads one way."""
    res = _CheckResult()
    for cid, c in load_cards(root):
        writes = c.get("writes")
        if writes in (None, "", "none"):
            continue
        ntype = writes if isinstance(writes, str) else ",".join(writes)
        ntype = ntype.strip()
        if not ntype or ntype == "none":
            continue
        if "," in ntype or " " in ntype:
            res.violations.append(
                f"written_by_join: {cid} decides.writes names more than one type "
                f"('{ntype}') — must be one type, a chain, or none")
            continue
        admitted, pred = _type_written_by(root, ntype)
        if admitted is None:
            continue  # type declares no written_by -> gates nothing
        role = str(c.get("role", "") or cid)
        if role not in admitted:
            res.violations.append(
                f"written_by_join: {cid} role '{role}' writes {ntype}, but "
                f"[{ntype}] written_by admits {{ {', '.join(sorted(admitted))} }}")
            continue
        if pred is not None:
            try:
                ok = bool(eval(pred, _PRED_NS, {"role": role, "card": c}))   # noqa: S307
            except Exception:                                          # noqa: BLE001
                ok = False
            if not ok:
                res.violations.append(
                    f"written_by_join: {cid} fails [{ntype}] seat_predicate "
                    f"'{pred}' for role '{role}'")
    return res


# --------------------------------------------------------------------------- #
# Checker driver
# --------------------------------------------------------------------------- #
CHECKERS = [
    ("orphan_pin", check_orphan_pins),
    ("duplicate_transcript", check_duplicate_transcripts),
    ("rotated_by", check_rotated_by),
    ("director_kids", check_director_kids),
    ("unresolved", check_unresolved),
    ("body_table", check_body_tables),
    ("card_grammar", check_card_grammar),
    ("written_by_join", check_written_by_join),
]


def run_check(root: Path):
    """(violations, warnings) on `root`, ordered by class then message.

    Classes 1-6 return plain lists and are wired as before; classes 7-8 return
    _CheckResult so a card can warn (fewer than the matrix) without flipping
    the exit code while still refusing (more than the matrix)."""
    v = []
    w = []
    for _name, fn in CHECKERS:
        r = fn(root)
        if isinstance(r, _CheckResult):
            v.extend(r.violations)
            w.extend(r.warnings)
        else:
            v.extend(r)
    return v, w


# --------------------------------------------------------------------------- #
# Render — THE chart from the two declarations only
# --------------------------------------------------------------------------- #
def render(root: Path) -> str:
    seats = load_seats(root)
    ladder = load_ladder(root)
    roles = ladder.get("roles") or []
    lines = []
    lines.append("COMMAND HIERARCHY — one source of truth (config:seats + "
                 "ladder:ladder frontmatter only)")
    lines.append("")
    lines.append("SEATS — instance registry, authoritative where a seat exists")
    lines.append("| seat | tier | role | model | effort | harness | session_kind"
                 " | rotated_by | owns_goal | live |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for s in seats:
        name = s.get("name", "?")
        lines.append(
            f"| {name} | {s.get('tier', '')} | {s.get('role', '')} "
            f"| {s.get('model', '')} | {s.get('effort', '')} "
            f"| {s.get('harness', '')} | {s.get('session_kind', '')} "
            f"| {s.get('rotated_by', '')} | {s.get('owning_goal') or ''} "
            f"| {'yes' if _has_pin(root, name) else 'no'} |")
    lines.append("")
    lines.append("LADDER classes — (tier, role) defaults, "
                 "applied ONLY where no seat exists")
    lines.append("| tier | role | harness | model | effort | settings |")
    lines.append("|---|---|---|---|---|---|")
    for r in roles if isinstance(roles, list) else []:
        lines.append(
            f"| {r.get('tier', '')} | {r.get('role', '')} "
            f"| {r.get('harness', '')} | {r.get('model', '')} "
            f"| {r.get('effort', '')} | {r.get('settings', '')} |")
    lines.append("")
    # hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council — the
    # reporting chain, derived from the ladder's `towns:` list and the
    # council-role rows in config:seats (none exist yet): Core Council ->
    # Prime, every other town's Council -> Core Council. A declared town with
    # no council seat renders as UNSEATED, never as an absent edge; with no
    # Core Council seat at all, the Prime IS the Core Council for the other
    # towns (rendered as such, never a missing edge).
    raw_towns = ladder.get("towns") or []
    declared = [str(t).strip() for t in raw_towns
                if isinstance(t, str) and t.strip()] or ["core"]
    councils = [s for s in seats
                if str(s.get("role") or "").strip() == "council"]
    council_town = {}
    for c in councils:
        t = str(c.get("town") or "").strip() or "core"
        council_town.setdefault(t, str(c.get("name") or "?"))
    lines.append("TOWN COUNCILS — reporting chain "
                 "(hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council)")
    lines.append("| town | council | reports_to |")
    lines.append("|---|---|---|")
    for t in declared:
        reports = "Prime" if t == "core" else "Core Council"
        if t == "core" and t not in council_town:
            # No Core Council seat — the Prime plays it. Rendered as such,
            # never as a missing edge.
            lines.append(f"| {t} | Prime (as Core Council) | Prime |")
        elif t in council_town:
            lines.append(f"| {t} | {council_town[t]} | {reports} |")
        else:
            # A declared town with no council seat renders as unseated rather
            # than inventing a row.
            lines.append(f"| {t} | ? (unseated) | {reports} |")
    lines.append("")
    lines.append("Chain: Core Council -> Prime; every other town's Council -> "
                 "Core Council. A council is a seat row with `role: council` and "
                 "a `town:` cell; absent one the town's council is unseated, and "
                 "with no core council seat the Prime plays it (never a missing "
                 "edge).")
    lines.append("")
    lines.append("PRECEDENCE (dispatch.py resolve_seat_spec): seat row overrides "
                 "'(tier,role)' class overrides config.harnesses. The word 'role' "
                 "is overloaded across two axes — a rotate.py spawn --tier profile "
                 "name and a ladder role for dispatch. Both are true.")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _resolve_root(arg: str | None) -> Path:
    if arg:
        return Path(arg).resolve()
    import locations
    root = locations.find_project_root()
    if root is None:
        raise SystemExit("hierarchy.py: could not resolve project root "
                         "(no .agi/config.json found). Pass --root.")
    return root


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="hierarchy.py")
    ap.add_argument("mode", nargs="?", choices=["render"],
                    help="'render' prints THE chart; omit for --check-style")
    ap.add_argument("--root", default=None, help="graph root (default: resolve)")
    ap.add_argument("--check", action="store_true",
                    help="run the drift checker, exit nonzero on violations")
    args = ap.parse_args(argv)

    root = _resolve_root(args.root)
    do_check = args.check or args.mode != "render"
    if args.mode == "render":
        sys.stdout.write(render(root))
        return 0  # render never fails the run

    violations, warnings = run_check(root)
    if violations:
        print("\n".join(violations))
        print(f"\nhierarchy.py --check: {len(violations)} violation(s).")
        return 1
    if warnings:
        print("\n".join(warnings))
        print(f"\nhierarchy.py --check: clean but {len(warnings)} warning(s) "
              f"(fewer than the matrix declares).")
        return 0
    print("hierarchy.py --check: clean — every seat accounted, no drift.")
    return 0


if __name__ == "__main__":
    sys.exit(main())