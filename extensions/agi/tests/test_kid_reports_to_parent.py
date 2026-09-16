"""hypothesis:l4-a-kid-reports-to-its-parent-and-the-seat-hears-one-dm-per-round.

The four conjuncts, driven against the REAL `cli._alarm_dispatcher_on_done`
and the REAL `send.py` entry gate on a temp project with a temp session
manifest:

  1. A kid's completion goes to its PARENT (`spawned_by_agent`), never the
     dispatching seat, and the completion line is appended to the kid's own
     manifest entry as `report`.
  2. A parent's own `done` sends exactly ONE dm to its dispatcher seat, whose
     body carries accepted/demoted/failed counts, the kid node ids and the
     branch tip.
  3. `send.py send <not-my-parent>` from a kid is refused (non-zero, one
     line, nothing written); `send.py send <parent>` still works.
  4. (brief text is asserted in test_brief.py; the prompts are prose.)

No live pane is ever nudged: `send._nudge_window` is replaced with a no-op
for every test here, so the assertions read the INBOX FILE, never tmux.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import locations  # noqa: E402


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


cli = _load("cli")
send_mod = _load("send")

ITER = "L9.001"
SEAT = "seat-director"
PARENT = "a00-parent-1"


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A scratch repo with a scratch `.agi` graph, no git required yet."""
    root = tmp_path / "project"
    graph = root / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (graph / "sessions").mkdir(parents=True)
    return root


@pytest.fixture
def graph(project: Path) -> Path:
    return project / ".agi"


@pytest.fixture(autouse=True)
def _no_pane(monkeypatch):
    """NO LIVE TMUX PANE IS EVER NUDGED. `send` delivers to the inbox file;
    the wake is suppressed, so every assertion below reads bytes on disk."""
    monkeypatch.setattr(send_mod, "_nudge_window",
                        lambda *a, **k: None, raising=False)
    yield


def _iter_dir(graph: Path) -> Path:
    return locations.iteration_dir(graph, ITER)


def _write_manifest(graph: Path, rows: list[dict]) -> None:
    it = _iter_dir(graph)
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({"agents": rows}, indent=2))


def _read_manifest(graph: Path) -> dict:
    return json.loads((_iter_dir(graph) / "manifest.json").read_text())


def _write_agent_record(graph: Path, agent_id: str, spawned_by: str | None,
                        **extra) -> None:
    d = _iter_dir(graph) / agent_id
    d.mkdir(parents=True, exist_ok=True)
    rec = {"id": agent_id, "spawned_by_agent": spawned_by}
    rec.update(extra)
    (d / "agent.json").write_text(json.dumps(rec))


def _inbox(graph: Path, who: str) -> Path:
    return graph / "sessions" / "inbox" / f"{who}.md"


# --------------------------------------------------------------------------
# 1. a kid's completion goes to its parent, never the seat
# --------------------------------------------------------------------------

def test_kid_completion_dms_parent_and_records_report(graph, monkeypatch
                                                      ):
    """N kids -> 0 seat dms, 1 dm each to the parent, `report` on each entry."""
    kids = [("a00-kid-1", "experiment:k1", "proved"),
            ("a00-kid-2", "experiment:k2", "pending")]
    rows = [{"id": k, "status": "done", "node_id": n,
             "spawned_by_agent": PARENT, "dispatched_by": SEAT}
            for k, n, _ in kids]
    _write_manifest(graph, rows)
    monkeypatch.setattr(cli, "_session_root", lambda: graph)

    for kid, node, verdict in kids:
        monkeypatch.setenv("AGI_TIER", "kid")
        monkeypatch.setenv("AGI_AGENT_ID", kid)
        cli._alarm_dispatcher_on_done(graph, ITER, kid, node, verdict)

    assert not _inbox(graph, SEAT).exists(), \
        "a kid must never wake the dispatching seat"
    parent_inbox = _inbox(graph, PARENT)
    assert parent_inbox.is_file(), "the parent heard nothing"
    text = parent_inbox.read_text()
    assert text.count("from:") == len(kids), text
    for kid, node, verdict in kids:
        assert f"agent={kid}" in text
        assert f"node={node}" in text
        assert f"verdict={verdict}" in text

    manifest = _read_manifest(graph)
    by_id = {a["id"]: a for a in manifest["agents"]}
    for kid, node, verdict in kids:
        assert by_id[kid]["report"] == (
            f"iter={ITER} agent={kid} node={node} verdict={verdict}")


