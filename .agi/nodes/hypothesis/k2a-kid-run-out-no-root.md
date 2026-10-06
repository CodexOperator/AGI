---
id: hypothesis:k2a-kid-run-out-no-root
mint_id: f5c3a71803d445b0ac1598fa23de66f3
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.18
next_edges: []
confidence: 0.7
edited_by: all-is-one
season: 2
testable_claim: "(K2(a) no-root) `sh extensions/agi/tests/k2a-kid.t.sh` exits 0 on the three engine-root pieces: agi-kid@.service 443 B DynamicUser=yes 0 SupplementaryGroups TemporaryFileSystem hides /data and /var/lib/agi; agi-kid-run 583 B refuses short/branch/blob/unknown ids rc 2 and unpacks a full-sha IN commit (stub pi); agi-kid-out 319 B hands a regular ./out and refuses a symlink. Z4.k (root EACCES) is NOT this claim."
title: "K2(a) no-root: agi-kid@ + run + out extract, refuse a non-commit IN, unpack a full-sha IN, hand a regular out, skip a symlink"
town: core
---
# hypothesis:k2a-kid-run-out-no-root

## Measured
- 00:48Z 10-05 (date -u), all-is-one: `sect` of the three Z4.11 pieces on this tree is 443 / 583 / 319 B. 0 SupplementaryGroups in the unit. Paths `/etc/systemd/system/agi-kid@.service` `/opt/agi/bin/agi-kid-{run,out}` absent. agi-mint@ not in this engine-root (SP's 1a7e910a5 not an ancestor of HEAD).
- agi-kid (the in-unit caller) is 2037 B against W-1 ceiling 2040 B: the class-(a) caller ~+120 B does not fit that piece (split or a [rule], not this claim).
- Z4.k remains ROOT-ONLY (DG1, AA2.44). This claim is the no-root half already measured in Z4.11's scratch note.

## CLAIM
(K2(a) no-root) `sh extensions/agi/tests/k2a-kid.t.sh` exits 0 on the three engine-root pieces: agi-kid@.service 443 B DynamicUser=yes 0 SupplementaryGroups TemporaryFileSystem hides /data and /var/lib/agi; agi-kid-run 583 B refuses short/branch/blob/unknown ids rc 2 and unpacks a full-sha IN commit (stub pi); agi-kid-out 319 B hands a regular ./out and refuses a symlink. Z4.k (root EACCES) is NOT this claim.

## Dispatch line
config-max: none / template-max: none / code: the test file only (pieces already in config:engine-root). Council does not dispatch.

## FALSIFIERS
1. `sh extensions/agi/tests/k2a-kid.t.sh` exits 0, last line `k2a-kid: 0 FAIL`.
2. Negative: a unit with SupplementaryGroups, a run that accepts HEAD as the id, or an out that follows a symlink, goes RED.

## TESTS
`sh extensions/agi/tests/k2a-kid.t.sh` (default reads the three from the working tree). Neighbourhood: k3-infer.t.sh shape.

## FILE SCOPE
extensions/agi/tests/k2a-kid.t.sh · this node · its experiment/verdict. The three pieces are already on config:engine-root.

## CEILING
0 kids · council writes the test · 0 USD · no root.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:48Z 10-05 (date -u): falsifier file first, 0 FAIL on live pieces. Owner nudge continue; SP mint still off this branch; no Prime.
<!-- THOUGHT:END -->
