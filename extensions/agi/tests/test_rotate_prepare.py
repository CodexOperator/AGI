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
import subprocess
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


def test_prepare_dirty_names_the_non_churn_paths(prep_root, capsys,
                                                 monkeypatch):
    """g15.24 clause (3): a dirty non-churn path is NAMED in the BLOCK line
    — never a bare 'dirty tree'. Up to FIVE paths then '+N more'; cron-owned
    churn paths are excluded from both the count and the names so no caller
    reads a bare 'dirty tree' and no churn path is falsely blamed."""
    dirty = {("status", "--porcelain"): [
        " M rotate.py", "?? tools/new.py", " M a.py", " M b.py", " M c.py",
        " M d.py", " M e.py", " M f.py",
        # cron-owned churn: excluded from the count AND the names
        "?? .agi/comms/season-2/dm/x.md",
        " M .agi/sessions/rotations/sequence.json"]}
    ok = {("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({**dirty, **ok}))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] dirty tree" in out
    # the FIRST FIVE non-churn paths are named; nothing beyond is guessed
    assert "rotate.py" in out and "tools/new.py" in out
    assert "a.py" in out and "b.py" in out and "c.py" in out
    # five shown, eight non-churn dirty -> three more, named count, not bare
    assert ", +3 more" in out
    # churn paths are never named, and the paths past the +N more cut
    # (d.py, e.py, f.py) are NOT listed as separate dirty paths either.
    assert "dm/x.md" not in out and "sequence.json" not in out
    assert ", d.py" not in out and ", e.py" not in out and ", f.py" not in out


def test_prepare_clean_names_no_paths(prep_root, capsys, monkeypatch):
    """The naming never pollutes the clean case: no dirty path -> the check
    names a plain '[ok] dirty tree', exactly as before."""
    clean = {("status", "--porcelain"): [],
             ("rev-list", "--count", "@{u}..HEAD"): ["0"],
             ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(clean))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] dirty tree" in out
    assert "dirty tree:" not in out


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
    """A genuinely-CLEAN fixture exits 0 — every git captive MEASURED ok, the
    unpushed captive asserted at its real pushed value (0 ahead of upstream),
    never degraded to `unmeasured`. The vacuous form used `_no_git`, so check
    1 read `unpushed commits (unmeasured)` and the pass said nothing about the
    seat's real push state at all: the fixture passed whether the captive was
    pushed or unpushed. FALSIFIER (hypothesis:l4-meter-pin-refuses-a-target-
    that-is-not-a-pin-and-prepare-prints-the-clear-line-that-clears piece 4):
    mutate the captive IN the test — set the SAME fixture's `@{u}..HEAD` count
    to 1 — and the checklist must now BLOCK by name, exit 3, proving the
    fixture asserts the real outcome instead of reading it."""
    clean = {("status", "--porcelain"): [],
             ("rev-parse", "--abbrev-ref", "HEAD"): ["feature/clean"],
             ("rev-list", "--count", "@{u}..HEAD"): ["0"],   # really pushed
             ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(clean))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] unpushed commits" in out          # measured pushed, not unmeasured
    assert "[ok] dirty tree" in out
    assert "[ok] behind origin/season/s2 (0)" in out
    assert "[BLOCK]" not in out
    # FALSIFIER: flip the captive to unpushed, by mutating the injected count
    # (never by reading the fixture) — the same clean fixture must now BLOCK.
    unpushed = dict(clean)
    unpushed[("rev-list", "--count", "@{u}..HEAD")] = ["1"]
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(unpushed))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] unpushed commits" in out


