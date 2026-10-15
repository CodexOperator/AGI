---
id: experiment:a00-020ce45f-48e2be
mint_id: 946d8f4bb7854df3ba1f5bff8c212fae
type: experiment
parents:
  - hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line
next_edges: []
confidence: 0.85
edited_by: a00-8e88a179
evidence_runs:
  - experiment:a00-020ce45f-48e2be
loop: hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f1810588b9987adc
season: 2
title: "DH.679: the withdrawn merge-in control removed from all three places it survives, incl. the machine-read probes row"
town: core
verdict: proved
---
# experiment:a00-020ce45f-48e2be

DH.679 CORRECTIVE (kid a00-020ce45f), all four items NODE-TEXT fixes landed through the
logged writer `extensions/agi/bin/write.py` only. 0 production lines, 0 test lines.

| # | item | disposition | where |
|---|------|-------------|-------|
| 1 | withdrawn "8 of those 9" in the hypothesis Agent Notes | FIXED in the bytes | hypothesis body 44 rewritten (the DH.630 note now says the control was the WRONG file, NINE not eight, all nine inherited) |
| 2 | the TARGET node's Agent Notes carries the withdrawn pair | FIXED in the bytes | experiment:a00-42ca5cbe-9e17ff body 318 rewritten; the pair is named WITHDRAWN in place, not deleted silently |
| 3 | the withdrawn control survives in a MACHINE-READ field | FIXED in the bytes | `set probes` replaces conjunct-2 (see below) |
| 4 | TEMPLATE-MAX: merge-order sentence in TWO bodies | FIXED in the bytes | kept ONCE in the hypothesis Agent Notes; experiment body 270-285 now CITES it and does not restate it |

## Item 3 — write.py CAN set `probes`, so no separate settling command was owed

The order said: "if write.py cannot set that field, SAY SO on your node and run the one
command that settles it". It can: `verb_set` -> `_coerce` parses a JSON array into one
nested value (`write.py:247`, `_coerce` at `write.py:622-631`, the `hypothesis:l3-write-set-nested-json`
leg). The field was therefore REPLACED, not annotated:

```
$ python3 -c "import json,subprocess,sys; ..."   # read fm['probes'], swap conjunct 2, re-emit
updated: experiment:a00-42ca5cbe-9e17ff
```

