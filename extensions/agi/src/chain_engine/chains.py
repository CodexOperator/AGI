"""Chain discovery: find all valid chains in a graph (chain-engine/R1)."""
from __future__ import annotations

from collections import deque
from pathlib import Path
import pickle
import sys
import time
from typing import Iterator

from graph_core.graph import Graph
from graph_core.types import RenderableGraph

from .types import Chain, is_valid_transition

# ---------------------------------------------------------------------------
# Pickle cache for warm find_chains results
# ---------------------------------------------------------------------------

def _get_chain_cache_file(graph_dir: str) -> str:
    """Cache path for a given graph dir.

    Derived per call — the previous module-global memo meant the first
    graph_dir seen in a process captured the cache path for every later one.
    """
    return str(Path(graph_dir).resolve() / ".chain_cache.pkl")


# Bumped whenever the cache payload gains a field the reader depends on.
# Version 1 caches predate `truncated_reason` (TODO.md H0e): a partial result
# written by that code is indistinguishable from a complete one, so they are
# refused outright rather than trusted.
CHAIN_CACHE_VERSION = 2


def _save_chain_cache(graph_dir: str, chains: list[Chain],
                      node_count: int, mtime: float,
                      truncated_reason: str | None = None) -> None:
    """Save find_chains results to pickle cache.

    `truncated_reason` records that the result is partial, so a warm hit can
    re-warn instead of serving the truncation silently (H0e).
    """
    try:
        cache_file = _get_chain_cache_file(graph_dir)
        cached = {
            "cache_version": CHAIN_CACHE_VERSION,
            "chains": chains,
            "node_count": node_count,
            "mtime": mtime,
            "truncated_reason": truncated_reason,
            "saved_at": time.time(),
        }
        with open(cache_file, "wb") as f:
            pickle.dump(cached, f, protocol=pickle.HIGHEST_PROTOCOL)
    except OSError:
        pass  # Non-fatal — cache write failure doesn't break traversal


def _load_chain_cache(graph_dir: str, node_count: int, mtime: float) \
        -> tuple[list[Chain], str | None] | None:
    """Load cached chains if sources unchanged.

    Returns `(chains, truncated_reason)`, or None on any miss. A pre-versioned
    cache is a miss: it cannot say whether it is complete.
    """
    try:
        cache_file = _get_chain_cache_file(graph_dir)
        with open(cache_file, "rb") as f:
            cached = pickle.load(f)
        if cached.get("cache_version") != CHAIN_CACHE_VERSION:
            return None
        if (cached.get("node_count") == node_count
                and cached.get("mtime") == mtime):
            return cached["chains"], cached.get("truncated_reason")
    except Exception:
        pass
    return None


# -----------------------------------------------------------------------
# Helpers: read next_edges from YAML frontmatter (post_wire-independent)
# -----------------------------------------------------------------------

import re


def _load_next_edges_from_disk(graph_dir: str,
                                next_edges: dict[str, list[str]]) -> None:
    """Parse next_edges from .md frontmatter files in graph_dir.

    This is the authoritative source — the loader doesn't parse next_edges
    and post_wire may not have run yet. We read YAML frontmatter directly.
    """
    nodes_path = Path(graph_dir)
    if not nodes_path.is_dir():
        return

    # Regex to extract next_edges list from YAML frontmatter.
    # Matches "next_edges:" followed by indented list items.
    next_re = re.compile(r'^next_edges:\s*$', re.MULTILINE)
    item_re = re.compile(r'^\s+-\s+"?([^"\n]+)"?', re.MULTILINE)

    for md_path in nodes_path.rglob("*.md"):
        try:
            text = md_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        # Extract node_id from frontmatter 'id:' field
        id_match = re.search(r'^id:\s*"?([^"\n]+)"?', text, re.MULTILINE)
        if not id_match:
            continue
        node_id = id_match.group(1).strip()

        # Find next_edges block
        ne_match = next_re.search(text)
        if not ne_match:
            continue
        start = ne_match.end()
        # Read lines until we hit a non-indented line (end of block)
        block_lines = []
        for line in text[start:].splitlines():
            if line and not line[0].isspace():
                break
            block_lines.append(line)
        block = "\n".join(block_lines)

        targets = item_re.findall(block)
        if targets:
            targets_deduped = []
            seen = set()
            for t in targets:
                t = t.strip()
                if t and t not in seen:
                    seen.add(t)
                    targets_deduped.append(t)
            next_edges.setdefault(node_id, []).extend(targets_deduped)


