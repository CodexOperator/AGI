#!/usr/bin/env python3
"""dashboard.py — a read-only terminal view of the graph, built for a HUMAN (G9.1).

Every other artefact in this system is written for an agent: `INJECTION.md` is
a spawn prompt, `GOALS.md` and `TODO.md` are dense on purpose, the ASCII map
caps at 200 lines and truncates silently. None of them assume the reader is a
person who has never seen this project's vocabulary. This script does.

If you don't know what a "chain" or a "verdict" is, that's fine — this output
defines each term the first time it uses it and never assumes you looked
anything up.

INVARIANT (non-negotiable, see nodes/goal/g9.md in the tree repo): this
script is a READER, never a WRITER. It must be safe to run at any moment,
including mid-iteration of the loop it is watching. It:
  - opens no file in this project for writing
  - creates no directory
  - runs no `git` subcommand that mutates history or the working tree
  - never calls a snapshot script, the CLI, or the driver

It also renders the graph's *damage*, not a flattering picture of it:
truncated chain search, dangling references, verdicts that claim evidence
without any real evidence behind them, and declared-but-empty goals are
surfaced by name, with counts — never hidden behind a clean-looking summary.

Usage:
    python3 bin/dashboard.py [--project PATH] [--watch [SECONDS]]
                              [--no-color] [--section NAME]

    --project PATH   project root (default: walk up from cwd for
                      agi-tree.config.json / autoresearch-tree.config.json)
    --watch [N]      redraw every N seconds (default 10). Ctrl-C exits
                      cleanly. Meant to sit in a split terminal next to a
                      Claude Code session.
    --no-color       disable ANSI colour. Colour also auto-disables when
                      stdout is not a terminal.
    --section NAME   print only one section: goals, metrics, health,
                      activity. Default: all of them.

Standard library only. No new dependencies.
"""
from __future__ import annotations

import argparse
import io
import re
import shutil
import subprocess
import sys
import textwrap
import time
from collections import Counter
from contextlib import redirect_stderr
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = BIN_DIR.parent

# metrics.py is the single source of truth for every number this dashboard
# shows (TODO.md H3) — it is imported, never reimplemented, per the brief.
sys.path.insert(0, str(BIN_DIR))
import metrics  # noqa: E402
import evidence_gate  # noqa: E402

SECTIONS = ("goals", "metrics", "health", "activity")

# Node-type stage order for a chain that runs to completion. Used only to
# describe *how far* a goal's work has gotten — never as a score.
STAGE_ORDER = [
    "idea", "hypothesis", "experiment", "verdict", "mvp",
    "outcome", "bigger_outcome", "bigger-outcome",
    "app_purpose", "app-purpose", "task",
]

