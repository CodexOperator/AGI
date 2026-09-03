"""Tests for bin/metrics.py — the H3 replacement for the gameable primary metric.

Core claims under test:
- the default primary metric is never `longest_chain_length`
- `evidence_fraction` is computable from the corpus and cannot be inflated by
  adding hops (the exact gaming that produced H3 and H0c)
"""

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"

# Load evidence_gate first and register it in sys.modules *before* metrics is
# loaded, so metrics.py's own `from evidence_gate import ...` binds the exact
# same function objects this test module holds — needed for the identity
# check in test_metrics_shares_evidence_gates_normalize_function below.
eg_spec = importlib.util.spec_from_file_location("evidence_gate", BIN / "evidence_gate.py")
evidence_gate = importlib.util.module_from_spec(eg_spec)
sys.modules["evidence_gate"] = evidence_gate
eg_spec.loader.exec_module(evidence_gate)

spec = importlib.util.spec_from_file_location("metrics", BIN / "metrics.py")
metrics = importlib.util.module_from_spec(spec)
sys.modules["metrics"] = metrics
spec.loader.exec_module(metrics)


def _node(root, ntype, slug, fm_extra="", parents=(), body="body"):
    d = root / "nodes" / ntype.replace("-", "_")
    d.mkdir(parents=True, exist_ok=True)
    lines = ["---", f'id: "{ntype}:{slug}"', f"type: {ntype}"]
    if parents:
        lines.append("parents:")
        lines += [f"  - {p}" for p in parents]
    if fm_extra:
        lines.append(fm_extra.rstrip())
    lines += ["---", "", body, ""]
    (d / f"{slug}.md").write_text("\n".join(lines))


@pytest.fixture()
def project(tmp_path):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "nodes").mkdir()
    return tmp_path


# ------------------------------------------------------------ primary metric


def test_default_primary_is_not_the_gameable_metric():
    assert metrics.DEFAULT_METRIC_PRIMARY not in metrics.GAMEABLE_METRICS
    assert metrics.DEFAULT_METRIC_PRIMARY == "outcome_coverage"


def test_primary_falls_back_to_default_when_config_omits_it():
    assert metrics.primary_metric_name({}) == metrics.DEFAULT_METRIC_PRIMARY
    assert metrics.primary_metric_name({"metric_primary": "  "}) == \
        metrics.DEFAULT_METRIC_PRIMARY


def test_primary_honours_config():
    assert metrics.primary_metric_name({"metric_primary": "evidence_fraction"}) == \
        "evidence_fraction"


def test_gameable_primary_emits_a_warning(project, capsys):
    (project / "agi-tree.config.json").write_text(
        json.dumps({"metric_primary": "longest_chain_length"})
    )
    _node(project, "hypothesis", "h1")
    metrics.emit(project)
    out = capsys.readouterr()
    assert "gameable" in out.err
    assert "METRIC_WARNING gameable_primary=longest_chain_length" in out.out


def test_emit_prints_primary_name_and_value(project):
    (project / "agi-tree.config.json").write_text(
        json.dumps({"metric_primary": "evidence_fraction"})
    )
    _node(project, "experiment", "r1")
    _node(project, "verdict", "v1", "verdict: proved\nevidence_runs:\n  - experiment:r1")
    buf = io.StringIO()
    metrics.emit(project, out=buf)
    text = buf.getvalue()
    assert "METRIC primary_metric=evidence_fraction" in text
    assert "METRIC primary_value=1.0" in text


# --------------------------------------------------------- evidence_fraction


def test_evidence_fraction_counts_only_asserting_verdicts(project):
    _node(project, "experiment", "r1")
    _node(project, "verdict", "v1", "verdict: proved\nevidence_runs:\n  - experiment:r1")
    _node(project, "verdict", "v2", "verdict: inconclusive_lean_proved:60")
    _node(project, "verdict", "v3", "verdict: pending")   # excluded entirely
    _node(project, "hypothesis", "h1")                    # no verdict field
    s = metrics.evidence_stats(project / "nodes")
    assert s["verdicts_asserting"] == 2
    assert s["verdicts_pending"] == 1
    assert s["verdicts_evidence_backed"] == 1
    assert s["evidence_fraction"] == 0.5


def test_sentinel_evidence_runs_does_not_count_as_backed(project):
    """H4c: the exact defect. `evidence_runs: [synthetic]` must not satisfy
    `evidence_fraction`'s `>= 1` any more than it satisfies the gate's."""
    _node(project, "verdict", "v1", "verdict: proved\nevidence_runs:\n  - synthetic")
    s = metrics.evidence_stats(project / "nodes")
    assert s["verdicts_evidence_backed"] == 0
    assert s["evidence_fraction"] == 0.0
    assert s["unevidenced_decisive_verdicts"] == 1


def test_pending_without_evidence_does_not_lower_the_score(project):
    _node(project, "experiment", "r1")
    _node(project, "verdict", "v1", "verdict: proved\nevidence_runs:\n  - experiment:r1")
    before = metrics.evidence_stats(project / "nodes")["evidence_fraction"]
    for i in range(10):
        _node(project, "verdict", f"p{i}", "verdict: pending")
    after = metrics.evidence_stats(project / "nodes")["evidence_fraction"]
    assert before == after == 1.0


