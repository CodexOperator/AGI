---
id: hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands
mint_id: 9cacec8426ba42c2a5a3ebec9f9ee10a
type: hypothesis
parents:
  - goal:g15.29.15
next_edges: []
assigned: director-engine (leaf goal:g15.29.15, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: 840ef5aedc03a901
season: 2
testable_claim: After the fix, applying the printed sub --dry-run diff to the on-disk node yields byte-for-byte the file the real sub then writes (a body with a duplicate leading frontmatter block included), both built by ONE shared assembly helper, proved by a committed test red on the pre-fix bytes, with test_write_sub.py, test_write.py and test_node_writer.py green.
title: "The sub dry-run preview is the bytes update_node lands (goal:g15.29.15; assigned: director-engine)"
town: core
---
# hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands

# hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands

**Assigned: director-engine** (leaf goal:g15.29.15; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
write.py:2674 preview applies set_fm before absorb (:2678), never runs _carry_thought, never adds ring_decision (submit adds it at :2017); update_node is carry (node_writer.py:1034) -> absorb (:1045) -> set_fm (:1057); the '-' side is a synthetic serialize (write.py:3105-3107); test_write_sub.py:53-67 checks substrings only
```

## CLAIM
After the fix, applying the printed sub --dry-run diff to the on-disk node yields byte-for-byte the file the real sub then writes (a body with a duplicate leading frontmatter block included), both built by ONE shared assembly helper, proved by a committed test red on the pre-fix bytes, with test_write_sub.py, test_write.py and test_node_writer.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_write_sub.py test_write.py test_node_writer.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
write.py · node_writer.py (one shared helper) · a test file

HAZARD: update_node is THE node writer: its output must stay byte-identical

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