# ---------------------------------------------------------------------------
# Traversal bounds (H0c)
# ---------------------------------------------------------------------------
#
# The corpus at ~/.hermes/agi-tree/ contains chains gamed to 2000 hops (TODO.md
# H3).  Unbounded path enumeration over those chains never terminates, which
# hung the whole render stage (TODO.md H0c).  find_chains is therefore bounded
# on three independent axes and *degrades to partial output* — it never hangs
# and never raises.

# Real chains follow idea → hypothesis+ → experiment+ → verdict → mvp →
# outcome → bigger_outcome → app_purpose: eight types, a few repeats, so a
# meaningful chain is tens of nodes.  512 leaves two orders of magnitude of
# headroom while excluding the pathological 2000-hop shortcut chains.
DEFAULT_MAX_PATH_LEN = 512

# Consumers only need a count, the longest chain, and a ranked top-N.  10k
# chains is far more than any renderer displays and bounds worst-case memory
# (10k x 512 ids) at a few tens of MB.
DEFAULT_MAX_CHAINS = 10_000

# The render stage runs once per loop iteration and its whole budget is a few
# seconds.  20 s is generous for a healthy graph (the 158-node corpus renders
# in well under 1 s) and is a hard ceiling for a sick one.
DEFAULT_DEADLINE_S = 20.0


def _warn_truncated(reason: str, chains_found: int) -> None:
    print(
        f"WARN: find_chains truncated ({reason}); "
        f"returning {chains_found} partial chain(s)",
        file=sys.stderr,
    )


def _make_can_reach_terminal(graph: RenderableGraph,
                             next_edges: dict[str, list[str]],
                             memo: dict[str, bool]):
    """Build an *iterative* `can_reach_terminal(nid)` closure.

    Deliberately not recursive: chains in the wild reach 2000 hops, which blows
    CPython's recursion limit (TODO.md H0c defect 2).  Cycles resolve to False
    rather than looping forever.
    """

    def can_reach_terminal(start: str) -> bool:
        if start in memo:
            return memo[start]
        stack: list[str] = [start]
        in_progress: set[str] = set()
        while stack:
            nid = stack[-1]
            if nid in memo:
                stack.pop()
                in_progress.discard(nid)
                continue
            node = graph.get_node(nid)
            if node is None:
                memo[nid] = False
                stack.pop()
                continue
            if node.type == "app_purpose":
                memo[nid] = True
                stack.pop()
                in_progress.discard(nid)
                continue
            children = next_edges.get(nid, [])
            if nid not in in_progress:
                in_progress.add(nid)
                pending = [c for c in children
                           if c not in memo and c not in in_progress]
                if pending:
                    stack.extend(pending)
                    continue
            # Children resolved (anything still unresolved is on a cycle → False)
            memo[nid] = any(memo.get(c, False) for c in children)
            in_progress.discard(nid)
            stack.pop()
        return memo.get(start, False)

    return can_reach_terminal


# ---------------------------------------------------------------------------
# Core chain finding
# ---------------------------------------------------------------------------

