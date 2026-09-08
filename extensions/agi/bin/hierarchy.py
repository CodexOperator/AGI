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
    """`config:seats`'s `seats:` rows, or [] when absent."""
    p = Path(root) / "nodes" / ".geometry" / "seats.md"
    if not p.is_file():
        return []
    try:
        nf = _fm.load_node_file(p)
        rows = (nf.frontmatter or {}).get("seats") or []
        return [dict(r) for r in rows if isinstance(r, dict)]
    except Exception:                                                # noqa: BLE001
        return []


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
    """The dir seats write their meter pins into: `<graph root>/sessions`."""
    return Path(root) / "sessions"


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
# Checker driver
# --------------------------------------------------------------------------- #
CHECKERS = [
    ("orphan_pin", check_orphan_pins),
    ("duplicate_transcript", check_duplicate_transcripts),
    ("rotated_by", check_rotated_by),
    ("director_kids", check_director_kids),
    ("unresolved", check_unresolved),
    ("body_table", check_body_tables),
]


def run_check(root: Path) -> list:
    """All violations on `root`, ordered by class then message."""
    out = []
    for _name, fn in CHECKERS:
        out.extend(fn(root))
    return out


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
        return 0 if not run_check(root) else 0  # render never fails the run

    violations = run_check(root)
    if violations:
        print("\n".join(violations))
        print(f"\nhierarchy.py --check: {len(violations)} violation(s).")
        return 1
    print("hierarchy.py --check: clean — every seat accounted, no drift.")
    return 0


if __name__ == "__main__":
    sys.exit(main())