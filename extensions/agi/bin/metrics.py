#!/usr/bin/env python3
"""metrics.py — compute and emit the loop's METRIC lines (TODO.md H3).

Was an inline heredoc inside `driver.sh:emit_metrics`, which made the
metric untestable and left `longest_chain_length` as the de-facto primary.
Agents proved that metric gameable — 9 chains x 2000 hops via shortcut
cycles (`hops=2*cycle+8`) carrying no signal, and the pathological
structure then broke the render path (H0c).

The primary metric now comes from `agi-tree.config.json`
(`metric_primary`), defaulting to :data:`DEFAULT_METRIC_PRIMARY` —
never chain length. `longest_chain_length` stays as a descriptive
secondary statistic.

`evidence_fraction` is the bridge to the H4 evidence gate: the fraction
of asserting verdicts that carry `evidence_runs >= 1`. It cannot be
inflated by adding hops — only by doing experiments.

Usage:
    metrics.py <project_root>
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evidence_gate import (  # noqa: E402
    DECISIVE_VERDICTS,
    build_corpus,
    normalize_evidence_runs,
)

#: Fallback when a project's config omits `metric_primary`. Deliberately not
#: `longest_chain_length` (H3).
DEFAULT_METRIC_PRIMARY = "outcome_coverage"

#: Metrics that are descriptive only and must never be primary.
GAMEABLE_METRICS = ("longest_chain_length",)


def _load_graph(root: Path):
    proj_src = root / "src"
    if (proj_src / "graph_core").is_dir():
        sys.path.insert(0, str(proj_src))
    sys.path.insert(0, str(PLUGIN_ROOT / "src"))
    from graph_core.loader import load_directory
    from graph_core.edge import Edge

    g, loaded = load_directory(root / "nodes")
    for ln in loaded:
        for parent_id in ln.node.parents:
            if g.has_node(parent_id):
                try:
                    g.add_edge(Edge(source_id=parent_id, target_id=ln.node.id,
                                    relation="spawns"))
                except Exception:
                    pass
                pn = g.get_node(parent_id)
                if pn is not None:
                    pn.children.add(ln.node.id)
    return g


def longest_chain_length(g) -> int:
    """Longest descendant chain. Descriptive only — gameable (H3).

    Deliberately iterative. The recursive version raised RecursionError at ~990
    deep on the agi-tree corpus, whose chains were gamed to 2000 hops — the same
    defect H3b removed from render-context.py, and it aborted the whole metrics
    stage over a metric that is only descriptive. Back-edges resolve to 0 rather
    than looping, matching chain_engine's cycle convention.
    """
    cache: dict[str, int] = {}
    on_stack: set[str] = set()

    for root in g.node_ids:
        if root in cache:
            continue
        stack: list[tuple[str, bool]] = [(root, False)]
        while stack:
            nid, expanded = stack.pop()
            if expanded:
                n = g.get_node(nid)
                cache[nid] = max(
                    (cache.get(c, 0) + 1 for c in n.children if c != nid),
                    default=0,
                )
                on_stack.discard(nid)
                continue
            if nid in cache:
                continue
            n = g.get_node(nid)
            if n is None or not n.children:
                cache[nid] = 0
                continue
            on_stack.add(nid)
            stack.append((nid, True))
            for c in n.children:
                if c != nid and c not in cache and c not in on_stack:
                    stack.append((c, False))

    return max(cache.values(), default=0)


def _iter_frontmatter(nodes_dir: Path):
    import yaml
    if not nodes_dir.is_dir():
        return
    for nf in sorted(nodes_dir.rglob("*.md")):
        try:
            text = nf.read_text(encoding="utf-8")
        except Exception:
            continue
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1]) or {}
        except Exception:
            continue
        if isinstance(fm, dict):
            yield nf, fm


def evidence_stats(nodes_dir: Path) -> dict:
    """Evidence accounting over verdict-bearing nodes.

    Denominator is *asserting* verdicts — everything except `pending`.
    `pending` is excluded on purpose: H4 permits it without evidence, so
    counting it would penalise honest uncertainty.

    `evidence_runs` is resolved against the corpus (goal:g3.1 / H4c) using
    the exact same `build_corpus` + `normalize_evidence_runs` functions
    `evidence_gate.py` uses to gate a write. One definition, shared by
    import, not reimplemented here — so this metric and the gate cannot
    read the same field and disagree (that drift was the H4c root cause).
    """
    corpus = build_corpus(nodes_dir)
    asserting = 0
    backed = 0
    decisive = 0
    decisive_backed = 0
    pending = 0
    for _nf, fm in _iter_frontmatter(nodes_dir):
        v = fm.get("verdict")
        if not isinstance(v, str) or not v.strip():
            continue
        v = v.strip()
        runs = normalize_evidence_runs(fm.get("evidence_runs"), corpus=corpus)
        if v == "pending":
            pending += 1
            continue
        asserting += 1
        if runs >= 1:
            backed += 1
        if v in DECISIVE_VERDICTS:
            decisive += 1
            if runs >= 1:
                decisive_backed += 1
    return {
        "verdicts_asserting": asserting,
        "verdicts_pending": pending,
        "verdicts_evidence_backed": backed,
        "evidence_fraction": (backed / asserting) if asserting else 0.0,
        "decisive_verdicts": decisive,
        "decisive_evidence_fraction": (decisive_backed / decisive) if decisive else 0.0,
        # Gate-violation counter: should be 0 once H4 holds in both writer
        # paths. Nonzero = a bypass or a hand-edited node.
        "unevidenced_decisive_verdicts": decisive - decisive_backed,
    }


# Canonical name first; the legacy name stays accepted during the rename window.
CONFIG_NAMES = ("agi-tree.config.json", "autoresearch-tree.config.json")


def config_path(root: Path) -> Path | None:
    """First existing config file in `root`, or None if it is not a project."""
    for name in CONFIG_NAMES:
        p = root / name
        if p.exists():
            return p
    return None


def read_config(root: Path) -> dict:
    cfg_path = config_path(root)
    if cfg_path is None:
        return {}
    try:
        return json.loads(cfg_path.read_text()) or {}
    except Exception:
        return {}


def primary_metric_name(cfg: dict) -> str:
    """Config's `metric_primary`, else the non-gameable default (H3)."""
    name = cfg.get("metric_primary")
    if not isinstance(name, str) or not name.strip():
        return DEFAULT_METRIC_PRIMARY
    return name.strip()