def find_chains(graph: RenderableGraph,
                graph_dir: str | None = None,
                *,
                max_chains: int = DEFAULT_MAX_CHAINS,
                max_path_len: int = DEFAULT_MAX_PATH_LEN,
                deadline_s: float | None = DEFAULT_DEADLINE_S) -> list[Chain]:
    """Find all valid chains in the graph.

    A chain is an ordered path from an 'idea' node following 'next' edges,
    whose type sequence matches the autoresearch chain:
        idea hypothesis+ experiment+ verdict mvp outcome bigger_outcome app_purpose

    Multiple consecutive hypothesis or experiment nodes are allowed.
    Paths that skip a required type are rejected.
    Two chains may share a prefix — they are NOT deduplicated.
    A node is never visited twice on the same path (cycle guard).

    Traversal is bounded on three axes (see DEFAULT_* above).  On hitting any
    bound the chains found so far are returned and a `WARN: find_chains
    truncated (...)` line is printed to stderr — the render stage degrades to
    partial output rather than hanging the loop (TODO.md H0c).

    Results are cached to graph_dir/.chain_cache.pkl (node_count + mtime bust).
    Truncation is cached with them and re-warned on every warm hit, so a partial
    answer can never be served as a complete one (TODO.md H0e).

    Args:
        graph: A RenderableGraph (Graph or subgraph) to search.
        graph_dir: Nodes directory for cache read/write. If None, cache disabled.
        max_chains: Stop after this many complete chains.
        max_path_len: Abandon any path longer than this many nodes.
        deadline_s: Wall-clock budget in seconds. None disables the clock guard.

    Returns:
        List of chains, each chain is a list of node ids. Possibly partial.
    """
    # ---- Try warm cache first ----
    if graph_dir is not None:
        try:
            nodes_path = Path(graph_dir)
            node_count = 0
            mtime = 0.0
            if nodes_path.is_dir():
                node_count = sum(1 for _ in nodes_path.rglob("*.md"))
                mtime = max(
                    (f.stat().st_mtime for f in nodes_path.rglob("*.md")
                     if f.is_file()),
                    default=0.0,
                )
            cached = _load_chain_cache(graph_dir, node_count, mtime)
            if cached is not None:
                cached_chains, cached_reason = cached
                # A truncated answer stays labelled truncated for as long as it
                # is served — otherwise the corpus under-reports forever with no
                # warning at all (H0e).
                if cached_reason:
                    _warn_truncated(f"{cached_reason}, cached",
                                    len(cached_chains))
                return cached_chains
        except OSError:
            pass

    deadline = None if deadline_s is None else time.monotonic() + deadline_s

    chains: list[Chain] = []

    # Build adjacency: node_id -> list of target_ids by relation
    # NOTE: graph.edges may be empty (loader doesn't parse next_edges from YAML).
    # Also node.next_edges attrs may be empty (post_wire hasn't run).
    # Read next_edges directly from YAML frontmatter files as authoritative source.
    next_edges: dict[str, list[str]] = {}
    spawns_edges: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.relation == "next":
            next_edges.setdefault(edge.source_id, []).append(edge.target_id)

    # Read next_edges from YAML frontmatter (authoritative, post_wire-independent)
    if graph_dir is not None:
        _load_next_edges_from_disk(graph_dir, next_edges)

    # Also build from node.next_edges attribute (populated by post_wire at runtime)
    for nid in graph.node_ids:
        node = graph.get_node(nid)
        if node is None:
            continue
        # Collect next_edges from node attribute
        if hasattr(node, "next_edges") and node.next_edges:
            for target_id in node.next_edges:
                if target_id != nid:  # guard against self-loops
                    next_edges.setdefault(nid, []).append(target_id)
        # Build spawns_edges from parents field
        for parent_id in node.parents:
            spawns_edges.setdefault(parent_id, []).append(nid)

    # Find all idea nodes (roots with no 'next' incoming edge)
    next_targets: set[str] = {t for targets in next_edges.values() for t in targets}
    idea_nodes = [
        nid for nid in graph.node_ids
        if graph.get_node(nid).type == "idea" and nid not in next_targets
    ]

    # ---- Phase 1: memoized verdict → app_purpose reachability ----
    # Pre-compute which verdict nodes can reach app_purpose via next_edges.
    # This lets us skip dead-end verdict subtrees entirely.
    verdict_can_reach_app: dict[str, bool] = {}
    if next_edges:
        app_ids: set[str] = {nid for nid in graph.node_ids
                             if graph.get_node(nid).type == "app_purpose"}

        # Build reverse next_edges adjacency for reverse BFS from app_purposes
        reverse_adj: dict[str, list[str]] = {}
        for src, targets in next_edges.items():
            for t in targets:
                reverse_adj.setdefault(t, []).append(src)

        # BFS from all app_purposes backward through next_edges
        reachable_from_app: set[str] = set()
        queue: deque[str] = deque(list(app_ids))
        while queue:
            cur = queue.popleft()
            if cur in reachable_from_app:
                continue
            reachable_from_app.add(cur)
            for prev in reverse_adj.get(cur, []):
                if prev not in reachable_from_app:
                    queue.append(prev)

        verdict_can_reach_app = {
            vid: vid in reachable_from_app for vid in graph.node_ids
            if graph.get_node(vid).type == "verdict"
        }

    # ---- Phase 2: memoized, iterative verdict→terminal reachability ----
    _memo: dict[str, bool] = {}
    _can_reach_terminal = _make_can_reach_terminal(graph, next_edges, _memo)

    # Pre-populate memo for verdict nodes that can't reach app_purpose
    # (skip their spawns subtrees entirely)
    for vid, can_reach in verdict_can_reach_app.items():
        if not can_reach:
            _memo[vid] = False

    # ---- Phase 3: traverse from each idea root ----
    # The wall-clock budget is shared *fairly* across roots: each root gets
    # `remaining / roots_left`, and whatever it doesn't spend rolls over to the
    # roots after it. A single pathological root therefore degrades to partial
    # output for itself instead of starving every root that follows it —
    # on the agi-tree corpus that is the difference between 0 chains and 18.
    roots = sorted(idea_nodes)  # sorted for determinism
    reasons: set[str] = set()
    for i, idea_id in enumerate(roots):
        root_deadline = deadline
        if deadline is not None:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                reasons.add("deadline")
                break
            root_deadline = time.monotonic() + remaining / (len(roots) - i)

        reason = _traverse_iterative(
            idea_id, graph, next_edges, spawns_edges, [],
            chains, verdict_can_reach_app, _can_reach_terminal,
            max_chains=max_chains,
            max_path_len=max_path_len,
            deadline=root_deadline,
        )
        if reason is not None:
            reasons.add(reason)
        # max_path_len only prunes the offending path — keep going.
        # max_chains is a global budget — stop everything.
        if reason == "max_chains":
            break

    truncated_reason = "+".join(sorted(reasons)) if reasons else None
    if truncated_reason:
        _warn_truncated(truncated_reason, len(chains))

    # ---- Cache results ----
    if graph_dir is not None:
        try:
            nodes_path = Path(graph_dir)
            mtime = 0.0
            node_count = 0
            if nodes_path.is_dir():
                node_count = sum(1 for _ in nodes_path.rglob("*.md"))
                mtime = max(
                    (f.stat().st_mtime for f in nodes_path.rglob("*.md")
                     if f.is_file()),
                    default=0.0,
                )
            _save_chain_cache(graph_dir, chains, node_count, mtime,
                              truncated_reason=truncated_reason)
        except OSError:
            pass

    return chains


