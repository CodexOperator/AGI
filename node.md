---
id: experiment:a00-a023d95f-de315a
mint_id: e4510b3ae2dd430fbb6dc0008ac42e11
type: experiment
parents:
  - hypothesis:l4-a-no-window-started-record-waits-the-promised-delay-the-own-tail-re-claims-a-stale-claim-and-the-dead-seat-marker-is-pathspec-committed
next_edges: []
confidence: 0.85
edited_by: a00-a9a3a324
evidence_runs:
  - experiment:a00-a023d95f-de315a
loop: hypothesis:l4-a-no-window-started-record-waits-the-promised-delay-the-own-tail-re-claims-a-stale-claim-and-the-dead-seat-marker-is-pathspec-committed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 870b9e4454d8125d
season: 2
title: A00 a023d95f de315a
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-a023d95f-de315a

## Experiment

g15.25 FIX-ONLY build (mur-SL2.25 residues (a)+(f)). Measured the pre-fix
state by symbol on the season-2 main tip (63c67f057), implemented the claim
in rotate.py, and proved it on the built bytes with 5 new tests.

**Pre-fix measurements (confirmed each is a real falsifier by reverting the
fix and watching the test fail):**

1. JOIN GATE clause (3a) — `run_after_join_for_seat`: the wait/refuse gate
   was `if window_id and not joined.get("found")`, so a STARTED record with
   NO window @id (`joined == {}`) skipped the gate entirely and was performed
   at delay 0 (as if fresh) — probe: a past-age no-window record reached
   `run_after_join` with NO `join unresolved` refusals (had only
   `unknown startup placeholder {pid}`), never the promised max-wait bound.
   FIX: ONE code path — `if not joined.get("found")` — so both a windowed
   rejoin-failed record and a no-window record wait `after_join_max_wait_s`
   then perform once with the join-dependent entries refused by name.

2. CLAIM (2) — the OWN tail at step (6.4) used `_after_join_already_performed`,
   which treated ANY `after_join` key (including a dead claim) as performed, so
   the tail DEFERRED on a stale claim instead of re-claiming. FIX: the guard is
   now STALE-AWARE — with `stale_s` it returns False for a stale claim (no
   results, older than `after_join_claim_stale_s`) via the SAME `_claim_is_stale`
   helper the watch path uses, so the tail falls through and re-claims with its
   OWN performer identity. A live claim still defers; a completed run still guards.
   `cmd_rotate_self` now passes the template's stale bound.

3. CLAIM (3) / residue (f) — the late dead-seat `after_join {skipped, age_s}`
   marker wrote the record with a bare `rp.write_text` (no pathspec commit),
   so MAIN read `M` on a committed record and the next restart re-saw the
   record. FIX: the marker now goes through `_commit_after_join_record` with
   `commit_label="dead-seat"`; gitless fixtures SKIP harmlessly.

**5 tests appended to test_after_join_service.py** (<= 5 ceiling):
  (a) test_no_window_record_waits_delay_not_performed
  (b) test_no_window_record_past_wait_performs_with_named_refusals
  (c) test_tail_reclaims_stale_claim_with_own_identity
  (d) test_dead_seat_marker_committed_by_pathspec
  (e) test_watch_performed_then_tail_guard_skips_second

## Evidence

`python3 -m pytest extensions/agi/tests/test_after_join_service.py ...` -> 72 passed.
after_join + tail + selfreap + startup + next neighbors: 228 passed.
rotate neighborhood (18 files incl. test_rotate.py, tmpls, closeout, tail,
recover, latch_sweep, launch_wrapper, ...): 545 passed, 1 xfailed.
No existing after_join assertion changed — extend only (test (c) borrows the
claim-stale fixture shape; test (b) mirrors the windowed join-gate test with
window_id="").

Falsifier proof (pre-fix state, each reverted then re-passed):
  fix1 reverted -> (b) FAILS (no `join unresolved` refusal on the no-window
        pid-dep entry)
  fix2 reverted -> (c) FAILS (`_after_join_already_performed(..., stale_s=300)`
        returned True for a stale claim)
  fix3 reverted -> (d) FAILS (no `dead-seat` commit in git log on the fixture
        repo)

THOUGHT: this is a FIX-ONLY build order, not a measurement — reproduced each
defect on the pre-fix bytes, then proved the built bytes. The claim's "(e)
watch + tail -> one perform" is a regression-guard (the results-block guard is
unchanged and passes both pre- and post-fix); the load-bearing fixes are (1),(2),(3)
and their tests (b),(c),(d). Caveat: test (c) drives the tail re-claim through
run_after_join/_claim_after_join (the seam cmd_rotate_self calls) rather than a
full cmd_rotate_self integration, to stay hermetic.

## Agent Notes
g15.25 FIX-ONLY (a)+(f): implemented in rotate.py - one join gate for both record shapes (no-window waits delay+max_wait, past bound refuses join-dependent by name); tail step-6.4 guard stale-aware via same _claim_is_stale (re-claims own identity); dead-seat marker committed by pathspec label dead-seat. 5 tests appended, all 3 fixes proven genuine falsifiers by revert; 773 rotate/after_join tests green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.104. All three fixes are in the built bytes and I re-ran them myself: test_after_join_service.py 72/72, and 753 passed + 1 xfailed across the 23 test_rotate* + after_join files (no regression). Clauses (1) and (3) carry GENUINE falsifiers: test (b) fails on the pre-fix guard `if window_id and not joined.get("found")` (a no-window pid-dep entry got no `join unresolved after Ns` refusal), test (d) fails without the `dead-seat` pathspec commit in the fixture git log. Clause (2) is correct by construction -- `_after_join_already_performed` is now stale-aware through the SAME `_claim_is_stale` helper the watch uses, and cmd_rotate_self:15552-15560 reads `startup` (defined rotate.py:14743) and passes the template stale bound -- but its PRODUCTION wiring is UNTESTED: test (c) drives the helper and run_after_join directly, never cmd_rotate_self step (6.4), so no test asserts the tail actually falls through instead of skipping. Test (a) is a regression guard, not a falsifier: the age gate returned None before the join gate pre-fix too, so it passes either way. DEMOTED proved -> inconclusive_lean_proved:85 for the untested tail integration; the other three clauses are proven, and clause (2) is verified by file:line reading rather than by a run.
<!-- THOUGHT:END -->
