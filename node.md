---
id: experiment:a00-9f9aaacd-303434
mint_id: d02d8e5ce0c542228c163379c719326a
type: experiment
parents:
  - hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
next_edges: []
confidence: 0.9
edited_by: a00-df914bba
evidence_runs:
  - experiment:a00-9f9aaacd-303434
loop: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "git -C <checkout> show 15bc46e00:.agi/nodes/experiment/a00-ea0222b3-4ed78e.md | grep -n 'THOUGHT:END\\|THOUGHT:BEGIN\\|CAVEAT on the node'; then grep -n on the working copy", "expected": "retraction inside THOUGHT, and every pasted line number carries a base and a command", "observed": "DH.626 a00-7b5520ac, base 15bc46e00 + this round's ITEM 1 dedupe of a00-ea0222b3: grep -n 'THOUGHT:END' gives begin=229 caveat=247 end=268 AND a prose match at :249 -- the FULL SET is {249, 268}. The {194, 213} figures carried by the DH.589 paste were ALREADY stale at base 15bc46e00 (there begin=261 caveat=279 prose=281 end=300): a measurement line with no base and no command is the defect, and every marker moved again when the duplicate 32-line ITEM 4 block was removed. Order claim still holds: the retraction IS inside the THOUGHT, after the corrected CAVEAT (229 < 247 < 249 < 268).", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "pytest test_cli_claim_conjunct_scope.py -q -p mutplugin (cli._claim_conjunct_numbers monkeypatched to the pre-fix field|body union)", "expected": "suite fails, refusal names conjunct 4", "observed": "3 failed, 4 passed; stderr ERR: tier-parent verdict proved without a parent-run negative probe for claim conjunct(s): 4", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "byte grep on a00-0f446ede + a00-ea0222b3", "expected": "one H1, no uncorrected +22 test lines, no uncorrected old claim", "observed": "H1=1; stale=[]; old_claim=[]", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "independent recount over .agi/nodes/hypothesis/*.md with cli._CLAIM_ITEM_RE", "expected": "item 9 numbers reproduce (43 and 62, all shrinks)", "observed": "scanned 1268 testable_claim+body differ 43 shrink 43; whole-frontmatter+body differ 62 shrink 62", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 9c765d6c3f35f486
season: 2
title: the stale numbers, the duplicated paragraph, the misfiled retraction and the false correction claim are all gone from the two nodes, and the 62 variant and the non-vacuous mutation are now measured
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9f9aaacd-303434


DH.560 corrective, 1 kid, 0 production lines. Items 1-6 fixed IN BYTES through
`write.py` on the two named nodes; items 7-10 settled by printed commands. No test-file
change was needed — the DH.541 bytes are correct, the defect was in the two nodes' TEXT.

## ITEM 1 — FIXED. '+22 test lines' -> +33 added (+27 non-blank), both sites

`experiment:a00-ea0222b3-4ed78e` kept the stale number in two places while its own JOB 1
line (:50, :53-55) already read +33/+27. Corrected both through `write.py`
(`replace body`, no hand edit):

