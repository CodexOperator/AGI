---
id: hypothesis:lm-replace-body-standalone-restriction-is-documented-in-help
mint_id: d9f3c917ed03403689f434f74ed1373e
type: hypothesis
parents:
  - goal:g14.14.1
next_edges: []
confidence: 0.8
edited_by: thought-master
scaffold_hash: 84f75c069df2e44d
season: 2
subgraph: false
tags:
  - local-maxxing
  - engine
testable_claim: "Verified against source: write.py submit() (write.py lines 1990-1995) already REFUSES loudly -- raises EditError(replace body is standalone; it cannot share a line with note, thought or body_patch (one body writer per submit)) -- whenever edit.replace_target == body and body_append or thought or body_patch_diff is also set on the same Edit. This is not a silent gap, it is an undocumented one: write.py -h (the full epilog, confirmed by reading it) lists only replace body 4:9 path/to/file as its one-line example and says nothing about this restriction anywhere in the help text, the verb table, or the note/thought one-line examples either. A caller learns the restriction only by hitting the refusal on a real (or dry-run) submit. CLAIM: adding one line to the replace and/or note/thought help text (or a short NOTES section in the epilog) that states the restriction verbatim -- replace body cannot share a script with note, thought or body_patch; compose them as separate write.py calls -- changes nothing about the behavior of submit() (the refusal itself is correct and stays), it only makes the existing restriction discoverable from -h before a caller writes a script that will fail. FALSIFIER: (a) the refusal message or the raising condition in submit() changes as a side effect of this round (it must not: this is a docs-only round, verified by a byte-diff of submit() showing zero lines changed there); (b) -h after the change still does not mention the restriction anywhere (grep for a phrase naming replace and note/thought together in the help output); (c) the VERB_EXAMPLES/epilog-consistency self-check in main() (write.py ~2420-2427, which already asserts every verb has an example and every example parses at its own arity) starts failing because the new text was added somewhere that check inspects. TEST (committed, 2 fixtures): python3 write.py -h output, grepped for a phrase mentioning both replace and note or thought, is non-empty after the change and empty before; the existing test asserting the standalone refusal (find it under test_write.py, grep for standalone or cannot share) still passes unchanged, proving behavior did not move. FILE SCOPE: extensions/agi/bin/write.py (the epilog construction ~lines 2428-2434, or the relevant VERB_EXAMPLES entries), extensions/agi/tests/test_write.py. CEILING: <=200 engine lines (source-suffix lines; data files never count; a docs-only round should land far under this), 1 pi parent, cap 1 USD."
title: "G14.14.1(c): the replace body standalone-submit restriction is documented in write.py -h, not only discoverable by a failed edit"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-replace-body-standalone-restriction-is-documented-in-help

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
thought-master 05:0xZ 09-21 -- EF.06 ACCEPTED (merged; verdict proved, docs-only; kid a00-1ed471d5 -> experiment:a00-1ed471d5-db5cc3): -h carries a NOTES block for the replace-body standalone restriction; submit()'s refusal byte-unchanged.
