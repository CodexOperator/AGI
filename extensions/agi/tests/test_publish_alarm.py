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

Part 3 adds a fourth, and it pulls in the opposite direction from the first
three: **the bytes must land somewhere even when the main path is blocked**, on
`cron/pending-<graph-sha>`, locally, never pushed. The tension is the point —
a safety net that made the alarm read healthy would be the same bug as an alarm
that never fired, so parking is still a refusal (non-zero exit, `last_success_*`
frozen, the clock still climbing) and the fallback is held to the same gate-2
verification the real publish is.

Part 4 adds a fifth, and it is about the *other* half of "silently": **a
refusal has to be a no-op**. It was not. Step 1 re-derived every contract
straight into `nodes/` and committed a grid version for each, and only then did
gate 2 get a say — so a refused run during the last rename left **184 junk
nodes** and 184 burned grid versions behind, which then armed gate 0 for the
next run. "It refused" has to mean "nothing happened", because that is what
every reader assumes it means.

goal:s20 adds a sixth, and it is the half of the path everything above stops
short of. All five claims end at the **local commit**. `publish-engine.sh`
commits the engine and deliberately does not push, on the stated grounds that
pushing is the hourly push cron's job — and for the engine repo that cron did
not exist. The two halves shipped apart and the gap was invisible from both
sides: publish-engine reported success every time,
`hours_since_successful_publish` read healthy, the local tree was healthy, and
the remote sat **3 days and 25 commits** behind. It was found by looking at
GitHub, which is the failure mode this whole goal exists to remove. So section
6 pins a count of what has been committed and not pushed — **state, not an
event**, because a push that succeeds with nothing to push is
indistinguishable from one that shipped 25 commits.
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

_l3_spec = importlib.util.spec_from_file_location("level3_publish", BIN / "level3.py")
l3 = importlib.util.module_from_spec(_l3_spec)
_l3_spec.loader.exec_module(l3)

_grid_spec = importlib.util.spec_from_file_location("grid_publish", BIN / "grid.py")
grid = importlib.util.module_from_spec(_grid_spec)
_grid_spec.loader.exec_module(grid)

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


def _run_publish(root: Path, *args, env=None):
    return subprocess.run(["bash", str(PUBLISH_SH), *args],
                          cwd=root, capture_output=True, text=True, env=env)


def _run_hook(cwd: Path):
    """Run the hook with a scrubbed environment, as CC would."""
    env = dict(os.environ)
    env.pop("AGI_TREE_PROJECT_ROOT", None)
    env.pop("AUTORESEARCH_TREE_PROJECT_ROOT", None)
    return subprocess.run(["bash", str(HOOK_SH)], cwd=cwd,
                          capture_output=True, text=True, env=env)


# ------------------------------------------ 1. the alarm that used to live here
#
# `hours_since_successful_publish` and `publish_blocked_reason` (goal:g7.10)
# read `context/publish-state.json` through `metrics.publish_stats` and turned
# it into two METRIC lines. goal:g11 merged the graph and engine repos that
# `publish-engine.sh` moved bytes between, so the publish this alarm existed to
# catch can no longer happen — and a metric permanently reporting its own
# sentinel is exactly the failure mode H3/H4c already forced this project to
# remove elsewhere. `metrics.py` no longer computes either number
# (mvp:g11-crons-metrics-residual). `publish-engine.sh` and the SessionStart
# banner below (sections 2-4) are untouched — they still read this same marker
# file directly — only the METRIC-line mirror of it is gone.


def test_publish_stats_no_longer_exists_on_metrics():
    """Regression: the function that emitted a permanent sentinel for a
    publish goal:g11 made structurally impossible must not come back."""
    assert not hasattr(metrics, "publish_stats")
    assert not hasattr(metrics, "read_publish_state")
    assert not hasattr(metrics, "NEVER_PUBLISHED_HOURS")
    assert not hasattr(metrics, "NEVER_RUN_REASON")


def test_the_retired_publish_metrics_are_not_emitted(project):
    """The exact two METRIC keys measured on a real `driver.sh --smoke` run
    and found to always read a sentinel, never a measurement."""
    _write_state(project, last_run_status="refused", last_run_reason="graph-dirty",
                 last_success_epoch=time.time() - 40 * 3600)
    buf = io.StringIO()
    metrics.emit(project, out=buf)
    text = buf.getvalue()
    assert "hours_since_successful_publish" not in text
    assert "publish_blocked_reason" not in text
    assert "publish_stalled" not in text


