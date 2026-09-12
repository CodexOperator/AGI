---
id: hypothesis:l4-the-stops-end-of-slot-scan-is-fence-run-aware-so-a-heading-inside-a-nested-fence-never-truncates-the-slot
mint_id: 5fa34acf1f424f878eed4c0b2de4effa
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: e95553b36cb5a84c
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (SL7.41 residue, mur digest wf_438874da-7a6 line (5), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: rotate.py:11113-11120 (_write_stops_section :11066, the ### sub-header branch) tracks in_fence by toggling on ANY line whose stripped prefix is three backticks, so a four-backtick outer fence opens, the first inner three-backtick line toggles it CLOSED, and a #-leading line inside the inner block (a shell comment, a heading quoted in a stops line) sets end=j: the slot is truncated there on the NEXT write and the tail is re-appended as body; _replace_fence_after (:5141, its two startswith checks at :5148/:5155) pairs on the first three-backtick prefix the same way, so a handoff --driven replacement of a fenced region under a longer outer fence pairs the wrong delimiters. CommonMark: a fence closes only on a fence of the SAME character whose run is at least as long as the opener's, with nothing else on the line. CLAIM: both scans record the opener's backtick run length and treat a line as a closing fence only when its run is >= the opener's; a #-leading line inside any nested fence never ends the slot; a stops text whose fenced block contains an inner three-backtick block round-trips byte-identical across two consecutive --stops writes. FALSIFIERS: two consecutive _write_stops_section calls with an inner-fenced stops text produce different files; a ### slot whose first fence is four backticks and contains an inner sh block loses lines after a # line; _replace_fence_after replaces the inner block instead of the outer. TESTS: test_rotate.py (where _replace_fence_after / _write_stops_section are tested today) — the nested-fence round trip; the #-inside-inner-fence case; one _replace_fence_after case with a four-backtick outer. FILE SCOPE: extensions/agi/bin/rotate.py — the :11113-11120 loop and _replace_fence_after only; extensions/agi/tests/test_rotate.py. EXCLUDED: _stops_replace_fenced_region, _render_stops_block, the section splitter, the card layout. CEILING: one fence-run helper used at two sites, three tests."
thought_session: sensei-director-genXIII-L13
title: "the stops end-of-slot scan and _replace_fence_after pair fences by backtick-run length, so a #-leading line inside an inner three-backtick block under a four-backtick fence never ends the slot"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-stops-end-of-slot-scan-is-fence-run-aware-so-a-heading-inside-a-nested-fence-never-truncates-the-slot

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
