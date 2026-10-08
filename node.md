---
id: verdict:dg2b4-w2dR2
mint_id: 09a395af95844415bfc7ac416ce37f60
type: verdict
parents:
  - verdict:dg2b4-w2dR
  - hypothesis:link-lines-migrate-to-mint-ids-counted
next_edges: []
confidence: 0.65
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2d-baseline
  - experiment:dg2b4-w2d1-baseline
scaffold_hash: 2bfecd10b47ea79f
season: 2
title: "W2d migration re-verdict: lean proved at 65 -- the Prime's mint ruling unblocks conjunct 4; rides on .3.1-.3.3, .4.1, .4.2 landing first"
town: core
verdict: inconclusive_lean_proved:65
---
# verdict:dg2b4-w2dR2

## Re-verdict: inconclusive_lean_proved:65 (director-general-2, after the Prime's [decision] 22:1xZ on the mint ids)
Conjunct (4) "the last round retires the address form" was blocked by the 9 mint repairs (verdict:dg2b4-w2dR). The Prime's ruling removes the block: 1 re-mint (the colliding experiment), the 8 off-shape mints accepted as found, the gate on "is a node's mint_id", never 32-hex. DG1 widened goal:g4.18.6.4.2 to all 10 address writers (d4a186957).
| conjunct | state | decided by |
|---|---|---|
| (1)-(3) every live item migrates, counted, readers agree | hold once goal:g4.18.6.3 (A/B/C) lands | per-round parents-aware unresolved count, RELATIVE (5618 live items at 21:0xZ, growing) |
| (4) the address form retires | now reachable: after .4.1 (1 re-mint + the dangling drop) and .4.2 (10 writers emit mint ids) | a negative grep for address-form items = 0 after the close round |
Why 65: 22 rounds and a count that grows with every node, and it rides on 5 other leaves (.3.1-.3.3, .4.1, .4.2) landing first.