#: Goal states whose chains still accrue score. `phasing-out` and `complete`
#: are deliberately absent (goal:g5): a retired goal's chains stay in the
#: graph and stay attributable, they just stop moving the number.
SCORING_GOAL_STATUSES = frozenset({"active", "horizon"})


def goal_attribution(nodes_dir: Path) -> dict:
    """Map every node to the goals it descends from, and score accordingly.

    goal:g5 — `status` is a field the engine acts on, not a human
    convention. Two things follow from that and both are here:

    1. A node under a `phasing-out` or `complete` goal is **excluded from
       the primary metric** but **kept attributable** — it is still in the
       graph, still reachable, still counted in the descriptive totals.
       Retiring a goal must not look like deleting its work.
    2. A node under no goal at all keeps scoring. That is deliberate and
       conservative: most of this corpus predates goal nodes, and silently
       zeroing it would be a metric change disguised as a lifecycle rule.
       Attribution is a reason to *exclude*, never the only reason to
       include.

    Returns counts, not opinions — `compute` decides what to do with them.
    """
    statuses: dict[str, str] = {}
    parents: dict[str, list] = {}
    types: dict[str, str] = {}

    for _nf, fm in _iter_frontmatter(nodes_dir):
        nid = fm.get("id")
        if not isinstance(nid, str) or not nid.strip():
            continue
        nid = nid.strip()
        types[nid] = str(fm.get("type") or "")
        raw = fm.get("parents")
        parents[nid] = [p.strip() for p in raw if isinstance(p, str) and p.strip()] \
            if isinstance(raw, (list, tuple)) else []
        if types[nid] == "goal":
            st = fm.get("status")
            statuses[nid] = st.strip() if isinstance(st, str) and st.strip() else "active"

    def goals_of(nid: str) -> set:
        """Goal ids reachable upward from `nid`. Cycle-safe by construction."""
        seen, stack, found = {nid}, list(parents.get(nid, ())), set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            if cur in statuses:
                found.add(cur)
                continue  # a goal's own parents are goals; stop at the first
            stack.extend(parents.get(cur, ()))
        return found

    scoring_mvp = scoring_hyp = 0
    retired_nodes = unattributed = 0
    for nid, ntype in types.items():
        if ntype == "goal":
            continue
        gs = goals_of(nid)
        if not gs:
            unattributed += 1
        # Retired only when every goal it answers to is retired. A node
        # shared with a live goal still earns its keep.
        scores = (not gs) or any(statuses.get(g) in SCORING_GOAL_STATUSES for g in gs)
        if not scores:
            retired_nodes += 1
            continue
        if ntype == "mvp":
            scoring_mvp += 1
        elif ntype == "hypothesis":
            scoring_hyp += 1

    by_status: dict[str, int] = defaultdict(int)
    for st in statuses.values():
        by_status[st] += 1

    return {
        "scoring_mvp_count": scoring_mvp,
        "scoring_hypothesis_count": scoring_hyp,
        "retired_goal_nodes": retired_nodes,
        "unattributed_nodes": unattributed,
        "goals_active": by_status.get("active", 0),
        "goals_horizon": by_status.get("horizon", 0),
        "goals_retired": by_status.get("phasing-out", 0) + by_status.get("complete", 0),
        "goal_count": len(statuses),
    }


