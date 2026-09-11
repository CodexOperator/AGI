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


# --------------------------------------------------------------------------
# The sanctuary theme (hypothesis:l3w4-sanctuary-theme).
# --------------------------------------------------------------------------

_SEAT_ROWS = [
    {"name": "belam", "role": "prime_director", "tier": 3},
    {"name": "adv-self-perpetuating", "role": "parent", "tier": 3},
    {"name": "adv-all-is-one", "role": "parent", "tier": 3},
    {"name": "adv-alive", "role": "parent", "tier": 3},
    {"name": "liaison", "role": "director", "tier": 1},
    {"name": "dir-g1", "role": "director", "tier": 1},
]


def test_sanctuary_frame_builds_scene_from_seat_rows_fixture():
    """tier-3 rows are mantled spirits; tier-1 director rows are probe wisps."""
    scene = V.sanctuary_frame(_SEAT_ROWS, [1, 2, 3], None)
    assert scene.registry_present is True
    assert scene.ephemeral_wisps == 3
    assert scene.rotating is None
    assert [s["name"] for s in scene.spirits] == [
        "belam", "adv-self-perpetuating", "adv-all-is-one", "adv-alive"]
    assert [p["name"] for p in scene.probes] == ["liaison", "dir-g1"]


def test_sanctuary_mantled_tier_non_three_joins_spirits():
    """A seated Sanctuary Master sits on her mantle, not her tier."""
    rows = _SEAT_ROWS + [{"name": "sanctuary-master", "role": "director",
                          "tier": 1, "mantled": True}]
    scene = V.sanctuary_frame(rows, [], None)
    names = [s["name"] for s in scene.spirits]
    assert "sanctuary-master" in names
    assert all(p["name"] != "sanctuary-master" for p in scene.probes)


def test_sanctuary_theme_shows_no_registry_when_seats_missing():
    """Absent seats => 'no seat registry yet' in both readers, no traceback."""
    scene = V.SanctuaryScene((), (), 0, None, False)
    assert V.render_sanctuary_human(scene) == ["no seat registry yet"]
    assert "no seat registry yet" in V.render_sanctuary_llm(scene)


def test_sanctuary_rotating_strand_names_holder_and_seat():
    """A `<seat>.genN` window resolves the strand to that row's rotated_by."""
    rows = _SEAT_ROWS + [{"name": "belam", "role": "prime_director", "tier": 3,
                          "rotated_by": "quorum"}]
    windows = ["agi-rc:0", "belam.gen2", "dir-g1.gen1"]
    rot = V.rotating_seat(rows, windows)
    assert rot == ("quorum", "belam")
    scene = V.sanctuary_frame(rows, [], rot)
    human = "\n".join(V.render_sanctuary_human(scene))
    llm = V.render_sanctuary_llm(scene)
    assert "quorum ~~~✧~~~> belam (rotating)" in human
    assert "quorum ~~~✧~~~> belam" in llm


def test_sanctuary_non_seat_gen_window_is_ignored():
    """A `.genN` window that names no seat is not invented into a strand."""
    rows = [{"name": "belam", "role": "prime_director", "tier": 3}]
    assert V.rotating_seat(rows, ["unknown.gen1"]) is None


def test_sanctuary_human_and_llm_state_the_same_spirits_and_wisps():
    """Both readers draw the identical spirits, probes, and ephemeral count."""
    scene = V.sanctuary_frame(_SEAT_ROWS, [1, 2], ("quorum", "belam"))
    human = "\n".join(V.render_sanctuary_human(scene))
    llm = V.render_sanctuary_llm(scene)
    for s in scene.spirits:
        assert s["name"] in human and f"spirit {s['name']}" in llm
    for p in scene.probes:
        assert p["name"] in human and f"probe {p['name']}" in llm
    assert "2 ephemeral wisps" in human and "ephemeral_wisps: 2" in llm


