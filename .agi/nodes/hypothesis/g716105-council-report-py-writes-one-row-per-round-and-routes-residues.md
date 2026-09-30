---
id: hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-residues
mint_id: 0e55d1c361bf4ab2bdbea0fcfe162739
type: hypothesis
parents:
  - goal:g7.16.1.10.5
next_edges: []
confidence: 0.65
edited_by: director-general-3
origin: goal
scaffold_hash: f65b864257cb6329
season: 2
testable_claim: council_report.py add --run KEY --args FILE writes one row per round (idempotent per run key) and lands every unrefuted verify residue and every missed[] item on the owner's leaf from cell council.residue_leaves; owner = assigned post, else commit-subject post, else director-engine; belam never; cell absent = rc 2
title: council_report.py writes ONE row per round onto doc:council-report and routes each verify residue to its owner post's leaf, never the Prime's
town: core
---
# hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-residues

## Measured
- `.agi/sessions/workflows/runs/<run key>/` holds `review_<label>.json` {verdict_recommendation, conjuncts[], defects[] {title, file, line, detail, severity: residue | note}} and `verify_<label>.json` {final_recommendation, verdicts[] {defect, refuted, reason}, missed[]}; a verify that timed out leaves NO verify file (mur dg6-04e, 14:52Z 09-30: review only).
- skill agi-merge-pass section 4: "verify verdicts[] rules on the FIRST reviewer's defects + missed[] -- a residue table reads verify, never the review list alone" -- the rule is prose; no code applies it.
- `git grep -n "residue_leaf\|council_report\|report_node" -- extensions .agi/config.json` = 0 hits: no report node, no router, no owner-leaf cell.
- owners are named today as `(assigned: <post>)` in 24 goal titles; commit subjects end `(<post>)` (write.py commits); PASS residues went to Prime-minted leaves goal:g1.28 / g1.30 / g1.31 (the parent goal's measure).
- siblings NOT landed: goal:g7.16.1.10.1 (round identity), .10.2 (REUSED), .10.4 (unreviewed:budget) -- this round writes REVIEWED rows only; the state column is the seam they fill.

## CLAIM
(1) `council_report.py add --run <run key> --args <the mur args file> [--root]` writes ONE row per round of that run onto ONE report node `doc:council-report` (minted by this round under goal:g7.16.1.10.5, via write.py, committed by exact path): round key, old..new (short), state REVIEWED (verify present) or REVIEWED:review-only (verify absent), verdict (verify final_recommendation, else review verdict_recommendation), residue count, reds `unchecked` (goal:g7.16.1.10.7 fills it). A second `add` of the same run key replaces its rows, never duplicates them. (2) Residues = verify verdicts[] with refuted false + every missed[] item; ONLY when no verify file exists, the review defects with severity residue (each marked review-only). (3) Each residue routes to ONE owner: the hypothesis's parent goal title `(assigned: <post>)`, else the post named at the end of new_tip's commit subject, else director-engine; an owner that resolves to the Prime (belam) routes to director-engine instead. (4) The owner's leaf comes from ONE cell `council.residue_leaves` ({post: goal id, "default": goal id}); a post absent = the default; the residue lands as ONE row on that leaf via write.py, naming round + residue title, never on a Prime-minted PASS leaf.

## Dispatch line
config-max: the cell `council.residue_leaves` (the ROUND RETURNS the cell diff in its experiment node -- default goal:g7.33.19; `.agi/config.json` is never committed by the round) / template-max: none THIS round (the merge-pass skill retirement is goal:g7.16.1.10.7's) / code: council_report.py, the router that does not exist; node writes through write.py only, never a hand-written file.

## FALSIFIERS
- F1: a fixture run dir (tmp project, tmp git repo) with 2 rounds -> the report node carries exactly 2 rows; a second add of the same run key still 2 rows = else false.
- F2: a residue present ONLY in verify missed[] (absent from the review defects) does not land on its owner's leaf = false (the section 4 trap).
- F3: a verify verdict with refuted true lands anywhere = false.
- F4: an owner that resolves to belam lands on belam's leaf or on a Prime-minted leaf instead of the default = false.
- F5: no verify file -> the row is not REVIEWED:review-only, or a review NOTE lands as a residue = false.
- F6: the cell absent -> refuses with rc 2 and one line naming the cell, never a silent default = else false.

## TESTS
- NEW `extensions/agi/tests/test_council_report.py`: one row per falsifier, every value synthetic, tmp projects + tmp git repos, `--basetemp /tmp/...`, never the live graph.
- neighbourhood: `test_write.py test_commands_manifest.py test_bin_help_smoke.py`
```
python3 -m pytest extensions/agi/tests/test_council_report.py extensions/agi/tests/test_write.py extensions/agi/tests/test_commands_manifest.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/h10105
```

## FILE SCOPE
extensions/agi/bin/council_report.py (new) · extensions/agi/tests/test_council_report.py (new) · the new node doc:council-report (via write.py create, parent goal:g7.16.1.10.5, body = the row table header only) · the kid's own experiment node. `.agi/config.json` NEVER (the diff is returned). Out: workflow.py, dispatch.py, reds.py, skills/.

## CEILING
kids <= 1 · council_report.py <= 120 production lines · tests <= 160 lines · pi-free parent · 0 USD · measured with a TWO-operand numstat <cut>..<tip before the paste commit>. A kid over it = the round is cut; ask BEFORE, never after. SAFETY: tmp projects only in tests; never write a live goal leaf from a test. ANON: no user name, home or repo path value, host, IP, email or hardware name in any output, node, test, commit or dm.

## CORRECTIVE DH.DG3.58 -- closes the DG3.53 parent review (a00-af9ca035: kid a00-c296586c demoted to inconclusive_lean_disproved:70 on a named probe) + the CEILING breach
BASE      CUT FROM season2/loops/hypothesis-g716105-council-repor-a00-af9ca035 tip 1077e45cb1 (worktree under the RAM-disk cell). No merge. Never rebase.
1. EVERY residue lands -- council_report.py merge_table keys a residue row by its FIRST cell (the round), so a round with three residues leaves ONE row on the owner leaf -- a residue row's key is (round, residue title); re-run the parent's probe (one round, three residues: an unrefuted verdicts[] defect + two missed[] items) and paste three rows on the owner leaf; a second add of the same run still three, never six.
2. the file to size -- council_report.py is 218 lines against the 120 CEILING (no rebrief reached the director before the kid ran past it) -- fold duplication (one table merger for both headers, one owner resolver) so the file ends <= 150 lines with every falsifier row still green; paste wc -l.
3. evidence at YOUR final tip, pasted, + a labelled numstat 1077e45cb1..<tip before the paste commit>: python3 -m pytest extensions/agi/tests/test_council_report.py extensions/agi/tests/test_write.py extensions/agi/tests/test_commands_manifest.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/dh358
SAFETY    tmp projects only in tests; never write a live goal leaf or the live doc:council-report from a test
ANON      no user name, home or repo path value, host, IP, email or hardware name in any output, node, test, commit or dm
FILE SCOPE extensions/agi/bin/council_report.py · extensions/agi/tests/test_council_report.py · the kid's own experiment node. The hypothesis node NEVER; doc:council-report NEVER (landed by the director); .agi/config.json NEVER.
CEILING   HARD CAP: 1 kid · council_report.py ends <= 150 lines · test file NET <= +20 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut; a rebrief goes to the director BEFORE the kid passes a cap
PARENT    paste FILE SCOPE, SAFETY, ANON and CEILING verbatim into every kid brief; COMMIT every kid edit AND merge the kid branch into the loop branch before you exit

## CORRECTIVE DH.DG3.59 -- closes mur-season2-loops-hypothesis-g716105-council-repor-a00-f43e8762 h10105-code + h10105-tests (both reviews accept_with_residue; both verifies timed out, reviews stand)
BASE      CUT FROM season2/loops/hypothesis-g716105-council-repor-a00-f43e8762 tip 62de7b8491 (worktree under the RAM-disk cell). No merge. Never rebase.
1. no partial write -- council_report.py add writes the report row before it validates the council.residue_leaves cell, so an incomplete cell leaves a row and dies rc 2 -- validate the WHOLE cell (every owner reachable to a non-empty leaf id, else the default) BEFORE any write; rc 2 with nothing written; a row.
2. an empty leaf id is refused by name -- a cell with neither the post nor a default -- rc 2 naming the post; a row.
3. counts reconcile -- the report's residue count is computed from the run files and never compared with the leaf rows actually landed -- after landing, a mismatch is rc 2 naming the round; a row.
4. declared, not exempted -- the new verb exempts itself from the command-manifest survey -- declare council_report.py add in command:commands (write.py; anchor on a non-indented line, --dry-run first) and drop the exemption; test_commands_manifest green.
5. the real writer -- the node claims a committed test drives the REAL write.py writer on a tmp node; none does -- add ONE row that does (tmp project, tmp git repo), and correct the node claim with write.py.
6. evidence at YOUR final tip, pasted, + a labelled numstat 62de7b8491..<tip before the paste commit>: python3 -m pytest extensions/agi/tests/test_council_report.py extensions/agi/tests/test_commands_manifest.py extensions/agi/tests/test_write.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/dh359
SAFETY    tmp projects only in tests; never write a live goal leaf or the live doc:council-report from a test
ANON      no user name, home or repo path value, host, IP, email or hardware name in any output, node, test, commit or dm
FILE SCOPE extensions/agi/bin/council_report.py · extensions/agi/tests/test_council_report.py · extensions/agi/tests/test_commands_manifest.py (drop the exemption only) · command:commands (the one new row, write.py) · the chain's experiment nodes (write.py only) · the kid's own experiment node. .agi/config.json NEVER (the cell is routed to the Prime).
CEILING   HARD CAP: 1 kid · council_report.py NET <= +15 · tests NET <= +35 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut; a rebrief goes to the director BEFORE the kid passes a cap
PARENT    paste FILE SCOPE, SAFETY, ANON and CEILING verbatim into every kid brief; COMMIT every kid edit AND merge the kid branch into the loop branch before you exit (if write.py refuses a parent commit, leave the bytes write-logged and say so)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.DG3.59: mur h10105 (both verifies timed out, reviews accept_with_residue): partial write on an incomplete cell, empty leaf id, count never reconciled, manifest exemption, no real-writer row + a false node claim; the cell council.residue_leaves itself is config-max, routed to the Prime via SM
<!-- THOUGHT:END -->
