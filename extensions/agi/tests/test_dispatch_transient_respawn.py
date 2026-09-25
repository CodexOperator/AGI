"""Tests for hypothesis:l4-the-pi-runners-retry-a-transient-5xx-with-bounded-
backoff-logged-by-name-never-a-real-failure, conjunct (2): the DISPATCHER.

A kid that dies at its FIRST call, leaving ONLY pi's local catalogue warning
and a 5xx signature line in `output.log`, is a dead round nobody re-runs
(measured: iter-TM.07/a00-1fec07a8/output.log = two lines, no commit, no
node). The claim under test: dispatch polls a bounded startup grace after
Popen and re-spawns exactly that class of death under the SAME lease, agent
id, worktree and log, bounded at 3 attempts, naming each attempt in the log.

No live spawn, no network, no real sleep: `subprocess.Popen` is faked and the
grace/backoff seam `dispatch._GRACE_SLEEP` is a no-op.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

CATALOGUE = (b'Model "deepseek-v4" not found for provider "openrouter". '
             b'Using custom model id.\n')
DEAD_520 = b"error code: 520\n"


def _load_dispatch():
    spec = importlib.util.spec_from_file_location("agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()
_FX = _load_dispatch.__module__


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {"adapter": "pi", "provider": "fake",
                             "models": {"kid": "deepseek-v4"}}},
        "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 0, role: kid, "
        "harness: pi, model: deepseek-v4}\n---\nbody")
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR"):
        os.environ.pop(k, None)
    return tmp_path


class _StubProc:
    """A fake child: `poll()` returns None `left` times, then `rc` forever."""

    def __init__(self, pid, rc, left):
        self.pid = pid
        self._rc = rc
        self._left = left
        self.returncode = None

    def poll(self):
        if self._left <= 0:
            if self._rc is not None:
                self.returncode = self._rc
            return self.returncode
        self._left -= 1
        return None


def _fake_spawn(monkeypatch, plans):
    """Patch ONLY the spawn Popen (the one with `start_new_session=True`).

    `plans` is one dict per expected spawn, in order:
      bytes -> written to that spawn's log handle before the child is judged
      rc    -> the exit code the child eventually reports (None = never)
      left  -> number of `poll()` calls that see it alive first
    Returns the list of (argv, proc) actually spawned."""
    spawned = []
    real_popen = subprocess.Popen

    def _patched(argv, **kwargs):
        if not kwargs.get("start_new_session"):
            return real_popen(argv, **kwargs)
        plan = plans[len(spawned)] if len(spawned) < len(plans) else plans[-1]
        f = kwargs.get("stdout")
        if f is not None and plan.get("bytes"):
            f.write(plan["bytes"])
            f.flush()
        proc = _StubProc(1000 + len(spawned), plan.get("rc"), plan.get("left", 0))
        spawned.append((argv, proc))
        return proc

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_tmux_start", lambda *a, **kw: None)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    return spawned


def _argv(tmp_path: Path, *extra):
    return [str(BIN / "dispatch.py"), str(tmp_path), "1",
            "--level", "small", "--harness", "pi", "--tier", "kid",
            "--target", "hypothesis:x", *extra]


def _logs(root: Path):
    return sorted(root.glob(".agi/sessions/**/output.log"))


def test_transient_startup_death_is_respawned_and_named(
        project, monkeypatch, capsys):
    """(a) A child that dies rc 1 inside the grace leaving ONLY the catalogue
    warning + `error code: 520` is re-spawned under the SAME lease, agent id,
    worktree and log, with an `attempt 2` line appended; the second child is
    the one that ends up registered."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520, "rc": 1, "left": 0},
        {"bytes": b"", "rc": None, "left": 99},
    ])
    monkeypatch.setattr(sys, "argv", _argv(project))

    code = dispatch.main()
    assert code == 0, f"a rescued round must register and exit 0, got {code}"
    assert len(spawned) == 2, f"expected ONE re-spawn, got {len(spawned)}"
    # the SAME argv: same agent id, same worktree, same env, same lease
    assert spawned[0][0] == spawned[1][0], "re-spawn changed the command"

    logs = _logs(project)
    assert len(logs) == 1, f"re-spawn must reuse the SAME log: {logs}"
    text = logs[0].read_text()
    assert "attempt 2" in text, f"no by-name re-spawn line in the log:\n{text}"
    assert "error code: 520" in text or "520" in text, text

    agents = json.loads(
        (sorted(project.glob(".agi/sessions/**/manifest.json"))[0]).read_text()
    )["agents"]
    assert len(agents) == 1, f"exactly one round registered, got {agents}"
    assert agents[0]["pid"] == spawned[1][1].pid, \
        "the registered pid must be the RE-SPAWNED child"


