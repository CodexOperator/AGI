"""SM.36 integration residue, SLICE B -- items (3), (4), (5) of
hypothesis:l4-sm36-integration-residue-v3-post-merge-target-mirror-behind-
check-alias-arm-plan-line-header-fields-structural-push-test-one-scope-rule.

Item (6) (the structural push test) lives in `test_branches.py`, next to the
literal grep it replaces.

Fixtures only: no network, no real git, no real tmux.
`--delete-old` stays DRY in every test here (the seam is a recorder; the
non-live path executes zero subprocesses).
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


def _rec(calls):
    def _r(*args, **kwargs):
        calls.append(args)
    return _r


# ---- item (3): the trunk/alias arm refuses an alias BY NAME ---------------

def test_alias_surface_refused_by_name_no_push_no_delete(tmp_path, capsys):
    """SM.36 residue (3): the final `else:` arm of `_apply_surfaces` used to
    head-push `_dst` and (under --delete-old) push `:{_src}` for ANY
    spelling -- including a one-season ALIAS. An alias is refused BY NAME:
    no push argv at all, counted skipped, and the refusal names it."""
    alias = "seat/old@s2"          # parse() -> kind=alias
    surfaces = [{"kind": "branch (origin)", "src": "origin/season2/main",
                 "dst": f"origin/{alias}", "action": "seam-git"}]
    calls = []
    applied, skipped = rotate._apply_surfaces(
        tmp_path, surfaces, delete_old=True, run_git=_rec(calls),
        run_tmux=lambda *a: None)
    err = capsys.readouterr().err
    assert "REFUSED" in err and alias in err, err
    assert calls == [], f"no git argv may be issued for an alias: {calls}"
    assert skipped == 1 and applied == 0, (applied, skipped)


def test_alias_as_the_source_spelling_is_also_refused(tmp_path, capsys):
    """The refusal keys on EITHER leg: an alias on the `src` side (the old
    name being renamed away) is refused by the same by-name check."""
    alias = "post/old@s2"
    surfaces = [{"kind": "branch (origin)", "src": f"origin/{alias}",
                 "dst": "origin/season2/main", "action": "seam-git"}]
    calls = []
    applied, skipped = rotate._apply_surfaces(
        tmp_path, surfaces, delete_old=True, run_git=_rec(calls),
        run_tmux=lambda *a: None)
    err = capsys.readouterr().err
    assert "REFUSED" in err and alias in err, err
    assert calls == [], calls
    assert skipped == 1 and applied == 0, (applied, skipped)


def test_trunk_arm_still_head_renames_a_real_trunk(tmp_path):
    """No over-refusal: a genuine trunk spelling (neither post/loop nor
    alias) keeps today's head rename and the --delete-old plan argv."""
    surfaces = [{"kind": "branch (origin)", "src": "origin/season1/main",
                 "dst": "origin/season2/main", "action": "seam-git"}]
    calls = []
    rotate._apply_surfaces(tmp_path, surfaces, delete_old=True,
                           run_git=_rec(calls), run_tmux=lambda *a: None)
    assert ("push", "origin", "season2/main") in calls, calls
    assert ("push", "origin", ":season1/main") in calls, calls


# ---- item (4): the rename-apply PLAN line is unconditional ----------------

def _post_surfaces():
    return [{"kind": "branch (origin)",
             "src": "origin/season2/posts/old",
             "dst": "origin/season2/posts/new", "action": "seam-git"}]


def test_rename_apply_prints_plan_line_without_delete_old(tmp_path, capsys):
    """SM.36 residue (4): without --delete-old the rename-apply printed no
    plan line at all. The PLAN line now prints unconditionally, and the
    rename still rides the ADDITIVE mirror -- never a post head push."""
    calls = []
    rotate._apply_surfaces(tmp_path, _post_surfaces(), run_git=_rec(calls),
                           run_tmux=lambda *a: None)
    err = capsys.readouterr().err
    assert "rename-post PLAN" in err, err
    assert "season2/posts/new" in err, err
    assert ("push", "origin", "season2/posts/new:refs/agi/posts/new") \
        in calls, calls
    assert not any(c[0] == "push" and len(c) == 3
                   and c[2] == "season2/posts/new" for c in calls), calls


def test_rename_apply_delete_old_still_prints_plan_and_is_dry(
        tmp_path, monkeypatch, capsys):
    """With --delete-old the PLAN line still prints, the delete is only the
    seam's would-run argv, and NO real process runs: the non-live path
    cannot prove containment, so nothing is deleted."""
    real = []
    monkeypatch.setattr(rotate.subprocess, "run",
                        lambda *a, **k: real.append((a, k)))
    calls = []
    rotate._apply_surfaces(tmp_path, _post_surfaces(), delete_old=True,
                           run_git=_rec(calls), run_tmux=lambda *a: None)
    err = capsys.readouterr().err
    assert "rename-post PLAN" in err and "delete-old" in err, err
    assert ("push", "origin", ":season2/posts/old") in calls, calls
    assert real == [], f"non-live path must run no subprocess: {real}"


def test_rename_apply_plan_line_prints_on_the_live_path_too(tmp_path, capsys):
    """The live path (the only one that can delete) prints the same PLAN
    line; the delete there stays behind `_containment_proof`."""
    surfaces = _post_surfaces()
    calls = []

    def _git(*args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(list(args), 0, "", "")

    rotate._apply_surfaces(tmp_path, surfaces, delete_old=False, live=True,
                           run_git=_git, run_tmux=lambda *a: None)
    err = capsys.readouterr().err
    assert "rename-post PLAN" in err, err


# ---- item (5): a first seating carries the header cells through -----------

def test_first_seating_preserves_predecessor_session_and_session_ref(tmp_path):
    """SM.36 residue (5): `_first_seating_handoff_write` rewrote the whole
    header through `_write_handoff` with NEITHER predecessor_session nor
    session_ref, so a first seating dropped what an earlier rotation had
    stamped. Both cells survive the generation rewrite."""
    hands = rotate._seat_hands(tmp_path)
    hands.mkdir(parents=True, exist_ok=True)
    hp = hands / "belam.handoff.md"
    hp.write_text("seat: belam\n"
                  "generation: 3\n"
                  "rotated_at: 2026-01-01T00:00:00Z\n"
                  "predecessor_session: sensei-main\n"
                  "session_ref: @7\n", encoding="utf-8")
    assert rotate._first_seating_handoff_write(tmp_path, "belam", 4) is True
    text = hp.read_text(encoding="utf-8")
    assert "generation: 4" in text, text
    assert "predecessor_session: sensei-main" in text, text
    assert "session_ref: @7" in text, text
    # idempotent: an already-correct generation is left byte-identical
    assert rotate._first_seating_handoff_write(tmp_path, "belam", 4) is False
    assert "predecessor_session: sensei-main" in hp.read_text(encoding="utf-8")


def test_first_seating_missing_header_is_still_written(tmp_path):
    """A missing header is written, never left absent -- and no cell value
    is invented (no session_ref line appears from nothing)."""
    assert rotate._first_seating_handoff_write(tmp_path, "fresh", 1) is True
    text = (rotate._seat_hands(tmp_path) / "fresh.handoff.md").read_text(
        encoding="utf-8")
    assert "generation: 1" in text, text
    assert "session_ref" not in text, text