ID_RE = re.compile(r'^id:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)

STATUS_LABEL = {
    "active": "being worked now",
    "horizon": "declared, not started",
    "complete": "done",
    "mothballed": "shelved",
}


# --------------------------------------------------------------------------
# colour
# --------------------------------------------------------------------------

class Palette:
    def __init__(self, enabled: bool):
        self.enabled = enabled

    def _wrap(self, code: str, text: str) -> str:
        if not self.enabled:
            return text
        return f"\x1b[{code}m{text}\x1b[0m"

    def bold(self, t): return self._wrap("1", t)
    def dim(self, t): return self._wrap("2", t)
    def red(self, t): return self._wrap("31", t)
    def green(self, t): return self._wrap("32", t)
    def yellow(self, t): return self._wrap("33", t)
    def blue(self, t): return self._wrap("34", t)
    def cyan(self, t): return self._wrap("36", t)

    def status(self, status: str, t: str) -> str:
        if status == "active":
            return self.green(t)
        if status == "complete":
            return self.blue(t)
        if status == "horizon":
            return self.dim(t)
        return self.yellow(t)  # unrecognised status — worth the eye catch


# --------------------------------------------------------------------------
# root resolution — read-only, mirrors metrics.py / cli.py / grid.py
# --------------------------------------------------------------------------

def find_root(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit).resolve()
        if metrics.config_path(p) is None:
            print(f"ERR: no agi-tree.config.json (or legacy "
                  f"autoresearch-tree.config.json) found under {p}",
                  file=sys.stderr)
            sys.exit(1)
        return p
    return metrics._find_root(Path.cwd())


# --------------------------------------------------------------------------
# data collection — every function here is read-only
# --------------------------------------------------------------------------

def _descendants(g, node_id: str) -> set[str]:
    """BFS over the in-memory child pointers metrics._load_graph wires from
    each node's `parents:` frontmatter field. Pure read of the Graph object;
    touches no file."""
    seen = {node_id}
    stack = [node_id]
    while stack:
        cur = stack.pop()
        n = g.get_node(cur)
        if n is None:
            continue
        for c in n.children:
            if c not in seen:
                seen.add(c)
                stack.append(c)
    seen.discard(node_id)
    return seen


def _stage_rank(node_type: str) -> int:
    try:
        return STAGE_ORDER.index(node_type)
    except ValueError:
        return -1


def collect_goals(g, fm_by_id: dict) -> list[dict]:
    """One record per goal node: status, seeds declared vs resolved, and how
    much real work (if any) sits under it."""
    out = []
    for n in g.nodes:
        if n.type != "goal":
            continue
        _path, fm = fm_by_id.get(n.id, (None, {}))
        seeds = fm.get("seeds") or []
        if not isinstance(seeds, list):
            seeds = [seeds]
        seeds_resolved = sum(1 for s in seeds if g.has_node(str(s)))
        desc = _descendants(g, n.id)
        types = Counter(g.get_node(d).type for d in desc)
        furthest = max((_stage_rank(t) for t in types), default=-1)
        out.append({
            "id": n.id,
            "goal_id": fm.get("goal_id", n.id),
            "title": fm.get("title", n.id),
            "status": fm.get("status", "unknown"),
            "goal_kind": fm.get("goal_kind", "unknown"),
            "parents": fm.get("parents") or [],
            "seeds_declared": len(seeds),
            "seeds_resolved": seeds_resolved,
            "built_count": len(desc),
            "furthest_stage": STAGE_ORDER[furthest] if furthest >= 0 else None,
            "is_stub": len(desc) == 0,
        })
    out.sort(key=lambda r: _goal_sort_key(r["goal_id"]))
    return out


def _goal_sort_key(goal_id: str):
    # "G9.1" -> (9, 1); "G9" -> (9, 0); "S1" -> (0, 1) sorts short-terms first
    m = re.match(r"^([A-Za-z]*)(\d+)(?:\.(\d+))?$", str(goal_id))
    if not m:
        return (999, 0, str(goal_id))
    return (int(m.group(2)), int(m.group(3) or 0), str(goal_id))


def _naive_evidence_count(value) -> int:
    """What `evidence_runs` would count as if trusted at face value: list
    length, a direct int, or a digit string. Deliberately reimplemented here
    rather than imported from `evidence_gate.normalize_evidence_runs`.

    That function's contract changed *while this dashboard was being built*
    — a sibling fix for the same defect this function detects (goal:g3.1 in
    the tree repo) landed mid-session and gave `normalize_evidence_runs` a
    required `corpus=` keyword, with `corpus=None` now failing every list
    closed to 0. Depending on it here would make the "naive vs resolved"
    comparison below silently break every time that upstream contract moves
    again. This tiny, stable duplicate is the deliberate fix: it reimplements
    ~4 lines of pure arithmetic, not the evidence-gate *policy* (`metrics.py`
    is still the only source of the actual `evidence_fraction` figure).
    """
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return max(value, 0)
    if isinstance(value, (list, tuple, set)):
        return len(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return 0


def resolved_evidence_stats(nodes_dir: Path, g) -> dict:
    """The general form of the sentinel-evidence defect (goal:g3.1 in the
    tree repo): `evidence_runs` is only real evidence if its entries resolve
    to an actual node in this graph. `evidence_runs: [synthetic]` — or any
    other string that isn't a live node id — inflates a naive count without
    a single experiment having run.

    This does not special-case the string "synthetic". Any list entry that
    fails `g.has_node(entry)` is unresolved, including a bare integer count
    (`evidence_runs: 3`), which fails closed here because there is no id in
    it to check — the same "fail closed, not a silent pass" rule the tree
    repo's own goal node prescribes for this defect.

    Returns both the naive count and the resolved count so the caller can
    show the gap between them directly, independent of whether the writer
    path (`evidence_gate.py`) currently applies that same resolution itself.
    """
    asserting = 0
    naive_backed = 0
    resolved_backed = 0
    sentinel_only = 0  # naive-backed but resolves to nothing real
    examples: list[str] = []
    for _nf, fm in metrics._iter_frontmatter(nodes_dir):
        v = fm.get("verdict")
        if not isinstance(v, str) or not v.strip() or v.strip() == "pending":
            continue
        asserting += 1
        er = fm.get("evidence_runs")
        naive_runs = _naive_evidence_count(er)
        resolved = 0
        if isinstance(er, (list, tuple, set)):
            resolved = sum(1 for e in er if isinstance(e, str) and g.has_node(e))
        if naive_runs >= 1:
            naive_backed += 1
        if resolved >= 1:
            resolved_backed += 1
        elif naive_runs >= 1:
            sentinel_only += 1
            if len(examples) < 5:
                examples.append(f"{fm.get('id', '?')} evidence_runs={er!r}")
    return {
        "asserting": asserting,
        "naive_backed": naive_backed,
        "naive_fraction": round(naive_backed / asserting, 3) if asserting else 0.0,
        "resolved_backed": resolved_backed,
        "resolved_fraction": round(resolved_backed / asserting, 3) if asserting else 0.0,
        "sentinel_only": sentinel_only,
        "sentinel_examples": examples,
    }


def find_duplicate_ids(nodes_dir: Path) -> list[tuple[str, Path, Path]]:
    """Node files whose `id:` collides with one already seen (sorted walk).

    graph_core.loader.load_directory() silently keeps the first file and
    drops every later one for the same id (`if not g.has_node(...)`) — so a
    node that looks present in a listing may not actually be in the graph at
    all. This is graph damage the human needs to see; it costs one directory
    walk and zero writes.
    """
    seen: dict[str, Path] = {}
    dupes: list[tuple[str, Path, Path]] = []
    if not nodes_dir.is_dir():
        return dupes
    for f in sorted(nodes_dir.rglob("*.md")):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = ID_RE.search(text)
        if not m:
            continue
        nid = m.group(1).strip()
        if nid in seen:
            dupes.append((nid, seen[nid], f))
        else:
            seen[nid] = f
    return dupes


def dangling_and_orphans(g) -> dict:
    dangling = []
    no_parent_by_type: Counter = Counter()
    for n in g.nodes:
        if not n.parents:
            no_parent_by_type[n.type] += 1
        for p in n.parents:
            if not g.has_node(p):
                dangling.append((n.id, p))
    return {"dangling": dangling, "no_parent_by_type": no_parent_by_type}


def chain_health(g, nodes_dir: Path) -> dict:
    """Chain-finding stats, WITHOUT the pickle warm-cache.

    chain_engine.chains.find_chains(graph_dir=...) writes
    `<nodes_dir>/.chain_cache.pkl` when given a graph_dir — a write this
    dashboard's read-only invariant forbids. Passing `graph_dir=None`
    disables that cache entirely (per its own docstring) at the cost of
    always doing a cold traversal. On the 534-node agi-tree corpus that
    traversal is well under a second, which is cheap enough to always pay
    for the guarantee.
    """
    result = {
        "available": False, "chain_count": 0, "longest": 0,
        "truncated": False, "truncated_reason": None,
    }
    try:
        from chain_engine.chains import find_chains
    except ImportError:
        return result
    result["available"] = True
    buf = io.StringIO()
    with redirect_stderr(buf):
        chains = find_chains(g, graph_dir=None)
    result["chain_count"] = len(chains)
    result["longest"] = max((len(c) for c in chains), default=0)
    warn = buf.getvalue()
    if "truncated" in warn:
        result["truncated"] = True
        m = re.search(r"truncated \(([^)]+)\)", warn)
        result["truncated_reason"] = m.group(1) if m else warn.strip()
    return result


def recent_activity(root: Path) -> dict:
    """Last commit touching nodes/, read via `git log` (never `git add`,
    `commit`, `checkout`, or anything else that mutates). Falls back to
    node mtimes if this isn't a git repo — either way the source used is
    named in the output so the reader isn't left guessing.
    """
    out = {"source": None, "summary": None, "files_changed": 0, "when": None}
    is_repo = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--git-dir"],
        capture_output=True, text=True, timeout=5,
    ).returncode == 0
    if is_repo:
        res = subprocess.run(
            ["git", "-C", str(root), "log", "-1",
             "--format=%h|%ar|%s", "--", "nodes"],
            capture_output=True, text=True, timeout=5,
        )
        line = res.stdout.strip()
        if res.returncode == 0 and line:
            sha, when, subject = line.split("|", 2)
            files = subprocess.run(
                ["git", "-C", str(root), "diff", "--name-only",
                 f"{sha}^", sha, "--", "nodes"],
                capture_output=True, text=True, timeout=5,
            )
            n_files = len([ln for ln in files.stdout.splitlines() if ln.strip()])
            out.update(source="git log (last commit touching nodes/)",
                       summary=subject, when=when, files_changed=n_files,
                       commit=sha)
            return out
    # Fallback: newest mtime under nodes/ — read-only stat(), no git needed.
    nodes_dir = root / "nodes"
    newest = None
    newest_path = None
    if nodes_dir.is_dir():
        for f in nodes_dir.rglob("*.md"):
            try:
                mt = f.stat().st_mtime
            except OSError:
                continue
            if newest is None or mt > newest:
                newest, newest_path = mt, f
    if newest is not None:
        out.update(
            source="newest file mtime under nodes/ (not a git repo, or no "
                   "commits touch nodes/)",
            summary=str(newest_path.relative_to(root)),
            when=time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(newest)),
        )
    return out


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def _wrap(text: str, width: int, indent: str = "") -> list[str]:
    w = max(20, width - len(indent))
    return [indent + ln for ln in textwrap.wrap(text, w)] or [indent]


