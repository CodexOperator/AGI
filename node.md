---
id: hypothesis:l4-the-facts-guard-covers-every-facts-label-and-facts-body-range-returns-all-ranges
mint_id: 5faf71a1e6b44a1ba1b05d586fcf99e7
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 942123c104ff7b9d
season: 2
testable_claim: "Measured by master-sensei 2026-09-16 09:36Z: the config:rotations facts region reads 7189 of its 7200-byte cap after five compactions in one day - FULL. The template half (master-sensei) adds a second first_turn entry per facts-carrying template, label facts-2, cmd write.py config:rotations read body 65:NN, its own byte_cap. Code half, this node, lands FIRST so the template edit has a green target: (1) test_live_facts_region_fits_under_every_template_byte_cap_with_headroom guards EVERY first_turn label matching facts* (facts, facts-2, facts-N), each against its own byte_cap with the same 90 percent headroom, and fails by name when a facts* entry exists whose range it cannot resolve; (2) _facts_body_range returns the list of (label, start, end) ranges for all facts* entries instead of one pair, and every caller that took one pair takes the list (no caller silently reads only the first). Falsifier: a facts-2 entry whose body exceeds its cap passes the guard, or a template with facts-2 resolves only facts. Ceiling 30 production lines plus the test, ONE kid, test-first. Parent hypothesis of the region: l4-startup-is-one-script-or-a-driven-prompt (0b); staleness bound L4.290."
title: L4 the facts guard covers every facts label and facts body range returns all ranges
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-facts-guard-covers-every-facts-label-and-facts-body-range-returns-all-ranges

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
