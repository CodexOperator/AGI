"""briefing.py — the graph-level facts both readers are handed (goal:g9.7).

The interesting tests here are the two **silent-zero** ones. Both defects
produced plausible output and raised nothing, which is the failure mode a
briefing is most exposed to: nobody diffs a map against yesterday's map.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))


def _load():
    spec = importlib.util.spec_from_file_location("briefing", BIN / "briefing.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["briefing"] = m
    spec.loader.exec_module(m)
    return m


B = _load()


class _Node:
    def __init__(self, nid, ntype, children=()):
        self.id, self.type = nid, ntype
        self.children = set(children)
        self.parents, self.tags = set(), []


class _EdgeStyle:
    """A graph that answers `edges_from` — what `load_directory` builds."""

    class _E:
        def __init__(self, t): self.target = t

    def __init__(self, nodes):
        self._n = {n.id: n for n in nodes}
        self.edge_count = sum(len(n.children) for n in nodes)

    @property
    def nodes(self): return list(self._n.values())
    def __len__(self): return len(self._n)
    def get_node(self, nid): return self._n.get(nid)
    def edges_from(self, nid):
        n = self._n.get(nid)
        return [self._E(c) for c in sorted(n.children)] if n else []


class _AdjacencyStyle:
    """A graph with NO Edge objects — what `zoom._load_wired_graph` builds."""

    def __init__(self, nodes):
        self._n = {n.id: n for n in nodes}
        self.edge_count = 0
        self.edges = iter(())

    @property
    def nodes(self): return list(self._n.values())
    def __len__(self): return len(self._n)
    def get_node(self, nid): return self._n.get(nid)


def _corpus():
    return [
        _Node("idea:big", "idea", ["hypothesis:h1", "hypothesis:h2"]),
        _Node("hypothesis:h1", "hypothesis", ["experiment:e1"]),
        _Node("hypothesis:h2", "hypothesis"),
        _Node("experiment:e1", "experiment"),
        _Node("idea:small", "idea", ["hypothesis:h3"]),
        _Node("hypothesis:h3", "hypothesis"),
    ]


def test_descendants_agree_across_both_graph_representations():
    """🔴 The silent zero. Two live representations disagree on where
    adjacency lives: `load_directory` answers `edges_from`, and
    `zoom._load_wired_graph` builds no edges at all and hangs `children` on
    the nodes. A count written against only the first returned 0 for every
    idea on the second — so the attractor list, which is what an agent reads
    to choose a target, came out all zeros in alphabetical order and looked
    entirely plausible. Nothing raised.
    """
    edge_g = _EdgeStyle(_corpus())
    adj_g = _AdjacencyStyle(_corpus())

    for g in (edge_g, adj_g):
        assert B.count_descendants(g, "idea:big") == 3, (
            f"{type(g).__name__} lost the subtree")
        assert B.count_descendants(g, "idea:small") == 1


def test_edge_count_is_a_property_of_the_graph_not_of_its_loader():
    """`edges: 0` was reported about a graph with 866 of them."""
    assert B.build(Path("."), _EdgeStyle(_corpus())).edge_count == 4
    assert B.build(Path("."), _AdjacencyStyle(_corpus())).edge_count == 4


def test_attractors_are_ranked_by_descendants_not_by_id():
    """All-zero counts sort alphabetically and still look like a ranking."""
    b = B.build(Path("."), _AdjacencyStyle(_corpus()))
    assert b.attractors[0] == ("idea:big", 3)
    assert [nid for nid, _ in b.attractors] == ["idea:big", "idea:small"]


def test_a_cycle_does_not_hang_the_descendant_walk():
    nodes = [_Node("idea:a", "idea", ["idea:b"]), _Node("idea:b", "idea", ["idea:a"])]
    assert B.count_descendants(_AdjacencyStyle(nodes), "idea:a") == 1


def test_attractors_exclude_deprecated_ideas_even_with_a_big_subtree():
    """A deprecated idea with a large (also-deprecated) descendant tree must
    not out-rank a live idea just because nobody re-scored it on retirement
    -- `viewport.frame_stream`'s `hide_deprecated` already keeps this out of
    the map (goal:s23); the attractor list read the same adjacency with no
    such filter.
    """
    nodes = [
        _Node("idea:domain-graph-core", "idea",
              ["hypothesis:d1", "hypothesis:d2"]),
        _Node("hypothesis:d1", "hypothesis"),
        _Node("hypothesis:d2", "hypothesis"),
        _Node("idea:engine-todo", "idea", ["hypothesis:e1"]),
        _Node("hypothesis:e1", "hypothesis"),
    ]
    fm_by_id = {
        "idea:domain-graph-core": {"status": "deprecated"},
        "hypothesis:d1": {"status": "deprecated"},
        "hypothesis:d2": {"status": "deprecated"},
    }
    b = B.build(Path("."), _AdjacencyStyle(nodes), fm_by_id=fm_by_id)
    ids = [nid for nid, _ in b.attractors]
    assert "idea:domain-graph-core" not in ids, (
        "a deprecated idea must not appear in the attractor list at all")
    assert b.attractors == [("idea:engine-todo", 1)]


def test_a_live_idea_ranks_by_its_live_descendants_not_its_deprecated_ones():
    """A live idea with a mixed live/deprecated descendant tree counts only
    the live half -- the same exclusion applied one level down from the idea
    itself, to the descendants it is scored by.
    """
    nodes = [
        _Node("idea:mixed", "idea", ["hypothesis:live", "hypothesis:dead"]),
        _Node("hypothesis:live", "hypothesis"),
        _Node("hypothesis:dead", "hypothesis"),
    ]
    fm_by_id = {"hypothesis:dead": {"status": "deprecated"}}
    b = B.build(Path("."), _AdjacencyStyle(nodes), fm_by_id=fm_by_id)
    assert b.attractors[0] == ("idea:mixed", 1)


def test_the_rules_have_exactly_one_home():
    """The chain rules and the taxonomy are module constants, not formatter
    literals — `goal:g1.10`'s lesson applied to the contract itself."""
    md = "\n".join(B.to_markdown(B.build(Path("."), _AdjacencyStyle(_corpus()))))
    assert B.VERDICT_TAXONOMY in md
    for rule in B.CHAIN_RULES:
        assert rule in md
