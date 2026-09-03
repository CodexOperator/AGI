"""Tests for `bin/viewport.py` — `goal:g9.4` under `goal:g9.7`.

The load-bearing test here is `test_both_formatters_read_one_stream`: it is
`goal:g9.7`'s falsifier executed, and it is what stops the human viewport and
the LLM's injected context from drifting into two views again.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))


def _load_viewport():
    spec = importlib.util.spec_from_file_location("viewport", BIN / "viewport.py")
    m = importlib.util.module_from_spec(spec)
    # Registered BEFORE exec: `@dataclass` resolves annotations through
    # `sys.modules[cls.__module__]`, so a module that is not yet there makes
    # the decorator fail with a bare AttributeError on None.
    sys.modules["viewport"] = m
    spec.loader.exec_module(m)
    return m


V = _load_viewport()


# --------------------------------------------------------------------------
# A tiny fake graph. Deliberately not the real corpus: these assert the
# renderer's behaviour, which must not change when the corpus does.
# --------------------------------------------------------------------------

class _Node:
    def __init__(self, nid, ntype, parents=(), children=()):
        self.id = nid
        self.type = ntype
        self.parents = list(parents)
        self.children = set(children)


class _Graph:
    """Spells `node_ids` as a SET attribute, like the real Graph does."""
    def __init__(self, nodes):
        self._n = {n.id: n for n in nodes}
        self.node_ids = set(self._n)

    def has_node(self, nid):
        return nid in self._n

    def get_node(self, nid):
        return self._n.get(nid)


@pytest.fixture
def graph():
    return _Graph([
        _Node("goal:a", "goal", children=["hypothesis:h1", "hypothesis:h2"]),
        _Node("hypothesis:h1", "hypothesis", ["goal:a"], ["experiment:e1"]),
        _Node("hypothesis:h2", "hypothesis", ["goal:a"]),
        _Node("experiment:e1", "experiment", ["hypothesis:h1"]),
        _Node("goal:b", "goal"),
        _Node("verdict:orphan", "verdict", ["goal:GONE"]),
    ])


@pytest.fixture
def fm():
    return {
        "goal:a": {"title": "Goal A", "status": "active"},
        "goal:b": {"title": "Goal B", "status": "horizon"},
        "hypothesis:h1": {"title": "H one", "verdict": "pending"},
        "hypothesis:h2": {"title": "H two", "verdict": "proved"},
        "experiment:e1": {"title": "E one", "verdict": "proved",
                          "evidence_runs": ["experiment:e1"]},
        "verdict:orphan": {"title": "Orphan"},
    }


# --------------------------------------------------------------------------
# goal:g9.7 — one render, two readers.
# --------------------------------------------------------------------------

def test_both_formatters_read_one_stream(graph, fm):
    """g9.7's falsifier. Same frames, same order, in both outputs."""
    frames = V.frame_stream(graph, fm, "goal:a", 3)
    human = V.render_human(frames, 0, 0, 50, 300)
    llm = V.render_llm(frames, 0, 0, 50, 300)

    llm_ids = [ln.split("`")[1] for ln in llm.splitlines() if "`" in ln]
    assert llm_ids == [f.node_id for f in frames]
    assert len([ln for ln in human if ln.strip()]) == len(frames)


def test_changing_the_stream_changes_both_views(graph, fm):
    """The mechanical half of g9.7: there is no way to change one only."""
    shallow = V.frame_stream(graph, fm, "goal:a", 1)
    deep = V.frame_stream(graph, fm, "goal:a", 3)
    assert len(deep) > len(shallow)

    h_s = [ln for ln in V.render_human(shallow, 0, 0, 50, 300) if ln.strip()]
    h_d = [ln for ln in V.render_human(deep, 0, 0, 50, 300) if ln.strip()]
    l_s = V.render_llm(shallow, 0, 0, 50, 300)
    l_d = V.render_llm(deep, 0, 0, 50, 300)

    assert len(h_d) > len(h_s), "human view did not follow the stream"
    assert len(l_d.splitlines()) > len(l_s.splitlines()), "llm view did not follow"


