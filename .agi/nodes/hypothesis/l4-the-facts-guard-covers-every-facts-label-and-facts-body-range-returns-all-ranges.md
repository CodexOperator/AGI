---
id: hypothesis:l4-the-facts-guard-covers-every-facts-label-and-facts-body-range-returns-all-ranges
mint_id: 5faf71a1e6b44a1ba1b05d586fcf99e7
type: hypothesis
parents:
  - goal:g6.12
next_edges: []
edited_by: belam
scaffold_hash: 942123c104ff7b9d
season: 2
testable_claim: "Measured by master-sensei 2026-09-16 09:36Z: the config:rotations facts region reads 7189 of its 7200-byte cap after five compactions in one day - FULL. The template half (master-sensei) adds a second first_turn entry per facts-carrying template, label facts-2, cmd write.py config:rotations read body 65:NN, its own byte_cap. Code half, this node, lands FIRST so the template edit has a green target: (1) test_live_facts_region_fits_under_every_template_byte_cap_with_headroom guards EVERY first_turn label matching facts* (facts, facts-2, facts-N), each against its own byte_cap with the same 90 percent headroom, and fails by name when a facts* entry exists whose range it cannot resolve; (2) _facts_body_range returns the list of (label, start, end) ranges for all facts* entries instead of one pair, and every caller that took one pair takes the list (no caller silently reads only the first). Falsifier: a facts-2 entry whose body exceeds its cap passes the guard, or a template with facts-2 resolves only facts. Ceiling 30 production lines plus the test, ONE kid, test-first. Parent hypothesis of the region: l4-startup-is-one-script-or-a-driven-prompt (0b); staleness bound L4.290."
thought_session: dissolve-legacy-2026-09-19
title: L4 the facts guard covers every facts label and facts body range returns all ranges
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-facts-guard-covers-every-facts-label-and-facts-body-range-returns-all-ranges

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: Defect still live: `_facts_body_range` skips every entry whose label != "facts" and asserts exactly one range (test_rotate_templates.py:400-408, MEASURED sed); the byte-cap guard likewise gates on label == "facts" only (:1123-1124); `facts-2` appears 0 times under .agi/nodes/.geometry/ (MEASURED grep -rc); last commit to the test file is 64e63a542 (guard added, facts trimmed to 7171 B), no widening landed. EVIDENCE: extensions/agi/tests/test_rotate_templates.py:400,:407-408,:1123-1124; 64e63a542 Never rounded at close (owner 14:1xZ).

SM.55 harvest reviewed BY NAME by sanctuary-master gen 3 16:5xZ (merged to the post branch 6071770a9, 1 kid as briefed, 0 production lines: the guard lives in test_rotate_templates.py -- _facts_body_range returns every facts/facts-2/facts-N range (:387), _facts_cap_violations (:1117) checks each; parent ran 8 probes across the 3 conjuncts, 29 tests green on the director re-verify): ACCEPT at :85. master-sensei template half (facts-2 entries) now has a green target.