# --------------------------------------------------------------------------
# hypothesis:l3w4-seat-graph-view — seats render ON the graph, not beside it.
# One OccupantIndex, two readers (goal:g9.7 applied one level down). Three
# red-first tests from the claim: an attached seat appears on its node's line;
# that seat is NOT in the idle band; a seat with no target IS in the idle band
# and on no node line.
# --------------------------------------------------------------------------


def _occ(at_nodes, idle):
    return V.OccupantIndex._from(at_nodes, idle)


def test_an_attached_seat_renders_inline_on_its_nodes_line(graph, fm):
    """The claim's first falsifier, rendered both ways: a seat joined to a node
    appears on that node's rendered line, in the human view and the llm view."""
    frames = V.frame_stream(graph, fm, "goal:a", 2)
    occ = _occ({"hypothesis:h1": ["belam"]}, ())

    human = V.render_human(frames, 0, 0, 30, 300, occupants=occ)
    h_line = [ln for ln in human if "H one" in ln][0]
    assert V.GLYPH["seat"] in h_line and "belam" in h_line
    # the node id the seat was joined to carries the seat; a sibling does not
    other = [ln for ln in human if "H two" in ln][0]
    assert "belam" not in other

    llm = V.render_llm(frames, 0, 0, 30, 300, occupants=occ)
    assert "seats=belam" in [ln for ln in llm.splitlines() if "h1" in ln][0]


def test_the_idle_band_does_not_contain_an_attached_seat(graph, fm):
    """The claim's second falsifier: attachment removes a seat from the band."""
    frames = V.frame_stream(graph, fm, "goal:a", 1)
    occ = _occ({"hypothesis:h1": ["liaison"]}, ("dir-g1", "dir-g15"))

    human = "\n".join(V.render_human(frames, 0, 0, 30, 300, occupants=occ))
    band = human.split("idle:")[1]
    assert "dir-g1" in band
    assert "liaison" not in band

    llm = V.render_llm(frames, 0, 0, 30, 300, occupants=occ)
    idle_section = llm.split("## idle seats")[1].split("## the graph")[0]
    assert "dir-g1" in idle_section and "dir-g15" in idle_section
    assert "liaison" not in idle_section


def test_a_seat_with_no_target_is_idle_and_on_no_node_line(graph, fm):
    """The claim's third falsifier: an unattached seat sits in the band and
    nowhere on the tree — a view that hides emptiness is worse than none."""
    frames = V.frame_stream(graph, fm, "goal:a", 2)
    occ = _occ({}, ("spare-seat",))

    human = V.render_human(frames, 0, 0, 30, 300, occupants=occ)
    on_lines = [ln for ln in human if "spare-seat" in ln]
    assert len(on_lines) == 1
    assert "idle:" in on_lines[0]

    llm = V.render_llm(frames, 0, 0, 30, 300, occupants=occ)
    assert "spare-seat" in llm.split("## idle seats")[1].split("## the graph")[0]
    assert "spare-seat" not in [ln for ln in llm.splitlines() if "- `" in ln]


def test_seat_index_joins_a_pinned_seat_through_its_manifest_target():
    """The join itself: a seat's meter pin names its session, whose agent id is
    the manifest row carrying the node it works on."""
    agents = [{"id": "a00-abc123", "target": "hypothesis:h1",
               "tier": "parent", "role": None}]
    rows = [{"name": "belam", "role": "prime_director"},
            {"name": "dir-g16", "role": "director"}]
    sessions = {"belam": "/g/.agi/sessions/a00-abc123/output.log"}
    at_nodes, idle = V.seat_index(agents, rows, sessions)
    assert at_nodes == {"hypothesis:h1": ["belam"]}
    assert idle == ["dir-g16"]


def test_seat_index_never_invents_a_node_for_a_rowless_session():
    """A session whose agent id is absent from the manifest is idle, not placed."""
    agents = [{"id": "a00-other", "target": "goal:x"}]
    rows = [{"name": "liaison", "role": "director"}]
    at_nodes, idle = V.seat_index(agents, rows,
                                  {"liaison": "/g/.agi/sessions/a00-ghost/log"})
    assert at_nodes == {}
    assert idle == ["liaison"]