Conjunct 2 now records the CORRECT control (this round's base `fc4fa8132`, not
`1ea22df7d`'s own file), states the old `8F/13P` row as WITHDRAWN in the machine-read
field, and CITES the sibling node that holds the pasted counts rather than retyping a
number I did not measure myself:

```
$ grep -n '"conjunct": 2' .agi/nodes/experiment/a00-42ca5cbe-9e17ff.md
  - {"conjunct": 2, "class": "wire", "cmd": "DH.679 CORRECTION -- the control is THIS ROUND'S
     BASE FILE, not 1ea22df7d's own. ... observed": "WITHDRAWN, do not harvest: the old
     8F/13P control (taken from 1ea22df7d's own file) is a wrong-file artefact and the old
     'the test file cannot merge up alone' causality is false. ...", "result": "PASS"}
```

Conjuncts 1 and 3 are byte-unchanged. The `class` stays `wire` and the six required keys
(`_PROBE_KEYS`, cli.py:1118) are all present, so the row still counts for the gate.

## UNVERIFIED, and said so rather than run

I did NOT re-run the wire probe: the order's rule 0 bans the row
`test_capture_rotate_self_step_keeps_the_owed_slot` by NAME, and a00-ffaf1904's parent review
already recorded that a re-run of it is the shape that TERM'd the prime. So the corrected
control is cited, not reproduced. The measured counts stay on
`experiment:a00-ffaf1904-015138` (its item table rows (a)/(b)/(c) and its GATE probe), which is
in FILE SCOPE and already carries them. Two breadths exist and neither is a defect in my
change: that node's own parent review records `9F/14P/2D` for the two-param deselect and
`7F/14P/4D` for the whole-row deselect, and the breadth was uniform across all three arms.

## The near miss I avoided

Fixing item 2 by DELETING the sentence would have been cleaner and wrong: the DH.630
measurement it sits next to is still true, and a node that quietly drops a round's record
reads exactly like a node that never ran it. Each withdrawn clause is marked in place, with
the reason, and the surviving claim is restated on the one node that owns it.

## Ceiling

```
$ git diff --numstat -- extensions/agi/bin extensions/agi/hooks extensions/agi/src
(empty)
```

0 production lines against a 20 ceiling; 0 test lines against 40. No code changed, so no
suite run was owed. No `git` beyond that one read-only measurement; no commit, no push.

## OUTSIDE (named, not touched)

- `extensions/agi/tests/test_rotation_alert_capture.py:570` -- the row a whole-suite run keeps
  executing; the prime-TERM shape is named only in an order's example, never in the file. A
  permanent marker belongs there, outside this round's file scope.
- `extensions/agi/bin/cli.py:1118` `_PROBE_KEYS` -- `write.py` can now replace a `probes` row
  wholesale, but nothing warns that a `probes` row may quote a measurement that a later round
  WITHDRAWS. A `withdrawn` key, or a gate that reads the prose THOUGHT for a withdrawal, is the
  structural fix for the DH.599-item-4 / DH.679-item-3 class.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.679 (a00-8e88a179) -- judged on the BYTES of the three node files, never on this node table, which is a four-row "FIXED in the bytes" grid and exactly the shape that reads green while a number survives. (1) WHAT THE INSTRUCTION SAID, quoted: "For EACH item: fix it in the bytes, OR ... run the one command that settles it and PASTE its output on your node (never type a number)", and item 3 verbatim: "The withdrawn control survives in a MACHINE-READ field, not just prose ... extensions/agi/bin/cli.py:2026 keys on `probes`, so the superseded number is what a harvest reads". (2) WHAT THE MACHINE ACTUALLY DOES: three probes I BUILT AND RAN from extensions/agi/bin. WIRE (item 3): frontmatter.read_frontmatter on a00-42ca5cbe-9e17ff returns 3 probes rows and cli._probe_defect(p) is the empty string for all three, so the replaced row still satisfies _PROBE_KEYS (cli.py:1118) and the gate still counts it; "8 failed, 13 passed" is absent from the JSON a harvest keys on, and "8F/13P" survives only inside the words "WITHDRAWN, do not harvest". GATE (items 1+2): the string "8 of those 9" / "8 of 9 pre-existing" occurs EXACTLY TWICE across the hypothesis and the target node, and in both cases inside a sentence that opens WITHDRAWN and names the wrong control file; my first pass reported both as LIVE, because the pattern match ignored the 160 characters before the hit -- a probe artefact I re-ran with context rather than accepted. AUTH (item 4): the merge-ORDER sentence is asserted on the hypothesis (THOUGHT line 57 and Agent Notes line 65, the latter marked "stated HERE ONLY") and appears as a STANDALONE claim nowhere in the target node body; the single body hit is the citation inside the probes row, "Merge ORDER (...) is stated ONCE on the parent hypothesis ..., Agent Notes; this node cites it". The citation resolves: experiment:a00-ffaf1904-015138:48-50 carries rows (a) 23 passed / 2 deselected, (b) 9 failed / 14 passed / 2 deselected, (c) CONTROL 9 failed / 14 passed / 2 deselected -- the corrected control the probes row points a reader at instead of retyping. This round touched node markdown only: 0 production lines against a 15 cap, 0 test lines against 40. (3) THE NEAR MISS: a corrective that DELETES the withdrawn sentence instead of marking it -- three tidy nodes with no trace that a number was ever wrong, and the graph can no longer tell a node that was corrected from a node that was never wrong; the DH.630 measurement standing next to it loses its history. The kid chose in-place withdrawal and named the choice itself. The second near miss is fixing only the PROSE (hypothesis + target Agent Notes, probes row untouched) -- precisely the shape the order's item 3 was written for; the kid went one hop further than the two prose items asked. The third near miss is citing a00-ffaf1904 for the corrected digits without pasting them, which forces a reader holding only the machine-read field to follow the link to verify; I accept it because the node names the rows (a)/(b)/(c) and the file, and a retyped number is the exact failure class this round exists to stop. (4) IF I DEVIATED FROM A STANDING RULE: two. (a) The orders tell the PARENT to "COMMIT every kid edit AND every node edit on the loop branch", and my tier rules forbid me to touch git at all; the property of THIS case that settles it is that all four items are node-text edits already made through the logged writer, so the bytes are staged for the lander and a hand commit would duplicate the commit the loop is about to make. (b) I did not re-run the wire probe myself: rule 0 bans that row by NAME, and the kid was right to cite rather than re-run; my review stands on the bytes and on the three probes above, none of which touch the banned row. VERDICT: ACCEPTED as proved -- all four items landed in the bytes, the machine-read field is clean and still gate-valid, 0 production lines, a real kid-authored title, parents resolving to the target hypothesis, evidence_runs naming the node itself. RESIDUE, named not ridden: the DH.630 parent review (lines 351, 354, 356) and the pasted run transcript at line 280 still carry "8F pre-round" and "8 failed, 13 passed" as HISTORY. That is correct -- a record of what was measured at the time is evidence, not a live claim -- but a reader grepping the number must read past them. The only structural fix is the one the kid already named: a withdrawn key on the probe dict at cli.py:1118, OUTSIDE this round's file scope, routed to the director's findings row.
<!-- THOUGHT:END -->

## Agent Notes
PUSH: a probes row that quotes a MEASUREMENT later withdrawn is the recurring defect (DH.599 item 4, DH.679 item 3). cli.py:1118 validates the six keys and nothing else, so a withdrawal must be carried by hand into the field. A withdrawn key on the probe dict, or a gate that reads the node prose for a withdrawal, kills the class.

## Agent Notes
DH.679: withdrawn merge-in control fixed in the bytes at all three places it survived - hypothesis Agent Notes, target node Agent Notes, and the machine-read probes conjunct-2 wire row (write.py CAN set probes); merge-ORDER sentence deduplicated to the hypothesis (TEMPLATE-MAX); 0 production lines; wire probe cited, not re-run (rule 0)
