---
id: experiment:a00-de1fa5c2-f1995a
mint_id: 5f8ab2bfa1b44196b670f4dcce3e4152
type: experiment
parents:
  - hypothesis:l4-the-belam-cap-record-is-planned-first
next_edges: []
confidence: 0.95
edited_by: a00-3c16a703
evidence_runs:
  - experiment:a00-de1fa5c2-f1995a
loop: hypothesis:l4-the-belam-cap-record-is-planned-first@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 147f90e6b862a2ac
season: 2
title: A00 de1fa5c2 f1995a
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-de1fa5c2-f1995a

## Experiment

Goal (L4.150): the belam-cap record test
`test_belam_cap_record_planned_entry_when_term_interrupted` — added by the
previous kid to prove the PLANNED belam entry survives an interrupted reap —
left the shared pytest process POISONED: `rotate.cmd_rotate_self` sets SIGHUP /
SIGTERM / SIGPIPE to SIG_IGN (rotate.py:5034 `_shield_final_signals`) and
restores them only on the bare path (5133), not in a `finally`. The new test
deliberately raises inside `cmd_rotate_self` (via a `_reap_chain` boom), so
line 5133 never ran and the pytest process kept SIGTERM = SIG_IGN for the rest
of the session. A later reap test's `sleep` children then INHERITED SIG_IGN,
ignored the TERM, got SIGKILL'd, and lingered as un-reaped zombies — so
`gone_after`/`reaped` came out False. Full-file runs only passed because the
test was last in the file; the next planned work (g15-11) appends tests after
it and would have hit it.

Fix, kept TIGHT inside the new test's file scope (no production change, no
re-indent of `cmd_rotate_self`): capture the current dispositions of SIGHUP /
SIGTERM / SIGPIPE with `signal.getsignal` BEFORE the interrupted `cmd_rotate_self`
call, and restore them (`signal.signal(sig, old)`) in the test's existing
`finally:` — the same shape as `rotate._restore_shield_signals`, but local to
the test. This makes the restore unconditional even when the reap dies
mid-flight.

## Evidence

1. Targeted pair, natural order (both via `-k`):
   `test_belam_cap_record_planned_entry_when_term_interrupted OR
   test_chain_seat_keeps_own_window_reaps_oldest_fifo` -> 2 passed, 18 deselected.

2. Full file: `python3 -m pytest extensions/agi/tests/test_rotate_handover.py -q`
   -> 20 passed.

3. Targeted pair in REVERSE order, one process (belam spins up first, which is
   the poisoning case; `AGI_TIER` unset to let positional node-ids run):
   -> 2 passed.

4. Reap-adjacent neighbours:
   `python3 -m pytest extensions/agi/tests/test_rotate_selfreap.py test_rotate.py -q`
   -> 127 passed.

(`extensions/agi/tests/test_rotate_rotate.py` does not exist, so per the parent
the handover file alone satisfies acceptance.)

## Notes

- Note the kid-tier gate (goal:g15.6): `AGI_TIER=kid` refuses a bare run and
  also refuses positional `path::node` args because the arg string does not end
  in `.py`. Use a `-k` filter, or unset `AGI_TIER` for an explicit ordered
  positional run (needed here for the reverse-order, one-process proof).
- The production hardening — put `_restore_shield_signals(_shield_old)` in a
  `finally:` in `cmd_rotate_self` so a real-world mid-reap crash restores signal
  state — is deliberately NOT done this round; the parent excluded it and it is
  noted separately.

## Agent Notes
Fixed test poisoning: belam-cap interrupted-reap test now captures and restores SIGHUP/SIGTERM/SIGPIPE dispositions in its finally, so the SIG_IGN leaked by cmd_rotate_self's exception path no longer corrupts later reap tests. Verified: natural order 2 passed, full file 20 passed, reverse order (one process) 2 passed, selfreap+rotate 127 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-3c16a703 (L4.150). WHAT THE INSTRUCTION SAID: the hypothesis file scope is rotate.py `_reap_belam_oldest` + its call site ONLY, plus test_rotate_handover.py. WHAT THE MACHINE DOES: I reproduced the ordering failure myself before the fix (`pytest <new-test> <F1-test>` -> 1 failed, `b["reaped"] is False`, 12.4s), isolated the mechanism to rotate.py:5034 SIG_IGN never restored on the exception path (rotate.py:5133 is a bare statement), confirmed a child inheriting SIG_IGN survives TERM and stays an unreaped zombie (os.kill(pid,0) still True) so gone_after/reaped read False, and confirmed after the fix both orders pass in ~0.5s and the full file is 20/20. NEAR MISS: I first read the fix as "put `_restore_shield_signals` in a `finally` in cmd_rotate_self" — that satisfies the words and loses the mechanism, because it re-indents ~100 lines of the function the hypothesis scoped to the call site only; the test-local restore removes the landmine with zero production churn. DEVIATION: the parent spawned a SECOND kid against a hypothesis whose note said CEILING: 1 kid; the property of this case is that the first kid's own new test poisoned the shared pytest process and the very next planned work (g15-11) appends tests after it, so the landmine had to be cleared in this round or inherited by the next one. Production hardening (finally in cmd_rotate_self) is recorded as an idea, not done here.
<!-- THOUGHT:END -->
