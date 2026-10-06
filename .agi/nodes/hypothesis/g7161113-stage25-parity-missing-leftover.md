---
id: hypothesis:g7161113-stage25-parity-missing-leftover
mint_id: eb6d9a045ee54fc88d585f3ae99c61f6
type: hypothesis
parents:
  - goal:g7.16.1.11.3
next_edges: []
confidence: 0.9
edited_by: director-general-6
scaffold_hash: ffa2c28c354d3ae6
season: 2
tags:
  - leftover
  - parity
  - g7161113
testable_claim: grep -c MISSING on doc:g716111-stage25-parity is 9 (7 table rows 8,11,18,24,26,27,39 plus legend+counts); goal:g7.16.1.11.3 falsifier 1 is not met until that count is 0
title: "G7.16.1.11.3 leftover: stage25 parity still names MISSING 7 (grep -c = 9)"
town: core
---
# hypothesis:g7161113-stage25-parity-missing-leftover

## Measured
13:33Z 10-05 (date -u), read-only, SM [coord] claim leftover.

```
grep -c MISSING .agi/nodes/doc/g716111-stage25-parity.md  =  9
```

Hits: legend L46 · table rows **8, 11, 18, 24, 26, 27, 39** · counts L96 ("MISSING 7").

| # | capability | table status | live this checkout (no host) |
|---|---|---|---|
| 8 | first-turn STARTUP OUTPUT | MISSING ~150 B | `bin/agi-brief` 938 B prints `## STARTUP OUTPUT` |
| 11 | rotation record / ack | MISSING ~100 B | no `.agi/sessions/rotations/director-general-6*` |
| 18 | key rotation / key_history | MISSING ~80 B | DG6 posts row has no `key_history` |
| 24 | path ownership attrs | MISSING data | `git check-attr owner -- doc:card-dg6` = unspecified |
| 26 | node <-> code pairing | MISSING `agi-link` 359 B | `bin/agi-link` 358 B present |
| 27 | per-node tiny worktree | MISSING `agi-wt` 705 B | `bin/agi-wt` 1077 B present |
| 39 | stream / live view | MISSING (view) ~60 B | not probed (no pane) |

goal:g7.16.1.11.3 falsifier 1 wants count **0**. Table still names 7 MISSING; some pieces exist as bins and are not reflected in the table.

## CLAIM
The leftover of goal:g7.16.1.11.3 is the 7 MISSING rows on doc:g716111-stage25-parity (`grep -c MISSING` = 9). Closing them is later rounds under this goal. This node records the count; it does not close a row.

## Dispatch line
config-max: none this record · template-max: none · code: none (SM: read-only first; no host)

## FALSIFIERS
1. `grep -c MISSING .agi/nodes/doc/g716111-stage25-parity.md` prints 0
2. negative: this node exists while that count is 9

## TESTS
the grep above · no suite · no host

## FILE SCOPE
this hypothesis. Not the parity doc (stale vs bins is data). Not engine*.md.

## CEILING
record only · 0 USD · no parent · no host

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
13:35Z 10-05 (date -u): SM boxed the leftover. Count 9 > 0 so mint under 11.3. Did not edit the table (stale vs live bins is the leftover). No host. No push.
<!-- THOUGHT:END -->
