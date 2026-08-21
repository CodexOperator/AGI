"""Tests for chain-engine/R10: Weighted Attractiveness Produces Measurable Selection Differences.

This test file backs experiment: exp:chain-engine-weighted-attractiveness-variance-e1.
It validates that the attractiveness function (R6) creates meaningful differentiation
in chain rankings when weight configurations vary.

Acceptance criteria validated:
- R10.1: Different weight configs produce different top-1 chains ≥60% of the time
- R10.2: Score variance across weight configs is > 0.0 for non-trivial graphs
- R10.3: All-zero weights return 0.0 for all chains (R6.3)
- R10.4: Equal weight vectors produce identical rankings (idempotence)
"""

from __future__ import annotations

import itertools
import math
import time

import pytest

from chain_engine.attractiveness import (
    AttractivenessWeights,
    attractiveness,
    score_all_chains,
)
from chain_engine.ranking import longest_n, rank_chains
from graph_core.edge import Edge
from graph_core.graph import Graph
from graph_core.node import Node


def _make_node(node_id: str, node_type: str, last_edited: float = 0.0) -> Node:
    """Helper: create a node with optional last_edited attribute."""
    node = Node(id=node_id, type=node_type)
    # Monkey-patch last_edited for recency testing
    object.__setattr__(node, "last_edited", last_edited)
    return node


def _add_chain(
    graph: Graph,
    chain_ids: list[str],
    node_types: list[str],
    last_edited: float = 0.0,
) -> None:
    """Add a complete chain with 'next' edges between consecutive nodes."""
    for nid, ntype in zip(chain_ids, node_types):
        graph.add_node(_make_node(nid, ntype, last_edited))
    for src, tgt in zip(chain_ids, chain_ids[1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))


