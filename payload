"""Bounded-traversal regression tests for chain_engine.chains (TODO.md H0c).

Background: the 29,422-node corpus at ~/.hermes/agi-tree/ contains chains gamed
to 2000 hops (TODO.md H3). The original `find_chains` enumerated every path with
no cycle guard, no caps and a full path copy per step, and `_can_reach_terminal`
was recursive. Together that hung the render stage (killed at 300 s) and would
have raised RecursionError even if enumeration had been bounded.

These tests assert the three bounds fire, that traversal degrades to partial
output instead of hanging or raising, and that deep graphs are handled
iteratively.
"""
from __future__ import annotations

import pickle
import time
from pathlib import Path

import pytest

from graph_core.edge import Edge
from graph_core.graph import Graph
from graph_core.node import Node

from chain_engine.chains import (
    CHAIN_CACHE_VERSION,
    DEFAULT_MAX_CHAINS,
    DEFAULT_MAX_PATH_LEN,
    DEFAULT_DEADLINE_S,
    _make_can_reach_terminal,
    find_chains,
    find_chains_from_node,
)

TAIL_TYPES = ["verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]


def _link(g: Graph, src: str, tgt: str) -> None:
    g.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))


def _deep_chain_graph(hops: int) -> tuple[Graph, list[str]]:
    """idea -> hypothesis * hops -> experiment -> verdict .. app_purpose."""
    g = Graph()
    ids = ["idea:0"]
    types = ["idea"]
    for i in range(hops):
        ids.append(f"hyp:{i:05d}")
        types.append("hypothesis")
    ids.append("exp:0")
    types.append("experiment")
    for t in TAIL_TYPES:
        ids.append(f"{t}:0")
        types.append(t)
    for nid, ntype in zip(ids, types):
        g.add_node(Node(id=nid, type=ntype))
    for a, b in zip(ids, ids[1:]):
        _link(g, a, b)
    return g, ids


# ---------------------------------------------------------------------------
# H0c action 4: deep-chain completion
# ---------------------------------------------------------------------------

def test_deep_2000_hop_chain_completes_quickly_with_default_bounds(capsys):
    """A >=2000-hop chain must not hang; defaults truncate it in ~no time."""
    g, _ = _deep_chain_graph(2000)
    t0 = time.monotonic()
    chains = find_chains(g)
    elapsed = time.monotonic() - t0
    assert elapsed < 5.0, f"find_chains took {elapsed:.1f}s on a 2000-hop chain"
    # 2008 nodes > DEFAULT_MAX_PATH_LEN, so no complete chain survives.
    assert chains == []
    assert "WARN: find_chains truncated (max_path_len)" in capsys.readouterr().err


def test_deep_2000_hop_chain_found_when_path_cap_raised():
    """With the length cap lifted the deep chain is returned intact, fast."""
    g, ids = _deep_chain_graph(2000)
    t0 = time.monotonic()
    chains = find_chains(g, max_path_len=5000)
    elapsed = time.monotonic() - t0
    assert elapsed < 5.0, f"find_chains took {elapsed:.1f}s"
    assert chains == [ids]
    assert len(chains[0]) == 2007  # idea + 2000 hypotheses + experiment + 5 tail


def test_can_reach_terminal_is_iterative_on_deep_chain():
    """The old recursive helper blew the stack around ~1000 hops."""
    g, ids = _deep_chain_graph(2000)
    next_edges: dict[str, list[str]] = {}
    for e in g.edges:
        if e.relation == "next":
            next_edges.setdefault(e.source_id, []).append(e.target_id)
    can_reach = _make_can_reach_terminal(g, next_edges, {})
    assert can_reach(ids[0]) is True  # no RecursionError
    # A node hanging off nothing cannot reach app_purpose.
    g.add_node(Node(id="hyp:orphan", type="hypothesis"))
    assert can_reach("hyp:orphan") is False


# ---------------------------------------------------------------------------
# Cycle guard
#
# Graph.add_edge rejects cycles, so a cycle can only enter find_chains through
# next_edges parsed straight out of YAML frontmatter — which is exactly the
# authoritative source find_chains uses on the real corpus.
# ---------------------------------------------------------------------------