def render_goals(g, fm_by_id: dict, pal: Palette, width: int) -> list[str]:
    goals = collect_goals(g, fm_by_id)
    real = sum(1 for r in goals if not r["is_stub"])
    stub = len(goals) - real
    lines = [pal.bold("GOALS — what exists, and what is actually being worked"), ""]
    lines += _wrap(
        f"{len(goals)} goals are declared. {real} have at least one real node "
        f"built under them; {stub} are declared with nothing built yet "
        "(a \"stub\" below).", width)
    lines.append("")

    by_parent: dict[str, list[dict]] = {}
    top: list[dict] = []
    for r in goals:
        parents = [p for p in r["parents"] if isinstance(p, str)]
        if parents:
            by_parent.setdefault(parents[0], []).append(r)
        else:
            top.append(r)

    def render_row(r: dict, indent: str) -> list[str]:
        # Pad the PLAIN tag first, then colour it — colouring first and
        # padding after would count invisible ANSI bytes as visible columns
        # and misalign every row differently depending on status length.
        tag_plain = f"[{r['status']}]".ljust(13)
        tag = pal.status(r["status"], tag_plain)
        status_note = STATUS_LABEL.get(r["status"], f"unrecognised status: {r['status']!r}")
        prefix = f"{indent}{tag_plain}{r['goal_id']:<6} "
        title = r["title"]
        room = width - len(prefix)
        if room > 10 and len(title) > room:
            title = title[:room - 1] + "…"
        head = f"{indent}{tag}{r['goal_id']:<6} {title}"
        rows = [head]
        if r["is_stub"]:
            seed_note = (f"{r['seeds_declared']} seed(s) declared, none built yet"
                         if r["seeds_declared"] else "no seeds declared either")
            detail = f"{indent}    stub — {seed_note}. ({status_note})"
        else:
            stage = r["furthest_stage"] or "?"
            seed_note = ""
            if r["seeds_declared"] and r["seeds_resolved"] < r["seeds_declared"]:
                seed_note = (f"; {r['seeds_declared'] - r['seeds_resolved']} of "
                             f"{r['seeds_declared']} declared seed(s) don't "
                             "point at a real node")
            detail = (f"{indent}    real — {r['built_count']} node(s) built, "
                     f"furthest reached: {stage}{seed_note}. ({status_note})")
        rows += _wrap(detail, width)
        return rows

    for r in top:
        lines += render_row(r, "")
        for child in sorted(by_parent.get(r["id"], []), key=lambda c: c["goal_id"]):
            lines += render_row(child, "   ")
    return lines


