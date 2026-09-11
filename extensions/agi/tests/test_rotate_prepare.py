"""Tests for the STEP 2 captive rotate-out checklist — `rotate.py prepare`
(goal:g15.14, hypothesis:l4-rotate-self-drives-the-handoff-and-prepares-the-
spawn).

RED FIRST: every claim below was written before the code. Each drives a
fixture GRAPH root — git answers are injected through `rotate._git_maybe`
(the same seam the driven writer degrades on), never a live tree:

1. **--prepare lists the dirty tree + the unpushed commit + the stale pin
   by name and exits 3** — the three named captives, one line each.
2. **A clean fixture exits 0** — no blocker named, safe to rotate.
3. **rotate-self on the dirty fixture refuses with the SAME line** — the
   one function, two callers: rotate-self refuses BY NAME, never a second
   implementation.

FALSIFIER: a --prepare that passes while rotate-self refuses (or vice
versa) fails these tests.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "extensions"))   # the `agi` package
_BIN = _REPO / "extensions" / "agi" / "bin"
sys.path.insert(0, str(_BIN))  # so the lazy `import verification` resolves

from agi.bin import rotate  # noqa: E402


@pytest.fixture
def prep_root(tmp_path):
    """A fixture GRAPH root (`nodes/` marks it a graph dir) with a seat that
    owns generation 3, a CURRENT-generation meter pin and a FRESH card — the
    'clean' state every test starts from. Tests then break it by injecting
    git lines / re-pointing the pin."""
    (tmp_path / "nodes").mkdir(parents=True)
    sess = tmp_path / "sessions"
    (sess / "seats").mkdir(parents=True)      # meter pins + handoffs
    (sess / "quorum").mkdir(parents=True)     # the card rotate-self briefs
    (sess / "seats" / "adv-alive.handoff.md").write_text(
        "seat: adv-alive\ngeneration: 3\n", encoding="utf-8")
    # a CURRENT pin: written_gen matches the seat's generation, so it is not
    # stale — a seat at gen 3 that owns a gen-3 transcript pins gen 3.
    (sess / "adv-alive.meter").write_text("3\t/some/transcript.jsonl\n",
                                          encoding="utf-8")
    # a card NEWER than the last commit so the mtime check passes.
    (sess / "quorum" / "adv-alive.md").write_text(
        "# SESSION HANDOFF — fixture\n\n## §3 🔴 NEXT COMMAND\nbash next\n",
        encoding="utf-8")
    return tmp_path


def _no_git(monkeypatch):
    """A non-repo fixture: every git read degrades to None/absent -> the
    git-based checks report ok (they only block on recorded evidence)."""
    monkeypatch.setattr(rotate, "_git_maybe",
                        lambda *a, **k: None)


def _git_map(lines):
    """Inject canned `_git_maybe` answers keyed by the args tuple."""
    def fake(cwd, *args):
        return lines.get(args)
    return fake


def _args(**over):
    base = dict(seat="adv-alive")
    base.update(over)
    return SimpleNamespace(**base)


def _rotate_self_args(**over):
    base = dict(name="adv-alive", force=False, timeout=5, debug_file=None,
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=False, successor_argv=None, role="parent")
    base.update(over)
    return SimpleNamespace(**base)


def _stale_pin(prep_root):
    """Re-point the seat's meter pin at a generation it no longer owns — the
    classic predecessor-stale pin (seat_pin-stale)."""
    pin = prep_root / "sessions" / "adv-alive.meter"
    pin.write_text("2\t/some/predecessor.jsonl\n", encoding="utf-8")


def test_prepare_lists_dirty_unpushed_stale_pin_exits_3(
        prep_root, capsys, monkeypatch):
    """The three captives the checklist must name: a dirty working tree, an
    unpushed commit on the checked-out branch, and a stale meter pin. --force
    is NOT passed (prepare has no force), the checklist names all three and
    exit 3 blocks the spawn."""
    # dirty tree (the porcelain line exists -> non-empty)
    dirty = {("status", "--porcelain"): [" M rotate.py"]}
    unpushed = {("rev-list", "--count", "@{u}..HEAD"): ["2"]}
    ok = {("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({**dirty, **unpushed, **ok}))
    rc = rotate.cmd_prepare(_args(), prep_root)
    err = capsys.readouterr()
    assert rc == 3
    assert "dirty tree" in err.out
    assert "unpushed commits" in err.out
    assert "seat_pin-stale" in err.out


def test_prepare_dirty_ignores_cron_owned_churn(prep_root, capsys,
                                                monkeypatch):
    """Sensei 18:26Z (measured on a MAIN-checkout seat): the dirty-tree
    captive blocked on `.agi/comms/season-2/dm/*.md` (send.py writes them as
    dms flow) and `.agi/sessions/rotations/sequence.json` -- cron-owned churn
    grid_sync commits, never the seat's dirt. Those paths alone -> [ok];
    a real change beside them still blocks."""
    churn = [" M .agi/comms/season-2/dm/master-sensei--belam.md",
             "?? .agi/comms/season-2/dm/a00-1234--sensei-director.md",
             " M .agi/sessions/rotations/sequence.json",
             # Sensei 18:29Z: UNTRACKED rotation records blocked a rotate-self
             # with 0 modified files
             "?? .agi/sessions/rotations/master-sensei.20260911T182900Z.json",
             "?? .agi/sessions/rotations/belam.20260911T175100Z.json"]
    ok = {("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({("status", "--porcelain"): churn, **ok}))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] dirty tree" in out
    # a genuine edit -- or an UNTRACKED new file outside the churn paths (a
    # test never `git add`-ed) -- beside the churn still blocks
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({("status", "--porcelain"):
                                  churn + ["?? extensions/agi/tests/test_x.py"],
                                  **ok}))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3
    assert "[BLOCK] dirty tree" in out


def test_prepare_card_check_reads_the_last_work_commit_only(
        prep_root, capsys, monkeypatch):
    """Sensei 18:29Z: two porcelain sync commits aged the card and blocked
    the rotation. The card check now reads the last NON-MERGE commit that
    touched something other than cron-owned churn (.agi/comms, the rotation
    records) or the card itself — that spec, and no bare `log -1`. A stale
    card against THAT commit still blocks."""
    card = prep_root / "sessions" / "quorum" / "adv-alive.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text("# card\n", encoding="utf-8")
    import os
    os.utime(card, (1000000000, 1000000000))   # long before any commit
    spec = ("log", "-1", "--no-merges", "--format=%ct", "--", ".",
            ":(exclude).agi/comms", ":(exclude).agi/sessions/rotations",
            ":(exclude)sessions/quorum/adv-alive.md")
    ok = {("status", "--porcelain"): [],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    # the bare `log -1` answer is NOT consulted any more
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({**ok, ("log", "-1", "--format=%ct"):
                                  ["9999999999"]}))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] card older than last commit" in out
    # the work-commit spec IS, and a card older than it blocks
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({**ok, spec: ["9999999999"]}))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] card older than last commit" in out


def test_prepare_clean_fixture_exits_0(prep_root, capsys, monkeypatch):
    """No blocker named: every check reports ok and the checklist exits 0 —
    safe to rotate."""
    _no_git(monkeypatch)   # non-repo: git checks degrade to ok
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0
    assert "[ok]" in out
    assert "[BLOCK]" not in out


def test_rotate_self_refuses_on_dirty_with_same_line(
        prep_root, capsys, monkeypatch):
    """rotate-self runs the SAME checks and refuses BY NAME — a dirty tree +
    unpushed commit + stale pin refuse with the exact blocker line, exit 3,
    before any side effect (no started record, no handoff)."""
    dirty = {("status", "--porcelain"): [" M rotate.py"]}
    unpushed = {("rev-list", "--count", "@{u}..HEAD"): ["1"]}
    ok = {("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({**dirty, **unpushed, **ok}))
    _stale_pin(prep_root)
    rc = rotate.cmd_rotate_self(_rotate_self_args(), prep_root)
    err = capsys.readouterr().err
    assert rc == 3
    assert "rotate-self blocked: dirty tree" in err
    assert "rotate-self blocked: unpushed commits" in err
    assert "seat_pin-stale" in err
    # refusal is atomic: nothing was started, no handoff bumped
    assert not (prep_root / "sessions" / "seats" / "adv-alive.handoff.md"
                ).read_text(encoding="utf-8").startswith("seat: adv-alive\ngeneration: 4")


def test_prepare_names_behind_captive_and_card_stale(prep_root, capsys,
                                                     monkeypatch):
    """The other captives are each NAMED too: behind origin/season/s2 (N) and
    a card whose mtime sits before the last commit."""
    behind = {("rev-list", "--count", "HEAD..origin/season/s2"): ["5"],
              ("status", "--porcelain"): [],
              ("rev-list", "--count", "@{u}..HEAD"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(behind))
    # card mtime older than the injected last commit
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({**behind,
                                  ("log", "-1", "--format=%ct"): ["9999999999"]}))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3
    assert "behind origin/season/s2 (5)" in out
    # the clearing command MERGES -- `never rebase` is a standing rule of this
    # tree (director fix-up at the SL1.02 harvest; the kid printed pull --rebase)
    assert "git merge --no-edit origin/season/s2" in out
    assert "rebase" not in out
    assert "card older than last commit" in out