def test_unevidenced_decisive_counter_is_the_gate_violation_alarm(project):
    _node(project, "verdict", "v1", "verdict: proved")             # orphan
    _node(project, "verdict", "v2", "verdict: disproved\nevidence_runs: 3")
    s = metrics.evidence_stats(project / "nodes")
    assert s["decisive_verdicts"] == 2
    # goal:g7.3 — BOTH are unevidenced now. `evidence_runs: 3` used to buy v2
    # a pass here while naming nothing that could be checked; this assertion
    # read `== 1` until 2026-08-27 and was quietly measuring the hole.
    assert s["unevidenced_decisive_verdicts"] == 2
    assert s["decisive_evidence_fraction"] == 0.0


def test_a_resolvable_reference_still_counts_as_evidence(project):
    """The other half of goal:g7.3: closing the hole must not close the honest
    path. A verdict citing a real node is still decisive."""
    _node(project, "experiment", "e1", "type: experiment")
    _node(project, "verdict", "v1", 'verdict: proved\nevidence_runs: ["experiment:e1"]')
    s = metrics.evidence_stats(project / "nodes")
    assert s["unevidenced_decisive_verdicts"] == 0
    assert s["decisive_evidence_fraction"] == 1.0


def test_empty_corpus_is_zero_not_a_crash(project):
    s = metrics.evidence_stats(project / "nodes")
    assert s["evidence_fraction"] == 0.0
    assert s["unevidenced_decisive_verdicts"] == 0
    assert s["shadow_decisive_verdicts"] == 0


def test_shadow_counter_catches_a_status_that_contradicts_its_verdict(project):
    """`unevidenced_decisive_verdicts` reads `verdict:` only, so a demoted
    node whose `status:` still says 'proved' looks honest to it. That blind
    spot is what `shadow_decisive_verdicts` counts."""
    _node(project, "verdict", "v1",
          "status: proved\nverdict: inconclusive_lean_proved:50\nevidence_runs: 0")
    s = metrics.evidence_stats(project / "nodes")
    assert s["unevidenced_decisive_verdicts"] == 0      # verdict: is honest
    assert s["shadow_decisive_verdicts"] == 1           # status: is not
    assert s["shadow_decisive_no_verdict"] == 0


def test_shadow_counter_catches_a_verdict_expressed_only_as_status(project):
    """The worse case: no `verdict:` field at all, so the decisive claim is
    invisible to every other number in evidence_stats."""
    _node(project, "verdict", "v1", "status: proved")
    s = metrics.evidence_stats(project / "nodes")
    assert s["decisive_verdicts"] == 0                  # invisible, as designed
    assert s["verdicts_asserting"] == 0
    assert s["shadow_decisive_verdicts"] == 1
    assert s["shadow_decisive_no_verdict"] == 1


def test_shadow_counter_ignores_a_status_its_verdict_agrees_with(project):
    """Redundant, not contradictory — the gate demotes both together."""
    _node(project, "verdict", "v1", "status: proved\nverdict: proved\nevidence_runs: 3")
    assert metrics.evidence_stats(project / "nodes")["shadow_decisive_verdicts"] == 0


def test_shadow_counter_ignores_lifecycle_statuses(project):
    _node(project, "task", "t1", "status: pending")
    _node(project, "idea", "i1", "status: open")
    _node(project, "goal", "g1", "status: active")
    _node(project, "verdict", "v1", "status: open\nverdict: disproved\nevidence_runs: 3")
    assert metrics.evidence_stats(project / "nodes")["shadow_decisive_verdicts"] == 0


def test_shadow_counter_ignores_tags(project):
    """Tags keep 'proved' as a historical record of the original claim."""
    _node(project, "verdict", "v1",
          "verdict: inconclusive_lean_proved:50\ntags:\n  - proved")
    assert metrics.evidence_stats(project / "nodes")["shadow_decisive_verdicts"] == 0


def test_metrics_shares_evidence_gates_normalize_function():
    """One resolution function, not two — metrics.py must not drift from
    the gate (goal:g3.1 item 5: they read the same field, so they must
    share one definition or they will quietly disagree again)."""
    assert metrics.normalize_evidence_runs is evidence_gate.normalize_evidence_runs
    assert metrics.build_corpus is evidence_gate.build_corpus


def test_gate_and_metrics_agree_on_the_same_input(project):
    """Same evidence_runs value, evaluated through both entry points,
    produces the same count."""
    _node(project, "experiment", "real")
    corpus = evidence_gate.build_corpus(project / "nodes")
    for value in (["synthetic"], ["experiment:real"], ["experiment:ghost"], 3, None):
        gate_count = evidence_gate.normalize_evidence_runs(value, corpus=corpus)
        metrics_count = metrics.normalize_evidence_runs(value, corpus=corpus)
        assert gate_count == metrics_count


