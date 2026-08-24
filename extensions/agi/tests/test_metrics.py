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


def _node(root, ntype, slug, fm_extra="", parents=()):
    d = root / "nodes" / ntype.replace("-", "_")
    d.mkdir(parents=True, exist_ok=True)
    lines = ["---", f'id: "{ntype}:{slug}"', f"type: {ntype}"]
    if parents:
        lines.append("parents:")
        lines += [f"  - {p}" for p in parents]
    if fm_extra:
        lines.append(fm_extra.rstrip())
    lines += ["---", "", "body", ""]
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
    assert s["unevidenced_decisive_verdicts"] == 1
    assert s["decisive_evidence_fraction"] == 0.5


def test_empty_corpus_is_zero_not_a_crash(project):
    s = metrics.evidence_stats(project / "nodes")
    assert s["evidence_fraction"] == 0.0
    assert s["unevidenced_decisive_verdicts"] == 0


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
    """goal:g5 — `complete`/`phasing-out` chains keep their nodes and lose
    their score. Retiring a goal must not look like deleting its work."""
    _goal(project, "g1", "active")
    _goal(project, "g2", "complete")
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
    _goal(project, "g2", "complete")
    _node(project, "hypothesis", "shared", parents=["goal:g1", "goal:g2"])
    m = metrics.compute(project)
    assert m["scoring_hypothesis_count"] == 1
    assert m["retired_goal_nodes"] == 0


def test_goal_status_counts_are_emitted(project):
    _goal(project, "g1", "active")
    _goal(project, "g2", "horizon")
    _goal(project, "g3", "complete")
    _goal(project, "g4", "phasing-out")
    m = metrics.compute(project)
    assert (m["goals_active"], m["goals_horizon"], m["goals_retired"]) == (1, 1, 2)
    assert m["goal_count"] == 4


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