# --------------------------------------------------------------------------
# Traversal
# --------------------------------------------------------------------------

def test_children_appear_directly_beneath_their_parent(graph, fm):
    """Pre-order, not breadth-first.

    BFS was the first implementation and it emitted every depth-0 node, then
    every depth-1 node, so the indentation described a nesting the ORDER
    contradicted. A tree view whose order disagrees with its indentation is
    simply wrong, and no assertion existed to say so.
    """
    ids = [f.node_id for f in V.frame_stream(graph, fm, "goal:a", 3)]
    assert ids == ["goal:a", "hypothesis:h1", "experiment:e1", "hypothesis:h2"]


def test_depth_bounds_the_walk(graph, fm):
    assert [f.node_id for f in V.frame_stream(graph, fm, "goal:a", 0)] == ["goal:a"]
    assert len(V.frame_stream(graph, fm, "goal:a", 1)) == 3


def test_traversal_is_deterministic(graph, fm):
    a = [f.node_id for f in V.frame_stream(graph, fm, "goal:a", 3)]
    b = [f.node_id for f in V.frame_stream(graph, fm, "goal:a", 3)]
    assert a == b


def test_a_cycle_does_not_hang_the_walk(fm):
    g = _Graph([
        _Node("goal:x", "goal", children=["goal:y"]),
        _Node("goal:y", "goal", ["goal:x"], ["goal:x"]),
    ])
    ids = [f.node_id for f in V.frame_stream(g, {}, "goal:x", 10)]
    assert ids == ["goal:x", "goal:y"]


def test_an_unknown_anchor_fails_loudly(graph, fm):
    with pytest.raises(SystemExit):
        V.frame_stream(graph, fm, "goal:nope", 2)


# --------------------------------------------------------------------------
# goal:g9 — render damage, never hide it.
# --------------------------------------------------------------------------

def test_a_dangling_parent_is_rendered_as_damage(graph, fm):
    f = V.frame_stream(graph, fm, "verdict:orphan", 0)[0]
    assert "dangling parent" in f.damaged
    assert V.GLYPH["damaged"] in V.render_human([f], 0, 0, 5, 300)[0]
    assert "DAMAGE" in V.render_llm([f], 0, 0, 5, 300)


def test_a_decisive_verdict_without_evidence_is_damage(graph, fm):
    f = [x for x in V.frame_stream(graph, fm, "goal:a", 2)
         if x.node_id == "hypothesis:h2"][0]
    assert "no evidence" in f.damaged


def test_a_decisive_verdict_with_evidence_is_not_damage(graph, fm):
    f = [x for x in V.frame_stream(graph, fm, "goal:a", 2)
         if x.node_id == "experiment:e1"][0]
    assert f.damaged == ""


def test_damage_reaches_both_views(graph, fm):
    """g9 and g9.7 together: damage a human can see is damage an agent is
    told about, because it rides on the Frame rather than on a formatter."""
    frames = V.frame_stream(graph, fm, "verdict:orphan", 0)
    assert V.GLYPH["damaged"] in "".join(V.render_human(frames, 0, 0, 5, 300))
    assert "DAMAGE" in V.render_llm(frames, 0, 0, 5, 300)


# --------------------------------------------------------------------------
# Default view
# --------------------------------------------------------------------------

def test_default_roots_are_the_active_goals(graph, fm):
    assert V.default_roots(graph, fm) == ["goal:a"]


def test_default_roots_fall_back_when_nothing_is_active(graph):
    roots = V.default_roots(graph, {})
    assert "goal:a" in roots and "goal:b" in roots
    assert "experiment:e1" not in roots


def test_node_ids_as_a_set_attribute_does_not_crash(graph, fm):
    """The real `Graph` spells this as a set, and calling it crashed the
    entire default view. The smoke check missed it because it grepped stdout
    for a glyph, and absent output looks identical to a traceback."""
    assert V._all_ids(graph)


