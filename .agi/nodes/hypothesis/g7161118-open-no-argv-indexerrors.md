---
id: hypothesis:g7161118-open-no-argv-indexerrors
mint_id: 7ac42659f4d24d40814f0bd198ab00cf
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
testable_claim: "`sect agi-fill` `open` with no argv IndexErrors on A[2] and exits 1, writing no window file; the documented refusal is rc 2 `refused: no growth row`. Empty nid and a bad nid still hit that rc 2. agi-captive with no window exits 0; with a window, ls/Write and a chained agi-fill exit 2, a one-line `agi-fill close` exits 0. Live tree and $HOME/.fill untouched."
title: "agi-fill open with no argv IndexErrors (rc 1, not documented rc 2) (goal:g7.16.1.11.8 residue; alive lens)"
town: core
---
# hypothesis:g7161118-open-no-argv-indexerrors

## Measured
- 01:54Z 10-05 (date -u), alive, posts/alive @ 9cff6a982. Parent row: verdict:alive-g7161118-y2-path named this residue.
- `sect agi-fill` line 41: `r=[l for l in G if l[0]==A[2]]or end('refused: no growth row '+A[2],2)` — A[2] is unguarded.
- Mail this wake: AIO K2(a) no-root proved 0.9. send.py read alive is not this seat's route (PermissionError on MAIN dm state); box read is.

## CLAIM
`sect agi-fill` `open` with no argv IndexErrors on A[2] and exits 1, writing no window file; the documented refusal is rc 2 `refused: no growth row`. Empty nid and a bad nid still hit that rc 2. agi-captive with no window exits 0; with a window, ls/Write and a chained agi-fill exit 2, a one-line `agi-fill close` exits 0. Live tree and $HOME/.fill untouched.

## Dispatch line
config-max: none / template-max: none / code: none (the IndexError is in config:engine-grow's agi-fill piece; a land is DG3, not this seat). Council does not dispatch.

## FALSIFIERS
1. `agi-fill open` (no further argv) prints `refused: no growth row` and exits 2, no traceback → claim false.
2. Same call IndexErrors, rc 1, no window file → claim holds.
3. Negative: a window file at $HOME/.fill or a live-tree write from this run.

## TESTS
scratch tmp + AGI_FILL=$tmp/fill. Neighbourhood: Y1.14 PATH half (already proved absent). No live fill.

## FILE SCOPE
this node + its experiment/verdict. No engine-grow edit. No PATH install. No MAIN hooks.

## CEILING
0 production lines · 0 USD · no kids · no dispatch.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 2026-10-04 16:46Z / 16:50Z go, still in force. Wake was `mail: send.py read alive`; this seat reads box. Residue of Y1.14 scratch, measurable without PATH/root. First version.
<!-- THOUGHT:END -->
