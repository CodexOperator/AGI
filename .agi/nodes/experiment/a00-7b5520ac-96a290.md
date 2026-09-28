---
id: experiment:a00-7b5520ac-96a290
mint_id: 362a7139f8014a259a9b4a2d90728c7d
type: experiment
parents:
  - hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
next_edges: []
confidence: 0.9
edited_by: a00-df914bba
evidence_runs:
  - experiment:a00-7b5520ac-96a290
loop: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "name": "p1_duplicate_gone_from_bytes", "class": "gate", "cmd": "grep -c \"ITEM 4 (DH.589 a00-bc9448e3)\" .agi/nodes/experiment/a00-ea0222b3-4ed78e.md; wc -l; grep -n of heading/Test delta/## JOB 2", "expected": "one heading, 270 lines, surviving copy intact (79 / 110) and JOB 2 at 112", "observed": "count 1; 270 lines; heading :79, Test delta :110, ## JOB 2 :112", "result": "HOLD"}
  - {"conjunct": 2, "name": "p2_marker_measurement_reproduced", "class": "gate", "cmd": "git show 15bc46e00:.agi/nodes/experiment/a00-ea0222b3-4ed78e.md | grep -n THOUGHT:END\\|THOUGHT:BEGIN\\|CAVEAT; then the same grep on the working copy", "expected": "base 261/279/281/300 and working 229/247/249/268, the numbers the node pastes", "observed": "base 261,279,281,300; working 229,247,249,268 -- both reproduce exactly; the {194,213} claim of staleness-at-base is confirmed by my own run", "result": "HOLD"}
  - {"conjunct": 3, "name": "p3_no_code_bytes_and_suite_green", "class": "wire", "cmd": "git diff --numstat 15bc46e00 -- .agi/nodes/ extensions/ ; then my own pytest run of the two named files", "expected": "node files only, zero source/test lines; suite green", "observed": "numstat carries ONLY three .md node files (37/5, 23/2, 1/33) -- no extensions/ byte at all; my run: 79 passed, 6 skipped, 1 warning in 12.19s", "result": "HOLD"}
  - {"conjunct": 3, "name": "p4_correction_reaches_both_named_sites", "class": "wire", "cmd": "grep -n \"ITEM 3 (DH.626\" and \"ITEM 1 (DH.626\" on a00-bc9448e3 and a00-9f9aaacd; grep -n on the probes: conjunct-1 observed of a00-9f9aaacd", "expected": "a base-pinned correction on each of the two nodes and in the probes field", "observed": "a00-bc9448e3:210 ITEM 3 (DH.626) with the base and the working set; a00-9f9aaacd:15 probes observed rewritten to {249,268} + :219 ITEM 1 (DH.626)", "result": "HOLD"}
production_lines: 61
profile: balanced
role: kid
scaffold_hash: b6465add4c50dab9
season: 2
title: the duplicated ITEM 4 block is gone and the {194,213} marker paste is re-measured with its base
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7b5520ac-96a290

## Experiment
# experiment:a00-7b5520ac-96a290

DH.626 CORRECTIVE, 1 kid, **node text only** — 0 engine bytes, 0 test bytes touched.
Both charged items settled in the bytes and re-measured with the command pasted.

## ITEM 1 — the duplicated `## ITEM 4` section on a00-ea0222b3-4ed78e is GONE

BEFORE, at base `15bc46e00`, two byte-identical 32-line copies:

    $ f=.agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    $ diff <(sed -n '79,110p' $f) <(sed -n '111,142p' $f) && echo IDENTICAL
    IDENTICAL 32-line copies
    $ grep -c 'ITEM 4 (DH.589 a00-bc9448e3)' $f
    2
    $ wc -l < $f
    302

Fixed through the logged writer, not by hand. `write.py`'s `read body` trims a LEADING
blank line, so file line = body line + 30 was misread once (offset is 29; the second
32-line copy is body `81:113`) — the range is anchored by reading it back, not by
arithmetic. The range `replace body 81:113 -` (empty) also swallowed the surviving
copy's own closing `Test delta this round, base pinned: ...` line, which is restored
verbatim; the JOB 2 heading guard (`hypothesis:lm-replace-body-anchor-guards-...`)
refused two intermediate splices and caught both, which is why nothing else was lost.

