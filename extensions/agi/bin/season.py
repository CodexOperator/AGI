#!/usr/bin/env python3
"""season.py — season lifecycle: status, judge, rollover.

Reads the ladder node for tiers, current_season, and caps. Every write goes
through write.py (shell out), never a direct file write.

Subcommands:
  status                          — per-tier plan/report counts, ratios, cost
  judge <report-node-id>          — stamp a judgment record on a report node
    [--against <plan-node-id>]
  rollover [--dry-run]            — print or perform season N+1 rollover
    [--visions-from <dir|file>]   — vision bodies verbatim (owner text + gloss)
    [--name <name>]               — name season 1 in the ladder's season_names
    [--branch]                    — git checkout -b season/s<N> after the write
    [--allow-unjudged]            — bypass the unjudged-overview stage gate
  retag                           — backfill the season stamp
  merge-up <branch>               — --no-ff merge a loop branch into its recorded
                                    base branch, suite-green gate, worktree removed
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

#: send.py path — judge --quorum shells `send.py audience prime ...` on a
#: deadlock (hypothesis:l3w4-quorum-reviews).
SEND_PY = Path(__file__).resolve().parent / "send.py"


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
    "short-term" and "long-term". `perpetual` is the 2026-09-06 canonical
    spelling of `long-term` (hypothesis:l3w1-goal-kind-perpetual) and maps to
    the same ladder plan type, so a perpetual goal still tallies as a tier-1
    plan and a report under it still resolves it as its plan parent. This
    normaliser accounts for all three.
    """
    if kind == "short-term":
        return "short-term goal"
    if kind in ("long-term", "perpetual"):
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
        # `perpetual` is the canonical spelling of `long-term` as of the
        # l3w1-goal-kind-perpetual rename; a ladder-declared "long-term goal"
        # plan is written down in nodes as `goal_kind: perpetual`.
        return "perpetual"
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

    # ---- quorum review (hypothesis:l3w4-quorum-reviews) ----
    # The advisors review through their visions in a room; a 3-0/2-1 tally
    # stamps `alignment` here, a 1-1-1 deadlock or any --morals vote falls
    # through to `send.py audience prime` instead and leaves alignment unset.
    quorum_align = None
    quorum_adjust = None
    quorum_note = None
    quorum_audienced = False
    if getattr(args, "quorum", False):
        try:
            import send
        except ImportError:
            print(f"ERR: cannot import send.py for --quorum (no sibling "
                  f"send.py?)", file=sys.stderr)
            return 1
        room = getattr(args, "room", "") or "tier3-quorum"
        round_ = (getattr(args, "judge_round", "")
                  or os.environ.get("AGI_LOOP", "default"))
        croot = send.comms_root(root, getattr(args, "comms_root", "") or None)
        try:
            tally = send.tally_votes(croot, room, report_id, round_)
        except SystemExit:
            # tally_votes prints "ERR: incomplete quorum ..." to stderr
            return 1
        any_morals = any(bool(t.get("morals")) for t in tally.values())
        aligned_n = sum(1 for t in tally.values()
                        if t.get("alignment") == "aligned")
        adjust_n = sum(1 for t in tally.values()
                       if t.get("alignment") == "adjust")
        tally_desc = "; ".join(f"{v}={tally[v].get('alignment')}"
                                for v in send.VISIONS if v in tally)
        quorum_note = f"quorum {room} (round {round_}): {tally_desc}"

        if any_morals or (aligned_n < 2 and adjust_n < 2):
            # deadlock, or the morals outrank the quorum: the prime decides
            reason = (f"morals at stake in quorum review of {report_id} "
                      f"(round {round_})" if any_morals else
                      f"quorum deadlocked on {report_id} (round {round_})")
            aud_flags = ["audience", "prime", "--reason",
                         f"{reason}: {tally_desc}"]
            if any_morals:
                aud_flags.append("--morals")
            res = subprocess.run(
                [sys.executable, str(SEND_PY)] + aud_flags,
                capture_output=True, text=True, cwd=str(root))
            if res.returncode != 0:
                print(f"ERR: audience prime failed: "
                      f"{res.stderr.strip() or res.stdout.strip()}",
                      file=sys.stderr)
                return 1
            if res.stdout.strip():
                print(res.stdout.strip())
            quorum_audienced = True
        else:
            quorum_align = "aligned" if aligned_n >= 2 else "adjust"
            dissents = [t for t in tally.values()
                        if t.get("alignment") != quorum_align]
            quorum_adjust = (dissents[0].get("reason", "") if dissents
                             else "")

    if quorum_audienced:
        print(f"quorum did not reach a majority on {report_id}: alignment "
              f"unset; the disputed call goes to the prime")
        return 0

    # Write the judgment record using write.py
    set_fields = {
        "judged_against": final_against,
        "season": season,
    }
    if lens_id:
        set_fields["lens"] = lens_id
    if quorum_align is not None:
        set_fields["alignment"] = quorum_align
        if quorum_adjust:
            set_fields["adjust"] = quorum_adjust

    rc = _shell_out_write(root, report_id, set_fm=set_fields,
                          note=quorum_note)
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
    if quorum_align is not None:
        print(f"  alignment: {quorum_align} (quorum majority)")
    else:
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

