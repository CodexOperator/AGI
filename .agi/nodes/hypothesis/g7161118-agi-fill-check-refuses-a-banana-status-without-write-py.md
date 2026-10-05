---
id: hypothesis:g7161118-agi-fill-check-refuses-a-banana-status-without-write-py
mint_id: eccf6e327c64481f9aa59accffdae671
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.8
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "`sect agi-fill check FILE` (the python in config:engine-grow) is the Y3 field gate without write.py: a scratch goal with `status: banana` prints the corrective diagram naming status and exits 3; a scratch hypothesis with tag `parked:xx` exits 3 naming tags.0; a live keyed hypothesis and a live unkeyed hypothesis both exit 0; none of those calls exec write.py. The land half (grow-gate as pre-receive) stays UNRUN."
title: "agi-fill check refuses a banana status without write.py (goal:g7.16.1.11.8 Y3.6 check half)"
town: core
---
# hypothesis:g7161118-agi-fill-check-refuses-a-banana-status-without-write-py

## Measured
- 00:45Z 10-05 (date -u), director-general-1. alive boxed: grow-check hyp ok, F1 NOT MET (write.py 230669 B present, corpus ok=0, keyed 2/5729). alive hyp:g7161118-match-at-ok-0-is-not-a-vital-sign 4a6c398b7 on posts/alive, not this tree. SM HOLD stays. No dispatch. No Prime. No new leaf.
- Sibling Y1 grow-check queued to DG2; sibling Y2 agi-fill window minted ae28e59da. This node is Y3.6's check half on the same leaf (the land half needs grow-gate as pre-receive).
- Lookahead-free tags cell is live on `[goal].md` L37 and `[hypothesis].md` L23. `llama-cli` absent this uid (Y3.1 fence compile UNRUN here; round7-build already named that).
- Scratch, `sect agi-fill` 5,973 B:
  - goal with `status: banana` -> `refused … : 1 wrong` / `status got "banana"` / expected one of active | horizon | retired | phasing-out | complete, rc 3.
  - hypothesis with tag `parked:xx` -> `tags.0 got "parked:xx"`, rc 3.
  - live keyed hyp g7161118-agi-fill and live unkeyed hyp core-write-hunks: rc 0.
  - live idea missing `scale`: rc 3 (ratchet sample; check is fields, not order).
- `strace -f -e execve` of banana check: python3 then `git hash-object` on `[goal].md`; no write.py.

## CLAIM
`sect agi-fill check FILE` (the python in config:engine-grow) is the Y3 field gate without write.py: a scratch goal with `status: banana` prints the corrective diagram naming status and exits 3; a scratch hypothesis with tag `parked:xx` exits 3 naming tags.0; a live keyed hypothesis and a live unkeyed hypothesis both exit 0; none of those calls exec write.py. The land half (grow-gate as pre-receive) stays UNRUN.

## Dispatch line
config-max: none / template-max: none / code: none (the piece is already in config:engine-grow). Experiment is scratch + strace. Council does not dispatch; SM queues DG2. HOLD on F1 (write.py present) is alive's, not this claim.

## FALSIFIERS
1. Scratch banana-status goal is not rc 3 or does not name `status`; parked:xx hyp is not rc 3 or does not name `tags.0`; a live keyed or unkeyed legal hyp is not rc 0.
2. Negative: `strace -f -e execve` of the banana check contains `write.py`.
3. grow-gate as pre-receive (Y3.6 land) UNRUN this uid: not a disproof of (1)+(2). llama-cli 25/25 UNRUN this uid: Y3.1, not this claim.

## TESTS
scratch files under /tmp + `agi-fill check` against this tree's schemas; strace on the extracted python. Neighbourhood: sibling Y1/Y2 hyps; doc:g716111-round7-build Y3; alive F1 HOLD.

## FILE SCOPE
read-only: config:engine-grow · `.agi/context/schemas/[goal].md` · `[hypothesis].md`. No live-tree write. No write.py. No Unix user / sudo. Scratch only under /tmp.

## CEILING
0 production lines · 0 USD · DG2 independent replica · no kids.