def test_clean_exit_zero_inside_the_grace_is_never_respawned(
        project, monkeypatch, capsys):
    """(b) A child that exits 0 inside the grace takes today's path: exactly
    one Popen, no `attempt` line."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520, "rc": 0, "left": 1},
    ])
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert len(spawned) == 1, "rc 0 must never be re-spawned"
    assert "attempt 2" not in _logs(project)[0].read_text()


def test_a_child_alive_past_the_grace_is_never_touched(
        project, monkeypatch, capsys):
    """(c) A healthy child outliving the grace: exactly one Popen, no
    `attempt` line, dispatch returns as today."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520, "rc": None, "left": 999},
    ])
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert len(spawned) == 1, "a live child must never be re-spawned"
    assert "attempt 2" not in _logs(project)[0].read_text()


def test_a_non_transient_startup_death_is_not_respawned(
        project, monkeypatch, capsys):
    """The falsifier guard on the bytes: a child that died with anything else
    in its log (here a real thought) is never re-spawned."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520 + b"# kid: writing node\n", "rc": 1,
         "left": 0},
    ])
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert len(spawned) == 1, "a death after real output must not be retried"


def test_the_classifier_reads_only_whole_signature_logs(tmp_path):
    """The decision itself: ONLY non-empty signature lines => transient."""
    cat = tmp_path / "a.log"
    cat.write_bytes(CATALOGUE + DEAD_520)
    assert dispatch._startup_death_is_transient(cat)
    mixed = tmp_path / "b.log"
    mixed.write_bytes(CATALOGUE + b'{"stage": "x"}\n')
    assert dispatch._startup_death_is_transient(mixed) is None
    empty = tmp_path / "c.log"
    empty.write_bytes(b"\n\n")
    assert dispatch._startup_death_is_transient(empty) is None
    missing = tmp_path / "d.log"
    assert dispatch._startup_death_is_transient(missing) is None


def _deprecated_files(root: Path):
    dep = root / ".agi" / "nodes" / "deprecated"
    return [f for d in dep.glob("*") if d.is_dir() for f in d.glob("*.md")]


def test_transient_exhaustion_is_bounded_at_three_and_deprecates(
        project, monkeypatch, capsys):
    """item 3 + item 1: a child that ALWAYS dies transiently is re-spawned
    exactly `_GRACE_MAX_ATTEMPTS` (3) times and no more, then dispatch exits 5
    -- and the orphan scaffold that leaves behind (no agent record ever
    registered) is deprecated the same run, like every other seam."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520, "rc": 1, "left": 0},
    ])
    monkeypatch.setattr(dispatch, "_GRACE_BACKOFF_S", (0, 0))
    monkeypatch.setattr(sys, "argv", _argv(project))

    code = dispatch.main()
    assert code == 5, f"exhaustion must return rc 5, got {code}"
    assert len(spawned) == dispatch._GRACE_MAX_ATTEMPTS == 3, (
        f"expected exactly 3 spawns, got {len(spawned)}")
    assert _deprecated_files(project), (
        "an exhausted transient death must deprecate its orphan scaffold")


def _read_fm(path: Path):
    import graph_core.persistence.frontmatter as fm_reader
    return dict(fm_reader.load_node_file(path).frontmatter)


@pytest.fixture()
def parent_project(project: Path) -> Path:
    """A parent-capable variant of the scratch project: config carries a
    parent model and the ladder a tier-1 parent row, so a `--tier parent
    --orders` live spawn can write the orders copy the rc-5 exhaustion block
    is now proven to unlink. Every existing kid-tier test keeps its row."""
    cfg = json.loads((project / ".agi" / "config.json").read_text())
    cfg["harnesses"]["pi"]["models"]["parent"] = "glm-flash"
    (project / ".agi" / "config.json").write_text(json.dumps(cfg))
    (project / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n"
        "  - {tier: 1, role: parent, harness: pi, model: glm-flash}\n"
        "  - {tier: 0, role: kid, harness: pi, model: deepseek-v4}\n"
        "---\nbody")
    return project