def render_metrics(m: dict, cfg: dict, resolved: dict, width: int, pal: Palette) -> list[str]:
    lines = [pal.bold("METRICS — where the graph stands, with known contamination named"), ""]

    primary = metrics.primary_metric_name(cfg)
    if primary in metrics.GAMEABLE_METRICS:
        lines += _wrap(
            f"!! this project is configured to score itself on '{primary}', "
            "which can be inflated by adding meaningless steps with no real "
            f"progress. Read '{metrics.DEFAULT_METRIC_PRIMARY}' below instead.",
            width)
    else:
        val = m.get(primary, "?")
        lines += _wrap(
            f"Scored on: {primary} = {val}  (the number this project is "
            "actually trying to move)", width)
    lines.append("")

    lines.append(f"Outcome Coverage:  {m['outcome_coverage']}  "
                 "(mvps per hypothesis — how often an idea actually reaches "
                 "a working prototype, not just a plan)")
    lines.append(f"Node count:        {m['node_count']}   Edges: {m['edge_count']}")
    lines.append(f"Average Depth:     {m['avg_chain_depth']}  "
                 "(average number of steps a node sits from where its work started)")
    lines.append(f"Branching Factor:  {m['chain_branching_factor']}  "
                 "(average number of next-steps each branching node spawns)")
    lines.append(pal.dim(
        f"Longest Chain:     {m['longest_chain_length']} steps  "
        "(DESCRIPTIVE ONLY — this project was gamed to fake 2000-step "
        "chains that carried no real work; never treat this as a target)"))
    lines.append("")

    # Evidence Fraction: `evidence_runs` can be satisfied by writing
    # something that ISN'T a real reference (a placeholder string, a bare
    # count with nothing to check) — see resolved_evidence_stats() for the
    # general rule. What matters here is the GAP between "trusted at face
    # value" (naive) and "checked against the graph" (resolved); which one
    # `metrics.py` itself is currently reporting is measured live rather
    # than assumed, because the writer path this number is meant to police
    # is itself active development (see the caveats in the experiment node
    # this dashboard was built to write).
    reported = m["evidence_fraction"]
    naive, resolvedf = resolved["naive_fraction"], resolved["resolved_fraction"]
    matches_naive = abs(reported - naive) < 1e-9
    matches_resolved = abs(reported - resolvedf) < 1e-9 and not matches_naive
    contaminated = resolved["sentinel_only"] > 0

    if not contaminated:
        lines.append("Evidence Fraction — no unresolved evidence entries found:")
    elif matches_resolved:
        lines.append(pal.green(
            "Evidence Fraction — currently reports the CHECKED value "
            "(good — but read on, unresolved entries still exist elsewhere):"))
    else:
        lines.append(pal.yellow("Evidence Fraction — CONTAMINATED, read the caveat below:"))
    lines += _wrap(
        f"  metrics.py currently reports: {reported}  "
        f"({m['verdicts_evidence_backed']} of {m['verdicts_asserting']} "
        "verdicts that claim 'proved' or 'disproved' carry an "
        "`evidence_runs` entry, by metrics.py's own rule)", width)
    lines += _wrap(
        "  a verdict can claim evidence by writing something in "
        "`evidence_runs` that ISN'T a reference to any real experiment — a "
        "placeholder string, or a number with nothing behind it to check. "
        f"If trusted at face value with no checking at all, this graph's "
        f"figure would be: {naive}  ({resolved['naive_backed']} of "
        f"{resolved['asserting']}).", width)
    lines += _wrap(
        f"  checked against the graph (only counts evidence that resolves "
        f"to a real node): {resolvedf}  ({resolved['resolved_backed']} of "
        f"{resolved['asserting']}).", width)
    if resolved["sentinel_only"]:
        lines += _wrap(
            f"  {resolved['sentinel_only']} verdict(s) currently pass the "
            "naive check on an entry that resolves to nothing real.", width)
    if resolved["sentinel_examples"]:
        lines.append("  example unresolved entries:")
        for ex in resolved["sentinel_examples"]:
            lines.append(f"    - {ex}")
    lines.append("")
    lines.append(f"Unevidenced decisive verdicts (claim proved/disproved, "
                 f"evidence_runs empty by metrics.py's own rule): "
                 f"{m['unevidenced_decisive_verdicts']}")
    return lines


