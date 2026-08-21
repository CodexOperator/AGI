"""Tests for chain-engine/R1: Chain definition (chain-engine/chains.py)."""
from __future__ import annotations

import pytest

from graph_core.edge import Edge
from graph_core.graph import Graph
from graph_core.node import Node


def _make_node(node_id: str, node_type: str) -> Node:
    return Node(id=node_id, type=node_type)


def _add_chain(graph: Graph, chain_ids: list[str], node_types: list[str]) -> None:
    """Add a chain of nodes with 'next' edges between consecutive nodes."""
    for nid, ntype in zip(chain_ids, node_types):
        graph.add_node(_make_node(nid, ntype))
    for src, tgt in zip(chain_ids, chain_ids[1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))


class TestChainDefinition:
    """R1.1: Chain is an ordered sequence of node ids whose types appear in order."""

    def test_single_full_chain(self):
        """One complete chain from idea to app_purpose."""
        graph = Graph()
        chain_ids = ["idea:1", "hyp:1", "exp:1", "verdict:1", "mvp:1", "outcome:1", "bigger:1", "app:1"]
        node_types = ["idea", "hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
        _add_chain(graph, chain_ids, node_types)

        from chain_engine.chains import find_chains
        chains = find_chains(graph)

        assert len(chains) == 1
        assert chains[0] == chain_ids

    def test_empty_graph(self):
        """Graph with no nodes returns no chains."""
        graph = Graph()
        from chain_engine.chains import find_chains
        chains = find_chains(graph)
        assert chains == []

    def test_only_idea_node(self):
        """A lone idea node (no successors) returns no chains."""
        graph = Graph()
        graph.add_node(_make_node("idea:1", "idea"))
        from chain_engine.chains import find_chains
        chains = find_chains(graph)
        assert chains == []


class TestMultipleHypothesisExperiment:
    """R1.2: Multiple consecutive hypothesis or experiment nodes allowed."""

    def test_two_hypotheses(self):
        """Chain with two consecutive hypothesis nodes."""
        graph = Graph()
        chain_ids = ["idea:1", "hyp:1", "hyp:2", "exp:1", "verdict:1", "mvp:1", "outcome:1", "bigger:1", "app:1"]
        node_types = ["idea", "hypothesis", "hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
        _add_chain(graph, chain_ids, node_types)

        from chain_engine.chains import find_chains
        chains = find_chains(graph)

        assert len(chains) == 1
        assert chains[0] == chain_ids

    def test_two_experiments(self):
        """Chain with two consecutive experiment nodes."""
        graph = Graph()
        chain_ids = ["idea:1", "hyp:1", "exp:1", "exp:2", "verdict:1", "mvp:1", "outcome:1", "bigger:1", "app:1"]
        node_types = ["idea", "hypothesis", "experiment", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
        _add_chain(graph, chain_ids, node_types)

        from chain_engine.chains import find_chains
        chains = find_chains(graph)

        assert len(chains) == 1
        assert chains[0] == chain_ids

    def test_multiple_hypotheses_and_experiments(self):
        """Chain with multiple hypotheses and experiments interleaved."""
        graph = Graph()
        chain_ids = ["idea:1", "hyp:1", "hyp:2", "exp:1", "exp:2", "exp:3", "verdict:1", "mvp:1", "outcome:1", "bigger:1", "app:1"]
        node_types = ["idea", "hypothesis", "hypothesis", "experiment", "experiment", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
        _add_chain(graph, chain_ids, node_types)

        from chain_engine.chains import find_chains
        chains = find_chains(graph)

        assert len(chains) == 1
        assert chains[0] == chain_ids


class TestPathSkippingRequiredType:
    """R1.3: Path skipping a required type is NOT recognized as a chain."""

    def test_skips_experiment_rejected(self):
        """Path that jumps from hypothesis to verdict (skipping experiment) is rejected."""
        graph = Graph()
        # Build: idea -> hyp -> verdict (no experiment)
        graph.add_node(_make_node("idea:1", "idea"))
        graph.add_node(_make_node("hyp:1", "hypothesis"))
        graph.add_node(_make_node("verdict:1", "verdict"))
        graph.add_node(_make_node("mvp:1", "mvp"))
        graph.add_node(_make_node("outcome:1", "outcome"))
        graph.add_node(_make_node("bigger:1", "bigger_outcome"))
        graph.add_node(_make_node("app:1", "app_purpose"))
        graph.add_edge(Edge(source_id="idea:1", target_id="hyp:1", relation="next"))
        graph.add_edge(Edge(source_id="hyp:1", target_id="verdict:1", relation="next"))
        graph.add_edge(Edge(source_id="verdict:1", target_id="mvp:1", relation="next"))
        graph.add_edge(Edge(source_id="mvp:1", target_id="outcome:1", relation="next"))
        graph.add_edge(Edge(source_id="outcome:1", target_id="bigger:1", relation="next"))
        graph.add_edge(Edge(source_id="bigger:1", target_id="app:1", relation="next"))

        from chain_engine.chains import find_chains
        chains = find_chains(graph)

        assert chains == []

    def test_skips_mvp_rejected(self):
        """Path that jumps from verdict to outcome (skipping mvp) is rejected."""
        graph = Graph()
        graph.add_node(_make_node("idea:1", "idea"))
        graph.add_node(_make_node("hyp:1", "hypothesis"))
        graph.add_node(_make_node("exp:1", "experiment"))
        graph.add_node(_make_node("verdict:1", "verdict"))
        graph.add_node(_make_node("outcome:1", "outcome"))
        graph.add_node(_make_node("bigger:1", "bigger_outcome"))
        graph.add_node(_make_node("app:1", "app_purpose"))
        graph.add_edge(Edge(source_id="idea:1", target_id="hyp:1", relation="next"))
        graph.add_edge(Edge(source_id="hyp:1", target_id="exp:1", relation="next"))
        graph.add_edge(Edge(source_id="exp:1", target_id="verdict:1", relation="next"))
        graph.add_edge(Edge(source_id="verdict:1", target_id="outcome:1", relation="next"))
        graph.add_edge(Edge(source_id="outcome:1", target_id="bigger:1", relation="next"))
        graph.add_edge(Edge(source_id="bigger:1", target_id="app:1", relation="next"))

        from chain_engine.chains import find_chains
        chains = find_chains(graph)

        assert chains == []


class TestSharedPrefixNotDeduplicated:
    """R1.4: Two chains may share a prefix; they are NOT deduplicated."""

    def test_fork_after_hypothesis(self):
        """Two chains sharing idea->hyp->exp prefix diverge at experiment."""
        graph = Graph()
        # Chain A: idea -> hyp -> exp1 -> verdict -> mvp -> outcome -> bigger -> app
        # Chain B: idea -> hyp -> exp2 -> verdict -> mvp -> outcome -> bigger -> app
        graph.add_node(_make_node("idea:1", "idea"))
        graph.add_node(_make_node("hyp:1", "hypothesis"))
        graph.add_node(_make_node("exp:1a", "experiment"))
        graph.add_node(_make_node("exp:1b", "experiment"))
        graph.add_node(_make_node("verdict:1a", "verdict"))
        graph.add_node(_make_node("verdict:1b", "verdict"))
        graph.add_node(_make_node("mvp:1a", "mvp"))
        graph.add_node(_make_node("mvp:1b", "mvp"))
        graph.add_node(_make_node("outcome:1a", "outcome"))
        graph.add_node(_make_node("outcome:1b", "outcome"))
        graph.add_node(_make_node("bigger:1a", "bigger_outcome"))
        graph.add_node(_make_node("bigger:1b", "bigger_outcome"))
        graph.add_node(_make_node("app:1a", "app_purpose"))
        graph.add_node(_make_node("app:1b", "app_purpose"))

        # Chain A edges
        graph.add_edge(Edge(source_id="idea:1", target_id="hyp:1", relation="next"))
        graph.add_edge(Edge(source_id="hyp:1", target_id="exp:1a", relation="next"))
        graph.add_edge(Edge(source_id="exp:1a", target_id="verdict:1a", relation="next"))
        graph.add_edge(Edge(source_id="verdict:1a", target_id="mvp:1a", relation="next"))
        graph.add_edge(Edge(source_id="mvp:1a", target_id="outcome:1a", relation="next"))
        graph.add_edge(Edge(source_id="outcome:1a", target_id="bigger:1a", relation="next"))
        graph.add_edge(Edge(source_id="bigger:1a", target_id="app:1a", relation="next"))

        # Chain B edges (fork at experiment)
        graph.add_edge(Edge(source_id="hyp:1", target_id="exp:1b", relation="next"))
        graph.add_edge(Edge(source_id="exp:1b", target_id="verdict:1b", relation="next"))
        graph.add_edge(Edge(source_id="verdict:1b", target_id="mvp:1b", relation="next"))
        graph.add_edge(Edge(source_id="mvp:1b", target_id="outcome:1b", relation="next"))
        graph.add_edge(Edge(source_id="outcome:1b", target_id="bigger:1b", relation="next"))
        graph.add_edge(Edge(source_id="bigger:1b", target_id="app:1b", relation="next"))

        from chain_engine.chains import find_chains
        chains = find_chains(graph)

        assert len(chains) == 2
        # Both chains should share the idea and hypothesis
        assert chains[0][:2] == ["idea:1", "hyp:1"]
        assert chains[1][:2] == ["idea:1", "hyp:1"]
        # But diverge at experiment
        assert chains[0][2] == "exp:1a"
        assert chains[1][2] == "exp:1b"

    def test_two_independent_chains(self):
        """Two completely independent idea nodes yield two separate chains."""
        graph = Graph()
        # Chain 1
        chain1_ids = ["idea:1", "hyp:1", "exp:1", "verdict:1", "mvp:1", "outcome:1", "bigger:1", "app:1"]
        chain1_types = ["idea", "hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
        _add_chain(graph, chain1_ids, chain1_types)

        # Chain 2
        chain2_ids = ["idea:2", "hyp:2", "exp:2", "verdict:2", "mvp:2", "outcome:2", "bigger:2", "app:2"]
        chain2_types = ["idea", "hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
        _add_chain(graph, chain2_ids, chain2_types)

        from chain_engine.chains import find_chains
        chains = find_chains(graph)

        assert len(chains) == 2
        chain_ids = [c[0] for c in chains]
        assert "idea:1" in chain_ids
        assert "idea:2" in chain_ids


class TestDeterminism:
    """Chains are returned in deterministic order regardless of insertion order."""

    def test_deterministic_order(self):
        """Two separate runs produce the same chain order."""
        graph1 = Graph()
        chain1_ids = ["idea:1", "hyp:1", "exp:1", "verdict:1", "mvp:1", "outcome:1", "bigger:1", "app:1"]
        chain1_types = ["idea", "hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
        _add_chain(graph1, chain1_ids, chain1_types)
        chain2_ids = ["idea:2", "hyp:2", "exp:2", "verdict:2", "mvp:2", "outcome:2", "bigger:2", "app:2"]
        chain2_types = ["idea", "hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
        _add_chain(graph1, chain2_ids, chain2_types)

        from chain_engine.chains import find_chains
        chains1 = find_chains(graph1)

        # Rebuild graph in different order
        graph2 = Graph()
        _add_chain(graph2, chain2_ids, chain2_types)  # idea:2 first
        _add_chain(graph2, chain1_ids, chain1_types)  # idea:1 second

        chains2 = find_chains(graph2)

        assert chains1 == chains2


class TestFindChainsFromNode:
    """Mid-chain join support: find chains starting from a specific node."""

    def test_start_from_hypothesis(self):
        """Starting mid-chain from hypothesis finds remaining path."""
        graph = Graph()
        chain_ids = ["idea:1", "hyp:1", "exp:1", "verdict:1", "mvp:1", "outcome:1", "bigger:1", "app:1"]
        node_types = ["idea", "hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
        _add_chain(graph, chain_ids, node_types)

        from chain_engine.chains import find_chains_from_node
        chains = find_chains_from_node(graph, "hyp:1")

        assert len(chains) == 1
        # Chain starts from hypothesis (not idea)
        assert chains[0] == chain_ids[1:]  # hyp:1 onwards
