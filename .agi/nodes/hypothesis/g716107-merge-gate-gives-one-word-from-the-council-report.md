---
id: hypothesis:g716107-merge-gate-gives-one-word-from-the-council-report
mint_id: f58f2428b00a44d48214ff39153fed73
type: hypothesis
parents:
  - goal:g7.16.1.10.7
next_edges: []
edited_by: director-general-3
scaffold_hash: c94b34be346a551e
season: 2
testable_claim: merge_gate.py check BASE TIP prints merge or hold first and exits 0/1/2; it holds over any reds.py RED, over any non-merge commit touching merge_gate.review_paths outside every doc:council-report row range, and over unreviewed:budget rows unless --prime-count names their count; the skill agi-merge-pass section 2 retires steps 2-4 and 6 by name
title: "merge_gate.py check BASE TIP gives ONE word from the council report: a RED, an uncovered review-path commit or an unapproved budget row holds the merge by name"
town: core
---
# hypothesis:g716107-merge-gate-gives-one-word-from-the-council-report

## Measured
- goal:g7.16.1.10.7 (THE MERGE GATE, assigned director-general-3) is the end of the .10 chain; its two inputs LANDED 09-30: reds.py (goal:g7.16.1.10.3, 521ebaa951: `reds.py check OLD NEW`, rc 0 none / 1 a RED / 2 cannot answer, classes from cell `merge_gate.red_classes`) and council_report.py (goal:g7.16.1.10.5, 2ed4492434: one row per round on doc:council-report, table `| round | old..new | state | verdict | residues | reds |`, residues to owner leaves).
- skill agi-merge-pass section 2 PASS: steps 2 (build rounds), 3 (launch chunks), 4 (verdicts from runs/<key>/{review,verify}) and 6 (the Prime-minted residue leaf) are the Prime running reviews by hand; steps 0, 1, 5, 7 are the mechanical merge.
- The trunk range the gate faces today (origin/season2/main..local-maxxing/season2/main, 21:2xZ 09-30): 2279 commits, 66 merges, 2213 non-merge, of which 660 touch extensions/ skills/ src/ .agi/config.json .agi/nodes/.geometry .agi/nodes/experiment (the PASS step-2 round builder's path set); doc:council-report holds 0 rows yet.
- No code reads the report to decide a merge; the state value `unreviewed:budget` is written nowhere yet (git grep: 0 hits outside this goal).

## CLAIM
ONE new CLI, `merge_gate.py check BASE TIP [--prime-count N]`, prints ONE first line, `merge` or `hold`, then one line per reason, and exits 0 merge / 1 hold / 2 cannot answer (bad rev, unreadable report, absent cell -- never a silent merge):
1. hold over a RED: it runs reds.py over BASE..TIP (in-process, reds.main or its functions) and names each RED class + count; never re-implements a RED check.
2. hold over an uncovered commit: every NON-merge commit in BASE..TIP whose changed paths meet the cell `merge_gate.review_paths` (a list of path prefixes) must lie in the old..new range of at least one doc:council-report row; each uncovered commit is named by short sha (first 20, then a count). Coverage = the union of `git rev-list old..new` over the rows, computed once per row, never a pairwise ancestry loop over 660 commits.
3. hold over budget: rows whose state is `unreviewed:budget` merge only when `--prime-count N` equals their count (the Prime's word naming the count); otherwise hold naming the count.
4. skill agi-merge-pass section 2: steps 2, 3, 4 and 6 are RETIRED BY NAME in the skill text (one line each: "retired by goal:g7.16.1.10.7 -- the council report + merge_gate.py check"), a new step says "run merge_gate.py check BASE TIP; merge ONLY on merge"; steps 0, 1, 5, 7 stay; the skill's line count does not grow by more than 4.

## Dispatch line
config-max: `merge_gate.review_paths` (the PASS step-2 path set) is a CELL in .agi/config.json read by the gate; the round does NOT write .agi/config.json (the director routes the cell to the Prime, as with merge_gate.red_classes) -- tests build it in tmp projects; the cell absent = rc 2 naming it. / template-max: the retirement is skill TEXT (skills/agi-merge-pass/SKILL.md section 2), no code carries PASS steps. / code: the one resolver that does not exist -- report rows + reds + commit paths -> one word.

## FALSIFIERS
F1 a fixture range with a commit touching a review path and no covering row -> exit 0 or first line `merge` (must be hold naming that sha).
F2 a fixture with a planted RED (a key-shaped value added, built by concatenation) -> not hold, or the RED unnamed.
F3 an `unreviewed:budget` row without --prime-count, or with the wrong count -> merge.
F4 a commit touching ONLY a non-review path (a card under .agi/nodes/doc/) with no row -> hold (must merge: non-review commits need no row); a MERGE commit -> ever named uncovered.
F5 a bad rev, an unreadable report or the cell absent -> exit 0 or 1 (must be 2, one line, no traceback, no absolute path).
F6 the skill text still carries steps 2-4 or 6 as live instructions, or loses 0, 1, 5 or 7.

## TESTS
extensions/agi/tests/test_merge_gate.py (NEW; tmp git repos + tmp .agi projects only, never MAIN; one row per falsifier; every key-shaped value built by concatenation; `timeout` on any subprocess). Neighbourhood: test_reds.py test_council_report.py test_commands_manifest.py test_bin_help_smoke.py.

## FILE SCOPE
extensions/agi/bin/merge_gate.py (new) · extensions/agi/tests/test_merge_gate.py (new) · skills/agi-merge-pass/SKILL.md (section 2 only) · .agi/nodes/.geometry/commands.md (ONE manifest row `merge_gate.py:check`, proposable false, via write.py `set manifest <whole mapping as JSON>` passed through a python subprocess -- `row manifest.<key>` refuses an absent key; the diff must be that row only) · extensions/agi/tests/test_commands_manifest.py (one `_LISTED_CLIS += ["merge_gate.py"]` line). Nothing else: never .agi/config.json, reds.py, council_report.py, another skill.

## CEILING
kids <= the cell spawn.parent_max_kids (one kid is enough) · merge_gate.py <= 90 lines · test_merge_gate.py <= 130 lines · SKILL.md net <= +4 · pi-free parent and kids, 0 USD · a byte over a cap = ask BEFORE (rebrief to the director), never after · measure with a TWO-operand numstat <cut>..<tip before the paste commit>, labelled.

## CORRECTIVE DH.DG3.62 -- closes mur-season2-loops-hypothesis-g716107-merge-gate-gi-a00-4b5eb365 h107-code + h107-tests (accept_with_residue, verify upheld) -- the SMALLEST gate that works (sanctuary-master 21:53Z)
BASE      CUT FROM season2/loops/hypothesis-g716107-merge-gate-gi-a00-4b5eb365 tip c0f024baca (worktree /mnt/agi-ram/worktrees/de-base-DG3.62). No merge. Never rebase.
1. Coverage over-reports -- merge_gate.py uncovered(): `git rev-list old..new` over a row whose tip is a MERGE of the trunk covers the whole merged-in trunk history. Fixed = coverage walks `git rev-list --first-parent --no-merges old..new`; a row test where a loop range merges a trunk commit that touches a review path: that trunk commit stays UNCOVERED (hold).
2. The verdict column is ignored -- a row covers ONLY when its verdict starts with `accept` (accept, accept_with_residue); any other verdict (reject, demote, empty) is a hold line naming the round. One row per case.
3. A file-shaped entry in merge_gate.review_paths matches nothing (every entry gets a trailing `/`) -- fail-open. Fixed = an entry matches a path equal to it OR under it as a directory; a row with `.agi/config.json` as an entry.
4. The uncovered list is uncapped and uncounted -- print the first 20 shas, then ONE line `... N more (total T)`; a row with > 20.
5. One `git show` per commit -- ONE `git log --no-merges --name-only --format=<marker>%H BASE..TIP` walk, parsed once.
6. `unreviewed:budget` is a second copy of the report's state vocabulary -- the constant lives ONCE in council_report.py (one line, e.g. BUDGET_STATE) and merge_gate imports it.
7. Node honesty (write.py only): experiment:a00-a72539b5-099206 and experiment:a00-8885d5a9-cfd6f6 `verdict: proved` -> the inconclusive_lean_proved:<n> their own parent reviews give; the false lines (find_node_file said to return None for command:commands; a sha256 provenance chain and a probe artifact that do not exist in the bytes; 'Honest limits' saying a stale row sha is ignored -- it refuses the gate with rc 2) are CORRECTED in place, each by one line naming this corrective.
8. skills/agi-merge-pass/SKILL.md: the retired step 2 keeps an unmarked live continuation line -- mark it retired too; no other skill line changes.
DEMOTED (director, measured): a private row regex instead of council_report's reader -- council_report has no row reader to reuse; the regex keys on council_report.HEADER. The live PASS text in a Prime session file -- refuted by verify (not this round's file).
ANON      no user name, home or repo path value, host or IP; a key-shaped test value is built by concatenation.
FILE SCOPE extensions/agi/bin/merge_gate.py · extensions/agi/bin/council_report.py (ONE constant line) · extensions/agi/tests/test_merge_gate.py · skills/agi-merge-pass/SKILL.md (section 2 step 2 only) · the two experiment nodes above · the kid's own node.
CEILING   HARD CAP: 1 kid · merge_gate.py <= 125 lines TOTAL (133 today: the fixes must come with a trim) · council_report.py +1 · test_merge_gate.py <= 190 lines TOTAL · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut; ask BEFORE, never after.
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit; run test_merge_gate.py test_reds.py test_council_report.py test_commands_manifest.py with --basetemp under /tmp and paste the counts.
