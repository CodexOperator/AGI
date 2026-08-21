"""Query API for the capillary DAG (hypothesis:a00-204c9d9e-1d958f).

Exposes strategic navigation queries over the research graph:
1. task_attractiveness(task_id)      — score based on descendant_count, chain_recency, type_balance
2. chain_gaps(domain)                — hypotheses in a domain with no verdict yet
3. next_best_hypothesis(weights_fn) — top-N hypotheses to extend next
4. coverage_report()                 — per-domain counts: ideas/hypotheses/experiments/verdicts/MVPs/outcomes

All functions are pure: they never mutate the graph.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from graph_core.graph import Graph
    from graph_core.types import RenderableGraph

    from .attractiveness import AttractivenessWeights
    from .types import Chain


@dataclass
class CoverageReport:
    """Per-domain coverage counts for all chain node types."""

    domain: str
    ideas: int
    hypotheses: int
    experiments: int
    verdicts: int
    mvps: int
    outcomes: int
    bigger_outcomes: int
    app_purposes: int
    total: int


# ---------------------------------------------------------------------------
# Query 1: task_attractiveness
# ---------------------------------------------------------------------------

def task_attractiveness(
    task_id: str,
    graph: "RenderableGraph",
    weights: "AttractivenessWeights | None" = None,
) -> float:
    """Score how attractive a task is for an agent to work on (Q1).

    Score = parent_chain_signal + sibling_count * 0.5 + descendent_reach

    - parent_chain_signal: +3 if task's parent hypothesis has verdict/children (on a chain)
    - sibling_count: number of siblings (other children of parent hypothesis)
    - descendent_reach: fraction of total graph reachable from task via outgoing edges

    Returns 0.0 if task_id not found.

    Args:
        task_id: the task node id
        graph: the graph
        weights: unused here (kept for API consistency with attractiveness)

    Returns:
        float attractiveness score (higher = more attractive)
    """
    node = graph.get_node(task_id)
    if node is None:
        return 0.0

    # Task nodes are leaves: parents set comes from frontmatter
    parents = node.parents
    if not parents:
        return 0.0

    # Score based on parent hypothesis: use graph edges for children
    parent = list(parents)[0]  # take first parent
    outgoing = _build_outgoing(graph)
    verdict_children = [
        e.target_id for e in graph.edges
        if e.source_id == parent and ("verdict" in e.target_id.lower() or e.target_id.startswith("verdict:"))
    ]
    experiment_children = [
        e.target_id for e in graph.edges
        if e.source_id == parent and (e.target_id.startswith("exp:") or e.target_id.startswith("experiment:"))
    ]
    task_children = [
        e.target_id for e in graph.edges
        if e.source_id == parent and e.target_id.startswith("task:")
    ]

    parent_chain_signal = 0.0
    if verdict_children:
        parent_chain_signal += 2.0  # parent has verdict, needs MVP
    elif experiment_children:
        parent_chain_signal += 1.5  # parent has experiment, needs verdict
    elif task_children:
        parent_chain_signal += 1.0  # parent has tasks, needs experiment

    # sibling_count: other tasks spawned by same hypothesis
    sibling_count = max(0, len(task_children) - 1)

    # descendent_reach: BFS descendants from task
    descendants = _bfs_descendants(task_id, graph)
    descendent_reach = len(descendants) / max(len(graph.node_ids), 1) * 10.0

    return parent_chain_signal + sibling_count * 0.5 + descendent_reach


def _build_outgoing(graph: "RenderableGraph") -> dict[str, set[str]]:
    """Build outgoing edges map: source_id -> set of target_ids."""
    outgoing: dict[str, set[str]] = {}
    for edge in graph.edges:
        outgoing.setdefault(edge.source_id, set()).add(edge.target_id)
    return outgoing


def _bfs_descendants(node_id: str, graph: "RenderableGraph") -> set[str]:
    """BFS to find all descendants of node_id via any outgoing edge."""
    outgoing = _build_outgoing(graph)
    visited: set[str] = set()
    queue = list(outgoing.get(node_id, set()))
    while queue:
        nid = queue.pop(0)
        if nid in visited:
            continue
        visited.add(nid)
        queue.extend(list(outgoing.get(nid, set())))
    return visited


# ---------------------------------------------------------------------------
# Query 2: chain_gaps
# ---------------------------------------------------------------------------

def chain_gaps(domain: str, graph: "RenderableGraph") -> list[tuple[str, str]]:
    """Return hypothesis nodes in a domain that have no verdict yet (Q2).

    Filters hypothesis nodes matching the domain and returns those with no verdict child.
    Handles both `hyp:{domain}-r{number}` and `{domain}-r{number}` naming.

    Returns list of (hypothesis_id, status) tuples sorted by r-number.

    Args:
        domain: domain name (e.g. 'graph-core', 'chain-engine')
        graph: the graph

    Returns:
        List of (hypothesis_id, status) tuples with no verdict.
    """
    import re

    # Find hypothesis nodes matching domain pattern
    hyps: list[tuple[int, str]] = []
    # Match hyp:domain-r{number} or domain-r{number}
    pattern = re.compile(rf"^(?:hyp:)?{re.escape(domain)}-r(\d+)", re.IGNORECASE)
    for nid in graph.node_ids:
        m = pattern.match(nid)
        if m:
            hyps.append((int(m.group(1)), nid))

    hyps.sort(key=lambda x: x[0])

    # For each hypothesis, check if it has a verdict child
    # Build verdict set first
    verdict_ids: set[str] = {nid for nid in graph.node_ids if nid.startswith("verdict:")}
    verdict_ids.update(nid for nid in graph.node_ids if "verdict" in nid.lower())

    # Build spawns/next outgoing edges map
    outgoing: dict[str, set[str]] = {}
    for edge in graph.edges:
        outgoing.setdefault(edge.source_id, set()).add(edge.target_id)

    gaps: list[tuple[str, str]] = []
    for _, nid in hyps:
        children = outgoing.get(nid, set())
        has_verdict = any(vid in verdict_ids or "verdict" in vid.lower() for vid in children)
        if not has_verdict:
            node = graph.get_node(nid)
            status = getattr(node, "status", "pending") if node else "pending"
            gaps.append((nid, status))

    return gaps


# ---------------------------------------------------------------------------
# Query 3: next_best_hypothesis
# ---------------------------------------------------------------------------

def next_best_hypothesis(
    graph: "RenderableGraph",
    weights: "AttractivenessWeights | None" = None,
    n: int = 5,
) -> list[tuple[str, float, int]]:
    """Return top-N hypotheses to extend next, ranked by chain-progress score (Q3).

    Considers all hypothesis nodes and computes a chain-progress score:
    - +5 if hypothesis has verdict children (on a chain, needs MVP next)
    - +3 if hypothesis has experiment children (active chain, needs verdict next)
    - +2 if hypothesis has task children (spawned, needs experiment next)
    - +1 per descendant node (more graph reach = more important)

    Args:
        graph: the graph
        weights: unused (kept for API consistency)
        n: number of results to return

    Returns:
        List of (hypothesis_id, score, descendant_count) tuples, sorted descending by score.
    """
    outgoing = _build_outgoing(graph)
    results: list[tuple[str, float, int]] = []

    for nid in graph.node_ids:
        node = graph.get_node(nid)
        if node is None:
            continue
        # Include hypothesis nodes: type == 'hypothesis' or id starts with 'hyp:'
        is_hypothesis = (
            node.type == "hypothesis"
            or nid.startswith("hyp:")
            or "hypothesis" in nid.lower()
        )
        if not is_hypothesis:
            continue

        children = outgoing.get(nid, set())
        has_verdict = any(c.startswith("verdict:") for c in children)
        has_experiment = any(c.startswith("exp:") for c in children)
        has_task = any(c.startswith("task:") for c in children)

        # Chain-progress scoring
        score = 0.0
        if has_verdict:
            score += 5.0  # needs MVP next
        elif has_experiment:
            score += 3.0  # needs verdict next
        elif has_task:
            score += 2.0  # needs experiment next
        else:
            score += 0.5  # no children yet, still possible

        descendants = len(_bfs_descendants(nid, graph))
        score += descendants * 0.1  # small bonus for graph reach

        results.append((nid, score, descendants))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:n]


# ---------------------------------------------------------------------------
# Query 4: coverage_report
# ---------------------------------------------------------------------------

def coverage_report(graph: "RenderableGraph") -> list[CoverageReport]:
    """Return per-domain coverage report: counts of each node type per domain (Q4).

    Parses node ids for domain prefix (e.g. 'graph-core', 'chain-engine') and
    counts node types within each domain.

    Returns list of CoverageReport sorted by total descending.
    """
    import re

    # Domain extraction: nodes with form "{domain}-{rest}" where domain is a known big idea
    known_domains = [
        "graph-core",
        "chain-engine",
        "schema-registry",
        "renderers",
        "embeddings",
        "environment-indexers",
        "autoresearch-tree-skill",
        "cli-invocation",
        "session-management",
        "vector-embedding-isomorphism",
        "auteurs",
        "exporters",
    ]

    # Build domain map for each node
    domain_counts: dict[str, dict[str, int]] = {d: _empty_counts() for d in known_domains}
    domain_counts["_other"] = _empty_counts()

    # Count types per domain based on parent idea node
    # Build idea -> children map
    idea_children: dict[str, set[str]] = {}
    for edge in graph.edges:
        if edge.relation == "spawns":
            idea_children.setdefault(edge.source_id, set()).add(edge.target_id)
        elif edge.relation == "next":
            idea_children.setdefault(edge.source_id, set()).add(edge.target_id)

    # Find idea nodes and their domains
    idea_domains: dict[str, str] = {}
    for nid in graph.node_ids:
        node = graph.get_node(nid)
        if node and node.type == "idea":
            # Domain is the suffix after "idea:" or the full id
            domain = nid.replace("idea:", "").replace("idea/", "")
            idea_domains[nid] = domain
            if domain not in domain_counts:
                domain_counts[domain] = _empty_counts()

    # Count each node by traversing from idea through spawns/next
    node_domain: dict[str, str] = {}
    for idea_id, domain in idea_domains.items():
        queue = list(idea_children.get(idea_id, []))
        while queue:
            child = queue.pop(0)
            if child in node_domain:
                continue
            node_domain[child] = domain
            queue.extend(list(idea_children.get(child, [])))

    # Assign each node to a domain
    for nid in graph.node_ids:
        domain = node_domain.get(nid, "_other")
        node = graph.get_node(nid)
        ntype = node.type if node else "unknown"
        if domain in domain_counts:
            domain_counts[domain][ntype] = domain_counts[domain].get(ntype, 0) + 1
        else:
            domain_counts["_other"][ntype] = domain_counts["_other"].get(ntype, 0) + 1

    # Build CoverageReport list
    reports: list[CoverageReport] = []
    for domain, counts in domain_counts.items():
        if domain == "_other":
            continue
        total = sum(counts.values())
        if total == 0:
            continue
        reports.append(CoverageReport(
            domain=domain,
            ideas=counts.get("idea", 0),
            hypotheses=counts.get("hypothesis", 0),
            experiments=counts.get("experiment", 0),
            verdicts=counts.get("verdict", 0),
            mvps=counts.get("mvp", 0),
            outcomes=counts.get("outcome", 0),
            bigger_outcomes=counts.get("bigger_outcome", 0),
            app_purposes=counts.get("app_purpose", 0),
            total=total,
        ))

    reports.sort(key=lambda r: r.total, reverse=True)
    return reports


def _empty_counts() -> dict[str, int]:
    return {
        "idea": 0,
        "hypothesis": 0,
        "experiment": 0,
        "verdict": 0,
        "mvp": 0,
        "outcome": 0,
        "bigger_outcome": 0,
        "app_purpose": 0,
    }
