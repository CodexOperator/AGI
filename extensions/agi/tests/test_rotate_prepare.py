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

import importlib.util
import inspect
import json
import os
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


def _seed_gen_record(root, name, gen_after):
    """Seed ONE latest rotation record carrying `gen_after` -- the
    engine-written source `_generation_measured` falls back to when the
    config:seats row carries no generation cell (hypothesis:l4-a-posts-
    generation-is-measured-from-its-row-or-latest-record-never-from-a-
    handoff-header-it-can-hand-edit). The handoff header is never read as a
    gate, so fixtures seed a record, not a header."""
    rot = rotate._rotations_dir(root)
    rot.mkdir(parents=True, exist_ok=True)
    (rot / f"{name}.20260917T000000Z.rotation.json").write_text(
        json.dumps({"rotation": "rotate-self", "seat": name,
                    "gen_after": gen_after}), encoding="utf-8")


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
    _seed_gen_record(tmp_path, "adv-alive", 3)  # seat OWNS gen 3 (record)
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


def _stamp(prep_root, ts):
    """Write the seat's OWN last-act stamp (bin/last_act.py) with `ts`."""
    p = prep_root / "sessions" / "seats" / "adv-alive.last-act"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"{ts}\n", encoding="utf-8")
    return p


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
    # SM.40: churn paths ARE named -- but on their OWN never-blocking
    # `[ok] rotation churn:` line, never in the dirty-tree BLOCK line (a
    # hidden class was the bug). The paths past the +N more cut (d.py, e.py,
    # f.py) are still NOT listed.
    _block_line = next(ln for ln in out.splitlines()
                       if ln.startswith("[BLOCK] dirty tree"))
    assert "dm/x.md" not in _block_line and "sequence.json" not in _block_line
    assert ("[ok] rotation churn: .agi/comms/season-2/dm/x.md, "
            ".agi/sessions/rotations/sequence.json") in out, out
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


def test_prepare_card_check_reads_the_seats_own_last_act(
        prep_root, capsys, monkeypatch):
    """Check 4 is the SEAT'S OWN clock (bin/last_act.py), NEVER the repo-wide
    `git log -1 --no-merges -- .` spec: an unmeasurable own act reads NOT
    stale (P7), and an own act after the card blocks. A foreign seat's commit
    is invisible to it (conjunct 2)."""
    import os
    card = prep_root / "sessions" / "quorum" / "adv-alive.md"
    os.utime(card, (1000000000, 1000000000))   # long before any commit
    ok = {("status", "--porcelain"): [],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    seen = []
    def recorder(cwd, *args):
        seen.append(args)
        return ok.get(args)
    monkeypatch.setattr(rotate, "_git_maybe", recorder)
    # no own act measurable -> ok, the ancient card is NOT stale (P7).
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[ok] card older than last commit" in out
    # an own act AFTER the card blocks.
    _stamp(prep_root, "9999999999")
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] card older than last commit" in out
    # FALSIFIER (no second implementation of the clock): check 4 issues NO
    # repo-wide `log --no-merges` spec of its own.
    assert all("--no-merges" not in a for a in seen), seen


def test_stops_rotation_parameter_is_retired_by_name():
    """SM.68 residue (6): `_prepare_checks` no longer takes `stops_rotation`.
    The SL7.30 seats/posts exclusion it gated was removed when check 4 moved
    to the seat-scoped `bin/last_act.py` clock, leaving a parameter NOTHING
    read while its docstring still claimed it changed behaviour -- SL7.30's
    original assertion had been DELETED, not re-anchored. This names the
    retirement in the SIGNATURE; the old test only asserted the dead argument
    was inert, which would pass forever."""
    assert "stops_rotation" not in inspect.signature(
        rotate._prepare_checks).parameters


def test_card_check_names_the_unmeasurable_state(
        prep_root, capsys, monkeypatch):
    """SM.68 residue (5): no stamp AND no card commit -> NOTHING measurable.
    That used to print the SAME `[ok] card older than last commit` a
    measured-fresh seat prints, so a seat whose clock could not be read was
    indistinguishable from one read and found fresh. The unmeasurable verdict
    is named; the measured-fresh label stays byte-identical."""
    ok = {("status", "--porcelain"): [],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(ok))
    # no stamp, git absent -> card_stale returns (False, None): unmeasured.
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    line = next(ln for ln in out.splitlines()
                if "card older than last commit" in ln)
    assert line.startswith("[ok]"), line
    assert "unmeasured" in line, line
    # measured-fresh: a real own act BEHIND the card -> the plain label, no
    # suffix (the existing test pins the same string for the fresh case).
    _stamp(prep_root, "1000000000")
    os.utime(prep_root / "sessions" / "quorum" / "adv-alive.md",
             (2000000000, 2000000000))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    line = next(ln for ln in out.splitlines()
                if "card older than last commit" in ln)
    assert line == "[ok] card older than last commit", line


