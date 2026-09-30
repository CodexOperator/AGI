"""test_push_gap.py -- the stranded-push alarm (goal:s20), restored.

This section lived in test_publish_alarm.py (section 6, 01cd96628^ lines
956-1331) and left with it when publish-engine.sh was retired
(goal:g7.16.1.4.1.1); it was the ONLY coverage of LIVE code: metrics.py's
push_gap_stats / UNPUSHED_WARN_AT / unpushed_commits, the no-network
guarantee, and the SessionStart hook's stranded-push banner. Restored verbatim
on sanctuary-master's residue 116 (mur wf_35fe675a-d5b); only the helpers it
uses came along.
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1]
BIN = PLUGIN / "bin"
HOOK_SH = PLUGIN / "hooks" / "cc-session-start.sh"

spec = importlib.util.spec_from_file_location("metrics", BIN / "metrics.py")
metrics = importlib.util.module_from_spec(spec)
sys.modules["metrics"] = metrics
spec.loader.exec_module(metrics)


@pytest.fixture()
def project(tmp_path):
    """A minimal project: the config marker is what makes a dir a project."""
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "nodes").mkdir()
    (tmp_path / "context").mkdir()
    return tmp_path


def _git(root: Path, *args):
    subprocess.run(["git", *args], cwd=root, check=True,
                   capture_output=True, text=True)


def _run_hook(cwd: Path):
    """Run the hook with a scrubbed environment, as CC would."""
    env = dict(os.environ)
    env.pop("AGI_TREE_PROJECT_ROOT", None)
    env.pop("AUTORESEARCH_TREE_PROJECT_ROOT", None)
    return subprocess.run(["bash", str(HOOK_SH)], cwd=cwd,
                          capture_output=True, text=True, env=env)


def _init_repo(root: Path):
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")



# ------------------------- 6. the stranded push (goal:s20)
#
# Sections 1-5 all end at the local commit. This one starts there. Every repo
# below is a throwaway built inside `tmp_path`, and every push is between two
# of them — nothing here has, or could reach, a real remote.


def _repo_with_upstream(root: Path) -> Path:
    """A repo with a genuine `@{upstream}`, and the bare repo it tracks.

    Built by pushing to a local bare repo rather than by writing config,
    because the whole measurement is `refs/remotes/origin/*` and only a real
    push creates one. `-u` in the same step is what sets the upstream.
    """
    origin = root.parent / (root.name + "-origin.git")
    subprocess.run(["git", "init", "-q", "--bare", str(origin)],
                   check=True, capture_output=True, text=True)
    root.mkdir(parents=True, exist_ok=True)
    _init_repo(root)
    (root / "f.txt").write_text("0\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "base")
    _git(root, "remote", "add", "origin", str(origin))
    _git(root, "push", "-q", "-u", "origin", "HEAD")
    return origin


def _commits(root: Path, n: int):
    """`n` real commits on the current branch. The content has to differ each
    time or `git commit` finds nothing to do and the count silently comes out
    short — which is a way for one of these tests to pass while measuring
    nothing."""
    for i in range(n):
        (root / "f.txt").write_text(f"work {i}\n")
        _git(root, "commit", "-qam", f"work {i}")


# ------------------------------------------- the number itself


def test_unpushed_commits_counts_what_the_remote_does_not_have(tmp_path):
    """The reading that would have caught the outage. 25 was the real number;
    any N will do, so long as it is N and not a boolean 'behind'."""
    repo = tmp_path / "work"
    _repo_with_upstream(repo)
    _commits(repo, 25)

    assert metrics.unpushed_commits(repo) == (25, "")


def test_pushing_takes_the_number_back_to_zero(tmp_path):
    """`0` is the one reassuring value this metric has, and it must be earned
    by an actual push — not by any of the ways of failing to measure."""
    repo = tmp_path / "work"
    _repo_with_upstream(repo)
    _commits(repo, 3)
    assert metrics.unpushed_commits(repo)[0] == 3

    _git(repo, "push", "-q", "origin", "HEAD")

    assert metrics.unpushed_commits(repo) == (0, "")


# --------------------------------- and every way of not being able to measure


def test_no_upstream_is_not_zero(tmp_path):
    """A fresh fork with no remote configured. `rev-list @{upstream}..HEAD`
    fails outright here, and if that quietly became `0` the alarm would report
    perfect health precisely where it is blind."""
    repo = tmp_path / "work"
    repo.mkdir()
    _init_repo(repo)
    (repo / "f.txt").write_text("0\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")

    assert metrics.unpushed_commits(repo) == (metrics.UNKNOWN_GAP, "no-upstream")


def test_detached_head_is_not_zero(tmp_path):
    """`@{upstream}` is a property of a branch. A detached HEAD has none, so
    the question has no answer — which is a different fact from the answer 0."""
    repo = tmp_path / "work"
    _repo_with_upstream(repo)
    _commits(repo, 2)
    _git(repo, "checkout", "-q", "--detach")

    assert metrics.unpushed_commits(repo) == (metrics.UNKNOWN_GAP, "detached-head")


def test_a_path_that_is_not_a_git_repo_is_not_zero(tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    assert metrics.unpushed_commits(plain) == (metrics.UNKNOWN_GAP, "not-a-repo")


def test_a_missing_engine_clone_is_not_zero_and_does_not_crash(tmp_path):
    """G8 forkability: a project that has not cloned the engine yet is not
    failing at anything, and must neither raise nor read as healthy."""
    assert metrics.unpushed_commits(tmp_path / "nope") == \
        (metrics.UNKNOWN_GAP, "missing")


def test_an_engine_dir_inside_the_graph_repo_never_answers_for_the_graph(tmp_path):
    """The wrong number that would read as a measurement. If `<project>/agi` is
    an ordinary directory rather than a clone, `git -C` answers for the
    enclosing repo — so the engine's gap would be reported as a copy of the
    graph's, and a stale engine would be invisible behind a healthy graph."""
    graph = tmp_path / "graph"
    _repo_with_upstream(graph)
    _commits(graph, 7)
    (graph / "agi").mkdir()

    assert metrics.unpushed_commits(graph) == (7, "")
    assert metrics.unpushed_commits(graph / "agi") == \
        (metrics.UNKNOWN_GAP, "not-a-repo")


