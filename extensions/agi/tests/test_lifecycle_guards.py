"""`goal:s25` and `goal:s26` — two guards on bookkeeping that moves the metric.

Both exist because of the same pattern this session found three times:
lifecycle and scaffolding bookkeeping leaking into `outcome_coverage`. A goal
wrongly marked `complete` scores (since `goal:g5` shipped), and a corpus built
from the wrong directory lets a verdict cite a node that is not in the graph.
"""
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import evidence_gate as eg   # noqa: E402


# ------------------------------------------------ goal:s25 — build_corpus


def _node(d: Path, nid: str):
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{nid.split(':')[-1]}.md").write_text(f"---\nid: {nid}\ntype: mvp\n---\nbody\n")


def test_build_corpus_reads_a_real_nodes_dir(tmp_path):
    _node(tmp_path / "nodes" / "mvp", "mvp:real")
    assert eg.build_corpus(tmp_path / "nodes") == frozenset({"mvp:real"})


def test_build_corpus_refuses_a_project_root(tmp_path):
    """The measured hazard: handed a project root it returned 657 ids vs
    29,582 — the purged gamed corpus resurrected — so a verdict citing a
    deleted node would resolve and pass the gate (goal:s10 -> goal:s25)."""
    _node(tmp_path / "nodes" / "mvp", "mvp:real")
    _node(tmp_path / "stray", "mvp:not-in-the-graph")

    with pytest.raises(eg.CorpusRootError) as exc:
        eg.build_corpus(tmp_path)
    assert "nodes" in str(exc.value)

    # and the correct call is unaffected by the stray file next door
    assert eg.build_corpus(tmp_path / "nodes") == frozenset({"mvp:real"})


def test_a_missing_directory_is_still_empty_not_an_error(tmp_path):
    """A project with no graph yet is a legitimate state (`goal:g5`'s
    three-depths invariant), not a mistake. Unchanged behaviour."""
    assert eg.build_corpus(tmp_path / "nowhere") == frozenset()


def test_the_three_live_callers_still_pass(tmp_path):
    """`goal:s25`'s falsifier, second half. The guard is worthless if it
    breaks the callers it was written to protect."""
    _node(tmp_path / "nodes" / "mvp", "mvp:real")
    root = tmp_path
    assert eg.build_corpus(root / "nodes") == frozenset({"mvp:real"})


# ------------------------------------- goal:s26 — premature `complete`


def _goal_fm(gid, status, kind="subgoal", parents=None):
    return {
        "type": "goal", "goal_id": gid, "status": status,
        "goal_kind": kind, "parents": parents or [],
    }


def _snapshot_goals():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "snapshot_goals_mod", BIN / "snapshot-goals.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_a_complete_root_with_a_live_subgoal_warns(capsys):
    """The owner's rule, and it caught a real misclassification: the 2026-09-02
    sweep recommended `goal:g5` -> `complete` while `goal:g5.1` was horizon."""
    sg = _snapshot_goals()
    existing = {
        "goal:g5": _goal_fm("G5", "complete", kind="long-term"),
        "goal:g5.1": _goal_fm("G5.1", "horizon", parents=["goal:g5"]),
    }
    offenders = sg.warn_premature_complete(existing)
    assert offenders == [("G5", "G5.1", "horizon")]
    assert "goal:s26" in capsys.readouterr().err


def test_active_and_horizon_subgoals_both_count(capsys):
    sg = _snapshot_goals()
    existing = {
        "goal:g5": _goal_fm("G5", "complete", kind="long-term"),
        "goal:g5.1": _goal_fm("G5.1", "active", parents=["goal:g5"]),
        "goal:g5.2": _goal_fm("G5.2", "horizon", parents=["goal:g5"]),
    }
    assert len(sg.warn_premature_complete(existing)) == 2


def test_a_fully_finished_tree_is_silent(capsys):
    """Retire or complete every subgoal and the warning goes — g5.26's
    falsifier, second clause."""
    sg = _snapshot_goals()
    existing = {
        "goal:g5": _goal_fm("G5", "complete", kind="long-term"),
        "goal:g5.1": _goal_fm("G5.1", "complete", parents=["goal:g5"]),
        "goal:g5.2": _goal_fm("G5.2", "retired", parents=["goal:g5"]),
    }
    assert sg.warn_premature_complete(existing) == []
    assert capsys.readouterr().err == ""


def test_a_childless_short_term_goal_never_warns(capsys):
    """Third falsifier clause: the rule is about roots with live children and
    nothing else. A completed S-goal is the normal success case."""
    sg = _snapshot_goals()
    existing = {"goal:s22": _goal_fm("S22", "complete", kind="short-term")}
    assert sg.warn_premature_complete(existing) == []
    assert capsys.readouterr().err == ""