# --------------------------------------------------------------------------
# Space axis
# --------------------------------------------------------------------------

def test_the_window_pans_without_changing_the_stream(graph, fm):
    frames = V.frame_stream(graph, fm, "goal:a", 3)
    top0 = V.render_human(frames, 0, 0, 2, 300)
    top1 = V.render_human(frames, 1, 0, 2, 300)
    assert top0 != top1
    assert len(V.frame_stream(graph, fm, "goal:a", 3)) == len(frames)


def test_horizontal_pan_slices_columns(graph, fm):
    frames = V.frame_stream(graph, fm, "goal:a", 0)
    assert V.render_human(frames, 0, 0, 1, 40)[0].startswith(V.GLYPH["root"])
    assert not V.render_human(frames, 0, 6, 1, 40)[0].startswith(V.GLYPH["root"])


def test_every_line_is_padded_to_the_window_width(graph, fm):
    frames = V.frame_stream(graph, fm, "goal:a", 3)
    for ln in V.render_human(frames, 0, 0, 10, 55):
        assert len(ln) == 55


# --------------------------------------------------------------------------
# Live axis
# --------------------------------------------------------------------------

def test_agents_render_as_spiders_where_they_work(graph, fm):
    frames = V.frame_stream(graph, fm, "goal:a", 1,
                            {"hypothesis:h1": ["a00-kid", "a00-parent"]})
    line = [ln for ln in V.render_human(frames, 0, 0, 10, 300) if "H one" in ln][0]
    assert line.count(V.GLYPH["spider"]) == 2
    assert "agents=a00-kid,a00-parent" in V.render_llm(frames, 0, 0, 10, 300)


def test_agents_of_iteration_reads_manifest_and_agent_json(tmp_path):
    d = tmp_path / "sessions" / "iter-001" / "a1"
    d.mkdir(parents=True)
    (tmp_path / "sessions" / "iter-001" / "manifest.json").write_text(
        '{"agents":[{"id":"a1","tier":"parent","target":"goal:t"}]}')
    (d / "agent.json").write_text('{"owns":["verdict:v1"]}')
    got = V.agents_of_iteration(tmp_path, "iter-001")
    assert got == {"verdict:v1": ["a1"]}


def test_a_missing_or_corrupt_manifest_returns_nothing_rather_than_raising(tmp_path):
    assert V.agents_of_iteration(tmp_path, "iter-404") == {}
    d = tmp_path / "sessions" / "iter-002"
    d.mkdir(parents=True)
    (d / "manifest.json").write_text("{not json")
    assert V.agents_of_iteration(tmp_path, "iter-002") == {}


# --------------------------------------------------------------------------
# Time axis
# --------------------------------------------------------------------------

def test_iteration_points_are_sorted_oldest_first(tmp_path):
    for n in ("iter-003", "iter-001", "iter-002"):
        (tmp_path / "sessions" / n).mkdir(parents=True)
    assert V.iteration_points(tmp_path) == ["iter-001", "iter-002", "iter-003"]


def test_iteration_points_on_a_project_with_no_sessions(tmp_path):
    assert V.iteration_points(tmp_path) == []


# --------------------------------------------------------------------------
# goal:g9 — reader, never writer.
# --------------------------------------------------------------------------

def test_the_module_contains_no_write_surface():
    src = (BIN / "viewport.py").read_text()
    for forbidden in ('"w"', "'w'", ".write_text(", ".mkdir(", "os.remove",
                      "shutil.rmtree", "git commit", "git checkout"):
        assert forbidden not in src, f"viewport must not write: found {forbidden}"


# --------------------------------------------------------------------------
# L1.04 — the briefing. goal:g9.7 applied to everything that is NOT a frame.
# --------------------------------------------------------------------------