def test_kid_without_parent_stamp_warns_and_keeps_old_behaviour(
        graph, monkeypatch, capsys):
    """A pre-existing live round (no `spawned_by_agent`) keeps today's dm and
    prints exactly ONE stderr warning -- it must not crash or go silent."""
    _write_manifest(graph, [{"id": "a00-old-kid", "status": "done",
                             "dispatched_by": SEAT}])
    monkeypatch.setattr(cli, "_session_root", lambda: graph)
    monkeypatch.setenv("AGI_TIER", "kid")
    monkeypatch.setenv("AGI_AGENT_ID", "a00-old-kid")

    cli._alarm_dispatcher_on_done(graph, ITER, "a00-old-kid",
                                  "experiment:old", "proved")

    err = capsys.readouterr().err
    assert err.count("no spawned_by_agent stamp") == 1
    assert _inbox(graph, SEAT).is_file(), "old behaviour falls back to seat"


# --------------------------------------------------------------------------
# 2. the parent harvest is exactly one seat dm carrying the shape
# --------------------------------------------------------------------------

def _git_repo_with_branch(root: Path, branch: str) -> str:
    def g(*a):
        return subprocess.run(["git", "-C", str(root), *a],
                              capture_output=True, text=True, check=True)
    g("init", "-q")
    g("config", "user.email", "t@example.invalid")
    g("config", "user.name", "t")
    (root / "seed.txt").write_text("seed\n")
    g("add", "seed.txt")
    g("commit", "-qm", "seed")
    g("branch", branch)
    return g("rev-parse", branch).stdout.strip()


def test_parent_harvest_is_one_seat_dm_with_the_shape(project, graph,
                                                      monkeypatch, capsys):
    branch = "loop/round-x"
    tip = _git_repo_with_branch(project, branch)
    rows = [
        {"id": PARENT, "status": "running", "dispatched_by": SEAT,
         "branch": branch},
        {"id": "a00-kid-1", "status": "done", "node_id": "experiment:k1",
         "spawned_by_agent": PARENT},
        {"id": "a00-kid-2", "status": "failed", "node_id": "experiment:k2",
         "spawned_by_agent": PARENT},
    ]
    _write_manifest(graph, rows)
    monkeypatch.setattr(cli, "_session_root", lambda: graph)
    monkeypatch.setenv("AGI_TIER", "parent")
    monkeypatch.setenv("AGI_AGENT_ID", PARENT)

    cli._alarm_dispatcher_on_done(graph, ITER, PARENT, None, "pending")

    inbox = _inbox(graph, SEAT)
    assert inbox.is_file(), "the seat heard nothing"
    text = inbox.read_text()
    assert text.count("from:") == 1, "a parent sends exactly ONE seat dm"
    capsys.readouterr()
    assert "accepted=1 demoted=0 failed=1" in text, text
    assert "kids=[experiment:k1, experiment:k2]" in text, text
    assert f"tip={tip}" in text, text
    # a kid that never completed still cannot add a second seat dm
    assert text.count("from:") == 1


# --------------------------------------------------------------------------
# 3. the send.py gate: a kid may dm only its parent
# --------------------------------------------------------------------------