def outcome_coverage(mvp_count: int, hypothesis_count: int) -> float:
    """The default primary metric: mvps per hypothesis.

    Goal-attributable — it moves only when a hypothesis actually reaches an
    mvp, so padding hops cannot shift it (H3). Shared with
    `bin/render-context.py`, which reports it in the injected map, so the map
    and the METRIC lines can never disagree about what the loop is scored on.
    """
    return mvp_count / max(hypothesis_count, 1)


def compute(root: Path) -> dict:
    g = _load_graph(root)

    by_type: dict[str, int] = defaultdict(int)
    for n in g.nodes:
        by_type[n.type] += 1

    mvp_count = by_type.get("mvp", 0)
    hyp_count = by_type.get("hypothesis", 0)
    non_leaf = [n for n in g.nodes if n.children]
    branching = sum(len(n.children) for n in non_leaf) / max(len(non_leaf), 1)
    avg_depth = sum(len(n.parents) for n in g.nodes) / max(len(g), 1)

    # goal:g5 — score over live goals only. `mvp_count` stays whole-graph so
    # the descriptive total and the scored total are both visible; a gap
    # between them is exactly how much work is parked behind retired goals.
    attr = goal_attribution(root / "nodes")

    m: dict[str, float | int | str] = {
        "longest_chain_length": longest_chain_length(g),
        "avg_chain_depth": round(avg_depth, 2),
        "mvp_count": mvp_count,
        "outcome_coverage": round(
            outcome_coverage(attr["scoring_mvp_count"],
                             attr["scoring_hypothesis_count"]), 3),
        "chain_branching_factor": round(branching, 2),
        "node_count": len(g),
        "edge_count": g.edge_count,
    }
    m.update(attr)
    ev = evidence_stats(root / "nodes")
    m.update(ev)
    m["evidence_fraction"] = round(ev["evidence_fraction"], 3)
    m["decisive_evidence_fraction"] = round(ev["decisive_evidence_fraction"], 3)
    # Composite suggested by H3: depth is only worth what the evidence
    # behind it is worth. Bounded by evidence_fraction <= 1.
    m["evidence_weighted_depth"] = round(avg_depth * ev["evidence_fraction"], 3)
    return m


def emit(root: Path, out=None) -> dict:
    out = out if out is not None else sys.stdout
    cfg = read_config(root)
    m = compute(root)
    primary = primary_metric_name(cfg)

    if primary in GAMEABLE_METRICS:
        print(
            f"!! METRIC-WARNING metric_primary='{primary}' is gameable (TODO.md H3): "
            "agents reached 9 chains x 2000 hops via shortcut cycles carrying no "
            f"signal. Move it to secondary_metrics and set metric_primary to "
            f"'{DEFAULT_METRIC_PRIMARY}' or 'evidence_fraction'.",
            file=sys.stderr,
        )
        print(f"METRIC_WARNING gameable_primary={primary}", file=out)

    # goal:g5 / L5 — rotation the engine enforces. `max_goals_active` was a
    # number in the config that nothing read, so "active" drifted into
    # meaning "declared" and the field stopped carrying information. This
    # does not refuse to run: the config value is a commitment about focus,
    # and the honest response to breaking it is to say so every iteration,
    # not to block work that is already in flight.
    max_active = (cfg.get("cc_dispatch") or {}).get("max_goals_active")
    active = m.get("goals_active", 0)
    if isinstance(max_active, int) and max_active > 0 and active > max_active:
        print(
            f"!! METRIC-WARNING goals_active={active} exceeds "
            f"cc_dispatch.max_goals_active={max_active}. Every goal marked "
            "`active` claims to be in flight; when most of them are not, the "
            "field stops distinguishing anything and the backlog becomes "
            "invisible. Move the ones you are not working to `horizon` — that "
            "is what `horizon` is for (goal:g5).",
            file=sys.stderr,
        )
        print(f"METRIC_WARNING goal_rotation={active}/{max_active}", file=out)

    for k, v in m.items():
        print(f"METRIC {k}={v}", file=out)

    if primary not in m:
        print(f"!! METRIC-WARNING metric_primary='{primary}' is not computed by "
              "metrics.py; no primary value emitted.", file=sys.stderr)
    else:
        print(f"METRIC primary_metric={primary}", file=out)
        print(f"METRIC primary_value={m[primary]}", file=out)
    return m


def _find_root(start: Path) -> Path:
    d = start.resolve()
    while d != d.parent:
        if config_path(d) is not None:
            return d
        d = d.parent
    print("ERR: no agi-tree.config.json found", file=sys.stderr)
    sys.exit(1)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(argv[0]) if argv else _find_root(Path.cwd())
    emit(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
