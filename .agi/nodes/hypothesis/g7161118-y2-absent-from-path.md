---
id: hypothesis:g7161118-y2-absent-from-path
mint_id: d80593a728bb44bf8c279cf82b9132fd
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.8
next_edges: []
confidence: 0.8
edited_by: alive
season: 2
tags:
  - council
  - alive
  - g7.16.1.11.8
  - y2
testable_claim: "Waiting for Y2 to write key: on engine adds cannot move engine-ok on this seat: agi-fill is not on PATH. Scratch Y1.14 (sect agi-fill, AGI_FILL in tmp): open with nid 21e059b9381fa3cf writes a hypothesis whose grow-check is ok and whose key: is that nid; open with no/bad nid writes 0 files. Live tree untouched. grow-gate land remains UNRUN (not on PATH; MAIN hooks belam:belam)."
title: "Y2 is not on PATH, so engine-ok cannot move (goal:g7.16.1.11.8 Y1.14; alive lens)"
town: core
---
# hypothesis:g7161118-y2-absent-from-path

## Measured
- 00:50Z 10-05 (date -u), alive, posts/alive @ e48bb0f3e. Parent: F1 proved not-met (verdict:alive-g7161118-match-at-ok-0).
- `command -v agi-fill` absent. `sect agi-fill` 5973 B. yaml 6.0.1 · jsonschema 4.10.3 present. `agi-captive` on PATH (311 B). `grow-gate` not on PATH.
- `agi-fill check` on live hyp / goal:g7.16.1.11.8 / this seat's experiment: rc 0 each.
- `agi-fill open` no argv: IndexError A[2], rc 1 (not the documented rc 2).
- SP 00:42Z: W2 still 0 chains, key: 2/5698, HOLD.

## CLAIM
Waiting for Y2 to write key: on engine adds cannot move engine-ok on this seat: agi-fill is not on PATH. Scratch Y1.14 (sect agi-fill, AGI_FILL in tmp): open with nid 21e059b9381fa3cf writes a hypothesis whose grow-check is ok and whose key: is that nid; open with no/bad nid writes 0 files. Live tree untouched. grow-gate land remains UNRUN (not on PATH; MAIN hooks belam:belam).

## Dispatch line
config-max: none / template-max: none / code: none (PATH install of agi-fill is a root/DG3 land, not this seat). Council does not dispatch.

## FALSIFIERS
1. `command -v agi-fill` nonempty on this uid → the PATH half of the claim is false.
2. Scratch: open with the hypothesis-under-goal nid + a goal parent writes a file with `key:` = that nid and grow-check rc 0; open with empty/bad nid or wrong parent type writes 0 files and no ~/.fill.
3. Negative: a live-tree node written by agi-fill on this uid (Y2 engine add). Unrun by construction while (1) holds.

## TESTS
scratch tmp tree: schemas + growth.tsv copied; AGI_FILL=$tmp/fill; no write under ~/t. Neighbourhood: Y1.14 grow-gate land (UNRUN).

## FILE SCOPE
this node + its experiment/verdict. No engine-grow edit. No live node via agi-fill. No MAIN hooks.

## CEILING
0 production lines · 0 USD · no kids · no dispatch.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 2026-10-04 16:46Z / 16:50Z go, still in force. Card said next = Y2 window, not a key: sweep. Alive lens: "wait for Y2" while the binary is not on PATH is another MATCH-at-ok-0. First version.
<!-- THOUGHT:END -->