def test_rc5_exhaustion_issue_line_names_the_death_and_keeps_id(
        project, monkeypatch, capsys):
    """The rc-5 exhaustion block reports `_report_unregistered_scaffold`
    (the died-transiently detail) BEFORE returning 5, and the deprecation
    keeps the scaffolded node's id (goal:g15.25 SM.28 -- UNTESTED BY NAME:
    the existing bounded test asserts rc 5 + deprecation but never reads the
    JSON issue line). A KID-tier spawn that always dies transiently is
    exhausted at 3 attempts; a scaffold exists (a kid's artefact is its own
    node), so the report+deprecate seam fires."""
    spawned = _fake_spawn(monkeypatch, [
        {"bytes": CATALOGUE + DEAD_520, "rc": 1, "left": 0},
    ])
    monkeypatch.setattr(dispatch, "_GRACE_BACKOFF_S", (0, 0))
    monkeypatch.setattr(sys, "argv", _argv(project))

    code = dispatch.main()
    assert code == 5, f"exhaustion must return rc 5, got {code}"
    assert len(spawned) == dispatch._GRACE_MAX_ATTEMPTS == 3, (
        f"expected exactly 3 attempts, got {len(spawned)}")

    issue = [json.loads(l) for l in capsys.readouterr().out.splitlines()
             if l.lstrip().startswith("{")]
    assert issue, "rc-5 must emit the named JSON issue line"
    assert issue[0]["issue"] == "scaffolded-but-unregistered", issue
    assert "died transiently" in issue[0]["detail"], issue[0]["detail"]
    node_id = issue[0]["node_id"]

    moved = _deprecated_files(project)
    assert moved, f"scaffold {node_id} not deprecated"
    fm = _read_fm(moved[0])
    assert fm.get("status") == "deprecated", fm
    assert fm.get("id") == node_id, (
        f"deprecated node must keep its own id (never re-minted): {fm}")


def test_rc5_exhaustion_unlinks_the_orders_copy(
        parent_project, tmp_path, monkeypatch, capsys):
    """The rc-5 exhaustion block unlinks the orders copy before `return 5`
    (goal:g15.25 SM.28 -- the OTHER UNTESTED-BY-NAME residue). The orders
    copy only writes on the PARENT tier, and a parent scaffolds no node (a
    parent's artefact is its kids' nodes, goal:s27) -- so the orders-unlink
    branch is driven here by exhaustively transiently dying parent spawns,
    and the issue-line/deprecate seam is driven by the kid test above."""
    orders = tmp_path / "orders.md"
    orders.write_text("SCOPE: touch only dispatch.py\n")

    # capture whether the orders copy exists at the moment of the FIRST
    # Popen: the copy is written BEFORE the spawn, so its presence there
    # proves the later "no orders.* left" assert is about the UNLINK, not
    # about a branch that skipped the write.
    wrote_before_spawn = {}
    spawned = []
    real_popen = subprocess.Popen

    def _patched(argv, **kwargs):
        if not kwargs.get("start_new_session"):
            return real_popen(argv, **kwargs)
        if not spawned:
            iter_dir = parent_project / ".agi" / "sessions" / "iter-001"
            wrote_before_spawn["present"] = sorted(iter_dir.glob("orders.*"))
        f = kwargs.get("stdout")
        if f is not None:
            f.write(CATALOGUE + DEAD_520)
            f.flush()
        spawned.append(argv)
        return _StubProc(1000 + len(spawned), 1, 0)  # always-dying child

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_tmux_start", lambda *a, **kw: None)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.setattr(dispatch, "_GRACE_BACKOFF_S", (0, 0))
    monkeypatch.setattr(sys, "argv", _argv(
        parent_project, "--tier", "parent",
        "--orders", str(orders), "--from", "sanctuary-director"))

    code = dispatch.main()
    assert code == 5, f"exhaustion must return rc 5, got {code}"
    assert len(spawned) == dispatch._GRACE_MAX_ATTEMPTS == 3, (
        f"expected exactly 3 attempts, got {len(spawned)}")
    assert wrote_before_spawn.get("present"), (
        "the orders copy was never written before the spawn; the unlink has "
        "nothing to prove")

    iter_dir = parent_project / ".agi" / "sessions" / "iter-001"
    leftovers = sorted(iter_dir.glob("orders.*"))
    assert leftovers == [], (
        f"rc-5 exhaustion left an orders copy: {leftovers}")
