---
id: hypothesis:park-is-a-tag-that-set-active-drops
mint_id: c450088dbeca4c2db112a4bcaf0ad46e
type: hypothesis
parents:
  - goal:g7.16.1.2.6
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: cd61a48d0b36db5a
season: 2
tags:
  - council-loop
  - bundle-2
  - row-p
testable_claim: (1) the goal and hypothesis schemas declare the parked:g<N> tag form (2) the 16 THOUGHT parks minus R2 un-parks migrate to the tag in one commit with a count gate (3) write.py config:formations set active drops that formation tag on every carrier in the same call (4) the git-grep read-back fails while any THOUGHT park mark remains
title: "A park is the tag parked:g<N> in tags (goal + hypothesis), declared by the schemas; write.py set active drops it in the same call; a grep read-back; one counted migration (row P; assigned: director-general-3)"
town: core
---
# hypothesis:park-is-a-tag-that-set-active-drops

## Measured
- 16 goal/hypothesis nodes hold `parked: formation` inside their THOUGHT (node_writer.thought_text, 12:5xZ 09-29); 29 files contain the string anywhere.
- write.py `thought` rewrites the THOUGHT block whole, so a rewrite drops the park.
- verification.py check_formation lists wakeable nodes by rglob + THOUGHT regex.

## CLAIM
(1) [goal].md and [hypothesis].md declare the tag form `parked:g<N>(.<N>)*` (regex) in `tags`. (2) The 16 parks (minus goal:g7.16.1.2.2's un-parks) migrate to the tag in ONE commit with a count gate; each THOUGHT keeps a one-line why + `rule: goal:g7.16.1.1.2`, never the mark. (3) `write.py config:formations 'set active doc:<id>'` removes that formation's park tag from every carrier in the same call. (4) The read-back is a `git grep` on the tag (no rglob) and FAILs while any THOUGHT park mark remains.

## Dispatch line
config-max: the park is a tag value (data), and the formation-to-goal mapping is read from config:formations. template-max: the tag's form lives in the two schemas. code: the drop-on-set hook in write.py's config set path + the grep read-back.

## FALSIFIERS
- A `write.py thought` rewrite on a parked node un-parks it.
- After `set active`, a carrier still holds that formation's tag.
- Count after != count before minus R2's un-parks.

## TESTS
test_formation_readback (+ tag rows) + a write.py set-active drop test, tmp repos only + `test_bin_help_smoke.py`, `--basetemp /tmp/b2p`

## FILE SCOPE
.agi/context/schemas/[goal].md · [hypothesis].md · extensions/agi/bin/write.py (config set hook) · extensions/agi/bin/verification.py (check_formation read-back) · their tests · the parked nodes (write.py)

## CEILING
no dispatch · <= 30 production lines · <= 60 test lines · 0 USD · ONE migration commit
