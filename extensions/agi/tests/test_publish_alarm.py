"""The publish cron must never fail silently (goal:g7.10, parts 1 and 2).

`publish-engine.sh` is the hourly `:37` cron. Its gate-0 refusal — the graph
must have no uncommitted change under `nodes/` or `GOALS.md` — is **correct**
and nothing here weakens it. What these tests pin is everything around it:

- it refused **40 consecutive times and published nothing at all**, from
  install on 2026-08-25 until someone checked by hand on 2026-08-27;
- the refusal went to a log nobody reads. No metric moved, `driver.sh --smoke`
  said nothing, `INJECTION.md` said nothing;
- one self-inflicted dirty node arms it permanently (one character of YAML
  quoting did, for weeks), and the 3.11/3.12 f-string flap then made it
  *intermittent*, which is worse: healthy-looking half the time is exactly
  when nobody investigates.

So three claims, and each has to hold on its own:

1. a stall moves a number (`hours_since_successful_publish`) and names itself
   (`publish_blocked_reason`);
2. a refusal exits non-zero and leaves a durable, machine-readable marker;
3. the SessionStart hook shouts about that marker *inside* a project and stays
   a **silent no-op outside one** — that silence is the only thing that makes
   registering the hook globally, for every session on the machine, safe.
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
PUBLISH_SH = BIN / "publish-engine.sh"
HOOK_SH = PLUGIN / "hooks" / "cc-session-start.sh"

eg_spec = importlib.util.spec_from_file_location("evidence_gate", BIN / "evidence_gate.py")
evidence_gate = importlib.util.module_from_spec(eg_spec)
sys.modules["evidence_gate"] = evidence_gate
eg_spec.loader.exec_module(evidence_gate)

spec = importlib.util.spec_from_file_location("metrics", BIN / "metrics.py")
metrics = importlib.util.module_from_spec(spec)
sys.modules["metrics"] = metrics
spec.loader.exec_module(metrics)

STATE_REL = Path(*metrics.PUBLISH_STATE_PATH)


# --------------------------------------------------------------- fixtures


@pytest.fixture()
def project(tmp_path):
    """A minimal project: the config marker is what makes a dir a project."""
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "nodes").mkdir()
    (tmp_path / "context").mkdir()
    return tmp_path


def _write_state(root: Path, **fields):
    p = root / STATE_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(fields), encoding="utf-8")
    return p


def _read_state(root: Path) -> dict:
    return json.loads((root / STATE_REL).read_text(encoding="utf-8"))


def _git(root: Path, *args):
    subprocess.run(["git", *args], cwd=root, check=True,
                   capture_output=True, text=True)


def _git_project(tmp_path) -> Path:
    """A project that is also a git repo with one committed node."""
    root = tmp_path / "proj"
    (root / "nodes").mkdir(parents=True)
    (root / "agi-tree.config.json").write_text("{}")
    (root / "nodes" / "n.md").write_text('---\nid: "goal:n"\ntype: goal\n---\n\nbody\n')
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "init")
    return root


def _dirty(root: Path):
    """The exact state gate 0 exists to refuse: an uncommitted node change."""
    with (root / "nodes" / "n.md").open("a") as fh:
        fh.write("\nuncommitted\n")


def _run_publish(root: Path, *args):
    return subprocess.run(["bash", str(PUBLISH_SH), *args],
                          cwd=root, capture_output=True, text=True)


def _run_hook(cwd: Path):
    """Run the hook with a scrubbed environment, as CC would."""
    env = dict(os.environ)
    env.pop("AGI_TREE_PROJECT_ROOT", None)
    env.pop("AUTORESEARCH_TREE_PROJECT_ROOT", None)
    return subprocess.run(["bash", str(HOOK_SH)], cwd=cwd,
                          capture_output=True, text=True, env=env)


# ------------------------------------------ 1. the alarm has to move a number


def test_never_published_is_the_loudest_value_not_the_quietest(project):
    """The inversion that hid the outage: for this metric higher is worse, so
    `0` — "published seconds ago", the most reassuring number in the range —
    must not be what "never published at all" reads as."""
    s = metrics.publish_stats(project)
    assert s["hours_since_successful_publish"] == metrics.NEVER_PUBLISHED_HOURS
    assert metrics.NEVER_PUBLISHED_HOURS > 24 * 365   # unmistakably not elapsed time
    assert s["publish_blocked_reason"] == metrics.NEVER_RUN_REASON


def test_no_marker_at_all_does_not_report_as_healthy(project):
    """A cron that has never written a marker has never published. Empty is
    reserved for "the last run succeeded" and may mean nothing else."""
    assert metrics.publish_stats(project)["publish_blocked_reason"] != ""


def test_a_successful_publish_clears_both_numbers(project):
    now = time.time()
    _write_state(project, last_run_status="ok", last_run_reason="",
                 last_success_epoch=now - 1800)
    s = metrics.publish_stats(project, now=now)
    assert s["hours_since_successful_publish"] == 0.5
    assert s["publish_blocked_reason"] == ""


def test_a_refusal_names_itself_and_keeps_the_clock_running(project):
    """40 refusals in a row must be legible as 40 hours of not publishing."""
    now = time.time()
    _write_state(project, last_run_status="refused", last_run_reason="graph-dirty",
                 last_success_epoch=now - 40 * 3600)
    s = metrics.publish_stats(project, now=now)
    assert s["hours_since_successful_publish"] == 40.0
    assert s["publish_blocked_reason"] == "graph-dirty"


def test_a_cron_that_simply_stops_still_moves_the_number(project):
    """No refusal, no error — the cron is just gone. The metric needs no
    threshold to catch that: elapsed time since a real publish is unbounded."""
    now = time.time()
    _write_state(project, last_run_status="ok", last_success_epoch=now - 72 * 3600)
    assert metrics.publish_stats(project, now=now)["hours_since_successful_publish"] == 72.0


def test_a_refusal_with_no_reason_is_still_not_silent(project):
    _write_state(project, last_run_status="refused", last_run_reason="")
    assert metrics.publish_stats(project)["publish_blocked_reason"] == \
        metrics.UNKNOWN_REASON


def test_a_corrupt_marker_alarms_rather_than_reassures(project):
    """Unreadable and absent collapse to the same answer on purpose. A marker
    this metric cannot parse is not evidence that anything was published."""
    p = project / STATE_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{not json at all")
    s = metrics.publish_stats(project)
    assert s["hours_since_successful_publish"] == metrics.NEVER_PUBLISHED_HOURS
    assert s["publish_blocked_reason"] == metrics.NEVER_RUN_REASON


def test_a_clock_that_moved_backwards_does_not_read_as_a_future_publish(project):
    now = time.time()
    _write_state(project, last_run_status="ok", last_success_epoch=now + 9999)
    assert metrics.publish_stats(project, now=now)["hours_since_successful_publish"] == 0.0


@pytest.mark.parametrize("raw", [
    "graph dirty\nsecond line",
    "  contracts disagree  ",
    "REFUSING: nodes/ + GOALS.md",
])
def test_the_reason_survives_as_one_metric_token(project, raw):
    """`METRIC k=v` is a whitespace-delimited line format: a space makes the
    value a truncated field plus a stray one, a newline makes a second
    malformed record. Neither fails loudly."""
    _write_state(project, last_run_status="refused", last_run_reason=raw)
    buf = io.StringIO()
    metrics.emit(project, out=buf)
    line = [ln for ln in buf.getvalue().splitlines()
            if ln.startswith("METRIC publish_blocked_reason=")]
    assert len(line) == 1
    value = line[0].split("=", 1)[1]
    assert value and " " not in value and "\t" not in value
    assert len(value) <= metrics.MAX_REASON_LEN


def test_a_reason_that_is_not_a_string_does_not_crash_the_metrics_stage(project):
    _write_state(project, last_run_status="refused", last_run_reason={"a": 1})
    assert metrics.publish_stats(project)["publish_blocked_reason"] == \
        metrics.UNKNOWN_REASON


def test_both_metrics_reach_the_metric_lines(project):
    """They have to appear in every `--smoke` run, which is this loop."""
    buf = io.StringIO()
    metrics.emit(project, out=buf)
    text = buf.getvalue()
    assert "METRIC hours_since_successful_publish=" in text
    assert "METRIC publish_blocked_reason=" in text


def test_compute_carries_the_publish_alarm(project):
    m = metrics.compute(project)
    assert "hours_since_successful_publish" in m
    assert "publish_blocked_reason" in m


def test_a_stall_raises_a_warning_a_healthy_publish_does_not(project, capsys):
    _write_state(project, last_run_status="refused", last_run_reason="graph-dirty",
                 last_success_epoch=time.time() - 3600)
    metrics.emit(project)
    out = capsys.readouterr()
    assert "METRIC_WARNING publish_stalled=graph-dirty" in out.out
    assert "STALLED" in out.err
    # the reassuring true thing, said where the fear is
    assert "NOT lost" in out.err and "grid.py commit" in out.err

    _write_state(project, last_run_status="ok", last_success_epoch=time.time())
    metrics.emit(project)
    assert "publish_stalled" not in capsys.readouterr().out


# ---------------------------------- 2. non-zero exit + a durable marker


def test_a_refusal_exits_non_zero(tmp_path):
    root = _git_project(tmp_path)
    _dirty(root)
    r = _run_publish(root)
    assert r.returncode != 0, r.stdout + r.stderr


def test_a_refusal_writes_a_machine_readable_marker(tmp_path):
    root = _git_project(tmp_path)
    _dirty(root)
    _run_publish(root)
    state = _read_state(root)
    assert state["last_run_status"] == "refused"
    assert state["last_run_reason"] == "graph-dirty"
    assert isinstance(state["last_run_epoch"], int)


def test_the_marker_is_not_written_under_nodes(tmp_path):
    """It must not live where gate 0 looks. A publish marker under `nodes/`
    would leave an uncommitted change on every run and arm, permanently, the
    exact gate it exists to report on."""
    assert metrics.PUBLISH_STATE_PATH[0] != "nodes"
    root = _git_project(tmp_path)
    _dirty(root)
    _run_publish(root)
    assert (root / STATE_REL).is_file()
    assert not list((root / "nodes").glob("publish-state*"))


def test_the_refusal_says_the_bytes_are_safe(tmp_path):
    """The reasonable fear when a publish stalls is that engine work is
    evaporating, and it is wrong: `grid.py commit --all` runs on its own
    ungated 5-minute cadence. Say so at the moment the fear arrives."""
    root = _git_project(tmp_path)
    _dirty(root)
    r = _run_publish(root)
    text = r.stdout + r.stderr
    assert "NOT lost" in text
    assert "grid.py commit --all" in text


def test_a_refusal_does_not_erase_the_last_real_publish(tmp_path):
    """That timestamp is the whole alarm — a refusal that reset it would make
    a two-day outage indistinguishable from a fresh install."""
    root = _git_project(tmp_path)
    _write_state(root, schema=1, last_run_status="ok", last_run_reason="",
                 last_success_epoch=1000, last_success_graph_commit="deadbee")
    _dirty(root)
    _run_publish(root)
    state = _read_state(root)
    assert state["last_run_status"] == "refused"
    assert state["last_success_epoch"] == 1000
    assert state["last_success_graph_commit"] == "deadbee"


def test_dry_run_never_touches_the_marker(tmp_path):
    """`--dry-run` is a report. A hand-run dry pass overwriting the cron's
    record of what really happened would be a new way to lose the signal."""
    root = _git_project(tmp_path)
    _write_state(root, schema=1, last_run_status="ok", last_success_epoch=1000)
    before = (root / STATE_REL).read_text()
    _dirty(root)
    r = _run_publish(root, "--dry-run")
    assert r.returncode != 0
    assert (root / STATE_REL).read_text() == before


def test_gate_zero_is_still_a_refusal(tmp_path):
    """Nothing here weakens the gate: a dirty graph must still not publish.
    A published engine has to cite a graph commit that exists."""
    root = _git_project(tmp_path)
    _dirty(root)
    r = _run_publish(root)
    assert "REFUSING" in r.stdout
    assert r.returncode != 0
    # ...and it refused before doing anything at all
    assert "re-deriving contracts" not in r.stdout


# ------------------------------------------------- 3. the SessionStart hook


def test_the_hook_is_a_silent_no_op_outside_a_project(tmp_path):
    """Registered globally in ~/.claude/settings.json, so it runs for every
    session in every directory on this machine. Silence outside a project is
    the entire safety argument for that."""
    outside = tmp_path / "not-a-project"
    outside.mkdir()
    r = _run_hook(outside)
    assert r.returncode == 0
    assert r.stdout == ""
    assert r.stderr == ""


def test_the_hook_stays_silent_outside_a_project_even_with_a_stray_marker(tmp_path):
    """A `context/publish-state.json` with no config file beside it is not a
    project, and must not make the hook speak."""
    outside = tmp_path / "not-a-project"
    (outside / "context").mkdir(parents=True)
    (outside / "context" / "publish-state.json").write_text(
        json.dumps({"last_run_status": "refused", "last_run_reason": "graph-dirty"}))
    r = _run_hook(outside)
    assert r.returncode == 0
    assert r.stdout == ""


def test_the_hook_shouts_when_the_publish_is_stalled(project):
    (project / "context" / "INJECTION.md").write_text("map\n")
    _write_state(project, schema=1, last_run_status="refused",
                 last_run_reason="graph-dirty", last_run_detail="nodes/ is dirty",
                 last_success_epoch=time.time() - 40 * 3600)
    r = _run_hook(project)
    assert r.returncode == 0
    assert "STALLED" in r.stdout
    assert "graph-dirty" in r.stdout
    # and it must carry the true reassurance, not just the alarm
    assert "No payload bytes are lost" in r.stdout
    assert "grid.py commit --all" in r.stdout
    # and it must not have eaten the map it also exists to inject
    assert "agi-tree map (auto-injected)" in r.stdout


def test_the_hook_shouts_even_when_there_is_no_map_to_inject(project):
    """The old hook exits silently when `INJECTION.md` is missing. The alarm
    has to survive that path — a project too broken to render a map is exactly
    the one whose publish is most likely stalled."""
    assert not (project / "context" / "INJECTION.md").exists()
    _write_state(project, schema=1, last_run_status="refused",
                 last_run_reason="contracts-disagree")
    r = _run_hook(project)
    assert r.returncode == 0
    assert "STALLED" in r.stdout


def test_the_hook_is_quiet_when_the_publish_is_healthy(project):
    (project / "context" / "INJECTION.md").write_text("map\n")
    now = time.time()
    _write_state(project, schema=1, last_run_status="ok", last_run_reason="",
                 last_run_epoch=now, last_success_epoch=now,
                 last_success_graph_commit="abc1234")
    r = _run_hook(project)
    assert r.returncode == 0
    assert "STALLED" not in r.stdout
    assert "agi-tree map (auto-injected)" in r.stdout


def test_the_hook_shouts_when_the_cron_itself_has_stopped(project):
    """`last_run_status: ok` and nothing since. An hourly cron silent for a
    day and a half has stopped, not slowed."""
    (project / "context" / "INJECTION.md").write_text("map\n")
    old = time.time() - 36 * 3600
    _write_state(project, schema=1, last_run_status="ok", last_run_epoch=old,
                 last_success_epoch=old)
    r = _run_hook(project)
    assert "STALLED" in r.stdout
    assert "has not run" in r.stdout


def test_a_corrupt_marker_does_not_break_the_hook(project):
    """A hook that can fail is a hook that gets uninstalled — and this one has
    to keep working precisely when the project is in a broken state."""
    (project / "context" / "INJECTION.md").write_text("map\n")
    (project / STATE_REL).write_text("{ truncated")
    r = _run_hook(project)
    assert r.returncode == 0
    assert "agi-tree map (auto-injected)" in r.stdout


def test_no_marker_means_no_banner(project):
    """A project that never installed the publish cron has nothing to be told,
    and a permanent false alarm in every session is how a mechanism like this
    gets switched off. `metrics.py` still reports `never-run` for the same
    state, for whoever is actually reading the numbers."""
    (project / "context" / "INJECTION.md").write_text("map\n")
    r = _run_hook(project)
    assert "STALLED" not in r.stdout
    assert metrics.publish_stats(project)["publish_blocked_reason"] == \
        metrics.NEVER_RUN_REASON