def render_health(g, nodes_dir: Path, pal: Palette, width: int) -> list[str]:
    lines = [pal.bold("HEALTH WARNINGS — the graph's damage, not a clean picture of it"), ""]

    da = dangling_and_orphans(g)
    dangling = da["dangling"]
    no_parent = da["no_parent_by_type"]

    lines.append(pal.status("horizon" if not dangling else "mothballed",
                            f"Dangling parent references: {len(dangling)}"))
    if dangling:
        lines += _wrap(
            "A node points at a parent id that does not exist anywhere in "
            "the graph — the link is broken. First few:", width, "  ")
        for child, missing in dangling[:6]:
            lines.append(f"    {child}  ->  {missing} (missing)")
        if len(dangling) > 6:
            lines.append(f"    ... and {len(dangling) - 6} more")
    lines.append("")

    total_no_parent = sum(no_parent.values())
    lines.append(f"Nodes with no parent at all: {total_no_parent}")
    lines += _wrap(
        "(expected for goal/idea nodes, which are meant to be roots; "
        "unexpected for anything downstream of an idea)", width, "  ")
    for t, c in sorted(no_parent.items(), key=lambda kv: -kv[1]):
        lines.append(f"    {t:<16} {c}")
    lines.append("")

    dupes = find_duplicate_ids(nodes_dir)
    lines.append(pal.status("horizon" if not dupes else "mothballed",
                            f"Duplicate node ids on disk: {len(dupes)}"))
    if dupes:
        lines += _wrap(
            "Two files declare the same id. The loader silently keeps only "
            "the first (alphabetically) and drops the rest — the dropped "
            "file's content is invisible to every tool that reads this "
            "graph, including this dashboard, even though the file still "
            "exists on disk. First few:", width, "  ")
        def _rel(p: Path) -> str:
            try:
                return str(p.relative_to(nodes_dir))
            except ValueError:
                return p.name

        for nid, kept, shadowed in dupes[:6]:
            lines.append(f"    {nid}: kept {_rel(kept)}, hid {_rel(shadowed)}")
        if len(dupes) > 6:
            lines.append(f"    ... and {len(dupes) - 6} more")
    lines.append("")

    ch = chain_health(g, nodes_dir)
    if not ch["available"]:
        lines.append(pal.yellow(
            "Chain search: unavailable (chain_engine not importable in this "
            "project) — chain-based stats below are not shown."))
    else:
        lines.append(f"Chain search: {ch['chain_count']} chain(s) found, "
                     f"longest is {ch['longest']} steps.")
        if ch["truncated"]:
            lines.append(pal.yellow(
                f"  !! search was CUT SHORT ({ch['truncated_reason']}) — the "
                "true chain count and longest chain may be higher than what "
                "is shown. This is a safety limit, not a bug: without it, a "
                "sufficiently tangled graph can hang the whole tool."))
        else:
            lines.append("  search completed; not cut short.")
    return lines