def _build_from_frontmatter(tmp_path: Path,
                            typed: dict[str, str],
                            edges: dict[str, list[str]]) -> tuple[Graph, Path]:
    """Write a nodes dir whose frontmatter carries `edges`; return (graph, dir).

    The Graph holds the nodes but no 'next' edges (Graph would reject cycles).
    """
    nodes = tmp_path / "nodes"
    g = Graph()
    for i, (nid, ntype) in enumerate(sorted(typed.items())):
        g.add_node(Node(id=nid, type=ntype))
        d = nodes / ntype
        d.mkdir(parents=True, exist_ok=True)
        targets = edges.get(nid, [])
        block = ""
        if targets:
            block = "next_edges:\n" + "".join(f'  - "{t}"\n' for t in targets)
        (d / f"{i}.md").write_text(
            f'---\nid: "{nid}"\ntype: {ntype}\n{block}---\n\nbody\n'
        )
    return g, nodes


FULL_TYPES = {
    "idea:1": "idea", "hyp:a": "hypothesis", "hyp:b": "hypothesis",
    "exp:1": "experiment", "verdict:1": "verdict", "mvp:1": "mvp",
    "outcome:1": "outcome", "bigger:1": "bigger_outcome",
    "app:1": "app_purpose",
}


def test_cycle_in_next_edges_terminates(tmp_path):
    """hypothesis nodes in a next-edge cycle must not loop forever."""
    g, nodes = _build_from_frontmatter(tmp_path, FULL_TYPES, {
        "idea:1": ["hyp:a"],
        "hyp:a": ["hyp:b"],
        "hyp:b": ["hyp:a", "exp:1"],  # hyp:b -> hyp:a closes a cycle
        "exp:1": ["verdict:1"],
        "verdict:1": ["mvp:1"],
        "mvp:1": ["outcome:1"],
        "outcome:1": ["bigger:1"],
        "bigger:1": ["app:1"],
    })
    t0 = time.monotonic()
    chains = find_chains(g, graph_dir=str(nodes))
    assert time.monotonic() - t0 < 5.0
    assert chains == [[
        "idea:1", "hyp:a", "hyp:b", "exp:1", "verdict:1", "mvp:1",
        "outcome:1", "bigger:1", "app:1",
    ]]


def test_self_loop_in_next_edges_terminates(tmp_path):
    g, nodes = _build_from_frontmatter(
        tmp_path,
        {"idea:1": "idea", "hyp:1": "hypothesis"},
        {"idea:1": ["hyp:1"], "hyp:1": ["hyp:1"]},
    )
    assert find_chains(g, graph_dir=str(nodes)) == []


# ---------------------------------------------------------------------------
# Caps: each one degrades to partial output, none raises
# ---------------------------------------------------------------------------

def _fan_graph(width: int) -> Graph:
    """idea -> width hypotheses -> width experiments -> shared tail.

    Yields width*width distinct complete chains.
    """
    g = Graph()
    g.add_node(Node(id="idea:1", type="idea"))
    for t in TAIL_TYPES:
        g.add_node(Node(id=f"{t}:0", type=t))
    for a, b in zip(TAIL_TYPES, TAIL_TYPES[1:]):
        _link(g, f"{a}:0", f"{b}:0")
    for i in range(width):
        h = f"hyp:{i:03d}"
        g.add_node(Node(id=h, type="hypothesis"))
        _link(g, "idea:1", h)
        for j in range(width):
            e = f"exp:{j:03d}"
            if not g.has_node(e):
                g.add_node(Node(id=e, type="experiment"))
                _link(g, e, "verdict:0")
            _link(g, h, e)
    return g


def test_max_chains_cap_returns_partial_output(capsys):
    g = _fan_graph(10)  # 100 complete chains
    chains = find_chains(g, max_chains=7)
    assert len(chains) == 7
    err = capsys.readouterr().err
    assert "WARN: find_chains truncated (max_chains)" in err
    assert "returning 7 partial chain(s)" in err


