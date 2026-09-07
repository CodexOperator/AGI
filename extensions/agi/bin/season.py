#!/usr/bin/env python3
"""season.py — season lifecycle: status, judge, rollover.

Reads the ladder node for tiers, current_season, and caps. Every write goes
through write.py (shell out), never a direct file write.

Subcommands:
  status                          — per-tier plan/report counts, ratios, cost
  judge <report-node-id>          — stamp a judgment record on a report node
    [--against <plan-node-id>]
  rollover [--dry-run]            — print or perform season N+1 rollover
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402
from graph_core.persistence import frontmatter  # noqa: E402


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: The ladder node path, relative to the graph root.
LADDER_NODE_REL = Path("nodes") / ".geometry" / "ladder.md"

#: write.py path (we shell out, never write files directly).
WRITE_PY = Path(__file__).resolve().parent / "write.py"


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class Tier:
    """One tier from the ladder declaration."""

    tier: int
    plan_types: list[str]
    report_type: str | None
    judged_against: str
    lens: str
    cadence: str


@dataclass
class TierStats:
    """Aggregated counts for one tier."""

    tier: int
    plan_types: list[str]
    report_type: str | None
    plans_active: int = 0
    plans_total: int = 0
    reports_active: int = 0
    reports_total: int = 0
    orphan_reports: int = 0  # reports with no resolved plan parent
    cost_usd: float = 0.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_ladder(root: Path) -> dict:
    """Load the ladder node frontmatter."""
    path = Path(root) / LADDER_NODE_REL
    if not path.exists():
        print(f"ERR: ladder node not found at {path}", file=sys.stderr)
        sys.exit(1)
    nf = frontmatter.load_node_file(path)
    return nf.frontmatter


def _load_tiers(root: Path) -> list[Tier]:
    """Parse the ladder node's tiers declaration."""
    fm = _load_ladder(root)
    tiers_raw = fm.get("tiers", [])
    tiers = []
    for t in tiers_raw:
        tiers.append(Tier(
            tier=t.get("tier", 0),
            plan_types=list(t.get("plan_types", [])),
            report_type=t.get("report_type"),
            judged_against=str(t.get("judged_against", "")),
            lens=str(t.get("lens", "")),
            cadence=str(t.get("cadence", "")),
        ))
    return tiers


def _get_current_season(root: Path) -> int:
    """Read current_season from the ladder node."""
    fm = _load_ladder(root)
    return int(fm.get("current_season", 1))


def _get_caps(root: Path) -> dict:
    """Read caps from the ladder node."""
    fm = _load_ladder(root)
    return dict(fm.get("caps", {}))


def _plan_type_for_kind(kind: str) -> str:
    """Map a goal_kind to the corresponding plan_type name.

    The ladder node declares plan types like "short-term goal" and
    "long-term goal", but the actual frontmatter goal_kind stores the shorter
    "short-term" and "long-term". This normaliser accounts for both.
    """
    if kind == "short-term":
        return "short-term goal"
    if kind == "long-term":
        return "long-term goal"
    return kind


def _kind_from_goal_type(plan_type: str) -> str | None:
    """Map a ladder plan type back to the goal_kind stored in nodes.

    Returns None for non-goal plan types (vision, moral).
    """
    if plan_type == "subgoal":
        return "subgoal"
    if plan_type == "short-term goal":
        return "short-term"
    if plan_type == "long-term goal":
        return "long-term"
    return None