def render_activity(act: dict, width: int, pal: Palette) -> list[str]:
    lines = [pal.bold("RECENT ACTIVITY — what the loop did last"), ""]
    lines.append(f"source: {act['source'] or 'none found'}")
    if act.get("summary"):
        lines += _wrap(f"when: {act['when']}", width)
        lines += _wrap(f"what: {act['summary']}", width)
        if "files_changed" in act and act.get("commit"):
            lines.append(f"files touched under nodes/: {act['files_changed']}")
    else:
        lines.append("(no activity found — empty project, or nodes/ has "
                     "never been touched)")
    return lines


# --------------------------------------------------------------------------
# top-level render
# --------------------------------------------------------------------------

def gather(root: Path) -> dict:
    """One read pass over the corpus. Everything downstream is pure formatting."""
    g = metrics._load_graph(root)
    cfg = metrics.read_config(root)
    m = metrics.compute(root)
    nodes_dir = root / "nodes"
    resolved = resolved_evidence_stats(nodes_dir, g)
    fm_by_id = {}
    for nf, fm in metrics._iter_frontmatter(nodes_dir):
        nid = fm.get("id")
        if isinstance(nid, str):
            fm_by_id[nid] = (nf, fm)
    act = recent_activity(root)
    return {
        "g": g, "cfg": cfg, "m": m, "nodes_dir": nodes_dir,
        "resolved": resolved, "fm_by_id": fm_by_id, "act": act,
    }