def test_a_symlinked_engine_clone_still_measures(tmp_path):
    """The counterpart to the test above: `<project>/agi` is a symlink in at
    least one real project, and `--show-toplevel` reports the resolved path.
    Comparing those as strings would refuse every real engine."""
    engine = tmp_path / "engine"
    _repo_with_upstream(engine)
    _commits(engine, 4)
    graph = tmp_path / "graph"
    graph.mkdir()
    (graph / "agi").symlink_to(engine)

    assert metrics.unpushed_commits(graph / "agi") == (4, "")


def test_the_unknown_sentinel_cannot_be_mistaken_for_a_measurement(tmp_path):
    """Not `0` — that is the value that means 'nothing is stranded'. And below
    every possible true reading, since a commit gap is a count."""
    assert metrics.UNKNOWN_GAP != 0
    assert metrics.UNKNOWN_GAP < 0


# ------------------------------------------------- no network, ever


def test_measuring_the_gap_makes_no_network_call(tmp_path, monkeypatch):
    """`metrics.py` runs on every `driver.sh --smoke`, and `--smoke` is meant
    to be a cheap dry pass. A `git fetch` here would freshen the number and put
    network I/O in the loop's cheapest path."""
    repo = tmp_path / "work"
    _repo_with_upstream(repo)
    _commits(repo, 2)

    seen = []
    real = metrics.subprocess.run

    def spy(cmd, *a, **kw):
        seen.append(list(cmd))
        return real(cmd, *a, **kw)

    monkeypatch.setattr(metrics.subprocess, "run", spy)
    assert metrics.unpushed_commits(repo) == (2, "")

    assert seen, "expected the measurement to shell out to git at all"
    for cmd in seen:
        assert set(cmd) & {"fetch", "ls-remote", "pull", "push", "remote"} == set(), cmd


def test_the_gap_is_still_measurable_with_an_unreachable_remote(tmp_path):
    """The same claim from the outside. `origin` is repointed at a closed port,
    so anything that touched the network would fail or hang — and the answer is
    unchanged, because the count comes off local remote-tracking refs.

    That is also the honest cost, stated: those refs advance only when this
    machine pushes or fetches, so the number means 'commits this machine has
    not pushed'. When it is wrong it over-reports stranded work, which is the
    correct direction for an alarm to be wrong."""
    repo = tmp_path / "work"
    _repo_with_upstream(repo)
    _commits(repo, 5)
    _git(repo, "remote", "set-url", "origin", "https://127.0.0.1:1/blocked.git")

    assert metrics.unpushed_commits(repo) == (5, "")