def test_adding_hops_cannot_inflate_evidence_fraction(project):
    """The H3 gaming attack: hops=2*cycle+8. Chain length moves; evidence doesn't."""
    _node(project, "experiment", "r1")
    _node(project, "verdict", "v1", "verdict: proved\nevidence_runs:\n  - experiment:r1")
    _node(project, "verdict", "v2", "verdict: disproved")
    base = metrics.compute(project)
    prev = "verdict:v1"
    for i in range(30):
        _node(project, "hypothesis", f"hop{i}", parents=[prev])
        prev = f"hypothesis:hop{i}"
    after = metrics.compute(project)
    assert after["longest_chain_length"] > base["longest_chain_length"]  # gamed
    assert after["evidence_fraction"] == base["evidence_fraction"] == 0.5  # immune


def test_compute_emits_the_full_metric_set(project):
    _node(project, "hypothesis", "h1")
    _node(project, "mvp", "m1", parents=["hypothesis:h1"])
    m = metrics.compute(project)
    for key in ("longest_chain_length", "avg_chain_depth", "mvp_count",
                "outcome_coverage", "chain_branching_factor", "node_count",
                "edge_count", "evidence_fraction", "evidence_weighted_depth",
                "unevidenced_decisive_verdicts"):
        assert key in m, key
    assert m["outcome_coverage"] == 1.0


def test_evidence_weighted_depth_is_zero_without_evidence(project):
    _node(project, "hypothesis", "h1")
    _node(project, "verdict", "v1", "verdict: proved", parents=["hypothesis:h1"])
    m = metrics.compute(project)
    assert m["evidence_weighted_depth"] == 0.0


# ------------------------------------------------- deep corpora (H0c/H3b class)

def test_deep_chain_does_not_blow_the_stack(project):
    """The agi-tree corpus is gamed to 2000 hops; the recursive walk died at ~990.

    A descriptive-only metric must never be able to abort the metrics stage.
    """
    _node(project, "idea", "n0000")
    for i in range(1, 2000):
        _node(project, "hypothesis", f"n{i:04d}",
              parents=[f"hypothesis:n{i - 1:04d}" if i > 1 else "idea:n0000"])

    m = metrics.compute(project)
    assert m["longest_chain_length"] == 1999


def test_cycle_in_parents_terminates(project):
    """Back-edges resolve rather than looping (chain_engine's convention)."""
    _node(project, "hypothesis", "a", parents=["hypothesis:b"])
    _node(project, "hypothesis", "b", parents=["hypothesis:a"])
    assert metrics.compute(project)["longest_chain_length"] >= 0


# --------------------------------------------------- goal lifecycle (goal:g5)


def _goal(root, gid, status):
    _node(root, "goal", gid, fm_extra=f"status: {status}")


def test_retired_goal_chains_stop_scoring_but_stay_attributable(project):
    """goal:g5 — a *retired* goal's chains keep their nodes and lose their
    score. Retiring a goal must not look like deleting its work.

    Used `complete` as the retired status until 2026-09-02, when the two
    states were split: `complete` now scores and only `retired` does not."""
    _goal(project, "g1", "active")
    _goal(project, "g2", "retired")
    _node(project, "hypothesis", "live", parents=["goal:g1"])
    _node(project, "mvp", "live-m", parents=["hypothesis:live"])
    _node(project, "hypothesis", "dead", parents=["goal:g2"])
    _node(project, "mvp", "dead-m", parents=["hypothesis:dead"])

    m = metrics.compute(project)
    # whole-graph totals are untouched — the work is still there
    assert m["mvp_count"] == 2
    # ...but only the live goal's chain scores
    assert m["scoring_mvp_count"] == 1
    assert m["scoring_hypothesis_count"] == 1
    assert m["retired_goal_nodes"] == 2
    assert m["outcome_coverage"] == 1.0


def test_horizon_goals_still_score(project):
    """`horizon` is declared-and-committed, not retired."""
    _goal(project, "g1", "horizon")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    m = metrics.compute(project)
    assert m["scoring_hypothesis_count"] == 1
    assert m["retired_goal_nodes"] == 0


def test_unattributed_nodes_keep_scoring(project):
    """Attribution is a reason to exclude, never the only reason to include.
    Most of this corpus predates goal nodes; zeroing it would be a metric
    change wearing a lifecycle rule as a disguise."""
    _node(project, "hypothesis", "orphan")
    _node(project, "mvp", "orphan-m", parents=["hypothesis:orphan"])
    m = metrics.compute(project)
    assert m["scoring_hypothesis_count"] == 1
    assert m["scoring_mvp_count"] == 1
    assert m["unattributed_nodes"] == 2
    assert m["retired_goal_nodes"] == 0


def test_node_shared_with_a_live_goal_still_scores(project):
    """Retired only when *every* goal it answers to is retired."""
    _goal(project, "g1", "active")
    _goal(project, "g2", "retired")
    _node(project, "hypothesis", "shared", parents=["goal:g1", "goal:g2"])
    m = metrics.compute(project)
    assert m["scoring_hypothesis_count"] == 1
    assert m["retired_goal_nodes"] == 0