def test_kid_send_gate_refuses_foreign_target_and_allows_parent(
        project, graph, monkeypatch, capsys):
    _write_manifest(graph, [{"id": "a00-kid-1", "status": "running",
                             "spawned_by_agent": PARENT,
                             "dispatched_by": SEAT}])
    _write_agent_record(graph, "a00-kid-1", PARENT)
    monkeypatch.chdir(project)
    monkeypatch.setenv("AGI_TIER", "kid")
    monkeypatch.setenv("AGI_AGENT_ID", "a00-kid-1")

    rc = send_mod.main(["send", SEAT, "let me out"])
    err = capsys.readouterr().err
    assert rc != 0
    assert "REFUSED" in err
    assert "a00-kid-1" in err and PARENT in err and SEAT in err
    assert err.count("\n") == 1, repr(err)
    assert not _inbox(graph, SEAT).exists(), "refusal wrote an inbox"

    rc2 = send_mod.main(["send", PARENT, "here is my report"])
    assert rc2 == 0
    parent_inbox = _inbox(graph, PARENT)
    assert parent_inbox.is_file()
    assert "here is my report" in parent_inbox.read_text()


def test_kid_send_gate_allows_its_parent_via_to_flag(project, graph,
                                                     monkeypatch, capsys):
    """The `--to` dm path is gated the same way (same target, same refusal)."""
    _write_agent_record(graph, "a00-kid-1", PARENT)
    monkeypatch.chdir(project)
    monkeypatch.setenv("AGI_TIER", "kid")
    monkeypatch.setenv("AGI_AGENT_ID", "a00-kid-1")

    rc = send_mod.main(["send", "--to", SEAT, "sneak"])
    assert rc != 0
    assert "REFUSED" in capsys.readouterr().err


# --------------------------------------------------------------------------
# 4. R5: `send --room` is gated exactly like the dm paths
# --------------------------------------------------------------------------

def test_kid_send_room_is_refused_before_any_write(project, graph,
                                                   monkeypatch, capsys):
    """A room reaches every member, seats included -- so a kid may not post
    into ANY room. Refused (exit 3, nothing written) BEFORE the room write,
    and the same post from a non-kid tier is unaffected."""
    _write_agent_record(graph, "a00-kid-1", PARENT)
    monkeypatch.chdir(project)
    monkeypatch.setenv("AGI_AGENT_ID", "a00-kid-1")
    room_file = send_mod.comms_root(graph, None) / "room" / "quorum.md"

    monkeypatch.setenv("AGI_TIER", "kid")
    rc = send_mod.main(["send", "--room", "quorum", "let me out"])
    err = capsys.readouterr().err
    assert rc == 3
    assert "REFUSED" in err
    assert "room quorum" in err
    assert err.count("\n") == 1, repr(err)
    assert not room_file.exists(), "the room refusal wrote a room"

    monkeypatch.setenv("AGI_TIER", "parent")
    rc2 = send_mod.main(["send", "--room", "quorum", "an allowed post"])
    assert rc2 == 0
    assert room_file.is_file()
    assert "an allowed post" in room_file.read_text()


# --------------------------------------------------------------------------
# 5. R2: the LIVE two-manifest topology, driven through the REAL `cli.py done`
#
# `test_parent_harvest_is_one_seat_dm_with_the_shape` above puts the parent
# row and the kid rows in ONE manifest and calls
# `cli._alarm_dispatcher_on_done` directly -- so it passed even while the live
# two-manifest topology emitted NOTHING (the parent's row lives only in the
# DISPATCHER/MAIN manifest while the kid rows live in the parent's own
# worktree manifest). These two tests build that topology with a real git
# worktree and drive `cli.main(["done", ...])`, the real entrypoint.
# --------------------------------------------------------------------------

def _git(cwd: Path, *args):
    return subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True)


def _two_manifest_project(tmp_path: Path, parent_row: dict) -> tuple[Path, Path]:
    """MAIN carries the DISPATCHER manifest (the parent's row); a linked
    WORKTREE is the tree the parent runs in. Returns (main, worktree)."""
    main = tmp_path / "main"
    graph = main / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    it = locations.iteration_dir(graph, ITER)
    it.mkdir(parents=True)
    (it / "manifest.json").write_text(json.dumps({"agents": [parent_row]}))
    (graph / "nodes" / "seed.md").write_text("seed\n")
    _git(main, "init", "-q")
    _git(main, "config", "user.email", "t@example.invalid")
    _git(main, "config", "user.name", "t")
    _git(main, "add", "-A")
    _git(main, "commit", "-qm", "seed")
    wt = tmp_path / "parent-wt"
    added = _git(main, "worktree", "add", "-q", "-b", "round-x", str(wt))
    assert added.returncode == 0, added.stderr
    return main, wt