def _collect_stats(root: Path, tiers: list[Tier], season: int) -> list[TierStats]:
    """Walk the graph and accumulate counts per tier."""
    nodes_dir = Path(root) / "nodes"

    stats = {}
    for t in tiers:
        stats[t.tier] = TierStats(
            tier=t.tier,
            plan_types=t.plan_types,
            report_type=t.report_type,
        )

    # Walk every node file
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
        except Exception:
            continue
        fm = nf.frontmatter
        t = fm.get("type", "")
        if not t:
            continue
        status = str(fm.get("status", "active"))

        # Check if this node is a report type for any tier
        for tier_obj in tiers:
            if tier_obj.report_type and t == tier_obj.report_type:
                s = stats[tier_obj.tier]
                s.reports_total += 1
                if status == "active":
                    s.reports_active += 1
                # Check if judged_against is set
                judged = fm.get("judged_against")
                if not judged:
                    s.orphan_reports += 1
                break

        # Check if this is a goal with a plan kind for a tier
        if t == "goal":
            kind = fm.get("goal_kind", "")
            for tier_obj in tiers:
                plan_type = _plan_type_for_kind(kind)
                if plan_type in tier_obj.plan_types:
                    s = stats[tier_obj.tier]
                    s.plans_total += 1
                    if status == "active":
                        s.plans_active += 1
                    break

        # Vision nodes are their own type
        if t == "vision":
            for tier_obj in tiers:
                if "vision" in tier_obj.plan_types:
                    s = stats[tier_obj.tier]
                    s.plans_total += 1
                    if status == "active":
                        s.plans_active += 1
                    break

        # Moral nodes
        if t == "moral":
            for tier_obj in tiers:
                if "moral" in tier_obj.plan_types:
                    s = stats[tier_obj.tier]
                    s.plans_total += 1
                    if status == "active":
                        s.plans_active += 1
                    break

    return [stats[k] for k in sorted(stats)]


def _shell_out_write(root: Path, node_id: str,
                     set_fm: dict | None = None,
                     note: str | None = None,
                     actor: str = "season.py",
                     session: str = "season") -> int:
    """Call write.py to modify a node. Returns exit code."""
    script_parts = []
    if set_fm:
        for k, v in set_fm.items():
            if isinstance(v, dict):
                import json
                v = json.dumps(v, separators=(',', ':'))
            script_parts.append(f"set {k} {v}")
    if note:
        script_parts.append(f"note {note}")

    if not script_parts:
        return 0

    script = " && ".join(script_parts)
    cmd = [
        sys.executable, str(WRITE_PY),
        node_id,
        script,
        "--actor", actor,
        "--session", session,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(root))
    if result.returncode != 0:
        print(f"ERR: write.py failed for {node_id}: {result.stderr.strip()}",
              file=sys.stderr)
    return result.returncode


# ---------------------------------------------------------------------------
# Subcommand: status
# ---------------------------------------------------------------------------

def cmd_status(root: Path, args) -> int:
    """Print per-tier plan and report counts, ratios, mismatches."""
    tiers = _load_tiers(root)
    season = _get_current_season(root)
    stats_list = _collect_stats(root, tiers, season)

    print(f"Season {season} status")
    print("=" * 60)
    print()

    for s in stats_list:
        plan_types_str = ", ".join(s.plan_types)
        report_type_str = s.report_type or "(none)"
        print(f"Tier {s.tier}: plans={plan_types_str}  report={report_type_str}")

        plans_label = "plans" if s.plans_total != 1 else "plan"
        reports_label = "reports" if s.reports_total != 1 else "report"

        if s.report_type:
            # Show active/total for both
            print(f"  {plans_label}: {s.plans_active} active / {s.plans_total} total")
            print(f"  {reports_label}: {s.reports_active} active / {s.reports_total} total")

            if s.plans_total > 0:
                ratio = s.reports_total / s.plans_total
                print(f"  report/plan ratio: {ratio:.2f}")
            else:
                print(f"  report/plan ratio: — (no plans)")

            # Plans without reports (plans - reports, but clamped)
            diff = s.plans_total - s.reports_total
            if diff > 0:
                print(f"  plans without reports: {diff}")
            elif diff < 0:
                print(f"  reports without plans: {-diff}")

            if s.orphan_reports > 0:
                print(f"  {s.orphan_reports} report(s) with no judged_against field")
        else:
            print(f"  {plans_label}: {s.plans_active} active / {s.plans_total} total")
            if s.plans_total > 0:
                print(f"  (never judged by machine)")

        print()

    # Season 1 baseline comparison from the brief
    print("Season 1 baseline (from design brief, §1):")
    print(f"  subgoal: 71 (8 active) / outcome: 23 → 0.32")
    print(f"  long-term: 21 (4 active) / bigger_outcome: 19 → ~1.0")
    print(f"  vision: 17 / overview: 0")

    return 0


