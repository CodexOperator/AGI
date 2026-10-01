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
testable_claim: "merge_gate.py check BASE TIP prints merge or hold first and exits 0/1/2; it holds over any reds.py RED, over any non-merge commit touching merge_gate.review_paths outside every doc:council-report row range, and over unreviewed:budget rows unless --prime-count names their count [the trailing conjunct -- the skill agi-merge-pass section 2 retirement -- is MOVED to goal:g7.16.1.10.7.1 by corrective DH.DG3.67, option A: the scored claim at NEW is the gate CODE only]"
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
2. hold over an uncovered commit: every NON-merge commit in BASE..TIP whose changed paths meet the cell `merge_gate.review_paths` (a list of path prefixes) must lie in the old..new range of at least one ACCEPTING doc:council-report row -- its verdict starts with `accept` (merge_gate.py `verdict.startswith("accept")`, corrective DH.DG3.62 item 2; any other verdict is a hold line naming the round; restated by DH.DG3.68); each uncovered commit is named by short sha (first 20, then a count). Coverage = the union of `git rev-list --first-parent --no-merges old..new` over the ACCEPTING rows (DH.DG3.62 item 1), computed once per row, never a pairwise ancestry loop over 660 commits.
3. hold over budget: rows whose state is `unreviewed:budget` merge only when `--prime-count N` equals their count (the Prime's word naming the count); otherwise hold naming the count.
4. [MOVED to goal:g7.16.1.10.7.1 by corrective DH.DG3.67 -- option A: the gate CODE landed alone and the skill is restored to its merge-base, so this conjunct is NOT part of the scored claim at NEW; the retirement is its own leaf] skill agi-merge-pass section 2: steps 2, 3, 4 and 6 are RETIRED BY NAME in the skill text (one line each: "retired by goal:g7.16.1.10.7 -- the council report + merge_gate.py check"), a new step says "run merge_gate.py check BASE TIP; merge ONLY on merge"; steps 0, 1, 5, 7 stay; the skill's line count does not grow by more than 4.

## Dispatch line
config-max: `merge_gate.review_paths` (the PASS step-2 path set) is a CELL in .agi/config.json read by the gate; the round does NOT write .agi/config.json (the director routes the cell to the Prime, as with merge_gate.red_classes) -- tests build it in tmp projects; the cell absent = rc 2 naming it. / template-max: the retirement is skill TEXT (skills/agi-merge-pass/SKILL.md section 2), no code carries PASS steps. / code: the one resolver that does not exist -- report rows + reds + commit paths -> one word.

## FALSIFIERS
F1 a fixture range with a commit touching a review path and no covering row -> exit 0 or first line `merge` (must be hold naming that sha).
F2 a fixture with a planted RED (a key-shaped value added, built by concatenation) -> not hold, or the RED unnamed.
F3 an `unreviewed:budget` row without --prime-count, or with the wrong count -> merge.
F4 a commit touching ONLY a non-review path (a card under .agi/nodes/doc/) with no row -> hold (must merge: non-review commits need no row); a MERGE commit -> ever named uncovered.
F5 a bad rev, an unreadable report or the cell absent -> exit 0 or 1 (must be 2, one line, no traceback, no absolute path).
F6 [MOVED to goal:g7.16.1.10.7.1 by corrective DH.DG3.67 -- the F6 row was DROPPED by DH.DG3.65 when the skill was restored to its merge-base; it is no longer falsifiable at NEW] the skill text still carries steps 2-4 or 6 as live instructions, or loses 0, 1, 5 or 7.

## TESTS
extensions/agi/tests/test_merge_gate.py (NEW; tmp git repos + tmp .agi projects only, never MAIN; one row per falsifier; every key-shaped value built by concatenation; `timeout` on any subprocess). Neighbourhood: test_reds.py test_council_report.py test_commands_manifest.py test_bin_help_smoke.py.

## FILE SCOPE
extensions/agi/bin/merge_gate.py (new) · extensions/agi/tests/test_merge_gate.py (new) · skills/agi-merge-pass/SKILL.md (section 2 only) · .agi/nodes/.geometry/commands.md (ONE manifest row `merge_gate.py:check`, proposable false, via write.py `set manifest <whole mapping as JSON>` passed through a python subprocess -- `row manifest.<key>` refuses an absent key; the diff must be that row only) · extensions/agi/tests/test_commands_manifest.py (one `_LISTED_CLIS += ["merge_gate.py"]` line). Nothing else: never .agi/config.json, reds.py, council_report.py, another skill.

## CEILING
(superseded by the CORRECTIVE caps below — the 90/130-line figures died with the first implementation; DH.DG3.62 then set 125/190 and DH.DG3.64 sets 125/195)
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

## CORRECTIVE DH.DG3.64 -- closes mur-season2-loops-hypothesis-g716107-merge-gate-gi-a00-61b3ea24 h107b-code + h107b-tests (accept_with_residue, verify upheld)
BASE      CUT FROM season2/loops/hypothesis-g716107-merge-gate-gi-a00-61b3ea24 tip 7fc4351a45 (worktree /mnt/agi-ram/worktrees/de-base-DG3.64). No merge. Never rebase.
1. merge_gate.py -- the path walk runs with git's default core.quotePath, so a review-path file whose name has non-ASCII bytes arrives C-quoted and matches no prefix (fail-open). Fixed = the walk passes `-c core.quotePath=false` (or -z); one row with a non-ASCII file under a review path -> hold.
2. merge_gate.py -- a second literal of the budget state survives in the argparse help text: the help names it through the imported constant, never a typed copy.
3. test_merge_gate.py -- C5's `show not in seen` breaks on any fixture where reds.py itself issues git show (a deleted node file): assert on the gate's OWN walk, not on every git call; the file ends with a newline.
4. Node honesty (write.py only; every SITE, not one): experiment:a00-a72539b5-099206 and experiment:a00-8885d5a9-cfd6f6 still repeat the refuted sha256 / write-log / probe-artifact chain at every other site (a00-a72539b5 ~:153-175 incl. the false 'iter-DG3.60 is absent' clause and the 'exactly TWO write-log entries' line; a00-8885d5a9 :117 and :123) -- each site corrected in place naming DH.DG3.64; experiment:a00-5b52f00d-9ab743 probe P7 ('NO unreviewed:budget literal') and its fix-7 row ('three false lines corrected') re-stated to what the bytes show; its after-count for test_merge_gate.py = the real wc -l.
5. The hypothesis node carries two live CEILING blocks: the original CEILING line gains '(superseded by the CORRECTIVE caps below)'.
DEMOTED (director, measured): 'write-log not tracked' -- the harvest check ran against the round worktree's .agi/sessions/write-log.jsonl (untracked by design; both entries matched sha256). The every-row verdict hold (rows outside BASE..TIP) -- the report is the council's ledger, a non-accepting row anywhere is a hold worth naming; noted, not changed. The '@@' sentinel collision -- a path line never starts with the sentinel the walk emits; noted.
ANON      no user name, home or repo path value, host or IP.
FILE SCOPE extensions/agi/bin/merge_gate.py · extensions/agi/tests/test_merge_gate.py · the three experiment nodes above · this hypothesis node (item 5 only) · the kid's own node.
CEILING   HARD CAP: 1 kid · merge_gate.py <= 125 lines TOTAL · test_merge_gate.py <= 195 lines TOTAL · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut; ask BEFORE, never after.
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit; run test_merge_gate.py test_reds.py test_council_report.py test_commands_manifest.py with --basetemp under /tmp and paste the counts.

## CORRECTIVE DH.DG3.65 -- closes mur-season2-loops-hypothesis-g716107-merge-gate-gi-a00-9147a830 h107c-code + h107c-nodes (accept_with_residue, verify upheld) + the pending council [decision] 23:04Z, option A applied as the safe default
BASE      CUT FROM season2/loops/hypothesis-g716107-merge-gate-gi-a00-9147a830 tip c03601a725 (worktree /mnt/agi-ram/worktrees/de-base-DG3.65). No merge. Never rebase.
1. Option A (the gate CODE lands alone; the skill retirement becomes its own leaf later): skills/agi-merge-pass/SKILL.md restored byte-identical to the trunk merge-base 8523e5e563 (paste `git diff 8523e5e563 -- skills/agi-merge-pass/SKILL.md | wc -l` = 0), and test_merge_gate.py drops test_f6 (the one row that reads that skill). merge_gate.py, its manifest row and every other test row stay.
2. test_merge_gate.py C6 -- asserts only rc + the first word: it also asserts the hold names the non-ASCII commit's sha (as F1 does), so a hold for any other reason fails it.
3. test_merge_gate.py C5 -- the _git spy cannot see a direct subprocess call added to merge_gate.py later: one assertion that merge_gate.py holds exactly ONE subprocess call, inside _git (read the module source), beside the existing spy.
4. test_merge_gate.py:3 docstring -- names its real row inventory (F1-F5, C1-C6 after item 1), never a stale list.
5. Node honesty (write.py only): experiment:a00-a72539b5-099206 last line (:197) still says the sha256 chain + probe_geom artifact 'are absent from the bytes', contradicting its own :153-159 -- corrected in place naming DH.DG3.65. experiment:a00-157cc732-9a0afc: the probes[] RESIDUAL entry and body :20/:101/:105 name a00-5b52f00d:101 as uncorrected though c03601a725 corrected it -- restated as closed; the '15 sites corrected' row matches its own enumeration (count them); THOUGHT PROBE-B attributes `ip addr` to reds.py -- it lives in anonymize.py's hook (reds.py's only subprocess is _git).
DEMOTED (verify, refuted or not a defect): the 46-vs-31 production-lines note (each scoped to its own round); MISS1 (C6 is a real falsifier: fails on the base gate); MISS4 (reds' git show is covered by test_reds f2/f12b). UNVERIFIED, recorded only: item 5 of DH.DG3.64 rode in the harness auto-commit beabfae987, not a write.py commit.
COUNCIL   'the gate edits its own source and nothing gates it' -- carried to the council with the [decision], never a code change in this round.
ANON      no user name, home or repo path value, host or IP.
FILE SCOPE skills/agi-merge-pass/SKILL.md (restore only) · extensions/agi/tests/test_merge_gate.py · experiment:a00-a72539b5-099206 · experiment:a00-157cc732-9a0afc · the kid's own node. merge_gate.py is NOT in scope.
CEILING   HARD CAP: 1 kid · 0 production lines · test_merge_gate.py <= 195 lines TOTAL · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut; ask BEFORE, never after.
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit; run test_merge_gate.py test_reds.py test_council_report.py test_commands_manifest.py with --basetemp under /tmp and paste the counts.

## CORRECTIVE DH.DG3.67 -- closes mur-season2-loops-hypothesis-g716107-merge-gate-gi-a00-1cf7dc42 h107d-code + h107d-nodes (accept_with_residue, verify upheld)
BASE      CUT FROM season2/loops/hypothesis-g716107-merge-gate-gi-a00-1cf7dc42 tip e8643d3171 (worktree /mnt/agi-ram/worktrees/de-base-DG3.67). No merge. Never rebase.
1. This hypothesis node (write.py) -- testable_claim (:11), CLAIM 4 (:28) and FALSIFIER F6 (:39) [cites corrected from ~:13 / ~:25 by DH.DG3.68] still claim the skill retirement that DH.DG3.65 reversed (option A): each is marked MOVED to goal:g7.16.1.10.7.1 (minted horizon 01:5xZ 10-01), in place, naming DH.DG3.67 -- the scored claim at NEW = the gate code only.
2. .agi/nodes/.geometry/commands.md:3119 (the merge_gate.py:check row, write.py only) -- its reason names 'skill agi-merge-pass section 2 step 5a', which the restored skill does not carry: the reason says the gate is not yet wired into the PASS and names goal:g7.16.1.10.7.1. proposable stays false.
3. test_merge_gate.py C5 -- `src.count('subprocess.run') == 1` fails on a comment or docstring that merely names it: count CALLS with `ast` over the gate module's own source (merge_gate.__file__): exactly one call whose function is an attribute of `subprocess`, and it sits inside `_git`. A mutant with a second direct subprocess call FAILS the row; a mutant that only adds a comment naming subprocess.run PASSES it (say how you checked both).
4. test_merge_gate.py docstring -- C6 is DH.DG3.64 item 1, not DH.DG3.62; and the 'no test touches the live repo' sentence states its one exception honestly (C5 parses the gate module's own source, read-only).
5. Node honesty, experiment:a00-25b9567f-7b7291 (write.py): :45 Evidence row [cite corrected from :44 by DH.DG3.68 director close] restated to a measurement that is true (merge_gate.py does not exist at 8523e5e563; vs BASE c03601a725 the SKILL.md restore is 5 insertions / 6 deletions; the production cap is 0, not 40); :80 the commit refusal is the agent-git pre-commit hook (extensions/agi/hooks/agent-git/pre-commit), which ADMITS a branch kid in an isolated worktree -- never 'write.py refuses by design'; THOUGHT (4)'s standing rule ('the grep wins') leaves the round node (a standing rule lives in a template, not here: the director carries it up as a [rule] line).
DEMOTED (verify refuted): C5 line-number anchor (true as landed) · parent AUTH sha claim (write-log does carry node_id + sha256) · F2's host read (pre-existing, outside the diff) · the :114 cite (inside the named function) · 'four node sites' (frame wording) · a00-5b52f00d historical counts (time-qualified, out of scope). NOTED: the kid node's grid ref is owed by the merge's grid.py commit, not the round.
ANON      no user name, home or repo path value, host or IP.
FILE SCOPE extensions/agi/tests/test_merge_gate.py · .agi/nodes/.geometry/commands.md (the merge_gate.py:check reason only) · this hypothesis node (item 1) · experiment:a00-25b9567f-7b7291 · the kid's own node. merge_gate.py and SKILL.md are NOT in scope.
CEILING   HARD CAP: 1 kid · 0 production lines · test_merge_gate.py <= 195 lines TOTAL · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut; ask BEFORE, never after.
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit (the pre-commit hook admits a branch kid in its own worktree); run test_merge_gate.py test_reds.py test_council_report.py test_commands_manifest.py test_bin_help_smoke.py with --basetemp under /tmp and paste the counts.

## CORRECTIVE DH.DG3.68 -- closes mur-season2-loops-hypothesis-g716107-merge-gate-gi-a00-46e3ab5f h107e-code + h107e-nodes (accept_with_residue, verify upheld) -- executed by an Opus 5.5 subagent of DG3 (owner lanes 02:27Z)
BASE      CUT FROM season2/loops/hypothesis-g716107-merge-gate-gi-a00-46e3ab5f tip cfffd738f7 (branch de-base-DG3.68, worktree /mnt/agi-ram/worktrees/de-base-DG3.68). No merge. Never rebase.
1. test_merge_gate.py C5 (:183-187) -- containment is a lower bound only (a regression from the split-based guard at daacec388e:181): the single subprocess call lies within _git's lineno..end_lineno, AND merge_gate.py carries no `from subprocess import` (ImportFrom of subprocess = fail). Mutants: call moved to a helper defined after _git -> FAIL; a from-import call -> FAIL; a comment naming subprocess.run -> PASS (state how each was checked).
2. Node honesty (write.py only): experiment:a00-25b9567f-7b7291:51 'tier kid may not commit ... the known guard' corrected like its sibling row (the agent-git pre-commit hook, which admits a branch kid); experiment:a00-2656a173-cf9e09 :67 the same sentence, and :18 / :93 / :95 + THOUGHT (4) restated: items 2 and 5 ARE in the range, landed by the director's harvest commit 0e72419ae9; this hypothesis's CLAIM 2 (:26) names the accepting-verdict condition the gate applies (merge_gate.py verdict.startswith accept); the DH.DG3.67 block's cites (~:13 / ~:25) -> the real CLAIM 4 / F6 lines.
DEMOTED (director, measured): config:commands edited_by flip = write.py's own provenance stamp on every write, not a second edit · the harvest commit's write-log sha claim = the log is untracked by design (checked at harvest, sha256 equal, 3/3) · the MOVED marks dangle only until the chain merges onto the trunk, where goal:g7.16.1.10.7.1 lives (61dd3a0d68) · the merge_gate cells absent on MAIN = routed to the Prime (card BANKED), the gate answers rc 2 by design until set · 'the ONE live read' + StopIteration + name-based matcher (verify refuted).
CARRIED UP: template_max 'when a brief and a grep disagree the grep wins' -> a [rule] line from DG3 with the [merge-up], never a round-node sentence.
FILE SCOPE extensions/agi/tests/test_merge_gate.py · experiment:a00-25b9567f-7b7291 · experiment:a00-2656a173-cf9e09 · this hypothesis node (CLAIM 2 + the DH.DG3.67 cites only).
CEILING   0 production lines · test_merge_gate.py <= 195 lines TOTAL · 0 USD beyond the subagent.
EVIDENCE (ffef25a4fc, re-measured by verify h107f): helper-after-_git mutant FAIL · from-import mutant FAIL · comment-only mutant PASS; test_merge_gate.py 195 lines; 305 passed 8 skipped

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.DG3.68 + director close: C5 containment bounded on both ends + no subprocess from-import (verify h107f measured the three mutants); the node-prose residues h107f named closed by the director in-loop (no re-mur, per skill agi-corrective §3 row 1)
<!-- THOUGHT:END -->
