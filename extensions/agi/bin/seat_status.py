#!/usr/bin/env python3
"""seat_status.py — one live read of every seat, the spawn budget, and the
telemetry roll-up (hypothesis:l3w4-telemetry-seat-status).

Owner (2026-09-07): the telemetry long-term goal should lead to build nodes
that *literally show live stats including seat status in the graph*. So the
graph has everything. `goal:g16` already commits to a per-node/session
roll-up; seat status is what the owner's text adds to it.

## One compute, two readers

Like `briefing.py` and the `frame_stream`, this module computes a single
`SeatsView` once and `viewport.py --live` renders that same object in both
`render_human` and `render_llm` — and `--theme sanctuary` already falls back
to it through `load_seat_rows`. Two renderings, one set of facts.

## It computes, it never writes

Nothing here opens a file for writing. Every number is read: the seat
registry (`config:seats`'s `seats:` list), each seat's meter pin and the
fraction it resolves to, the ephemeral lease population, and the already-
summed `cost_usd_total` on this season's report nodes. Absent anything — no
`seats.md`, no pin, no config — it fails open to `fraction=None` / empty
lists rather than raising, so a half-configured project still renders with the
board it has, exactly as `briefing.py` degrades.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

#: Report node types the roll-up writes its `*_total` fields to. Mirrors
#: `telemetry_rollup.py`'s accepted types — never restated here.
REPORT_TYPES = ("outcome", "bigger_outcome", "overview")

#: Default ladder field the meter's fractions are measured against, when the
#: ladder node or its field is absent. Mirrors rotate's own default.
DEFAULT_DIRECTOR_CONTEXT_TOKENS = 1_000_000


@dataclass
class SeatsView:
    """Every fact the live seat-status section states, computed once."""

    registry_present: bool = False
    seats: list = field(default_factory=list)
    #: Each seat: {name, role, session_kind, rotated_by, worktree,
    #:            session_ref, fraction: float|None, fraction_source: str}
    ephemeral_live: int = 0
    ephemeral_cap: int = 0
    rollup_config_read: bool = False
    rollup_reports_measured: int = 0
    rollup_cost_usd_total: float = 0.0


def _load_registry_rows(root: Path) -> tuple[list, bool]:
    """`(rows, present)` for `config:seats`'s `seats:` list.

    Reads THROUGH `hierarchy.load_seats` — the single reader of the two
    declared frontmatter sources (hypothesis:l3w4-hierarchy-one-source) — the
    same file `dispatch.py --seat` and `rotate.py meter --seat` read. The
    seat_status copy of the seats.md read is gone so the view cannot drift
    from the chart. Presence resolves THROUGH geometry_config (posts-first,
    else the deprecated seats.md), never a literal seats.md — the same
    post:seats-renamed resolver every other reader uses
    (hypothesis:l4-a-seat-is-a-post-everywhere). Absent file ->
    `([], False)`, the fail-open contract everything else degrades to.
    """
    import geometry_config as _gc
    cfg = _gc.geometry_config_path(root)
    present = cfg is not None and cfg.is_file()
    rows = []
    try:
        import hierarchy as _hier
        rows = _hier.load_seats(root)
    except Exception as exc:                                        # noqa: BLE001
        print(f"warn: seat_status could not read seats via hierarchy: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return list(_rows_via_zoom(root)), True
    return list(rows), True if rows or present else False


def _rows_via_zoom(root: Path) -> list:
    """Last-resort row read, posts-first with the seats fallback. zoom's
    frontmatter view is keyed by file-id+list-key, so the renamed layout
    (`config:posts`.`posts`) must be tried before the deprecated
    `config:seats`.`seats` — a hardcoded seats-only lookup returns [] the
    moment the file is posts.md."""
    try:
        import zoom as _zoom
        gf = _zoom._frontmatter_for(root, ".geometry")
        rows = (gf.get("config:posts") or {}).get("posts")
        if not rows:
            rows = (gf.get("config:seats") or {}).get("seats")
        return rows or []
    except Exception:                                                # noqa: BLE001
        return []


def _seat_fraction(root: Path, name: str):
    """`(fraction, source, raw_usage)` for one seat's meter pin, best-effort.

    Resolves the seat-stable pin `<root>/sessions/<name>.meter`, reads the
    transcript it names, parses usage and divides by the ladder's
    `director_context_tokens`. Any of the four steps being absent or malformed
    returns `(None, reason)` rather than raising — the seat still renders,
    flagged as unmeasured.
    """
    try:
        import rotate as _rotate
        pin = _rotate.find_pin_log(root, seat=name)
        if pin is None:
            return None, "no_pin"
        target = _rotate._read_pin_target(pin)
        if target is None:
            return None, "pin_empty"
        usage = _rotate.parse_usage_from_cc_transcript(target)
        if usage is None:
            usage = _rotate.parse_usage_from_rc_log(target)
        if usage is None:
            return None, "no_usage"
        context = _rotate.load_ladder_field(
            root, "director_context_tokens", DEFAULT_DIRECTOR_CONTEXT_TOKENS)
        try:
            context = int(context)
        except (TypeError, ValueError):
            context = DEFAULT_DIRECTOR_CONTEXT_TOKENS
        return _rotate.calculate_fraction(usage, context), "meter"
    except Exception as exc:                                         # noqa: BLE001
        print(f"warn: seat_status could not read meter for {name}: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return None, "error"


def _ephemeral(root: Path):
    """`(live, cap, config_read)` for the fire-and-forget spawn budget."""
    try:
        import spawn_budget as _sb
        live = _sb.live_count(root)
        cfg = {}
        try:
            import metrics as _m
            cfg = _m.read_config(root) or {}
        except Exception:                                             # noqa: BLE001
            pass
        cap = _sb.max_live(cfg)
        return live, cap, True
    except Exception as exc:                                          # noqa: BLE001
        print(f"warn: seat_status could not read spawn budget: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 0, 0, False


def _rollup(fm_by_id: dict, season: str) -> tuple[int, float]:
    """`(count, cost_total)` over the already-loaded report nodes.

    `fm_by_id` is the `id -> frontmatter` map viewport already builds for the
    frame stream; reuse it rather than recompute a read. A report counts when
    its type is a roll-up target, its `season` equals the current one, and it
    carries a `cost_usd_total` — the roll-up's own field, never re-added here.
    """
    if not fm_by_id:
        return 0, 0.0
    count = 0
    total = 0.0
    for fm in fm_by_id.values():
        if not isinstance(fm, dict):
            continue
        if fm.get("type") not in REPORT_TYPES:
            continue
        if season and str(fm.get("season") or "") != str(season):
            continue
        c = fm.get("cost_usd_total")
        if c is None:
            continue
        try:
            total += float(c)
        except (TypeError, ValueError):
            continue
        count += 1
    return count, total


def _season(root: Path) -> str:
    try:
        return str(load_ladder_field(root, "current_season", "") or "")
    except Exception:                                                  # noqa: BLE001
        return ""


def load_ladder_field(root: Path, field: str, default):
    """Thin re-export so `collect` need not open the ladder node itself."""
    try:
        import rotate as _rotate
        return _rotate.load_ladder_field(root, field, default)
    except Exception:                                                  # noqa: BLE001
        return default


def collect(root: Path, fm_by_id: dict) -> SeatsView:
    """Compute the one `SeatsView` both renderers state.

    `root` is the project/graph root as `viewport` resolves it. `fm_by_id` is
    the frontmatter map viewport already built for the frame stream — reusing
    it, never re-reading it.
    """
    rows, present = (_rows_via_zoom(root), False)
    try:
        rows, present = _load_registry_rows(root)
    except Exception:                                                  # noqa: BLE001
        rows, present = (_rows_via_zoom(root), rows is not None and False)
        present = bool(rows)

    seats: list = []
    for r in rows or []:
        name = str(r.get("name") or "")
        if not name:
            continue
        fraction, fsrc = _seat_fraction(root, name)
        seats.append({
            "name": name,
            "role": str(r.get("role") or ""),
            "session_kind": str(r.get("session_kind") or ""),
            "rotated_by": str(r.get("rotated_by") or ""),
            "worktree": str(r.get("worktree") or ""),
            "session_ref": str(r.get("session_ref") or ""),
            "fraction": fraction,
            "fraction_source": fsrc,
        })

    live, cap, cfg_read = _ephemeral(root)
    count, cost = _rollup(fm_by_id, _season(root))
    return SeatsView(
        registry_present=present,
        seats=seats,
        ephemeral_live=live,
        ephemeral_cap=cap,
        rollup_config_read=cfg_read,
        rollup_reports_measured=count,
        rollup_cost_usd_total=cost,
    )


def to_markdown(v: SeatsView) -> list[str]:
    """The full section, for `render_llm`."""
    out = ["## seat status"]
    if not v.registry_present:
        out.append("no seat registry yet")
        return out
    for s in v.seats:
        frac = f" {s['fraction']:.0%}" if s["fraction"] is not None else ""
        wt = f" worktree={s['worktree']}" if s.get("worktree") else ""
        addr = f" [{s['session_ref']}]" if s.get("session_ref") else ""
        out.append(f"- seat {s['name']}{addr} ({s['role']}/{s['session_kind']})"
                   f" rotated_by={s['rotated_by'] or '-'}{frac}{wt}")
    out.append(f"- ephemeral live/cap: {v.ephemeral_live}/{v.ephemeral_cap}"
               + ("" if v.rollup_config_read else " (spawn-budget unread)"))
    out.append(f"- rollup: {v.rollup_reports_measured} report(s), "
               f"cost_usd_total={v.rollup_cost_usd_total:.2f}")
    return out


def to_compact(v: SeatsView) -> list[str]:
    """One line per seat plus the two summaries — the human viewport's slice."""
    if not v.registry_present:
        return ["no seat registry yet"]
    out = []
    for s in v.seats:
        frac = f" {s['fraction']:.0%}" if s["fraction"] is not None else ""
        out.append(f"{s['name']} ({s['role']}){frac}")
    out.append(f"ephemeral {v.ephemeral_live}/{v.ephemeral_cap} · "
               f"rollup ${v.rollup_cost_usd_total:.2f} "
               f"({v.rollup_reports_measured})")
    return out


