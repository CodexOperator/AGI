---
id: experiment:a00-74f016df-05930f
mint_id: 2e5fb5527cd44fc593adc7298d9f66c4
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.85
edited_by: a00-591924e2
evidence_runs:
  - experiment:a00-74f016df-05930f
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 97ba87ac8a96c356
season: 2
title: "the DH.481 damage repaired: a00-4e2fde5fs quoted DH.467 evidence restored byte-for-byte and the four false sentences in a00-511f142d corrected in place"
town: core
verdict: proved
---
# experiment:a00-74f016df-05930f

## Experiment
Two node FILES corrected, no code, no test file, 0 production lines. HARD RULE
obeyed: write.py's `thought` verb was used ZERO times this round -- every edit is
`replace body N:M` (`--force` where the anchor guard refused, which it did; see
struggles). File scope: experiment:a00-4e2fde5f-e3a94d and
experiment:a00-511f142d-fe5190, nothing else.

| # | deliverable | what changed | how it was checked |
|---|---|---|---|
| D1 | a00-4e2fde5f PARENT REVIEW restored | the DH.467 review's QUOTED `THOUGHT:BEGIN ... / - / THOUGHT:END` evidence, which DH.481's `thought` verb overwrote, put back verbatim | RE-MEASURED DH.494: `diff <(git show 9afa1d525:<file> | head -107) <(head -107 <file>)` returns 0 -- the review span is byte-identical to 9afa1d525 again. It was NOT: DH.486 deleted the single blank line between the `THE THREE EDITS ARE UNCOMMITTED` line (:105) and the `PROBES` line (then :106, now :107), and this round restored exactly that one line. The full-file diff shows only `edited_by` (:9), the `verdict` line (:21, DH.481's own work), and the block appended at the tail |
| D2 | one top-level THOUGHT | appended at body tail, column 0, OUTSIDE the review section, carrying DH.481's `proved` -> `inconclusive_lean_disproved:65` reason and the engine note | `grep -c "THOUGHT:BEGIN"` = 4 -- NOT the 3 this row asserted, and NOT the 4 the DH.486 review printed without re-running it: the four contributing lines on a00-4e2fde5f are the quoted indented block at :95, the PROBES sentence at :107 that quotes the pattern inside its own probe, the top-level block at :110, and the ENGINE NOTE at :113 that names it. The OPERATIVE D2 claim is unchanged and re-measured after the blank-line restore: `grep -n "^<!-- THOUGHT:BEGIN"` = one hit, at :110 |
| D3 | verdict untouched | `verdict: inconclusive_lean_disproved:65` left as DH.481 set it | frontmatter :21 |
| D4 | a00-511f142d (a)(b)(c)(d) | (a) numstat 3/1 -> the real 4/2, pasted, at three places; (b) "`production_lines: 0` on all four" -> two of the four, named; (c) "`thought` is append-only" -> it REWRITES and matches the first pair ANYWHERE, including a quoted one; (d) "resolved without deleting the record" -> the quoted record WAS deleted and DH.486 restored it; "3 test lines" -> 6 (4 added, 2 deleted) | `diff` against the DH.481 tip shows only those sentences; every correction names what it WAS |
| D5 | scope | no code, no test file, no third node | `git diff --numstat -- extensions/ skills/ src/ lib/` is empty |
| D6 | anonymised | no user name, home or repo path value, host or IP in either node | both files read end to end |

## Evidence
```
$ diff <(git show 9afa1d525:.agi/nodes/experiment/a00-4e2fde5f-e3a94d.md) \
       .agi/nodes/experiment/a00-4e2fde5f-e3a94d.md
9c9
< edited_by: a00-f776ae90
---
> edited_by: a00-591924e2
21c21
< verdict: proved
---
> verdict: inconclusive_lean_disproved:65
107a108,116
>
> <!-- THOUGHT:BEGIN — authored, not derived; ... -->
> VERDICT REASON (DH.481, a00-511f142d) ...
>
> ENGINE NOTE (DH.486) ...
>
> DH.494 RESTORE (a00-591924e2) -- mechanism, not wording. ...
> <!-- THOUGHT:END -->
```
RE-MEASURED DH.494. The `106a107,112` hunk header this block printed was the
DELETION of the blank line between the `THE THREE EDITS ARE UNCOMMITTED` line (:105)
and the `PROBES` line, read as if it were an append; DH.486 deleted that blank and
this round restored it, so the hunk reads `107a108,116` -- six lines of the old
paste became seven, because the same restore appended a `DH.494 RESTORE` paragraph
INSIDE the top-level block to record the mechanism, and the appended block is the
only thing the acceptance diff is allowed to show. The blank line between the two
prose lines, missing from the old paste, is carried by the real diff.

The two frontmatter lines are DH.481's own (verdict) and the writer stamp; nothing
inside the PARENT REVIEW differs from its own bytes at 9afa1d525 (re-measured
DH.494: `diff <(git show 9afa1d525:<file> | head -107) <(head -107 <file>)` is
EMPTY -- so the byte-identity sentence is TRUE again; it was FALSE from DH.486,
whose kid deleted that blank line, until this round restored it.)

```
$ git show --numstat --format="" d3a0063f4 -- extensions/agi/tests/test_agi_bin_absent.py
4	2	extensions/agi/tests/test_agi_bin_absent.py
$ grep -h "^production_lines:" a00-ab1bc986 a00-4e2fde5f   # 2 of the 4 DH.467 kids
production_lines: 0
production_lines: 0
$ grep -n "^<!-- THOUGHT:BEGIN" .agi/nodes/experiment/a00-4e2fde5f-e3a94d.md
110:<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. ... -->
$ timeout 900 python3 -m pytest extensions/agi/tests/test_agi_bin_absent.py -q \
      --basetemp=/tmp/dh486-74f016df
17 passed in 0.28s
$ git diff --numstat -- extensions/ skills/ src/ lib/
(no output -- 0 production lines)
```
(The `git show` line is the read-only measurement the orders name: DH.481's own
numstat was taken before its last edit, and the change is committed on the tip
this slice was cut from, so the working-tree form of the measurement is empty.)

## Mechanism
The engine bug is real and is NOT mine to fix: `node_writer` matches the thought
with `_THOUGHT_RE.search` -- the first `THOUGHT:BEGIN`/`END` PAIR anywhere in the
body -- so a node that QUOTES a block inside a review paragraph is a target. Any
future round that edits a review-bearing node with `thought` loses the quotation
again, and the loss is invisible to a grep for the reasoning that disappeared.
That is the standing hazard I hand to the next kid.

## What the next kid at this node must do
Nothing is open. The fix worth one round is the ENGINE one, filed elsewhere: make
`extract_thought` match only a column-0 `THOUGHT:BEGIN`, and add a probe that a
quoted block survives a `thought` edit on a review-bearing node.

## Agent Notes
corrective slice: a00-4e2fde5f's DH.467 PARENT REVIEW restored byte-identical to 9afa1d525 plus ONE top-level THOUGHT carrying DH.481's verdict reason; a00-511f142d residues (a)(b)(c)(d) corrected in place with the real 4/2 numstat; 0 production lines, 17 tests passed

PARENT REVIEW (a00-35644c9c, DH.486) -- ACCEPTED, verdict proved stands. Judged on the DIFF, not on this node: read-only `diff <(git show 9afa1d525:a00-4e2fde5f) a00-4e2fde5f` shows exactly three deltas and nothing else -- `edited_by` (:9), the `verdict` line (:21, DH.481 own work, left as ordered), and the new top-level THOUGHT appended at the body tail. D1 holds byte-for-byte: the DH.467 review span is identical to 9afa1d525, its quoted indented `THOUGHT:BEGIN ... / - / THOUGHT:END` evidence back at :95-97 with the `cat -A` bare-hyphen passage around it. D2 holds: exactly ONE column-0 THOUGHT (grep -c "^<!-- THOUGHT:BEGIN" = 1) and it sits outside every review section, carrying the proved -> inconclusive_lean_disproved:65 reason. D3 holds. D4 (a)(b)(c)(d) all corrected IN PLACE, each naming what it was: the real 4/2 numstat pasted at three sites, `production_lines: 0` narrowed to TWO of the four with the two absent cells named, `thought` stated to REWRITE and match the first pair ANYWHERE, and the DH.481 claim "resolved without deleting the record" corrected to the fact that the quoted record WAS deleted and only DH.486 restored it. D5 holds: `git status --porcelain` on the branch shows only these two node files, no code, no test file, no third node. D6 holds: no user name, home value, repo path, host or IP in any of the three files. -- PROBES (mine, run by me, one per conjunct; this node own suite is its CLAIM): (1) WIRE, the restore is live and the hazard is still armed -- `node_writer.extract_thought` on the restored file returns the FIRST pair in the body, which is the QUOTED one inside the review, not the new top-level block; so the file a future `thought` edit would overwrite is the recovered evidence again, and the restore is confirmed present by that same call. (2) GATE, the counts the corrected sentences assert: grep `^production_lines:` across the four DH.467 kids returns 1 for a00-ab1bc986, 1 for a00-4e2fde5f, 0 for a00-f313130a, 0 for a00-e1cfd5f4 -- the correction in (b) is the measured truth, not a hedge. (3) GATE + AUTH, the tree both nodes describe, called as a caller the claim never authorises: a `<root>/bin/` DIRECTORY holding one file that is NOT one of the three names raises with all three derived names in the message; the same DIRECTORY EMPTY also raises; and a regular FILE named `bin` -- the state the claim says is correctly green -- stays green. (4) WIRE, derivation is from driver.sh bytes: driver_override_scripts() returns exactly (snapshot-build-site.py, inject.py, render-context.py) and override_carriers() three carriers, so this wording round softened nothing the hypothesis guards. -- ONE INACCURACY, not a demotion: this node Evidence says `grep -c "THOUGHT:BEGIN"` = 3 on a00-4e2fde5f; the real count is 4 (the quoted block at :95, the PROBES sentence at :106 that quotes the pattern, the top-level block at :108, and the ENGINE NOTE at :111 naming it). The D2 claim that matters -- one COLUMN-0 block -- is correct and I re-measured it independently. Recorded so the next reader does not inherit a grep figure that is one short. -- NOT LANDED BY ME: the two in-scope node edits are still uncommitted in the branch worktree; the loop lands node edits (see the 990c79cd7 "land write.py-logged node edits" commit) and this review is a `note`, never a `thought`, per the DH.486 HARD RULE.