# --------------------------------------------------------------------------
# ROUND 2 — the layered map (hypothesis:l3w4-seat-graph-view). THE TIE IS
# THE POINT: each quorum advisor is anchored to its ONE vision by
# `personality_ref`, each director-kid to its ONE perpetual goal by
# `owning_goal`. One `AnchorIndex`, two readers (goal:g9.7 one level down).
# --------------------------------------------------------------------------

_FULL_ROWS = [
    {"name": "belam", "role": "prime_director", "tier": 3},
    {"name": "adv-self-perpetuating", "role": "parent", "tier": 3,
     "personality_ref": "vision:self-perpetuating"},
    {"name": "adv-all-is-one", "role": "parent", "tier": 3,
     "personality_ref": "vision:all-is-one"},
    {"name": "adv-alive", "role": "parent", "tier": 3,
     "personality_ref": "vision:alive"},
    {"name": "liaison", "role": "director", "tier": 1,
     "owning_goal": "goal:g17"},
    {"name": "dir-g1", "role": "director", "tier": 1,
     "owning_goal": "goal:g1"},
]

_FM = {"vision:self-perpetuating": {"title": "V"},
       "vision:all-is-one": {"title": "V"},
       "vision:alive": {"title": "V"},
       "goal:g17": {"title": "G"},
       "goal:g1": {"title": "G"}}


def test_the_tie_resolves_advisor_to_vision_and_director_to_goal():
    """Round 2's falsifier: an advisor's `personality_ref` and a director's
    `owning_goal` both bind the seat to a graph node — the tie rendered for
    the first time. It must resolve, not be guessed."""
    ai = V.build_anchor_index(_FULL_ROWS, _FM)
    by_name = {r["name"]: r for r in ai.anchored}
    assert by_name["adv-self-perpetuating"]["anchor"] == "vision:self-perpetuating"
    assert by_name["adv-all-is-one"]["anchor"] == "vision:all-is-one"
    assert by_name["adv-alive"]["anchor"] == "vision:alive"
    assert by_name["liaison"]["anchor"] == "goal:g17"
    assert by_name["dir-g1"]["anchor"] == "goal:g1"


def test_a_seat_with_no_tie_is_unanchored_never_invented():
    """belam has neither personality_ref nor owning_goal, and an unresolvable
    ref (engine-gone vision) must not become a fabricated anchor."""
    rows = [{"name": "belam", "role": "prime_director", "tier": 3},
            {"name": "ghost", "role": "parent", "tier": 3,
             "personality_ref": "vision:GONE"}]
    ai = V.build_anchor_index(rows, _FM)
    assert ai.anchored == ()
    assert {r["name"] for r in ai.unanchored} == {"belam", "ghost"}


def test_hierarchy_renders_each_seat_at_its_anchor_both_readers(graph, fm):
    """The layered-map falsifier: the hierarchy layer names each seat's anchor
    in the HUMAN pane and the LLM pane, g9.7 one level down."""
    ai = V.build_anchor_index(_FULL_ROWS, _FM)
    human = "\n".join(V.hierarchy_lines(ai))
    for needle in ("→ vision:self-perpetuating", "→ goal:g17",
                   "belam", "adv-alive"):
        assert needle in human

    frames = V.frame_stream(graph, fm, "goal:a", 2)
    llm = V.render_llm(frames, 0, 0, 30, 300, occupants=None,
                       anchors=ai, layer="graph")
    for needle in ("## agent hierarchy",
                   "seat adv-self-perpetuating (parent, tier 3) "
                   "→ vision:self-perpetuating",
                   "seat liaison (director, tier 1) → goal:g17",
                   "_map_layer_on_top: graph_"):
        assert needle in llm, f"llm view omits {needle!r}"