def test_rotate_self_refuses_on_dirty_with_same_line(
        prep_root, capsys, monkeypatch):
    """rotate-self runs the SAME checks and refuses BY NAME — a dirty tree +
    unpushed commit + stale pin refuse with the exact blocker line, exit 3,
    before any side effect (no started record, no handoff)."""
    dirty = {("status", "--porcelain"): [" M rotate.py"]}
    branch = {("rev-parse", "--abbrev-ref", "HEAD"): ["feature/rotate"]}
    unpushed = {("rev-list", "--count", "@{u}..HEAD"): ["1"]}
    ok = {("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({**dirty, **branch, **unpushed, **ok}))
    _stale_pin(prep_root)
    _seat_row(prep_root, 3)          # P1-c: registry gate runs first; seat must exist
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


def _seat_row(prep_root, gen, pid=None):
    """Write a config:seats row for adv-alive carrying an explicit
    `generation` — the AUTHORITY the check reads FIRST (the handoff header
    is only the fallback). `pid` pins a process-id the background-tasks line
    counts descendants under, when set."""
    g = prep_root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    row = {"name": "adv-alive", "role": "parent",
           "generation": gen, "worktree": ""}
    if pid is not None:
        row["pid"] = pid
    (g / "seats.md").write_text(
        "---\ntype: config\nseats:\n  - " + json.dumps(row) + "\n---\n",
        encoding="utf-8")


def test_prepare_blocks_when_row_generation_older_than_pin(
        prep_root, capsys, monkeypatch):
    """The generation comes from the config:seats ROW first (the authority),
    not the handoff header. Row generation 2 while the pin is written for gen
    3 -> the meter-pin captive BLOCKS by name with cur=2. (Hypothesis l4-...-
    measure-generation-upstream-and-season, piece 1.)"""
    _seat_row(prep_root, 2)          # row outweighs the fixture handoff's 3
    _no_git(monkeypatch)             # git degrades to ok; only the pin blocks
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3
    assert "[BLOCK] meter pin stale (seat_pin-stale) cur=2" in out


def test_prepare_check5_clear_line_names_pin_file_and_clears_when_run(
        prep_root, monkeypatch, capsys, tmp_path):
    """The stale-pin clear line is the ONE command that actually clears, both
    halves right (hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-pin-
    and-prepare-prints-the-clear-line-that-clears): --pin names the seat's REAL
    <sessions>/<seat>.meter (never a --seat --pin <transcript> pair that both
    misleads and trips the cross-generation read refusal), and --session-log
    names the pin's own recorded transcript when known. Running that EXACT
    printed line re-points the pin to the current generation, and the NEXT
    prepare passes check 5."""
    transcript = tmp_path / "the-predecessor.jsonl"
    transcript.write_text("FAKE JSONL\n", encoding="utf-8")
    pin = prep_root / "sessions" / "adv-alive.meter"
    pin.write_text(f"2\t{transcript}\n", encoding="utf-8")   # stale: cur=3
    _no_git(monkeypatch)
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] meter pin stale" in out
    clear = (f"rotate.py meter --pin {prep_root / 'sessions' / 'adv-alive.meter'} "
             f"--session-log {transcript}")
    assert clear in out, out
    assert "--seat" not in clear, "the clear line never uses --seat"
    assert "<transcript>" not in clear, "a known transcript is named, not a placeholder"
    # RUN the printed line as printed (same CLI entry, pin + transcript)
    m = SimpleNamespace(session_log=str(transcript),
                        pin=str(prep_root / "sessions" / "adv-alive.meter"),
                        seat=None, check=False)
    rc2 = rotate.cmd_meter(m, prep_root)
    err = capsys.readouterr()
    assert rc2 == 0, err
    # the NEXT prepare passes check 5 (stale pin cleared)
    rc3 = rotate.cmd_prepare(_args(), prep_root)
    out3 = capsys.readouterr().out
    assert rc3 == 0, out3
    assert "[ok] meter pin stale" in out3


def test_prepare_check5_clear_line_prefers_row_transcript_over_stale_pin(
        prep_root, capsys, monkeypatch):
    """P1-d falsifier: when check 5 BLOCKS (a STALE pin — another
    generation's by definition), the clear line names the config:seats ROW's
    transcript (resolved the way the meter does, from session_id + cwd), and
    NEVER the stale pin's recorded written_path. The old order filled
    known_transcript from the pin FIRST, so a predecessor's stale pin named
    the WRONG transcript for the re-point."""
    g = prep_root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    row = {"name": "adv-alive", "role": "parent", "generation": 3,
           "worktree": "", "cwd": str(prep_root / "seat-hub"),
           "session_id": "row-sess-001"}
    (g / "seats.md").write_text(
        "---\ntype: config\nseats:\n  - " + json.dumps(row) + "\n---\n",
        encoding="utf-8")
    # the pin is STALE: records generation 2, the row owns generation 3
    pin = prep_root / "sessions" / "adv-alive.meter"
    pin.write_text("2\t/some/predecessor.jsonl\n", encoding="utf-8")
    _no_git(monkeypatch)
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] meter pin stale" in out
    # row-derived transcript, never the stale pin's predecessor path
    row_transcript = rotate.transcript_from_registry_dict(row)
    assert row_transcript
    assert "/some/predecessor.jsonl" not in out
    assert row_transcript in out
    assert "--session-log" in out