def _traverse_iterative(
    start_id: str,
    graph: RenderableGraph,
    next_edges: dict[str, list[str]],
    spawns_edges: dict[str, list[str]],
    path: Chain,
    chains: list[Chain],
    verdict_can_reach_app: dict[str, bool],
    can_reach_terminal: callable,
    *,
    max_chains: int = DEFAULT_MAX_CHAINS,
    max_path_len: int = DEFAULT_MAX_PATH_LEN,
    deadline: float | None = None,
) -> str | None:
    """Iterative DFS from start_id, building valid chain paths.

    The path is kept as a single mutable list plus an `on_path` set, so no
    per-step copies are made and a node is never revisited on the same path.

    Pruning optimizations:
    - Verdict nodes whose next_edges chain cannot reach app_purpose are dead ends.
    - When a verdict has next_edges children, spawns_edges are skipped entirely
      (only explore spawns when verdict has no next_edges = fallback path).

    Returns:
        None if traversal ran to completion, otherwise a short reason string
        naming the bound that fired ("max_chains", "max_path_len", "deadline").
    """
    if graph.get_node(start_id) is None:
        return None

    current_path: Chain = list(path)
    on_path: set[str] = set(current_path)
    if start_id in on_path:
        return None
    current_path.append(start_id)
    on_path.add(start_id)

    # frame = [node_id, successors | None, next_index]
    stack: list[list] = [[start_id, None, 0]]
    reason: str | None = None
    hit_len_cap = False
    steps = 0

    while stack:
        steps += 1
        if deadline is not None and (steps & 0x3FF) == 0 \
                and time.monotonic() > deadline:
            reason = "deadline"
            break

        frame = stack[-1]
        node_id = frame[0]
        node = graph.get_node(node_id)

        if frame[1] is None:
            # First visit to this frame.
            if node is not None and node.type == "app_purpose":
                chains.append(list(current_path))
                if len(chains) >= max_chains:
                    reason = "max_chains"
                    break
                frame[1] = []  # terminal — do not traverse past app_purpose
            elif len(current_path) >= max_path_len:
                hit_len_cap = True
                frame[1] = []
            elif node is None:
                frame[1] = []
            else:
                # _get_successors returns reverse-sorted; re-reverse so index
                # order is ascending-sorted (deterministic, same as before).
                frame[1] = list(reversed(_get_successors(
                    node_id, node, next_edges, spawns_edges,
                    verdict_can_reach_app, can_reach_terminal,
                )))

        successors = frame[1]
        idx = frame[2]
        if idx >= len(successors):
            stack.pop()
            on_path.discard(current_path.pop())
            continue
        frame[2] = idx + 1

        succ_id = successors[idx]
        if succ_id in on_path:
            continue  # cycle guard — never revisit a node on the current path
        succ_node = graph.get_node(succ_id)
        if succ_node is None:
            continue

        # Validate transition (only for 'next' edges; spawns can jump types)
        if node_id in next_edges:
            if not is_valid_transition(node.type, succ_node.type):
                continue

        current_path.append(succ_id)
        on_path.add(succ_id)
        stack.append([succ_id, None, 0])

    if reason is None and hit_len_cap:
        reason = "max_path_len"
    return reason