def test_layer_on_top_swaps_which_layer_renders_faint(graph, fm):
    """The toggle's render half: with the graph on top the hierarchy is the
    faint under-layer, and vice versa — the same `AnchorIndex`, one edit."""
    ai = V.build_anchor_index(_FULL_ROWS, _FM)
    frames = V.frame_stream(graph, fm, "goal:a", 2)

    graph_top = V.render_human(frames, 0, 0, 30, 300, occupants=None,
                               anchors=ai, layer="graph")
    hier_top = V.render_human(frames, 0, 0, 30, 300, occupants=None,
                              anchors=ai, layer="hierarchy")
    assert "map layers: on top = graph" in "\n".join(graph_top)
    assert "map layers: on top = hierarchy" in "\n".join(hier_top)
    # under-layer is faint-prefixed; the top layer's blocks are not
    assert any(ln.startswith("~ agent hierarchy") for ln in graph_top)
    assert not any(ln.startswith("~ agent hierarchy") for ln in hier_top)
    # graph frame lines stay full whenever the graph is on top
    assert not any(ln.startswith("~ ●") and "Goal A" in ln for ln in graph_top)


def test_the_layered_llm_keeps_frame_ids_parseable(graph, fm):
    r"""Adding the hierarchy block must not break _verify's frame-id scan:
    the graph lines stay in `- id` backticked form, and `- seat …` lines
    never match _FRAME_LINE."""
    ai = V.build_anchor_index(_FULL_ROWS, _FM)
    frames = V.frame_stream(graph, fm, "goal:a", 2)
    llm = V.render_llm(frames, 0, 0, 30, 300, occupants=None,
                       anchors=ai, layer="hierarchy")
    ids = [m.group(1) for m in (V._FRAME_LINE.match(ln) for ln in llm.splitlines())
           if m]
    assert ids == [f.node_id for f in frames]


def test_the_live_map_prints_no_secret():
    """The owner is about to livestream this view; NO pane may carry a secret.
    The round-2 code must not reference creds or files that hold them."""
    src = (BIN / "viewport.py").read_text()
    round2 = src[src.index("ROUND 2"):]
    for forbidden in ("Authorization", "token", "api_key", "api-key",
                      "secret", ".env", "password"):
        assert forbidden.lower() not in round2.lower(), (
            f"layered map may not print a secret: found {forbidden!r}")


def test_the_map_toggle_is_bound_in_the_interactive_tui():
    """The keypress half of the toggle must exist, not just the render half."""
    src = (BIN / "viewport.py").read_text()
    assert "m swap layer" in src
    assert 'layer = "hierarchy" if layer == "graph" else "graph"' in src


def test_town_is_derived_via_the_shared_helper_from_the_frame(tmp_path):
    """hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council — each
    Frame carries the town of its nearest vision, derived through the SAME
    helper node_writer/brief/zoom use (never a branch on a town NAME,
    goal:g8.2), only when a nodes_dir is offered; without one it is ''.
    A goal whose vision_ref lands in a non-core town renders town=<that>.
    """
    nodes = tmp_path / "nodes"
    (nodes / "vision").mkdir(parents=True)
    (nodes / "vision" / "va.md").write_text(
        "---\nid: vision:va\ntype: vision\ntown: townA\n---\nbody\n",
        encoding="utf-8")
    (nodes / "goal").mkdir()
    (nodes / "goal" / "g.md").write_text(
        "---\nid: goal:g\ntype: goal\nparents:\n  - vision:va\n"
        "title: G town\n---\nbody\n", encoding="utf-8")
    g = _Graph([_Node("goal:g", "goal", ["vision:va"]),
                _Node("vision:va", "vision")])
    fm = {"goal:g": {"title": "G town"}, "vision:va": {"town": "townA"}}

    frames = V.frame_stream(g, fm, "goal:g", 3,
                            nodes_dir=str(nodes))
    assert frames[0].node_id == "goal:g"
    assert frames[0].town == "townA"
    # Without a nodes_dir the annotation is absent, not guessed.
    frames_no_src = V.frame_stream(g, fm, "goal:g", 3)
    assert frames_no_src[0].town == ""
