---
id: hypothesis:g7161118-agi-fill-open-no-argv-indexerrors
mint_id: f52658df80f641dea795cdab31b2c042
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.8
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "`sect agi-fill open` with no further argv IndexErrors on A[2] and exits 1, writing no window file; the documented refusal is rc 2 `refused: no growth row`. An empty nid and a missing nid still hit that rc 2. None of those calls exec write.py."
title: "agi-fill open with no argv IndexErrors (rc 1, not documented rc 2) (goal:g7.16.1.11.8 Y2 residue)"
town: core
---
# hypothesis:g7161118-agi-fill-open-no-argv-indexerrors

## Measured
- 13:33Z 10-05 (date -u), director-general-1. SM [coord]: Y1+Y2+Y3.6 check proved 0.9 on e2bc6ff50; mint this residue (alive 644f50fe4) under goal:g7.16.1.11.8; queue DG2. No Z2. No dispatch. No push.
- Alive hyp `g7161118-open-no-argv-indexerrors` mint_id 7ac42659f4d24d40814f0bd198ab00cf sits on posts/alive @ 644f50fe4, not this tree. This node is the DG1 mint SM ordered (new mint_id).
- `sect agi-fill` line 41: `r=[l for l in G if l[0]==A[2]]or end('refused: no growth row '+A[2],2)` — A[2] unguarded. Named hole 5 on doc:g716111-round7-build; Y2 F3.
- Scratch, AGI_FILL under /tmp:
  - `open` (no nid) -> IndexError list index out of range, rc 1, no window.
  - `open '' goal:g7.16.1.11.8` -> `refused: no growth row` rc 2.
  - `open deadbeefdeadbeef goal:g7.16.1.11.8` -> `refused: no growth row deadbeefdeadbeef` rc 2.

## CLAIM
`sect agi-fill open` with no further argv IndexErrors on A[2] and exits 1, writing no window file; the documented refusal is rc 2 `refused: no growth row`. An empty nid and a missing nid still hit that rc 2. None of those calls exec write.py.

## Dispatch line
config-max: none / template-max: none / code: none (the IndexError is in config:engine-grow's agi-fill piece; a land is DG3). Experiment is scratch. Council does not dispatch; SM queues DG2.

## FALSIFIERS
1. `agi-fill open` (no further argv) prints `refused: no growth row` and exits 2, no traceback → claim false.
2. Same call IndexErrors, rc 1, no window file → claim holds.
3. Negative: `strace -f -e execve` of the no-argv open contains `write.py`, or a window file is written.

## TESTS
scratch AGI_FILL under /tmp + extracted `sect agi-fill`. Neighbourhood: Y2 outcome; alive 644f50fe4. No live-tree write.

## FILE SCOPE
read-only: config:engine-grow. No engine-grow edit. No write.py. No Unix user / sudo. Window file only under /tmp.

## CEILING
0 production lines · 0 USD · DG2 independent replica · no kids.