def test_horizon_goal_keeps_scoring(project):
    """A `horizon` goal is in SCORING_GOAL_STATUSES and its children must
    score identically to `active`. This is trivially true via the same code
    path, but no test asserts it -- and a regression that removed `horizon`
    from the set would silently lose coverage."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"])
    before = metrics.compute(project)

    _goal(project, "g1", "horizon")
    after = metrics.compute(project)

    assert after["outcome_coverage"] == before["outcome_coverage"]
    assert (after["scoring_mvp_count"], after["scoring_hypothesis_count"]) == (1, 1)
    assert after["retired_goal_nodes"] == 0
    assert after["goals_horizon"] == 1
    assert after["goals_active"] == 0


def test_goal_status_counts_are_emitted(project):
    _goal(project, "g1", "active")
    _goal(project, "g2", "horizon")
    _goal(project, "g3", "complete")
    _goal(project, "g4", "phasing-out")
    _goal(project, "g5", "retired")
    m = metrics.compute(project)
    # goal:g5 — `goals_retired` used to include `complete`, the same collapse
    # SCORING_GOAL_STATUSES made. A finished goal is not a retired one.
    assert (m["goals_active"], m["goals_horizon"]) == (1, 1)
    assert m["goals_complete"] == 1
    assert m["goals_retired"] == 2          # phasing-out (legacy) + retired
    assert m["goal_count"] == 5


# ------------------------------- goal:g5 falsifier: complete vs retired
# The goal's own revision (2026-09-01) states three clauses and this is each
# of them as a test. All three were unobservable on the live corpus the day
# they were written -- 1 retired goal, 0 hypotheses under it -- so fixtures
# are the only place they can be checked before a sweep creates the shape.


def test_completing_a_goal_does_not_move_the_metric(project):
    """Clause 1, and the defect that forced the revision.

    Marking a goal with a closed hypothesis->mvp chain `complete` must leave
    `outcome_coverage` exactly where it was. Measured on 2026-09-01: a sweep
    marked nine goals complete/retired on falsifiers and coverage fell
    0.27 -> 0.232 with no work undone. A metric that drops when you finish
    teaches you not to finish.
    """
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"])
    before = metrics.compute(project)["outcome_coverage"]

    _goal(project, "g1", "complete")        # same gid, rewritten status
    after = metrics.compute(project)

    assert after["outcome_coverage"] == before
    assert (after["scoring_mvp_count"], after["scoring_hypothesis_count"]) == (1, 1)
    assert after["retired_goal_nodes"] == 0


def test_retiring_a_goal_removes_its_closed_chain_from_both_terms(project):
    """Clause 2. A chain that concluded "retire this goal" produced evidence
    *for stopping* -- a decision about the graph, not a contribution to it.
    Counting it would reward abandoning goals, so it leaves numerator and
    denominator together."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "keep", parents=["goal:g1"])
    _node(project, "mvp", "keep-m", parents=["hypothesis:keep"])
    _goal(project, "g2", "active")
    _node(project, "hypothesis", "drop", parents=["goal:g2"])
    _node(project, "mvp", "drop-m", parents=["hypothesis:drop"])
    assert metrics.compute(project)["scoring_mvp_count"] == 2

    _goal(project, "g2", "retired")
    m = metrics.compute(project)

    assert (m["scoring_mvp_count"], m["scoring_hypothesis_count"]) == (1, 1)
    assert m["retired_goal_nodes"] == 2     # both, still in the graph
    assert m["mvp_count"] == 2              # descriptive total untouched


