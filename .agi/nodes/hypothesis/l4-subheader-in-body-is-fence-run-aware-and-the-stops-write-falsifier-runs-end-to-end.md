---
id: hypothesis:l4-subheader-in-body-is-fence-run-aware-and-the-stops-write-falsifier-runs-end-to-end
mint_id: 625ccd2259dc4bf1bf78953ae748bf01
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 9bd3b8eb3cabdb3a
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (Prime XVI dm 17:07Z (mur-SL2.23 digest), line numbers measured by the Prime on main tip 36fa24d1d — `git show 36fa24d1d:<file> | sed -n` before trusting one; cite at seat tip d51c9a917, re-measure on your base; line (c), SL7.62 residue). MEASURED: `_subheader_in_body(body, token)` at rotate.py:5067-5077 scans for a `## ` / `### ` heading by line with no fence-run tracking, so a heading-shaped line inside a ``` fenced block (the stop block quotes headings verbatim) is found as a section head — the same defect SL7.48 fixed in the stops end-of-slot scan and SL7.62 fixed in `_split_card_sections`; each fix carried its own fence walker instead of one shared helper; the SL7.62 test `test_split_card_sections_fenced_hash_heading_not_a_section` (test_rotate.py:3065) pins the splitter but the stops-WRITE path (rotate-self `--stops` writing the slot, then a re-read) has no end-to-end test that a fenced heading in the written stops text does not corrupt the next split. CLAIM: (a) ONE fence-run walker (a generator yielding (line, in_fence) over a body, fence = a line starting with ``` or ~~~ toggling state, run-length aware for ```` etc.) used by `_subheader_in_body`, `_split_card_sections` and the stops scan — the two existing walkers are replaced by calls to it, behaviour byte-identical on their existing tests; (b) `_subheader_in_body` ignores headings inside a fence; (c) an end-to-end test writes a stops text containing a fenced `## fake` line through the real stops-slot writer, re-reads the card and asserts `_split_card_sections` and `_subheader_in_body` both see the real sections only. FALSIFIERS: a fenced `## X` still resolves as a subheader; the three readers disagree on any fixture; the e2e test passes with the fence walker removed. TESTS: test_rotate.py — fenced subheader ignored, shared-walker parity on the SL7.48/SL7.62 fixtures, stops-write e2e. FILE SCOPE: extensions/agi/bin/rotate.py — `_subheader_in_body`, `_split_card_sections`, the stops scan's fence logic (refactor to the shared walker only), one new walker; extensions/agi/tests/test_rotate.py. EXCLUDED: the card's content, the merge of WORK/foreign rows (`_merge_region`, SL7.52/66), rotate-self's other steps. CEILING: one walker, three call sites, three tests."
thought_session: sensei-director-genXIV-L14
title: _subheader_in_body is fence-run-aware — the third fence-unaware card reader after the stops scan (SL7.48) and _split_card_sections (SL7.62) — and the stops-write falsifier is pinned end-to-end through rotate-self's stops slot
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-subheader-in-body-is-fence-run-aware-and-the-stops-write-falsifier-runs-end-to-end

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