def _get_successors(
    node_id: str,
    node,  # Node object
    next_edges: dict[str, list[str]],
    spawns_edges: dict[str, list[str]],
    verdict_can_reach_app: dict[str, bool],
    can_reach_terminal: callable,
) -> list[str]:
    """Return ordered successor list for a node, with pruning.

    Strategy:
    - For verdict nodes: only use next_edges if they CAN reach app_purpose,
      otherwise fall back to spawns_edges.
    - For non-verdict nodes: next_edges first, then spawns_edges fallback.
    - Dead-end verdict subtrees (no path to app_purpose) return [].
    """
    nxt = next_edges.get(node_id, [])
    spawn = spawns_edges.get(node_id, [])

    # Verdict pruning: if verdict has next_edges, check if they lead anywhere
    if node.type == "verdict":
        if nxt:
            # Only follow next_edges if they can reach app_purpose
            # (verdict_can_reach_app already computed for all verdict nodes)
            if not verdict_can_reach_app.get(node_id, False):
                # next_edges chain is dead end — try spawns fallback
                if spawn:
                    return list(reversed(sorted(spawn)))
                return []
            return list(reversed(sorted(nxt)))
        elif spawn:
            return list(reversed(sorted(spawn)))
        return []

    # Non-verdict: prefer next_edges, fall back to spawns
    if nxt:
        return list(reversed(sorted(nxt)))
    if spawn:
        return list(reversed(sorted(spawn)))
    return []


def find_chains_from_node(graph: RenderableGraph,
                          start_id: str,
                          *,
                          max_chains: int = DEFAULT_MAX_CHAINS,
                          max_path_len: int = DEFAULT_MAX_PATH_LEN,
                          deadline_s: float | None = DEFAULT_DEADLINE_S
                          ) -> list[Chain]:
    """Find all chains that start from a specific node.

    Useful for mid-chain join (chain-engine/R4).
    Note: does not use the pickle cache (single-node origin, different use).
    Bounded exactly like find_chains.
    """
    chains: list[Chain] = []
    next_edges: dict[str, list[str]] = {}
    spawns_edges: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.relation == "next":
            next_edges.setdefault(edge.source_id, []).append(edge.target_id)
    for nid in graph.node_ids:
        node = graph.get_node(nid)
        if node is None:
            continue
        for parent_id in node.parents:
            spawns_edges.setdefault(parent_id, []).append(nid)

    start_node = graph.get_node(start_id)
    if start_node is None:
        return []

    # Build verdict reachability for pruning
    app_ids = {nid for nid in graph.node_ids
               if graph.get_node(nid).type == "app_purpose"}

    reverse_adj: dict[str, list[str]] = {}
    for src, targets in next_edges.items():
        for t in targets:
            reverse_adj.setdefault(t, []).append(src)

    reachable_from_app: set[str] = set()
    queue: deque[str] = deque(list(app_ids))
    while queue:
        cur = queue.popleft()
        if cur in reachable_from_app:
            continue
        reachable_from_app.add(cur)
        for prev in reverse_adj.get(cur, []):
            if prev not in reachable_from_app:
                queue.append(prev)

    verdict_can_reach_app = {
        vid: vid in reachable_from_app for vid in graph.node_ids
        if graph.get_node(vid).type == "verdict"
    }

    _memo: dict[str, bool] = {}
    _can_reach_terminal = _make_can_reach_terminal(graph, next_edges, _memo)

    for vid, can_reach in verdict_can_reach_app.items():
        if not can_reach:
            _memo[vid] = False

    reason = _traverse_iterative(
        start_id, graph, next_edges, spawns_edges, [], chains,
        verdict_can_reach_app, _can_reach_terminal,
        max_chains=max_chains,
        max_path_len=max_path_len,
        deadline=None if deadline_s is None else time.monotonic() + deadline_s,
    )
    if reason is not None:
        _warn_truncated(reason, len(chains))
    return chains