def test_retiring_a_goal_with_no_chain_changes_nothing(project):
    """Clause 3, narrow reading (the owner's, 2026-09-02): "no closed chain"
    means no chain at all. Nothing to include or exclude, so both terms of
    the ratio are untouched."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"])
    _goal(project, "g2", "active")          # bare goal, no nodes under it
    before = metrics.compute(project)

    _goal(project, "g2", "retired")
    after = metrics.compute(project)

    assert after["outcome_coverage"] == before["outcome_coverage"]
    assert after["scoring_mvp_count"] == before["scoring_mvp_count"]
    assert after["scoring_hypothesis_count"] == before["scoring_hypothesis_count"]


def test_retiring_cannot_launder_unconverted_hypotheses_out_of_the_ratio(project):
    """The anti-gaming clause, and the reason this is not a one-constant fix.

    A hypothesis under a retired goal that never reached an mvp STAYS in the
    denominator. Without this, retiring goals in bulk -- which is exactly what
    a goal sweep does -- would raise `outcome_coverage` for free, and nothing
    in the metric could tell that apart from honest retirement.
    """
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"])
    _goal(project, "g2", "active")
    for i in range(3):                      # dead weight: never converted
        _node(project, "hypothesis", f"open{i}", parents=["goal:g2"])
    before = metrics.compute(project)
    assert before["scoring_hypothesis_count"] == 4

    _goal(project, "g2", "retired")
    after = metrics.compute(project)

    assert after["scoring_hypothesis_count"] == 4, "open hypotheses must not leave"
    assert after["outcome_coverage"] == before["outcome_coverage"]
    assert after["retired_open_hypotheses"] == 3
    assert after["retired_goal_nodes"] == 0


def test_legacy_phasing_out_still_reads_as_retired(project):
    """`phasing-out` is the pre-2026-09-02 spelling and stays accepted
    permanently -- a reader that stopped recognising it would silently start
    scoring the retired chains of every project that predates the rename."""
    _goal(project, "g1", "phasing-out")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"])
    m = metrics.compute(project)
    assert (m["scoring_mvp_count"], m["scoring_hypothesis_count"]) == (0, 0)
    assert m["retired_goal_nodes"] == 2


def test_exceeding_max_goals_active_warns_but_does_not_refuse(project, capsys):
    """L5 — rotation the engine enforces. A commitment about focus that
    nothing reads is not a commitment."""
    (project / "agi-tree.config.json").write_text(
        json.dumps({"cc_dispatch": {"max_goals_active": 1}})
    )
    _goal(project, "g1", "active")
    _goal(project, "g2", "active")
    m = metrics.emit(project)
    out = capsys.readouterr()
    assert "METRIC_WARNING goal_rotation=2/1" in out.out
    assert "max_goals_active" in out.err
    assert m["goals_active"] == 2      # emitted, not aborted


def test_within_max_goals_active_is_silent(project, capsys):
    (project / "agi-tree.config.json").write_text(
        json.dumps({"cc_dispatch": {"max_goals_active": 3}})
    )
    _goal(project, "g1", "active")
    metrics.emit(project)
    assert "goal_rotation" not in capsys.readouterr().out


def test_goal_cycle_does_not_hang_attribution(project):
    """Cycle-safety is structural, not incidental — assert it."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "a", parents=["hypothesis:b"])
    _node(project, "hypothesis", "b", parents=["hypothesis:a"])
    m = metrics.compute(project)
    assert m["unattributed_nodes"] == 2


# ------------------------------------------ node lifecycle (goal:g7.10)
#
# `status: deprecated` retires a node **file that is kept, never deleted**.
# Retirement therefore has to be trackable over time as a number, or it is
# indistinguishable from nothing having happened.


def test_deprecated_nodes_are_counted(project):
    _node(project, "build", "old", "status: deprecated")
    _node(project, "build", "older", "status: deprecated")
    _node(project, "build", "live", "status: active")
    m = metrics.compute(project)
    assert m["deprecated_node_count"] == 2
    assert m["active_node_count"] == 1


def test_node_count_does_not_drop_when_a_node_is_deprecated(project):
    """G7's invariant: nothing the loop produces is silently lost. A total
    that shrinks on retirement is exactly the shape of loss it forbids — you
    could not tell a deprecation from a deletion. `active_node_count` is the
    number that is allowed to move."""
    _node(project, "build", "a")
    _node(project, "build", "b")
    before = metrics.compute(project)
    assert (before["node_count"], before["active_node_count"]) == (2, 2)

    _node(project, "build", "b", "status: deprecated")   # retire in place
    after = metrics.compute(project)
    assert after["node_count"] == before["node_count"] == 2
    assert after["deprecated_node_count"] == 1
    assert after["active_node_count"] == 1


def test_a_graph_with_no_deprecations_reads_zero_not_absent(project):
    """0 and "not computed" must not look the same: an alarm you cannot
    distinguish from a missing metric is not an alarm."""
    _node(project, "build", "a")
    m = metrics.compute(project)
    assert m["deprecated_node_count"] == 0
    assert m["active_node_count"] == m["node_count"] == 1


def test_lifecycle_count_is_not_goal_attribution(project):
    """`retired_goal_nodes` counts nodes whose every answering goal is
    retired — attribution, and a node is caught by it without anyone touching
    it. `deprecated_node_count` counts the node's own declared status. Two
    different questions; reusing one for the other makes both unreadable.

    Two fixture changes on 2026-09-02, both to keep this testing the
    distinction rather than goal:g5's new rules. `complete` -> `retired`,
    because `complete` now scores and produces no retired-by-attribution node
    at all. And `hypothesis` -> `experiment`, because an *unconverted*
    hypothesis under a retired goal is deliberately spared and stays in the
    denominator (the anti-gaming clause) -- so it would not be counted here
    either, for a reason that has nothing to do with what this test asks."""
    _goal(project, "g1", "retired")
    _node(project, "experiment", "under-dead-goal", parents=["goal:g1"])
    _node(project, "build", "self-retired", "status: deprecated")
    m = metrics.compute(project)
    assert m["retired_goal_nodes"] == 1        # attribution only
    assert m["deprecated_node_count"] == 1     # declaration only
    assert m["active_node_count"] == m["node_count"] - 1


def test_deprecated_status_tolerates_case_and_whitespace(project):
    _node(project, "build", "a", "status: Deprecated")
    _node(project, "build", "b", 'status: "  deprecated  "')
    assert metrics.compute(project)["deprecated_node_count"] == 2