def render(root: Path, data: dict, pal: Palette, width: int,
          section: str | None) -> str:
    out: list[str] = []
    if section is None:
        out.append(pal.bold(f"agi-tree dashboard — {root}"))
        out.append(pal.dim(
            time.strftime("generated %Y-%m-%d %H:%M:%S UTC", time.gmtime())
            + "  (read-only view — this tool writes nothing)"))
        out.append("=" * min(width, 78))
        out.append("")

    parts = {
        "goals": lambda: render_goals(data["g"], data["fm_by_id"], pal, width),
        "metrics": lambda: render_metrics(data["m"], data["cfg"], data["resolved"], width, pal),
        "health": lambda: render_health(data["g"], data["nodes_dir"], pal, width),
        "activity": lambda: render_activity(data["act"], width, pal),
    }
    order = [section] if section else list(SECTIONS)
    for i, name in enumerate(order):
        out += parts[name]()
        if i < len(order) - 1:
            out.append("")
            out.append("-" * min(width, 78))
            out.append("")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Read-only terminal dashboard of the graph, for a human "
                    "reader who does not know this project's vocabulary.")
    ap.add_argument("--project", default=None,
                    help="project root (default: walk up from cwd)")
    ap.add_argument("--watch", nargs="?", const=10, default=None, type=float,
                    metavar="SECONDS",
                    help="redraw every SECONDS (default 10) until Ctrl-C")
    ap.add_argument("--no-color", action="store_true",
                    help="disable ANSI colour")
    ap.add_argument("--section", choices=SECTIONS, default=None,
                    help="print only this section")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = find_root(args.project)

    use_color = (not args.no_color) and sys.stdout.isatty()
    pal = Palette(use_color)
    width = shutil.get_terminal_size(fallback=(80, 24)).columns
    width = max(40, width)

    def draw_once() -> None:
        data = gather(root)
        text = render(root, data, pal, width, args.section)
        print(text, end="")

    if args.watch is None:
        draw_once()
        return 0

    interval = max(1.0, float(args.watch))
    try:
        while True:
            if sys.stdout.isatty():
                sys.stdout.write("\x1b[2J\x1b[H")
            draw_once()
            print(pal.dim(f"\n(refreshing every {interval:g}s — Ctrl-C to stop)"))
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nstopped.")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