#: The five morals (goal:g12) — a new season's vision parents, in canonical
#: order (the schema table in [moral].md).
MORALS = ["moral:faith", "moral:love", "moral:empathy",
          "moral:antifragility", "moral:beauty"]


def _season_nodes(root: Path, season: int, node_type: str) -> list[str]:
    """The ids of every node of `node_type` stamped with `season`."""
    out = []
    nodes_dir = Path(root) / "nodes"
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
        except Exception:
            continue
        fm = nf.frontmatter
        if fm.get("type") == node_type and fm.get("season") == season:
            nid = fm.get("id")
            if isinstance(nid, str) and nid:
                out.append(nid)
    return out


def _unjudged_overviews(root: Path, season: int) -> list[str]:
    """Overviews of `season` whose `judged_against` is unset (brief 2.9 gate)."""
    out = []
    nodes_dir = Path(root) / "nodes"
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = frontmatter.load_node_file(f)
        except Exception:
            continue
        fm = nf.frontmatter
        if fm.get("type") == "overview" and fm.get("season") == season:
            if not fm.get("judged_against"):
                nid = fm.get("id", "?")
                out.append(str(nid))
    return out


def _load_vision_sources(arg: str) -> list[dict]:
    """Read vision owner text from a markdown file or a directory of them.

    Each file's body is taken **verbatim** — the prime writes the files from
    brief §1.8 and season.py never invents or edits vision prose. The leading
    `# Title` heading names the node and is stripped from the body; everything
    after it (text + gloss) is the body.
    """
    p = Path(arg)
    files = sorted(p.glob("*.md")) if p.is_dir() else [p]
    sources = []
    for fp in files:
        if not fp.exists():
            print(f"ERR: vision source not found: {fp}", file=sys.stderr)
            continue
        text = fp.read_text(encoding="utf-8")
        lines = text.splitlines()
        title = fp.stem
        i = 0
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i < len(lines) and lines[i].strip().startswith("# "):
            title = lines[i].strip()[2:].strip()
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
        body = "\n".join(lines[i:]).strip("\n")
        sources.append({"file": str(fp), "slug": fp.stem,
                        "title": title, "body": body})
    return sources


def _mint_vision(root: Path, source: dict, season_overviews: list[str],
                 new_season: int):
    """Mint one vision node, `--actor owner`, body verbatim. Returns NodeWrite."""
    from node_writer import write_node
    moral_adherence = {m: "unknown" for m in MORALS}
    extra = {
        "title": source["title"],
        "season": new_season,
        "season_parents": list(season_overviews),
        "proposes_goals": [],
        "moral_adherence": moral_adherence,
        "status": "open",
        "tags": ["vision", "rollover"],
        "edited_by": "owner",
    }
    return write_node(root, "vision", source["slug"],
                      parents=MORALS, extra_fm=extra,
                      body=source["body"], heading=True, bypass=True)


def _find_git_root(root: Path) -> Path | None:
    """Walk up from the project root to the enclosing git repo (or None)."""
    cur = root.resolve()
    while True:
        if (cur / ".git").exists():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent


def cmd_rollover(root: Path, args) -> int:
    """Print or perform a season rollover.

    Wave-2 genesis rollover (brief §1.8, §2.8, §2.9):
      * mint three visions from `--visions-from` (dir or file), bodies taken
        **verbatim** from the owner text (text + gloss); `--actor owner`;
      * `--name <name>` names season 1 in the ladder's `season_names` through
        write.py (e.g. `genesis`);
      * `--branch` opens `season/s<new>` with `git checkout -b` after the
        graph writes, then prints the next commands — never pushes;
      * a stage gate (brief 2.9) refuses the rollover while any season-current
        overview lacks a judgment unless `--allow-unjudged` is given,
        printing the count.

    The dry run prints every node it would mint (title, parents,
    season_parents, actor), every ladder field it would set, and the branch
    step — and changes nothing.
    """
    dry_run = bool(getattr(args, "dry_run_explicit", False)
                   or getattr(args, "dry_run", False))
    allow_unjudged = bool(getattr(args, "allow_unjudged", False))
    name = (getattr(args, "name", "") or "").strip()
    want_branch = bool(getattr(args, "branch", False))
    visions_from = (getattr(args, "visions_from", "") or "").strip()

    ladder_fm = _load_ladder(root)
    season = int(ladder_fm.get("current_season", 1))
    new_season = season + 1
    caps = _get_caps(root)
    vision_cap = int(caps.get("vision", 3))

    print(f"Rollover: season {season} → {new_season}")
    print("[DRY RUN — no changes will be written]" if dry_run
          else "[REAL RUN — performing the plan]")
    print()

    # ---- Stage gate (brief 2.9): refuse while any season-current overview
    # ---- lacks a judgment, unless --allow-unjudged.
    unjudged = _unjudged_overviews(root, season)
    if unjudged:
        print(f"{len(unjudged)} overview(s) of season {season} lack a judgment:")
        for oid in unjudged:
            print(f"  {oid}")
        if not allow_unjudged:
            print("REFUSED: pass --allow-unjudged to roll over anyway")
            return 1
        print("[--allow-unjudged] proceeding anyway")
    print()

    # ---- Season-current overviews become the new visions' season_parents.
    season_overviews = _season_nodes(root, season, "overview")
    existing_new = set(_season_nodes(root, new_season, "vision"))

    print(f"Visions to mint for season {new_season}:")
    if visions_from:
        sources = _load_vision_sources(visions_from)
        if not sources:
            print("ERR: no vision source files read from --visions-from",
                  file=sys.stderr)
            return 1
        for s in sources:
            nid = f"vision:{s['slug']}"
            if nid in existing_new:
                print(f"  SKIP {nid} — already exists (season {new_season})")
                continue
            print(f"  MINT {nid}")
            print(f"    title: {s['title']}")
            print(f"    parents: {', '.join(MORALS)}")
            print(f"    season_parents: {', '.join(season_overviews) or '(none)'}")
            print("    actor: owner")
            print(f"    season: {new_season}")
            print("    moral_adherence: 'unknown' for each moral parent")
            print("    body (verbatim, text + gloss):")
            for body_line in s["body"].splitlines():
                print(f"      {body_line}")
            print()
    else:
        caps_from = int(ladder_fm.get("caps_apply_from_season", 2))
        if new_season < caps_from:
            open_v = vision_cap
        else:
            open_v = max(0, vision_cap - len(existing_new))
        print(f"  Mint up to {open_v} new vision(s) (cap: {vision_cap})")
        if open_v > 0:
            print("    bodies require --visions-from <dir|file>: owner text "
                  "verbatim, never invented")
            print(f"    each parents: {', '.join(MORALS)}")
            print(f"    each season_parents: {', '.join(season_overviews) or '(none)'}")
            print("    each actor: owner")
    print()

    # ---- Ladder fields (through write.py).
    print("Ladder writes:")
    if name:
        print(f"  season_names[1] = {name}")
    print(f"  Bump ladder current_season: {season} → {new_season}")
    print()

    # ---- Branch step (never pushes).
    branch_name = f"season/s{new_season}"
    if want_branch:
        print(f"Branch: git checkout -b {branch_name} (never pushes)")

    if dry_run:
        return 0

    # ===================== REAL RUN — perform the plan =====================
    # Stamped season on the newly minted nodes must be the NEW season. write_node
    # reads AGI_SEASON from the environment (falling back to the ladder's
    # current_season), so export it for the mint pass and restore afterwards.
    old_env_season = os.environ.get("AGI_SEASON")
    os.environ["AGI_SEASON"] = str(new_season)
    try:
        # 1. Mint the visions, --actor owner, bodies verbatim.
        if visions_from:
            from node_writer import WRITTEN, SKIPPED, REJECTED
            sources = _load_vision_sources(visions_from)
            minted = 0
            for s in sources:
                nid = f"vision:{s['slug']}"
                if nid in existing_new:
                    continue
                res = _mint_vision(root, s, season_overviews, new_season)
                if res.status in (WRITTEN,):
                    print(f"minted {nid} (parents: {len(MORALS)} morals, "
                          f"season_parents: {len(season_overviews)} overviews, actor owner)")
                    minted += 1
                else:
                    print(f"ERR: {nid} not minted ({res.status}: {res.reason})",
                          file=sys.stderr)
            if not minted:
                print("no new visions minted (all already exist or files missing)")
    finally:
        if old_env_season is None:
            os.environ.pop("AGI_SEASON", None)
        else:
            os.environ["AGI_SEASON"] = old_env_season

    # 2. Name season 1 and bump the season on the ladder (through write.py).
    ladder_set = {}
    if name:
        season_names = dict(ladder_fm.get("season_names") or {})
        season_names[1] = name
        ladder_set["season_names"] = season_names
    ladder_set["current_season"] = new_season
    rc = _shell_out_write(root, "ladder:ladder", set_fm=ladder_set)
    if rc != 0:
        return rc
    if name:
        print(f"season_names[1] = {name} written on the ladder")
    print(f"ladder current_season: {season} → {new_season}")

    # 3. Open the season branch (never pushes).
    if want_branch:
        git_root = _find_git_root(root)
        if git_root is None:
            print("ERR: no git repo found; branch step skipped", file=sys.stderr)
            return 1
        brc = subprocess.run(
            ["git", "-C", str(git_root), "checkout", "-b", branch_name],
            capture_output=True, text=True)
        if brc.returncode != 0:
            print(f"ERR git checkout -b {branch_name}: {brc.stderr.strip()}",
                  file=sys.stderr)
            return 1
        print(f"opened branch {branch_name}")

    print(f"Rollover to season {new_season} complete.")
    print("Next commands (prime):")
    print("  * the three advisors each take a vision")
    print("  * perpetual directors bootstrap their goals and hang each under its vision")

    return 0