def test_compute_no_longer_carries_the_publish_alarm(project):
    m = metrics.compute(project)
    assert "hours_since_successful_publish" not in m
    assert "publish_blocked_reason" not in m


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
    gets switched off."""
    (project / "context" / "INJECTION.md").write_text("map\n")
    r = _run_hook(project)
    assert "STALLED" not in r.stdout


# ------------------------------- 4. branch and continue (goal:g7.10 part 3)
#
# The three sections above are all about being *heard*. This one is about not
# *stopping*: a refusal that parks its bytes on `cron/pending-<graph-sha>` keeps
# the work reachable without ever writing the default branch from a graph commit
# that does not exist. Both invariants at once, which is why the goal names this
# the recommended default.


PAIR_FILES = {
    "extensions/agi/bin/foo.py": "import os\n\n\ndef foo():\n    pass\n",
    "extensions/agi/src/pkg/bar.py": "import sys\n\n\ndef bar():\n    pass\n",
}


def _git_out(root: Path, *args) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True).stdout.strip()


def _init_repo(root: Path):
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")


def _pair(tmp_path, engine_lags: bool = True, extra_nodes: dict | None = None,
          staged: bool = False):
    """A real graph repo with grid-backed payloads beside a real engine repo —
    the smallest arrangement in which a pending branch can carry actual bytes.

    `engine_lags` rewrites one engine file *after* the grid recorded it, so the
    engine tree is genuinely behind the graph. Without that every path collapses
    to "already matched" and the interesting half is never exercised.

    `staged` also lays down `<project>/payloads/`, the checkout `grid.py
    checkout --all` produces and every real project has. It matters on the
    success path and only there: `grid.py commit` takes no `--engine-root`, so
    with no staged copy it resolves payloads against *its own* location on disk
    — the real repo, not the fixture's engine — finds nothing, and records a
    version with the payload entry dropped. Off by default because the part-3
    tests deliberately move the *engine* tree under a fresh `grid.cmd_commit`,
    which a staged copy would shadow.
    """
    engine = tmp_path / "engine"
    for rel, text in PAIR_FILES.items():
        p = engine / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    _init_repo(engine)
    _git(engine, "add", "-A")
    _git(engine, "commit", "-qm", "engine base")

    project = tmp_path / "proj"
    (project / "nodes" / "build").mkdir(parents=True)
    (project / "agi-tree.config.json").write_text("{}")
    if staged:
        for rel, text in PAIR_FILES.items():
            p = project / "payloads" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
    for rel in PAIR_FILES:
        node_id, fm, body, _ = l3.build_node(rel, engine / rel, None)
        slug = node_id.split(":", 1)[-1]
        l3.write_frontmatter(project / "nodes" / "build" / f"{slug}.md", fm,
                             body, origin="build-scan")
    for slug, text in (extra_nodes or {}).items():
        (project / "nodes" / "build" / f"{slug}.md").write_text(text, encoding="utf-8")
    _init_repo(project)
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)
    _git(project, "add", "-A")
    _git(project, "commit", "-qm", "graph base")

    if engine_lags:
        (engine / "extensions/agi/bin/foo.py").write_text("# stale\n", encoding="utf-8")
        _git(engine, "commit", "-qam", "engine falls behind the graph")
    return project, engine


def _pending(project: Path) -> str:
    return "cron/pending-" + _git_out(project, "rev-parse", "--short", "HEAD")


def _dirty_a_node(project: Path):
    """Arm gate 0 the way the real thing arms it: one uncommitted node."""
    node = sorted((project / "nodes" / "build").glob("*.md"))[0]
    with node.open("a") as fh:
        fh.write("\nuncommitted\n")


def _publish(project: Path, engine: Path, *args, env=None):
    return _run_publish(project, "--engine-root", str(engine), *args, env=env)


def test_a_blocked_publish_parks_the_bytes_instead_of_stranding_them(tmp_path):
    """The whole of part 3: the main path is blocked and the tree still lands
    somewhere a human can reach it."""
    project, engine = _pair(tmp_path)
    _dirty_a_node(project)
    branch = _pending(project)

    r = _publish(project, engine)

    assert r.returncode != 0, r.stdout + r.stderr
    assert _git_out(engine, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}")
    # ...and it carries the graph's bytes, not the engine's stale ones
    parked = _git_out(engine, "show", f"{branch}:extensions/agi/bin/foo.py")
    assert parked == PAIR_FILES["extensions/agi/bin/foo.py"].strip()
    assert _git_out(engine, "show", "HEAD:extensions/agi/bin/foo.py") == "# stale"


def test_the_fallback_never_writes_the_default_branch(tmp_path):
    """The invariant gate 0 exists for survives the fallback: the default
    branch is still only ever written from a graph commit that exists."""
    project, engine = _pair(tmp_path)
    before = _git_out(engine, "rev-parse", "master")
    _dirty_a_node(project)

    _publish(project, engine)

    assert _git_out(engine, "rev-parse", "master") == before


def test_the_fallback_leaves_the_engine_checkout_exactly_where_it_was(tmp_path):
    """Why this uses a detached worktree and not `git checkout -b` in the
    engine's own tree: work once piled up on an `iter24-extend-300hop` branch
    while a cron pushed `master` and published nothing. A cron that moves a
    shared checkout out from under its readers is that failure again."""
    project, engine = _pair(tmp_path)
    head, branch = _git_out(engine, "rev-parse", "HEAD"), _git_out(engine, "branch", "--show-current")
    _dirty_a_node(project)

    _publish(project, engine)

    assert _git_out(engine, "rev-parse", "HEAD") == head
    assert _git_out(engine, "branch", "--show-current") == branch
    assert _git_out(engine, "status", "--porcelain") == ""


def test_the_fallback_leaves_no_worktree_behind(tmp_path):
    """It builds in a temporary worktree; a cron that leaks one per hour would
    be its own slow failure."""
    project, engine = _pair(tmp_path)
    before = _git_out(engine, "worktree", "list")
    tmproot, env = _hermetic_tmp_env(tmp_path)
    leaked = len(list(tmproot.glob("agi-publish-fallback.*")))
    _dirty_a_node(project)

    _publish(project, engine, env=env)

    assert _git_out(engine, "worktree", "list") == before
    # counted, not asserted absent: hermetic now (private TMPDIR), but kept as
    # a count rather than an absence assert -- a genuine fallback dir this
    # call itself needed to leave (if that were ever the correct behavior)
    # should still be tolerated, only another process's can't intrude anymore
    assert len(list(tmproot.glob("agi-publish-fallback.*"))) == leaked


def test_parking_the_bytes_does_not_make_the_alarm_read_healthy(tmp_path):
    """The error that would undo part 1 from the other side. A refusal that
    successfully parked is STILL a refusal: the clock keeps climbing and the
    block keeps naming itself, or a permanent stall looks like a healthy repo
    with a slightly unusual branch list."""
    project, engine = _pair(tmp_path)
    _write_state(project, schema=1, last_run_status="ok", last_run_reason="",
                 last_success_epoch=1000, last_success_graph_commit="deadbee")
    _dirty_a_node(project)

    _publish(project, engine)

    state = _read_state(project)
    assert state["last_run_status"] == "refused"
    assert state["last_run_reason"] == "graph-dirty"
    assert state["last_success_epoch"] == 1000
    assert state["last_success_graph_commit"] == "deadbee"


def test_the_marker_says_where_the_parked_bytes_went(tmp_path):
    """Additive keys, and they have to be enough to find the branch: the alarm
    tells you it is stalled, this tells you nothing was lost while it was."""
    project, engine = _pair(tmp_path)
    _dirty_a_node(project)
    branch = _pending(project)

    _publish(project, engine)

    state = _read_state(project)
    assert state["last_fallback_status"] == "parked"
    assert state["last_fallback_branch"] == branch
    assert state["last_fallback_commit"] == _git_out(engine, "rev-parse", "--short", branch)


def test_a_second_run_at_the_same_dirty_state_does_not_commit_again(tmp_path):
    """This is the `:37` cron. A graph dirty for three days is 72 runs, and 72
    commits of identical bytes is manufactured junk — the same shape as the 184
    junk nodes a refused run once left behind."""
    project, engine = _pair(tmp_path)
    _dirty_a_node(project)
    branch = _pending(project)

    _publish(project, engine)
    first = _git_out(engine, "rev-parse", branch)
    r2 = _publish(project, engine)

    assert r2.returncode != 0
    assert _git_out(engine, "rev-parse", branch) == first
    assert _git_out(engine, "rev-list", "--count", f"master..{branch}") == "1"
    assert _read_state(project)["last_fallback_status"] == "already-parked"


def test_a_moving_grid_does_add_a_second_commit(tmp_path):
    """The idempotency check is a diff, not a mute button. The branch name is
    keyed on the graph sha, which does not move while the graph is dirty — but
    `grid.py commit --all` is a separate ungated 5-minute cron, so the content
    genuinely changes between runs and must still be parked."""
    project, engine = _pair(tmp_path)
    _dirty_a_node(project)
    branch = _pending(project)
    _publish(project, engine)

    (engine / "extensions/agi/bin/foo.py").write_text("import os\n\n\ndef foo():\n    return 2\n")
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)
    _publish(project, engine)

    assert _git_out(engine, "rev-list", "--count", f"master..{branch}") == "2"
    assert _git_out(engine, "show", f"{branch}:extensions/agi/bin/foo.py").endswith("return 2")


def test_the_pending_branch_can_still_be_fast_forwarded(tmp_path):
    """The commit message tells a human to `merge --ff-only`. That has to be
    true, which means the branch must always descend from the default branch."""
    project, engine = _pair(tmp_path)
    _dirty_a_node(project)
    branch = _pending(project)

    _publish(project, engine)

    assert subprocess.run(["git", "merge-base", "--is-ancestor", "master", branch],
                          cwd=engine).returncode == 0


def test_the_parked_commit_does_not_claim_the_graph_sha_describes_it(tmp_path):
    """Under a graph-dirty refusal the bytes come from the grid, which runs
    ahead of the graph's git HEAD — so the tree is attributable to no graph
    commit at all. That is the whole reason master refused, and a message that
    read like ordinary provenance would launder it."""
    project, engine = _pair(tmp_path)
    _dirty_a_node(project)
    branch = _pending(project)

    _publish(project, engine)

    msg = _git_out(engine, "log", "-1", "--format=%B", branch)
    assert "NOT AS PROVENANCE" in msg
    assert "nearest COMMITTED state of the graph" in msg
    assert "merge --ff-only" in msg and "branch -D" in msg


def test_the_fallback_parks_nothing_the_real_publish_would_refuse(tmp_path):
    """Gate 2 has not run when gate 0 refuses, so the fallback runs it itself.
    A pending branch is one fast-forward from the default branch — parking
    unverified bytes there just moves the drift one command away instead of
    stopping it."""
    ghost = ('---\nid: "build:ghost"\ntype: build\nlevel: 3\n'
             'payload_ref: extensions/agi/bin/ghost.py\n---\n\nbody\n')
    project, engine = _pair(tmp_path, extra_nodes={"ghost": ghost})
    _dirty_a_node(project)
    branch = _pending(project)

    r = _publish(project, engine)

    assert r.returncode != 0
    assert _git_out(engine, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}") == ""
    assert _read_state(project)["last_fallback_status"] == "verify-failed"


def test_a_declined_fallback_shows_what_the_verify_actually_said(tmp_path):
    """Sending that output to /dev/null cost a real diagnosis: a fallback
    declined `verify-failed` while a concurrent `*/5` grid cron ran, and
    afterwards there was no way to tell drift from a lost race. A decline whose
    evidence is gone is the failure mode this goal is named after."""
    ghost = ('---\nid: "build:ghost"\ntype: build\nlevel: 3\n'
             'payload_ref: extensions/agi/bin/ghost.py\n---\n\nbody\n')
    project, engine = _pair(tmp_path, extra_nodes={"ghost": ghost})
    _dirty_a_node(project)

    r = _publish(project, engine)

    assert "missing_payload" in r.stdout
    assert "extensions/agi/bin/ghost.py" in r.stdout


def test_dry_run_creates_no_branch(tmp_path):
    """`--dry-run` writes nothing, and a branch is a write."""
    project, engine = _pair(tmp_path)
    _dirty_a_node(project)
    branch = _pending(project)

    r = _publish(project, engine, "--dry-run")

    assert r.returncode != 0
    assert _git_out(engine, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}") == ""
    assert not (project / STATE_REL).exists()


def test_the_fallback_never_cuts_a_branch_in_the_graph_repo(tmp_path):
    """`ENGINE_ROOT` defaults to a path derived from the script's own location,
    which for a copy running out of the graph's `payloads/` tree resolves to a
    directory *inside the graph repo*. `git -C` would answer for the graph, and
    the fallback would cut `cron/pending-*` in the thoughtgraph."""
    project, _engine = _pair(tmp_path)
    _dirty_a_node(project)
    inside = project / "payloads"
    inside.mkdir()

    r = _run_publish(project, "--engine-root", str(inside))

    assert r.returncode != 0
    assert _git_out(project, "branch", "--list", "cron/*") == ""
    assert _read_state(project)["last_fallback_status"] == "no-engine"


def test_a_stale_pending_branch_is_rebuilt_rather_than_extended(tmp_path):
    """If the default branch moved on without it, a pending branch can no
    longer be fast-forwarded. Extending it would park work onto a ref whose
    documented landing instruction has quietly stopped working."""
    project, engine = _pair(tmp_path)
    _dirty_a_node(project)
    branch = _pending(project)
    _publish(project, engine)
    stale = _git_out(engine, "rev-parse", branch)

    # Move master by editing a file the graph already claims. A *new* engine
    # file would be an orphan with no level-3 node, which is drift — verify
    # would decline the fallback and this test would pass for the wrong reason.
    (engine / "extensions/agi/src/pkg/bar.py").write_text("# master moved on\n")
    _git(engine, "commit", "-qam", "master moves without the pending branch")
    _publish(project, engine)

    assert _git_out(engine, "rev-parse", branch) != stale
    assert subprocess.run(["git", "merge-base", "--is-ancestor", "master", branch],
                          cwd=engine).returncode == 0


# ---------------------------- 5. an atomic refusal (goal:g7.10 part 4)
#
# Section 4 is about a refusal that still gets the work somewhere. This one is
# about a refusal that does not get anything ANYWHERE — the graph repo is left
# exactly as the run found it. Derivation happens in a throwaway `git worktree`
# of the graph (a worktree and not a `cp -r`, because `--from-grid` resolves
# payloads out of `refs/grid/*` and a plain copy has no object store to read
# them from), gate 2 reads that tree, and `nodes/` and the grid are written only
# once the gate has passed.


GHOST_NODE = ('---\nid: "build:ghost"\ntype: build\nlevel: 3\n'
              'payload_ref: extensions/agi/bin/ghost.py\n---\n\nbody\n')

NEW_PAYLOAD = "import json\n\n\ndef fresh():\n    return json.dumps({})\n"


def _nodes_digest(root: Path) -> str:
    """A hash of every byte under `nodes/`. `git status` is not enough here —
    the claim is byte-identical, and a rewrite that happens to restore the same
    text is a different fact from never having written."""
    import hashlib
    h = hashlib.sha256()
    for p in sorted((root / "nodes").rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(root)).encode())
            h.update(b"\0")
            h.update(p.read_bytes())
            h.update(b"\0")
    return h.hexdigest()


def _grid_tips(root: Path) -> dict[str, str]:
    out = _git_out(root, "for-each-ref", "refs/grid", "--format=%(refname) %(objectname)")
    return dict(line.split() for line in out.splitlines() if line)


def _scratch_dirs(tmproot: Path | None = None) -> int:
    root = tmproot if tmproot is not None else Path(os.environ.get("TMPDIR", "/tmp"))
    return len(list(root.glob("agi-publish-derive.*")))


def _hermetic_tmp_env(tmp_path: Path) -> tuple[Path, dict]:
    """A private TMPDIR for one test, so its agi-publish-*.XXXXXX scratch-dir
    count can never be perturbed by another concurrent process's own call
    (publish-engine.sh's mktemp already guarantees globally-unique names --
    the flake this fixes was purely a shared-glob COUNT racing against
    unrelated concurrent activity, never a real name collision; both
    tmproot derivations in publish-engine.sh (_scratch_tmp_root and the
    plain fallback path) honor $TMPDIR, so this makes the whole scratch tree
    private, not just the count-check)."""
    scratch_tmp = tmp_path / "scratch-tmp"
    scratch_tmp.mkdir()
    return scratch_tmp, {**os.environ, "TMPDIR": str(scratch_tmp)}


def test_a_contracts_disagree_refusal_leaves_nodes_byte_identical(tmp_path):
    """The 184 junk nodes, in miniature. `build:ghost` claims a payload that is
    in neither the engine nor the grid, so gate 2 refuses — and `nodes/` must
    come out of that run exactly as it went in."""
    project, engine = _pair(tmp_path, extra_nodes={"ghost": GHOST_NODE})
    before = _nodes_digest(project)

    r = _publish(project, engine)

    assert r.returncode != 0, r.stdout + r.stderr
    assert _read_state(project)["last_run_reason"] == "contracts-disagree"
    assert _nodes_digest(project) == before
    assert _git_out(project, "status", "--porcelain", "--", "nodes/") == ""


def test_a_contracts_disagree_refusal_burns_no_grid_versions(tmp_path):
    """The other half of the junk. `grid.py commit --all` used to run *before*
    gate 2, so a refused run recorded a version for every node the derivation
    had just rewritten — history of a state that was thrown away."""
    project, engine = _pair(tmp_path, extra_nodes={"ghost": GHOST_NODE})
    before = _grid_tips(project)

    _publish(project, engine)

    assert _grid_tips(project) == before


def test_a_refusal_says_that_it_wrote_nothing(tmp_path):
    """"It refused" reads as "nothing happened" whether or not that is true, so
    the message has to be the one that is."""
    project, engine = _pair(tmp_path, extra_nodes={"ghost": GHOST_NODE})

    r = _publish(project, engine)

    assert "nothing written" in r.stdout
    assert _read_state(project)["last_run_detail"].endswith(
        "nodes/ and the grid are exactly as this run found them")


def test_the_scratch_worktree_never_survives_the_run(tmp_path):
    """This is the `:37` cron. One leaked worktree per hour is the same class
    of slow failure the whole goal exists to remove."""
    project, engine = _pair(tmp_path, extra_nodes={"ghost": GHOST_NODE})
    worktrees = _git_out(project, "worktree", "list")
    tmproot, env = _hermetic_tmp_env(tmp_path)
    leaked = _scratch_dirs(tmproot)

    _publish(project, engine, env=env)

    assert _git_out(project, "worktree", "list") == worktrees
    # hermetic now (private TMPDIR) -- see _hermetic_tmp_env
    assert _scratch_dirs(tmproot) == leaked


def test_the_derivation_never_touches_the_real_nodes_dir(tmp_path):
    """Sharper than the digest check: the *mtime* of every node file has to be
    untouched too, so a rewrite-with-identical-bytes cannot pass for a no-op."""
    project, engine = _pair(tmp_path, extra_nodes={"ghost": GHOST_NODE})
    before = {p: p.stat().st_mtime_ns
              for p in sorted((project / "nodes").rglob("*.md"))}

    _publish(project, engine)

    assert {p: p.stat().st_mtime_ns
            for p in sorted((project / "nodes").rglob("*.md"))} == before


def test_the_happy_path_still_applies_publishes_and_commits(tmp_path):
    """Holding the derivation back is only correct if it still lands when the
    gate passes. The engine lags the graph here, so there is something to
    publish and the run cannot pass by doing nothing."""
    project, engine = _pair(tmp_path, staged=True)
    engine_head = _git_out(engine, "rev-parse", "HEAD")
    graph_commit = _git_out(project, "rev-parse", "--short", "HEAD")

    r = _publish(project, engine)

    assert r.returncode == 0, r.stdout + r.stderr
    assert _git_out(engine, "rev-parse", "HEAD") != engine_head
    assert graph_commit in _git_out(engine, "log", "-1", "--format=%B")
    assert (engine / "extensions/agi/bin/foo.py").read_text() == \
        PAIR_FILES["extensions/agi/bin/foo.py"]
    assert _git_out(engine, "status", "--porcelain") == ""
    state = _read_state(project)
    assert state["last_run_status"] == "ok"
    assert state["last_success_graph_commit"] == graph_commit


def test_a_successful_run_applies_the_derivations_prunes_too(tmp_path):
    """The apply has a delete half. A `build-scan` node whose payload exists
    nowhere is pruned by `level3.py` — in the scratch tree, so the pruning only
    reaches `nodes/` on the success path, and it does still reach it."""
    stale = ('---\nid: "build:bin-gone"\ntype: build\nlevel: 3\n'
             'origin: build-scan\npayload_ref: extensions/agi/bin/gone.py\n'
             '---\n\nbody\n')
    project, engine = _pair(tmp_path, extra_nodes={"bin-gone": stale}, staged=True)
    assert (project / "nodes" / "build" / "bin-gone.md").is_file()

    r = _publish(project, engine)

    assert r.returncode == 0, r.stdout + r.stderr
    assert not (project / "nodes" / "build" / "bin-gone.md").exists()


def test_a_file_authored_under_payloads_still_publishes(tmp_path):
    """goal:g6.1's deadlock, which holding the derivation back would otherwise
    reintroduce. A file written under `payloads/` is in neither the engine nor
    the grid, so the node minted for it reads as `missing_payload` — real drift
    by stitch's definition. If that node stayed in the scratch it would never
    reach `nodes/`, so the `*/5` grid cron would never see it, so its payload
    would never enter the grid, so the gate would refuse again next hour,
    forever. A newly minted node is adopted before the gate is retried."""
    project, engine = _pair(tmp_path, staged=True)
    fresh = project / "payloads" / "extensions" / "agi" / "bin" / "fresh.py"
    fresh.write_text(NEW_PAYLOAD, encoding="utf-8")

    r = _publish(project, engine)

    assert r.returncode == 0, r.stdout + r.stderr
    assert (project / "nodes" / "build" / "bin-fresh.md").is_file()
    assert (engine / "extensions/agi/bin/fresh.py").read_text() == NEW_PAYLOAD
    assert _read_state(project)["last_run_status"] == "ok"


def test_a_newly_minted_node_is_all_a_refusal_may_leave(tmp_path):
    """The one deliberate exception, held to its exact size. When a new payload
    file and real drift arrive together the new node is adopted (see above) and
    the run still refuses — and the adopted node, with its own first grid
    version, is the *whole* of what is left behind. No re-derived bodies."""
    project, engine = _pair(tmp_path, extra_nodes={"ghost": GHOST_NODE}, staged=True)
    fresh = project / "payloads" / "extensions" / "agi" / "bin" / "fresh.py"
    fresh.write_text(NEW_PAYLOAD, encoding="utf-8")
    tips = _grid_tips(project)

    r = _publish(project, engine)

    assert r.returncode != 0
    assert _read_state(project)["last_run_reason"] == "contracts-disagree"
    assert _git_out(project, "status", "--porcelain", "--", "nodes/").splitlines() == \
        ["?? nodes/build/bin-fresh.md"]
    new_refs = set(_grid_tips(project)) - set(tips)
    assert len(new_refs) == 1
    assert not {r for r in tips if tips[r] != _grid_tips(project).get(r)}


def test_dry_run_writes_neither_nodes_nor_grid_versions(tmp_path):
    """`--dry-run` is a report. It now builds a whole scratch tree to make one,
    which is a new set of ways for it to stop being one."""
    project, engine = _pair(tmp_path, staged=True)
    tmproot, env = _hermetic_tmp_env(tmp_path)
    nodes, tips, leaked = (_nodes_digest(project), _grid_tips(project),
                           _scratch_dirs(tmproot))
    worktrees = _git_out(project, "worktree", "list")

    r = _publish(project, engine, "--dry-run", env=env)

    assert r.returncode == 0, r.stdout + r.stderr
    assert _nodes_digest(project) == nodes
    assert _grid_tips(project) == tips
    assert not (project / STATE_REL).exists()
    assert _git_out(engine, "status", "--porcelain") == ""
    assert _git_out(project, "worktree", "list") == worktrees
    # hermetic now (private TMPDIR) -- see _hermetic_tmp_env
    assert _scratch_dirs(tmproot) == leaked


def test_dry_run_does_not_adopt_a_newly_minted_node(tmp_path):
    """The adoption is a write, so a dry pass may not do it — and must say so
    rather than report a block a real run would have cleared."""
    project, engine = _pair(tmp_path, staged=True)
    fresh = project / "payloads" / "extensions" / "agi" / "bin" / "fresh.py"
    fresh.write_text(NEW_PAYLOAD, encoding="utf-8")

    r = _publish(project, engine, "--dry-run")

    assert r.returncode != 0
    assert not (project / "nodes" / "build" / "bin-fresh.md").exists()
    assert "would be applied and" in r.stdout


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