def test_prepare_blocks_when_ack_is_from_older_generation(
        prep_root, capsys, monkeypatch):
    """Same row-first authority for the ack: row generation 2 while the ack
    records gen_after 1 -> the stale-ack captive BLOCKS by name."""
    _seat_row(prep_root, 2)
    sess = prep_root / "sessions"
    (sess / "seats" / "adv-alive.ack.json").write_text(
        json.dumps({"seat": "adv-alive", "gen_after": 1}), encoding="utf-8")
    _no_git(monkeypatch)
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3
    assert "[BLOCK] stale ack (adv-alive.ack.json) cur=2" in out


def test_prepare_generation_unmeasured_is_said_not_silent(
        prep_root, capsys, monkeypatch):
    """A seat with NEITHER a config:seats row generation NOR a handoff header
    prints both captives as ok + a plain `generation unmeasured` note, never
    silently passing with cur_gen=0 (the old `cur_gen`-truthiness gate made
    them inert on exactly that seat)."""
    _no_git(monkeypatch)
    rc = rotate.cmd_prepare(_args(seat="ghost"), prep_root)
    out = capsys.readouterr().out
    assert rc == 0
    assert ("[ok] meter pin stale (seat_pin-stale) generation unmeasured: "
            "no config:seats row, no handoff") in out
    assert ("[ok] stale ack (ghost.ack.json) generation unmeasured: "
            "no config:seats row, no handoff") in out