def test_other_statuses_are_not_deprecation(project):
    for i, st in enumerate(("active", "phasing-out", "complete", "pending",
                            "open", "proved")):
        _node(project, "build", f"n{i}", f"status: {st}")
    m = metrics.compute(project)
    assert m["deprecated_node_count"] == 0
    assert m["active_node_count"] == m["node_count"]


def test_lifecycle_counts_reach_the_metric_lines(project):
    _node(project, "build", "a", "status: deprecated")
    buf = io.StringIO()
    metrics.emit(project, out=buf)
    text = buf.getvalue()
    assert "METRIC deprecated_node_count=1" in text
    assert "METRIC active_node_count=0" in text


# ------------------------------- goal:g3 falsifier: the removal guard (L1.08)
#
# goal:g5 taught the metric that retiring a GOAL cannot raise the score.
# Nothing said the same about deprecating a NODE, and deprecation is the other
# removal: it takes nodes out of the graph's live half one at a time instead of
# a subtree at a time. Removal must obey the same law as addition -- it cannot
# move the primary on its own.
#
# The hole was measured, not imagined. This corpus carries 61 `origin:
# build-site` hypotheses and zero build-site mvps, 52 of them never reaching a
# verdict. The cleanup that deprecates them would have moved `outcome_coverage`
# 0.271 -> 0.470 for free. Fixtures, not corpus counts, because another parent
# is minting nodes concurrently and any assertion on 940 or 0.271 would flake.


def test_deprecating_unconverted_hypotheses_cannot_raise_the_primary(project):
    """The falsifier, and the whole reason this guard exists.

    A deprecated hypothesis that never reached an mvp STAYS in the
    denominator. Without this, the cheapest way to raise the primary is to
    deprecate the evidence against it -- and nothing in the metric could tell
    that apart from honest cleanup.
    """
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"])
    _goal(project, "g2", "active")
    for i in range(3):                      # dead weight: never converted
        _node(project, "hypothesis", f"open{i}", parents=["goal:g2"])
    before = metrics.compute(project)
    assert (before["scoring_mvp_count"], before["scoring_hypothesis_count"]) == (1, 4)

    for i in range(3):                      # retire in place, same ids
        _node(project, "hypothesis", f"open{i}", "status: deprecated",
              parents=["goal:g2"])
    after = metrics.compute(project)

    assert after["scoring_hypothesis_count"] == 4, "open hypotheses must not leave"
    assert after["outcome_coverage"] == before["outcome_coverage"]
    assert after["deprecated_open_hypotheses"] == 3
    assert after["deprecated_excluded_nodes"] == 0
    # ...and the deprecation is real, not a no-op the guard is hiding
    assert after["deprecated_node_count"] == 3
    assert after["node_count"] == before["node_count"]


def test_deprecating_a_closed_chain_removes_both_terms(project):
    """The legitimate half. A chain that actually reached an mvp may leave
    scoring, exactly as goal retirement lets one leave -- numerator and
    denominator together, never one without the other."""
    _goal(project, "g1", "active")
    for tag in ("keep", "drop"):
        _node(project, "hypothesis", tag, parents=["goal:g1"])
        _node(project, "mvp", f"{tag}-m", parents=[f"hypothesis:{tag}"])
    assert metrics.compute(project)["outcome_coverage"] == 1.0

    _node(project, "hypothesis", "drop", "status: deprecated", parents=["goal:g1"])
    _node(project, "mvp", "drop-m", "status: deprecated", parents=["hypothesis:drop"])
    m = metrics.compute(project)

    assert (m["scoring_mvp_count"], m["scoring_hypothesis_count"]) == (1, 1)
    assert m["deprecated_excluded_nodes"] == 2
    assert m["deprecated_open_hypotheses"] == 0
    assert m["mvp_count"] == 2               # descriptive total untouched


def test_a_hypothesis_whose_mvp_still_scores_is_held(project):
    """The pairing clause, and the case goal retirement never had to face.

    Retirement takes a whole subtree, so a chain's mvp and hypothesis always
    left together. Deprecation couples nothing: deprecate the hypothesis,
    leave the mvp live, and the denominator drops while the numerator keeps
    the credit. Same free lift by a shorter route, so "closed" is measured
    against the mvps that are leaving too.
    """
    _goal(project, "g1", "active")
    for tag in ("a", "b"):
        _node(project, "hypothesis", tag, parents=["goal:g1"])
        _node(project, "mvp", f"{tag}-m", parents=[f"hypothesis:{tag}"])
    before = metrics.compute(project)

    _node(project, "hypothesis", "b", "status: deprecated", parents=["goal:g1"])
    after = metrics.compute(project)          # mvp:b-m deliberately left live

    assert after["scoring_mvp_count"] == 2
    assert after["scoring_hypothesis_count"] == 2, "its mvp still scores for it"
    assert after["outcome_coverage"] == before["outcome_coverage"]
    assert after["deprecated_open_hypotheses"] == 1


