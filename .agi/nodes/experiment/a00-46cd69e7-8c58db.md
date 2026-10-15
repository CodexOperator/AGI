---
id: experiment:a00-46cd69e7-8c58db
mint_id: d7d1d8afa39e40fa9e5cbe30a9abc7f2
type: experiment
parents:
  - hypothesis:l4-the-no-spawn-declined-branch-is-reached-by-its-caller-and-the-test-recorder-returns-no-fake-pid
next_edges: []
confidence: 0.9
edited_by: a00-f5d4d4aa
evidence_runs:
  - experiment:a00-46cd69e7-8c58db
loop: hypothesis:l4-the-no-spawn-declined-branch-is-reached-by-its-caller-and-the-test-recorder-returns-no-fake-pid@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 88e83c5dcaf9b024
season: 2
title: A00 46cd69e7 8c58db
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-46cd69e7-8c58db

## Experiment

g15.25 FIX-ONLY build claim (SL7.65 on hypothesis:l4-the-no-spawn-declined-branch-...).

**Pre-fix measured** (function name): helper `_spawn_rotate_self` had NO_SPAWN
branch at rotation_alert.py:812-820 returning None under `AGI_HOOK_NO_SPAWN`;
the caller gate (e) in `_gated_rotate` (:903-908) also checked it and returned
"no-spawn" first — TWO checks, the helper's branch unreachable through its only
caller (dead code "that reads as the fix"). Recorder `_no_real_spawn`
(test_rotation_alert.py:79,84) returned FakeProc with pid 12345; the latch test
test_dead_latch_is_released_and_rerotates asserted `_latch_holder_pid == 12345`
(:1116) — a recorder path could latch a real-looking 12345.

**Implemented (one check, one recorder change, one new test):**
1. Deleted the helper's NO_SPAWN branch; gate (e) in `_gated_rotate` is now the
   ONE check (reached end-to-end through the production path). Helper docstring
   and the `_Popen` seam comment name gate (e) in the caller as the one guard.
2. `_no_real_spawn` returns pid `_RECORDER_PID = 2**24` (16777216) — a
   provably-DEAD sentinel (beyond OS pid_max, so `_pid_alive` reads it dead): a
   latch the recorder path leaves can never hold a generation against a phantom,
   and no test latches a real-looking 12345.
3. Added test_one_no_spawn_check_lives_in_gate_e_not_the_helper: a DIRECT call to
   `_spawn_rotate_self` under NO_SPAWN now REACHES the seam (no second check),
   pid(sentinel) is provably dead, and sentinel != 12345.

**Ran:** `python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q`.

## Evidence

36 passed in 8.90s (full file). Targeted subset
(-k "one_no_spawn_check or no_spawn or dead_latch or popen_seam"): 5 passed.
Baseline was green (4 passed for the no_spawn/latch/popen subset) BEFORE the
change; the out-of-process test (test_out_of_process_no_spawn_declines_and_
writes_no_latch) and the in-process no-spawn test still pass unmodified and
still assert "declined: AGI_HOOK_NO_SPAWN" — proving gate (e) remains the check
reached end to end. `grep AGI_HOOK_NO_SPAWN rotation_alert.py` now hits only the
single gate (e) `if` plus doc/comment mentions — one check, not two.

The phantom-12345 falsifier is closed: the only test that asserted a 12345 latch
now asserts `_RECORDER_PID` (16777216), and the recorder can no longer leave a
real-looking pid in a latch. No other repo test references the removed branch or
the old recorder pid.

## Agent Notes
g15.25 one-check fix: deleted _spawn_rotate_self NO_SPAWN branch (gate e in _gated_rotate is now the ONE check); _no_real_spawn returns provably-dead sentinel 2**24, no 12345 latch anywhere; test_rotation_alert.py 36/36 pass incl new one-check reach test.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f5d4d4aa, SL7.65) — accepted, not demoted. (1) INSTRUCTION: "either the helper NO_SPAWN branch is deleted (gate e is the one check, named in the helper docstring) or gate e is removed and the helper branch is the one check reached end to end — one check, not two; the recorder returns a FakeProc whose pid is a proved-dead or sentinel value that the latch writer refuses, or the recorder never reaches the latch write; the out-of-process test still passes." (2) MACHINE, cited: rotation_alert.py:802-820 helper now has no env check; gate (e) at :901 is the ONLY os.environ.get(AGI_HOOK_NO_SPAWN) if in the module (other hits are doc/comment); test_rotation_alert.py:63 _RECORDER_PID = 2 ** 24, :91 recorder returns it, :1128 asserts latch holder == _RECORDER_PID, :1290 new one-check test asserts a direct helper call REACHES the _Popen seam under NO_SPAWN. Built and ran: python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q -> 36 passed in 7.17s here, including the out-of-process no-spawn test. /proc/sys/kernel/pid_max = 4194304 = 2**22, so 2**24 (16777216) can never be a live pid and hook._pid_alive(_RECORDER_PID) is False. (3) NEAR MISS: deleting the dead branch and declaring "one check" on the comment alone would satisfy the words while the one-check property stayed untested; and a 999999-style sentinel would pass the words while remaining live on a box whose pid_max is 4194304 — the recorder latch would read held. The kid avoided both: a beyond-pid_max sentinel and a behavioral reach test. (4) DEVIATION: none.
<!-- THOUGHT:END -->
