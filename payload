"""Tests for bin/dashboard.py — the human-facing view (G9/G9.1).

Two invariants matter more than any single panel's wording:

1. The dashboard is a READER, never a WRITER. It must be safe to run at any
   moment, including mid-iteration. `test_running_the_dashboard_writes_nothing`
   proves this directly against a corpus fixture: no file's mtime changes,
   no new file appears — including `.chain_cache.pkl`, which
   `chain_engine.chains.find_chains()` writes when given a `graph_dir`, so the
   dashboard must call it with `graph_dir=None`.

2. It renders the graph's damage, not a clean picture of it: the evidence
   contamination check must be general (any `evidence_runs` entry that does
   not resolve to a real node in the graph, not just the literal string
   "synthetic"), and dangling refs / duplicate ids / stub goals must surface
   by name.
"""

import importlib.util
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
DASHBOARD = BIN / "dashboard.py"


def _load(name, filename=None):
    path = BIN / (filename or f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


dashboard = _load("dashboard")


# --------------------------------------------------------------------------
# fixtures
# --------------------------------------------------------------------------

def _node(root, ntype, slug, fm_extra="", parents=()):
    d = root / "nodes" / ntype
    d.mkdir(parents=True, exist_ok=True)
    lines = ["---", f'id: "{ntype}:{slug}"', f"type: {ntype}",
             f'title: "{ntype} {slug}"']
    if parents:
        lines.append("parents:")
        lines += [f"  - {p}" for p in parents]
    if fm_extra:
        lines.append(fm_extra.rstrip())
    lines += ["---", "", "body text", ""]
    (d / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")
    return d / f"{slug}.md"


@pytest.fixture()
def project(tmp_path):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "nodes").mkdir()
    return tmp_path


def _run(project, *args, timeout=30):
    return subprocess.run(
        [sys.executable, str(DASHBOARD), "--project", str(project), *args],
        capture_output=True, text=True, timeout=timeout,
    )


# --------------------------------------------------------------------------
# 1. the read-only invariant
# --------------------------------------------------------------------------

def _snapshot(root: Path) -> dict[str, float]:
    return {
        str(p): p.stat().st_mtime
        for p in root.rglob("*") if p.is_file()
    }


def test_running_the_dashboard_writes_nothing(project):
    """Full-corpus proof of invariant 1: run the real CLI, diff the tree."""
    goal = _node(project, "goal", "g1",
                "status: active\ngoal_kind: long-term\nseeds:\n  - idea:i1")
    _node(project, "idea", "i1", parents=["goal:g1"])
    hyp = _node(project, "hypothesis", "h1", parents=["idea:i1"])
    exp = _node(project, "experiment", "e1", parents=["hypothesis:h1"])
    _node(project, "verdict", "v1",
         'verdict: proved\nevidence_runs:\n  - "experiment:e1"',
         parents=["experiment:e1"])
    # a dangling ref and a bogus evidence entry, on purpose — the dashboard
    # must be able to run over damaged input without writing anything either.
    _node(project, "hypothesis", "orphan", parents=["idea:does-not-exist"])
    subprocess.run(["git", "-C", str(project), "init", "-q"], check=True)

    before_files = {str(p) for p in project.rglob("*") if p.is_file()}
    before_mtimes = _snapshot(project)

    result = _run(project, "--no-color")
    assert result.returncode == 0, result.stderr

    after_files = {str(p) for p in project.rglob("*") if p.is_file()}
    after_mtimes = _snapshot(project)

    assert after_files == before_files, \
        f"dashboard created files: {after_files - before_files}"
    changed = {p for p in before_mtimes if before_mtimes[p] != after_mtimes.get(p)}
    assert not changed, f"dashboard modified files: {changed}"
    # Named regression: this is the specific write chain_engine's find_chains
    # performs when given a graph_dir, and it must never fire here.
    assert not (project / "nodes" / ".chain_cache.pkl").exists()
    assert not (project / "context").exists()


def test_chain_health_never_passes_a_graph_dir(monkeypatch, project):
    """Unit-level guard for the same invariant: find_chains must be called
    with graph_dir=None so its pickle warm-cache never writes under nodes/.
    """
    calls = []

    class _FakeChainsModule:
        @staticmethod
        def find_chains(g, graph_dir=None, **kw):
            calls.append(graph_dir)
            return [["idea:i1"]]

    import types
    fake_pkg = types.ModuleType("chain_engine")
    fake_pkg.chains = _FakeChainsModule
    monkeypatch.setitem(sys.modules, "chain_engine", fake_pkg)
    monkeypatch.setitem(sys.modules, "chain_engine.chains", _FakeChainsModule)

    g = dashboard.metrics._load_graph(project)
    dashboard.chain_health(g, project / "nodes")
    assert calls == [None]


# --------------------------------------------------------------------------
# 2. evidence contamination — general pattern, not a "synthetic" special case
# --------------------------------------------------------------------------

def test_evidence_resolution_is_general_not_a_synthetic_special_case(project):
    """The corpus defect (agi-tree goal:g3.1) is `evidence_runs: [synthetic]`
    counting as backed. The fix must reject ANY unresolved string, proven
    here with a string that is not "synthetic" at all.
    """
    _node(project, "experiment", "real-exp")
    _node(project, "verdict", "backed",
         'verdict: proved\nevidence_runs:\n  - "experiment:real-exp"')
    _node(project, "verdict", "fake",
         'verdict: proved\nevidence_runs:\n  - "totally-made-up-placeholder"')
    _node(project, "verdict", "also-fake",
         'verdict: disproved\nevidence_runs:\n  - synthetic')

    g = dashboard.metrics._load_graph(project)
    stats = dashboard.resolved_evidence_stats(project / "nodes", g)

    assert stats["asserting"] == 3
    assert stats["resolved_backed"] == 1
    assert stats["sentinel_only"] == 2
    joined = " ".join(stats["sentinel_examples"])
    assert "totally-made-up-placeholder" in joined or "synthetic" in joined


def test_bare_integer_evidence_runs_fails_closed(project):
    """No list of ids to check means nothing is verified — the general rule
    fails closed rather than trusting an unverifiable count.

    **The two rules now agree, and that is goal:g7.3 landing.** This test used
    to assert the opposite: the dashboard resolved 0 while `metrics.py` still
    counted the bare `3` as backed, and the gap between them was described here
    as "the contamination the dashboard exists to name". `metrics.py` shares
    `normalize_evidence_runs` with the gate, so closing the hole in one closed
    it in both. The dashboard stops being the only honest counter.
    """
    _node(project, "verdict", "v1", "verdict: proved\nevidence_runs: 3")
    g = dashboard.metrics._load_graph(project)
    stats = dashboard.resolved_evidence_stats(project / "nodes", g)
    assert stats["resolved_backed"] == 0
    raw = dashboard.metrics.evidence_stats(project / "nodes")
    assert raw["verdicts_evidence_backed"] == 0, (
        "metrics.py and the dashboard must agree now that goal:g7.3 removed "
        "the bare-int path they used to disagree about")


def test_pending_excluded_but_inconclusive_counts_as_asserting(project):
    """Matches metrics.py's own rule exactly (H4): `pending` is the only
    verdict excluded from the denominator; `inconclusive_lean_*` still
    asserts something and is counted, it just isn't decisive."""
    _node(project, "verdict", "p1", "verdict: pending")
    _node(project, "verdict", "i1", "verdict: inconclusive_lean_proved:60")
    g = dashboard.metrics._load_graph(project)
    stats = dashboard.resolved_evidence_stats(project / "nodes", g)
    assert stats["asserting"] == 1


# --------------------------------------------------------------------------
# 3. health warnings
# --------------------------------------------------------------------------

def test_dangling_parent_reference_detected(project):
    _node(project, "hypothesis", "h1", parents=["idea:ghost"])
    g = dashboard.metrics._load_graph(project)
    da = dashboard.dangling_and_orphans(g)
    assert ("hypothesis:h1", "idea:ghost") in da["dangling"]


def test_no_dangling_when_parent_resolves(project):
    _node(project, "idea", "i1")
    _node(project, "hypothesis", "h1", parents=["idea:i1"])
    g = dashboard.metrics._load_graph(project)
    da = dashboard.dangling_and_orphans(g)
    assert da["dangling"] == []


def test_duplicate_ids_on_disk_detected(project):
    d = project / "nodes" / "idea"
    d.mkdir(parents=True)
    for slug in ("a-first", "b-second"):
        (d / f"{slug}.md").write_text(
            '---\nid: "idea:dup"\ntype: idea\n---\nbody\n', encoding="utf-8")
    dupes = dashboard.find_duplicate_ids(project / "nodes")
    assert len(dupes) == 1
    nid, kept, shadowed = dupes[0]
    assert nid == "idea:dup"
    assert kept.name == "a-first.md"     # sorted walk keeps the first
    assert shadowed.name == "b-second.md"


def test_no_duplicates_in_a_clean_corpus(project):
    _node(project, "idea", "i1")
    _node(project, "idea", "i2")
    assert dashboard.find_duplicate_ids(project / "nodes") == []


# --------------------------------------------------------------------------
# 4. goals: real vs stub
# --------------------------------------------------------------------------

def test_goal_with_no_descendants_is_a_stub(project):
    _node(project, "goal", "g1", "status: active\ngoal_kind: long-term\nseeds: []")
    g = dashboard.metrics._load_graph(project)
    fm_by_id = {fm["id"]: (nf, fm) for nf, fm in
               dashboard.metrics._iter_frontmatter(project / "nodes")}
    goals = dashboard.collect_goals(g, fm_by_id)
    assert len(goals) == 1
    assert goals[0]["is_stub"] is True
    assert goals[0]["built_count"] == 0


def test_goal_with_descendants_is_real_and_reports_furthest_stage(project):
    _node(project, "goal", "g1",
         "status: active\ngoal_kind: long-term\nseeds:\n  - idea:i1")
    _node(project, "idea", "i1", parents=["goal:g1"])
    _node(project, "hypothesis", "h1", parents=["idea:i1"])
    g = dashboard.metrics._load_graph(project)
    fm_by_id = {fm["id"]: (nf, fm) for nf, fm in
               dashboard.metrics._iter_frontmatter(project / "nodes")}
    goals = dashboard.collect_goals(g, fm_by_id)
    row = goals[0]
    assert row["is_stub"] is False
    assert row["built_count"] == 2
    assert row["furthest_stage"] == "hypothesis"


def test_seed_that_does_not_resolve_is_counted_separately(project):
    _node(project, "goal", "g1",
         "status: active\ngoal_kind: long-term\nseeds:\n  - idea:ghost")
    g = dashboard.metrics._load_graph(project)
    fm_by_id = {fm["id"]: (nf, fm) for nf, fm in
               dashboard.metrics._iter_frontmatter(project / "nodes")}
    goals = dashboard.collect_goals(g, fm_by_id)
    row = goals[0]
    assert row["seeds_declared"] == 1
    assert row["seeds_resolved"] == 0


# --------------------------------------------------------------------------
# 5. metrics section reuses bin/metrics.py rather than recomputing
# --------------------------------------------------------------------------

def test_metrics_section_matches_metrics_py_directly(project):
    _node(project, "hypothesis", "h1")
    _node(project, "mvp", "m1", parents=["hypothesis:h1"])
    expected = dashboard.metrics.compute(project)

    result = _run(project, "--no-color", "--section", "metrics")
    assert result.returncode == 0, result.stderr
    assert f"Outcome Coverage:  {expected['outcome_coverage']}" in result.stdout
    assert f"Node count:        {expected['node_count']}" in result.stdout


# --------------------------------------------------------------------------
# 6. CLI surface: --section, --no-color, --project, --watch
# --------------------------------------------------------------------------

def test_section_flag_prints_only_that_section(project):
    _node(project, "goal", "g1", "status: active\ngoal_kind: long-term")
    result = _run(project, "--no-color", "--section", "health")
    assert result.returncode == 0, result.stderr
    assert "HEALTH WARNINGS" in result.stdout
    assert "GOALS —" not in result.stdout
    assert "METRICS —" not in result.stdout
    assert "RECENT ACTIVITY" not in result.stdout


def test_invalid_section_name_is_rejected(project):
    result = _run(project, "--section", "nonsense")
    assert result.returncode != 0
    assert "invalid choice" in result.stderr


def test_no_color_flag_strips_ansi(project):
    _node(project, "goal", "g1", "status: active\ngoal_kind: long-term")
    result = _run(project, "--no-color")
    assert result.returncode == 0
    assert "\x1b[" not in result.stdout


def test_piped_output_has_no_ansi_even_without_the_flag(project):
    """subprocess.run's pipe is never a tty, so colour must auto-disable."""
    _node(project, "goal", "g1", "status: active\ngoal_kind: long-term")
    result = _run(project)  # no --no-color
    assert result.returncode == 0
    assert "\x1b[" not in result.stdout


def test_missing_project_config_errors_cleanly(tmp_path):
    empty = tmp_path / "not-a-project"
    empty.mkdir()
    result = _run(empty)
    assert result.returncode != 0
    assert "no agi-tree.config.json" in result.stderr


def test_watch_exits_cleanly_on_sigint(project):
    """Must exit without a traceback and with the ordinary success code."""
    _node(project, "goal", "g1", "status: active\ngoal_kind: long-term")
    proc = subprocess.Popen(
        [sys.executable, str(DASHBOARD), "--project", str(project),
         "--no-color", "--watch", "1"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    time.sleep(1.5)
    proc.send_signal(signal.SIGINT)
    try:
        _out, err = proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise
    assert proc.returncode == 0
    assert "Traceback" not in err


def test_watch_default_interval_is_ten_seconds(project):
    args = dashboard.build_parser().parse_args(
        ["--project", str(project), "--watch"])
    assert args.watch == 10


# --------------------------------------------------------------------------
# 7. degrades gracefully rather than crashing
# --------------------------------------------------------------------------

def test_empty_corpus_does_not_crash(project):
    result = _run(project, "--no-color")
    assert result.returncode == 0, result.stderr
    assert "0 goals are declared" in result.stdout


def test_narrow_terminal_does_not_crash(project):
    _node(project, "goal", "g1",
         "status: active\ngoal_kind: long-term\nseeds:\n  - idea:i1")
    _node(project, "idea", "i1", parents=["goal:g1"])
    env = dict(os.environ)
    env["COLUMNS"] = "20"
    result = subprocess.run(
        [sys.executable, str(DASHBOARD), "--project", str(project), "--no-color"],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert result.returncode == 0, result.stderr


def test_project_without_git_falls_back_to_mtime(project):
    _node(project, "idea", "i1")
    result = _run(project, "--no-color", "--section", "activity")
    assert result.returncode == 0, result.stderr
    assert "mtime" in result.stdout
