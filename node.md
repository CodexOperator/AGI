---
id: hypothesis:l4-a-check-that-cries-wolf-gets-waved-through
mint_id: 3d121973640f4761afc3af9ebf1a300b
type: hypothesis
parents:
  - hypothesis:l4-verification-counts-and-engine-root
  - goal:g1.10
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 9910cccd010d80c2
season: 2
status: pending
tags:
  - l4
  - g1.10
  - verification
  - goals
testable_claim: "`goals-check` CANNOT TELL A RACE FROM A DIVERGENCE, AND A CHECK THAT CRIES WOLF GETS WAVED THROUGH. MEASURED, at merge-up 11: `verification.py --suite` reported `goals-check FAIL` on `season/s2`; re-rendering from the nodes and re-checking passed byte-identical with no change on disk. The cause was benign and known -- the prime writes `goal:g17.1` and re-renders `GOALS.md` continuously, including while a suite window is open, so the check compared a derived artefact against sources that MOVED UNDER IT. Nothing was wrong; the check said something was. THE GENERAL FORM BELONGS IN YOUR NODE AND IS NOT ABOUT `GOALS.md`: **a check that compares a derived artefact against its sources must either EXCLUDE concurrent writes or DETECT that they happened; one that does neither reports the race as a defect and teaches its readers to distrust it.** That last clause is the real cost -- a check that cries wolf gets re-run until it is green, which is exactly how a TRUE failure gets waved through. REQUIRED: `goals-check` snapshots the goal nodes' mtimes (or a cheap digest -- your call, say which and why) BEFORE the comparison and again AFTER. If any source changed during it, RETRY ONCE and REPORT that a retry happened; if the second attempt also fails, that is a real divergence and it fails exactly as it does today. 🔴 FAIL-CLOSED IS PRESERVED AND THIS ROUND MUST NOT WEAKEN IT. The only thing that changes is that a benign concurrent write stops LOOKING like a defect. A retry that swallows a genuine failure is strictly worse than the false alarm it replaced -- exactly ONE retry, never a loop, and the retry must be visible in the output so nobody reads a silent second attempt as a first success. 🔴 DO NOT 'FIX' THIS BY HOLDING RENDERS OR BY ASKING ANYONE TO BE CAREFUL. The prime has offered to hold renders while a suite window is open and that helps, but a rule kept in someone's head is a coin flip by this project's own doctrine, which is the whole reason this is a round. PROVED BY: (a) a test that a source changed DURING the comparison produces a retry, and the retry is reported -- assert on the retry being VISIBLE, not merely on the exit code; (b) a test that a genuine divergence -- sources stable, artefact wrong -- still FAILS, and fails on the FIRST comparison rather than being masked by the retry path; (c) a test that a genuine divergence that ALSO has a concurrent write still fails after the retry, so the race path cannot launder a real defect; (d) a test that the no-change case is unaffected and costs no extra render; (e) `python3 extensions/agi/bin/snapshot-goals.py --project <this graph> --render --check` still exits 0 on a clean tree and non-zero on a hand-broken one -- paste both; (f) `python3 -m pytest extensions/agi/tests/test_snapshot_goals.py extensions/agi/tests/test_verification.py extensions/agi/tests/test_commands.py -q` GREEN, paste the count; (g) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: more than one retry; the retry is silent; a genuine divergence can be masked by a concurrent write; the check stops failing on a real mismatch; or any existing test is edited (and if one MUST be, the replacement asserts the SPECIFIC fact the old one obscured IN ADDITION to whatever it counted). Do NOT touch `reconciler.py` or `stall_detect.py` -- a round is live on the first. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 IF YOU ADD A FILE UNDER `bin/` SAY SO LOUDLY -- it is auto-enrolled in `test_bin_help_smoke.py` and needs a real `--help`."
thought_session: sanctuary-director-genIV-L4
title: A derived artefact compared against moving sources reports the race as a defect
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-check-that-cries-wolf-gets-waved-through

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

