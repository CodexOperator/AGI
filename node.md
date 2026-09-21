---
id: hypothesis:l4-conftest-tmux-guard
mint_id: be8c4c487cc34bd884906179aecb7a7a
type: hypothesis
parents:
  - idea:l4-conftest-tmux-guard
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: 2900d3820bb89392
season: 2
testable_claim: "Moving the tmux-nudge guard from test_send.py's file-local autouse fixture into extensions/agi/tests/conftest.py as a PROJECT-WIDE autouse fixture reduces real `tmux` subprocess invocations across the WHOLE test suite to zero, while (a) test_send.py's three `_fake_tmux` tests still exercise the real `_nudge_window` logic via their own per-test monkeypatch override (which must still win over the autouse default), and (b) every legitimate non-tmux subprocess call elsewhere in the suite -- in particular test_season.py's and test_rotate.py's real `git` invocations against a tmp_path sandbox -- is left untouched and still passes. Falsifiable via a fake `tmux` binary on PATH that logs its own invocations and exits 1: before, real tmux calls measured at test_send.py 0, test_mail_alert.py 6, test_rotate.py 2, test_season.py 2, full suite 11 (director's baseline, all against the live agi-rc session). After: the same measurement across the FULL suite must show zero, the full suite must still pass, AND the three _fake_tmux tests plus every git-based test in test_season.py/test_rotate.py must still individually pass. If the guard is instead a blanket 'raise on any non-tmux subprocess call' applied globally -- which would break the real git calls test_season.py and test_rotate.py's own fixtures depend on -- the hypothesis as stated is false and a selective, tmux-only interception (pass every non-tmux call through to the real subprocess) is required instead."
thought_session: sanctuary-helper-6b
title: A tmux-only, project-wide conftest.py guard zeroes real tmux calls suite-wide without breaking git-based tests
---
<!-- BODY:BEGIN -->
# hypothesis:l4-conftest-tmux-guard

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.5x brief -- widen the L4.10 tmux guard from one file to the whole suite

Assigned by sanctuary-director gen III (seat-sanctuary-director-4e), approved
by the Prime. Widens `goal:g15.3` / `hypothesis:l4b23-fixture-leak` (CLOSED
proved, but scoped to test_send.py only: `experiment:a00-7251f7a9-424a5f`) --
that round fixed the file the owner actually reported; it never claimed to
cover the rest of the suite, and it doesn't: `conftest.py` today carries only
the AGI_TIER collection gate (goal:g15.6) and no tmux guard at all.

WHY IT MATTERS: nothing is typed into a live pane today only because these
fixtures' recipient/window names ("seat-a", "tier2-directors", "sender", ...)
don't collide with a real live window. Name one "sanctuary-helper" and it
types into a real terminal. Until this lands, `--suite` stays opt-in and the
"until L4.10 lands" text in verification.py stays -- do NOT touch that file
or commands.py (L4.52 owns them right now) or write.py (L4.41 owns it).
conftest.py and the test modules under extensions/agi/tests/ are yours alone.

CURRENT STATE, read from the code (not guessed):
- `extensions/agi/tests/test_send.py:77-106` defines `_SafeSubprocess` (a
  stand-in whose `.run()` answers tmux calls with rc 1 and RAISES
  AssertionError on any non-tmux call) and an autouse fixture `_no_real_tmux`
  that does `monkeypatch.setattr(send_mod, "subprocess", _SafeSubprocess())`
  -- swapping test_send.py's OWN `send_mod` module-alias's subprocess
  reference. This protects ONLY tests in test_send.py that go through THAT
  specific `send_mod` object.
- `extensions/agi/tests/conftest.py` (goal:g15.6) has zero fixtures today --
  only a `pytest_cmdline_main` collection hook. No tmux guard exists there.

