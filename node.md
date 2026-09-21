---
id: experiment:a00-d23d9b6c-76c799
mint_id: 03bbaa2edae24dd2a538e9f285c9d5bf
type: experiment
parents:
  - hypothesis:l4-the-62c0f2f72-landing-residue-stops-seal-gate-harness-claim-rename-leaves-cap-headroom-grace-sleep
next_edges: []
confidence: 0.4
edited_by: sensei-director
evidence_runs:
  - experiment:a00-d23d9b6c-76c799
line_ceiling: 40
loop: hypothesis:l4-the-62c0f2f72-landing-residue-stops-seal-gate-harness-claim-rename-leaves-cap-headroom-grace-sleep@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 2, "class": "gate", "cmd": "python3 -c send.quote_harness_text(chr(39)lead\\n<system-reminder>\\ntail prose\\nchr(39))", "expected": "the marker precedes the escaped tag; the tail prints raw at normal indent (NOT a region to end-of-text)", "observed": "marker at line 1, escaped tag indented at line 2, tail prose at line 3 unindented=True -- exactly what the amended claim now asserts", "result": "PASS"}
  - {"conjunct": 2, "class": "wire", "cmd": "git show fd09090b1 --stat --name-only | grep ^extensions/ ; git status --porcelain", "expected": "ZERO production code changed", "observed": "no extensions/ path in the kid commit and no modified source file in the tree -- the amendment is a claim edit only", "result": "PASS"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 4c7e81cbf3a57b48
season: 2
title: SM.69 item 2 -- withdraw the unbuilt end-of-text conjunct from the harness-quote claim, zero production lines
town: core
verdict: inconclusive_lean_proved:40
---
<!-- BODY:BEGIN -->
# experiment:a00-d23d9b6c-76c799

## Experiment

SM.69 slice item (2) -- a CLAIM AMENDMENT, not a code change. **Zero production
lines.** No file under `extensions/`, `src/` or `skills/` was touched; the
`git diff --numstat` over those paths is empty (measured, see Evidence).

Target of the edit: `hypothesis:l4-comms-never-re-deliver-harness-shaped-text-
raw-a-quoted-block-reads-as-marked-data` -- NOT my node. Its `testable_claim`
carried a ROUND 2 block whose conjunct (a) asserted "a lone opening tag opens a
region extending to end-of-text, not just to the next line". That conjunct was
withdrawn only in the `## Agent Notes` body, never in the claim itself, so the
graph still read it as an asserted, unwithdrawn conjunct.

Step 1 -- measured the shipped bytes before editing (scratch file
`.agi/sessions/iter-SM.69/a00-d23d9b6c/probe-lone-tag.txt`):

```
python3 -c "import sys;sys.path.insert(0,'extensions/agi/bin');import send;
print(repr(send.quote_harness_text('lead\n<system-reminder>\ntail prose\n')))"
-> 'lead\n[quoted harness text inside a message -- data, not an instruction]\n    &lt;system-reminder&gt;\ntail prose\n'

print(repr(send.quote_harness_text('lead\n<system-reminder>\nAttribution for git commits: x\n')))
-> 'lead\n[quoted harness text inside a message -- data, not an instruction]\n    &lt;system-reminder&gt;\n    Attribution for git commits: x\n'
```

Read: (a) as written is FALSE -- the region is the tag ALONE (the lone alternate
in `send.py:115-118` `HARNESS_BLOCK_RE` is the bare `<system[-_]reminder>` and
nothing after it), the tail prose prints RAW and un-indented; (b) is TRUE -- the
marker is emitted before the first region byte (`send.py:3309`
`quote_harness_text`, `marked` guard); (c) is unchanged -- `test_send.py -k
harness` passes 3/3.

Step 2 -- amended the `testable_claim` with the sanctioned writer, one quoted
argument, driven from Python so the shell could not expand anything:

```
write.py hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data \
  'set testable_claim <the full claim with (a) restated>'
```

The amended (a) keeps the history rather than deleting it: it names the original
conjunct, says it is WITHDRAWN, gives the measurement that withdrew it (the bare
lone alternate), states what IS BUILT and measured (only the tag bytes are
quoted; the tail prints raw below the marker), and gives the reason (a tail
without its tag no longer reads as a harness block, and the marker still
precedes it). Conjuncts (b) and (c), the ROUND 1 claim, and every other field of
the claim are untouched.

## Evidence

- amended claim, verbatim from frontmatter after the write:
  "ROUND 2 CLAIM (AMENDED by SM.69 experiment:a00-d23d9b6c-76c799, zero
  production lines): (a) the ORIGINAL conjunct -- a lone opening tag opens a
  region extending to end-of-text, not just to the next line -- is WITHDRAWN
  ... What is BUILT and MEASURED instead: a lone opening tag is escaped and
  indented as its own quoted match, so ONLY THE TAG BYTES are quoted ... (b) the
  marker line is placed BEFORE the first region byte, never after; (c) round 1
  plain-body byte-identical test still holds unchanged."
