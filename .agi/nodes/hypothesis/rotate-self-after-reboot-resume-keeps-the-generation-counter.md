---
id: hypothesis:rotate-self-after-reboot-resume-keeps-the-generation-counter
mint_id: bdeabcb472dc42209beb91979db95bde
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: ecd9ee75d89708d3
season: 2
testable_claim: after a reboot resume, rotate-self writes generation N+1 into the row, the record gen_after and key_history to
title: rotate-self after a reboot resume keeps the generation counter (N -> N+1, never 1)
town: core
---
# hypothesis:rotate-self-after-reboot-resume-keeps-the-generation-counter

## RED (belam gen 24, 15:2xZ 10-01)
```
14:42Z hard reboot ─▶ heal RESUMED SEAT path ─▶ 15:07Z rotate-self belam gen 23 ─▶ record belam.20261001T150403Z: gen_before 23, gen_after 1
                                                                          ─▶ row generation 1 · key_history {from 23, to 1} signed by the gen-23 key
owner 07:3xZ 10-01 (verbatim on goal:g7.16.1.11): "make sure the session count is maintained so each new belam session iterates counters even if you do have to start it from I"
```
| fact | value |
|---|---|
| suspected cause | the post-reboot resume path restarts the numeral chain at I and derives gen from the numeral, not from row generation + 1 |
| hand fix | 3508b58d3: row generation -> 24, own row only; key_history entry 23->1 KEPT (its rotated_by_sig signs `belam\nretire\n23\n1\n<pub>`; send.py:3654 verifies by fp/pub only) |
| side effect | rotate.py refused to report success: predecessor window None after the reboot |

## FALSIFIER
A rotate-self of a post whose row reads generation N, run after a reboot-resume with no predecessor window, writes generation N+1 into the row, the record's gen_after and the key_history `to`. Disproved if any of the three reads 1 (or any value other than N+1).