🔴 WHY A LITERAL "MOVE" WOULD BREAK OTHER TESTS -- READ BEFORE YOU START:
`test_mail_alert.py` loads its OWN separate `send_mod` via the same
`importlib.util.spec_from_file_location("send", BIN / "send.py")` trick --
`module_from_spec` mints a FRESH module object per file, so patching
`send_mod.subprocess` in ONE file's namespace does not touch another file's
`send_mod`. That is consistent with the baseline below: test_mail_alert.py
still leaks 6 real tmux calls today despite test_send.py's existing guard.
WORSE: `test_rotate.py` and `test_season.py` do a plain `import subprocess`
(no send_mod alias) and BOTH contain real, legitimate, currently-passing
`subprocess.run(["git", ...])` calls against a tmp_path sandbox (confirmed
by grep -- e.g. test_season.py:651-654, test_rotate.py:813-820) alongside
whatever reaches tmux for real (their 2-and-2 baseline below). If you
relocate `_SafeSubprocess` UNCHANGED -- its "raise on any non-tmux
subprocess call" behaviour intact -- into a conftest.py autouse fixture,
EVERY one of those git calls starts raising AssertionError and you break
tests that pass today. This is a correction to the assignment as literally
worded ("move _SafeSubprocess, including its assertion"), made here rather
than discovered by you mid-round: the assertion's job was sound for
test_send.py alone (which has no legitimate non-tmux call to protect) and is
wrong once the same object guards files that do. Flag this in your own
report; do not silently drop it without saying so.