def _write_worktree_manifest(wt: Path, rows: list[dict]) -> None:
    it = locations.iteration_dir(wt / ".agi", ITER)
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({"agents": rows}))


def _write_parent_record(wt: Path) -> None:
    d = wt / ".agi" / "sessions" / locations.iteration_dirname(ITER) / PARENT
    d.mkdir(parents=True, exist_ok=True)
    (d / "agent.json").write_text(json.dumps(
        {"id": PARENT, "status": "running", "tier": "parent"}))


def _run_real_done(wt: Path, monkeypatch, capsys) -> int:
    """Drive the REAL `cli.main()` `done` entrypoint IN-PROCESS (by setting
    `sys.argv`, the way `cli.py` itself parses) so the autouse tmux guard and
    the `_nudge_window` no-op still apply -- a subprocess would bypass both
    and could reach a live pane."""
    monkeypatch.chdir(wt)
    monkeypatch.setenv("AGI_TIER", "parent")
    monkeypatch.setenv("AGI_AGENT_ID", PARENT)
    monkeypatch.setattr(sys, "argv", ["cli.py", "done", ITER, PARENT,
                                      "--verdict", "pending",
                                      "--confidence", "0.5",
                                      "--no-evidence-gate"])
    capsys.readouterr()
    rc = cli.main()
    captured = capsys.readouterr()
    assert rc == 0, captured.err
    return rc


def test_real_done_harvests_across_two_manifests(tmp_path, monkeypatch,
                                                 capsys):
    """The parent row is in MAIN's manifest, the kids are in the worktree's:
    the seat hears exactly ONE dm with the harvest shape."""
    parent_row = {"id": PARENT, "status": "running", "dispatched_by": SEAT,
                  "branch": "round-x"}
    main, wt = _two_manifest_project(tmp_path, parent_row)
    _write_worktree_manifest(wt, [
        {"id": "a00-kid-1", "status": "done", "node_id": "experiment:k1",
         "spawned_by_agent": PARENT},
        {"id": "a00-kid-2", "status": "failed", "node_id": "experiment:k2",
         "spawned_by_agent": PARENT},
    ])
    _write_parent_record(wt)

    _run_real_done(wt, monkeypatch, capsys)

    # the branch tip the dm names is the tip AFTER `done` -- a parent in a
    # linked worktree commits its round on the way out, so read it now.
    tip = _git(main, "rev-parse", "round-x").stdout.strip()

    # `send` resolves the inbox under the MAIN graph's `sessions/inbox`, the
    # shared room a seat reads -- not under the worktree it was called from.
    seat_inbox = main / ".agi" / "sessions" / "inbox" / f"{SEAT}.md"
    assert seat_inbox.is_file(), "the seat heard ZERO dms (the R1 defect)"
    text = seat_inbox.read_text()
    assert text.count("from:") == 1, "a parent sends exactly ONE seat dm"
    assert "accepted=1 demoted=0 failed=1" in text, text
    assert "kids=[experiment:k1, experiment:k2]" in text, text
    assert f"tip={tip}" in text, text


def test_real_done_zero_kids_is_still_exactly_one_seat_dm(tmp_path, monkeypatch,
                                                          capsys):
    """R3 zero-kids case: parent row in the dispatcher manifest, NO kids
    anywhere -> exactly one seat dm with accepted=0 demoted=0 failed=0, never
    a crash and never a second dm."""
    parent_row = {"id": PARENT, "status": "running", "dispatched_by": SEAT}
    main, wt = _two_manifest_project(tmp_path, parent_row)
    _write_worktree_manifest(wt, [])
    _write_parent_record(wt)

    _run_real_done(wt, monkeypatch, capsys)

    # `send` resolves the inbox under the MAIN graph's `sessions/inbox`, the
    # shared room a seat reads -- not under the worktree it was called from.
    seat_inbox = main / ".agi" / "sessions" / "inbox" / f"{SEAT}.md"
    assert seat_inbox.is_file(), "the seat heard nothing"
    text = seat_inbox.read_text()
    assert text.count("from:") == 1, "exactly ONE seat dm"
    assert "accepted=0 demoted=0 failed=0" in text, text
    assert "kids=[]" in text, text


