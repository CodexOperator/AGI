"""hypothesis:l4-spawn-cds-into-the-row-worktree-cell-when-set.

A seated `cmd_spawn` must launch the successor in the seat ROW's `worktree`
cell (relative to graph_root, absolute used as-is) instead of the spawner
process cwd. Every non-seated path must stay byte-for-byte today's line.

The assertions read the WIRE: the tmux argv `subprocess.run` receives (via
`_launch_window`) and the `cwd` kwarg `spawn_window` receives (via
`cmd_spawn`). An assertion on a helper we wrote is not an assertion on the
launch line.
"""
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate


def _seats_sheet(root, rows):
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (g / "seats.md").write_text(body, encoding="utf-8")


def _spawn_args(seat="director-seat", wins=None):
    return SimpleNamespace(
        name=seat, tier="kid", prompt_file=None, model=None, effort=None,
        settings=None, tmux_session="agi-rc", window_path=wins,
        dry_run=False, successor_argv=None, seat=seat, pid=None,
        no_autopsy=True, registry_dir=None, harness=None,
    )


@pytest.fixture
def spawned(monkeypatch):
    """Capture every `spawn_window` invocation and stub the two side effects
    that would otherwise need the live graph (first seating, window probe)."""
    calls = []

    def fake_spawn_window(**kw):
        calls.append(kw)
        return 0, "echo ok"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn_window)
    monkeypatch.setattr(rotate, "_existing_windows", lambda *a, **k: [])
    monkeypatch.setattr(rotate, "_first_seating_run",
                        lambda *a, **k: ("", []))
    return calls


# ---- the wire: _launch_window argv -------------------------------------- #

def test_launch_window_cwd_is_the_cd_target(monkeypatch, tmp_path):
    seen = []
    monkeypatch.setattr(rotate.subprocess, "run",
                        lambda argv, **kw: seen.append(argv)
                        or SimpleNamespace(returncode=0, stderr="",
                                           stdout=""))
    wd = tmp_path / "somewhere-else"
    wd.mkdir()
    assert rotate._launch_window("sess", "n", "echo hi", cwd=str(wd)) == 0
    assert f"cd {wd} && echo hi" == seen[-1][-1], seen[-1]
    # None keeps today's line byte-for-byte: the spawner process cwd.
    assert rotate._launch_window("sess", "n", "echo hi") == 0
    assert f"cd {os.getcwd()} && echo hi" == seen[-1][-1], seen[-1]


def test_spawn_window_threads_cwd_to_launcher(monkeypatch):
    seen = []
    monkeypatch.setattr(rotate, "_existing_windows", lambda *a, **k: [])
    monkeypatch.setattr(rotate, "_launch_window",
                        lambda s, n, c, **kw: seen.append(kw) or 0)
    rc, _ = rotate.spawn_window(name="x", tier="kid", prompt_file=None,
                                successor_argv="echo hi", cwd="/tmp/wtx")
    assert rc == 0 and seen[-1].get("cwd") == "/tmp/wtx"
    rotate.spawn_window(name="x", tier="kid", prompt_file=None,
                        successor_argv="echo hi")
    assert seen[-1].get("cwd") is None


# ---- cmd_spawn: row cell resolution ------------------------------------- #

def test_spawn_absolute_worktree_cell_launches_there(tmp_path, spawned):
    wt = tmp_path / "abs-post"
    wt.mkdir()
    _seats_sheet(tmp_path, [{"name": "director-seat", "role": "director",
                             "worktree": str(wt)}])
    assert rotate.cmd_spawn(_spawn_args(), tmp_path) == 0
    assert spawned[-1]["cwd"] == str(wt), spawned[-1]


def test_spawn_relative_worktree_cell_resolves_against_git_common_root(
        tmp_path, spawned, monkeypatch):
    # A RELATIVE cell is resolved against git_common_root(root) -- NOT root
    # itself, NOT os.getcwd(). Point the two at different dirs so a wrong
    # resolver fails loudly.
    main = tmp_path / "main-checkout"
    cell = Path(".agi") / "worktrees" / "post-sensei-director"
    (main / cell).mkdir(parents=True)
    monkeypatch.setattr(rotate.locations, "git_common_root",
                        lambda r: main)
    _seats_sheet(tmp_path, [{"name": "director-seat", "role": "director",
                             "worktree": str(cell)}])
    assert rotate.cmd_spawn(_spawn_args(), tmp_path) == 0
    assert spawned[-1]["cwd"] == str(main / cell), spawned[-1]


def test_spawn_empty_worktree_cell_keeps_todays_cwd(tmp_path, spawned):
    _seats_sheet(tmp_path, [{"name": "director-seat", "role": "director"}])
    assert rotate.cmd_spawn(_spawn_args(), tmp_path) == 0
    assert spawned[-1]["cwd"] is None, spawned[-1]


def test_spawn_missing_worktree_dir_falls_back_and_says_so(
        tmp_path, spawned, capsys):
    _seats_sheet(tmp_path, [{"name": "director-seat", "role": "director",
                             "worktree": "nope/does-not-exist"}])
    assert rotate.cmd_spawn(_spawn_args(), tmp_path) == 0
    assert spawned[-1]["cwd"] is None, spawned[-1]
    err = capsys.readouterr().err
    assert "[seating] worktree cell 'nope/does-not-exist'" in err, err