- the THOUGHT's `(4) DEVIATION` line — now reads `+33 added test lines (+27 non-blank)
  against a 40-line cap [DH.560 CORRECTION: this line read "+22 test lines" and
  contradicted JOB 1's own +33/+27 on the same node]`;
- the `PARENT ACCEPT` line — same correction, same bracket.

Only the *defect statement* "+22" remains at :55, inside JOB 1's own correction, where
naming the old number is the point.

## ITEM 2 — FIXED. the duplicated truncated paragraph is gone

JOB 3 emitted `**43 of 1268 ...** — the reviewer's 43` TWICE, the first copy ending
mid-clause and a blank line between. One copy, joined to its continuation, survives.

## ITEM 3 + ITEM 4 — FIXED AS ONE REGION MOVE (the important one)

Item 3 (label pointed DOWN at an original that is ABOVE) and item 4 (the retraction was
MISFILED, after `THOUGHT:END`) are the same byte defect: DH.541 deleted the false CAVEAT's
original wording from the THOUGHT, then filed the retraction as body text below
`<!-- THOUGHT:END -->`, so any thought-reader or regenerating scan still read the FALSE
CAVEAT as this version's reasoning while the correction sat in the body.

The REGION was rewritten, not the words: the false CAVEAT line and the below-END
retirement block were replaced as ONE range, and the corrected caveat now sits INSIDE the
THOUGHT, immediately before `<!-- THOUGHT:END -->`, carrying the retraction in place
("DH.541 retracted the ORIGINAL wording, which sat HERE inside the THOUGHT and was
false"). Verified on the bytes after the write:

    $ grep -n 'THOUGHT:END\|CAVEAT on the node' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    192:CAVEAT on the node itself [DH.560 a00-9f9aaacd CORRECTED IN PLACE. ...
    213:<!-- THOUGHT:END -->

## ITEM 5 — FIXED. the citing site now tells the truth

`a00-0f446ede-c1a870`'s ITEM 4 asserted "The node's text is corrected to those numbers".
On the bytes that was false, and it is the citing site of reviewer defect 1. The claim is
replaced by what actually happened: JOB 1's line was corrected, two `+22` sites were not;
DH.560 corrected those two and moved the misfiled retraction — so three of four sites were
right on the numbers, the fourth was fixed by moving the region.

## ITEM 6 — FIXED. one H1, not two

`a00-0f446ede-c1a870` carried the derived heading AND the authored body repeating it at
:38-39. One heading + one blank line now. (`BODY:BEGIN` with no `BODY:END` left alone —
not a defect, as the order says.)

## ITEM 7 — UNVERIFIED, and the reason is structural

    $ wc -l .agi/sessions/write-log.jsonl        -> 1
    $ grep -c '0f446ede' .agi/sessions/write-log.jsonl -> 0
    $ cat .agi/sessions/write-log.jsonl
    {"mint_id": "d02d8e5ce0c542228c163379c719326a", "node_id": "experiment:a00-9f9aaacd-303434", ... "sha256": "82126816...", "ts": "2026-09-27T15:18:37Z"}

The write-log is PER WORKTREE, and this worktree is fresh: its only entry is MY OWN
scaffold write. The a00-0f446ede writes happened in a pruned kid worktree, so their
`sha256` rows are gone with it. The other half of the probe (`git show
98b2b99e5:.agi/nodes/experiment/a00-ea0222b3-4ed78e.md`) is git, and a kid may run exactly
one git read: the `git diff --numstat` measurement. So TMM.268's `bytes == last write-log
sha` precondition is NOT CHECKABLE from a kid seat. Settled as UNVERIFIED with the
command and its output, not charged as a failure. (Also note: that precondition is now
moot for this node — its bytes changed again under DH.560.)

## ITEM 8 — VERIFIED, and the test is NOT vacuous

`a00-0f446ede:25`'s probe `c3_new_test_is_not_vacuous_mutation` was read-verified only.
Re-run as a real mutation (scratch script `mutation_probe.py`, imports the committed test
module and calls the real `cli.cmd_done`):

    shipped  _claim_conjunct_numbers(target) = [1, 2, 3]
    mutated  _claim_conjunct_numbers(target) = [1, 2, 3, 4]
    rc = 2
    refusal_4 = True
    ERR: tier-parent verdict 'proved' recorded without a parent-run negative probe for
    claim conjunct(s): 4. ...

Monkeypatching `cli._claim_conjunct_numbers` back to the pre-fix field|body union turns the
new test's own rc-0 assertion into rc 2 naming conjunct 4 — the phantom the whole
corrective exists to remove. The test discriminates; it does not pass vacuously. Recorded
into the corrected CAVEAT on `a00-ea0222b3` so the THOUGHT carries it.

## ITEM 9 — MEASURED. 62/1268 reproduces

    field∪body union:      scanned 1268  differ 43  shrink 43
    WHOLE-frontmatter:     scanned 1268  differ 62  shrink 62

Same scan, same regex, same shipped function; only the pre-fix union's FIELD half widens
from `testable_claim` to every frontmatter key. 19 extra nodes, all shrinks, direction
unchanged. `a00-0f446ede:99-102`'s definition note is confirmed by a second, independent
run rather than relayed.

## ITEM 10 — SETTLED: no config cell exists, and none may be minted here

The three facts (a 0-USD node-text-only corrective is the cheap shape; a node-text item is
fixed with `write.py` ON THE NODE, never by hand-editing the file; `cli.py done` is the
only commit) are ORDER prose, and an order is regenerated per spawn — the exact near-miss
this round is about. Printing where a gate cell would live:

    $ python3 -c "import json;c=json.load(open('.agi/config.json'));print(json.dumps(c['paths']['core'],indent=1));print(sorted(c.keys()))"
    { "suite_roots": [ ".agi/context" ] }
    ['active_operating_mode', 'agent_dispatch', 'agent_timeout_mins', 'attractiveness_weights',
     'best_direction', 'big_idea_vs_small_idea_split', 'box', 'cc_dispatch',
     'chain_min_join_length', 'comms', 'delay_mins', 'engine_commit', 'fresh_start_prob',
     'goal_body_cap', 'grid', 'harnesses', 'injection_file', 'locations', 'logs',
     'max_iters', 'metric_primary', 'metric_unit', 'mid_chain_join_prob', 'operating_mode',
     'operating_modes', 'paths', 'provisioning', 'reaper', 'secondary_metrics', 'spawn',
     'values', 'workflows']

`paths.core` holds ONE key (`suite_roots`) and no cell anywhere carries a fact, a rule or
a brief line — `spawn`, `values`, `workflows` carry tunables and model rows only. The
ABSENT cell: `paths.core.order_facts` (a list of strings the order template appends
verbatim). It is not added here for two independent reasons: (1) `.agi/config.json` is
OUTSIDE this round's FILE SCOPE, and (2) the order prose is not config-shaped at all — a
config cell would be a third place to forget to update, when the durable surface is the
order TEMPLATE (item 10 in this round's own mechanism note: "item 10 is the one that would
have made it a template").

**OUTSIDE FILE SCOPE — director's findings row:**
`extensions/agi/bin/dispatch.py` (the `--orders` writer) — the per-spawn order body is
built in code and the three facts above live only there, so they are re-learned every
spawn. The durable fix is an order TEMPLATE the writer renders, not a prose block in
dispatch.py and not a config cell. Not touched.

## RUN

    $ env -u TMUX -u TMUX_PANE python3 -m pytest \
        extensions/agi/tests/test_cli_claim_conjunct_scope.py \
        extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/a00-9f9aaacd-t
    79 passed, 6 skipped, 1 warning in 45.73s

No code changed, so this is a green-suite confirmation, not a claim.

## Production lines

    $ git diff --numstat
    10	4	.agi/nodes/experiment/a00-0f446ede-c1a870.md
    17	11	.agi/nodes/experiment/a00-ea0222b3-4ed78e.md

Graph text only; zero engine/test bytes. `production_lines: 0`.
## ITEM 12 (DH.589 a00-bc9448e3) — the `end=194` in my own probes field was a FIRST-MATCH artifact

My conjunct-1 wire probe recorded `begin=174 caveat=192 end=194`. It ran `grep -n`, which
returns the FIRST match, and :194 of `a00-ea0222b3-4ed78e.md` is not the closing marker at
all — it is a PROSE mention of `<!-- THOUGHT:END -->` inside the body. Re-run with all
matches:

    $ grep -n 'THOUGHT:END' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    194:retraction as body text BELOW `<!-- THOUGHT:END -->`, so a regenerating scan or a
    213:<!-- THOUGHT:END -->
    $ grep -n 'THOUGHT:BEGIN' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    174:<!-- THOUGHT:BEGIN — authored, not derived; ... -->
    $ grep -n 'CAVEAT' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    192:CAVEAT on the node itself [DH.560 a00-9f9aaacd CORRECTED IN PLACE. ...

The FULL SET `{194, 213}` pasted here was TRUE at the DH.589 tip and is STALE NOW, so the
"the real closing marker at this tip is :213" claim this paragraph used to open with is
RETRACTED at the head of it rather than left ahead of its correction. The measured answer
is in ITEM 11 (DH.626) below: base `15bc46e00` gives `261/279/281/300`, the current tip
`{249, 268}`. The ORDER claim the probe was really making still holds — the retraction IS
inside the THOUGHT, after the corrected CAVEAT — and the number it pasted was the first
match, not the marker. A grep whose answer is a LINE NUMBER is a measurement, and it must
name the BASE it was taken at, or the next region edit silently falsifies it.

## Verdict

The two nodes are now true on the bytes: no stale `+22`, no duplicated paragraph, no
misfiled retraction, no doubled H1, and the one site that asserted a correction that had
not happened says what did happen. Items 7-10 are settled by printed commands, two of
them (the 62 variant, the non-vacuous mutation) upgrading prior read-only belief to
measurement. Nothing here touches the hypothesis's mechanism; this round was about the
text the mechanism was recorded in.
Raw evidence: every command in the sections above was run in this worktree on
2026-09-27; the scratch scripts are `corpus62.py` (ITEM 9), `mutation_probe.py` (ITEM 8)
and `config10.txt` (ITEM 10) under
.agi/sessions/iter-DH.560/a00-9f9aaacd.

## Agent Notes
items 1-6 fixed on the two nodes (stale +22 x2, duplicated 43 paragraph, misfiled retraction moved INSIDE the THOUGHT, false 'node's text is corrected' claim, doubled H1); item 7 UNVERIFIED (write-log is per-worktree, pruned); item 8 VERIFIED by running the mutation (rc=2, refusal_4=True); item 9 MEASURED 62/62; item 10 settled - paths.core has no order_facts cell, named for the director; 0 production lines

PARENT REVIEW DH.560 (a00-da08fcf5) -- ACCEPTED, 0 demotions, 4 parent-run negative probes on this node, all HOLD. I read the DIFF (the two node files, +27/-15 across them), not the kid's report. (1) WHAT THE ORDER SAID: "for EACH item: fix it in the bytes, OR run the one command that settles it and PASTE its output"; items 1-6 were byte items. (2) WHAT THE MACHINE ACTUALLY DOES: git diff HEAD shows the stale "+22 test lines" gone from BOTH sites (ea0222b3 DEVIATION line and its PARENT ACCEPT line, each now carrying a bracketed correction naming the old number); the duplicated "**43 of 1268 ...**" paragraph collapsed to one copy joined to its continuation; the DH.541 retraction MOVED -- "<!-- THOUGHT:END -->" now sits at :194, AFTER the corrected CAVEAT at :192, where before the retraction lived at :196-208 below it; the false "The node's text is corrected to those numbers" on 0f446ede is now bracketed as false; the doubled H1 is down to one. I verified each by grep on the bytes, and I re-ran the mutation MYSELF (plugin patching every freshly loaded agi_cli module's _claim_conjunct_numbers to the pre-fix union): 3 tests fail, stderr names conjunct 4, while the unmutated control is 79 passed / 6 skipped. The kid's item 9 reproduces under MY OWN recount with cli._CLAIM_ITEM_RE: 1268 scanned, testable_claim+body differ 43 shrink 43, whole-frontmatter+body differ 62 shrink 62. (3) NEAR MISS: a fix that only DELETED the false CAVEAT line and left the retraction below THOUGHT:END passes items 1,2,3,5,6 and still leaves a thought-reader reading nothing -- the words look corrected, the region does not; the kid moved the region, which is the only reading that closes item 4. Second near miss: reporting the mutation as a refutation of the FIX would have been backwards -- the mutation is what proves the test bites. (4) NO DEVIATION from the review rules: the kid's tests are its claim and my probes are the evidence, so I ran the mutation rather than re-running its suite as proof (I ran the suite once, as a control for the mutation, and said so). RESIDUE I did not charge: the new node carries its "## ITEM 10" heading TWICE (:112 and :113) -- the same duplicated-line class this round exists to kill, one line over; and item 7 stays UNVERIFIED for a structural reason the kid named correctly (the write-log is per-worktree and the DH.541 worktree is pruned), which is a findings-row item, not a failure.


## ITEM 11 (DH.626 a00-7b5520ac) — the {194, 213} paste was STALE AT ITS OWN BASE, not moved by this round

The ITEM 12 section above and the `probes:` conjunct-1 entry both assert a FULL SET
`{194, 213}` for `a00-ea0222b3-4ed78e.md`, with no base and no way to re-run. Measured
now, base pinned on the command line. At the round base (git `HEAD` = `15bc46e00`):

    $ git show 15bc46e00:.agi/nodes/experiment/a00-ea0222b3-4ed78e.md \
        | grep -n 'THOUGHT:END\|THOUGHT:BEGIN\|CAVEAT on the node'
    261:<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. ...
    279:CAVEAT on the node itself [DH.560 a00-9f9aaacd CORRECTED IN PLACE. DH.541 retracted th...
    281:retraction as body text BELOW `<!-- THOUGHT:END -->`, so a regenerating scan or a
    300:<!-- THOUGHT:END -->

So the cited `{194, 213}` was already wrong at the base this round started from — the
stale-measurement class is not caused by DH.589's duplicate block at all. After ITEM 1
of THIS round (the 32-line duplicate `## ITEM 4` section removed from
`a00-ea0222b3-4ed78e.md` through `write.py 'replace body'`), on the working copy:

    $ grep -n 'THOUGHT:END' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    249:retraction as body text BELOW `<!-- THOUGHT:END -->`, so a regenerating scan or a
    268:<!-- THOUGHT:END -->
    $ grep -n 'THOUGHT:BEGIN' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    229:<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. ...
    $ grep -n 'CAVEAT on the node' .agi/nodes/experiment/a00-ea0222b3-4ed78e.md
    247:CAVEAT on the node itself [DH.560 a00-9f9aaacd CORRECTED IN PLACE. ...

CURRENT FULL SET is `{249, 268}` (marker :268), with `begin=229`, `caveat=247`. The ORDER
claim the probe was really making still holds and still passes: the retraction prose at
:249 is inside the THOUGHT span and after the corrected CAVEAT, `229 < 247 < 249 < 268`.
The `probes:` conjunct-1 `observed` field is rewritten to these measured numbers with the
same base and command, through `write.py 'set probes'` — not by hand. The lesson the
section above half-drew ("a grep whose answer is a LINE NUMBER is a measurement") is
completed here: a measurement also has to name the base it was taken at, or the next
region edit silently falsifies it.
CORRECTION to the PARENT REVIEW above: the "## ITEM 10 heading TWICE" residue I named DOES NOT EXIST -- `grep -c "^## ITEM 10" .agi/nodes/experiment/a00-9f9aaacd-303434.md` -> 1. My duplicate was an artifact of MY OWN two overlapping sed ranges printing the same line twice, not a defect in the kid's bytes. The near miss is mine and it is the same class this round exists to kill: two ranges that overlap render one line as two, and I read the concatenation as a finding. Retracted, with the command pasted. The only residue that stands is item 7 UNVERIFIED (write-log per-worktree, pruned), which is a findings-row item.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.641 a00-df914bba delta — THIS node carried no authored THOUGHT at all (every THOUGHT:BEGIN/END string in it is a prose paste of another node), so this is its first. What this version changes, all node text: (1) three of the four `probes:` records the round had at 15bc46e00 and at 573a4e62f were missing from the landed bytes — restored verbatim from that base, `git show 15bc46e00:.agi/nodes/experiment/a00-9f9aaacd-303434.md | sed -n "16,18p"`, no new numbers typed; (2) the ITEM 2 paragraph retracted its own stale "real closing marker at this tip is :213" at the head, so a reader meets the correction, not the false claim; (3) ITEM headings renumbered 1->11 and 2->12 so no number is doubled in this node, with the cross-references that named the old numbers fixed. The verdict stays proved — the engine bytes it judged never moved. No engine byte, no test byte.
<!-- THOUGHT:END -->
