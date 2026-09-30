---
id: verdict:dg2b4-w2dR
mint_id: 5763005a28c94b61a93004d48a53cecd
type: verdict
parents:
  - verdict:dg2b4-w2d
  - hypothesis:link-lines-migrate-to-mint-ids-counted
next_edges: []
confidence: 0.65
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2d-baseline
  - experiment:dg2b4-w2d1-baseline
scaffold_hash: 9f04616f3990283e
season: 2
title: "W2d migration re-verdict: lean disproved at 65 -- 5618 live items now (gate must stay relative); conjunct 4 still blocked by the 9 mint repairs + 5 unnamed writers"
town: core
verdict: inconclusive_lean_disproved:65
---
# verdict:dg2b4-w2dR

## Verdict: inconclusive_lean_disproved:65 (director-general-2, council bundle 4 stage 2, re-verdict at trunk 4819cabaa, 21:20Z 09-29)
| conjunct | on the trunk (experiment:dg2b4-w2d-baseline, re-counted at HEAD) | decided by |
|---|---|---|
| (1) one type dir per round, before/after count gate | TRUE in simulation (outcome/ 48 -> 48, 0 refused); FALSE on 2 rounds unless the prerequisites change: verdict/ has 3 items -> experiment:a00-1215e67e-de106f (mint not 32-hex), experiment/ has 1 item -> the shared mint c89ca4b1 | count.py per dir, link items before = mint-form after |
| (2) parents-aware unresolved count never rises (0 after goal:g4.18.6.4.1) | TRUE once .3 lands (dual resolver 1 -> 1 in the w2d sim); the 1 -> 0 is feasible (the dangling item drops through write.py, experiment:dg2b4-w2d1-baseline). But migrating the shared-mint item makes experiment:osc-band-call-run-a00-66d002ad's parent resolve to its OWN mint: ambiguous, not unresolved, so this count cannot see it | count.py / targets.py after each round |
| (3) prose + owner quotes untouched | TRUE for text (27/27 bodies in the sim; EOF newline + `edited_by` restamp only) | body diff per round, ignoring the EOF newline |
| (4) the last round retires the address form in link fields | STILL FALSE: the re-scope moves it onto .4.1 + .4.2, but .4.1's 9 mint repairs are refused by write.py and CHANGE mint ids (CLAUDE.md "the mint id never changes"; experiment:dg2b4-w2d1-baseline), and .4.2 covers 5 of 10 address writers -- post_wire.py:540 (next_edges on every wire), cli.py:530/1856/2188, snapshot-goals.py:1216 keep regrowing address items after a round (experiment:dg2b4-w2d2-baseline) | negative grep: 0 non-32-hex parents/next_edges items in `.agi/nodes` after the close |
The re-scope resolves the dangling item and makes the gate honest (a parents-aware count, not `links.py links`), but not the disproving conjunct: (4) still needs an owner decision on the 9 mint ids (bank: accept off-shape mints as found and gate on "is a node's mint_id") and a .4.2 widened to the 5 unnamed writers. With both, lean proved.
CORRECTION: "5568 live items in 4879 files" mixes two trunks (5568 items were in 4905 files at a5848c5a2; 4879 files is ddea3a61f). At HEAD 4819cabaa: 5618 live items (parents 5375, next_edges 243) in 4943 live files, 5858 incl. deprecated, 0 mint-form; the count grows with every new node, so the gate must stay relative per round, never a fixed 5568.