def test_deprecating_an_mvp_lowers_the_score_and_that_is_allowed(project):
    """Score-neutral at worst, never score-positive. Discarding a real mvp is
    the one direction removal is free to move the primary in."""
    _goal(project, "g1", "active")
    for tag in ("a", "b"):
        _node(project, "hypothesis", tag, parents=["goal:g1"])
        _node(project, "mvp", f"{tag}-m", parents=[f"hypothesis:{tag}"])
    assert metrics.compute(project)["outcome_coverage"] == 1.0

    _node(project, "mvp", "b-m", "status: deprecated", parents=["hypothesis:b"])
    m = metrics.compute(project)

    assert (m["scoring_mvp_count"], m["scoring_hypothesis_count"]) == (1, 2)
    assert m["outcome_coverage"] == 0.5
    assert m["deprecated_excluded_nodes"] == 1


def test_deprecation_score_delta_reports_the_refused_lift(project):
    """The guard is auditable, not implicit: the delta is exactly what
    deprecation would have collected had the guard not held."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h1", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h1"])
    _node(project, "hypothesis", "h2", parents=["goal:g1"])
    for i in range(2):
        _node(project, "hypothesis", f"d{i}", "status: deprecated",
              parents=["goal:g1"])
    m = metrics.compute(project)

    assert (m["scoring_mvp_count"], m["scoring_hypothesis_count"]) == (1, 4)
    assert m["deprecated_open_hypotheses"] == 2
    # held:  1/4 = 0.25   unguarded: 1/(4-2) = 0.5   delta: -0.25
    assert m["deprecation_score_delta"] == -0.25


def test_deprecation_score_delta_is_zero_when_nothing_is_held(project):
    """0 and "not computed" must not look the same, and a graph with no
    deprecated hypotheses is the ordinary case -- it reads 0.0, every run."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"])
    _node(project, "build", "retired-file", "status: deprecated")
    m = metrics.compute(project)
    assert m["deprecation_score_delta"] == 0.0
    assert m["deprecated_open_hypotheses"] == 0
    assert m["deprecated_excluded_nodes"] == 1


def test_deprecation_score_delta_is_never_positive(project):
    """The law, asserted over every shape the guard can meet at once: a
    closed chain, an open hypothesis, a live chain, a deprecated mvp and a
    deprecated non-scoring node. `<= 0` is arithmetic here -- the two ratios
    share a numerator and the unguarded denominator is the smaller one -- so
    a positive reading means the definition drifted, not that a corpus got
    unlucky."""
    _goal(project, "g1", "active")
    _goal(project, "g2", "retired")
    _node(project, "hypothesis", "live", parents=["goal:g1"])
    _node(project, "mvp", "live-m", parents=["hypothesis:live"])
    _node(project, "hypothesis", "gone", "status: deprecated", parents=["goal:g1"])
    _node(project, "mvp", "gone-m", "status: deprecated", parents=["hypothesis:gone"])
    _node(project, "hypothesis", "open", "status: deprecated", parents=["goal:g1"])
    _node(project, "hypothesis", "retired-open", parents=["goal:g2"])
    _node(project, "experiment", "e", "status: deprecated", parents=["goal:g1"])
    m = metrics.compute(project)
    assert m["deprecation_score_delta"] <= 0.0
    # the four leaving-buckets partition the leaving set, so they can be summed
    assert m["deprecated_open_hypotheses"] == 1
    assert m["deprecated_excluded_nodes"] == 3    # gone, gone-m, e
    assert m["retired_open_hypotheses"] == 1
    assert m["retired_goal_nodes"] == 0


def test_goal_retirement_takes_priority_over_deprecation_in_the_buckets(project):
    """A node can be both. It is reported once, under the older and coarser
    reason, so the buckets stay a partition -- and so the delta counts only
    what THIS guard is holding: a hypothesis goal:g5 already holds is not a
    hypothesis deprecation could have laundered."""
    _goal(project, "g1", "retired")
    _node(project, "hypothesis", "both", "status: deprecated", parents=["goal:g1"])
    m = metrics.compute(project)
    assert m["retired_open_hypotheses"] == 1
    assert m["deprecated_open_hypotheses"] == 0
    assert m["deprecation_score_delta"] == 0.0
    assert m["scoring_hypothesis_count"] == 1


def test_the_build_site_cleanup_shape_moves_the_primary_by_zero(project):
    """L1.09 in miniature: many generated hypotheses, no mvps of their own,
    deprecated wholesale. This is the shape the guard was written for -- the
    real set is 61 hypotheses and 0 mvps -- and the assertion is that the
    cleanup is worth exactly 0.000 of score."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "real", parents=["goal:g1"])
    _node(project, "mvp", "real-m", parents=["hypothesis:real"])
    _goal(project, "g2", "active")
    for i in range(5):
        _node(project, "hypothesis", f"gen{i}", "origin: build-site",
              parents=["goal:g2"])
    before = metrics.compute(project)
    assert before["outcome_coverage"] == 0.167          # 1/6

    for i in range(5):
        _node(project, "hypothesis", f"gen{i}",
              "origin: build-site\nstatus: deprecated", parents=["goal:g2"])
    after = metrics.compute(project)

    assert after["outcome_coverage"] == before["outcome_coverage"]
    assert after["deprecated_open_hypotheses"] == 5
    # and the size of what was refused is on the record: 1/6 -> 1/1
    assert after["deprecation_score_delta"] == -0.833


def test_deprecation_guard_counts_reach_the_metric_lines(project):
    """A guard nobody can read from the METRIC lines is a guard nobody
    audits."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", "status: deprecated", parents=["goal:g1"])
    buf = io.StringIO()
    metrics.emit(project, out=buf)
    text = buf.getvalue()
    assert "METRIC deprecated_open_hypotheses=1" in text
    assert "METRIC deprecated_excluded_nodes=0" in text