def _brief():
    """A Briefing built by hand, so these tests need no project on disk."""
    import importlib.util as _ilu
    spec = _ilu.spec_from_file_location("briefing", BIN / "briefing.py")
    m = _ilu.module_from_spec(spec)
    sys.modules["briefing"] = m
    spec.loader.exec_module(m)
    b = m.Briefing()
    b.node_count = 42
    b.edge_count = 17
    b.by_type = {"goal": 2, "hypothesis": 2}
    b.primary = "outcome_coverage"
    b.coverage = 0.375
    b.attractors = [("idea:x", 5)]
    return m, b


def test_the_llm_view_carries_the_rules_a_kid_is_judged_on(graph, fm):
    """🔴 Measured 2026-09-03: `--emit llm` was 45 lines to INJECTION.md's 271.

    The missing 226 were the entire contract — the metric, the taxonomy, the
    chain rules, the declared commands. A "view of what an LLM sees" that
    omits the rules is not a view of what an LLM sees, and it is why the
    viewport could not replace the renderer.
    """
    _m, b = _brief()
    frames = V.frame_stream(graph, fm, "goal:a", 3)
    llm = V.render_llm(frames, 0, 0, 50, 300, brief=b)

    for section in ("## graph snapshot", "## verdict taxonomy",
                    "## chain rules", "## attractive ideas"):
        assert section in llm, f"the llm view omits {section}"
    assert "evidence_runs >= 1" in llm, "the evidence rule must reach the kid"
    assert "chain length is never a target" in llm


def test_both_readers_are_told_the_same_facts(graph, fm):
    """The briefing is ONE object rendered twice, never two computations."""
    _m, b = _brief()
    frames = V.frame_stream(graph, fm, "goal:a", 3)
    llm = V.render_llm(frames, 0, 0, 50, 300, brief=b)
    human = "\n".join(V.render_human(frames, 0, 0, 50, 300, brief=b))

    for needle in ("42", "outcome_coverage", "0.375"):
        assert needle in llm and needle in human, (
            f"{needle!r} must reach both readers or they disagree about one graph")


def test_the_briefing_never_disturbs_the_frame_order(graph, fm):
    """🔴 The regression this nearly shipped with.

    `_verify` extracted node ids from "any line containing a backtick". The
    briefing is full of backticks — `metric_primary`, the verdict taxonomy,
    every declared command — so adding it turned the verifier's own input into
    noise. A verifier that silently starts measuring different lines has
    stopped verifying, which is worse than one that fails.
    """
    _m, b = _brief()
    frames = V.frame_stream(graph, fm, "goal:a", 3)
    llm = V.render_llm(frames, 0, 0, 50, 300, brief=b)

    ids = [mm.group(1) for mm in
           (V._FRAME_LINE.match(ln) for ln in llm.splitlines()) if mm]
    assert ids == [f.node_id for f in frames]

    naive = [ln.split("`")[1] for ln in llm.splitlines() if "`" in ln]
    assert naive != ids, (
        "if the naive match still works, this test is not testing anything")


def test_no_briefing_is_a_supported_state(graph, fm):
    """A viewport that can draw the graph beats one that refuses to start."""
    frames = V.frame_stream(graph, fm, "goal:a", 3)
    llm = V.render_llm(frames, 0, 0, 50, 300, brief=None)
    assert "## chain rules" not in llm
    ids = [mm.group(1) for mm in
           (V._FRAME_LINE.match(ln) for ln in llm.splitlines()) if mm]
    assert ids == [f.node_id for f in frames]


def test_the_compact_projection_states_the_same_numbers(graph, fm):
    """to_compact drops the rules text, never the facts."""
    m, b = _brief()
    compact = "\n".join(m.to_compact(b))
    full = "\n".join(m.to_markdown(b))
    for needle in ("42", "0.375", "outcome_coverage"):
        assert needle in compact and needle in full


def test_a_gameable_primary_is_named_as_invalid_in_the_briefing():
    """Never hand agents a target the engine itself rejects."""
    m, b = _brief()
    b.primary = "longest_chain_length"
    b.primary_is_gameable = True
    out = "\n".join(m.to_markdown(b))
    assert "not a valid" in out and "gameable" in out