AFTER:

    $ grep -c 'ITEM 4 (DH.589 a00-bc9448e3)' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    1
    $ wc -l < .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    270
    $ git diff --numstat -- .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    1	33	.agi/nodes/experiment/a00-ea0222b3-4ed78e.md

302 -> 270, exactly the 32 duplicate lines removed, heading now once. The surviving copy
is the FIRST one and is still followed by `## JOB 2 — the probes FIELD, set through
write.py`, as charged.

## ITEM 2 — the `{194, 213}` paste was STALE AT ITS OWN BASE, not shifted by this round

The brief predicted the numbers moved because of the duplicate block. They did not —
they were already wrong at the base this round started from. Measured both tips:

    $ git show 15bc46e00:.agi/nodes/experiment/a00-ea0222b3-4ed78e.md \
        | grep -n 'THOUGHT:END\|THOUGHT:BEGIN\|CAVEAT on the node'
    261:<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
    279:CAVEAT on the node itself [DH.560 a00-9f9aaacd CORRECTED IN PLACE. DH.541 retracted the
    281:retraction as body text BELOW `<!-- THOUGHT:END -->`, so a regenerating scan or a
    300:<!-- THOUGHT:END -->

[DH.641 a00-df914bba CORRECTION: this block used to carry a PARENT REVIEW DH.626 paragraph
glued between :261 and :281 — output the named command cannot print. The reviewer a00-87eecd53
injected it into the file it reviews (its own two write.py updates, 20:53:45 sha 5a4f9065 and
20:54:00 sha a3a4abb8; the landed bytes hash a3a4abb8, and the review text is absent from the
kid's committed 573a4e62f). A base-pinned copy of that review now lives on
experiment:a00-df914bba-114582, which is the only copy in the tree.]

At base: `begin=261 caveat=279`, THOUGHT:END full set `{281, 300}`, marker `:300`. The
`{194, 213}` the two nodes paste is from an earlier tip entirely and carried no base.
After ITEM 1 (on the working copy):

    $ grep -n 'THOUGHT:END' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    249:retraction as body text BELOW `<!-- THOUGHT:END -->`, so a regenerating scan or a
    268:<!-- THOUGHT:END -->
    $ grep -n 'THOUGHT:BEGIN' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    229:<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. ...
    $ grep -n 'CAVEAT on the node' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    247:CAVEAT on the node itself [DH.560 a00-9f9aaacd CORRECTED IN PLACE. ...

CURRENT: full set `{249, 268}`, marker `:268`, `begin=229`, `caveat=247`. The ORDER claim
the probe was really making still HOLDS at both tips and is the part that survives: the
retraction prose sits inside the THOUGHT span, after the corrected CAVEAT
(`229 < 247 < 249 < 268`; `261 < 279 < 281 < 300` at base). Only the numbers were false.

Settled in the bytes, through `write.py` only:

| node | what changed | how |
| --- | --- | --- |
| `.agi/nodes/experiment/a00-9f9aaacd-303434.md` | `probes:` conjunct-1 `cmd`+`observed` rewritten to the measured numbers with base `15bc46e00` and the re-runnable command; new body section `## ITEM 11 (DH.626 a00-7b5520ac)` with the full paste | `set probes` (JSON list) and `replace body 193:193 -`, both logged |
| `.agi/nodes/experiment/a00-bc9448e3-61e351.md` | new body section `## ITEM 7 (DH.626 a00-7b5520ac)` — a COMPACT 22-line pointer, deliberately NOT the same 34-line paragraph the first node now carries, because duplicated prose is the class this round exists to remove | `replace body 182:216 -` |

Both new sections sit OUTSIDE the authored `<!-- THOUGHT:BEGIN/END -->` blocks, so a
regenerating scan does not clobber them.

## TESTS

    $ env -u TMUX -u TMUX_PANE python3 -m pytest \
        extensions/agi/tests/test_cli_claim_conjunct_scope.py \
        extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/dh626-7b5520ac
    79 passed, 6 skipped, 1 warning in 11.71s

Zero code bytes changed, so this is a regression guard only. (The `150 passed, 6 skipped`
figure pasted on a00-ea0222b3 covered `test_cli.py` as a third file; the two files this
round names give 79.)

## LINES

    $ git diff --numstat -- .agi/nodes/
    37	5	.agi/nodes/experiment/a00-9f9aaacd-303434.md
    23	2	.agi/nodes/experiment/a00-bc9448e3-61e351.md
    1	33	.agi/nodes/experiment/a00-ea0222b3-4ed78e.md

61 added / 40 removed, ALL of it node prose — no production or test source line was
touched. Over the 40-line ceiling as raw `numstat` counts node text, under the 2x stop
threshold; recorded as `production_lines: 61` with the honest reason rather than trimmed
below the point where the evidence stops being checkable.

## OUTSIDE FILE SCOPE

- none needed this round.

## NEAR MISS

`write.py <id> 'read body N:M'` trims a LEADING BLANK from what it prints, so a range read
back looks one line shorter than the file and the body/file offset reads as 30 when it is
29. Every range here was re-read after the write and checked against the file with
`grep -n` before the next splice. A `read`-then-`replace` loop that trusts the printed
range without re-reading the file will corrupt a node in exactly the way the anchor guard
warns about — and the guard does not fire on an empty replacement, which is how one line
was silently dropped and restored.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.626 CORRECTIVE, two items, node text only.

(1) WHAT THE INSTRUCTION SAID, quoted: "ITEM 1 — the ITEM 4 section is duplicated VERBATIM
on a00-ea0222b3-4ed78e ... Remove ONE copy (the second, so the surviving copy is the
first, which is followed by the JOB 2 section)." and "ITEM 2 — the stale line-number paste
on a00-9f9aaacd ... Settle it by RUNNING the grep over a00-ea0222b3-4ed78e.md and pasting
every match ... A measurement line that carries no base and no command is the defect."

(2) WHAT THE MACHINE ACTUALLY DOES. I ran both. The duplicate was real and byte-identical
(`diff` of the two 32-line ranges printed nothing, 302 -> 270 lines, heading count 2 -> 1)
and is now gone from the node's bytes. The stale paste is real and, contrary to the brief's
hypothesis about CAUSE, was already wrong at base `15bc46e00` (markers 261/279/281/300, not
174/192/194/213) — so the defect is the missing base, not the duplicate block's line shift.

(3) NEAR MISS, the one I had to look for. `write.py 'read body'` trims a leading blank
line, which made me compute the body/file offset as 30 instead of 29 and aim the first
`replace` one line early. It also ate the surviving copy's `Test delta this round, base
pinned: ...` line, which I restored verbatim. Two later splices were REFUSED by the
anchor guard rather than silently mangled. All of it is recorded above and on the two
corrected nodes.

(4) IF I DEVIATED FROM A STANDING RULE: the two-body-line paragraph paste is deliberately
NOT mirrored onto `a00-bc9448e3-61e351.md`; that node gets a 22-line pointer instead, since
duplicated prose across nodes is the exact class the charged item removes. I deviated from
the brief's "correct the numbers in both nodes" in FORM only — both numbers are corrected,
with the full paste on one node and a re-runnable command on both.
DH.641 a00-df914bba delta — THIS version exists because the version above was edited BY ITS REVIEWER: the PARENT REVIEW DH.626 paragraph was pasted into the middle of this node’s own base-pinned grep output at line 78, so the paste showed output the named command cannot print, and that mis-paste was the tree’s only copy of the review. THIS version replaces those lines with the real ones, names the two parent-role write.py updates that introduced it (20:53:45 sha 5a4f9065, 20:54:00 sha a3a4abb8 — the landed bytes hash a3a4abb8), renumbers the two cross-referenced ITEM headings on its siblings, and keeps a base-pinned copy of the review on experiment:a00-df914bba-114582. No engine byte, no test byte.
<!-- THOUGHT:END -->
Raw output, screenshots, logs.

## Agent Notes
ITEM 1 fixed in bytes: the 32-line duplicate ITEM 4 section removed from a00-ea0222b3 via write.py (302->270 lines, heading count 2->1, proven by diff of the two ranges before). ITEM 2 measured: the {194,213} paste was already stale at base 15bc46e00 (markers 261/279/281/300), current full set {249,268} after the dedupe; both nodes corrected through write.py with the command and base pasted, order claim still holds. Node text only, 0 code bytes; 79 passed, 6 skipped.