# --------------------------------------------------------------------------
# 6. conjunct (4): the harvest names a measured overage against the record
#
# hypothesis:l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-
# for-a-parent-re-brief. The kid records `production_lines` / `line_ceiling`
# on its experiment node (conjunct 2); the harvest reads those fields off the
# node file and names an overage with no `rebrief_request` as a defect. It is
# a pure read -- no `git` runs here, because the parent already computes the
# kid's diff in its own prompt.
# --------------------------------------------------------------------------

def _write_kid_node(graph: Path, node_id: str, **fm) -> None:
    d = graph / "nodes" / "experiment"
    d.mkdir(parents=True, exist_ok=True)
    fields = {"id": node_id, "type": "experiment",
              "parents": "[hypothesis:x]"}
    fields.update(fm)
    body = "\n".join(f"{k}: {v}" for k, v in fields.items())
    (d / f"{node_id.split(':', 1)[1]}.md").write_text(
        f"---\n{body}\n---\nbody\n")


def _harvest_text(graph, monkeypatch, kid_node: str) -> str:
    _write_manifest(graph, [
        {"id": PARENT, "status": "running", "dispatched_by": SEAT,
         "branch": ""},
        {"id": "a00-kid-1", "status": "done", "node_id": kid_node,
         "spawned_by_agent": PARENT},
    ])
    monkeypatch.setattr(cli, "_session_root", lambda: graph)
    monkeypatch.setenv("AGI_TIER", "parent")
    monkeypatch.setenv("AGI_AGENT_ID", PARENT)
    cli._alarm_dispatcher_on_done(graph, ITER, PARENT, None, "pending")
    return _inbox(graph, SEAT).read_text()


def test_harvest_names_an_overage_with_no_rebrief(graph, monkeypatch, capsys):
    """Over 2x, no `rebrief_request` -> the exact named-defect token."""
    _write_kid_node(graph, "experiment:k-over",
                    production_lines=90, line_ceiling=40)
    text = _harvest_text(graph, monkeypatch, "experiment:k-over")
    capsys.readouterr()
    assert "overage=[experiment:k-over 90/40 no-rebrief]" in text, text
    assert "rebrief=" not in text, text


def test_harvest_names_a_rebrief_instead_of_an_overage(graph, monkeypatch,
                                                       capsys):
    """The SAME overage WITH a `rebrief_request` -> `rebrief=`, no defect."""
    _write_kid_node(graph, "experiment:k-over",
                    production_lines=90, line_ceiling=40,
                    rebrief_request="needs 80 lines")
    text = _harvest_text(graph, monkeypatch, "experiment:k-over")
    capsys.readouterr()
    assert "rebrief=[experiment:k-over 90/40]" in text, text
    assert "overage=" not in text, text


def test_harvest_is_unchanged_under_2x_or_with_no_record(graph, monkeypatch,
                                                         capsys):
    """Under 2x adds nothing; a pre-fix kid with no fields adds nothing --
    absent is not over-budget and no defect may be fabricated from it."""
    _write_kid_node(graph, "experiment:k-under",
                    production_lines=30, line_ceiling=40)
    under = _harvest_text(graph, monkeypatch, "experiment:k-under")
    capsys.readouterr()
    assert "overage=" not in under and "rebrief=" not in under, under
    assert "kids=[experiment:k-under]" in under, under

    _write_kid_node(graph, "experiment:k-bare")
    bare = _harvest_text(graph, monkeypatch, "experiment:k-bare")
    capsys.readouterr()
    assert "overage=" not in bare and "rebrief=" not in bare, bare
    assert "kids=[experiment:k-bare]" in bare, bare