# ---------------------------------------------------------------------------
# merge-up — per-parent branch merge into the recorded base branch
# ---------------------------------------------------------------------------
#
# `hypothesis:l3w4-parent-branch-merge-up`: a dispatched parent runs in its own
# git worktree on `loop/<slug>-<agent8>@s<N>`; a season seat then merges that
# branch upward with `season.py merge-up <branch>`, which:
#   * merges `--no-ff` into the branch's recorded BASE_BRANCH (never a
#     hardcoded season -- layer-agnostic, so a director branch cuts parents
#     and a parent branch cuts kids and each climbs one layer at a time),
#   * runs the suite on the merged tree and REFUSES (aborts the merge, leaves
#     the branch and worktree in place, reports the branch name) on red,
#   * on green removes the worktree and leaves the merge commit in place --
#     hashes are never rewritten (no rebase).
#
# The layer-agnostic base is windows: git_common_root resolves the MAIN
# checkout from any worktree depth, so a seat running inside a linked worktree
# still merges against the main repo's branch namespace.

DEFAULT_SUITE = "python3 -m pytest extensions/agi/tests/ -q"


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    """Run git in the given repo root, capturing output."""
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True)


def _current_branch(root: Path) -> str | None:
    out = _git(root, "branch", "--show-current")
    if out.returncode != 0:
        return None
    name = out.stdout.strip()
    return name or None