def test_hook_and_rotate_agree_on_the_card_stale_verdict(prep_root, monkeypatch):
    """(C) ONE verdict, TWO readers: the hook's gate (a) measure and rotate's
    `_prepare_checks` check 4 read the SAME seat-scoped clock (`bin/
    last_act.py`) on the SAME fixture state -- fresh AND stale. A second
    implementation of the clock is the falsifier; a disagreement between the
    thing that REFUSES the rotation and the thing that HOLDS it is worse than
    either being wrong alone."""
    import os
    hook_path = _REPO / "extensions" / "agi" / "hooks" / "rotation_alert.py"
    spec = importlib.util.spec_from_file_location("rotation_alert_agree",
                                                  hook_path)
    hook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hook)
    monkeypatch.delenv("AGI_SEAT", raising=False)
    _no_git(monkeypatch)
    card = prep_root / "sessions" / "quorum" / "adv-alive.md"

    def verdicts():
        hook_stale, _line = hook._card_stale_measure(prep_root, "adv-alive",
                                                     card)
        rot = [c for c in rotate._prepare_checks(prep_root, "adv-alive")
               if c[1] == "card older than last commit"][0]
        return hook_stale, rot[0]

    # FRESH: the stamp is older than the card.
    _stamp(prep_root, 1)
    assert verdicts() == (False, False)
    # STALE: the seat worked AFTER writing the card.
    os.utime(card, (1000000000, 1000000000))
    _stamp(prep_root, 2_000_000_000)
    assert verdicts() == (True, True)


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
    _seat_row_wt(prep_root, 3)   # own dirt blocks even when touch unmeasured
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
    `generation` — the AUTHORITY the check reads FIRST (the latest rotation
    record is only the fallback). `pid` pins a process-id the background-
    tasks line counts descendants under, when set."""
    g = prep_root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    row = {"name": "adv-alive", "role": "parent",
           "generation": gen, "worktree": ""}
    if pid is not None:
        row["pid"] = pid
    (g / "seats.md").write_text(
        "---\ntype: config\nseats:\n  - " + json.dumps(row) + "\n---\n",
        encoding="utf-8")


def _seat_row_wt(prep_root, gen):
    """A WORKTREE seat row (worktree non-empty): its dirt is its own, ALL of
    it blocks even when the merge touch-set is unmeasurable. Used by the
    rotate-self same-line refusal tests whose intent is 'own dirt blocks'
    WITHOUT depending on the SM.84 MAIN-post foreign-dirt scoping."""
    g = prep_root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    row = {"name": "adv-alive", "role": "parent",
           "generation": gen, "worktree": "/some/wt"}
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
    # SL7.87 (g15.25): the refusal names its evidence — the file's gen_after,
    # answer, source, written-time and the row's gen — not a bare `cur=N`.
    assert "[BLOCK] stale ack (adv-alive.ack.json): gen_after=1" in out
    assert "answer=?" in out and "source=unknown" in out
    assert "row gen=2" in out


def test_prepare_generation_unmeasured_is_said_not_silent(
        prep_root, capsys, monkeypatch):
    """A seat with NEITHER a config:seats row generation NOR a latest
    rotation record prints both captives as ok + a plain `generation
    unmeasured` note, never silently passing with cur_gen=0 (the old
    `cur_gen`-truthiness gate made them inert on exactly that seat)."""
    _no_git(monkeypatch)
    rc = rotate.cmd_prepare(_args(seat="ghost"), prep_root)
    out = capsys.readouterr().out
    assert rc == 0
    assert ("[ok] meter pin stale (seat_pin-stale) generation unmeasured: "
            "no config:seats row, no record") in out
    assert ("[ok] stale ack (ghost.ack.json) generation unmeasured: "
            "no config:seats row, no record") in out


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
    _seat_row_wt(prep_root, 3)  # own dirt blocks on a worktree seat
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
    # the merge is REFUSED: non-zero rc on the MERGE call ONLY (the claim
    # fetch and the merge-tree gate return rc 0, or the fetch would read as
    # fetch-failed and this scenario would never reach the merge). So NO
    # further git reads happen after the refused merge -- the `rev-parse
    # --short HEAD` key in gm would report the pre-merge sha if it were read.
    def _refuse_merge(cwd, *args):
        # args like ("merge", "--no-edit", "origin/season/s2")
        rc = 1 if (args and args[0] == "merge") else 0
        return SimpleNamespace(returncode=rc, stdout="")
    monkeypatch.setattr(rotate, "_git_proc", _refuse_merge)
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
    monkeypatch.setattr(rotate, "_git_proc", _git_proc_ok())
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
    monkeypatch.setattr(rotate, "_git_proc", _git_proc_ok())
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
    _git(root, "remote", "add", "origin", str(root))   # self-remote: makes
    # `git fetch origin <branch>` (the pre-count fetch) exit 0 instead of 128
    # ("origin does not appear to be a git repository"); a bare `fetch` with
    # no configured refspec never rewrites the hand-set origin/* refs below.
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


def test_prepare_check2_whitespace_only_delta_clean(prep_root, capsys,
                                                    monkeypatch):
    """CLAIM-2 prepare check 2, real fixture: a tracked seats.md whose ONLY
    delta vs HEAD is a missing EOF newline (the one-serializer EOJ dirt)
    reads CLEAN — named on ONE never-blocking line (`seats.md: whitespace-only
    delta, treated as clean`) and prepare exits 0. FALSIFIER: a REAL one-cell
    change in the same file still names a dirty-tree BLOCK (exit 3) — the
    gate is never weakened for a real change. The fixture sits on a post's
    own `seat/x` branch, so it is a WORKTREE post (row worktree non-empty) —
    its dirt is its own and ALL of it blocks, exactly as before the g15.25
    partition."""
    # a WORKTREE post: dirty-tree partition (MAIN-post only) never runs.
    monkeypatch.setattr(rotate, "_find_seat",
                        lambda root, name: {"name": "adv-alive",
                                            "worktree": "/some/wt"})
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


def test_prepare_check2_index_only_real_change_blocks(prep_root, capsys,
                                                      monkeypatch):
    """CLAIM (6a/SL7.17, hypothesis:l4-prepare-check-2-reads-the-index-blob...):
    a STAGED real edit whose working copy is restored to HEAD bytes must read
    DIRTY, never whitespace-only — prepare check 2 BLOCKS naming it
    'seats.md: staged change (index differs from HEAD)' so a rotation never
    proceeds over an unrecorded staged edit. FALSIFIER (pre-fix):
    `_path_delta_whitespace_only` compared HEAD against the WORKING file only,
    so the restored copy read whitespace-only and prepare exited 0. The
    fixture is a WORKTREE post (row worktree non-empty): its dirt blocks as
    today, the g15.25 partition never runs."""
    monkeypatch.setattr(rotate, "_find_seat",
                        lambda root, name: {"name": "adv-alive",
                                            "worktree": "/some/wt"})
    root = _real_repo(prep_root, conflict=False)
    (root / "seats.md").write_text("name\trole\nbelam\tprime\n",
                                   encoding="utf-8")
    _git(root, "add", "seats.md")
    _git(root, "commit", "-qm", "seats")
    _git(root, "update-ref", "refs/remotes/origin/seat/x",
         _git(root, "rev-parse", "HEAD").stdout.strip())
    # stage a REAL edit...
    (root / "seats.md").write_text("name\trole\nbelam\tadversary\n",
                                   encoding="utf-8")
    _git(root, "add", "seats.md")
    # ...then restore the working copy to HEAD bytes (a staged-only change):
    # porcelain `M `, index differs from HEAD in real bytes, working == HEAD.
    (root / "seats.md").write_text(
        _git(root, "show", "HEAD:seats.md").stdout, encoding="utf-8")
    rc = rotate.cmd_prepare(_args(perform=True), root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert ("[BLOCK] dirty tree: seats.md: staged change "
            "(index differs from HEAD)") in out, out
    assert "whitespace-only delta" not in out, out


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



# =====================================================================
# hypothesis:l4-rotate-self-pushes-and-continues-when-the-only-prepare-
# blocker-is-unpushed-commits (SL7.113) — the refusal already names `git
# push`, so exit 3 would be a call spent to type it (belam XVII paid 2 at
# 21:59Z). When the checklist's blockers are EXACTLY ONE entry and it is
# check 1 in a MEASURED-unpushed spelling (`unpushed commits` or `unpushed
# commits vs origin/<branch>` — NEVER `no upstream for <branch>`), rotate-
# self PERFORMS the push through `_stops_push(label='unpushed')` (the ONE
# helper, never a third implementation), completes any deferred pending
# swap on OK, and CONTINUES (no refusal). A refused push stays a BLOCK by
# name; two or more blockers are byte-identical to today; a `--dry-run`
# performs nothing and prints its would-push line. RED FIRST: written
# before the code; the push seam is the monkeypatched `_stops_push`
# recording its label.
# =====================================================================


def _real_unpushed_rotate_repo(tmp_path):
    """A REAL git repo with a bare origin and an upstreamed branch whose
    checked-out HEAD is ONE commit AHEAD of origin (the classic `git push`
    beltam paid to type). NOTHING is dirty, behind, or stale — the single
    prepare blocker is exactly check 1 measured-unpushed. The card is
    refreshed AFTER the unpushed commit so check 4 measures clean. Mirrors
    test_rotate's `_init_git_remote` + the rotate-self e2e fixtures so the
    post-push tail reaches spawn."""
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    (root / "nodes").mkdir(parents=True, exist_ok=True)
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent:\n    brief_file: extensions/agi/briefs/parent-successor.md\n"
        "    steps: [handoff, rename, spawn]\n    telemetry: [seat]\n"
        "---\n\nbody\n", encoding="utf-8")
    (g / "seats.md").write_text(
        "---\ntype: config\nseats:\n  - {\"name\": \"adv-alive\", "
        "\"role\": \"parent\", \"generation\": 1}\n---\n", encoding="utf-8")
    sess = root / "sessions"
    (sess / "seats").mkdir(parents=True)
    (sess / "quorum").mkdir(parents=True)
    (sess / "seats" / "adv-alive.handoff.md").write_text(
        "seat: adv-alive\ngeneration: 1\n", encoding="utf-8")
    card = sess / "quorum" / "adv-alive.md"
    card.write_text("# adv-alive card\n## Intro\ncarried\n", encoding="utf-8")
    win = root / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    bare = root / "remote.git"
    subprocess.run(["git", "init", "--bare", str(bare)], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(root), "init"], check=True,
                   capture_output=True)
    (root / ".gitignore").write_text(
        "remote.git/\nwindows.txt\nsessions/seats/\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin",
                    str(bare)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "fixture"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "push", "-u", "origin", "master"],
                   check=True, capture_output=True)
    # the ONE unpushed commit: HEAD is now ahead of origin/master by exactly 1
    (root / "unpushed.txt").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "unpushed.txt"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "unpushed"],
                   check=True, capture_output=True)
    # refresh the card so check 4 sees it NEWER than the unpushed commit
    import os as _os
    _os.utime(card, None)
    return root, win


def test_rotate_self_pushes_only_unpushed_blocker_and_continues(
        tmp_path, monkeypatch, capsys):
    """SL7.113 claim (1): with the ONE prepare blocker being check 1 measured
    `unpushed commits`, rotate-self PERFORMS the push through
    `_stops_push(label='unpushed')` (the ONE helper, never a new one), prints
    that push line, fires `_finish_pending_swap_on_push` (push: OK), and
    CONTINUES to the spawn — no refusal, exit 0. FALSIFIERS: a push on a
    multi-blocker refusal, a second push implementation, exit 3 instead of
    continuing."""
    root, win = _real_unpushed_rotate_repo(tmp_path)
    pushes = []

    def fake_push(root, label="stops"):
        # mirror the real `_stops_push` success line so the should-print push
        # line is asserted; label records which push site fired.
        pushes.append(label)
        print(f"{label} push: OK -- seat/x", file=sys.stderr)
        return None

    monkeypatch.setattr(rotate, "_stops_push", fake_push)
    finishes = []
    monkeypatch.setattr(rotate, "_finish_pending_swap_on_push",
                        lambda r, s, pl: finishes.append(pl) or "")

    def fake_spawn(**kw):
        # the post-spawn success check asserts the successor window exists
        # in `win` (the window_path seam reads it for the presence check).
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1,
                                         "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    import io as _io
    import contextlib as _c
    args = _rotate_self_args(window_path=str(win), session_ref="adv-alive-9")
    err = _io.StringIO()
    with _c.redirect_stderr(err):
        rc = rotate.cmd_rotate_self(args, root)
    err_text = err.getvalue()
    assert rc == 0, err_text
    # exactly ONE push, the 'unpushed' label (the stops/merge sites never ran)
    assert pushes == ["unpushed"], pushes
    assert "unpushed push: OK" in err_text
    # the deferred-swap helper fired AT this site with push: OK
    assert finishes == ["push: OK"], finishes
    # the refusal is gone: neither the blocked nor the refused line appears
    assert "rotate-self blocked:" not in err_text
    assert "rotate-self refused:" not in err_text


def test_rotate_self_unpushed_plus_dirty_refuses_no_push(
        prep_root, capsys, monkeypatch):
    """SL7.113 claim (3): TWO or more blockers (unpushed + dirty) -> the
    refusal is byte-identical to today (all names, exit 3) and NO push runs —
    the push seam is never called."""
    _seat_row_wt(prep_root, 3)   # own dirt blocks on a worktree seat
    gm = {("status", "--porcelain"): [" M rotate.py"],
          ("rev-parse", "--abbrev-ref", "HEAD"): ["seat/x"],
          ("rev-list", "--count", "@{u}..HEAD"): ["1"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    pushes = []
    monkeypatch.setattr(rotate, "_stops_push",
                        lambda root, label="stops": pushes.append(label) or None)
    rc = rotate.cmd_rotate_self(_rotate_self_args(), prep_root)
    err = capsys.readouterr().err
    assert rc == 3
    assert "rotate-self blocked: unpushed commits" in err
    assert "rotate-self blocked: dirty tree" in err
    assert "rotate-self refused: clear" in err
    assert pushes == [], pushes


def test_rotate_self_no_upstream_block_unchanged_no_push(
        prep_root, capsys, monkeypatch):
    """SL7.113 claim (1) NEVER-clause: a sole blocker whose clear sets an
    UPSTREAM (`no upstream for <branch>`) is NOT auto-pushed — its clear is
    `git push -u origin <branch>`, whose side effect (setting the upstream) is
    exactly what must stay a human BLOCK. Refusal unchanged, exit 3, push seam
    never called."""
    _seat_row(prep_root, 3)
    gm = {("status", "--porcelain"): [],
          ("rev-parse", "--abbrev-ref", "HEAD"): ["fresh/unpushed"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    pushes = []
    monkeypatch.setattr(rotate, "_stops_push",
                        lambda root, label="stops": pushes.append(label) or None)
    rc = rotate.cmd_rotate_self(_rotate_self_args(), prep_root)
    err = capsys.readouterr().err
    assert rc == 3
    assert "rotate-self blocked: no upstream for fresh/unpushed" in err
    assert "git push -u origin fresh/unpushed" in err
    assert pushes == [], pushes


def test_rotate_self_refused_push_exit3_no_spawn(
        tmp_path, prep_root, capsys, monkeypatch):
    """SL7.113 claim (2): a refused push stays a BLOCK by name —
    `rotate-self refused: <push error> — clear it, then re-run (nothing
    rotated)`, exit 3, nothing else touched (the spawn is never reached)."""
    _seat_row(prep_root, 3)
    gm = {("status", "--porcelain"): [],
          ("rev-parse", "--abbrev-ref", "HEAD"): ["seat/x"],
          ("rev-list", "--count", "@{u}..HEAD"): ["1"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    monkeypatch.setattr(
        rotate, "_stops_push",
        lambda root, label="stops": "push refused out: remote rejected")
    spawned = []
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: spawned.append(1) or (0, "echo hi"))
    rc = rotate.cmd_rotate_self(_rotate_self_args(), prep_root)
    err = capsys.readouterr().err
    assert rc == 3
    assert "rotate-self refused: push refused out: remote rejected — clear it," \
        in err
    assert "nothing rotated" in err
    assert spawned == [], "a refused push must never reach the spawn"


def test_rotate_self_dry_run_unpushed_prints_would_push_no_seam(
        prep_root, capsys, monkeypatch):
    """SL7.113 claim (4): `--dry-run` performs nothing and prints ONE line
    `(--dry-run) would push: <branch> (unpushed commits)` — the push seam is
    never called, exit 0 (the dry-run plan continues). FALSIFIER: a dry-run
    that pushes."""
    _seat_row(prep_root, 3)
    # prep_root has no rotations.md template -> resolve a parent template so
    # the (dry-run) plan tail past the would-push line does not refuse. A
    # step list of [handoff, spawn] keeps the dry-run plan short.
    monkeypatch.setattr(
        rotate, "_resolve_template",
        lambda *a, **k: ({"brief_file": "x.md", "steps": ["handoff",
                        "spawn"], "telemetry": []}, "parent", "test"))
    gm = {("status", "--porcelain"): [],
          ("rev-parse", "--abbrev-ref", "HEAD"): ["seat/x"],
          ("rev-list", "--count", "@{u}..HEAD"): ["1"],
          ("rev-list", "--count", "HEAD..origin/season/s2"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    pushes = []
    monkeypatch.setattr(rotate, "_stops_push",
                        lambda root, label="stops": pushes.append(label) or None)
    rc = rotate.cmd_rotate_self(_rotate_self_args(dry_run=True), prep_root)
    cap = capsys.readouterr()
    assert rc == 0, cap.err
    assert "(--dry-run) would push: seat/x (unpushed commits)" in cap.err
    assert pushes == [], "a dry-run must never push"
    assert "rotate-self blocked:" not in cap.err


# --- goal:g15.25 the dirty-tree gate on a shared MAIN checkout ---------------
# hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-blocks-only-on-
# dirt-the-merge-would-touch-foreign-dirt-is-named-never-a-block: on a MAIN
# post (row `worktree` empty) check 2 blocks ONLY when a dirty path is IN the
# merge touch-set (`git diff --name-only HEAD...origin/<sb>`, three-dot); a
# dirty path OUTSIDE it is another post's uncommitted work, named `foreign
# dirt`, never a block, never a stop_commit.


def test_prepare_check2_main_post_dirty_in_touch_set_blocks_naming_both(
        prep_root, capsys, monkeypatch):
    """FALSIFIER clause 1 — a dirty path IN the merge touch-set must still
    BLOCK on a MAIN post, named with BOTH facts (`<p>: dirty AND touched by
    origin/<sb>` in the dirty-tree line)."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post
    gm = {("status", "--porcelain"): [" M a.py", " M b.py"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): ["a.py"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] dirty tree: a.py" in out, out
    assert "touched by origin/season/s2" in out, out
    # b.py is foreign -> its own line, NAMED, never a blocker
    assert "[ok] foreign dirt (not in the merge): b.py" in out, out


def test_prepare_check2_main_post_dirty_outside_touch_is_foreign_no_block(
        prep_root, capsys, monkeypatch):
    """CLAIM (1)(2) — a dirty path OUTSIDE the touch-set on a MAIN post is
    NAMED `foreign dirt` on a never-blocking line: prepare exits 0, no
    dirty-tree BLOCK, no stop_commit path (nothing to refuse)."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post
    gm = {("status", "--porcelain"): [" M other.py"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): []}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[BLOCK]" not in out, out
    assert "[ok] dirty tree" in out, out
    assert "[ok] foreign dirt (not in the merge): other.py" in out, out


def test_prepare_check2_main_post_touch_unmeasured_scopes_own_paths(
        prep_root, capsys, monkeypatch):
    """CLAIM (7) / SM.84 measurement 1 & 2 — touch-set None (unmeasurable)
    on a MAIN post NO LONGER falls back to 'every dirty path blocks' (the
    old fallback REFUSED on foreign dirt: another post's card, HANDOFF.md,
    an untracked node draft). It scopes to the post's OWN paths: a foreign
    path is named `foreign dirt (merge target unmeasured)` on a never-
    blocking line (exit 0); the rotating post's OWN card still BLOCKS."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post, no touch answer
    gm = {("status", "--porcelain"):
              [" M HANDOFF.md",
               "?? .agi/nodes/hypothesis/other-post-draft.md"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[BLOCK]" not in out, out
    assert "[ok] dirty tree" in out, out
    assert ("[ok] foreign dirt (merge target unmeasured): HANDOFF.md "
            "[owner: unknown]" in out), out
    # the rotating post's OWN card still blocks on an unmeasurable MAIN post
    gm2 = {("status", "--porcelain"):
               [" M .agi/sessions/quorum/adv-alive.md"],
           ("rev-list", "--count", "@{u}..HEAD"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm2))
    rc2 = rotate.cmd_prepare(_args(), prep_root)
    out2 = capsys.readouterr().out
    assert rc2 == 3, out2
    assert "[BLOCK] dirty tree: .agi/sessions/quorum/adv-alive.md" in out2, out2
    assert "your own card" in out2, out2


def test_prepare_check2_sm84_dt_foreign_dirt_and_untracked_draft_pass(
        prep_root, capsys, monkeypatch):
    """SM.84 fixtures DT 00:18Z + DT 00:26Z on a MAIN post with an
    UNMEASURABLE merge target (the origin ref the gate never fetched): cron-
    owned comms + a rotation record (the churn class) plus HANDOFF.md, another
    post's card and another post's UNTRACKED node draft all PASS prepare and
    are NAMED -- the churn on the rotation-churn line, the rest as foreign
    dirt -- never a dirty-tree BLOCK (the old all-dirt fallback refused them)."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post, no touch answer
    gm = {("status", "--porcelain"): [
              " M .agi/comms/season-2/dm/other2.md",
              " M .agi/sessions/rotations/adv-alive.20260916T000000Z.json",
              " M HANDOFF.md",
              " M .agi/sessions/quorum/other-post.md",
              "?? .agi/nodes/hypothesis/other-post-draft.md"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"]}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[BLOCK] dirty tree" not in out, out
    assert ("[ok] rotation churn: .agi/comms/season-2/dm/other2.md, "
            ".agi/sessions/rotations/adv-alive.20260916T000000Z.json"
            in out), out
    assert ("[ok] foreign dirt (merge target unmeasured): "
            "HANDOFF.md [owner: unknown]" in out), out
    assert ".agi/sessions/quorum/other-post.md [owner: post other-post]" \
        in out, out
    assert ".agi/nodes/hypothesis/other-post-draft.md [owner: unknown]" \
        in out, out


def test_prepare_check2_worktree_post_dirt_blocks_even_outside_touch(
        prep_root, capsys, monkeypatch):
    """CLAIM (4) — a WORKTREE post (row `worktree` non-empty) is unchanged:
    its dirt is its own, ALL of it blocks; the partition never runs and no
    foreign line appears even when the touch-set would exclude the path."""
    g = prep_root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    row = {"name": "adv-alive", "role": "parent", "generation": 3,
           "worktree": "/some/wt"}
    (g / "seats.md").write_text(
        "---\ntype: config\nseats:\n  - " + json.dumps(row) + "\n---\n",
        encoding="utf-8")
    gm = {("status", "--porcelain"): [" M seats.md"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): []}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "[BLOCK] dirty tree: seats.md" in out, out
    assert "foreign dirt" not in out, out


def test_prepare_check2_main_post_behind_zero_touch_empty_no_block(
        prep_root, capsys, monkeypatch):
    """CLAIM (5) — behind == 0 (nothing to merge) -> the touch-set is empty
    -> the seat's dirty paths are all foreign -> no dirty-tree block; exit 0."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post
    gm = {("status", "--porcelain"): [" M seats.md"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): []}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[BLOCK]" not in out, out
    assert "[ok] foreign dirt (not in the merge): seats.md" in out, out


def test_prepare_check2_quoted_dirty_path_touch_set_real_fixture(
        prep_root, capsys):
    """FALSIFIER the last round missed (goal:g15.25, ONE failing clause): a
    dirty path git must QUOTE (`core.quotePath` — non-ASCII bytes, e.g.
    `caf\303\251.py` = café.py) must intersect the three-dot touch-set IFF
    the merge would actually touch it. On a REAL repo, (a) a quoted dirty
    file that `origin/season/s2` ALSO changed BLOCKS, named `touched by`;
    (b) the SAME quoted spelling dirty ONLY on the seat branch is FOREIGN and
    never blocks. Before the fix `_porcelain_path` stripped the quotes but did
    NOT decode git's octal escapes, so the dirty path `caf\\303\\251.py`
    never equalled the raw touch-set `"caf\\303\\251.py"` and scenario (a)
    passed block-less — the mechanical reason a rotation could clobber
    another post's uncommitted work.

    Both git sources are unquoted through the SAME `_git_unquote_path`, so
    the property that matters holds: dirty ∩ touch-set is non-empty when the
    merge would overwrite the file, for quoted names and plain ones alike."""
    def _build(root, season_adds_cafe):
        # the fixture graph seed the runs read (meter pin, handoff, card) —
        # mirroring _real_repo, but in a fresh sub-root per scenario so the
        # touch-set membership can differ between them.
        (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
        sess = root / "sessions"
        (sess / "seats").mkdir(parents=True)
        (sess / "quorum").mkdir(parents=True)
        (sess / "seats" / "adv-alive.handoff.md").write_text(
            "seat: adv-alive\ngeneration: 3\n", encoding="utf-8")
        (sess / "adv-alive.meter").write_text(
            "3\t/some/transcript.jsonl\n", encoding="utf-8")
        (sess / "quorum" / "adv-alive.md").write_text(
            "# SESSION HANDOFF — fixture\n\n## §3 🔴 NEXT COMMAND\nbash next\n",
            encoding="utf-8")
        _seat_row(root, 3)   # worktree "" -> a MAIN post
        _git(root, "init", "-q")
        _git(root, "remote", "add", "origin", str(root))
        _git(root, "config", "user.email", "test@example.com")
        _git(root, "config", "user.name", "test")
        _git(root, "config", "commit.gpgsign", "false")
        (root / "base.txt").write_text("base\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-qm", "base")
        base = _git(root, "rev-parse", "HEAD").stdout.strip()
        # season/s2 — ONE commit ahead of the merge base (+café.py in A)
        _git(root, "checkout", "-qb", "season/s2", base)
        if season_adds_cafe:
            (root / "café.py").write_text("season\n", encoding="utf-8")
        else:
            (root / "season.txt").write_text("season\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-qm", "season work")
        _git(root, "update-ref", "refs/remotes/origin/season/s2", "HEAD")
        # seat/x — ONE commit ahead of the merge base, diverged
        _git(root, "checkout", "-qb", "seat/x", base)
        (root / "seat.txt").write_text("seat\n", encoding="utf-8")
        if not season_adds_cafe:
            # a quoted-name file living ONLY on the seat branch -> it is dirty
            # AND outside the touch-set -> foreign, never a blocker.
            (root / "café.py").write_text("seat-only\n", encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-qm", "seat work")
        _git(root, "update-ref", "refs/remotes/origin/seat/x",
             _git(root, "rev-parse", "HEAD").stdout.strip())
        _git(root, "config", "branch.seat/x.remote", "origin")
        _git(root, "config", "branch.seat/x.merge", "refs/heads/seat/x")
        # the checked-out seat/x working copy: café.py, spelled how git quotes
        (root / "café.py").write_text(
            ("season-and-seat\n" if season_adds_cafe else "dirt\n"),
            encoding="utf-8")
        # re-touch the card so its mtime is NEWER than the last commit
        (sess / "quorum" / "adv-alive.md").write_text(
            "# SESSION HANDOFF — fixture\n\n## §3 🔴 NEXT COMMAND\nbash next\n",
            encoding="utf-8")
        return root
    # (a) quoted dirty path IS in the touch-set -> BLOCK, named `touched by`
    root_a = _build(prep_root / "a", season_adds_cafe=True)
    out_a = capsys.readouterr().out  # drain any earlier output
    rc_a = rotate.cmd_prepare(_args(), root_a)
    out_a = capsys.readouterr().out
    assert rc_a == 3, out_a
    assert "[BLOCK] dirty tree: café.py" in out_a, out_a
    assert "touched by origin/season/s2" in out_a, out_a
    # (b) same quoted spelling, dirty but NOT in the touch-set -> the dirty-
    # tree gate does NOT block on it: named FOREIGN on a never-blocking line.
    # rc here is 3 only because the auto-merge that --perform would run is
    # gated on a CLEAN tree (`perform and not dirty_paths`) and foreign dirt
    # still counts, so behind>0 then blocks; the dirty-tree check itself
    # passes, which is the claim (2) this falsifier guards.
    root_b = _build(prep_root / "b", season_adds_cafe=False)
    rc_b = rotate.cmd_prepare(_args(perform=True), root_b)
    out_b = capsys.readouterr().out
    assert "[BLOCK] dirty tree" not in out_b, out_b
    assert "[ok] dirty tree" in out_b, out_b
    assert "[ok] foreign dirt (not in the merge): café.py" in out_b, out_b
    assert rc_b == 3, out_b
    assert "[BLOCK] behind" in out_b, out_b


# SM.40 (hypothesis:l4-rotate-dirty-tree-refusal-partitions-blocking-from-
# foreign-dirt-like-the-merge-gate) — check 2 on a MAIN post names THREE
# classes, never one bare list: BLOCKING (merge touch-set PLUS the rotating
# post's OWN card), ROTATION CHURN (`_prepare_churn_path`'s paths — NAMED,
# never silently dropped: a hidden class was the bug), FOREIGN (owner guess
# parsed from the path). Measured defect: master-sensei 2026-09-16 10:04-10:05Z
# committed `.agi/tmp/kid1_thought.txt` and a root `orders-SL7.126-*.md`
# leftover to "unblock" a rotate because the bare list hid whose dirt it was.
# NO `.gitignore` rule: an ignore hides the class, the partition names it.
# The ROTATING ITER is NOT resolvable at prepare time (MEASURED: `_prepare_checks`
# receives only `seat`; dispatch.py sets AGI_LOOP to a loop ref like
# `hypothesis:...@s2`, never the `SL7.126` round slug), so no own-iter
# own-card BLOCK is shipped — the brief's F2 fallback (named iter owner) is.


def test_prepare_check2_untracked_kid_scratch_names_owner_unknown(
        prep_root, capsys, monkeypatch):
    """F1 — an untracked scratch file outside the merge
    (`.agi/tmp/kid1_thought.txt`) exits 0 and the foreign line NAMES it WITH
    an owner guess. Nothing in the path attributes it, so `[owner: unknown]`
    is the honest guess — never a bare path a reader commits to unblock."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post
    gm = {("status", "--porcelain"): ["?? .agi/tmp/kid1_thought.txt"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): []}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[BLOCK]" not in out, out
    assert ("[ok] foreign dirt (not in the merge): "
            ".agi/tmp/kid1_thought.txt [owner: unknown]") in out, out


def test_prepare_check2_orders_leftover_names_the_iter_owner(
        prep_root, capsys, monkeypatch):
    """F2 (the brief's fallback — the ROTATING iter is not resolvable at
    prepare time, see the block comment above) — a root-level
    `orders-<ITER>-*` leftover is FOREIGN, never a block, and its owner guess
    is parsed from the path: `iter SL7.126`, the master-sensei 10:05Z
    leftover a director committed to unblock."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post
    gm = {("status", "--porcelain"):
              ["?? orders-SL7.126-a00-fabd2604.md"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): []}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[BLOCK]" not in out, out
    assert ("orders-SL7.126-a00-fabd2604.md [owner: iter SL7.126]") in out, out


def test_prepare_check2_iter_session_dir_names_its_iter_owner(
        prep_root, capsys, monkeypatch):
    """The other iter-owned spelling the brief names: `.agi/sessions/
    iter-<ITER>/**` -> `iter <ITER>`. A kid's own scratch dir is never a
    block and never `unknown`."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post
    gm = {("status", "--porcelain"): ["?? .agi/sessions/iter-SL7.126/note.md"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): []}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "note.md [owner: iter SL7.126]" in out, out


def test_prepare_check2_rotation_churn_named_never_silently_dropped(
        prep_root, capsys, monkeypatch):
    """F3 — the churn class `_prepare_churn_path` matches (`.agi/comms/**`,
    `.agi/sessions/rotations/*.json`) is NAMED on one never-blocking
    `[ok] rotation churn:` line. Before SM.40 it was silently swallowed:
    prepare printed a plain `[ok] dirty tree` while the tree WAS dirty, and
    the class a reader most needs to recognise was invisible."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post
    gm = {("status", "--porcelain"):
              [" M .agi/sessions/rotations/sequence.json",
               "?? .agi/comms/season-2/dm/x--y.md"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): []}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[BLOCK]" not in out, out
    assert ("[ok] rotation churn: .agi/sessions/rotations/sequence.json, "
            ".agi/comms/season-2/dm/x--y.md") in out, out


def test_prepare_check2_main_post_own_card_blocks(
        prep_root, capsys, monkeypatch):
    """The own-card BLOCK: on a MAIN post a dirty `.agi/sessions/quorum/
    <seat>.md` is the rotating post's OWN uncommitted work — its owner guess
    IS this post — so it BLOCKS by name, even though the merge would not
    touch it. A post must not rotate over its own card."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post
    gm = {("status", "--porcelain"):
              [" M .agi/sessions/quorum/adv-alive.md"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): []}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 3, out
    assert ("[BLOCK] dirty tree: .agi/sessions/quorum/adv-alive.md"
            in out), out
    assert "your own card" in out, out


def test_prepare_check2_another_posts_card_is_foreign_named(
        prep_root, capsys, monkeypatch):
    """The boundary of the own-card BLOCK, asserted so the rule cannot widen:
    ANOTHER post's card is foreign, owner-named `post belam`, and never
    blocks."""
    _seat_row(prep_root, 3)   # worktree "" -> a MAIN post
    gm = {("status", "--porcelain"): [" M .agi/sessions/quorum/belam.md"],
          ("rev-list", "--count", "@{u}..HEAD"): ["0"],
          ("diff", "--name-only", "HEAD...origin/season/s2"): []}
    monkeypatch.setattr(rotate, "_git_maybe", _git_map(gm))
    rc = rotate.cmd_prepare(_args(), prep_root)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "[BLOCK]" not in out, out
    assert (".agi/sessions/quorum/belam.md [owner: post belam]") in out, out


# --------------------------------------------------------------------------
# SM.36 residue (2): prepare check 1 measures a post/loop branch against its
# LOCAL mirror ref `refs/agi/<kind>/<leaf>`, never `@{u}`/`origin/<branch>` --
# under SM.36 NO engine path advances an origin post head any more, so a seat
# rotation either read behind forever or a seat hand-pushed a head.
#
# Fixture: a REAL repo checked out on a v3 town-first post branch plus a bare
# origin; the mirror ref is created LOCALLY (`git update-ref`) so the check
# resolves it WITHOUT a fetch (prepare must never fetch -- fetch is a network
# WRITE). Fixture-only, bare-repo setup; `--delete-old` is never invoked.
# --------------------------------------------------------------------------


def _mirror_branch_repo(tmp_path, branch="core/season2/posts/adv-alive/main"):
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "--bare", "-q", str(origin)], check=True)
    repo = tmp_path / "repo"
    subprocess.run(["git", "init", "-q", "-b", branch, str(repo)], check=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / "README").write_text("x", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "init"], check=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin",
                    str(origin)], check=True)
    return repo


def _git_in(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)


def test_prepare_check1_counts_against_the_origin_mirror_ref(tmp_path):
    """Three faces of check 1 on a post spelling with a mirror ref, read
    from ORIGIN (SM.53 item 5 -- the local ref never exists on a live seat):
    (a) the origin mirror ref AT HEAD -> ok (0 unpushed);
    (b) the origin mirror ref BEHIND HEAD by one commit -> BLOCK, named by
        the mirror ref (not by a dead origin post head);
    (c) no origin mirror ref -> ok/unmeasured, NEVER the pre-fix
        `no upstream for <branch>` block (which counted a basis no engine
        path advances)."""
    repo = _mirror_branch_repo(tmp_path)
    mirror = "refs/agi/posts/adv-alive"

    # (a) origin mirror ref at HEAD -> 0 unpushed
    sha = _git_in(repo, "rev-parse", "HEAD").stdout.strip()
    assert _git_in(repo, "push", "origin",
                   f"{sha}:{mirror}").returncode == 0
    blocker, name, clear = rotate._prepare_checks(repo, "adv-alive")[0]
    assert blocker is False, (blocker, name)
    assert "unpushed commits vs refs/agi/posts/adv-alive" in name, name

    # (b) one commit ahead of the origin mirror -> BLOCK, by name
    (repo / "README").write_text("y", encoding="utf-8")
    _git_in(repo, "add", "-A")
    _git_in(repo, "commit", "-qm", "second")
    blocker, name, clear = rotate._prepare_checks(repo, "adv-alive")[0]
    assert blocker is True, (blocker, name)
    assert "unpushed commits vs refs/agi/posts/adv-alive" in name, name
    assert "HEAD:refs/agi/posts/adv-alive" in clear, clear

    # (c) no origin mirror ref -> ok/unmeasured, never `no upstream`
    assert _git_in(repo, "push", "origin",
                   f":{mirror}").returncode == 0
    blocker, name, clear = rotate._prepare_checks(repo, "adv-alive")[0]
    assert blocker is False, (blocker, name)
    assert "unmeasured" in name, name
    assert "no upstream for" not in name, name


def test_prepare_check1_origin_mirror_behind_head_and_unread(tmp_path):
    """SM.53 item 5, the falsifier: with NO local `refs/agi/posts/<seat>`
    ref (what a live seat actually has) check 1 measures ORIGIN's mirror.
    (i) an origin mirror tip BEHIND HEAD reports unpushed=True with a REAL
        count (`(1)`), where the PRE-FIX local-only read saw no local ref
        and returned unmeasured -- if this case no longer differs from the
        pre-fix one, the fix is inert;
    (ii) an origin read that FAILS reports unmeasured, never 'pushed'."""
    repo = _mirror_branch_repo(tmp_path)
    mirror = "refs/agi/posts/adv-alive"
    base = _git_in(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / "README").write_text("y", encoding="utf-8")
    _git_in(repo, "add", "-A")
    _git_in(repo, "commit", "-qm", "second")
    # the origin mirror tip is the BASE object, which IS present locally
    assert _git_in(repo, "push", "origin",
                   f"{base}:{mirror}").returncode == 0
    # (iii)/falsifier: no LOCAL mirror ref exists (the pre-fix read's basis)
    assert _git_in(repo, "rev-parse", "--verify",
                   mirror).returncode != 0

    blocker, name, clear = rotate._prepare_checks(repo, "adv-alive")[0]
    assert blocker is True, (blocker, name)      # (i) real unpushed count
    assert "unpushed commits vs refs/agi/posts/adv-alive" in name, name
    assert "(1)" in name or ": 1)" in name, name  # a MEASURED count, not 0
    assert "no local" not in name, name          # the pre-fix message is gone

    # (ii) an origin read that FAILS -> unmeasured, never 'pushed'
    _git_in(repo, "remote", "set-url", "origin", str(tmp_path / "nope.git"))
    blocker, name, clear = rotate._prepare_checks(repo, "adv-alive")[0]
    assert blocker is False, (blocker, name)
    assert "unmeasured" in name, name
    assert "vs refs/agi/posts/adv-alive" not in name, name


# SM.48 residue (1): `merge-up` is an act BY THE CALLER, never by the post it
# merged. The pre-fix call site stamped the resolved --post TARGET, so a
# Prime/SM merge-up of a director's post re-staled that DIRECTOR's card -- the
# captive loop reopened from the other side. Fixture-only: every git seam
# (merge, push, mirror, suite, lock, node counts, send) is injected, so no
# remote, no lock and no real merge is ever touched.
# --------------------------------------------------------------------------

def test_merge_up_stamps_the_caller_never_the_post_target(tmp_path, monkeypatch):
    """FALSIFIER: caller `prime` merges up post `director` -- the stamp must
    land on `prime`, and `director`'s stamp must NOT move. Exercised end to
    end through `cmd_merge_up` (not a source grep): the merge, push, mirror
    and suite seams are injected, the last-act seam is recorded."""
    import last_act as last_act_mod  # noqa: PLC0415

    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True)
    lock = tmp_path / "suite.lock"
    lock.write_text("")
    main = tmp_path / "main"
    main.mkdir()

    monkeypatch.setattr(rotate, "_caller_post",
                        lambda root: ("prime", {"seat": "prime"}, "test"))
    monkeypatch.setattr(rotate, "_find_seat", lambda root, seat: {"seat": seat})
    monkeypatch.setattr(rotate, "_rank_gate", lambda *a, **k: "")
    monkeypatch.setattr(rotate, "merge_up_plan", lambda root, post: {
        "main": main, "branch": "core/season2/posts/director/main",
        "target": "season2/main", "mirror": "refs/agi/posts/director"})
    monkeypatch.setattr(rotate, "_shared_graph_root", lambda root: graph)
    monkeypatch.setattr(rotate, "_closeout_branch", lambda cwd: "season2/main")
    monkeypatch.setattr(rotate, "_closeout_main_clean",
                        lambda m, b: (True, [], []))
    import verification  # noqa: PLC0415
    monkeypatch.setattr(verification, "acquire_suite_lock",
                        lambda groot: (lock, None))
    monkeypatch.setattr(rotate, "_merge_up_suite",
                        lambda root, m: (True, "ok", {"passed": 2}))
    monkeypatch.setattr(rotate, "_git_proc",
                        lambda cwd, *a: SimpleNamespace(returncode=0,
                                                        stdout="", stderr=""))
    monkeypatch.setattr(rotate, "_git_maybe", lambda cwd, *a: ["abc1234"])
    monkeypatch.setattr(rotate.branches, "mirror_and_prove",
                        lambda *a, **k: (True, "ok", {"ref": "refs/agi/x",
                                                      "sha": "deadbeefcafe"}))
    monkeypatch.setattr(rotate, "_origin_head_delete_gate",
                        lambda repo, branch, *, delete_old: ("dry", "no delete"))
    monkeypatch.setattr(rotate, "_node_counts", lambda groot: (1, 2, 3))
    monkeypatch.setattr(rotate, "_closeout_prime_seat", lambda root: "prime")
    import send as send_mod  # noqa: PLC0415
    monkeypatch.setattr(send_mod, "send", lambda *a, **k: ("prime", True))
    stamped: list[str] = []
    monkeypatch.setattr(last_act_mod, "touch_env",
                        lambda root, explicit=None: stamped.append(explicit) or "")

    args = SimpleNamespace(post="director", name=None, dry_run=False,
                           delete_old=False)
    assert rotate.cmd_merge_up(args, graph) == 0
    assert stamped == ["prime"], stamped            # the CALLER, not the post
    assert "director" not in stamped, stamped
    # the TARGET's own stamp is untouched on disk as well
    assert not (graph / "sessions" / "seats" / "director.last-act").exists()


# SM.48 residue (2): check 1 (`rev-list --count <upstream>..HEAD`) scoped by
# AUTHOR. A commit the acting checkout's own identity did not write -- a
# `grid_sync` cron commit on a shared trunk -- is not this seat's unpushed
# work and must not captive its rotation. Real fixture repo + bare origin.
# --------------------------------------------------------------------------

def _trunk_repo(tmp_path):
    """A real repo on `season2/main` with its upstream set and its
    user.email the SEAT's own identity; commits are then authored by
    whoever the test names (`grid <grid@agi>` for the cron)."""
    origin = tmp_path / "origin.git"
    repo = tmp_path / "repo"
    subprocess.run(["git", "init", "--bare", "-q", str(origin)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "season2/main", str(repo)],
                   check=True)
    _git_in(repo, "config", "user.email", "seat-x@agi")
    _git_in(repo, "config", "user.name", "seat-x")
    (repo / "seed").write_text("s\n", encoding="utf-8")
    _git_in(repo, "add", "-A")
    _git_in(repo, "commit", "-qm", "seed")
    _git_in(repo, "remote", "add", "origin", str(origin))
    _git_in(repo, "push", "-q", "-u", "origin", "season2/main")
    return repo


def _commit_as(repo, path, who):
    (repo / path).write_text("x\n", encoding="utf-8")
    _git_in(repo, "add", "-A")
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", f"{who} work"],
                   check=True, capture_output=True, text=True,
                   env={"PATH": "/usr/bin:/bin", "HOME": str(repo / ".."),
                        "GIT_AUTHOR_NAME": who, "GIT_AUTHOR_EMAIL": f"{who}@agi",
                        "GIT_COMMITTER_NAME": who,
                        "GIT_COMMITTER_EMAIL": f"{who}@agi"})


def test_prepare_check1_foreign_authors_unpushed_commit_never_blocks(tmp_path):
    """FALSIFIER: HEAD carries one unpushed commit authored by `grid` (the
    cron identity), not by this checkout's own identity -> check 1 must NOT
    block, and must NAME the foreign count rather than read a silent
    'pushed'. An unpushed commit of the seat's OWN is still a BLOCK with
    `git push` as the clear (SL7.113's auto-push path depends on it)."""
    repo = _trunk_repo(tmp_path)
    _commit_as(repo, "cron", "grid")

    blocker, name, clear = rotate._prepare_checks(repo, "seat-x")[0]
    assert blocker is False, (blocker, name)
    assert "unpushed commits vs refs/agi" not in name, name
    assert "other author" in name, name        # NAMED, never a silent pushed
    assert "grid" not in name                  # the count, not the identity
    assert "1" in name, name
    assert clear == "git push", clear

    # the pre-fix read (the unscoped count) really is 1 here -- the fixture
    # is not vacuous.
    raw = subprocess.run(["git", "-C", str(repo), "rev-list", "--count",
                          "@{u}..HEAD"], capture_output=True, text=True)
    assert raw.stdout.strip() == "1"

    # the seat's OWN unpushed commit still BLOCKS, exactly as before
    _commit_as(repo, "mine", "seat-x")
    blocker, name, clear = rotate._prepare_checks(repo, "seat-x")[0]
    assert blocker is True, (blocker, name)
    assert name == "unpushed commits", name
    assert clear == "git push", clear