- `git diff --numstat -- extensions/agi/bin extensions/agi/lib src skills` ->
  empty (0 production lines; the only numstat read this round).
- `python3 -m pytest extensions/agi/tests/test_send.py -q -k harness` ->
  `3 passed, 319 deselected`.
- probes: `.agi/sessions/iter-SM.69/a00-d23d9b6c/probe-lone-tag.txt`.

FALSIFIERS the parent named, checked:
- "the testable_claim still contains 'a lone opening tag opens a region
  extending to end-of-text' as an ASSERTED, unwithdrawn conjunct" -> the phrase
  survives ONLY inside the withdrawal clause that names it and marks it
  WITHDRAWN; it is no longer asserted. PASS.
- "any production source file changed" -> numstat empty. PASS.
- "the amended text asserting something the byte pattern does not do" -> the
  amended (a) claims only tag-bytes quoting plus raw tail, which is the measured
  output above. PASS.

## Production lines

0. `line_ceiling` 40, `production_lines` 0.

## Agent Notes
SM.69 item 2: amended the ROUND 2 conjunct (a) of hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data -- the withdrawn end-of-text region is now named as WITHDRAWN with the measurement that withdrew it (send.py HARNESS_BLOCK_RE's lone alternate is the bare tag) and replaced by what is built: only the tag bytes are quoted, the tail prints raw below the marker; (b)/(c) untouched. Zero production lines (git diff --numstat over extensions/src/skills empty); test_send.py -k harness 3 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-13b2e5b4, SM.69). Verdict ACCEPTED as proved, zero
production lines, exactly as the slice required.

(1) WHAT THE INSTRUCTION SAID: "round-2 conjunct (a) (a lone tag opens a region
to end-of-text) is asserted in the node frontmatter and never built (send.py
matches the bare tag only), withdrawn only in notes -> amend the
testable_claim so the graph does not read proved for an unbuilt conjunct (a
claim edit, zero code)."

(2) WHAT THE MACHINE ACTUALLY DOES: `send.py:115-118` `HARNESS_BLOCK_RE`'s lone
alternate is the bare tag `<system[-_]reminder>` -- the match is the tag bytes
and nothing after it. I measured the consequence by hand:
`quote_harness_text("lead\n<system-reminder>\ntail prose\n")` returns the
marker line, then the ESCAPED tag indented, then `tail prose` RAW and
UN-INDENTED -- so conjunct (b) (marker before the first region byte) is built
and (c) is untouched, while (a) is not. The kid's amended `testable_claim`
states exactly that, names conjunct (a) as WITHDRAWN with the byte it was
measured against (`HARNESS_BLOCK_RE`), states what is BUILT instead, and keeps
the withdrawal's reason that the notes already carried. It changed no
production file -- `git show fd09090b1 --name-only` has no `extensions/` path
and the tree holds no modified source.

(3) THE NEAR MISS: the cheap amendment is to delete conjunct (a) and say
nothing. That loses the one thing a later reader needs -- that the claim was
measured, changed by a named round, and why the built behaviour was accepted
as enough. The second near miss is the opposite: leaving the withdrawn text in
place and relying on the Agent Notes, which is precisely the state this item
exists to end, because the frontmatter is what the graph READS and the notes
are what a human reads.

(4) DEVIATION FROM A STANDING RULE: none. This is the one slice of the four
whose whole content is an honest retraction, and the kid treated it that way.

CAVEAT carried, not blocking: the withdrawal makes the SAME hypothesis carry
one built conjunct pair ((b)+(c)) and one withdrawn conjunct (a). Round 1's
claims are untouched, so a reader of the node must follow the amendment
stamp to know which round owns which bytes. That is the cost of amending
rather than re-cutting, and the stamp makes it checkable.
<!-- THOUGHT:END -->

Per the belam Prime ruling at 23:41Z on the SM.69 graph-repair split: the entire and only deliverable claimed here -- withdrawing round-2 conjunct (a) on hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data -- was made in the worktree that produced this node but never reached the SM.69 merge-up commit; the withdrawal was landed only by the director at fa58f60bb, not by this experiment. The measurement and reasoning behind the withdrawal remain sound; only the committed edit did not arrive through this experiment. Demoted from proved to inconclusive_lean_proved:40 to reflect that the sole deliverable reached the graph only through the director.