# ---------------------------------------------------------------------------
# Subcommand: judge
# ---------------------------------------------------------------------------

def cmd_judge(root: Path, args) -> int:
    """Stamp a judgment record on a report node.

    Sets judged_against (the given plan node id, or the report's first parent
    that is a plan type for its tier), lens (the plan node's own first goal or
    vision parent), alignment unknown, and season current.
    """
    report_id = args.report_id
    against_id = args.against
    debug = args.debug

    # Load ladder to get tier info
    ladder_fm = _load_ladder(root)
    tiers_raw = ladder_fm.get("tiers", [])
    season = int(ladder_fm.get("current_season", 1))

    # Collect all plan types across all tiers
    plan_types: set[str] = set()
    report_types: set[str] = set()
    tier_map: dict[str, int] = {}  # report_type -> tier
    lens_map: dict[str, str] = {}  # tier -> lens description

    for t in tiers_raw:
        tn = int(t.get("tier", 0))
        plans = [str(p) for p in t.get("plan_types", [])]
        report = str(t.get("report_type", "")) if t.get("report_type") else None
        lens_str = str(t.get("lens", ""))
        for p in plans:
            plan_types.add(p)
        if report:
            report_types.add(report)
            tier_map[report] = tn
        lens_map[str(tn)] = lens_str

    # Load the report node to check its type
    nodes_dir = Path(root) / "nodes"
    report_path = None
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
            if nf.frontmatter.get("id") == report_id:
                report_path = f
                break
        except Exception:
            continue

    if report_path is None:
        print(f"ERR: report node {report_id!r} not found", file=sys.stderr)
        return 1

    report_nf = frontmatter.load_node_file(report_path)
    report_type = str(report_nf.frontmatter.get("type", ""))
    report_parents = report_nf.frontmatter.get("parents", [])

    # Validate this is a known report type
    if report_type not in report_types:
        print(f"ERR: {report_id} has type {report_type!r}, not a report type "
              f"(known: {', '.join(sorted(report_types))}). Refusing to judge.",
              file=sys.stderr)
        return 1

    tier_num = tier_map.get(report_type, -1)

    # Determine which plan ids are valid for this tier
    tier_plan_types: list[str] = []
    for t in tiers_raw:
        if int(t.get("tier", 0)) == tier_num:
            tier_plan_types = [str(p) for p in t.get("plan_types", [])]
            break

    # Resolve the against_id: given explicitly or derived from parents
    final_against = against_id
    if not final_against:
        # Walk parents to find one whose type or goal_kind matches a plan type
        for pid in report_parents:
            pid_str = str(pid)
            for f in sorted(nodes_dir.rglob("*.md")):
                try:
                    nf = frontmatter.load_node_file(f)
                    if nf.frontmatter.get("id") == pid_str:
                        parent_type = str(nf.frontmatter.get("type", ""))
                        parent_kind = str(nf.frontmatter.get("goal_kind", ""))
                        from graph_core.identity import canonical_type
                        # Check if this parent is a known plan type
                        parent_plan_type = _plan_type_for_kind(parent_kind)
                        if parent_type == "goal" and parent_plan_type in tier_plan_types:
                            final_against = pid_str
                            break
                        if pid_str in plan_types or parent_type in plan_types:
                            final_against = pid_str
                            break
                except Exception:
                    continue
            if final_against:
                break

    if not final_against:
        print(f"ERR: no plan parent found for {report_id} (and --against not given)",
              file=sys.stderr)
        return 1

    # Load the plan node to derive the lens
    plan_path = None
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
            if nf.frontmatter.get("id") == final_against:
                plan_path = f
                break
        except Exception:
            continue

    lens_id = ""
    if plan_path:
        plan_nf = frontmatter.load_node_file(plan_path)
        plan_parents = plan_nf.frontmatter.get("parents", [])
        # The lens is the plan node's own first goal or vision parent
        for pid in plan_parents:
            pid_str = str(pid)
            for ff in sorted(nodes_dir.rglob("*.md")):
                try:
                    nf2 = frontmatter.load_node_file(ff)
                    nid = nf2.frontmatter.get("id", "")
                    if nid == pid_str:
                        nt = str(nf2.frontmatter.get("type", ""))
                        if nt in ("goal", "vision"):
                            lens_id = pid_str
                            break
                except Exception:
                    continue
            if lens_id:
                break

    if debug:
        print(f"DEBUG: report={report_id} type={report_type} tier={tier_num}")
        print(f"DEBUG: against={final_against} lens={lens_id} season={season}")

    # Write the judgment record using write.py
    set_fields = {
        "judged_against": final_against,
        "season": season,
    }
    if lens_id:
        set_fields["lens"] = lens_id

    rc = _shell_out_write(root, report_id, set_fm=set_fields)
    if rc != 0:
        return rc

    # moral_audit scaffold for overviews
    if report_type == "overview":
        # Reload to get current state
        report_nf = frontmatter.load_node_file(report_path)
        existing_audit = report_nf.frontmatter.get("moral_audit", {})
        if not isinstance(existing_audit, dict):
            existing_audit = {}

        MORAL_KEYS = ["faith", "love", "empathy", "antifragility", "beauty"]
        new_audit = {}
        changed = False
        for mk in MORAL_KEYS:
            if mk in existing_audit and isinstance(existing_audit[mk], dict):
                new_audit[mk] = existing_audit[mk]
            else:
                new_audit[mk] = {"value": "unknown", "evidence": None}
                changed = True

        if changed:
            rc2 = _shell_out_write(root, report_id, set_fm={"moral_audit": new_audit})
            if rc2 != 0:
                return rc2
            print(f"moral_audit scaffolded on {report_id} (filled missing keys)")

    print(f"Judgment stamped on {report_id}:")
    print(f"  judged_against: {final_against}")
    print(f"  lens: {lens_id or '(not found)'}")
    print(f"  alignment: unknown (set manually)")
    print(f"  season: {season}")

    if not lens_id:
        print(f"WARN: lens not derived — plan node {final_against} has no goal/vision parent",
              file=sys.stderr)

    return 0


