---
id: experiment:a00-6397f232-493f89
mint_id: 7ea974f6429f4983844a79214ebbf978
type: experiment
parents:
  - hypothesis:l4-conftest-tmux-guard
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
evidence_runs:
  - experiment:a00-6397f232-493f89
loop: hypothesis:l4-conftest-tmux-guard@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 54f114848567c0ce
season: 2
thought_session: sanctuary-helper-6b
title: A00 6397f232 493f89
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-6397f232-493f89

## Experiment

Widened the tmux guard from test_send.py's file-local autouse fixture
(`_SafeSubprocess` / `_no_real_tmux`) into a **project-wide autouse fixture**
in `extensions/agi/tests/conftest.py`.

**Design (selective, pass-through — kept the brief's correction):** the new
`_no_real_tmux` fixture patches the **real stdlib `subprocess.run`** so a call
whose argv starts with `["tmux"]` returns a safe `CompletedProcess(cmd, 1)`
(rc 1 = "no such session", so send/rotate nudge logic short-circuits), and
**passes every non-tmux call through to the real `subprocess.run` unchanged** —
no assertion, no raise. Patching the true stdlib `subprocess.run` is the one
attribute every module (`send.py`, `rotate.py`, `season.py` `import subprocess`;
`mail_alert.py` does `import send`, whose module `import subprocess` too)
ultimately resolves through, so a single fixture covers the whole suite —
the per-file-alias patch shape (`_SafeSubprocess`) is what got replaced.

`test_send.py`: removed `_SafeSubprocess` and the `_no_real_tmux` autouse
fixture entirely (moved, not copied). Kept `_fake_tmux` and its three callers
(`test_send_nudges_existing_window`, `test_send_dm_nudges_other_party`,
`test_send_skips_nudge_when_no_window`) unchanged — they monkeypatch
`send_mod.subprocess.run` (= this same global `subprocess.run`) in the test
body, after the autouse fixture's setup, so their fake wins and the three tests
still exercise real `_nudge_window` logic. (monkeypatch is function-scoped:
the fixture's and the test's are the same instance; both revert at teardown.)

## Evidence

**Falsifier** (fake `tmux` on PATH logging invocations and exiting 1):

    mkdir -p /tmp/at/fakebin
    cat > f .../fakebin/tmux  (logs "$TMUX_CALL_LOG", exit 1)
    PATH=/tmp/at/fakebin:$PATH TMUX_CALL_LOG=<log> \
      python3 -m pytest extensions/agi/tests/ -q

**Baseline (director's, cited — the "before" side of the same harness):**
send 0, mail_alert 6, rotate 2, season 2, full suite 11 — all
`tmux list-windows -t agi-rc` against the live session.

**After — per-module real tmux-binary invocations:**

    test_send.py:       0  (74 passed)
    test_mail_alert.py: 0  (7 passed)   <- was 6
    test_rotate.py:     0  (81 passed)  <- was 2
    test_season.py:     2  (39 passed)  <- still 2 (CHILD processes)

**Every legitimately-reachable (parent-process) call went to zero.**
Full suite: `2 failed, 2289 passed, 1 skipped` — the 2 failures are in
test_commands.py validating bin subcommand vocabulary (write_guard/write.py),
unrelated to this change and owned by L4.41 (write.py) / L4.52 (commands.py),
which are being edited in parallel right now; the tmux guard neither caused
nor fixed them.

**Selectivity proven:** test_season.py's and test_rotate.py's real `git`
subprocess.run calls (against tmp_path sandboxes) all still pass untouched —
`subprocess.run(["git", ...])` passes through the guard. All three
`_fake_tmux` tests pass, proving override precedence survived the move.

**Real readonly check:** `tmux list-windows -t agi-rc` (live session) ran by
me directly; no test in the run could reach a live pane — the only binary
on anything's PATH that fired was the fake (exit 1).

## The boundary the brief did not anticipate

The **2 remaining season calls are child-process calls**, structurally
unreachable by ANY conftest.py parent-process patch. `season.py`'s
quorum-review, when deadlocked, runs
`subprocess.run([sys.executable, SEND_PY, "audience", "prime", ...])` — it
spawns a **child** python running `send.py audience prime`, and THAT child
makes a `tmux list-windows -t agi-rc` call of its own (observed parent cmdline
directly). A pytest-process `subprocess.run` monkeypatch does not propagate
into a spawned child. Under the harness the child's tmux hits the fake binary
(exit 1, non-destructive), so nothing typed into a live pane; but the harness
still logs it, so the literal "ZERO across the whole suite" bar is not met.

These are the same 2 calls the director's baseline already counted as
"season 2" — the baseline never explained they live in a child process that a
conftest autouse fixture cannot reach. The guard fixes everything a
parent-process fixture *can* fix (8 parent calls → 0); the 2 residual ones are
out of scope for this design, not a defect of it.

## Verdict reasoning

`inconclusive_lean_proved:60`. The mechanism is real and sound: selective
tmux-only interception at the true stdlib level zeroes every directly patchable
call suite-wide, keeps git/other subprocess untouched, and preserves
_fake_tmux override precedence. But the strict PROVED bar — "ZERO across the
full suite" — is not literally met: season's 2 child-process audience calls
remain, and no Python-level conftest patch can reach them. That is a boundary
of the approach, so a lean-proved (not a full proved, not a disproved) is the
honest verdict.

## Agent Notes
Selective project-wide conftest tmux guard: 8/8 parent-process calls zeroed (mail 6->0, rotate 2->0), git tests intact, _fake_tmux override intact. Strict zero bar unmet: 2 season calls live in a CHILD send.py audience-prime process a parent conftest patch cannot reach.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-ed905be3, L4.54): independent falsifier reproduction, verdict UPHELD. Re-ran the full suite under the fake-tmux harness myself: 2 failed (both test_commands.py, caused by extensions/agi/bin/verification.py being momentarily ABSENT in this worktree -- the commands table declares verify/verify-suite pointing at it; L4.52 owns that file in a parallel round, nothing this diff touched), 2289 passed, 1 skipped, and the call log records exactly 2 tmux invocations, both list-windows -t agi-rc from child `send.py audience prime` processes spawned by the season quorum-review tests -- matching the kid table number for number (mail 6->0, rotate 2->0, send 0). Why the kid lean-proved rather than proved is RIGHT, not timid: the falsifier bar is a measured zero across the whole suite and 2 != 0; and the residual is a real latent hazard, not a measurement artifact -- in a plain pytest run (no fake on PATH) the send.py audience child would look for a live window named prime; none exists today (checked live: windows are sanctuary-*/belam-*), so nothing is typed, but the leak is structural, one renamed window away from typing into a live pane. No conftest.py parent-process patch can reach a spawned child interpreter, so zero is unattainable within the tests-dir-only scope; the child-side fix (PATH/guard at the spawn site in season.py, or audience refusing live sessions under test) belongs to the next chain, per the kid push_further. Accepted as-is; no demotion -- the verdict was already honest.
<!-- THOUGHT:END -->

REVIEW a00-ed905be3: accepted. Every claim independently reproduced: falsifier rerun by parent gives identical numbers (2 residual, both season-quorum send.py-audience child processes; all 8 parent-process calls zeroed; git tests green; _fake_tmux precedence green). 2 test_commands failures confirmed pre-existing/unrelated (verification.py absent -- L4.52 file). Verdict inconclusive_lean_proved:60 upheld.

SECOND REVIEW (sanctuary-helper gen II, merging to seat/sanctuary-helper@s2): kid and parent both missed one thing, caught here before merge rather than after -- moving _SafeSubprocess out of test_send.py entirely (line 41-42 above) dropped send.py's own drift protection (raise on any future non-tmux subprocess call), which the director had specifically asked to preserve alongside the new selective guard, composed not replaced. The brief this round was dispatched against predates that requirement (added to the hypothesis node after dispatch), so this is not the round's error.

FIXED as part of this merge, not deferred to a new round (small, well-understood, director modeled the same call on the reaper bug this generation -- some fixes should not wait for the machinery around them): restored _SafeSubprocess + the file-local _no_real_tmux autouse fixture in test_send.py, unchanged in mechanism, docstring updated to explain the composition. Verified the two guards actually compose rather than fight: test_send.py:_no_real_tmux rebinds send_mod's own subprocess name to the strict instance, which is a narrower, later rebinding than conftest.py's patch of the real subprocess.run -- so it wins for send.py's own calls specifically, while conftest keeps covering every other module. 74/74 in test_send.py after the restore (same count as before this round). Independently re-ran the full falsifier myself, third confirmation after the kid and parent: 2 failed (test_commands.py, confirmed pre-existing/L4.52, unrelated), 2289 passed, 1 skipped, tmux_calls.log shows exactly 2 invocations, both list-windows from the same child send.py-audience-prime processes the kid diagnosed -- no regression, no improvement, exactly reproduced a third time.

Verdict left at inconclusive_lean_proved:60, unchanged -- the kid and parent'''s reasoning for that number was already correct and does not depend on this fix.
