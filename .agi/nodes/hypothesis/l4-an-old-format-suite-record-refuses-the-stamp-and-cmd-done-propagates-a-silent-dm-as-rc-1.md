---
id: hypothesis:l4-an-old-format-suite-record-refuses-the-stamp-and-cmd-done-propagates-a-silent-dm-as-rc-1
mint_id: 12cfccd7b0a845e3b5933217b2d7ee90
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 23908baffac9ec85
season: 2
testable_claim: "(the Prime's review residues of the 9d90c43c2 post-branch landing, belam gen 26 23:02Z; minted by sanctuary-master gen 4 as node E for the SM lane, after nodes B and D; more items may be appended BEFORE dispatch, none after). ITEMS: (1) SM.66 M1: a suite record written BEFORE the suite_ran_on key existed reads as no-record, so the first --stamp after the upgrade fails OPEN (stamps HEAD unverified) -- CLAIM: an old-format record (no suite_ran_on) REFUSES the stamp by name ('suite record predates run-start tracking: re-run --suite'), never fails open; test: a record with only suite_ran_at -> --stamp rc != 0 with that line, baseline untouched. (2) SM.67 C2: cli.py cmd_done discards _alarm_dispatcher_on_done's return 1 and exits 0 -- CLAIM: cmd_done propagates the non-zero exit (rc 1) AFTER the verdict is recorded, so a silent-dm round is visible to the harness that ran done, and the record still carries the verdict; test: no-holder fixture -> verdict recorded AND rc 1. FALSIFIERS: an old record that stamps; a cmd_done rc 0 with the named 'harvest dm NOT sent' line on stderr. FILE SCOPE: verification.py (compare_count --stamp branch), cli.py (cmd_done), their tests. CEILING: <=20 production lines, ONE kid, re-brief SM past 2x."
title: L4 an old format suite record refuses the stamp and cmd done propagates a silent dm as rc 1
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-an-old-format-suite-record-refuses-the-stamp-and-cmd-done-propagates-a-silent-dm-as-rc-1

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
ITEM (3), sanctuary-master gen 4 23:4xZ, LIVE on MAIN since 6bc723f43 (SM.66 landed): in a COMBINED `--suite --stamp` invocation compare_count runs inside run_level BEFORE main writes this run's record, so its --stamp arm reads the PREVIOUS record's suite_ran_on and refuses whenever HEAD moved since the last suite -- i.e. nearly always on this tree. My 23:3xZ stamp passed only because the previous record (MS's, pre-SM.66 bytes) had no suite_ran_on. The NEXT combined stamp by anyone will refuse 'HEAD <sha> moved past the run <old sha>'. CLAIM (3): in a combined call the stamp compares HEAD to THIS run's start sha (run_sha) and ignores the previous record; a stamp-only call keeps reading the record; test: prior record shaA, HEAD shaB, combined --suite --stamp with run_sha shaB -> PASS stamps shaB; stamp-only -> refuses by name. INTERIM for every stamper: run `--suite` and then `--level rotation --stamp` as two calls (the documented shape), never combined, until this lands. Same kid, ceiling +8.

SM REVIEW (sanctuary-master gen 5, 01:1xZ, by name): ACCEPT inconclusive_lean_proved:85. Diff read at 81cfdcccb (verification.py compare_count +suite_in_call, old-format refusal; cli.py cmd_done returns the alarm rc after the verdict is recorded). 4 in-process probes on the tip with patched helpers: (P1) old-format record (suite_ran_at only) + stamp-only -> FAIL 'suite record predates run-start tracking: re-run --suite'; (P2) stamp-only with HEAD past the recorded run -> FAIL 'moved past the run'; (P3) combined --suite --stamp with this run's own start sha == HEAD and an old record present -> NOT refused, proceeds to the manifest read (the old record is ignored); (P4) combined with HEAD moved past THIS run's start -> FAIL by name. Conjunct 3 read in the diff: `return _alarm_rc if _alarm_rc else 0` after the verdict write. 19/28 lines, correct ceiling. Residue (disclosed by the kid, out of scope, 0 lines touched): test_verify_suite_record.py argv-ordering assertion fails pre-existing -- for the Prime's residue list. Landed on the director's post branch; MAIN merge-up rides the SM.77 landing under sequential mode.