# ---------------------------------------------------------------------------
# Subcommand: retag
# ---------------------------------------------------------------------------

#: A node whose id starts with this prefix is owner-tier (goal:g12) and may
#: only be written through write.py with `--actor owner`.
MORAL_PREFIX = "moral:"

#: The frontmatter key retag stamps.
SEASON_KEY = "season"


def cmd_retag(root: Path, args) -> int:
    """Backfill `season: 1` on every node that lacks a season stamp.

    The precondition for the season supernode predicate (design brief 2.7):
    a zoomed-out view collapses `season == 1` into one supernode, which only
    works if the stamp exists on every node. The writer stamps at mint, so
    pre-ladder nodes were never retagged; this is the one scripted pass that
    closes the gap.

    Rules (from hypothesis l3w0-season-retag):
      * every node under `nodes/`, including `nodes/deprecated/`, with no
        `season` field is stamped with the ladder's `current_season`;
      * a node that already has `season` is skipped, never overwritten;
      * every write shells out to write.py (never a direct file write), so
        the write guard stays silent and provenance (`edited_by`,
        `thought_session`) is recorded;
      * moral nodes are owner-tier (goal:g12): for those five only the
        shell-out uses `--actor owner`, and their existing `edited_by` /
        `thought_session` provenance is preserved rather than overwritten by
        this scripted pass.
    """
    dry_run = getattr(args, 'dry_run', False)
    actor = getattr(args, 'actor', "") or "season.py"
    session = getattr(args, 'session', "") or "season"
    season = _get_current_season(root)

    nodes_dir = Path(root) / "nodes"
    total = 0
    with_season = 0
    candidates: list[str] = []
    moral_ids: list[str] = []
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
        except Exception:
            continue
        fm = nf.frontmatter
        nid = fm.get("id")
        if not isinstance(nid, str) or not nid:
            continue  # not a node file (e.g. a loose doc)
        total += 1
        if fm.get(SEASON_KEY) is not None:
            with_season += 1
        else:
            candidates.append(nid)
            if nid.startswith(MORAL_PREFIX):
                moral_ids.append(nid)

    print(f"Retag: stamp season {season} on every node with none")
    print(f"  nodes: {total}")
    print(f"  with season: {with_season}")
    print(f"  without season: {len(candidates)}")
    if moral_ids:
        print(f"  moral (owner-tier, --actor owner): {len(moral_ids)}")
    if dry_run:
        print(f"[DRY RUN] {len(candidates)} node(s) would be stamped; nothing written")
        return 0

    if not candidates:
        print("nothing to stamp.")
        return 0

    stamped = 0
    failures = []
    for nid in candidates:
        if nid.startswith(MORAL_PREFIX):
            # Owner-tier (goal:g12): the stamp must not clobber the owner's
            # own edited_by/thought_session — write.py always sets edited_by
            # from --actor and only touches thought_session when --session is
            # truthy, so pass actor=owner and no session to preserve both.
            node_actor = "owner"
            node_session = ""
        else:
            node_actor = actor
            node_session = session
        rc = _shell_out_write(root, nid, set_fm={SEASON_KEY: season},
                              actor=node_actor, session=node_session)
        if rc == 0:
            stamped += 1
        else:
            failures.append(nid)

    # Re-count for the after figure.
    after_with_season = 0
    after_candidates = 0
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
        except Exception:
            continue
        fm = nf.frontmatter
        if not isinstance(fm.get("id"), str):
            continue
        if fm.get(SEASON_KEY) is not None:
            after_with_season += 1
        else:
            after_candidates += 1

    print(f"stamped: {stamped}")
    print(f"  after: {after_with_season} with season / {after_candidates} without")
    if failures:
        print(f"FAILED: {len(failures)} — {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


# ---------------------------------------------------------------------------
# Subcommand: rollover
# ---------------------------------------------------------------------------

def cmd_rollover(root: Path, args) -> int:
    """Print or perform a season rollover."""
    dry_run = getattr(args, 'dry_run_explicit', False) or getattr(args, 'dry_run', False)
    debug = getattr(args, 'debug', False)

    ladder_fm = _load_ladder(root)
    season = int(ladder_fm.get("current_season", 1))
    new_season = season + 1
    caps = _get_caps(root)
    vision_cap = caps.get("vision", 3)

    # Get stats for current season
    tiers = _load_tiers(root)
    stats_list = _collect_stats(root, tiers, season)

    print(f"Rollover: season {season} → {new_season}")
    if dry_run:
        print("[DRY RUN — no changes will be written]")
    print()

    # Check: any overviews of current season with no judgment record?
    # (overviews don't exist yet, but check anyway)
    nodes_dir = Path(root) / "nodes"
    unjudged_overviews = []
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
            fm = nf.frontmatter
            if fm.get("type") == "overview" and fm.get("season") == season:
                if not fm.get("judged_against"):
                    unjudged_overviews.append(fm.get("id", "?"))
        except Exception:
            continue

    if unjudged_overviews:
        print(f"BLOCKING: {len(unjudged_overviews)} overview(s) of season {season} "
              f"lack a judgment record:")
        for oid in unjudged_overviews:
            print(f"  {oid}")
        if not dry_run:
            print("Rollover refused. Judge or discard unjudged overviews first.",
                  file=sys.stderr)
            return 1
        print("(dry run continues despite blocker)")
        print()

    # What would be minted for new season:
    print("Would mint for season", new_season, ":")

    # New visions (up to caps.vision)
    # Existing visions at current season
    visions_current = 0
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
            fm = nf.frontmatter
            if fm.get("type") == "vision" and fm.get("season") == new_season:
                visions_current += 1
        except Exception:
            continue

    # Close current visions
    print(f"  Close {visions_current} vision(s) of season {season} → status: closed")
    visions_open_for_new = max(0, vision_cap - visions_current)
    # Also check the caps_apply_from_season flag for grandfathering
    caps_from = ladder_fm.get("caps_apply_from_season", 2)
    if new_season < caps_from:
        visions_open_for_new = vision_cap  # no cap for this season yet
    if visions_open_for_new > 0:
        print(f"  Mint up to {visions_open_for_new} new vision(s) (cap: {vision_cap})")
        if dry_run:
            print(f"    Each with parents: [moral:faith, moral:love, moral:empathy, "
                  f"moral:antifragility, moral:beauty]")
            print(f"    season_parents: [overviews of season {season}]")
            print(f"    proposes_goals: [], moral_adherence: all unknown")
    else:
        print(f"  Vision cap ({vision_cap}) reached; no new visions")

    # Overviews at current season: retag to closed
    overviews_current = 0
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
            fm = nf.frontmatter
            if fm.get("type") == "overview" and fm.get("season") == season:
                overviews_current += 1
        except Exception:
            continue
    if overviews_current > 0:
        print(f"  Retag {overviews_current} overview(s) of season {season} → status: closed")

    # Bump season
    print()
    print(f"  Bump ladder current_season: {season} → {new_season}")

    if not dry_run:
        # Perform the rollover
        print("Performing rollover...")

        # Close all current visions
        vision_ids_to_close = []
        for f in sorted(nodes_dir.rglob("*.md")):
            try:
                nf = frontmatter.load_node_file(f)
                fm = nf.frontmatter
                if fm.get("type") == "vision" and fm.get("season") == season and fm.get("status") != "closed":
                    vision_ids_to_close.append(str(fm.get("id", "")))
            except Exception:
                continue

        for vid in vision_ids_to_close:
            rc = _shell_out_write(root, vid, set_fm={"status": "closed"})
            if rc != 0:
                return rc

        # Close current overviews
        overview_ids_to_close = []
        for f in sorted(nodes_dir.rglob("*.md")):
            try:
                nf = frontmatter.load_node_file(f)
                fm = nf.frontmatter
                if fm.get("type") == "overview" and fm.get("season") == season and fm.get("status") != "closed":
                    overview_ids_to_close.append(str(fm.get("id", "")))
            except Exception:
                continue

        for oid in overview_ids_to_close:
            rc = _shell_out_write(root, oid, set_fm={"status": "closed"})
            if rc != 0:
                return rc

        # Bump season on ladder node
        rc = _shell_out_write(root, "ladder:ladder", set_fm={"current_season": new_season})
        if rc != 0:
            return rc

        print(f"Rollover to season {new_season} complete.")

    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".",
                    help="any path inside the project (default: .)")

    sub = ap.add_subparsers(dest="command", required=True)

    # status
    p_status = sub.add_parser("status", help="Print per-tier plan/report counts")

    # judge
    p_judge = sub.add_parser("judge", help="Stamp a judgment record on a report node")
    p_judge.add_argument("report_id", help="Node ID of the report node to judge")
    p_judge.add_argument("--against", default="",
                         help="Plan node ID (default: derived from report's parents)")
    p_judge.add_argument("--debug", action="store_true", help="Show debug info")

    # rollover
    p_rollover = sub.add_parser("rollover", help="Print or perform season rollover")
    p_rollover.add_argument("--dry-run", dest="dry_run_explicit",
                            action="store_true", default=False,
                            help="Only print what would happen")
    p_rollover.add_argument("--debug", action="store_true", help="Show debug info",
                            dest="debug")

    # retag
    p_retag = sub.add_parser("retag",
                             help="Backfill season on every node that lacks it")
    p_retag.add_argument("--dry-run", action="store_true", default=False,
                         help="Print what would happen and write nothing")
    p_retag.add_argument("--actor", default="",
                         help="edited_by for non-moral stamps (default: season.py)")
    p_retag.add_argument("--session", default="",
                         help="thought_session for stamps (default: season)")

    args = ap.parse_args(argv)

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    if args.command == "status":
        return cmd_status(root, args)
    elif args.command == "judge":
        return cmd_judge(root, args)
    elif args.command == "rollover":
        return cmd_rollover(root, args)
    elif args.command == "retag":
        return cmd_retag(root, args)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())