def _recorded_field(record_path: Path | None, key: str) -> str | None:
    """Read `key` from a JSON lease / agent record, if present."""
    if record_path is None:
        return None
    try:
        data = json.loads(record_path.read_text())
    except (OSError, ValueError):
        return None
    val = data.get(key)
    return val if isinstance(val, str) and val else None


def cmd_merge_up(root: Path, args) -> int:
    """`season.py merge-up <branch>` -- merge a branch --no-ff into its base."""
    git_root = locations.git_common_root(root)
    if git_root is None or not (git_root / ".git").exists():
        print("ERR: no git repo found", file=sys.stderr)
        return 1

    branch = args.branch
    record_path = Path(args.record).resolve() if args.record else None

    base = (args.target
            or _recorded_field(record_path, "base_branch")
            or _current_branch(git_root))
    if not base:
        print("ERR: cannot determine a base branch (detached HEAD?); "
              "pass --target", file=sys.stderr)
        return 1

    suite = (args.suite or _recorded_field(record_path, "suite")
             or DEFAULT_SUITE)
    worktree = (args.worktree or _recorded_field(record_path, "worktree"))

    # FALSE-GREEN guard: refuse a branch that carries no commits beyond its
    # base. Merging a zero-ahead branch produces a no-op merge commit that
    # reads as a green merge of nothing -- exactly how an empty loop branch
    # used to sail through every round and a human had to finish by hand.
    ahead = _git(git_root, "rev-list", "--count", f"{base}..{branch}")
    if ahead.returncode != 0:
        print(f"ERR cannot count {branch} ahead of {base}: "
              f"{ahead.stderr.strip()}", file=sys.stderr)
        return 1
    n_ahead = ahead.stdout.strip()
    if n_ahead == "0":
        print(f"REFUSED: {branch} is zero commits ahead of {base} -- "
              f"nothing to merge", file=sys.stderr)
        return 1
    print(f"{branch} is {n_ahead} commit(s) ahead of {base}")

    cur = _current_branch(git_root)
    if cur != base:
        sw = _git(git_root, "checkout", base)
        if sw.returncode != 0:
            print(f"ERR cannot check out base branch {base}: "
                  f"{sw.stderr.strip()}", file=sys.stderr)
            return 1
        print(f"checked out {base}")

    # Stage the merge WITHOUT committing -- the suite votes before the merge
    # commit is born, so a red suite can still `git merge --abort` and leave
    # the branch intact. --no-ff so hashes are never rewritten.
    mg = _git(git_root, "merge", "--no-ff", "--no-commit", branch)
    if mg.returncode != 0:
        print(f"ERR merge --no-ff {branch}: {mg.stderr.strip()}",
              file=sys.stderr)
        return 1
    # Never claim the merge before its commit exists -- a pretence of green is
    # indistinguishable from a real green, which is why the old success line
    # printed before anything had landed.
    print(f"staged merge of {branch} into {base} (suite gate pending)")

    # Suite-green gate on the merged tree.
    suite_proc = subprocess.run(suite, shell=True, cwd=str(git_root),
                                capture_output=True, text=True)
    if suite_proc.returncode != 0:
        ab = _git(git_root, "merge", "--abort")
        print(f"REFUSED: suite red after merging {branch} into {base} -- "
              f"merge aborted, branch {branch} left in place")
        if ab.returncode != 0:
            print(f"  (warn: git merge --abort failed: {ab.stderr.strip()})",
                  file=sys.stderr)
        return 1

    # Green: finalize the merge commit (default merge message, two parents).
    cmt = _git(git_root, "commit", "--no-edit")
    if cmt.returncode != 0:
        # FALSE-RED guard: `git commit` can return non-zero even after the
        # merge has in fact landed, and with blank stderr -- reporting failure
        # then lies in the same direction as the old false green. Judge by the
        # merge state, not the code: MERGE_HEAD exists only while a merge is
        # still unborn, so its absence after a failed commit means the merge
        # commit really exists and we should treat it as green.
        still_merging = (_git(git_root, "rev-parse", "--verify",
                              "MERGE_HEAD").returncode == 0)
        if still_merging:
            print(f"ERR finalize merge commit: "
                  f"{cmt.stderr.strip() or '(no stderr from git)'}",
                  file=sys.stderr)
            return 1
        # The merge actually landed; git merely mis-reported. Say so rather
        # than cry wolf and strand the worktree on a success.
        print(f"merged {branch} --no-ff into {base} (finalize returned "
              f"non-zero {cmt.returncode} but the merge commit exists; "
              f"treating as green)")
    else:
        print(f"merged {branch} --no-ff into {base}")

    # Green: remove the worktree (this branch's job is done).
    if worktree:
        wt = _git(git_root, "worktree", "remove", worktree)
        if wt.returncode != 0:
            # The suite is green and the branch is merged, so any uncommitted
            # or untracked bytes still in the scratch worktree are throwaway.
            wt2 = _git(git_root, "worktree", "remove", "--force", worktree)
            if wt2.returncode != 0:
                print(f"  (warn: worktree remove failed:"
                      f" {wt2.stderr.strip()})", file=sys.stderr)
            else:
                print(f"removed worktree {worktree} (forced; stray uncommitted"
                      f" bytes discarded)")
        else:
            print(f"removed worktree {worktree}")

    print(f"merge-up of {branch} >> {base} complete; suite green")
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
    p_judge.add_argument("--quorum", action="store_true", default=False,
                         help="review through the advisor quorum: vote on"
                              " alignment from a room (3-0/2-1 stamps,"
                              " 1-1-1 or --morals -> audience prime, no stamp)")
    p_judge.add_argument("--room", default="tier3-quorum",
                         help="quorum room to tally votes from")
    p_judge.add_argument("--round", dest="judge_round", default="",
                         help="round the votes belong to (default: AGI_LOOP)")
    p_judge.add_argument("--comms-root", default="",
                         help="override the comms root (default: config)")

    # rollover
    p_rollover = sub.add_parser("rollover", help="Print or perform season rollover")
    p_rollover.add_argument("--dry-run", dest="dry_run_explicit",
                            action="store_true", default=False,
                            help="Only print what would happen")
    p_rollover.add_argument("--debug", action="store_true", help="Show debug info",
                            dest="debug")
    p_rollover.add_argument("--visions-from", default="",
                            help="dir or file of markdown vision bodies (owner text "
                                 "verbatim); else generic count printed")
    p_rollover.add_argument("--name", default="",
                            help="name season 1 in the ladder's season_names "
                                 "(e.g. genesis)")
    p_rollover.add_argument("--branch", action="store_true", default=False,
                            help="open season/s<N> with git checkout -b after the "
                                 "graph writes (never pushes)")
    p_rollover.add_argument("--allow-unjudged", action="store_true", default=False,
                            help="proceed even while a season-current overview lacks "
                                 "a judgment")

    # retag
    p_retag = sub.add_parser("retag",
                             help="Backfill season on every node that lacks it")
    p_retag.add_argument("--dry-run", action="store_true", default=False,
                         help="Print what would happen and write nothing")
    p_retag.add_argument("--actor", default="",
                         help="edited_by for non-moral stamps (default: season.py)")
    p_retag.add_argument("--session", default="",
                         help="thought_session for stamps (default: season)")

    # merge-up
    p_merge = sub.add_parser(
        "merge-up",
        help="Merge a loop branch --no-ff into its base, suite-green gate")
    p_merge.add_argument("branch", help="loop/<slug>-<agent8>@s<N> branch to merge")
    p_merge.add_argument("--target", default="",
                         help="base branch to merge into (default: recorded "
                              "base_branch, else current branch)")
    p_merge.add_argument("--suite", default="",
                         help="suite command; non-zero aborts the merge")
    p_merge.add_argument("--worktree", default="",
                         help="worktree path to remove on green")
    p_merge.add_argument("--record", default="",
                         help="JSON lease/agent record supplying base_branch, "
                              "suite, worktree")

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
    elif args.command == "merge-up":
        return cmd_merge_up(root, args)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())