def test_it_is_a_warning_and_never_a_failure(capsys):
    """A hard error would make retiring a tree bottom-up, one commit per goal,
    unrepresentable — and `goal:g5` says a project stays legitimate at every
    depth. Returning offenders rather than raising is the whole contract."""
    sg = _snapshot_goals()
    existing = {
        "goal:g5": _goal_fm("G5", "complete", kind="long-term"),
        "goal:g5.1": _goal_fm("G5.1", "active", parents=["goal:g5"]),
    }
    assert sg.warn_premature_complete(existing)   # returns, does not raise


# --------------------------------- goal:s23 — load retired, do not render


def test_deprecated_node_ids_is_the_single_definition(tmp_path):
    """One predicate, in `metrics.py`, beside `node_lifecycle_stats`. A second
    copy in the renderer would be `goal:s17` again."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("m_mod", BIN / "metrics.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    d = tmp_path / "nodes" / "build"
    d.mkdir(parents=True)
    (d / "live.md").write_text("---\nid: build:live\ntype: build\n---\nx\n")
    (d / "dead.md").write_text(
        "---\nid: build:dead\ntype: build\nstatus: deprecated\n---\nx\n")

    assert m.deprecated_node_ids(tmp_path / "nodes") == frozenset({"build:dead"})
    # and it agrees with the count that was already published
    stats = m.node_lifecycle_stats(tmp_path / "nodes", 2)
    assert stats["deprecated_node_count"] == 1


def test_the_injected_map_hides_retired_nodes_without_mutating_the_graph():
    """`goal:s23`'s falsifier, both halves in one test: the map loses the
    retired node while the graph it was built from keeps it, because
    `by_type` counts and `find_chains` still read `g` a few lines later.

    🔴 **Retargeted 2026-09-03 (L1.05).** This used to exercise
    `render-context.py`'s `_LiveOnly` graph view. That file was retired and
    `inject.py` took over, and the filter did not come with it — the map
    looked correct only because the single retired build node happened to sit
    outside depth 3 of any root. Anchoring on its parent showed it at once.

    The invariant is the map's, not any one class's, so the test follows the
    invariant to whatever now implements it: `frame_stream(hide_deprecated=)`.
    The human viewport deliberately does the opposite and shows retired mass,
    which is why this is a flag and not a default.
    """
    import importlib.util
    src = BIN.parent / "src"
    sys.path.insert(0, str(src))

    spec = importlib.util.spec_from_file_location("vp_mod", BIN / "viewport.py")
    vp = importlib.util.module_from_spec(spec)
    sys.modules["vp_mod"] = vp
    spec.loader.exec_module(vp)

    class _N:
        def __init__(self, nid, ntype, children=()):
            self.id, self.type = nid, ntype
            self.children, self.parents = set(children), set()

    class _G:
        def __init__(self, nodes):
            self._n = {n.id: n for n in nodes}
        @property
        def nodes(self): return list(self._n.values())
        def __len__(self): return len(self._n)
        def has_node(self, nid): return nid in self._n
        def get_node(self, nid): return self._n.get(nid)

    g = _G([_N("idea:a", "idea", ["build:dead", "build:live"]),
            _N("build:dead", "build", ["verdict:under-dead"]),
            _N("verdict:under-dead", "verdict"),
            _N("build:live", "build")])
    fm = {"idea:a": {"title": "A", "status": "active"},
          "build:dead": {"title": "Dead", "status": "deprecated"},
          "verdict:under-dead": {"title": "Below", "status": "active"},
          "build:live": {"title": "Live", "status": "active"}}

    hidden = [f.node_id for f in
              vp.frame_stream(g, fm, "idea:a", 3, hide_deprecated=True)]
    assert "build:dead" not in hidden, "a retired node reached the injected map"
    assert "verdict:under-dead" not in hidden, (
        "a node reachable only through a retired parent is not a live head")
    assert hidden == ["idea:a", "build:live"]

    # The human viewport shows retired mass on purpose -- damage, not a
    # flattering picture. Same stream, different scope.
    shown = [f.node_id for f in vp.frame_stream(g, fm, "idea:a", 3)]
    assert "build:dead" in shown

    # A view, never a removal: the graph is untouched either way.
    assert len(g) == 4
    assert g.get_node("build:dead") is not None


# ------------------------- goal:s27 — a parent's completion is its kids'


def _completion():
    # Plain import: `BIN` is on sys.path, and loading it through
    # `importlib.util` without registering it in `sys.modules` leaves
    # `cls.__module__` unresolvable, which breaks `dataclasses` inside
    # `node_writer` — a real failure this test hit and a good reason to prefer
    # the ordinary import wherever the module name is importable.
    import completion
    return completion


def _scaffolded(root: Path, nid: str, filled: bool):
    """Write a node that is either an untouched scaffold or real work."""
    c = _completion()
    d = root / "nodes" / nid.split(":", 1)[0]
    d.mkdir(parents=True, exist_ok=True)
    body = c.scaffold_body_for(nid) if not filled else "\n# real work the kid did\n"
    (d / f"{nid.split(':')[-1]}.md").write_text(
        f"---\nid: {nid}\ntype: {nid.split(':', 1)[0]}\n---\n{body}")


def test_a_parent_is_complete_when_all_its_kids_are(tmp_path):
    c = _completion()
    _scaffolded(tmp_path, "experiment:k1", filled=True)
    _scaffolded(tmp_path, "experiment:k2", filled=True)
    assert c.owns_all_complete(tmp_path, ["experiment:k1", "experiment:k2"])


def test_a_parent_is_not_complete_while_one_kid_is_unfilled(tmp_path):
    c = _completion()
    _scaffolded(tmp_path, "experiment:k1", filled=True)
    _scaffolded(tmp_path, "experiment:k2", filled=False)
    assert not c.owns_all_complete(tmp_path, ["experiment:k1", "experiment:k2"])


def test_owning_nothing_is_not_complete(tmp_path):
    """A parent that spawned nothing did not finish its loop, it failed to
    start one. Returning True here would make the most common parent failure
    indistinguishable from success — the shape that hid the dropped-verdict
    bug for the whole life of the pi runtime."""
    c = _completion()
    assert not c.owns_all_complete(tmp_path, [])
    assert not c.owns_all_complete(tmp_path, None)
    assert not c.owns_all_complete(tmp_path, ["   "])


def test_no_harness_name_reaches_the_parent_completion_path():
    """`goal:g4.6`'s invariant. Tier is first-class in this engine; a harness
    name is not. Branching on the first is not what that goal forbids."""
    import ast
    src = (BIN / "completion.py").read_text()
    tree = ast.parse(src)
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    names |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    for banned in ("pi", "claude", "harness", "pid", "poll"):
        assert banned not in names, f"{banned!r} leaked into the completion path"


# ------------------- goal:s29 — where a build node may come from


def _rules():
    import spawn_gate as sg
    return sg, sg.load_spawn_rules(
        Path(__file__).resolve().parents[3] / ".agi/context/schemas")


def test_a_goal_alone_can_never_be_a_build_parent_shape():
    """`goal:s29`'s invariant, which is what this guard has always been for.

    Widened 2026-09-05 from "exactly two shapes" to "these four, and never a
    lone goal": the goal that motivated a version may now join an `mvp` or a
    census `idea` lineage. Pinning the count made the guard fail on a widening
    that kept the invariant intact, which is a guard measuring the wrong thing
    -- the thing that must never be true is `[goal]` on its own, because that
    is a goal minting a file out of nothing.
    """
    sg, rules = _rules()
    s = rules.get("build")
    assert not s.error, s.error
    expected = {("mvp",), ("build", "goal"), ("goal", "mvp"), ("goal", "idea")}
    for variant in ("code", "prose"):
        r = s.variants[variant]
        assert set(r.parent_shapes) == expected, variant
        assert ("goal",) not in r.parent_shapes, variant
        assert sorted(r.allowed_parents) == ["build", "goal", "idea", "mvp"]
        # `idea` is admitted in exactly one shape, always beside a goal, so it
        # can never mint a build node the way the census once did.
        idea_shapes = [sh for sh in r.parent_shapes if "idea" in sh]
        assert idea_shapes == [("goal", "idea")], variant


def test_parent_shapes_is_an_or_across_whole_shapes_not_an_and():
    """`min_parents_by_type` is an AND across kinds; this is an OR across
    shapes. `build`'s rule is genuinely a disjunction — one mvp, OR a build
    and a goal together — and neither half alone."""
    sg, _ = _rules()
    block = {
        "allowed_parents": ["mvp", "build", "goal"],
        "min_parents": 1, "max_parents": 2,
        "parent_shapes": [["mvp"], ["build", "goal"]],
    }
    rule, err = sg._parse_rule(block)
    assert not err, err
    assert rule.parent_shapes == (("mvp",), ("build", "goal"))


def test_a_shape_naming_a_disallowed_type_is_refused():
    """Same discipline as `min_parents_by_type`: a schema declaring a rule
    nobody can satisfy rejects its whole type forever, loudly and uselessly."""
    sg, _ = _rules()
    rule, err = sg._parse_rule({
        "allowed_parents": ["mvp"], "min_parents": 1, "max_parents": 2,
        "parent_shapes": [["mvp"], ["build", "goal"]],
    })
    assert rule is None and "allowed_parents does not permit" in err


def test_a_shape_outside_the_min_max_bounds_is_refused():
    sg, _ = _rules()
    rule, err = sg._parse_rule({
        "allowed_parents": ["mvp", "build", "goal"],
        "min_parents": 1, "max_parents": 1,
        "parent_shapes": [["build", "goal"]],
    })
    assert rule is None and "outside spawn.min_parents" in err


def test_absent_parent_shapes_leaves_every_other_type_alone():
    """Empty tuple = no shape restriction. Every type that does not declare
    `parent_shapes` must behave exactly as before."""
    sg, rules = _rules()
    rule, err = sg._parse_rule({
        "allowed_parents": ["goal"], "min_parents": 1, "max_parents": 2})
    assert not err and rule.parent_shapes == ()
    hyp = rules.get("hypothesis")
    if hyp and hyp.flat:
        assert hyp.flat.parent_shapes == ()
