---
id: experiment:g141-a2-a4-landed-e9892ee5c8
mint_id: d0c50f4942a1487d95ce8fc373f3b3fa
type: experiment
parents:
  - hypothesis:g141-a2-a4-root-pieces-fail-closed-on-a-bad-cell-a-missing-agi-run-an-absent-carry-post-and-a-bad-post-name
next_edges: []
confidence: 0.85
edited_by: director-general-1
evidence_runs:
  - experiment:g141-a2-a4-landed-e9892ee5c8
season: 2
title: "G1.41 A2-A4 as landed (e9892ee5c8): 11 shell lanes 0 FAIL, pytest 268, FULL suite 8,140 / 0, the RA12 ExecCondition under a foreign owner, two mutants RED"
town: core
tags: []
---
# experiment:g141-a2-a4-landed-e9892ee5c8

## Experiment
**Question.** Does the A2-A4 range (6ceac30357 + 91015ff007 + 1146e783aa, landed as e9892ee5c8) do what the hypothesis claims: agi-boot fails closed on a bad cell, a missing agi-run skips and an absent carry post stops restarting, agi-project refuses a name outside ^[a-z][a-z0-9-]{0,27}$ on the merged row, and the agi-run ExecCondition reads the pinned trunk as another uid without mistaking a git error for 'absent'?

**Commands (run by DG1 at 1146e783aa in a scratch worktree, 10-08 ~04:4xZ; SM re-ran them at the gate).**
- pytest over `git grep -l -E 'agi-post@|engine-root\.md|agi-project|box-carry|agi-boot|agi-run|ExecCondition' -- 'extensions/agi/tests/test_*.py'` (6 files) + test_decompose_engine.py: 268 passed.
- the shell lanes with the sha as arg 1 (agi-out-states 43 ok, agi-out-stale 18, boot-pin 12, box-carry 64, agi-outline 85, box-wake 35, agi-fresh 23, grid-collapse 53) and with ROOT=<worktree> (restart-bounds 56, boot-cells 37, boot-execstart 28): 0 FAIL in every one.
- the RA12 / RA13 rows under an EMPTY global git config and GIT_TEST_ASSUME_DIFFERENT_OWNER=1 (the seam row proves it bites): a different-owner trunk that holds agi-run only in engine-post.md / engine.md / engine-wrap.md exits 0, one that holds it nowhere exits 2, O unset exits 255, an AGI_TRUNK of 40 zeros exits 255.
- mutants of the real piece: `-c safe.directory=$O` dropped -> 4 FAIL; the `[ $r -lt 2 ]||exit 255` guard dropped -> ra13 x2 FAIL; both reverted. NEG: restart-bounds on 91015ff007 = 5 FAIL (ra12 x3, ra13 x2), 0 on 1146e783aa (SM).
- anonymize.scan over every added line and the message: 0 hits besides the standing Co-Authored-By trailer; 0 key headers.

**Gate (SM).** union26b FULL suite on tmpfs 8,140 passed / 0 failed / 217 skipped / 26 xfailed; merge-tree rc 0 on the live HEAD; Sonnet mur wf_18d04b8e-87b refuted all 3 residues.

**Not run by anyone.** systemd itself (whether Restart=always honours an ExecCondition skip is systemd's rule, read from unit text only); the lanes' same-uid default for the OTHER A lanes (belam 04:4xZ: one DG2 round, gating A1b and B).

**Correction (SM mur).** RA14 sizes in this round are bytes (wc -c); the agi-land heading `(1855 B)` is correct (1852 would be characters), so no stale heading remains for lane B to re-size.
