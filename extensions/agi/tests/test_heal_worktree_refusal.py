"""hypothesis:heal-never-reseats-a-worktree-post-into-main, defects (1)+(2).

heal's reseat of a dead seat must NEVER answer a worktree row with MAIN's
geometry, and must NEVER retry the launcher without `cwd`:

  (1) `_seat_geometry_dir` REFUSES (returns None) when a row CLAIMS a worktree
      whose own `.agi` does not exist, instead of silently handing back MAIN —
      which is what reseats a post INTO MAIN's nodes/, sessions/, quorum card
      and rotation state. `_recover_seat` then refuses by name and launches
      NOTHING; a main-checkout row (empty `worktree` cell) is unchanged.
  (2) the `except TypeError` no-cwd retry is reachable ONLY for the one
      signature it was written for — a pre-cwd launcher seam
      `launch(root, name, shell_cmd, window_path)` whose TypeError names the
      unexpected `cwd` keyword. ANY other TypeError (one raised INSIDE a
      correct, cwd-aware launcher) is refused, and a WORKTREE post refuses the
      no-cwd retry outright.

Fixture shape: a REAL worktree-shaped root (`<main>/.agi` plus
`<main>/.agi/worktrees/<name>/.agi`), driven through the real
`_watch_seats` pass with a fake launcher — never a real model, never tmux.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")

SEAT = "wt"
WT_CELL = ".agi/worktrees/seat-wt"
ROW = {"name": SEAT, "pid": 424242, "window": "@50", "role": "director",
       "model": "claude-sonnet-5", "generation": 2, "worktree": WT_CELL,
       "recover": True}


def _write_seats(graph: Path, rows: list[dict]) -> None:
    p = graph / "nodes" / ".geometry" / "seats.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:seats", "seats:"]
    lines += ["  - " + json.dumps(r) for r in rows]
    lines.append("---")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _worktree_root(tmp_path: Path, *, worktree: bool) -> tuple[Path, Path]:
    """A REAL worktree-shaped graph root. `worktree=False` is the same root
    with the worktree dir REMOVED — the shape a pruned worktree leaves."""
    main = tmp_path / "main"
    gdir = main / ".agi"
    (gdir / "sessions" / "quorum").mkdir(parents=True, exist_ok=True)
    (gdir / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    (gdir / "windows.txt").write_text("", encoding="utf-8")
    _write_seats(gdir, [dict(ROW)])
    wt_agi = gdir / "worktrees" / "seat-wt" / ".agi"
    wt_agi.mkdir(parents=True, exist_ok=True)
    _write_seats(wt_agi, [dict(ROW)])
    (wt_agi / "sessions" / "quorum").mkdir(parents=True, exist_ok=True)
    (wt_agi / "sessions" / "quorum" / f"{SEAT}.md").write_text(
        "# SESSION HANDOFF wt\nOWN-WORKTREE\n", encoding="utf-8")
    (gdir / "sessions" / "quorum" / f"{SEAT}.md").write_text(
        "# SESSION HANDOFF wt\nMAIN-STALE\n", encoding="utf-8")
    if not worktree:
        import shutil
        shutil.rmtree(gdir / "worktrees" / "seat-wt")
    return gdir, wt_agi


def _never_launcher(seen):
    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append({"cwd": cwd, "cmd": shell_cmd})
        return 515151, "@777"
    return launch


# --- (1) the geometry resolver REFUSES instead of falling back to MAIN -----

def test_seat_geometry_dir_refuses_a_claimed_worktree_with_no_geometry(tmp_path):
    """The same REAL worktree-shaped root, before and after the worktree dir
    is REMOVED (what a pruned worktree leaves): present -> its own `.agi`;
    removed -> None (never MAIN). A row with an empty `worktree` cell is a real
    main-checkout seat and keeps MAIN, which is correct for it."""
    import shutil
    gdir, wt_agi = _worktree_root(tmp_path, worktree=True)
    assert heal._seat_geometry_dir(gdir, ROW) == wt_agi
    shutil.rmtree(gdir / "worktrees" / "seat-wt")
    assert not (gdir / "worktrees" / "seat-wt").exists()
    assert heal._seat_geometry_dir(gdir, ROW) is None, \
        "a claimed-but-missing worktree must NOT be answered with MAIN's geometry"
    assert heal._seat_geometry_dir(gdir, {"worktree": ""}) == gdir, \
        "an empty worktree cell is a main-checkout seat: MAIN is correct"


def test_watch_seats_refuses_by_name_and_launches_nothing(tmp_path,
                                                          monkeypatch):
    """The end-to-end proof: a dead worktree seat whose worktree dir is gone
    is NAMED with the missing path in the watch log + the outcome, and the
    launcher is NEVER called (no launch, no MAIN card, no MAIN geometry)."""
    gdir, _ = _worktree_root(tmp_path, worktree=False)
    log = tmp_path / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    seen: list = []
    acted = heal._watch_seats(gdir, pid_alive=(lambda pid: False),
                              window_path=str(gdir / "windows.txt"),
                              launcher=_never_launcher(seen))
    assert seen == [], f"a launcher ran for a missing-worktree seat: {seen}"
    assert len(acted) == 1, acted
    assert acted[0].get("respawned") is not True, acted
    reason = json.dumps(acted[0])
    assert SEAT in reason and "seat-wt" in reason, \
        f"the refusal does not name the seat and the missing worktree: {reason}"
    assert "MAIN" in reason, f"the refusal does not say it refused MAIN: {reason}"
    text = log.read_text(encoding="utf-8")
    assert SEAT in text and "seat-wt" in text, \
        f"the watch log does not name the refusal: {text!r}"


# --- (2) the no-cwd retry is reachable for ONE signature only -------------

def test_typeerror_inside_a_cwd_aware_launcher_is_never_retried(tmp_path,
                                                                monkeypatch):
    """A cwd-aware launcher that raises a TypeError of its OWN (not about
    `cwd`) is called exactly ONCE and refused — the old `except TypeError`
    called it a second time WITHOUT cwd, waking the successor in MAIN."""
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True)
    calls: list = []

    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        calls.append(cwd)
        raise TypeError("int() argument must be a string, not 'NoneType'")

    out = heal._recover_seat(gdir, {"name": "mainseat", "role": "director",
                                    "pid": 111, "worktree": ""},
                             "pid gone", _load("rotate"),
                             windows=[], window_path=None, launcher=launch,
                             now=0.0)
    assert calls == [heal._seat_tree_dir(gdir, {"worktree": ""})], \
        f"the launcher was called again (calls={calls})"
    assert out["respawned"] is False and "TypeError" in out["reason"], out


def test_worktree_post_refuses_a_no_cwd_retry(tmp_path, monkeypatch):
    """A WORKTREE seat + a pre-cwd launcher seam (no `cwd` parameter at all,
    TypeError naming `cwd`): the recovery refuses by name rather than launch
    the successor into MAIN. The launcher is called ONCE, with cwd."""
    gdir, _ = _worktree_root(tmp_path, worktree=True)
    calls: list = []

    def precwd_launch(root, name, shell_cmd, window_path=None):
        calls.append("no-cwd")
        raise TypeError(
            "launch() got an unexpected keyword argument 'cwd'")

    out = heal._recover_seat(gdir, dict(ROW), "pid gone", _load("rotate"),
                             windows=[], window_path=None,
                             launcher=precwd_launch, now=0.0)
    assert calls == [], f"the no-cwd retry ran for a worktree seat: {calls}"
    assert out["respawned"] is False and "cwd" in out["reason"], out


def test_pre_cwd_seam_still_lands_for_a_main_checkout_seat(tmp_path):
    """The retry SURVIVES for the signature it was written for: a main-checkout
    seat (no `worktree` cell) + a pre-cwd seam is retried once, without cwd,
    and the recovery lands. Deleting the retry outright would break this."""
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True)
    calls: list = []

    def precwd_launch(root, name, shell_cmd, window_path=None):
        calls.append("no-cwd")
        return 515151, "@777"

    out = heal._recover_seat(gdir, {"name": "mainseat", "role": "director",
                                    "pid": 111, "worktree": ""},
                             "pid gone", _load("rotate"), windows=[],
                             window_path=None, launcher=precwd_launch,
                             now=0.0)
    assert calls == ["no-cwd"], calls
    assert out["respawned"] is True, out