CHANGE, the actual engineering decision:
1. In `conftest.py`, add a project-wide `autouse` fixture that intercepts
   subprocess calls whose argv starts with `"tmux"` (fake a safe rc-1
   CompletedProcess, exactly as `_SafeSubprocess` does today for tmux) and
   PASSES EVERY OTHER CALL THROUGH to the real `subprocess.run` unchanged --
   no assertion, no raise. Patch at a level that reaches every module's tmux
   calls uniformly: patching each file's own `send_mod`/`rotate`-alias
   subprocess reference one by one defeats the "project-wide" point (that is
   the exact per-file-copy shape being replaced); patching the true
   `subprocess.run` (the real stdlib module, the one every file's `import
   subprocess` and `send_mod`'s own internal `subprocess` both ultimately
   resolve through) is the level that actually covers send.py, rotate.py,
   season.py and mail_alert.py's tmux calls in one fixture. Confirm this
   reasoning against the actual code before committing to it -- you have
   read access to all four files' subprocess usage; use it rather than
   guessing at the right patch target.
2. In `test_send.py`, REMOVE `_SafeSubprocess` and `_no_real_tmux` (moved,
   not copied) -- keep `_fake_tmux` and the three tests that call it
   unchanged; their `monkeypatch.setattr` runs in the test body, after the
   autouse fixture's setup, and must still win (this is a setup-phase vs.
   test-body-phase ordering property, not something tied to which file
   defines the autouse fixture -- verify it still holds, don't just assume).

FALSIFIER, the director's own measurement harness, verbatim -- use exactly
this to measure both BEFORE (confirm the baseline) and AFTER (confirm zero):

    mkdir -p <scratch>/fakebin
    cat > <scratch>/fakebin/tmux  <<'EOF'
    #!/bin/bash
    echo "$@" >> "$TMUX_CALL_LOG"
    exit 1
    EOF
    chmod +x <scratch>/fakebin/tmux
    PATH="<scratch>/fakebin:$PATH" TMUX_CALL_LOG=<log> python3 -m pytest extensions/agi/tests/ -q

Non-destructive: nothing can reach a real pane through a fake that exits 1.
BASELINE (director's measurement, cite it, you do not need to re-derive it):
test_send.py 0 invocations, test_mail_alert.py 6, test_rotate.py 2,
test_season.py 2, FULL SUITE 11 -- all `tmux list-windows -t agi-rc` against
the live session. PROVED bar: the same harness records ZERO across the FULL
suite (not one module -- the whole directory) and the full suite still
passes at (at least) its current count.

The full-suite run above is PRE-APPROVED for this round specifically -- it
is the falsifier the Prime and director named, not a bare directory run you
are asking permission for. Run it. The `AGI_TIER=kid` collection gate
(goal:g15.6) does not block a bare directory run for you as a PARENT-tier
process (AGI_TIER is unset outside a kid) -- if you dispatch a sub-kid,
remember it WILL be gated and must run scoped or with `AGI_TIER` unset.

VERIFY, in order: (1) the falsifier above, before and after, both numbers
in your evidence; (2) `python3 -m pytest extensions/agi/tests/test_send.py -q`
-- the three `_fake_tmux` tests specifically pass, proving override
precedence survived the move; (3)
`python3 -m pytest extensions/agi/tests/test_season.py extensions/agi/tests/test_rotate.py -q`
-- every git-based test in both files still passes, proving the guard is
selective (tmux-only) and did not swallow legitimate subprocess calls; (4)
`tmux list-windows -t agi-rc` yourself, real, read-only, before you finish --
confirm nothing in your own test run typed into a live window (belt and
suspenders alongside the fake-binary harness).

KID CEILING: 2 -- one for the implementation, one for review/cleanup only if
the first kid's diff needs it, not for parallel exploration. This is more
subtle than a pure relocation (see the correction above); say plainly in
your report whether you found further call sites the baseline's 4-file
count above did not anticipate.

DO NOT: touch `extensions/agi/bin/verification.py` or `commands.py` (L4.52
owns them right now) or `extensions/agi/bin/write.py` (L4.41 owns it). Do
not touch any file outside `extensions/agi/tests/` (conftest.py and the test
modules only). Do not add a build node -- chain + evidence only, no build.
Do not run `git add -A`; stage only the files you actually changed. Do not
run `grid.py commit --all` on this seat branch (branch-blind refusal by
design) -- your worktree's protocol ends at `git commit` + `git push` on
your own branch/worktree; the parent director merges upward.

REPORT: write one `experiment` node whose parents is this hypothesis, with a
verdict on the testable claim (`proved` only if the full falsifier -- zero
real tmux across the whole suite, full suite still green, the three
_fake_tmux tests green, the git-based tests in test_season.py/test_rotate.py
green -- actually held; otherwise `inconclusive_lean_proved`/`disproved`
with your reasoning). `evidence_runs` must resolve to real node ids; your own
experiment counts once it exists. List every verify command you ran and its
actual output. Say plainly whether you kept the corrected (selective,
pass-through) design from this brief or found a better one, and why.

POST-DISPATCH REVIEW REQUIREMENT (director-confirmed correction; the kid brief above predates this and still says to REMOVE test_send.py's _SafeSubprocess/_no_real_tmux -- that instruction is now WRONG, not re-dispatching since the brief was already baked when this landed):

The correct design is BOTH layers, composed, not one replacing the other. KEEP test_send.py's existing STRICT _SafeSubprocess (raise on any non-tmux subprocess call) exactly where it is, scoped to send_mod, as send.py's own drift protection -- a pass-through conftest guard cannot catch send.py growing a future non-tmux subprocess call unnoticed; only the strict per-module assertion can. ADD the project-wide selective (tmux-only, pass-through) guard in conftest.py underneath/alongside it -- they compose via ordinary fixture-override ordering, the same way the three _fake_tmux tests already override the autouse default today.

AT REVIEW: if the landed round removed test_send.py's strict guard (as the brief literally instructed), name that as a regression explicitly, even if the falsifier goes fully green. Zero real tmux calls plus a passing full suite is still a WORSE tree than today if it also drops send.py's drift protection -- do not let a green run wave this through.

HELPER PRE-DISPATCH L4.258 (sanctuary-helper 3baf36, 2026-09-11 21:1xZ, fix-only, the point's 20:57Z order from PRIME XI's mur-40 verdict; second of three, cut after L4.257). TWO DEFENCE-IN-DEPTH GAPS, read on the seat tree: (1) test_heal_sweep.py `test_watch_once_calls_sweep_exactly_once` drives `heal.main()` `watch --once`, and a watch pass runs `_repair_stranded_wakes` + `_watch_seats` BEFORE `_sweep_finished_worktrees` (heal.py ~776-790); `_watch_seats` -> `_all_windows()` (heal.py ~907) shells out to `tmux list-windows -a` whenever `AGI_WINDOW_PATH` (heal.WINDOW_PATH_ENV, ~875) is unset, and a dead-looking seat row would continue to the respawn half's `tmux new-window` (~1129). The test today reaches the live tmux only through conftest.py's autouse `_no_real_tmux` (~322-362); it names NO seam of its own -- one autouse regression away from touching `agi-rc`. (2) NOTHING TESTS THE GUARD ITSELF: no test asserts `_no_real_tmux` is in force, so the fixture can be renamed, narrowed or dropped and every suite stays green while the next tmux-touching test lands on the live session (the way test_send.py's file-local guard once did). THE FIX, two small edits and nothing else: (a) in `test_watch_once_calls_sweep_exactly_once` ONLY (a sibling round, L4.257, is editing OTHER functions and fixtures in the same file -- touch no other line, append nothing at EOF): `monkeypatch.setenv('AGI_WINDOW_PATH', str(tmp windows file))` with an empty (or one `@1 nobody` line) file written by the test, plus one assertion that the seam was honoured (`heal._all_windows() == []` / the one row) so the seat scan of that pass reads the file and never a tmux subprocess, and a one-line docstring clause naming why. (b) NEW FILE `extensions/agi/tests/test_conftest_guard.py` with ONE test `test_conftest_tmux_guard_is_in_force`: `subprocess.run(['tmux', 'display-message', '-p', '#S'], capture_output=True, text=True)` from inside a test returns the guard's `CompletedProcess` -- `returncode == 1`, `stdout is None` (the guard builds `CompletedProcess(cmd, 1)` with no stdout; a REAL tmux with capture_output would return a str, and a missing tmux binary would raise FileNotFoundError, so the test fails either way if the autouse fixture is gone), and `subprocess.run.__name__ == '_guarded_run'`; plus the negative half: a NON-tmux call (`['true']` or `[sys.executable, '-c', 'print(1)']`) still runs for real (`returncode == 0`, stdout '1\n') -- the guard is selective by design. conftest.py and heal.py UNTOUCHED. FALSIFIER, prove it red first and paste the line: temporarily run the new test with `-p no:cacheprovider --noconftest`-style isolation or by monkeypatching `subprocess.run` back to the real one inside a throwaway probe -- it must FAIL there and PASS under the autouse guard. Run `pytest extensions/agi/tests/test_conftest_guard.py extensions/agi/tests/test_heal_sweep.py extensions/agi/tests/test_send.py -q` and report the count. CEILING 1 kid. Never touch the live tmux session; never name or run the streamer-stub's commands. Commit in the round's own worktree; the parent merges its kid with `git merge --no-ff`.

HELPER HARVEST L4.258 (sanctuary-helper 3baf36, 2026-09-11 21:5xZ, merged into seat/sanctuary-helper@s2 from loop/hypothesis-l4-conftest-tmux-guar-a00-95899b3c@s2; parent a00-95899b3c, kid a00-08f5186c verdict proved, parent review upheld). LANDED exactly as briefed, 3 files: NEW extensions/agi/tests/test_conftest_guard.py -- `test_conftest_tmux_guard_is_in_force` asserts a tmux subprocess call from inside a test is answered by the guard (`subprocess.run.__name__ == '_guarded_run'`, rc 1, stdout None) and a non-tmux call still runs for real (rc 0, stdout '1\n'); the kid proved it RED under `--noconftest` (1 failed) then green. `test_watch_once_calls_sweep_exactly_once` now writes a one-line window file, sets AGI_WINDOW_PATH to it and asserts `heal._all_windows() == [('@1', 'nobody')]` before the pass -- the seat scan of a watch --once pass reads the file, never `tmux list-windows -a` / `new-window`, even with the autouse guard gone. conftest.py and heal.py untouched. Director checks on the seat: pytest test_conftest_guard.py test_heal_sweep.py test_heal_watch.py test_send.py = 210 passed; links 0 broken; goals round-trip byte-identical; write_guard rc 0 (WARN on the merged-in kid node, expected); viewport PASS. No deviation from the brief; no residue. Sibling L4.257 edits other functions of test_heal_sweep.py -- its harvest re-runs the same files.
