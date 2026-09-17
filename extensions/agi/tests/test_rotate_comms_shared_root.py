# test_rotate_comms_shared_root.py -- L5.18
# hypothesis:l5-rename-post-staged-from-main-root-derives-main-comms-paths-
# for-a-worktree-post. Pre-fix, rename-post staged from MAIN enumerated the
# MAIN checkout's comms/season-*/dm/ while the boundary applied from the
# post's own worktree enumerated the WORKTREE's comms/ -- different tables,
# so _apply_staged refused the stage as drift (rc 2). The fix roots the dm
# walk at send.comms_root (ONE room per season on the MAIN checkout).
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


def _git(cwd, *args):
    subprocess.run(["git", "-C", str(cwd), *args], check=True,
                   capture_output=True, text=True)


def _seats(graph):
    geo = graph / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "seats.md").write_text(
        '---\nid: config:seats\nseats:\n  - '
        + json.dumps({"name": "old", "role": "kid"}, sort_keys=True)
        + '\n---\n# body\n', encoding="utf-8")


def _main_repo(tmp_path):
    """A real git repo whose `.agi/` graph is committed, so a linked worktree
    checks out the SAME seats/sessions but has its OWN (stale) comms/."""
    repo = tmp_path / "main"
    repo.mkdir()
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    graph = repo / ".agi"
    graph.mkdir()
    (graph / "config.json").write_text("{}", encoding="utf-8")
    _seats(graph)
    for parent, name in [("seats", "old.key"), ("quorum", "old.md"),
                         ("inbox", "old.md")]:
        p = graph / "sessions" / parent
        p.mkdir(parents=True, exist_ok=True)
        (p / name).write_text("x\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init graph")
    return repo, graph


def test_boundary_apply_from_worktree_finds_the_main_dm_room(tmp_path):
    """Stage from MAIN, apply the boundary from the post's own worktree: the
    SHARED comms room is the only one either may enumerate, so the fresh
    table matches the stage and the apply succeeds (rc 0). Pre-fix the
    worktree's own comms/ has no dm file, the stage drifts, and _apply_staged
    returns 2 with `staged plan drifted`."""
    repo, graph = _main_repo(tmp_path)
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "--detach", str(wt), "master")
    wt_graph = wt / ".agi"
    assert not (wt_graph / "comms").exists()  # the worktree's stale/empty room

    cdir = graph / "comms" / "season-1" / "dm"
    cdir.mkdir(parents=True)
    log = cdir / "buddy--old.md"
    log.write_text("hi\n", encoding="utf-8")
    side = cdir / "buddy--old.md.state.json"
    side.write_text(json.dumps({"old": 1, "other": 2}), encoding="utf-8")

    ns = argparse.Namespace(old_name="old", new_name="new", dry_run=False,
                            now=False, apply=False, root=None)
    assert rotate.cmd_rename_post(ns, graph) == 0
    assert (graph / "sessions" / "seats" / "old.rename.json").exists()

    assert rotate._apply_staged(wt_graph, "old", "new") == 0
    assert (cdir / "buddy--new.md").exists()
    assert not log.exists()
    data = json.loads((cdir / "buddy--new.md.state.json").read_text())
    assert "new" in data and "old" not in data
    assert not (graph / "sessions" / "seats" / "old.rename.json").exists()


def test_dm_walk_is_rooted_at_the_shared_comms_resolver(tmp_path, monkeypatch):
    """The worktree's own comms/ must never contribute a dm surface: with a
    dm file planted ONLY in the worktree, a boundary re-derivation from the
    worktree lists nothing for it (the shared room is what is read)."""
    repo, graph = _main_repo(tmp_path)
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "--detach", str(wt), "master")
    wt_graph = wt / ".agi"

    stale = wt_graph / "comms" / "season-1" / "dm"
    stale.mkdir(parents=True)
    (stale / "buddy--old.md").write_text("stale wt copy\n", encoding="utf-8")

    assert [s for s in rotate._dm_participants(wt_graph, "old", "new")] == []


def test_stage_main_apply_worktree_agrees_on_rotations_prose_and_alerts(tmp_path):
    """L5.18 kid 2: the rename surface table's rotations.md-derived rows (the
    prose `mention` rows AND the alerts.edges/audit/silent rows) must resolve
    from the SHARED graph root, so a worktree whose rotations.md is stale
    (cut BEFORE MAIN committed the line) can no longer split stage from
    boundary. Pre-fix the boundary re-derives zero rotations/alerts rows and
    refuses the stage as drift (rc 2)."""
    from agi.bin import locations
    repo, graph = _main_repo(tmp_path)
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "--detach", str(wt), "master")
    wt_graph = wt / ".agi"
    # MAIN commits a rotations.md mentioning `old` AFTER the worktree was cut
    geo = graph / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "rotations.md").write_text(
        "---\nid: config:rotations\n"
        'alerts: {"audit": ["old"], "edges": {"old": ["old"]}, "silent": []}\n'
        "---\n# body\nrotate old post\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "rotations mention")
    assert not (wt_graph / "nodes" / ".geometry" / "rotations.md").exists()

    ns = argparse.Namespace(old_name="old", new_name="new", dry_run=False,
                            now=False, apply=False, root=None)
    assert rotate.cmd_rename_post(ns, graph) == 0
    assert (graph / "sessions" / "seats" / "old.rename.json").exists()
    assert rotate._apply_staged(wt_graph, "old", "new") == 0
    assert not (graph / "sessions" / "seats" / "old.rename.json").exists()


def test_gate_still_refuses_a_genuinely_new_mention_after_staging(tmp_path):
    """Falsifier guard for the L5.18 kid-2 fix: routing rotations.md through
    the shared root must NOT weaken the drift gate. A mention MAIN adds
    AFTER the stage was written is a genuinely new surface and must still be
    refused (rc 2), stage left intact."""
    repo, graph = _main_repo(tmp_path)
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "--detach", str(wt), "master")
    wt_graph = wt / ".agi"
    geo = graph / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    rot = geo / "rotations.md"
    rot.write_text("---\nid: config:rotations\n---\n# body\nrotate old post\n",
                   encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "rotations mention")

    ns = argparse.Namespace(old_name="old", new_name="new", dry_run=False,
                            now=False, apply=False, root=None)
    assert rotate.cmd_rename_post(ns, graph) == 0
    # MAIN gains a SECOND mention after the stage was written
    rot.write_text(rot.read_text() + "and old again\n", encoding="utf-8")
    assert rotate._apply_staged(wt_graph, "old", "new") == 2
    assert (graph / "sessions" / "seats" / "old.rename.json").exists()