# ------------------------------------------------- the project's own repo
#
# Pre-goal:g11 this section was "both repos, and the wiring": the engine push
# was the one that broke, the `:07` graph push had exactly the same hole, and
# both had to be measured. goal:g11 merged graph and engine into one repo, so
# there is one number now, not two — and `unpushed_graph_commits` /
# `unpushed_engine_commits` collapsing to a single `unpushed_commits` is
# itself the fix under test here, not incidental cleanup
# (mvp:g11-crons-metrics-residual).


def test_push_gap_stats_measures_the_projects_own_repo(tmp_path):
    repo = tmp_path / "repo"
    _repo_with_upstream(repo)
    _commits(repo, 6)

    assert metrics.push_gap_stats(repo) == {"unpushed_commits": 6, "unpushed_reason": ""}


def test_push_gap_stats_resolves_a_graph_dir_to_its_enclosing_repo(tmp_path):
    """The exact defect this bug fix removes. Under the unified layout `root`
    is `<repo>/.agi`, not the repo's own toplevel — measuring `.agi` directly
    answers `not-a-repo` on every project running the new layout, forever,
    since `.agi` never becomes its own git repo. That was a real, observed
    reading (`unpushed_graph_reason=not-a-repo` on a real `driver.sh --smoke`
    run) before `push_gap_stats` was changed to resolve through
    `locations.repo_root` first."""
    repo = tmp_path / "repo"
    _repo_with_upstream(repo)
    graph_dir = repo / ".agi"
    graph_dir.mkdir()
    (graph_dir / "config.json").write_text("{}")
    _commits(repo, 3)

    assert metrics.push_gap_stats(graph_dir) == \
        {"unpushed_commits": 3, "unpushed_reason": ""}


def test_compute_and_emit_carry_the_push_gap(project):
    """They have to appear in every `--smoke` run, which is this loop."""
    m = metrics.compute(project)
    assert "unpushed_commits" in m
    assert "unpushed_reason" in m

    buf = io.StringIO()
    metrics.emit(project, out=buf)
    assert "METRIC unpushed_commits=" in buf.getvalue()


def test_a_non_project_does_not_crash_the_metrics_stage(project):
    """`project` is a tmp dir that is not a git repo at all. The gap reads
    unknown and nothing raises — the stage still emits its other numbers."""
    assert metrics.compute(project)["unpushed_commits"] == metrics.UNKNOWN_GAP


def test_the_reason_survives_as_one_metric_token(project):
    """`METRIC k=v` is whitespace-delimited: a value with a space becomes a
    truncated field plus a stray one."""
    buf = io.StringIO()
    metrics.emit(project, out=buf)
    line = [ln for ln in buf.getvalue().splitlines()
            if ln.startswith("METRIC unpushed_reason=")]
    assert len(line) == 1
    value = line[0].split("=", 1)[1]
    assert value and " " not in value and "\t" not in value


# ------------------------------------------------- when it raises its voice


def _emit_with_gap(project, capsys, **stats):
    base = {"unpushed_commits": 0, "unpushed_reason": ""}
    base.update(stats)
    real = metrics.push_gap_stats
    metrics.push_gap_stats = lambda _root: base
    try:
        metrics.emit(project)
    finally:
        metrics.push_gap_stats = real
    return capsys.readouterr()


def test_a_large_gap_shouts(project, capsys):
    out = _emit_with_gap(project, capsys, unpushed_commits=metrics.UNPUSHED_WARN_AT)
    assert f"METRIC_WARNING unpushed_commits={metrics.UNPUSHED_WARN_AT}" in out.out
    assert "NEVER BEEN PUSHED" in out.err


def test_a_healthy_repo_is_silent(project, capsys):
    out = _emit_with_gap(project, capsys)
    assert "METRIC_WARNING unpushed" not in out.out
    assert "NEVER BEEN PUSHED" not in out.err


def test_one_cycle_of_ordinary_work_does_not_shout(project, capsys):
    """Measured, not picked: over the 14 days to 2026-08-28, before goal:g11
    unified the two hourly push crons into `branch_push`, the busiest single
    hour of the pair produced 9 commits. A threshold that fires on one missed
    cycle is a threshold people learn to ignore."""
    assert metrics.UNPUSHED_WARN_AT > 9
    out = _emit_with_gap(project, capsys, unpushed_commits=9)
    assert "NEVER BEEN PUSHED" not in out.err