def test_max_chains_not_hit_returns_everything(capsys):
    g = _fan_graph(10)
    chains = find_chains(g)
    assert len(chains) == 100
    assert "WARN" not in capsys.readouterr().err


def test_max_path_len_cap_returns_partial_output(capsys):
    """Short chains survive; the over-long one is dropped, not raised on."""
    g, _ = _deep_chain_graph(40)
    chains = find_chains(g, max_path_len=10)
    assert chains == []
    assert "WARN: find_chains truncated (max_path_len)" in capsys.readouterr().err


def test_max_path_len_does_not_starve_later_roots(capsys):
    """One over-long root must not abort traversal of the remaining roots."""
    deep, _ = _deep_chain_graph(40)
    short_ids = ["idea:zz", "hyp:zz", "exp:zz", "verdict:zz", "mvp:zz",
                 "outcome:zz", "bigger:zz", "app:zz"]
    short_types = ["idea", "hypothesis", "experiment", "verdict", "mvp",
                   "outcome", "bigger_outcome", "app_purpose"]
    for nid, ntype in zip(short_ids, short_types):
        deep.add_node(Node(id=nid, type=ntype))
    for a, b in zip(short_ids, short_ids[1:]):
        _link(deep, a, b)

    chains = find_chains(deep, max_path_len=10)
    assert chains == [short_ids]  # "idea:0" (deep) pruned, "idea:zz" kept
    assert "WARN: find_chains truncated (max_path_len)" in capsys.readouterr().err


def test_deadline_cap_returns_partial_output(capsys):
    """A zero budget stops traversal without raising."""
    g, _ = _deep_chain_graph(20000)
    t0 = time.monotonic()
    chains = find_chains(g, max_path_len=10 ** 9, deadline_s=0.0)
    assert time.monotonic() - t0 < 10.0
    assert isinstance(chains, list)
    assert "WARN: find_chains truncated (deadline)" in capsys.readouterr().err


def test_deadline_none_disables_clock_guard():
    g, ids = _deep_chain_graph(50)
    assert find_chains(g, deadline_s=None) == [ids]


def test_bound_defaults_are_the_documented_ones():
    assert DEFAULT_MAX_PATH_LEN == 512
    assert DEFAULT_MAX_CHAINS == 10_000
    assert DEFAULT_DEADLINE_S == 20.0


# ---------------------------------------------------------------------------
# Determinism + public contract
# ---------------------------------------------------------------------------

def test_results_are_deterministic():
    g = _fan_graph(6)
    first = find_chains(g)
    second = find_chains(g)
    assert first == second
    assert first == sorted(first)


def test_find_chains_from_node_is_bounded(capsys):
    g, _ = _deep_chain_graph(2000)
    t0 = time.monotonic()
    chains = find_chains_from_node(g, "idea:0")
    assert time.monotonic() - t0 < 5.0
    assert chains == []
    assert "WARN: find_chains truncated" in capsys.readouterr().err


def test_find_chains_from_node_returns_deep_chain_when_uncapped():
    g, ids = _deep_chain_graph(2000)
    assert find_chains_from_node(g, "idea:0", max_path_len=5000) == [ids]


# ---------------------------------------------------------------------------
# Cache contract (graph_dir positional, None disables)
# ---------------------------------------------------------------------------

LINEAR_EDGES = {
    "idea:1": ["hyp:a"], "hyp:a": ["exp:1"], "exp:1": ["verdict:1"],
    "verdict:1": ["mvp:1"], "mvp:1": ["outcome:1"],
    "outcome:1": ["bigger:1"], "bigger:1": ["app:1"],
}
LINEAR_TYPES = {k: v for k, v in FULL_TYPES.items() if k != "hyp:b"}


def test_graph_dir_none_writes_no_cache(tmp_path):
    g, _ = _deep_chain_graph(3)
    find_chains(g, graph_dir=None)
    assert list(tmp_path.glob("**/.chain_cache.pkl")) == []


