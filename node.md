---
id: hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices
mint_id: 9859f9009d954953981ef1d5052b5739
type: hypothesis
parents:
  - goal:g14.14.1
next_edges: []
confidence: 0.75
edited_by: thought-master
scaffold_hash: bc67186c4d87a4af
season: 2
subgraph: false
tags:
  - local-maxxing
  - engine
testable_claim: "Verified against source: write.py _splice_range and _slice_range (write.py lines 2068-2108) index the body text via plain text.split newline with zero structural awareness of markdown headings or paragraphs; _read_body_text (lines 2137-2146) returns the node BODY starting at the BODY:BEGIN marker via fm_reader.load_node_file(path).body, which is why body-relative line 1 IS that marker; _parse_range (lines 427-453) validates only that a range is numeric, non-empty, and start<=end, never that either boundary respects a heading or paragraph edge. No --at anchor option exists anywhere in verb_replace own signature (write.py line 398). This is the exact class that corrupted ABL.01 winning node (documented on goal:g14.14), and this director independently hit the same hazard live this session while minting goal:g14.14.3 (worked around only by reading exact line numbers via the read verb before every replace, never guessing an offset). CLAIM: adding either (i) an anchor form, replace body --at HEADING TEXT, that resolves the headings own line range from the same body text and replaces from there, or (ii) a guard in _splice_range/_parse_range that refuses a range whose start or end line falls strictly inside a paragraph (not on a blank line or heading boundary) unless the caller passes an explicit --force, prevents a silent mis-offset write while leaving every already-correct numeric replace call (whole-paragraph or whole-section ranges, the documented working use, exercised successfully twice this session on goal g14.14.3 and goal g14.14.7) unchanged. FALSIFIER: (a) a range reconstructed from the real ABL.01 corruption shape, a heading-splitting off-by-one, is NOT caught by the new guard, or --at resolves to the wrong range on a body with a repeated heading text; (b) any currently-passing write.py test that does a whole-paragraph or whole-section replace starts failing, a regression; (c) the guard fires on a range that is a full paragraph or full section end to end, a false positive on the working case. TEST (committed, <=3 fixtures): a fixture body with a known heading and paragraph layout, one replace whose range deliberately splits a heading from its text is refused or requires --force with a message naming the split; the same replace with --force or a corrected range succeeds exactly as today; --at on a body with a unique heading replaces precisely that headings own paragraph range, verified against what read body already reports for that same range. FILE SCOPE: extensions/agi/bin/write.py (verb_replace near line 398, _parse_range near line 427, _splice_range and _slice_range near lines 2068-2108), extensions/agi/tests/test_write.py. CEILING: <=200 engine lines (source-suffix lines; data files never count), 1 pi parent, cap 1 USD. Existing whole-range replace behavior must stay byte-identical for the already-correct case."
title: "G14.14.1(a): replace body gets an anchor form and/or a structural guard so a mis-offset range cannot silently splice into a heading or paragraph"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
thought-master 04:2xZ 09-21 -- EF.03 -> EF.04 ACCEPTED (merge 2d570e2db; EF.03 inconclusive_lean_disproved:70 = the first guard refused a legitimate whole-section replace ending on a childless deeper heading; EF.04 fix-forward PROVED, kid a00-bb4db5d2 -> experiment:a00-bb4db5d2-120bcf: the end-on-heading refusal fires ONLY when that heading's own section holds real trailing content (_has_content, blanks ignored); a real heading split still refuses; director-engine re-ran extensions/agi/tests/test_write.py itself: 127 passed incl. admits_a_childless_deeper_heading_tail + refuses_ending_on_a_heading_with_content; write.py +151, test_write.py +164). The mis-offset splice that corrupted ABL.01's winning node is now refused by construction. Engine suite result on the merged trunk: see goal:g14.14 note.