def test_rotate_self_still_refuses_with_window_path_set(
        prep_root, capsys, monkeypatch):
    """The rotate-self gate is NOT keyed on the `--window-path` fixture seam
    (hypothesis l4-...-the-gate-is-not-a-test-seam): a live-invoked --window-
    path used to skip the whole checklist silently; now with a dirty fixture
    tree it STILL refuses BY NAME and exit 3."""
    dirty = {("status", "--porcelain"): [" M rotate.py"]}
    branch = {("rev-parse", "--abbrev-ref", "HEAD"): ["feature/rotate"]}
    ok = {("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map({**dirty, **branch, **ok}))
    _seat_row(prep_root, 3)          # P1-c: registry gate runs first; seat must exist
    rc = rotate.cmd_rotate_self(_rotate_self_args(window_path="/tmp/fake.txt"),
                                prep_root)
    err = capsys.readouterr().err
    assert rc == 3
    assert "rotate-self blocked: dirty tree" in err


def test_prepare_blocks_no_upstream_named(
        prep_root, capsys, monkeypatch):
    """A branch with NO upstream: `@{u}` does not resolve and `origin/<br>`
    does not exist either -> the unpushed captive BLOCKS `no upstream for
    <branch>` with the push -u command, instead of falling through inert as
    (None or 0) > 0 = False."""
    branch = {("rev-parse", "--abbrev-ref", "HEAD"): ["fresh/unpushed"]}
    ok = {("status", "--porcelain"): [],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    # neither `@{u}..HEAD` nor `origin/fresh/unpushed..HEAD` is injected -> None
    monkeypatch.setattr(rotate, "_git_maybe", _git_map({**branch, **ok}))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3
    assert "[BLOCK] no upstream for fresh/unpushed" in out
    assert "git push -u origin fresh/unpushed" in out


def test_prepare_season_branch_comes_from_the_ladder(
        prep_root, capsys, monkeypatch):
    """The season is resolved from the ladder's `current_season`, never a
    hardcoded season/s2. Ladder season 3 -> check 3 names origin/season/s3 and
    the merge command merges origin/season/s3 (and the geometry sync command
    derives the same branch)."""
    g = prep_root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "ladder.md").write_text(
        "---\ntype: config\ncurrent_season: 3\n---\n", encoding="utf-8")
    behind = {("status", "--porcelain"): [],
              ("rev-parse", "--abbrev-ref", "HEAD"): ["feature/x"],
              ("rev-list", "--count", "@{u}..HEAD"): ["0"],
              ("rev-list", "--count", "HEAD..origin/season/s3"): ["5"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(behind))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3
    assert "[BLOCK] behind origin/season/s3 (5)" in out
    assert "git fetch origin season/s3 && git merge --no-edit origin/season/s3" \
        in out
    assert rotate._geometry_sync_cmd(prep_root) == \
        "git fetch origin season/s3 && git merge --no-edit origin/season/s3"

# =====================================================================
# hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-
# seats-live-background-tasks (SL3.05) — RED FIRST: written before the code.
# `--perform` PERFORMS check 3 (the only-behind season merge) only when it
# is mechanical: check 2 (dirty tree) passed AND the merge applies with zero
# conflicts. A conflicting merge stays a BLOCK naming the paths. The
# background-tasks line is a LISTING, never a blocker. rotate-self's gate
# defaults `--perform` ON; bare `prepare` defaults it OFF.
# =====================================================================


def _git_proc_ok(rc=0):
    """A `_git_proc` seam: every call returns `rc` (0 = success) with empty
    stdout. The happy-path merge tests make the REAL `_perform_season_merge`'s
    `merge` call (which routes through `_git_proc`, the returncode-bearing
    seam) succeed; its other git reads still route through `_git_maybe`."""
    return lambda *a, **k: SimpleNamespace(returncode=rc, stdout="")


def _merge_seam(prep_root, behind_n=2, conflict_free=True, merged="abc1234"):
    """A clean, measurably-behind fixture with the merge seams injected:
    `_merge_applies_clean` True (zero conflicts) runs the REAL
    `_perform_season_merge`, whose every git read is supplied through
    `_git_maybe` so the merge line reports the injected sha. `conflict_free`
   =False swaps in the conflict branch without touching the tree."""
    gm = {("status", "--porcelain"): [],
          ("rev-parse", "--abbrev-ref", "HEAD"): ["seat/x"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): [str(behind_n)],
          ("fetch", "origin", "season/s2"): [],
          ("merge", "--no-edit", "origin/season/s2"): [],
          ("rev-parse", "--short", "HEAD"): [merged],
          ("log", "-1", "--no-merges", "--format=%ct", "--", ".",
           ":(exclude).agi/comms", ":(exclude).agi/sessions/rotations"):
          ["1000000000"]}
    return gm


def test_prepare_perform_merges_only_behind_clean(prep_root, capsys,
                                                  monkeypatch):
    """`prepare --seat S --perform` on a clean tree behind by 2 MERGES the
    only-behind season branch: the line reads performed with the sha, the
    check stops blocking, exit 0. A second run (now even) reads ok."""
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map(_merge_seam(prep_root)))
    monkeypatch.setattr(rotate, "_git_proc", _git_proc_ok())
    monkeypatch.setattr(rotate, "_merge_applies_clean",
                        lambda root, sb: True)
    rc = rotate.cmd_prepare(_args(perform=True), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] behind origin/season/s2 (2) — merged abc1234" in out
    assert "[BLOCK]" not in out
    # a SECOND run now that HEAD == origin (behind 0) reads plain ok
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map(_merge_seam(prep_root, behind_n=0)))
    rc = rotate.cmd_prepare(_args(perform=True), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] behind origin/season/s2 (0)" in out
    assert "merged" not in out


def test_prepare_perform_merge_refused_blocks_not_merged(
        prep_root, capsys, monkeypatch):
    """The success line is gated on the MERGE exit status, not on the pre-
    merge HEAD sha. A merge that git REFUSES (non-zero rc) must block like a
    false-ok blocker: `_perform_season_merge` returns None, check 3 prints
    BLOCK (never `— merged`), exit 3, and the success-sha path is not taken
    (the `rev-parse --short HEAD` read is never consulted — reaching it
    would report the stale pre-merge sha)."""
    gm = _merge_seam(prep_root)
    # the merge is REFUSED: non-zero rc, so NO further git reads happen. The
    # `rev-parse --short HEAD` key in gm would report the pre-merge sha if it
    # were consulted (the false ok); it must never be read on a failed merge.
    monkeypatch.setattr(rotate, "_git_proc", _git_proc_ok(rc=1))
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    monkeypatch.setattr(rotate, "_merge_applies_clean",
                        lambda root, sb: True)
    rc = rotate.cmd_prepare(_args(perform=True), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert ("[BLOCK] behind origin/season/s2 (2) — merge attempted, "
            "refused by git") in out
    assert "git merge --no-edit origin/season/s2" in out   # clear command stays
    assert "merged" not in out                # never a false ok


def test_prepare_perform_conflict_stays_block_names_path(prep_root, capsys,
                                                         monkeypatch):
    """A conflicting merge is NOT judgement-free: `--perform` leaves it a
    BLOCK naming the conflicting path and the merge command, and NEVER issues
    the merge (`_perform_season_merge` would raise if touched)."""
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map(_merge_seam(prep_root)))
    monkeypatch.setattr(rotate, "_merge_applies_clean",
                        lambda root, sb: False)
    monkeypatch.setattr(rotate, "_merge_conflict_paths",
                        lambda root, sb: "extensions/agi/bin/rotate.py")
    def _no_merge(*a, **k):
        raise AssertionError("merge was performed on a conflicting tree")
    monkeypatch.setattr(rotate, "_perform_season_merge", _no_merge)
    rc = rotate.cmd_prepare(_args(perform=True), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert ("[BLOCK] behind origin/season/s2 (2) — merge conflicts: "
            "extensions/agi/bin/rotate.py") in out
    assert "git merge --no-edit origin/season/s2" in out
    assert "merged" not in out


def test_prepare_perform_skips_merge_on_dirty_tree(prep_root, capsys,
                                                   monkeypatch):
    """`--perform` NEVER merges over a dirty tree: check 2 blocks first, so
    check 3 stays a BLOCK and no merge is issued (dirty-first)."""
    gm = _merge_seam(prep_root)
    gm[("status", "--porcelain")] = [" M rotate.py"]
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    monkeypatch.setattr(rotate, "_merge_applies_clean",
                        lambda root, sb: True)   # would merge IF consulted
    def _no_merge(*a, **k):
        raise AssertionError("merge was performed over a dirty tree")
    monkeypatch.setattr(rotate, "_perform_season_merge", _no_merge)
    rc = rotate.cmd_prepare(_args(perform=True), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] dirty tree" in out
    assert "[BLOCK] behind origin/season/s2 (2)" in out
    assert "merged" not in out


def test_prepare_bare_never_merges(prep_root, capsys, monkeypatch):
    """Bare `prepare` (no --perform) is a LISTING only: it NEVER merges, even
    when the merge happens to be clean — the line stays a BLOCK."""
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map(_merge_seam(prep_root)))
    monkeypatch.setattr(rotate, "_merge_applies_clean",
                        lambda root, sb: True)
    def _no_merge(*a, **k):
        raise AssertionError("bare prepare must not merge")
    monkeypatch.setattr(rotate, "_perform_season_merge", _no_merge)
    rc = rotate.cmd_prepare(_args(), prep_root)       # no --perform
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] behind origin/season/s2 (2)" in out
    assert "merged" not in out