def test_graph_dir_positional_round_trips_cache(tmp_path):
    """render-context.py calls find_chains(g, graph_dir=str(nodes_dir))."""
    g, nodes = _build_from_frontmatter(tmp_path, LINEAR_TYPES, LINEAR_EDGES)

    chains = find_chains(g, graph_dir=str(nodes))
    cache = nodes / ".chain_cache.pkl"
    assert cache.exists()
    assert chains and chains[0][0] == "idea:1"

    # Warm read returns the cached value.
    payload = pickle.loads(cache.read_bytes())
    assert payload["chains"] == chains
    assert find_chains(g, graph_dir=str(nodes)) == chains


def test_cache_path_is_per_directory(tmp_path):
    """Regression: the cache path used to be memoized in a module global."""
    ga, na = _build_from_frontmatter(tmp_path / "a", LINEAR_TYPES, LINEAR_EDGES)
    gb, nb = _build_from_frontmatter(tmp_path / "b", LINEAR_TYPES, LINEAR_EDGES)
    find_chains(ga, graph_dir=str(na))
    find_chains(gb, graph_dir=str(nb))
    assert (na / ".chain_cache.pkl").exists()
    assert (nb / ".chain_cache.pkl").exists()


# ---------------------------------------------------------------------------
# H0e: a truncated result must never be served as a complete one
# ---------------------------------------------------------------------------

def _deep_frontmatter_chain(tmp_path: Path, hops: int):
    """`_deep_chain_graph`, but persisted so find_chains can cache it."""
    ids = ["idea:0"] + [f"hyp:{i:05d}" for i in range(hops)] + ["exp:0"]
    types = ["idea"] + ["hypothesis"] * hops + ["experiment"]
    for t in TAIL_TYPES:
        ids.append(f"{t}:0")
        types.append(t)
    return _build_from_frontmatter(
        tmp_path,
        dict(zip(ids, types)),
        {a: [b] for a, b in zip(ids, ids[1:])},
    )


def test_truncated_result_rewarns_on_every_cache_hit(tmp_path, capsys):
    """The defect: the cold run warned, every warm run was silent."""
    g, nodes = _deep_frontmatter_chain(tmp_path, 40)

    assert find_chains(g, graph_dir=str(nodes), max_path_len=10) == []
    assert "WARN: find_chains truncated (max_path_len)" in capsys.readouterr().err

    assert find_chains(g, graph_dir=str(nodes), max_path_len=10) == []
    err = capsys.readouterr().err
    assert "WARN: find_chains truncated (max_path_len, cached)" in err


def test_complete_result_stays_silent_on_cache_hit(tmp_path, capsys):
    """Re-warning must be driven by truncation, not by cache hits as such."""
    g, nodes = _build_from_frontmatter(tmp_path, LINEAR_TYPES, LINEAR_EDGES)

    find_chains(g, graph_dir=str(nodes))
    capsys.readouterr()
    assert find_chains(g, graph_dir=str(nodes))
    assert "WARN" not in capsys.readouterr().err


def test_truncation_reason_is_persisted(tmp_path):
    g, nodes = _deep_frontmatter_chain(tmp_path, 40)
    find_chains(g, graph_dir=str(nodes), max_path_len=10)

    payload = pickle.loads((nodes / ".chain_cache.pkl").read_bytes())
    assert payload["truncated_reason"] == "max_path_len"
    assert payload["cache_version"] == CHAIN_CACHE_VERSION


def test_unversioned_cache_is_refused(tmp_path):
    """A pre-H0e cache cannot say whether it is complete, so it is not trusted."""
    g, nodes = _build_from_frontmatter(tmp_path, LINEAR_TYPES, LINEAR_EDGES)
    md = list(nodes.rglob("*.md"))
    (nodes / ".chain_cache.pkl").write_bytes(pickle.dumps({
        "chains": [["idea:stale"]],
        "node_count": len(md),
        "mtime": max(f.stat().st_mtime for f in md),
        "saved_at": time.time(),
    }))

    chains = find_chains(g, graph_dir=str(nodes))
    assert chains and chains[0][0] == "idea:1"
