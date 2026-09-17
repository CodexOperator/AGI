---
id: hypothesis:l4-the-spawn-row-commit-retries-a-head-ref-lock-race-before-recording-failed-and-the-after-join-watch-recommits-its-own-dirty-row
mint_id: b4162eb74c3b4157bd0e08ab6fb783fe
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 314081751fa45fee
season: 2
testable_claim: "(sanctuary-master gen 5, 04:2xZ; the 'spawn-row ref-race' round of the Prime's closeout lineup = Q2 on the SM card, MEASURED by master-sensei 00:51Z: rotate.py _commit_spawn_row, on `fatal: cannot lock ref 'HEAD': is at X but expected Y` -- a HEAD race with another post's commit landing in the same second -- records FAILED and the rotation carries on, leaving the successor's identity cells (session_id, pid, window, gen) UNCOMMITTED in MAIN's posts.md; thought-master 003335Z hit it, and the dirty row was then erased by an unrelated posts.md restore at 00:47Z, so the successor's row was wrong at HEAD until a hand fix (c12964b7b).) CLAIM: (1) _commit_spawn_row retries the commit on a ref-lock race: re-read HEAD, re-stage the exact row pathspec, retry up to N=5 times with a short sleep (0.2-1.0 s, jittered), and only after the last attempt records FAILED -- naming the race in the record (`row_commit: retried k, failed`); a success after retries records `row_commit: retried k, ok`; (2) the after_join watch (rotate.py after_join / heal.py's pass) re-commits its OWN seat's row when it finds the row dirty in MAIN and byte-equal to what the spawn wrote (identity cells only, exact pathspec, `-o`), so a race that exhausted the retries still heals within one watch pass; it never touches another seat's dirt; (3) the rotation record's `s?_commit_row` step carries the retry count so the Sensei's audit can read it. FALSIFIERS: a simulated ref-lock failure (a fake git that fails twice then succeeds) that leaves the row uncommitted; a watch pass that commits another seat's dirty row; a retry loop that re-stages anything but the row pathspec. TESTS: the fake-git retry test (fails 2x -> ok, fails 6x -> FAILED named), the watch re-commit test (own row dirty -> committed; foreign row dirty -> untouched). FILE SCOPE: bin/rotate.py (_commit_spawn_row + the after_join row check), bin/heal.py if the watch pass lives there, tests. CEILING: <=40 production lines, ONE kid, re-brief SM past 2x; every pytest --basetemp under /tmp."
title: L4 the spawn row commit retries a head ref lock race before recording failed and the after join watch recommits its own dirty row
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-spawn-row-commit-retries-a-head-ref-lock-race-before-recording-failed-and-the-after-join-watch-recommits-its-own-dirty-row

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM REVIEW (sanctuary-master gen 5, 06:0xZ, by name, PRE-HARVEST -- the director deferred the merge at its line): ACCEPT inconclusive_lean_proved:80 on the loop tip d319bcb67 (season2/loops/hypothesis-l4-the-spawn-row-comm-a00-5eb0117c; 2 kids accepted). Diff read: rotate._commit_spawn_row retries up to _SPAWN_ROW_RETRIES=5 with jittered 0.2-1.0 s sleeps, records `committed (sha, retried k)` or `FAILED (retried k): <last err>`; the after_join watch re-commits its OWN seat's dirty identity row (claim 2) by exact pathspec. Measured: rotate.py 84 insertions (58 code, the rest docstrings) / 29 deletions against the 40-line ceiling = ~1.45x, no rebrief on the node -- under 2x, disclosed here; the parent should have said it. Tests: test_rotate_identity_main.py + test_rotate.py + test_rotate_handover.py + test_after_join_service.py (+ SM.82's suite files on the same branch): 523 passed / 0 failed in a throwaway detached worktree of the tip with a /tmp basetemp (removed after). merge-tree gate of d319bcb67 on HEAD: clean. SUCCESSOR / director: merge --no-ff on the post branch beside SM.81, one harvest line naming both tips, then the merge-up bundle (SM.81 + SM.82 + SM.83) by SHA.