def main(argv: list[str] | None = None) -> int:
    """A real CLI (also the gate's plain listing). `--list` prints every seat
    row with its live fraction.
    """
    import argparse
    if argv is None:
        argv = sys.argv[1:]
    ap = argparse.ArgumentParser(
        prog="seat_status.py",
        description="One live read of the seat registry + spawn budget + "
                    "telemetry roll-up.")
    ap.add_argument("root", nargs="?", default=".",
                    help="project root (enclosing .agi/ wins); default cwd")
    ap.add_argument("--list", action="store_true",
                    help="print every declared seat with its live state")
    args = ap.parse_args(argv)
    import locations
    root = Path(args.root)
    root = locations.find_project_root(root) or root
    view = collect(root, {})
    lines = to_markdown(view) if not args.list else None
    if args.list:
        if not view.registry_present:
            print("no seat registry yet")
        else:
            for s in view.seats:
                frac = (f"{s['fraction']:.0%}"
                        if s['fraction'] is not None else "")
                print("\t".join([
                    s['name'], s['role'], s['session_kind'],
                    s['rotated_by'] or '-', s['worktree'] or '-',
                    s['session_ref'] or '-', frac, s['fraction_source']]))
        return 0
    print("\n".join(lines or []))
    return 0


if __name__ == "__main__":
    sys.exit(main())