def test_the_threshold_would_have_caught_the_real_outage(project, capsys):
    """3 days, 25 commits, publish reporting success the whole time."""
    assert metrics.UNPUSHED_WARN_AT <= 25
    out = _emit_with_gap(project, capsys, unpushed_commits=25)
    assert "METRIC_WARNING unpushed_commits=25" in out.out


def test_an_unmeasurable_gap_does_not_shout(project, capsys):
    """It is not a claim of health — the count reads the sentinel and the
    reason names the blind spot. But a fork with no remote configured is
    unconfigured, not stranded, and a banner it can never clear is how an alarm
    earns the reputation that gets it switched off."""
    out = _emit_with_gap(project, capsys,
                         unpushed_commits=metrics.UNKNOWN_GAP,
                         unpushed_reason="no-upstream")
    assert "NEVER BEEN PUSHED" not in out.err
    assert "METRIC_WARNING unpushed" not in out.out
    assert "METRIC unpushed_reason=no-upstream" in out.out


# ------------------------------------------------- and the hook reaches it


def _hook_project(tmp_path, gap: int):
    """A real project that is a real repo with a real upstream. The hook
    shells out to git for real, so nothing here can be faked with a state
    file."""
    graph = tmp_path / "graph"
    _repo_with_upstream(graph)
    (graph / "agi-tree.config.json").write_text("{}")
    (graph / "context").mkdir()
    (graph / "nodes").mkdir()
    _git(graph, "add", "-A")
    _git(graph, "commit", "-qm", "project marker")
    _git(graph, "push", "-q", "origin", "HEAD")
    _commits(graph, gap)
    return graph


def test_the_hook_shouts_when_commits_are_stranded(tmp_path):
    """A metric nobody reads is one step short of a failure that moves no
    metric. The next agent to open any session in this project is told."""
    graph = _hook_project(tmp_path, metrics.UNPUSHED_WARN_AT)
    (graph / "context" / "INJECTION.md").write_text("map\n")

    r = _run_hook(graph)

    assert r.returncode == 0
    assert "STRANDED" in r.stdout
    assert str(metrics.UNPUSHED_WARN_AT) in r.stdout
    assert "Nothing is lost" in r.stdout
    # and it must not have eaten the map it also exists to inject
    assert "agi-tree map (auto-injected)" in r.stdout


def test_the_hook_is_quiet_when_nothing_is_stranded(tmp_path):
    graph = _hook_project(tmp_path, 0)
    (graph / "context" / "INJECTION.md").write_text("map\n")

    r = _run_hook(graph)

    assert "STRANDED" not in r.stdout
    assert "agi-tree map (auto-injected)" in r.stdout


def test_the_hook_and_the_metric_cannot_disagree_about_the_threshold(tmp_path):
    """Two readers of one fact that could drift apart is a bug this project has
    already paid for (H4c). The hook imports `metrics.py` rather than
    reimplementing the count, so there is one definition, shared by import."""
    hook = HOOK_SH.read_text(encoding="utf-8")
    assert "UNPUSHED_WARN_AT" in hook
    assert "push_gap_stats" in hook
    assert "rev-list" not in hook


def test_the_hook_is_still_a_silent_no_op_outside_a_project(tmp_path):
    """Re-measured, not assumed. This is the entire safety argument for
    registering the hook globally in `~/.claude/settings.json`, and the new
    block runs git — so the claim has to be re-established, including from
    inside a git repo that is not a project."""
    outside = tmp_path / "not-a-project"
    _repo_with_upstream(outside)
    _commits(outside, 40)

    r = _run_hook(outside)

    assert r.returncode == 0
    assert r.stdout == ""
    assert r.stderr == ""


def test_the_retired_publish_alarm_stays_silent(project):
    """goal:g7.16.1.4.1.1 -- publish-engine.sh and its g7.10 SessionStart alarm
    are retired: a refusing publish-state.json (the shape that raised the
    banner at 01cd96628^) now makes the hook print no publish alarm."""
    state = project / "context" / "publish-state.json"
    state.write_text(json.dumps({
        "last_run_epoch": time.time() - 30 * 3600,
        "last_run_status": "refused", "last_run_reason": "gate0",
    }), encoding="utf-8")
    r = _run_hook(project)
    assert r.returncode == 0
    assert "publish is STALLED" not in r.stdout
    assert "publish-engine.sh" not in r.stdout