# --------------------------------------------------------- backward mvp rule
#
# `hypothesis:an-mvp-that-points-backward-is-score-neutral` (goal:g3, L1.08).
# `[mvp].md` says an mvp points FORWARD -- it names what a future build owes,
# never what one already delivered. Nine mvps minted 2026-09-03 were audited
# against that rule; two described a change already made and verified in the
# live tree rather than one still to be built, and would have raised
# `outcome_coverage`'s numerator for zero forward-pointing content -- the
# exact motion goal:g3 forbids. These tests fix the shape in miniature.

_BACKWARD_BODY = (
    "## Agent Notes\n"
    "Verified in-tree: the change is live at module.py:42. "
    "Ran the suite myself: 1382/1382 pass."
)


def test_backward_mvp_is_excluded_from_scoring(project):
    """The falsifier this rule exists for: an mvp whose body verifies an
    already-shipped change, with no source_files/payload_ref/build child,
    must not raise `scoring_mvp_count` -- or the numerator moves for a
    closure that was never a forward design."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"], body=_BACKWARD_BODY)
    m = metrics.compute(project)

    assert m["scoring_mvp_count"] == 0
    assert m["backward_mvp_count"] == 1
    assert m["mvp_count"] == 1, "descriptive total is untouched -- nothing was deleted"
    assert m["outcome_coverage"] == 0.0


def test_backward_mvp_does_not_spare_its_own_hypothesis(project):
    """A backward mvp is not 'leaving' -- it is neither deprecated nor under a
    retired goal, so it cannot invoke clause 3's sparing. Its hypothesis stays
    fully counted in the denominator, exactly as an unconverted hypothesis
    would: excluded credit, not excused work."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"], body=_BACKWARD_BODY)
    m = metrics.compute(project)

    assert m["scoring_hypothesis_count"] == 1
    assert m["outcome_coverage"] == 0.0


def test_a_forward_mvp_with_source_files_is_never_flagged(project):
    """Condition 1 of the rule (no forward evidence) guards the false
    positive: an mvp can legitimately quote a sibling's test run while also
    genuinely pointing forward, if it names its own source_files. The
    exclusion requires BOTH conditions, not just the language match."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", "source_files:\n  - bin/real_file.py",
          parents=["hypothesis:h"], body=_BACKWARD_BODY)
    m = metrics.compute(project)

    assert m["scoring_mvp_count"] == 1
    assert m["backward_mvp_count"] == 0


def test_a_forward_mvp_with_a_build_child_is_never_flagged(project):
    """The other half of condition 1: a real `build` node naming this mvp as
    its parent is the mechanical trail `level3.py` leaves when a build was
    actually minted FOR this mvp -- the strongest forward evidence there is,
    and it must win over language matching."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"], body=_BACKWARD_BODY)
    _node(project, "build", "b", parents=["mvp:m"])
    m = metrics.compute(project)

    assert m["scoring_mvp_count"] == 1
    assert m["backward_mvp_count"] == 0


def test_a_design_mvp_that_merely_mentions_something_existing_is_not_flagged(project):
    """Condition 2 (the language match) is narrow on purpose. An ordinary
    forward mvp routinely says something ELSE already exists -- a directory,
    a field, a sibling module -- without that being a claim about ITS OWN
    deliverable. `'already exists'` alone must not trip the rule; only a
    verification-of-shipped-code phrase does."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(
        project, "mvp", "m", parents=["hypothesis:h"],
        body=(
            "## MVP\n"
            "The `.agi/sessions/` tree already exists and is gitignored, so "
            "the new resolver (bin/resolve-provenance.py, not yet written) "
            "needs no new store."
        ),
    )
    m = metrics.compute(project)

    assert m["scoring_mvp_count"] == 1
    assert m["backward_mvp_count"] == 0


def test_backward_mvp_count_defaults_to_zero(project):
    """0 and 'not computed' must not look the same -- an ordinary graph with
    no backward mvps reads 0 every run, not an absent key."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"])
    m = metrics.compute(project)
    assert m["backward_mvp_count"] == 0


def test_backward_mvp_count_reaches_the_metric_lines(project):
    """A rule nobody can read from the METRIC lines is a rule nobody audits."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"], body=_BACKWARD_BODY)
    buf = io.StringIO()
    metrics.emit(project, out=buf)
    text = buf.getvalue()
    assert "METRIC backward_mvp_count=1" in text
    assert "METRIC scoring_mvp_count=0" in text
    assert "METRIC deprecation_score_delta=0.0" in text