def test_prepare_background_tasks_line_counts_row_pid(
        prep_root, capsys, monkeypatch):
    """The background-tasks LISTING names what is measurable: a config:seats
    row carrying a `pid` counts its live descendants (`_proc_children` seam
    here returns 2) as `2 proc`."""
    _no_git(monkeypatch)
    _seat_row(prep_root, 3, pid=314159)   # gen matches the fixture pin
    monkeypatch.setattr(rotate, "_proc_children", lambda pid: 2)
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "background tasks: 2 proc" in out


def test_prepare_background_tasks_unmeasured_without_pid(
        prep_root, capsys, monkeypatch):
    """A seat with no row pid (and no .claude/tasks dir) prints the line
    `unmeasured` — never a fabricated 0, never a guess."""
    _no_git(monkeypatch)
    rc = rotate.cmd_prepare(_args(seat="ghost"), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "background tasks: unmeasured" in out


def test_rotate_self_perform_merge_during_prepare_gate(
        prep_root, capsys, monkeypatch):
    """rotate-self's own `--prepare` is the SAME checklist but with `--perform`
    DEFAULTED ON (rotate-self's gate performs the only-behind merge). A clean,
    behind-by-2 tree through the rotate-self path prints the performed line
    and exit 0 — the mechanical merge costs zero tool calls. The seat must be
    REGISTERED (R1 registry gate in the --prepare path)."""
    _seat_row(prep_root, 3)            # R1 registry gate needs a registered seat
    monkeypatch.setattr(rotate, "_git_maybe",
                        _git_map(_merge_seam(prep_root)))
    monkeypatch.setattr(rotate, "_git_proc", _git_proc_ok())
    monkeypatch.setattr(rotate, "_merge_applies_clean",
                        lambda root, sb: True)
    rc = rotate.cmd_rotate_self(_rotate_self_args(prepare=True), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] behind origin/season/s2 (2) — merged abc1234" in out


# =====================================================================
# P2-a (SL5.06): the real merge gate + abort path on a LIVE git fixture.
# `_merge_applies_clean` / `_merge_conflict_paths` / `_perform_season_merge`
# are patched out in every committed test; these run the REAL merge-tree
# gate and the REAL merge against a real two-branch repo -- nothing about
# the merge is monkeypatched. The assertions are on what actually merged
# (HEAD advanced past the season commit, the season file is present), so a
# gate patched out fails them.
# =====================================================================


def _git(cwd, *args):
    """Run git in the fixture repo; raise on failure."""
    return subprocess.run(["git", "-C", str(cwd), *args],
                          check=True, capture_output=True, text=True)


def _real_repo(prep_root, conflict):
    """A REAL git worktree whose only-behind branch (`origin/season/s2`)
    merges into the checked-out `seat/x` branch CLEANLY (conflict=False) or
    with a conflict on `f.txt` (conflict=True). The merge-tree gate, the
    merge, the refs and the abort all run against the LIVE repo -- the
    fixture graph seed (meter pin, card, handoff) is committed in the base
    commit and the card is re-touched after the last commit so its mtime is
    fresh (check 4). Returns the repo root."""
    root = prep_root
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "test")
    _git(root, "config", "commit.gpgsign", "false")
    (root / "base.txt").write_text("base\n", encoding="utf-8")
    _git(root, "add", "-A")          # base.txt + the fixture graph seed
    _git(root, "commit", "-qm", "base")
    base = _git(root, "rev-parse", "HEAD").stdout.strip()
    # season/s2 — ONE commit ahead of the merge-base
    _git(root, "checkout", "-qb", "season/s2", base)
    if conflict:
        (root / "f.txt").write_text("season\n", encoding="utf-8")
    else:
        (root / "season.txt").write_text("season\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "season work")
    _git(root, "update-ref", "refs/remotes/origin/season/s2", "HEAD")
    # seat/x — ONE commit ahead of the merge-base, diverged
    _git(root, "checkout", "-qb", "seat/x", base)
    (root / "seat.txt").write_text("seat\n", encoding="utf-8")
    if conflict:
        (root / "f.txt").write_text("seat\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "seat work")
    _git(root, "update-ref", "refs/remotes/origin/seat/x", "HEAD")
    _git(root, "config", "branch.seat/x.remote", "origin")
    _git(root, "config", "branch.seat/x.merge", "refs/heads/seat/x")
    # the card must be NEWER than the last commit (check 4)
    (root / "sessions" / "quorum" / "adv-alive.md").write_text(
        "# SESSION HANDOFF — fixture\n\n## §3 🔴 NEXT COMMAND\nbash next\n",
        encoding="utf-8")
    return root


def test_prepare_perform_merge_same_ref_clean_real_fixture(
        prep_root, capsys):
    """P2-a clean: `prepare --perform` on a real repo where the only-behind
    branch merges cleanly runs the REAL merge-tree gate and MERGES the freshly-
    fetched SAME ref: the line names the merged sha, exit 0, HEAD advanced
    past the season commit and the season file is in the tree."""
    root = _real_repo(prep_root, conflict=False)
    rc = rotate.cmd_prepare(_args(perform=True), root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] behind origin/season/s2 (1) — merged" in out
    assert "[BLOCK]" not in out
    # the merge actually landed: HEAD moved past the seat-work commit and
    # the season file is present (a patched-out gate fails these)
    assert _git(root, "rev-parse", "HEAD").stdout.strip() \
        != _git(root, "rev-parse", "origin/seat/x").stdout.strip()
    assert "season.txt" in _git(root, "ls-files").stdout
    assert _git(root, "status", "--porcelain").stdout.strip() == ""


def test_prepare_perform_conflict_blocks_real_fixture(prep_root, capsys):
    """P2-a conflict: `prepare --perform` on a real repo where the only-behind
    branch conflicts on `f.txt` runs the REAL merge-tree gate -> BLOCK naming
    f.txt, exit 3, and NO merge was started (working tree untouched, no
    MERGING state, HEAD did not move)."""
    root = _real_repo(prep_root, conflict=True)
    rc = rotate.cmd_prepare(_args(perform=True), root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert ("[BLOCK] behind origin/season/s2 (1) — merge conflicts:"
            " f.txt") in out
    assert "merged" not in out
    # no half-merge: no MERGING state, no conflict markers left, HEAD unmoved
    assert "MERGING" not in _git(root, "status").stdout
    assert _git(root, "diff", "--name-only").stdout.strip() == ""
    assert _git(root, "log", "-1", "--format=%s").stdout.strip() \
        == "seat work"


def test_prepare_check2_whitespace_only_delta_clean(prep_root, capsys):
    """CLAIM-2 prepare check 2, real fixture: a tracked seats.md whose ONLY
    delta vs HEAD is a missing EOF newline (the one-serializer EOJ dirt)
    reads CLEAN — named on ONE never-blocking line (`seats.md: whitespace-only
    delta, treated as clean`) and prepare exits 0. FALSIFIER: a REAL one-cell
    change in the same file still names a dirty-tree BLOCK (exit 3) — the
    gate is never weakened for a real change."""
    root = _real_repo(prep_root, conflict=False)
    (root / "seats.md").write_text("name\trole\nbelam\tprime\n",
                                   encoding="utf-8")
    _git(root, "add", "seats.md")
    _git(root, "commit", "-qm", "seats")
    # the extra commit is 'pushed' so check 1 (unpushed commits) stays ok.
    _git(root, "update-ref", "refs/remotes/origin/seat/x",
         _git(root, "rev-parse", "HEAD").stdout.strip())
    # whitespace-only: drop ONLY the EOF newline from the working copy.
    (root / "seats.md").write_bytes(
        (root / "seats.md").read_bytes().rstrip(b"\n"))
    rc = rotate.cmd_prepare(_args(perform=True), root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] seats.md: whitespace-only delta, treated as clean" in out
    assert "[BLOCK]" not in out
    # falsifier: a REAL one-cell change stays a dirty-tree BLOCK.
    (root / "seats.md").write_text("name\trole\nbelam\tadversary\n",
                                   encoding="utf-8")
    rc = rotate.cmd_prepare(_args(perform=True), root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] dirty tree: seats.md" in out


def test_prepare_perform_season_merge_aborts_live_conflict(prep_root):
    """P2-a abort path: the REAL `_perform_season_merge` on the conflicting
    repo — the actual `git merge` CONFLICTS, so the function must run
    `git merge --abort` and return None, leaving the tree clean (never a
    half-merge). No gate is monkeypatched."""
    root = _real_repo(prep_root, conflict=True)
    sha = rotate._perform_season_merge(root, "season/s2")
    assert sha is None                     # the merge did not land
    # the half-merge was aborted: no MERGING state, no conflict markers
    assert "MERGING" not in _git(root, "status").stdout
    assert _git(root, "diff", "--name-only").stdout.strip() == ""
    assert _git(root, "log", "-1", "--format=%s").stdout.strip() \
        == "seat work"


def _master_with_season_repo(prep_root):
    """A REAL git repo CHECKED OUT ON `master` with a `season/s2` branch
    present ONE commit ahead — the state the branch guard MUST refuse a
    `--perform` on, rather than merge season INTO master. (The process cwd
    branches the guard on, so the caller chdir's into it.)"""
    root = prep_root
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "test")
    _git(root, "config", "commit.gpgsign", "false")
    (root / "base.txt").write_text("base\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "base")
    base = _git(root, "rev-parse", "HEAD").stdout.strip()
    # season/s2 — ONE commit ahead; master stays checked out
    _git(root, "checkout", "-qb", "season/s2", base)
    (root / "season.txt").write_text("season\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "season work")
    _git(root, "checkout", "-q", "master")
    return root


def test_prepare_perform_refuses_on_master_before_merge(
        prep_root, capsys, monkeypatch):
    """P1-b falsifier: `prepare --perform` on a repo checked out on master
    with a season branch present REFUSES with the branch-guard text and exit
    1 BEFORE any merge — it must never MERGE season INTO master. The guard
    reads the process cwd's branch, so we chdir into the fixture."""
    root = _master_with_season_repo(prep_root)
    monkeypatch.chdir(root)
    head_before = _git(root, "rev-parse", "HEAD").stdout.strip()
    rc = rotate.cmd_prepare(_args(perform=True), root)
    err = capsys.readouterr().err
    assert rc == 1
    assert "rotate refuses to run on master" in err
    assert "season/s2" in err
    # no merge: HEAD on master did not advance, the season file is absent
    assert _git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert "season.txt" not in _git(root, "ls-files").stdout


def test_rotate_self_unregistered_name_refuses_without_merge(
        prep_root, capsys, monkeypatch):
    """P1-c falsifier: rotate-self `--name <unregistered>` on a behind,
    mergeable repo refuses `no seat` with exit 1 and NO merge performed — the
    registry gate runs BEFORE the prepare/perform step, so a behind worktree
    does not merge a commit as a side effect before refusing. The fixture has
    NO `nodes/.geometry/seats.md`, so every name incl. `ghost` is unregistered."""
    root = _real_repo(prep_root, conflict=False)  # on seat/x, season/s2 behind, clean merge
    monkeypatch.chdir(root)
    rc = rotate.cmd_rotate_self(_rotate_self_args(name="ghost"), root)
    err = capsys.readouterr().err
    assert rc == 1
    assert "no seat 'ghost'" in err
    # no merge landed: HEAD did not move and the season file is absent
    assert "season.txt" not in _git(root, "ls-files").stdout
    assert _git(root, "status", "--porcelain").stdout.strip() == ""


def test_rotate_self_prepare_unregistered_name_refuses_without_merge(
        prep_root, capsys, monkeypatch):
    """R1 falsifier: `rotate-self --prepare --name <unregistered>` on a
    behind, mergeable repo REFUSES `no seat` BEFORE any merge. cmd_prepare
    (which the --prepare path delegates to) has NO registry check of its own,
    and --prepare sets perform = not dry_run — so without a registry gate in
    the --prepare path an unregistered name would MERGE a commit as a side
    effect before refusing. The fixture has NO seats.md, so `ghost` is
    unregistered; the clean behind branch would merge if the gate were absent."""
    root = _real_repo(prep_root, conflict=False)
    monkeypatch.chdir(root)
    rc = rotate.cmd_rotate_self(_rotate_self_args(name="ghost", prepare=True),
                                root)
    err = capsys.readouterr().err
    assert rc == 1
    assert "no seat 'ghost'" in err
    # no merge landed: HEAD did not move and the season file is absent
    assert "season.txt" not in _git(root, "ls-files").stdout
    assert _git(root, "status", "--porcelain").stdout.strip() == ""

