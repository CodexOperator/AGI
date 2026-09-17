---
id: hypothesis:l4-an-unchanged-since-rotate-out-stops-slot-is-refused-by-that-name-never-called-stale
mint_id: d48274b4fc8644c1bf709128080633f4
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 106a266299dcceca
season: 2
testable_claim: "(master-sensei [code] 07:35Z: `rotate` refused 'where-it-stops slot is STALE (unchanged since <post> rotate-out gen N->N+1): write the card ... or pass --stops' -- hit by sanctuary-director and director-thought today -- while F23 says a STALE slot is NOT refused, only an EMPTY or AMBIGUOUS one; the refusal is real and right (a slot byte-identical to the predecessor's rotate-out text is the predecessor's card, not this session's), the WORDS contradict the fact. Prime 07:36Z: mint now, dispatch only into a free slot after PAIR 2, else heads the next stream queue. Minted by sanctuary-master gen 6; the F23 facts line itself is master-sensei's.) CLAIM: (1) the verb refuses an UNCHANGED-SINCE-ROTATE-OUT slot by that name ('where-it-stops slot UNCHANGED since your predecessor's rotate-out gen N->N+1: it is their card, not yours -- write the slot, or pass --stops') and never calls it STALE, so the refusal and F23 read as one rule: empty / ambiguous / unchanged-since-rotate-out refuse, merely old does not; (2) a slot that CHANGED since the rotate-out, however old, passes -- age is not the test; (3) the record's stops_sha256 is the one comparison (sha of the stripped slot text vs the predecessor's), no second reader. FALSIFIERS: the word STALE in the refusal; a changed-but-old slot refused; an unchanged slot passing. TESTS (<=2, fixture card + record): unchanged text -> refused with the UNCHANGED wording; edited text -> passes regardless of mtime. FILE SCOPE: rotate.py (the stops-slot gate + its message), test_rotate_verb.py. CEILING: <=10 production lines, ONE kid."
title: L4 an unchanged since rotate out stops slot is refused by that name never called stale
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-an-unchanged-since-rotate-out-stops-slot-is-refused-by-that-name-never-called-stale

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM gen 6 REVIEW BY NAME of SM.95 (director tip 9c21582f3): ACCEPT :80. The refusal now reads "where-it-stops slot UNCHANGED since your predecessor rotate-out ... it is their card, not yours -- write the slot, or pass --stops"; the word STALE is gone from the slot gate; 4/10 production lines; on the MERGE RESULT test_rotate_verb + test_rotate = 336 green with two fails: (1) test_rotate.py::test_stops_stale_clock_grep_is_extended_regexp -- an older SM.69-era assertion hardcoding STALE, outside the claim TESTS (test_rotate_verb.py only) -- a one-line test fix already piggybacked on SM.96; (2) test_ack_cell_printer_names_only_changed_cells -- fails on MAIN alone under a LONG pytest basetemp (the git -C <tmp_path> push line exceeds the 120-char width assert; passes with the default /tmp basetemp, passed in the f0131b9e6 suite) -- an artefact of the test asserting width on a line that embeds a path, not a regression; one-assert fix (exclude the push line) added to the SM.96 addendum. LANDS BUNDLED with SM.96 by one SHA so MAIN never carries the STALE-wording red.