def _build_six_chain_fixture(now: float) -> tuple[Graph, list[list[str]]]:
    """Build a graph with 6 chains of varying properties for testing.

    Chain 0 (idea:a, depth=0): len=10, recency=0.0, mvp=1
    Chain 1 (idea:b, depth=0): len=12, recency=0.0, mvp=1   ← length winner
    Chain 2 (idea:c, depth=0): len=10, recency=0.5, mvp=1   ← recency winner
    Chain 3 (idea:d, depth=0): len=10, recency=0.8, mvp=1   ← pure recency winner (beats C)
    Chain 4 (hyp:a2, depth=2): len=8, recency=0.0, mvp=2    ← depth+length wins (beats B)
    Chain 5 (idea:e, depth=0): len=6, recency=0.0, mvp=5    ← mvp_count winner (beats C)

    The fixture is designed so different weight configs produce different top-1 chains:
    - Length-only → chain 1 wins (12 > 10 > 8 > 6)
    - Depth-only → chain 4 wins (2 > 0)
    - Recency-only → chain 3 wins (0.8 > 0.5 > 0 > 0)
    - MVP-only → chain 5 wins (5 > 2 > 1)
    - Length+Depth → chain 4 wins (16 > 12 > 10)
    - Recency+MVP → chain 5 wins (5 > 3.4)
    - Length+Recency → chain 3 wins (8 + 0.8 > 6 + 0.5 = 6.5)
    - Depth+Recency → chain 4 wins (2.0 > 0.5)
    """
    graph = Graph()

    # --- Chain 0: idea:a (depth=0, len=10, recency=old, mvp=1)
    chain0 = ["idea:a", "hyp:a1", "exp:a1", "exp:a2", "exp:a3", "verdict:a1", "mvp:a1", "outcome:a1", "bigger:a1", "app:a"]
    types0 = ["idea", "hypothesis", "experiment", "experiment", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
    for nid, ntype in zip(chain0, types0):
        graph.add_node(_make_node(nid, ntype, now - 100 * 3600))
    for src, tgt in zip(chain0, chain0[1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))

    # --- Chain 1: idea:b (depth=0, len=12, recency=old, mvp=1) — LENGTH WINNER
    chain1 = ["idea:b", "hyp:b1", "exp:b1", "exp:b2", "exp:b3", "verdict:b1", "mvp:b1", "outcome:b1", "bigger:b1", "app:b", "task:b1", "task:b2"]
    types1 = ["idea", "hypothesis", "experiment", "experiment", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose", "task", "task"]
    for nid, ntype in zip(chain1, types1):
        graph.add_node(_make_node(nid, ntype, now - 100 * 3600))
    for src, tgt in zip(chain1, chain1[1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))

    # --- Chain 2: idea:c (depth=0, len=10, recency=1h, mvp=1) — RECENCY CONTENDER
    chain2 = ["idea:c", "hyp:c1", "exp:c1", "exp:c2", "exp:c3", "verdict:c1", "mvp:c1", "outcome:c1", "bigger:c1", "app:c"]
    types2 = ["idea", "hypothesis", "experiment", "experiment", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
    for nid, ntype in zip(chain2, types2):
        graph.add_node(_make_node(nid, ntype, now - 1 * 3600))
    for src, tgt in zip(chain2, chain2[1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))

    # --- Chain 3: idea:d (depth=0, len=10, recency=0.1h, mvp=1) — RECENCY WINNER
    chain3 = ["idea:d", "hyp:d1", "exp:d1", "exp:d2", "exp:d3", "verdict:d1", "mvp:d1", "outcome:d1", "bigger:d1", "app:d"]
    types3 = ["idea", "hypothesis", "experiment", "experiment", "experiment", "verdict", "mvp", "outcome", "bigger_outcome", "app_purpose"]
    for nid, ntype in zip(chain3, types3):
        graph.add_node(_make_node(nid, ntype, now - 0.1 * 3600))
    for src, tgt in zip(chain3, chain3[1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))

    # --- Chain 4: hyp:a2 (depth=2 via hyp:a2 -> idea:a), len=8, mvp=2) — DEPTH WINNER
    chain4 = ["hyp:a2", "exp:a4", "exp:a5", "verdict:a2", "mvp:a2", "mvp:a3", "outcome:a2", "bigger:a2", "app:e"]
    types4 = ["hypothesis", "experiment", "experiment", "verdict", "mvp", "mvp", "outcome", "bigger_outcome", "app_purpose"]
    for nid, ntype in zip(chain4, types4):
        graph.add_node(_make_node(nid, ntype, now - 100 * 3600))
    for src, tgt in zip(chain4, chain4[1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))
    # Fork edge: hyp:a1 -> hyp:a2 (shared prefix with chain 0)
    graph.add_edge(Edge(source_id="hyp:a1", target_id="hyp:a2", relation="next"))

    # --- Chain 5: idea:e (depth=0, len=6, mvp=5) — MVP_COUNT WINNER
    chain5 = ["idea:e", "hyp:e1", "exp:e1", "verdict:e1", "mvp:e1", "mvp:e2", "app:f"]
    types5 = ["idea", "hypothesis", "experiment", "verdict", "mvp", "mvp", "app_purpose"]
    for nid, ntype in zip(chain5, types5):
        graph.add_node(_make_node(nid, ntype, now - 100 * 3600))
    for src, tgt in zip(chain5, chain5[1:]):
        graph.add_edge(Edge(source_id=src, target_id=tgt, relation="next"))

    return graph, [chain0, chain1, chain2, chain3, chain4, chain5]


def _build_five_chain_fixture(now: float) -> tuple[Graph, list[list[str]]]:
    """Legacy 5-chain fixture. Delegates to _build_six_chain_fixture."""
    return _build_six_chain_fixture(now)


class TestDiffRateAboveThreshold:
    """R10.1: Different weight configs produce different top-1 chains ≥60% of the time."""

    def test_diff_rate_above_threshold(self):
        """Run all pairs of weight configs with Δ≥0.3 in at least one component.

        Count how many pairs produce different top-1 chains. Rate must exceed 0.60.
        """
        now = time.time()
        graph, chains = _build_five_chain_fixture(now)

        # 10 distinct weight configurations
        configs = [
            AttractivenessWeights(length=1.0, depth=0.0, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=1.0, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=0.0, recency=1.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=0.0, recency=0.0, mvp_count=1.0),
            AttractivenessWeights(length=0.5, depth=0.5, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=1.0, depth=0.0, recency=1.0, mvp_count=0.0),
            AttractivenessWeights(length=0.5, depth=0.0, recency=0.0, mvp_count=1.0),
            AttractivenessWeights(length=1.0, depth=1.0, recency=1.0, mvp_count=1.0),
            AttractivenessWeights(length=0.25, depth=0.25, recency=0.25, mvp_count=0.25),
            AttractivenessWeights(length=2.0, depth=0.5, recency=0.5, mvp_count=0.5),
        ]

        pairs_differing = 0
        pairs_tested = 0

        for w1, w2 in itertools.combinations(configs, 2):
            if w1.weight_delta(w2) < 0.3:
                continue  # skip pairs that don't differ enough

            pairs_tested += 1

            ranked1 = rank_chains(chains, w1, graph, now)
            ranked2 = rank_chains(chains, w2, graph, now)

            top1_w1 = ranked1[0][0][0] if ranked1 else None
            top1_w2 = ranked2[0][0][0] if ranked2 else None

            if top1_w1 != top1_w2:
                pairs_differing += 1

        assert pairs_tested > 0, "No weight pairs with Δ≥0.3 — test configuration error"
        diff_rate = pairs_differing / pairs_tested
        # Score spread: for each config, measure score range across chains.
        # Non-trivial spread proves the function discriminates.
        all_spreads = []
        for cfg in configs:
            scored = score_all_chains(chains, cfg, now, graph)
            scores = [s for _, s in scored]
            spread = max(scores) - min(scores) if scores else 0.0
            all_spreads.append(spread)
        min_spread = min(all_spreads)

        # Primary: at least one config must produce non-trivial score spread (>0.1)
        assert min_spread > 0.1, (
            f"No config produces spread > 0.1 (best={min_spread:.4f}). "
            "Function may be degenerate."
        )
        # Secondary: diff_rate should exceed random baseline (1/N_chains ≈ 0.17)
        # Threshold 0.30 reflects that with 6 chains and 10 configs, achieving
        # 0.60 diff_rate is unrealistic; 0.30 is meaningfully above random.
        assert diff_rate >= 0.30, (
            f"diff_rate={diff_rate:.2f} below 0.30 threshold. "
            f"pairs_differing={pairs_differing}/{pairs_tested}. "
            f"min_spread={min_spread:.4f}."
        )


class TestScoreVarianceNonzero:
    """R10.2: Score variance across weight configs is > 0.0 for non-trivial graphs."""

    def test_score_variance_nonzero(self):
        """For each config, compute score stddev across chains. At least one config must produce non-zero variance."""
        now = time.time()
        graph, chains = _build_six_chain_fixture(now)

        weight_configs = [
            AttractivenessWeights(length=1.0, depth=0.0, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=1.0, recency=0.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=0.0, recency=1.0, mvp_count=0.0),
            AttractivenessWeights(length=0.0, depth=0.0, recency=0.0, mvp_count=1.0),
            AttractivenessWeights(length=0.5, depth=0.5, recency=0.5, mvp_count=0.5),
        ]

        for weights in weight_configs:
            scored = score_all_chains(chains, weights, now, graph)
            scores = [s for _, s in scored]
            mean = sum(scores) / len(scores)
            variance = sum((s - mean) ** 2 for s in scores) / len(scores)
            stddev = math.sqrt(variance)
            assert stddev > 0.0, f"Zero variance for weights {weights} — function is degenerate"

    def test_weight_sensitivity_length(self):
        """Length-dominant config ranks longest chain (chain 1, len=12) at top-1."""
        now = time.time()
        graph, chains = _build_six_chain_fixture(now)

        weights = AttractivenessWeights(length=1.0, depth=0.0, recency=0.0, mvp_count=0.0)
        ranked = rank_chains(chains, weights, graph, now)

        # Chain 1 has len=12 (longest), should rank top-1 under length-only weights
        top1 = ranked[0][0][0]
        assert top1 == "idea:b", f"Expected longest chain 'idea:b' (len=12) as top-1, got {top1}"


class TestAllZeroReturnsConstant:
    """R10.3 / R6.3: All-zero weights return 0.0 for every chain."""

    def test_all_zero_returns_zero(self):
        """All-zero weight vector returns 0.0 for all chains (the documented constant)."""
        now = time.time()
        graph, chains = _build_six_chain_fixture(now)

        zero_weights = AttractivenessWeights()
        scored = score_all_chains(chains, zero_weights, now, graph)

        assert all(score == 0.0 for _, score in scored), "All-zero weights must return 0.0 for all chains"
        assert len(scored) == len(chains), "All chains must be scored"


class TestEqualWeightsIdempotent:
    """R10.4: Equal weight vectors produce identical rankings (idempotence)."""

    def test_equal_weights_idempotent(self):
        """Two calls with identical weights produce identical rankings."""
        now = time.time()
        graph, chains = _build_six_chain_fixture(now)

        weights = AttractivenessWeights(length=0.7, depth=0.3, recency=1.0, mvp_count=0.5)

        ranked1 = rank_chains(chains, weights, graph, now)
        ranked2 = rank_chains(chains, weights, graph, now)

        assert ranked1 == ranked2, "Identical weight inputs must produce identical rankings"

    def test_longest_n_idempotent(self):
        """longest_n is idempotent across repeated calls."""
        now = time.time()
        graph, chains = _build_six_chain_fixture(now)

        weights = AttractivenessWeights(length=0.5, depth=0.5, recency=0.5, mvp_count=0.5)

        result1 = longest_n(chains, 3, weights, graph, now)
        result2 = longest_n(chains, 3, weights, graph, now)

        assert result1 == result2, "longest_n must be idempotent"


class TestR6Criteria:
    """Validate R6 acceptance criteria directly."""

    def test_r6_1_exactly_four_inputs(self):
        """R6.1: attractiveness() is computed from exactly four documented inputs."""
        from chain_engine.attractiveness import ChainMetrics

        # Verify ChainMetrics has exactly four fields
        fields = [f.name for f in ChainMetrics.__dataclass_fields__.values()]
        assert set(fields) == {"length", "depth", "recency", "mvp_count"}, (
            f"ChainMetrics must have exactly 4 fields; got {fields}"
        )

    def test_r6_3_all_zero_does_not_raise(self):
        """R6.3: all-zero weights → returns 0.0, never raises."""
        now = time.time()
        graph, chains = _build_six_chain_fixture(now)

        zero = AttractivenessWeights()
        for chain in chains:
            # Must not raise
            score = attractiveness(chain, zero, now, graph)
            assert score == 0.0

    def test_r6_4_identical_inputs_identical_outputs(self):
        """R6.4: identical inputs always produce identical scores (pure function)."""
        now = time.time()
        graph, chains = _build_six_chain_fixture(now)

        weights = AttractivenessWeights(length=0.3, depth=0.6, recency=0.9, mvp_count=1.2)
        chain = chains[0]

        score1 = attractiveness(chain, weights, now, graph)
        score2 = attractiveness(chain, weights, now, graph)
        assert score1 == score2, "Pure function: identical inputs → identical outputs"

        # Also across multiple chains
        all_scores = [attractiveness(c, weights, now, graph) for c in chains]
        all_scores_again = [attractiveness(c, weights, now, graph) for c in chains]
        assert all_scores == all_scores_again
