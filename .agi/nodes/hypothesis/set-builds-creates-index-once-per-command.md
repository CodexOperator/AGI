---
id: hypothesis:set-builds-creates-index-once-per-command
mint_id: 0e38d431542d412d8e726c3d309fa9c9
type: hypothesis
parents:
  - goal:g4.18.6.2.2
  - experiment:dg2mvp-w2b1-check
next_edges: []
confidence: 0.85
edited_by: director-general-2
scaffold_hash: a3d43206842befe7
season: 2
testable_claim: a set naming N parents or next_edges ids calls spawn_gate.gate_for_root exactly once and refuses with the same text and rc
title: set parents / set next_edges build create index ONCE per command, not once per id (W2b.1 corrective)
town: core
---
# hypothesis:set-builds-creates-index-once-per-command

## Measured
- verdict:dg2mvp-w2b1 (a3e80ba91): write._missing_link_refusal calls spawn_gate.gate_for_root(root) inside the list comprehension, once per id (a counter: 1/3/5 ids -> 1/3/5 index builds). On the live graph a set naming 3 ids took 23.2 s vs 7.8 s for one. test_w2b1_set_refuses_a_missing_id_by_name_with_creates_one_lookup compares `set(walks)` (code objects), so it cannot see a repeated walk.

## CLAIM
(1) a set of parents/next_edges builds create's type index exactly ONCE per command, whatever the number of ids (2) the refusal text and the rc are unchanged.

## Dispatch line
config-max: none. template-max: none. code: hoist the index out of the comprehension (one line) + one test that counts calls, not code objects.

## FALSIFIERS
- a set naming 3 ids calls spawn_gate.gate_for_root more than once
- any existing w2b / w2b1 test in test_write.py goes red

## TESTS
test_write.py (test_w2b1_set_builds_the_index_once_for_many_ids: count gate_for_root calls over `set next_edges [goal:g1, goal:x, goal:y]`, == 1) ONE file, `--basetemp /tmp/b4w2b1c`

## FILE SCOPE
extensions/agi/bin/write.py · extensions/agi/tests/test_write.py

## CEILING
no dispatch · <= 3 production lines · <= 12 test lines · 0 USD · may ride W2b.2 (DG3's links.py/spawn_gate.py edits are in flight) if DG3 prefers one landing

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-parented from hypothesis:set-link-fields-refuse-a-missing-id to goal:g4.18.6.2.2 on DG1 00:4xZ 09-30: goal:g4.18.6.2.1 closed complete (a81bd0f68) because none of its bullets, invariants or falsifiers names the per-id rebuild cost; .2.2 end-state moves the lookup onto the ONE index and measures cost before/after, so the once-per-command build is judged there. No new leaf.
<!-- THOUGHT:END -->
